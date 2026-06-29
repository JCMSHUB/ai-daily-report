#!/usr/bin/env bash
# Static checks for the ai-daily-report OpenClaw skill package.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ZIP_FILE="$ROOT_DIR/ai-daily-report-openclaw-skill.zip"

cd "$ROOT_DIR"

required_files=(
  "SKILL.md"
  "references/source-quality.md"
  "references/search-keywords.md"
  "references/template.md"
  "references/output-checklist.md"
  "references/task-descriptions.md"
  "references/personal-priorities.md"
  "scripts/save-to-getnote.sh"
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

bash -n scripts/save-to-getnote.sh
bash -n scripts/package-skill.sh
bash -n scripts/validate-skill.sh

parse_fixture_field() {
  local field="$1"
  printf '%s' '{"success":true,"data":{"note_id":"1914198881881698240"}}' | python3 -c '
import json, sys
field = sys.argv[1]
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
else:
    if field == "note_id":
        print(data.get("data", {}).get("note_id", ""))
    elif field == "success":
        success = data.get("success")
        code = data.get("code")
        if success is True or code in (0, "0", 200, "200"):
            print("true")
        else:
            print("false")
' "$field"
}

parse_success="$(parse_fixture_field success)"
parse_note_id="$(parse_fixture_field note_id)"

if [ "$parse_success" != "true" ] || [ "$parse_note_id" != "1914198881881698240" ]; then
  echo "JSON response parser check failed" >&2
  exit 1
fi

echo "Skill package validation passed."
