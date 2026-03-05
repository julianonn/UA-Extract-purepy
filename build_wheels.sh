#!/usr/bin/env bash
# outputs to ./dist/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"

echo "[build-wheels] Building ua-extract-purepy wheel..."

if ! command -v python3 &> /dev/null; then
  echo "[build-wheels] ERROR: python3 not found"
  exit 1
fi

mkdir -p "$DIST_DIR"

cd "$SCRIPT_DIR"
python3 -m pip install --quiet build
python3 -m build --wheel --quiet --outdir "$DIST_DIR"

WHEEL_FILE=$(ls -t "$DIST_DIR"/ua_extract*.whl | head -1)

if [ -f "$WHEEL_FILE" ]; then
  echo "[build-wheels] Built: $(basename "$WHEEL_FILE")"
  cd "$DIST_DIR"
  mv "$WHEEL_FILE" "$DIST_DIR/ua_extract_purepy-latest.whl"
  echo "[build-wheels] Symlink: ua_extract_purepy-latest.whl"
else
  echo "[build-wheels] ERROR: Wheel build failed"
  exit 1
fi

echo "[build-wheels] Done."
