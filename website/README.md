# Website

The documentation is also published as a small static website (MkDocs with the Material theme). It is built
from the same Markdown files as the repository, so there is only one copy of the content to maintain: edit
`docs/`, `hardware/README.md`, etc., and rebuild.

## What the build produces

A folder of plain HTML, CSS, JavaScript and images (`site/`). No database, no server-side code.

- **Works offline.** Fonts are the system fonts, and Mermaid (the diagram renderer) is bundled in
  `website/assets/`, so the pages make no request to the internet.
- **Works from disk.** Open `site/index.html` straight from a USB stick or an archive; search still works.
- **Works from any web server, at any path** (links are plain relative `.html` links).

## Build it

```sh
python3 -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r website/requirements.txt
tools/build_site.sh                                 # -> ./site
```

`tools/build_site.sh` runs `website/prepare.py`, which copies the repository into a temporary folder and adds
generated pages: photo galleries, the schematic viewer (`hardware/svg/*.svg`), file listings and the license page.
Links to folders are rewritten to point at those pages. The build runs in strict mode: a broken link fails it.

To preview while editing: run `python3 website/prepare.py . /tmp/tm31-stage`, then
`mkdocs serve -f /tmp/tm31-stage/mkdocs.yml` and open http://127.0.0.1:8000. That copy does not follow your
edits; run `prepare.py` again after changing files.

## Host it

- **GitHub Pages:** the workflow in `.github/workflows/pages.yml` builds and publishes the site on every push to
  `main`. Enable it once in the repository: *Settings → Pages → Source: GitHub Actions*. The site appears at
  `https://<user>.github.io/<repository>/`.
- **Your own server:** copy `site/` to any static web server (Nginx, Caddy, Apache, a NAS web share, ...).
  Each workflow run also keeps the built site as a downloadable artifact (`github-pages`, a tar archive).
- **Archive:** a zip of `site/` is a complete, offline copy of the documentation.

## Files

| File | Role |
|---|---|
| `mkdocs.yml` | Site configuration and navigation menu |
| `prepare.py` | Stages the repository and generates galleries, schematic viewer and listings |
| `requirements.txt` | Pinned Python packages for a reproducible build |
| `assets/extra.css` | Small style tweaks (wide tables, schematic background in dark mode) |
| `assets/mermaid.min.js` | Mermaid 11.4.1, MIT license (`assets/mermaid.LICENSE.txt`) |
| `assets/iframe-worker-shim.js` | iframe-worker 1.0.4 shim, MIT license: lets search run from `file://` |

## Longevity

The built site is plain static files and keeps working regardless of what happens to the tools that built it.
The build itself uses pinned versions (`requirements.txt`). Material for MkDocs is in maintenance mode until 2027;
its successor, Zensical, reads the same `mkdocs.yml` if the build ever needs to move.

When you add a documentation page, add it to `nav:` in `mkdocs.yml`; pages missing from the menu are still built
and searchable but only reachable through links.
