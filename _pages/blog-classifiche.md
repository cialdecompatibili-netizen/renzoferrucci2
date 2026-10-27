---
layout: single
title: "Classifiche"
author_profile: false
classes: wide
share: false
ref: blog-classifiche
permalink: /blog/classifiche/
---
{%- assign posts_l = site.posts | where: "lang", page.lang | where_exp: "p", "p.categories contains 'classifiche'" -%}
{%- include blog-lista.html cat="classifiche" -%}
