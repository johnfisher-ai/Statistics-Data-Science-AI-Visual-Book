# Statistics, Data Science and AI: A Visual Handbook

A 205-chapter HTML book with companion Jupyter notebooks, Excel datasets and branded report
pages. Public repo, published to GitHub Pages on every push to `main`.

**Author: John Fisher.** The book is complete at 205 of 205 chapters.

---

## Hard rules

These have each cost real time when broken. They are not preferences.

- **Never push.** The author pushes with `bash scripts/push_to_github.sh "message"` and reviews
  chapter by chapter. Commit freely; pushing is the author's.
- **Never `git commit --amend`, rebase, or rewrite history.** Always make a new follow-up commit.
  The author pushes out of band, so treat every existing commit as possibly published. This has
  bitten twice. Recovery without a force push: `git fetch`, `git reset --soft origin/main`,
  re-commit the delta.
- **No `Co-Authored-By` trailer** on commits.
- **The repo is PUBLIC.** Never store or use the GitHub password. The saleable PDF lives outside
  this repo.
- **On resume:** `git log --oneline -5` and confirm with the author what is already pushed.

---

## Layout

| Path | What it is |
|---|---|
| `chapters/*.html` | The 205 chapter pages. One file per chapter, named by slug. |
| `chapters/notebooks/*.ipynb` | Companion notebooks. Source of truth. |
| `chapters/notebooks/html/*.html` | **Generated.** Never hand-edit; rebuilt on deploy. |
| `data/*.xlsx` | Datasets. Three sheets: `Data`, `Codebook`, `Notes`. |
| `reports/*.html` | Branded report pages (plain-language brief + technical report). |
| `assets/img/*.png` | Chapter and report figures. |
| `assets/css/`, `assets/js/` | `book.css`, `chapter.css`, `quiz.css`, `report.css`, `quiz.js`. |
| `toc.html` | **The manifest.** Single source of truth for structure. |
| `scripts/` | `push_to_github.sh`, `apply_chapter_nav.py`, `inject_notebook_backlinks.py`. |

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
page `<h1>`. Change one, change all three.

---

## House style

- **American English**, strictly. Four cases are deliberately British and must stay:
  - `summarise` in `chapters/r-for-statistics.html` — the dplyr function name, one instance
    inside live R code.
  - `grey` in `case-study-ames-housing-prices` and its notebook — merging `grey` and `gray` in
    an `exterior_color` column **is** the cleaning lesson.
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
- **Keep `$` and `~` out of notebook markdown prose.** Two `$` on a line render as MathJax; two
  `~` render as strikethrough. Write "338,000 dollars" and "about 0.89". Both are fine inside
  code cells and plot titles.
- Per-part theme colour lives only in inline SVG colours, the notebook hero gradient, and
  `rw-card` colours. Global header chrome is fixed book-wide.

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
2. **Execute** with `nbclient`, kernel `nbtest-py`, cwd `chapters/notebooks`.
3. **Verify** every prose claim against the printed output, and **look at every figure** at its
   true rendered width.
4. **Render**: `python3 -m nbconvert --to html --template lab --output-dir html <name>.ipynb`
   (`jupyter` is not on PATH; use `python3 -m`).
5. **Re-inject backlinks**: `python3 scripts/inject_notebook_backlinks.py`. Rendering strips the
   "Back to the book" card. The script's `MAP` must gain an entry for every new notebook.

In practice you can skip 4 and 5 locally: the deploy workflow re-renders any changed `.ipynb`
and re-injects backlinks automatically. It does **not** execute, so step 2 is still yours.

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

---

## Standing author requests

1. A **"<topic> in Machine Learning & AI"** section (table plus research callout).
2. A **real Excel dataset** in `data/`, three sheets, with a `.rw-card` and a download button.
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
0 broken local references            · the only expected hit is ${href}, a JS template in toc.html
chapter count matches AVAILABLE      · apply_chapter_nav.py --check reports 0 drift
no prose em-dashes                   · entities limited to the six allowed
no British spellings                 · except the protected cases listed above
```

Current baseline: 345 notebooks, 700 plots, 0 errors, 205 chapters, 86 reports, 134 datasets.
