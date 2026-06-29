#!/usr/bin/env bash
# Compatibility wrapper for saving ai-daily-report Markdown to Get笔记.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/save-to-getnote.py" "$@"
