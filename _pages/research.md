---
layout: page
title: Research
permalink: /research/
description: Research themes, projects, and writing by Seong-Gyun Leem.
---

<section class="page-section">
  <h2>Research philosophy</h2>
  <p>I care about research that makes intelligent systems more useful, measurable, and dependable in the settings where people actually use them.</p>
</section>

<section class="page-section">
  <h2>Current areas</h2>
  <div class="research-grid">
    {% for area in site.data.research_areas %}
      <article id="{{ area.name | slugify }}" class="research-area">
        <h3>{{ area.name }}</h3>
        <p>{{ area.description }}</p>
      </article>
    {% endfor %}
  </div>
</section>

<section class="page-section">
  <h2>Selected writing</h2>
  {% assign research_posts = site.posts | where_exp: "post", "post.categories contains 'research'" %}
  {% if research_posts.size > 0 %}
    <div class="post-list">
      {% for post in research_posts limit: 5 %}
        {% include post-card.html post=post %}
      {% endfor %}
    </div>
  {% else %}
    <p class="empty-state">Research essays and project notes will be collected here.</p>
  {% endif %}
</section>

<section class="page-section">
  <h2>From speech to agents</h2>
  <p>This space will connect earlier work in speech and multimodal systems with current questions about agents, evaluation, and real-world machine learning.</p>
</section>
