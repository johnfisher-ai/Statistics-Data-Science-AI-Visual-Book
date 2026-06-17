#!/usr/bin/env bash
# Push the book to GitHub. Run this AFTER you've authenticated git
# (via `gh auth login`, or a Personal Access Token used as your password).
#
#   bash scripts/push_to_github.sh                 # push current commits
#   bash scripts/push_to_github.sh "commit message" # stage all, commit, then push
#
# Repo: https://github.com/johnfisher-ai/Statistics-Data-Science-AI-Visual-Book
set -euo pipefail

cd "$(dirname "$0")/.."                      # repo root (the book/ folder)

REMOTE_URL="https://github.com/johnfisher-ai/Statistics-Data-Science-AI-Visual-Book.git"

# Ensure we're on main
git rev-parse --verify main >/dev/null 2>&1 || git branch -M main
git checkout -q main 2>/dev/null || true

# Ensure the 'origin' remote points at the right repo
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
fi

# Optional: stage + commit if a message was supplied
if [ "${1:-}" != "" ]; then
  git add -A
  git -c user.name="John Fisher" -c user.email="johnrfisher@gmail.com" commit -m "$1"
fi

echo "Pushing to $REMOTE_URL (branch main) ..."
git push -u origin main
echo "✅ Pushed. Then enable Pages: Settings → Pages → Source: GitHub Actions."
