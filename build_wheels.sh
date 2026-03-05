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

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cd "$SCRIPT_DIR"
python3 -m pip install --quiet build
python3 -m build --wheel --quiet --outdir "$DIST_DIR"

WHEEL_FILE=$(ls "$DIST_DIR" | grep .whl | head -1)

if [ -n "$WHEEL_FILE" ]; then
  echo "[build-wheels] Built: $WHEEL_FILE"
  echo "$WHEEL_FILE" > "$DIST_DIR/latest_wheel.txt"
  echo "[build-wheels] Created pointer: latest_wheel.txt -> $WHEEL_FILE"
else
  echo "[build-wheels] ERROR: Wheel build failed"
  exit 1
fi

echo "[build-wheels] Done."