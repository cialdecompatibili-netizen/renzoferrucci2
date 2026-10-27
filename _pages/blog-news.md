---
layout: single
title: "News"
author_profile: false
classes: wide
share: false
ref: blog-news
permalink: /blog/news/
---
{%- assign posts_l = site.posts | where: "lang", page.lang | where_exp: "p", "p.categories contains 'news'" -%}
{%- include blog-lista.html cat="news" -%}
