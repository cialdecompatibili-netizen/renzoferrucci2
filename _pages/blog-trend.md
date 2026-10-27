---
layout: single
title: "Trend"
author_profile: false
classes: wide
share: false
ref: blog-trend
permalink: /blog/trend/
---
{%- assign posts_l = site.posts | where: "lang", page.lang | where_exp: "p", "p.categories contains 'trend'" -%}
{%- include blog-lista.html cat="trend" -%}
