# Statistics, Data Science and AI: A Visual Handbook

A 205-chapter HTML book with companion Jupyter notebooks, Excel datasets and branded report
pages. Public repo, published to GitHub Pages on every push to `main`.

**Author: John Fisher.** The book is complete at 205 of 205 chapters.

---

## Hard rules

These have each cost real time when broken. They are not preferences.

- **Push to `main` once the checks pass.** Decided October 27, 2026, replacing the rule that
  Claude never pushes. Claude Code sessions commit and push straight to `main`, one commit per
  chapter or round of edits, and the author reads each change on the live site. The workflow, the
  writing rules and the checks are in the private companion repository
  `johnfisher-ai/visual-book-notes`. Read its CLAUDE.md and the files it lists first. If a push to
  `main` is refused, push to a branch named for the work and tell the author.
- **Never `git commit --amend`, rebase, force-push or rewrite history.** Always make a new
  follow-up commit, and undo a pushed change with `git revert`. Treat every existing commit as
  published. Recovery for a local commit that went wrong: `git fetch`,
  `git reset --soft origin/main`, re-commit the delta.
- **No `Co-Authored-By` trailer** on commits.
- **The repo is PUBLIC.** Never store or use the GitHub password. The saleable PDF lives outside
  this repo.
- **On resume:** `git log --oneline -5`. A cloud session clones from GitHub, so everything in
  it is already pushed. The author pushes any edits made on his own computer before a session.

---

## Layout

| Path | What it is |
|---|---|
| `chapters/*.html` | The 205 chapter pages. One file per chapter, named by slug. |
| `chapters/notebooks/*.ipynb` | Companion notebooks. Source of truth. |
| `chapters/notebooks/html/*.html` | **Generated.** Never hand-edit; rebuilt on deploy. |
| `data/*.xlsx`, `data/*.csv` | Datasets. Most workbooks have three sheets: the data (named `Data` or for its contents), `Codebook` and `Notes`. 25 of the 134 add sheets such as a plan or a `Truth` sheet. |
| `reports/*.html` | Branded report pages (plain-language brief + technical report). |
| `assets/img/*.png` | Chapter and report figures. |
| `assets/css/`, `assets/js/` | `book.css`, `chapter.css`, `quiz.css`, `report.css`, `quiz.js`, and the dark theme: `theme.css` (**generated**, see House style) and `theme.js`. |
| `toc.html` | **The manifest.** Single source of truth for structure. |
| `scripts/` | `apply_chapter_nav.py`, `inject_notebook_backlinks.py`, `check_links.py`, `build_notebook_html.sh`, `build_sitemap.py` (rewrites `sitemap.xml` from the manifest; run it after adding a page), and `push_to_github.sh` (the author's old manual push, unused by sessions). |

The repo root **is** the `book/` folder. A `book/` segment inside any URL is a dead link.
Source material (raw images, reference books, sample data) lives in the parent workspace
directory and is deliberately outside git.

---

## Structure is computed, not written

`toc.html` holds a `PARTS` array and an `AVAILABLE` set.

- **Chapter numbers are positional** — computed from order in `PARTS`. The `n:` fields are
  cosmetic. Inserting a chapter shifts every number after it.
- **`AVAILABLE` gates publication.** A chapter in `PARTS` but not in `AVAILABLE` shows as
  coming soon.
- After any structural change run `python3 scripts/apply_chapter_nav.py`. It re-stamps only
  chapter **numbers** (title tag, crumb, hero, footer, prev/next cards). It never touches titles
  or hrefs, so prev/next wiring stays manual.
- `python3 scripts/apply_chapter_nav.py --check` reports drift without changing anything.

**Editing `AVAILABLE` safely:** slice the block by index and replace inside the slice. A
document-wide `s.replace('"slug"', ...)` hits the `slug:"..."` field in `PARTS` first and
silently corrupts the previous chapter's manifest entry. The tell is `apply_chapter_nav.py`
reporting the wrong chapter count. Always assert the manifest slug count is unchanged.

A chapter title lives in **three** places: the `PARTS` `t:` field, the page `<title>`, and the
page `<h1>`. Change one, change all three. All 205 have agreed since October 28, when the capstones' question
headings were replaced by their titles. The same words also appear in the page's `og:title` and
`twitter:title`, the neighbors' previous and next cards, the reports' chapter line and the notebook
backlink labels in `scripts/inject_notebook_backlinks.py` and the rendered notebook pages, so change
those with it.

---

## House style

- **American English**, strictly. Four cases are deliberately British and must stay:
  - `summarise` in `chapters/r-for-statistics.html` — the dplyr function name, one instance
    inside live R code.
  - `grey` in `case-study-ames-housing-prices` and its notebook — merging `grey` and `gray` in
    an `exterior_color` column **is** the cleaning lesson. `case-study-predicting-ames-house-prices`
    repeats the same step in its notebook's code.
  - `cancelled` in `case-study-multi-file-and-datetime-eda` — a status **data value** the code
    standardizes on and asserts against.
  - `GREY` in notebook code — a matplotlib colour constant (`GREY = "#94a3b8"`). Also `Greys`
    is a colormap name.
  - Also protected as proper nouns: **Harbour Point**, a store name in the ch175 capstone.
- **No prose em-dashes.** Use commas or parentheses. An em-dash is allowed only inside `<title>`.
- **Named entities in prose limited to** `&amp; &lt; &gt; &quot; &nbsp; &middot;`. Numeric
  entities are fine, and required inside `<svg>`.
- **Prose must read human, not AI.** Avoid: precious superlatives ("the gentlest in the book"),
  aphoristic one-liners, writerly meta-flourishes ("doubles as a template", "earn the right to"),
  cutesy filler adverbs, and stacked negative parallelism ("not X, it's Y"). Keep real idioms a
  person actually says. Read the intro and closing paragraphs for the essay-contest ring before
  committing.
- **The 12 writing rules** in the companion repository's CLAUDE.md apply to all new and edited
  prose here, alongside the rules in this section.
- **Keep `$` and `~` out of notebook markdown prose.** Two `$` on a line render as MathJax; two
  `~` render as strikethrough. Write "338,000 dollars" and "about 0.89". Both are fine inside
  code cells and plot titles.
- Per-part theme colour lives only in inline SVG colours, the notebook hero gradient, and
  `rw-card` colours. Global header chrome is fixed book-wide.
- **Text contrast.** Small text on the light pages needs 4.5:1, so color it with the tokens in
  `chapter.css`: `--ink-faint` for the faintest grey, the `--c-cyan-text`, `--c-green-text` and
  `--c-amber-text` shades for accents, and a plain `<a>` for a link, which `--link` colors and
  underlines. The book's cyan `#00d4ff` is for the dark hero and panels only. Check a new color
  with axe before committing.
- **Two themes.** The chapters, reports, introduction and 404 page follow the reader's device
  setting, and the switch in the top bar overrides it (October 29). A color a dark page has to
  change is written `var(--p-bg-ecfdf5, #ecfdf5)`, with the role `fg`, `bg` or `bd`, and the light
  pages never define these, so they show the original. After writing or editing a page, run the
  companion repository's `tools/theme/tokenize.py`, which rewrites any new hard-coded color, then
  `tools/theme/build_theme.py`, which rewrites `assets/css/theme.css`. Never edit `theme.css` by
  hand. A new page links `theme.css` and then `theme.js` after its other stylesheets, as every
  chapter's `<head>` does. Figures stay as drawn. `figure`, `.svg-wrap` and `.nb-fig` keep their
  light panels in the dark theme, so SVG colors need no tokens. Check both themes with axe.

---

## The rule that matters most

**Verify every prose claim against executed output.** Narration written before execution is
frequently wrong in specifics: a claimed skew that isn't, a "most" that is 24 percent, two groups
asserted to differ that turn out identical. Print the numbers, read them, then write the words.

Across the capstones this caught roughly a dozen false claims that were fluent and plausible.
Cite numbers from executed output, never from draft prose.

---

## Notebook pipeline

Build → execute → verify → render → wire.

1. **Build** the `.ipynb` (a builder script, or edit the JSON directly).
2. **Execute** with `nbclient`, cwd `chapters/notebooks`, on the Colab replica kernel `nb-colabsim`
   (file 3 of the companion repository builds it), so the saved outputs are what a Colab reader
   gets. A cell whose printed text already matches keeps its saved output.
3. **Verify** every prose claim against the printed output, and **look at every figure** at its
   true rendered width. The companion repository's `tools/checks/quote_check.py` lists every place
   the chapter, its reports and the notebook's markdown still quote a number the new run no longer
   prints. Run the notebook twice first, because a number that changes between runs can't be quoted.
4. **Render**: `python3 -m nbconvert --to html --template lab --output-dir html <name>.ipynb`
   (`jupyter` is not on PATH; use `python3 -m`).
5. **Re-inject the card**: `python3 scripts/inject_notebook_backlinks.py`. Rendering leaves out the
   book's card (the way back to the chapter, and Open in Colab, download and GitHub buttons), the tab
   title and link tags, and the page's contrast and heading fixes. The script's `MAP` must gain an
   entry for every new notebook. Render in an environment holding only the renderer libraries
   `deploy.yml` pins, with no IPython, as the deploy has (file 3 of the companion repository builds
   it), so the deploy's render matches the committed page. With IPython installed, nbconvert
   highlights code with IPython's lexer, which reads `x%2` as a line magic.

Always do 4 and 5, and commit the rendered HTML in the same commit as its notebook. The deploy
re-renders only the notebooks a push changes and publishes the committed HTML for all the others,
so HTML left uncommitted goes back to its old version at the next push that doesn't touch that
notebook. The October 16 commit changed 199 notebooks without their HTML, and their rendered pages
were committed on October 27. The deploy does **not** execute, so step 2 is always yours.

**Kernel:** `python3 -m ipykernel install --user --name nbtest-py` if missing. System python3
has pandas, numpy, matplotlib, seaborn, scipy, scikit-learn, statsmodels, nbformat, nbclient,
nbconvert, openpyxl, shap, lime, imblearn, mlxtend, torch, lifelines.

**Never re-run an old builder script** to edit an existing notebook. The scratchpad builders
predate later prose passes and re-running one silently reverts them. Edit the `.ipynb` directly.

---

## Capstone chapter layout

Copy the closing block from a recent capstone rather than writing it fresh. Fixed order:

```
… → What This Does Not Settle → What to Watch → "<Topic> in Data Science & AI" (id="in-ds-ai")
   → notebook (unnumbered) → takeaways (unnumbered) → quiz
```

- **What to Watch** is a `<ul class="checklist">` of forward-looking guidance, not a takeaways box.
- **Takeaways** comes *after* the notebook block, as `<div class="takeaways">`.
- The notebook block has **three buttons**: primary "View Notebook", amber `#f9ab00`
  "Open in Colab", ghost "View / Download on GitHub".
- Colab and GitHub URLs use `blob/main/chapters/notebooks/<slug>.ipynb`.
- Dataset and report links go in their own `rw-card`, **not** inside the dark `nb-cta` panel.
- A part-closing capstone also gets a `.partclose` block recapping the part by linked chapter title.

**Every capstone notebook gets a "First look" step** between Cleaning and the first method step:
md header → code (numeric summary, target 5 or 6 printed lines) → md `**What this shows.**` →
code (one two-panel figure at `figsize=(12.6, 4.4)`, or 2×2 at `(12.6, 8.2)`) → md
`**Left:** … **Right:** …`. Choose the technique to fit the data and foreshadow the finding.
Never print a `describe()` dump; put the quantiles on the picture. Never in the reports.

27 of the 41 capstone notebooks have a step named First look. The other 14, the older testing and
sampling capstones, already plot the data before testing under their own step names ("Visualize
first", "Explore before testing"), and John decided on October 28 to leave them as they are. The
A/B test design's First look reads only what was recorded before assignment, because its plan
forbids reading the outcome before the health check.

---

## Standing author requests

1. A **"<topic> in Machine Learning & AI"** section (table plus research callout).
2. A **realistic Excel dataset** in `data/`, with its data, `Codebook` and `Notes` sheets, a `.rw-card` and a download button.
   The datasets are written for the book, so label them realistic or teaching data, never real.
3. **Library-first notebooks.** statsmodels, scipy, scikit-learn over hand-rolled computation.
   Show a formula once for teaching, then the one-line library call.
4. **Visual-first.** Chapters carry 2+ editable inline SVGs; notebooks carry plenty of plots.
5. **Embed notebook figures into chapter text** as PNGs in `assets/img/` with `.nb-fig`.
6. **Reports carry their own visuals.** Brief gets one headline figure; technical gets one or two
   evidence figures. Report figures are **single-panel, 1200×620 at 150 dpi, 12–13pt type**,
   because `.rpt-body` is capped at 66ch.
7. Every capstone gets the **First look** step described above.

---

## Traps that have cost real time

- **Figure titles overflow their panel.** rcParams set `axes.titlelocation: "left"`, so a title
  wider than its axes runs into the next panel's title. Measure it rather than eyeballing.
- **Chapter-embedded PNGs are independent copies.** Fixing a figure in a notebook does not fix
  the chapter page. Rebuild by replaying the source cell at
  `dpi = existing_pixel_width / figsize_w`.
- **Old stored outputs hide broken code.** One notebook called `boxplot(labels=…)`, removed in
  matplotlib 3.9, invisible because the output predated the upgrade. Re-executing is the only
  way that surfaces.
- **Escape levels differ by layer.** A plain script needs `\n`; a builder whose cell sources sit
  in `'''…'''` needs `\\n`; patching a builder through a heredoc adds another layer.
- **Renumbering notebook steps orphans `Step N` cross-references** in prose. Sweep first.
- **A colon-free `.replace()` on a slug** hits `toc.html`'s `PARTS` before `AVAILABLE`. See above.

---

## Validate before every commit

```
notebooks execute with 0 errors      · every .ipynb has a rendered .html
quote_check.py lists no stale number · chapters and reports quote what the Colab replica prints
0 broken local references            · the only expected hit is ${href}, a JS template in toc.html
chapter count matches AVAILABLE      · apply_chapter_nav.py --check reports 0 drift
no prose em-dashes                   · entities limited to the six allowed
no British spellings                 · except the protected cases listed above
theme.css up to date                 · tokenize.py and build_theme.py --check report nothing to do
```

Current baseline: 345 notebooks, 700 plots, 0 errors, 205 chapters, 86 reports, 134 datasets.

The companion repository's `tools/checks/run.sh` runs these checks on the changed pages, along with
the HTML validator, axe and the naming scan. Its punch list records the October 27 baseline for
the checks the book doesn't pass yet.
