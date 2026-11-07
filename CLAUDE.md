# mistraltemplate1 - guida per Claude (template Jekyll adattivo)

Template Jekyll per GitHub Pages: si clona, si cambia quasi solo `_config.yml` e il sito si adatta (lingua, URL, brand, menu, shop). Obiettivo e stato del lavoro: `PROGETTO_TEMPLATE.md`.

**CREARE UN SITO DA QUESTO TEMPLATE: leggi PRIMA `docs/CLONAZIONE.md` (un comando `nuovo_sito.ps1` + `personalizza_clone.py` fanno colori, logo, sfondo home; un solo commit). Ogni automazione che impari va scritta come script in `automation/` e annotata li' (regola nella sezione 5): obiettivo meno tempo e meno commit per ogni nuovo sito.**

## Prima di toccare un clone (checklist)
1. `_config.yml`: `brand`, `description`, `default_lang`, `languages`, `whatsapp`, `contact_endpoint`, `ecommerce`. NON scrivere `url:`/`baseurl:` (li imposta GitHub Pages).
2. Menu: `_data/navigation.yml` (voci) + `_data/sottomenu.yml` (tendine, chiave = title identico). Url interni SENZA nome repo.
3. Home a blocchi: `_data/blocks_home.json` (campi id, nome, enabled, html). Modificare solo `html`, mai la struttura. Backup prima, rileggere il JSON dopo.
4. Colori/tema: `_data/tema.json`; kit blocchi in `assets/css/gaming.css` (nome storico, non rinominare; accento = `--gc-acc`).
5. Shop: `ecommerce: true` accende tutto. Dati in `_data/catalogo.json` (prezzi in centesimi) + una pagina per prodotto/categoria in `_negozio/` (esempi inclusi: `prodotto-esempio.md`, `categoria-esempio.md`).
6. Contenuti: `_pages/`, `_posts/`. Ogni pagina/articolo ha `ref:` (chiave di collegamento tra lingue).

## Regole d'oro
- ZERO valori fissi: niente nome repo, utente, dominio, telefono scritti nei layout/include/JS. Si usa `relative_url`, `site.*`, `_includes/site-name.html`.
- Admin (`admin/index.html`): `detectRepo()` ricava utente/repo dall'URL. Su dominio personalizzato chiede il repo una volta (localStorage `cms_repo`). Non hardcodarlo.
- `automation/publish.py`: percorso e URL ricavati da soli (cartella del file + remote git).
- Valore vuoto in config = funzione spenta, mai errore: i layout controllano che il campo sia pieno.
- Nessun plugin fuori da GitHub Pages. Build locale non disponibile su questo PC: si controlla online dopo il deploy.
- COMMENTARE i punti critici (layout, include, JS, CSS, config): dire cosa fa, cosa legge, cosa NON toccare.

## Multilingua (dettagli in `docs/MULTILINGUA.md`)
IT alla radice, altre lingue in `/xx/` create da admin > Lingue. Cambiare solo `default_lang` e `languages`. Traduzioni: `tr: copia|tradotto|da_aggiornare`, `tr_hash`; `automation/traduzioni_sync.py` + workflow marcano `da_aggiornare`. In Liquid niente `a contains b == false`: usare `{% if a contains b %}{% continue %}{% endif %}`.
**Lingue = cartelle (rilevamento automatico).** Clonare/rinominare una cartella `xx/` basta: `_includes/lingue-attive.html` la mette nel selettore (bandiera), `admin/js/lingue.js` (`lgDetect` + `lgNormalizza`, una volta per sessione aprendo admin > Lingue) la registra in `_config.yml` (languages + defaults), `_data/languages.yml`, `ui-text.yml` e corregge `lang`/`locale`/`permalink` dei file e gli url in `_data/i18n/xx/`; `traduzioni_sync.py` la vede da solo. La cartella e' la fonte di verita': il campo `lang:` dei file dopo un clone e' vecchio.
**Admin con lingua di lavoro** (`admin/js/lingua-admin.js`): selettore lingua nella barra in alto; Articoli, Pagine, Home e Menu usano gli STESSI editor ma leggono/scrivono `xx/_posts`, `xx/*.md`, `_data/i18n/xx/*`. Intercetta `window.fetch` e rimappa i path solo se lingua != base e sezione attiva in Articoli/Pagine/Menu; se il file lingua manca parte dalla copia della base (menu con url `/xx/`). Al salvataggio sistema il front matter (lang, locale, permalink, ref, `tr: tradotto` + `tr_hash`). NON riscrivere i path dentro index.html: aggiungere nuovi file da mappare in `mappa()`. `admin/js/core.js` e `articoli.js` NON sono caricati da index.html (legacy): la logica vera e' nello script inline di index.html.

## Eta' e date
MAI a mano: `<span data-eta="AAAA-MM-GG">N</span> anni`, `<span data-anni-da="AAAA">N</span> anni` (script in `_includes/footer/custom.html`).

## Design
MAI bordi laterali colorati su box, citazioni, avvisi, CTA. Box puliti con sfondo leggero o bordo uniforme.

## Pubblicare e lavorare
- Pubblicare con `..\pubblica.ps1` con `-Files` espliciti. Dopo il push NON aspettare la build: Mirco verifica da solo.
- Sessione interrotta: prima `read_file` e `git status --short`; spesso manca solo commit e push.
- PowerShell lungo: salvare in .ps1 e lanciare con `-NoProfile -ExecutionPolicy Bypass -File`. Mai chiamare funzioni RD/WR/CD/LS (alias: RD cancella!).
- Traduzioni: NIENTE GitHub Actions. L'hook `.githooks/pre-commit` lancia `automation/traduzioni_sync.py` a ogni commit (attivo con `git config core.hooksPath .githooks`, una volta per clone).
- Risposte brevissime, modifiche in una sola chiamata.

## Cose che funzionano
- Test senza build locale: simulare la logica JS dell'admin con node + `vm` (stub di `lgText`/`lgCommit` e albero finto) e lanciare `node --check` sul file. Esempio: `claudetemp\test_lingue.js` (clone en -> de rinominato).
- Rilevare le lingue dalle CARTELLE (non dal config) e normalizzare tutto il resto da li': evita config e cartelle fuori sync.
- Liquid senza plugin: costruire un array con `split` + `concat` + `uniq` dentro un include che fa solo `assign` (le variabili restano visibili a chi lo include).- Patch su file grandi con CRLF (admin/index.html): script node con `readFileSync`/`replace`/`writeFileSync` su stringhe esatte, mai edit multiriga a mano; poi `node --check` sui .js. Mock del wrapper fetch: `claudetemp\test_lingua_admin.js`.

SEO e lingue (24/10/2026)
- SEO per lingua: _includes/seo.html fa un solo meta robots (noindex se noindex:true o tr: copia), description per lingua da _data/languages.yml (chiave description; se manca NON la scrive), og:locale. hreflang in _includes/head/custom.html: solo versioni tradotte (stesso ref), x-default = lingua base. sitemap.xml propria (sostituisce jekyll-sitemap) con alternates hreflang, esclude noindex/copia/admin/404.
- Slug tradotti: lo slug e' il permalink del front matter; MAI scrivere a mano lo slug di un'altra lingua nei link: usare {% include url-ref.html ref="shop-negozio" %} (URL per ref nella lingua della pagina). Inglese: /en/shop/, /en/about-us/, /en/contact/, /en/category/, /en/shop/example-product/. carrello/ordine/grazie restano con slug italiano (noindex, e carrello.js controlla /grazie/). Una lingua clonata da admin parte con gli slug della base: tradurli cambiando permalink (e i link in menu/home).
- Lingua browser: script in head/custom.html. Solo prima visita, solo da pagine in lingua base, solo se esiste la versione tradotta; localStorage lang_pref = scelta ricordata (il click su bandiera/selettore la aggiorna); niente redirect per bot, ?nolang=1 o referrer dello stesso sito.


Elementi per pagina (24/10/2026)
- UN solo valore per tutte le liste: `per_page` in _config.yml (default 20), si cambia da admin > Impostazioni (10, 20, 50, 100, 200, 500). L'admin lo copia in localStorage 'cms_per_page' (getPerPage in admin/index.html); NON reintrodurre limiti separati per elenco.
- Admin: elenchi Articoli, Pagine e Prodotti usano getPerPage(); le miniature/metadati si leggono a gruppi di 6 (metaQueue in wp-elenchi.js) per non finire il limite API con 200-500 voci.
- Sito: assets/js/paginazione.js impagina blog, negozio e pagina categoria (it e en) con gli attributi data-pg, data-pg-item, data-per sul contenitore; le voci restano tutte nell'HTML. Filtri che usano hidden (pillole negozio) chiamano PgLista.refresh. Se aggiungi un nuovo elenco lungo: stessi tre attributi, niente codice nuovo.


Lezioni dal clone "cybersecurity" (24/10/2026)
- Home, Chi siamo e Servizi sono a blocchi con testi SEGNAPOSTO neutri (IT in `_data/`, EN in `_data/i18n/en/`). Stile `ent-*` in `assets/css/gaming.css`; i colori seguono `_data/tema.json` (accent = `--gc-acc`, accent_dark = `--gc-ink`): NON mettere `<style>` con colori nei blocchi.
- I JSON dei blocchi si generano con uno script node (JSON.stringify + rilettura con JSON.parse), mai a mano; apostrofi e accenti nei blocchi come entita' HTML (&#39; &egrave;).
- Dopo aver scritto/tradotto a mano le pagine di una lingua: `python automation/allinea_hash.py en` (imposta `tr: tradotto` e `tr_hash`). Senza, l'hook le marca `da_aggiornare`.
- Ogni pagina/articolo ha `ref:` anche in italiano (serve al collegamento tra lingue e al selettore).
- Dati, cifre e fonti nei testi: solo verificati sul web (cerca prima). Mai loghi clienti, recensioni, certificazioni o prezzi inventati.
- Il modulo contatti resta spento finche' `contact_endpoint` e' vuoto: chiederlo subito al cliente. Lo stesso per `whatsapp` ed `email`.
- Clone: `..\nuovo_sito.ps1` tiene `en/` di default (it,en). Con `-Lingue it` la cartella `en/` viene tolta: farlo solo se richiesto. `-Accento "#rrggbb"` imposta il colore.
- Pubblicare piu' file: `& ..\pubblica.ps1 -Repo x -Msg "..." -Files 'a','b'` (ora accetta anche `-Files a,b` da `-File`).


Lezioni dalla migrazione "pelletteria" -> "pelletteria2" (24/10/2026)
- Migrare un sito esistente in un clone: 1) mappare le due repo (menu, `_data/catalogo.json`, `_negozio/`, `blocks_home.json`, `_posts/`); 2) generare TUTTO con script node (accenti come `\uXXXX`, nei blocchi HTML entita' numeriche con una funzione `ent()`; JSON con `JSON.stringify` e rilettura); 3) `python automation/allinea_hash.py en`; 4) pubblicare con `..\pubblica.ps1 -Files ...`. Script di esempio: `claudetemp\build_pelletteria2\` (`dati.js` = categorie IT/EN, `build.js` = dati/menu, `build2.js` = blocchi/pagine/patch).
- Categorie a DUE LIVELLI: campo `genitore` in `catalogo.json` (il reparto non ha genitore; la sua pagina mostra le sottocategorie e i prodotti di tutte). Nome inglese in `tr.en.nome`. Ogni categoria ha DUE file con `ref: shop-cat-<id>`: `_negozio/categoria-<id>.md` (permalink `/negozio/categoria/<id>/`) e `en/negozio/categoria/<id>.md` (permalink `/en/shop/category/<slug-inglese>/`).
- Link dello shop: MAI `nz_lh | append: 'negozio/'` (in inglese puntava a `/en/negozio/`, che non esiste). Usare `{% include shop-url.html k="shop" %}`, `k="cat" id=...`, `k="prod" id=...`: cerca il `ref` (`shop-negozio`, `shop-cat-<id>`, `shop-prod-<id>`) nella lingua della pagina, poi nella base, poi la vecchia formula. Prodotti/categorie creati da admin senza `ref` in inglese ricadono sulla formula: aggiungere il `ref` a mano ai file.
- Il clone con `nuovo_sito.ps1 -File` storpia le virgole (`default_lang: it,en`) e CANCELLA `en/` e `_data/i18n/en`: dopo il clone controllare `default_lang` e che `en/` esista, altrimenti ripristinare dal template.
- Non portare nei blocchi i `<style>` del vecchio sito: si usano le classi `gc-*`/`ent-*` e `_data/tema.json` (copiare il tema.json del vecchio sito per mantenere i colori).
- Togliere i segnaposto che non servono (`_pages/servizi.md`, articolo di esempio, categoria/prodotto di esempio): restano online e indicizzati.
- Il modulo contatti resta spento senza `contact_endpoint` (il vecchio sito usava il worker del modello: non riusarlo, serve il worker del cliente).
- Questo template ha molti file non committati: le modifiche shop (shop-url.html, negozio-categoria, patch ai link) sono nel working tree ma NON committate; non usare `pubblica.ps1 -Tutto` qui.

## Lezioni dal clone pelletteria2 (24/10/2026)
- FOOTER: _includes/footer/custom.html mette di default © anno nome-sito - Design, Development & Digital Marketing by webtomars.it; site.footer_text nel _config.yml lo sovrascrive. Nei cloni non serve rifarlo.
- TEMA/COLORI: mai hex hardcoded (niente azzurri/teal/ghiaccio in menu.css, gaming.css, head/custom.html, layout): usare _data/tema.json (accent, accent_dark). Dopo il clone: cercare con grep i vecchi colori e sostituirli con la palette del nuovo sito.
- HOME: sfondo hero = assets/images/*-hero.jpg referenziato in gaming.css (.ent-hero). Nei cloni sostituirlo con una texture a tema (esempio: automation/genera_texture.py di pelletteria2, Pillow+numpy) e cambiare logo con automation/genera_logo.py.
- ORDINE CLONE: 1) tema.json 2) logo+texture 3) menu/categorie IT+EN 4) home/chi siamo 5) footer e segnaposto 6) commit+push+verifica online.

## Rivendita Etsy -> shop (07/11/2026) - UN comando
Sito online: https://renzoferrucci.com (prodotti in /negozio/<id>/). Il codice sta fuori dal repo, in `Desktop\libreria_comune` (come le DLL): non copiarlo qui.
- Comando: `Desktop\rivendita etsy\pubblica.bat --repo renzoferrucci2 --link <url etsy> --acquisto <euro> --taglia <x|-> --colore <x|-> [--dry-run] [--no-push]`. Fa: scarica annuncio, foto lusso Gemini (sfondo bianco), prezzo, descrizione, commit+push, stampa URL. Prima prova SEMPRE con `--dry-run` (zero crediti Gemini).
- Se l'annuncio ha taglie/colori e non li passi si ferma e li elenca: MAI indovinare una variante (prezzo/misure/colori dell'annuncio cambiano per variante). Chiedere a Mirco quale compra.
- Prezzo = triplo dell'acquisto, stile LUSSO: euro interi tondi, mai ,90/,99 (fino a 100 multipli di 5, 100-500 di 10, 500-2000 di 50, oltre di 100). Funzione `comune.prezzo.vendita`.
- Foto default = versione lusso con sfondo bianco #FFFFFF. Descrizione solo da dati reali dell'annuncio (`etsy.dettaglio`), in italiano; EN a mano.
- Scheda prodotto: tolta la scritta "Prodotto fisico" (`_layouts/negozio-prodotto.html`, resta solo "Prodotto digitale").
- Rimuovere un prodotto: `shop_jekyll.rimuovi(r"C:\...\renzoferrucci2", pid)` (percorso ASSOLUTO: con "." cerca in Desktop\repository e fallisce).
- Catalogo oggi: 16 prodotti. Borsa: id `borsa-test-b` (370 EUR, foto B lusso; l'id resta cosi' per non rompere l'URL). APERTO: Mirco deve dire taglia e colore della borsa per mettere misure e ricalcolare il prezzo (acquisto 121,01 = minimo, il massimo dell'annuncio e' 186,55).
- Dettagli di tutti i moduli e regole: `Desktop\libreria_comune\CLAUDE.md`.

- 07/11/2026 sera: la variante e' scelta dal PREZZO. Select Etsy 'variation-selector-1' = taglie con prezzo (Mini 26x9x17 = 121,01; Medio 33x10x20 = 158,34; Grande 39x11x24 = 186,55). Borsa sul sito = Mini, misure gia' nella descrizione IT+EN.
- FUTURO (non ora): scrapare anche le varianti COLORE (variation-selector-0: Nero Argento, Oro nero, Borgogna Argento, Borgogna Oro, Caffe Argento) e proporle tutte come varianti sul sito. Per ora solo MISURE della variante della foto di default.


- 07/11/2026 notte, VARIANTI + CATEGORIE (automatici in rivendita.py):
  * Varianti: se l'annuncio Etsy ha menu taglie/colori e NON passi --taglia/--colore, pubblica TUTTE le combinazioni (comune/varianti.py: legge i select Etsy, prezzo per misura = vendita(prezzo Etsy), catalogo.json > prodotti[].varianti, id carrello = pid__combinazione). Con --taglia/--colore pubblica come prima (variante singola). Layout: _layouts/negozio-prodotto.html (menu), _includes/negozio-riga.html (elenco: 'Scegli le opzioni'), _includes/masthead.html (voci carrello). Foto: una sola (quella di default); foto per colore = futuro (campo immagine nelle combinazioni, non ancora usato).
  * Categorie: comune/categorie.py sceglie Reparto > Sottocategoria dal testo (es. Donna > Borse a tracolla in pelle, id borse-a-tracolla-in-pelle), la crea con pagine IT+EN se manca. Reparto uomo/donna dal testo (default donna); il titolo categoria include il reparto (es. "Borse a tracolla in pelle donna" / "... uomo"), id donna senza suffisso, id uomo con suffisso -uomo. --categoria <id> la forza. Regole nuove tipi prodotto: REGOLE in categorie.py.
  * Provare senza pubblicare: python rivendita.py --repo <repo> --link <url> --acquisto <prezzo> --dry-run

- 07/11/2026 notte, FASI FOTO (rivendita.py --fase, token Gemini a gradini; ~17 crediti per foto, cache: mai rigenera se il file esiste):
  * --fase 1 (default): prodotto con foto ORIGINALE dell'annuncio, nessun credito. Tutte le varianti (misure x colori), categoria automatica.
  * --fase 2: stessa cosa ma foto LUSSO con Gemini (sfondo bianco). Si puo' rilanciare sullo stesso prodotto: aggiorna foto e testi, conserva varianti e foto colori. Se Gemini non risponde / crediti finiti: pubblica comunque con la foto originale e lo scrive (rilancia --fase 2 piu' tardi).
  * --fase 3: come la 2 + foto per ogni COLORE con Gemini partendo dalla foto lusso (il primo colore = foto di default, gli altri vengono ricolorati). --colori borgogna,caffe per farne solo alcuni (es. a crediti scarsi). La foto cambia scegliendo il colore sulla scheda e nel carrello.
  * Esempio: python rivendita.py --repo renzoferrucci2 --link <url etsy> --acquisto 121.01 --fase 1   (poi --fase 2, poi --fase 3 quando hai crediti)
  * Codice: libreria_comune\rivendita.py + comune\gemini_foto.py (modo colore), comune\varianti.py (foto_colori, descrivi), comune\categorie.py. Layout foto-colore: _layouts\negozio-prodotto.html, _includes\masthead.html.

- 07/11/2026 notte, PROVA GENERALE 2: portapassaporto (CotswoldWears, annuncio 1863311721) pubblicato in fase 1 (foto originale), acquisto 42,78 -> vendita 130 EUR, categoria Piccola pelletteria donna. Commit 969f7e8. Fix: la foto non si trovava perche' Etsy usa la chiave JSON-LD "contentURL" (non "contentUrl"), corretto in libreria_comune\rivendita.py. Lezioni: (1) il prezzo d'acquisto va preso dall'annuncio (ld offers), non da risultati di ricerca simili; (2) annuncio non disponibile = pagina "Questo articolo non e' disponibile": fermarsi, e cancellare la cache ricerche\dettaglio_<id>.json; (3) APERTO: se l'annuncio non ha sezioni (CARATTERISTICHE/TAGLIE) la descrizione sul sito e' solo il titolo -> da migliorare.

- 07/11/2026 notte, STABILIZZATO rivendita.py (1 comando, poche chiamate): (1) --acquisto ora OPZIONALE: se manca legge il prezzo dall'annuncio; (2) annuncio non disponibile/pagina bloccata -> si ferma, non pubblica e cancella la cache dettaglio; (3) descrizione di ripiego se l'annuncio non ha sezioni: punti elenco dell'annuncio (senza doppioni ne' righe sui colori), altrimenti le prime 3 frasi; (4) rilanciare lo stesso comando AGGIORNA il prodotto, non lo duplica (verificato: 17 prodotti). Flusso minimo: python rivendita.py --repo renzoferrucci2 --link <url> --fase 1 [--dry-run prima]. Commit 21963e7.

- 07/11/2026 notte, NOMI STILE LUSSO (rivendita.py > nome_lusso, automatico; --nome lo forza): nome = 'Tipo prodotto [dettaglio] in pelle', max 5 parole. Regole: primo segmento prima di / | , ; : - ; via SEO (personalizzato, fatto/xxx a mano, artigianale, premium, regalo per..., di alta qualita'), via il genere (uomo/donna: sta nella categoria), taglio alla prima ' e ', 'vera pelle' -> 'in pelle'. Esempi: 'Portapassaporto in pelle', 'Borsa shopper grande in pelle', 'Portafoglio bifold in pelle'. Per nuove regole: modifica nome_lusso. Portapassaporto ora su /negozio/portapassaporto-in-pelle/ (vecchio indirizzo rimosso), commit 97b9446.
