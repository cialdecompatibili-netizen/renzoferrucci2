# -*- coding: utf-8 -*-
"""renzo_logo_apply.py - genera la FAVICON di renzoferrucci.com (rombo art deco con RF).
Scrive in renzoferrucci2: assets/images/favicon.svg, favicon-32/48/192/512.png, apple-touch-icon.png, favicon.ico (root + assets/images).

=== COLORI (cambiali solo qui sotto) ===
  ORO   #FFD43B  oro-giallo BRILLANTE, volutamente piu giallo e saturo dell'oro del sito (#8a6d3b, usato per link/menu).
                 Perche': su nero a 16 px l'oro scuro/spento si confonde, il giallo acceso resta leggibile (contrasto ~15:1).
  NERO  #0A0A0A  fondo del rombo, quasi nero puro: piu scuro = piu contrasto con l'oro.
  Fuori dal rombo: TRASPARENTE (niente quadrato), cosi il rombo occupa tutto lo spazio.

=== FONT ===
  Georgia GRASSETTO (Windows: C:\\Windows\\Fonts\\georgiab.ttf; nell'SVG font-weight 700).
  Serif con grazie = look luxury; il grassetto + un leggero contorno (STROKE) ingrossa le aste delle lettere
  perche' a 16 px le linee sottili spariscono. Solo 2 lettere (RF): piu testo = illeggibile.

=== TRUCCHI PER LEGGERSI PICCOLISSIMO (da guide favicon, applicati) ===
  1. Alto contrasto: giallo acceso su nero, solo 2 colori, niente sfumature ne' ombre.
  2. Via i dettagli sottili: tolto il rombo interno a filo; resta UN anello oro spesso + le lettere.
  3. Forma piena: il rombo tocca i 4 bordi (piu area = lettere piu grandi).
  4. Linee spesse: anello >= 7 unita' su 100 e lettere in grassetto con contorno.
  5. Disegno a grande (supersampling x8) e riduzione: i bordi restano nitidi a 16/32/48 px.
  6. Taglia 48 px inclusa: Google vuole favicon con lato multiplo di 48 (48, 96, 192...).
  7. Controllare SEMPRE la versione 16 px, non solo la grande.
  8. DUE versioni: PICCOLA (favicon.svg, favicon-32.png, favicon.ico) = rombo oro PIENO + una sola "R" nera grassa
     (con RF e anello a 16 px le lettere si fondevano in una macchia); GRANDE (48/180/192/512 px, logo nel menu)
     = rombo nero con anello oro + RF. Anteprima 16 px ingrandita: claudetemp\favicon_16_preview.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

B = r"C:\Users\mirco\Desktop\repository\renzoferrucci2"
I = os.path.join(B, "assets", "images")
ORO = "#FFD43B"
NERO = "#0A0A0A"
FONT = r"C:\Windows\Fonts\georgiab.ttf"   # Georgia grassetto
A_OUT = 49.5      # semi-diagonale rombo esterno (anello oro); 50 = bordo immagine
A_IN = 42.0       # semi-diagonale rombo interno nero -> spessore anello = A_OUT - A_IN
FS = 38           # corpo lettere (unita' su 100)
STROKE = 0.9      # contorno oro sulle lettere = piu peso a piccole dimensioni
TY = 51.5         # altezza del centro delle lettere

def rombo(a):
    return "50,%s %s,50 50,%s %s,50" % (50 - a, 50 + a, 50 + a, 50 - a)
SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
       '<polygon points="%s" fill="%s"/><polygon points="%s" fill="%s"/>'
       '<text x="50" y="%s" text-anchor="middle" dominant-baseline="central" '
       'font-family="Georgia,\'Times New Roman\',serif" font-weight="700" font-size="%s" '
       'fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round">RF</text></svg>'
       ) % (rombo(A_OUT), ORO, rombo(A_IN), NERO, TY, FS, ORO, ORO, STROKE)
open(os.path.join(I, "favicon.svg"), "w", encoding="utf-8", newline="\n").write(SVG)

def mk(n):
    s = 8; N = n * s; k = N / 100
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def rh(a, c):
        d.polygon([(50*k, (50-a)*k), ((50+a)*k, 50*k), (50*k, (50+a)*k), ((50-a)*k, 50*k)], fill=c)
    rh(A_OUT, ORO); rh(A_IN, NERO)
    f = ImageFont.truetype(FONT, int(FS*k))
    d.text((50*k, TY*k), "RF", font=f, fill=ORO, anchor="mm", stroke_width=max(1, int(STROKE*k/2)), stroke_fill=ORO)
    return im.resize((n, n), Image.LANCZOS)

def mk_small(n):
    """Versione PICCOLA (16/32 px e SVG): rombo oro PIENO + una sola R nera grassa. Zero dettagli = massimo contrasto."""
    s = 8; N = n * s; k = N / 100
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(50*k, 0.5*k), (99.5*k, 50*k), (50*k, 99.5*k), (0.5*k, 50*k)], fill=ORO)
    f = ImageFont.truetype(FONT, int(60*k))
    d.text((50*k, 52*k), "R", font=f, fill=NERO, anchor="mm", stroke_width=max(1, int(1.2*k/2)), stroke_fill=NERO)
    return im.resize((n, n), Image.LANCZOS)

# SVG (usato da Chrome nella scheda): versione piccola semplice
SVG_SMALL = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><polygon points="%s" fill="%s"/>'
             '<text x="50" y="52" text-anchor="middle" dominant-baseline="central" font-family="Georgia,\'Times New Roman\',serif" '
             'font-weight="700" font-size="60" fill="%s" stroke="%s" stroke-width="1.2" stroke-linejoin="round">R</text></svg>'
             ) % (rombo(49.5), ORO, NERO, NERO)
open(os.path.join(I, "favicon.svg"), "w", encoding="utf-8", newline="\n").write(SVG_SMALL)
# versione grande con anello e RF: tenuta in favicon-detail.svg (non collegata)
open(os.path.join(I, "favicon-detail.svg"), "w", encoding="utf-8", newline="\n").write(SVG)

mk_small(32).save(os.path.join(I, "favicon-32.png"))
for n, name in [(48, "favicon-48.png"), (180, "apple-touch-icon.png"), (192, "favicon-192.png"), (512, "favicon-512.png")]:
    mk(n).save(os.path.join(I, name))
for p in (os.path.join(B, "favicon.ico"), os.path.join(I, "favicon.ico")):
    mk_small(256).save(p, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
mk_small(16).resize((128, 128), Image.NEAREST).save(r"C:\Users\mirco\Desktop\claudetemp\favicon_16_preview.png")
print("ok")

