---
layout: page
title: Publications
permalink: /publications/
description: Selected publications by Seong-Gyun Leem.
---

<p class="page-lede">A structured record of research publications, with links to papers, code, and project pages.</p>

{% assign publications = site.data.publications | sort: "year" | reverse %}
{% if publications.size > 0 %}
{% assign previous_year = "" %}
{% for publication in publications %}
{% if publication.year != previous_year %}
{% if previous_year != "" %}</div></section>{% endif %}
<section class="publication-year">
<h2>{{ publication.year }}</h2>
<div class="publication-list">
{% assign previous_year = publication.year %}
{% endif %}
{% include publication-item.html publication=publication %}
{% if forloop.last %}</div></section>{% endif %}
{% endfor %}
{% else %}
<p class="empty-state">Publication records will be added here.</p>
{% endif %}
