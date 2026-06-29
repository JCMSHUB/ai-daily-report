#!/usr/bin/env bash
# Build the OpenClaw skill zip from the current working tree.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_FILE="$ROOT_DIR/ai-daily-report-openclaw-skill.zip"
TMP_FILE="$ROOT_DIR/.ai-daily-report-openclaw-skill.zip.tmp"

cd "$ROOT_DIR"

rm -f "$TMP_FILE"
zip -qr "$TMP_FILE" \
  SKILL.md \
  references \
  scripts \
  -x '*.DS_Store' \
  -x '*/.DS_Store' \
  -x '.git/*' \
  -x '__MACOSX/*'

mv "$TMP_FILE" "$OUT_FILE"
echo "Built $OUT_FILE"
