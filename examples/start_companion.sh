#!/usr/bin/env bash
set -euo pipefail

# A convenience script to start the companion program
PYTHON=/usr/bin/python3
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "Starting companion from $BASE_DIR"

$PYTHON "$BASE_DIR/src/companion/main.py"
