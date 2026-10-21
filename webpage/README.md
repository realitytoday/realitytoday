# Reality Today – website

Static, bilingual (EN/DE) site for <https://realitytoday.github.io>, served by GitHub Pages.

- `content/` – Markdown sources of the guides (`<project>.en.md`, `<project>.de.md`)
- `tools/build.py` – builds the HTML pages from the content (`pip install markdown`, then `python tools/build.py`)
- `assets/` – CSS, logo, favicon, screenshots
- `.nojekyll` – serve files as they are

Generated HTML is committed, so the deploy workflow (`../.github/workflows/pages.yml`) just publishes this folder.
Run `python tools/build.py` after editing content or the templates in `build.py`.

Preview locally: `python -m http.server -d webpage 8000`
