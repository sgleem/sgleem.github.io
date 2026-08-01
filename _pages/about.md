---
layout: page
title: About
permalink: /about/
description: About Seong-Gyun Leem.
---

<p class="page-lede">{{ site.data.profile.role }}</p>

<p>I write about the technical and human questions that arise while leveraging intelligent systems to change our lives, alongside personal reflections on living in the era of AI agents. My interests include model evaluation, real-world data, speech and multimodal systems, AI literacy and education, and AI governance. </p>

<p>This site is a place for durable research essays, practical notes, paper discussions, and personal essays. Detailed publication history can be found in the <a href="{{ site.baseurl }}/publications/">publication archive</a>.</p>

## Elsewhere

<ul class="link-list">
  {% assign links = site.data.profile.links %}
  {% if links.github %}<li><a href="{{ links.github }}">GitHub</a></li>{% endif %}
  {% if links.google_scholar %}<li><a href="{{ links.google_scholar }}">Google Scholar</a></li>{% endif %}
  {% if links.linkedin %}<li><a href="{{ links.linkedin }}">LinkedIn</a></li>{% endif %}
  {% if links.cv %}<li><a href="{{ links.cv }}">CV</a></li>{% endif %}
  {% if links.email %}<li><a href="mailto:{{ links.email }}">Email</a></li>{% endif %}
</ul>
