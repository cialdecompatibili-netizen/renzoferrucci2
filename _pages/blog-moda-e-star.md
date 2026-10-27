---
layout: single
title: "Moda e star"
author_profile: false
classes: wide
share: false
ref: blog-moda-e-star
permalink: /blog/moda-e-star/
---
{%- assign posts_l = site.posts | where: "lang", page.lang | where_exp: "p", "p.categories contains 'moda-e-star'" -%}
{%- include blog-lista.html cat="moda-e-star" -%}
