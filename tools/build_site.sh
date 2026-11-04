#!/bin/sh
# Build the documentation website into ./site (plain static files).
# Needs: python3 and the packages in website/requirements.txt (pip install -r website/requirements.txt).
# Run from the repository root.
set -e
STAGE=$(mktemp -d)
python3 website/prepare.py . "$STAGE/stage"
mkdocs build --strict -f "$STAGE/stage/mkdocs.yml" -d "$PWD/site"
rm -rf "$STAGE"
echo "Built ./site  (open site/index.html, or serve the folder with any web server)"
