# Publishing Guide

Everything needed to get the book online and keep it updated.

- **GitHub user:** `johnfisher-ai`
- **Repository:** `Statistics-Data-Science-AI-Visual-Book`
- **Repo root = this `book/` folder** (so `index.html` is served at the site root)
- **Live URL (after setup):** https://johnfisher-ai.github.io/Statistics-Data-Science-AI-Visual-Book/

> ⚠️ Keep the repo **Public** and do **not** add reviewers as collaborators. That combination is what
> gives you full read/write while reviewers can only view/run/copy in Colab — never alter your original.

---

## One-time setup

### 1. Create the empty repo on GitHub
Go to https://github.com/new and create **`Statistics-Data-Science-AI-Visual-Book`**, **Public**,
with **no** README/.gitignore (this folder already has them).

### 2. Authenticate git (pick ONE — password no longer works)

**Option A — GitHub CLI (easiest):**
```bash
brew install gh        # if not installed
gh auth login          # choose GitHub.com → HTTPS → login in browser
```

**Option B — Personal Access Token (PAT):**
Create a token at https://github.com/settings/tokens (scope: `repo`). When git asks for a password
during push, paste the **token** instead. (Username = `johnfisher-ai`.)

### 3. Push this folder
Run from inside the `book/` folder:
```bash
git push -u origin main
```
(The local repo, `main` branch, and `origin` remote are already configured — see "Initial commit" below.)

### 4. Turn on GitHub Pages
In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
The included workflow (`.github/workflows/deploy.yml`) then renders the notebooks and deploys automatically.
First deploy takes ~1–2 minutes; the live URL appears under the Actions run and in Settings → Pages.

---

## Per-chapter workflow (every time you add/update content)

1. **Write** the chapter HTML (`chapters/chNN.html`) and notebook (`chapters/notebooks/chNN_*.ipynb`).
2. **Execute the notebook** so outputs are saved into the `.ipynb` (open it and Run All, or it's
   pre-executed when generated). The "View" page shows whatever outputs are saved in the file.
3. **Add Colab/View/Download buttons** to the chapter page, pointing at:
   ```
   View:    notebooks/html/chNN_<slug>.html
   Colab:   https://colab.research.google.com/github/johnfisher-ai/Statistics-Data-Science-AI-Visual-Book/blob/main/chapters/notebooks/chNN_<slug>.ipynb
   GitHub:  https://github.com/johnfisher-ai/Statistics-Data-Science-AI-Visual-Book/blob/main/chapters/notebooks/chNN_<slug>.ipynb
   ```
4. **Flip the chapter live** in `toc.html`: add its number to `const AVAILABLE = new Set([1, ...]);`
   and restore the "Next" link on the previous chapter page.
5. **(Optional) Render locally to preview:** `bash scripts/build_notebook_html.sh`
   *(Not required for production — the deploy workflow renders notebooks in the cloud.)*
6. **Commit & push:**
   ```bash
   git add -A
   git commit -m "Add Chapter NN: <title>"
   git push
   ```
   GitHub Actions rebuilds the notebook HTML and redeploys the site automatically.

---

## Notes
- Notebook HTML in `chapters/notebooks/html/` is committed for convenience, but the workflow regenerates
  it on every push — so it's always in sync with the `.ipynb`.
- Reviewers who open a notebook in Colab get an ephemeral copy: they can run, edit, download (`File →
  Download`), or copy (`File → Save a copy in Drive`), but cannot write back to this repo.
