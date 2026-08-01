# SG's Log

The personal research and writing site of Seong-Gyun Leem. It is a text-first Jekyll site for research essays, engineering notes, paper notes, and personal essays.

## Local development

This site targets GitHub Pages and uses the `github-pages` gem.

```bash
bundle install
bundle exec jekyll serve
```

Open <http://localhost:4000> to preview the site. To perform a one-time production build, run:

```bash
bundle exec jekyll build
```

## Adding a post

Create a dated Markdown file in `_posts/` using the schema in [`docs/post-template.md`](docs/post-template.md). Use one controlled category:

- `research`
- `engineering`
- `paper-notes`
- `personal`

Use tags for narrower topics. Set `featured: true` for essays that should appear in the homepage feature section. Set `math: true` only on posts that contain MathJax expressions.

## Site content

- `_data/profile.yml` stores the short profile and external links.
- `_data/publications.yml` stores structured publication records.
- `_data/navigation.yml` controls the global navigation.
- `_pages/` contains the durable Writing, Publications, About, Archive, Categories, and Search pages.

The site keeps the default GitHub Pages build path and does not require a JavaScript framework or a database.
