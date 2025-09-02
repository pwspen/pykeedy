#!/bin/bash

# Get the script's directory
SCRIPT_DIR="$(dirname "$0")"

# Create venv in script directory if it doesn't exist
cd "$SCRIPT_DIR"
[ ! -d "venv" ] && uv venv

# Delete any PNG files in the script directory
rm -f *.png

# Run all Python files from parent directory
for file in ../*.py; do
    [ -f "$file" ] || continue
    echo "Running $(basename "$file")..."
    uv run "$file"
done

# Create results.md in parent directory with links to PNG files
echo "# Results" > ../results.md
echo "" >> ../results.md
for png in *.png; do
    [ -f "$png" ] || continue
    echo "![]($(basename "$SCRIPT_DIR")/$png)" >> ../results.md
done