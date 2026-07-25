#!/usr/bin/env bash
# Static checks for the ai-daily-report OpenClaw skill package.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ZIP_FILE="$ROOT_DIR/ai-daily-report-openclaw-skill.zip"

cd "$ROOT_DIR"

required_files=(
  "SKILL.md"
  "references/event-quality.md"
  "references/discovery-framework.md"
  "references/writing-template.md"
  "references/publishing-checklist.md"
  "references/task-descriptions.md"
  "references/personal-priorities.md"
  "scripts/save-to-getnote.py"
  "scripts/package-skill.sh"
  "scripts/validate-skill.sh"
)

if [ ! -f "$ZIP_FILE" ]; then
  echo "Missing package: $ZIP_FILE" >&2
  exit 1
fi

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "Missing required file: $file" >&2
    exit 1
  fi
  if ! unzip -l "$ZIP_FILE" "$file" >/dev/null; then
    echo "Package missing required file: $file" >&2
    exit 1
  fi

  local_hash="$(shasum -a 256 "$file" | awk '{print $1}')"
  zip_hash="$(unzip -p "$ZIP_FILE" "$file" | shasum -a 256 | awk '{print $1}')"
  if [ "$local_hash" != "$zip_hash" ]; then
    echo "Package content differs from working tree: $file" >&2
    exit 1
  fi
done

if unzip -l "$ZIP_FILE" | grep -q '\.DS_Store'; then
  echo "Package contains .DS_Store" >&2
  exit 1
fi

bash -n scripts/package-skill.sh
bash -n scripts/validate-skill.sh
python3 - <<'PY'
from pathlib import Path

path = Path("scripts/save-to-getnote.py")
compile(path.read_text(encoding="utf-8"), str(path), "exec")
PY

python3 - <<'PY'
import importlib.util
import os
import tempfile
import time
from pathlib import Path

spec = importlib.util.spec_from_file_location("save_to_getnote", "scripts/save-to-getnote.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

fixture = {"success": True, "data": {"note_id": "1914198881881698240"}}
if not module.is_success(fixture) or module.note_id_from(fixture) != "1914198881881698240":
    raise SystemExit("JSON response parser check failed")

with tempfile.TemporaryDirectory() as tmp:
    archive_dir = Path(tmp)
    old_report = archive_dir / "ai-daily-report-older.md"
    unrelated_file = archive_dir / "keep.txt"
    old_report.write_text("old", encoding="utf-8")
    unrelated_file.write_text("keep", encoding="utf-8")
    old_time = time.time() - 15 * 86400
    os.utime(old_report, (old_time, old_time))

    os.environ["AI_DAILY_REPORT_LOCAL_DIR"] = tmp
    os.environ["AI_DAILY_REPORT_RETENTION_DAYS"] = "14"
    report = Path("ai-daily-report-2026-07-25.md")
    archive_file, removed = module.archive_locally(report, "# AI 情报简报")

    if archive_file.read_text(encoding="utf-8") != "# AI 情报简报":
        raise SystemExit("Local report archive check failed")
    if old_report.exists() or removed != 1:
        raise SystemExit("Local report retention check failed")
    if not unrelated_file.exists():
        raise SystemExit("Local report cleanup removed a non-Markdown file")
PY

echo "Skill package validation passed."
