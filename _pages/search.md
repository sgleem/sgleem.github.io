---
layout: page
title: Search
permalink: /search/
description: Search all writing on SG's Log.
---

<div id="search-container">
    <label for="search-input">Search writing</label>
    <input type="search" id="search-input" placeholder="Search titles, tags, and full text" autocomplete="off">
    <p id="search-status" class="muted" role="status">Search across titles, descriptions, categories, tags, and article text.</p>
    <ul id="results-container"></ul>
</div>

<script src="{{ site.baseurl }}/assets/simple-jekyll-search.min.js" type="text/javascript"></script>

<script>
  var searchInput = document.getElementById('search-input');
  var searchStatus = document.getElementById('search-status');

  SimpleJekyllSearch({
    searchInput: searchInput,
    resultsContainer: document.getElementById('results-container'),
    searchResultTemplate: '<li class="search-result"><a href="{url}"><strong>{title}</strong><span>{category} · {date}</span><p>{description}</p></a></li>',
    noResultsText: 'No matching writing found.',
    json: '{{ site.baseurl }}/search.json'
  });

  searchInput.addEventListener('input', function () {
    searchStatus.textContent = this.value ? 'Matching writing:' : 'Search across titles, descriptions, categories, tags, and article text.';
  });
</script>