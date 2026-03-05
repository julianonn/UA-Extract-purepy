#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UA_EXTRACT_DIR="$REPO_ROOT/UA-Extract-purepy"
WHEELS_DIR="$REPO_ROOT/webapp/public/wheels"

echo "[build-wheels] Building ua-extract-purepy wheel..."


if ! command -v python3 &> /dev/null; then
  echo "[build-wheels] ERROR: python3 not found"
  exit 1
fi

mkdir -p "$WHEELS_DIR"

cd "$UA_EXTRACT_DIR"
python3 -m pip install --quiet build
python3 -m build --wheel --quiet --outdir "$WHEELS_DIR"


WHEEL_FILE=$(ls -t "$WHEELS_DIR"/ua_extract*.whl | head -1)

if [ -f "$WHEEL_FILE" ]; then
  echo "[build-wheels] Built: $(basename "$WHEEL_FILE")"
else
  echo "[build-wheels] ERROR: Wheel build failed"
  exit 1
fi

echo "[build-wheels] Done."
