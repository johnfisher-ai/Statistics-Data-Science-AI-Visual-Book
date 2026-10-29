# Statistics, Data Science and AI: A Visual Handbook

A visual, clickable handbook on statistics, data science and AI, in 205 HTML chapter pages, 195 of them
paired with a runnable Python notebook. By **John Fisher**.

🌐 **Live site:** https://johnfisher-ai.github.io/Statistics-Data-Science-AI-Visual-Book/

---

## How readers use it

1. **Read** a chapter (static HTML, works anywhere).
2. **View the notebook**, a rendered HTML page with all the code *and its outputs*, with nothing to install.
3. **Open in Colab** to run and edit the code in the browser. A Google login is needed only to *run* it,
   and each reader gets a throwaway copy, so the original in this repository never changes.
4. **Download or view on GitHub** to get the raw `.ipynb`.

## Project structure

```
.
├── index.html                  # Title page
├── introduction.html           # How the book works
├── toc.html                    # Contents, and the manifest: PARTS sets the order, AVAILABLE what is published
├── infographics*.html          # Printable visual reviews of several parts
├── 404.html                    # Shown for an address that doesn't exist
├── sitemap.xml                 # Every published page, for search engines (scripts/build_sitemap.py)
├── chapters/
│   ├── <slug>.html             # The 205 chapter pages, named by slug, with inline SVG figures
│   └── notebooks/
│       ├── <slug>.ipynb        # Companion notebooks, saved with their outputs
│       └── html/               # The rendered notebooks that "View Notebook" opens
├── reports/                    # A plain-language brief and a technical report for each capstone
├── data/                       # The datasets (.xlsx and .csv), all written for the book
├── assets/                     # css/, js/ and img/, the chapter and report figures
├── scripts/                    # Chapter numbering, notebook backlinks, link checks, rendering, the sitemap
├── requirements.txt            # The libraries the notebooks import
└── .github/workflows/          # deploy.yml publishes to Pages; check-links.yml checks every link
```

Chapter numbers are computed from the order of `PARTS` in `toc.html`, so inserting a chapter
renumbers everything after it. `python3 scripts/apply_chapter_nav.py` then re-stamps the numbers
on every page, and `--check` reports drift without changing anything.

## Local preview

Open `index.html` in a browser. To render a notebook after editing it:

```bash
pip install -r requirements.txt
python3 -m nbconvert --to html --template lab --output-dir chapters/notebooks/html chapters/notebooks/<slug>.ipynb
python3 scripts/inject_notebook_backlinks.py
```

The last step adds what rendering leaves out: the card with the way back to the chapter and the
buttons to open the notebook in Colab, download it or view it on GitHub, the tab title and link tags,
and the styles that keep the page readable. `bash scripts/build_notebook_html.sh`
renders all 345 notebooks the same way. Rendering doesn't run the code, so a notebook shows the outputs
saved in it. Run it first if you changed its code.

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

It also validates the backlink table in `scripts/inject_notebook_backlinks.py`, which
rewrites notebook HTML at deploy time. A wrong anchor there outlives any fix to the
rendered pages, because the next re-render puts it straight back.

**This runs in CI.** `.github/workflows/check-links.yml` fails a push or a pull request
that leaves a link pointing at nothing.

## Publishing

See **[PUBLISHING.md](PUBLISHING.md)** for how a change reaches the site and how to add or revise a chapter.

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
