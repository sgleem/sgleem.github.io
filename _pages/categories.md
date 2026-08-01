---
layout: page
permalink: /categories/
title: Categories
---

<p class="page-lede">Browse writing by its four controlled categories.</p>

<div class="category-list">
{% for category_name in site.content_categories %}
  <section id="{{ category_name | slugify }}" class="category-group">
    <h2>{{ category_name }}</h2>
    {% assign category_posts = site.categories[category_name] %}
    {% if category_posts.size > 0 %}
      {% for post in category_posts %}
        {% include post-card.html post=post compact=true %}
      {% endfor %}
    {% else %}
        <p class="muted">No writing in this category yet.</p>
      {% endif %}
    </section>
{% endfor %}
</div>