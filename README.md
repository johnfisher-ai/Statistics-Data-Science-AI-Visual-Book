# Statistics, Data Science and AI: A Visual Handbook

A visual, clickable handbook on statistics and data science — HTML chapter pages paired with
runnable Python notebooks. By **John Fisher**.

🌐 **Live site:** https://johnfisher-ai.github.io/Statistics-Data-Science-AI-Visual-Book/

---

## How readers use it

1. **Read** a chapter (static HTML, works anywhere).
2. **View the notebook** — a rendered HTML page with all code *and outputs*, instantly, no install.
3. **Open in Colab** — run and edit the code live in the browser (a Google login is needed only to *run*;
   viewing is free). Readers get their own throwaway copy — the original in this repo is never changed.
4. **Download / view on GitHub** — grab the raw `.ipynb` or read it on GitHub.

## Project structure

```
.
├── index.html                  # Title page
├── toc.html                    # Table of contents (flip chapters live via the AVAILABLE set)
├── assets/css/                 # book.css (global) + chapter.css (chapter layout)
├── chapters/
│   ├── ch01.html               # Chapter pages (inline SVG graphics — fully editable)
│   └── notebooks/
│       ├── ch01_what_is_statistics.ipynb   # Source notebooks (outputs pre-executed)
│       └── html/                            # Rendered HTML (auto-built; what "View" links to)
├── scripts/build_notebook_html.sh          # Local notebook → HTML renderer
├── requirements.txt
└── .github/workflows/deploy.yml            # Auto-render notebooks + deploy to Pages on push
```

## Local preview

Just open `index.html` in a browser. To re-render notebooks after editing them:

```bash
pip install -r requirements.txt
bash scripts/build_notebook_html.sh
```

## Checking links

```bash
python3 scripts/check_links.py              # local and self-referencing links
python3 scripts/check_links.py --external   # also HTTP-check outside hosts
```

Resolves every `href` and `src` in all 646 pages: relative paths, in-page anchors, and
the Colab, `github.com/blob` and Pages URLs that point back into this repository. Those
last ones are checked against the local tree with no network call, which is the only way
to catch a broken Colab button: the chapter page loads fine, and the notebook 404s only
when a reader clicks it.

## Publishing

See **[PUBLISHING.md](PUBLISHING.md)** for first-time setup and the per-chapter workflow.

---

## License

**The book, the figures and the datasets: [CC BY 4.0](LICENSE). The code: [MIT](LICENSE-CODE).**

Use any of it, including commercially, with credit. Teach from it, translate it, quote
it, build on it. A reasonable credit:

> John Fisher, *Statistics, Data Science and AI: A Visual Handbook*.
> https://johnfisher-ai.github.io/Statistics-Data-Science-AI-Visual-Book/

See **[LICENSES.md](LICENSES.md)** for which license covers which files.

Every dataset in `data/` was written for this book. Two are named after well-known public
datasets and are **not** those datasets: see **[data/README.md](data/README.md)** before
comparing results against published analyses.

© 2026 John Fisher.
