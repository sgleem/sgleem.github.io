---
layout: page
title: Writing
permalink: /writing/
description: Research essays, engineering notes, paper notes, and personal essays.
---

<p class="page-lede">Research essays, engineering notes, paper notes, and personal essays on playing with intelligent systems.</p>

<nav class="category-filter" aria-label="Writing categories">
  <a href="{{ site.baseurl }}/writing/">All writing</a>
  {% for category in site.content_categories %}
    <a href="{{ site.baseurl }}/categories/#{{ category | slugify }}">{{ category }}</a>
  {% endfor %}
</nav>

{% if site.posts.size > 0 %}
  <div class="post-list">
    {% for post in site.posts %}
      {% include post-card.html post=post %}
    {% endfor %}
  </div>
{% else %}
  <p class="empty-state">Writing will appear here as essays and notes are published.</p>
{% endif %}
