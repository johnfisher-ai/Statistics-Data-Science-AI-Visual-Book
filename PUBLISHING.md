# Publishing guide

How a change reaches the live site, and how to add or revise a chapter.

- **GitHub user:** `johnfisher-ai`
- **Repository:** `Statistics-Data-Science-AI-Visual-Book`, whose root is the book folder, so `index.html` is served at the site root
- **Live site:** https://johnfisher-ai.github.io/Statistics-Data-Science-AI-Visual-Book/

> Keep the repository **public**, and don't add reviewers as collaborators. Readers can then view,
> run and copy any notebook in Colab, and none of them can change the original.

---

## How the site is published

Every push to `main` runs `.github/workflows/deploy.yml`. It renders the notebooks the push changed,
adds the "Back to the book" card to each rendered page, and publishes the whole folder to GitHub
Pages. The rendered HTML of every other notebook is published as it is committed. A deploy takes a
few minutes, and longer when many notebooks changed.

The deploy doesn't run notebooks, so a notebook page shows the outputs saved in the `.ipynb`. Run a
notebook top to bottom before committing it. Its saved outputs come from the library versions Colab
runs, so that a reader who opens it in Colab sees the same numbers the page does.

To render every notebook again, run the workflow by hand from the Actions tab ("Build & Deploy Book
to GitHub Pages", then "Run workflow"). That is needed when the backlink card in
`scripts/inject_notebook_backlinks.py` changes design, because the script skips pages that already
have a card. A second workflow, `.github/workflows/check-links.yml`, fails any push that leaves a
link pointing at nothing.

Since October 27, 2026, Claude Code sessions commit straight to `main` once the checks pass, one
commit per chapter or round of edits, and John reads each change on the live site. A change is undone
with `git revert`, never by rewriting history. `scripts/push_to_github.sh` is the old manual push
from John's Mac and is no longer needed. The book's `CLAUDE.md` is the technical manual for these
sessions.

---

## Adding or revising a chapter

1. **Write the page** as `chapters/<slug>.html`. A slug comes from words, never numbers or dates, and
   never changes once published, because other sites link to chapters by slug. Start from an existing
   chapter's `<head>`, which links the stylesheets and the light and dark themes.
2. **Place it in `toc.html`.** Add an entry to `PARTS` where it belongs in reading order, and its slug
   to `AVAILABLE` to publish it. A chapter in `PARTS` but not in `AVAILABLE` shows as coming soon. A
   chapter's title lives in three places, the `PARTS` entry, the page's `<title>` and its `<h1>`, so
   change all three together.
3. **Renumber.** Chapter numbers come from the order of `PARTS`, so inserting a chapter shifts every
   number after it. `python3 scripts/apply_chapter_nav.py` re-stamps the numbers on every page. It
   doesn't change titles or links, so set the previous and next cards on the new chapter and its two
   neighbors by hand.
4. **Build and run the notebook**, `chapters/notebooks/<slug>.ipynb`, so its outputs are saved.
5. **Render it** and add the backlink card:
   ```bash
   python3 -m nbconvert --to html --template lab --output-dir chapters/notebooks/html chapters/notebooks/<slug>.ipynb
   python3 scripts/inject_notebook_backlinks.py
   ```
   A new notebook needs an entry in that script's `MAP` first. Commit the rendered HTML in the same
   commit as its notebook. The deploy renders only the notebooks a push changes, so HTML left out of a
   commit goes back to its old version at the next push that doesn't touch that notebook.
6. **Link the notebook** from the chapter with three buttons:
   ```
   View:    notebooks/html/<slug>.html
   Colab:   https://colab.research.google.com/github/johnfisher-ai/Statistics-Data-Science-AI-Visual-Book/blob/main/chapters/notebooks/<slug>.ipynb
   GitHub:  https://github.com/johnfisher-ai/Statistics-Data-Science-AI-Visual-Book/blob/main/chapters/notebooks/<slug>.ipynb
   ```
7. **Update the sitemap.** `python3 scripts/build_sitemap.py` rewrites `sitemap.xml` from the manifest,
   which a new chapter, report or notebook needs. `--check` says whether it is out of date.
8. **Check and push.** `python3 scripts/check_links.py` should resolve every link, and
   `python3 scripts/apply_chapter_nav.py --check` should report no drift. Then commit and push to `main`.

To flag a revised chapter in the contents for one push cycle, add its slug to `UPDATED_CHAPTERS` in
`toc.html`, which shows a temporary "Updated" badge, and empty the set again at the next push.

---

## Notes

- A reader who opens a notebook in Colab gets a copy of their own. They can run it, edit it, download
  it (File, Download) or save it to their Drive (File, Save a copy in Drive), and none of that writes
  back to this repository.
- The licenses are in [LICENSES.md](LICENSES.md), and the datasets are described in
  [data/README.md](data/README.md).
