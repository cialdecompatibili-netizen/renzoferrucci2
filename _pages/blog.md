---
ref: blog
layout: single
title: Journal
permalink: /blog/
author_profile: false
classes: wide
share: false
---
{%- assign posts_l = site.posts | where: "lang", page.lang -%}
{%- include blog-lista.html -%}
