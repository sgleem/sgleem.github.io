---
layout: page
permalink: /archive/
title: Archive
---

<p class="page-lede">A chronological index of research, engineering, paper, and personal writing.</p>

<p class="category-summary">
  Categories:
  {% for category in site.content_categories %}
    <a href="{{ site.baseurl }}/categories/#{{ category | slugify }}">{{ category }}</a>{% unless forloop.last %}, {% endunless %}
  {% endfor %}
</p>

{% if site.posts.size > 0 %}
  {% assign previous_year = "" %}
  {% for post in site.posts %}
    {% assign year = post.date | date: "%Y" %}
    {% if year != previous_year %}
      {% if previous_year != "" %}</div></section>{% endif %}
      <section class="archive-year">
        <h2>{{ year }}</h2>
        <div class="archive-list">
      {% assign previous_year = year %}
    {% endif %}
    {% assign category = post.category %}
    {% unless category %}{% assign category = post.categories | first %}{% endunless %}
    <p>
      <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
      <span class="archive-meta">{{ post.date | date: "%B %-d" }}{% if category %} · {{ category }}{% endif %}</span>
    </p>
    {% if forloop.last %}</div></section>{% endif %}
  {% endfor %}
{% else %}
  <p class="empty-state">Published writing will appear in the archive.</p>
{% endif %}
