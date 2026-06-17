#!/usr/bin/env bash
# Render every chapter notebook to HTML (code + outputs) into chapters/notebooks/html/.
# These rendered pages are what the "View Notebook" buttons link to.
#
# Usage:  bash scripts/build_notebook_html.sh
# Requires: jupyter + nbconvert  (pip install -r requirements.txt)
set -euo pipefail

cd "$(dirname "$0")/.."          # repo root (the book/ folder)
SRC="chapters/notebooks"
OUT="chapters/notebooks/html"
mkdir -p "$OUT"

shopt -s nullglob
count=0
for nb in "$SRC"/*.ipynb; do
  name="$(basename "${nb%.ipynb}")"
  echo "Rendering $name ..."
  jupyter nbconvert --to html --output-dir "$OUT" --output "$name.html" "$nb"
  count=$((count+1))
done

echo "Done. Rendered $count notebook(s) to $OUT/"
