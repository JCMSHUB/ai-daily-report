#!/usr/bin/env bash
# ai-daily-report -> Get笔记 Markdown 内容保存脚本
# 用法: bash save-to-getnote.sh <markdown_file>

set -euo pipefail

MD_FILE="${1:-}"
if [ -z "$MD_FILE" ]; then
  echo "用法: $0 <markdown_file>" >&2
  exit 1
fi

if [ ! -f "$MD_FILE" ]; then
  echo "Markdown 文件不存在: $MD_FILE" >&2
  exit 1
fi

CONFIG_FILE="${OPENCLAW_CONFIG_FILE:-/root/.openclaw/openclaw.json}"

API_KEY="${GETNOTE_API_KEY:-}"
CLIENT_ID="${GETNOTE_CLIENT_ID:-}"

if [ -z "$API_KEY" ] && [ -f "$CONFIG_FILE" ]; then
  API_KEY="$(python3 - "$CONFIG_FILE" <<'PY' 2>/dev/null || true
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)
print(data.get("skills", {}).get("entries", {}).get("getnote", {}).get("env", {}).get("GETNOTE_API_KEY", ""))
PY
)"
fi

if [ -z "$CLIENT_ID" ] && [ -f "$CONFIG_FILE" ]; then
  CLIENT_ID="$(python3 - "$CONFIG_FILE" <<'PY' 2>/dev/null || true
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)
print(data.get("skills", {}).get("entries", {}).get("getnote", {}).get("env", {}).get("GETNOTE_CLIENT_ID", ""))
PY
)"
fi

if [ -z "$API_KEY" ] || [ -z "$CLIENT_ID" ]; then
  echo "Get笔记凭证未配置：需要 GETNOTE_API_KEY / GETNOTE_CLIENT_ID，或 OpenClaw getnote 配置。" >&2
  exit 1
fi

TITLE="$(python3 - "$MD_FILE" <<'PY'
import sys
title = ""
with open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            break
if not title:
    title = "AI情报简报"
print(title)
PY
)"

NOTE_TYPE="${GETNOTE_NOTE_TYPE:-plain_text}"

PAYLOAD="$(python3 - "$MD_FILE" "$TITLE" "$NOTE_TYPE" <<'PY'
import json, sys
path, title, note_type = sys.argv[1:4]
with open(path, encoding="utf-8") as f:
    content = f.read()

body = {
    "title": title,
    "content": content,
    "note_type": note_type,
    "tags": ["AI情报简报"]
}
print(json.dumps(body, ensure_ascii=False))
PY
)"

TOPIC_ID="${GETNOTE_TOPIC_ID:-G0P13z4J}"

post_json() {
  local url="$1"
  local payload="$2"
  curl --silent --show-error --fail \
    --connect-timeout "${GETNOTE_CONNECT_TIMEOUT:-10}" \
    --max-time "${GETNOTE_MAX_TIME:-30}" \
    -X POST "$url" \
    -H "Authorization: $API_KEY" \
    -H "X-Client-ID: $CLIENT_ID" \
    -H "Content-Type: application/json" \
    -d "$payload"
}

parse_json_field() {
  local field="$1"
  python3 - "$field" <<'PY'
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
PY
}

RESPONSE="$(post_json "https://openapi.biji.com/open/api/v1/resource/note/save" "$PAYLOAD")"

SAVE_OK="$(printf '%s' "$RESPONSE" | parse_json_field success 2>/dev/null || echo "false")"
NOTE_ID="$(printf '%s' "$RESPONSE" | parse_json_field note_id 2>/dev/null || true)"

if [ "$SAVE_OK" = "true" ] && [ -n "$NOTE_ID" ]; then
  echo "已将 Markdown 内容保存到 Get笔记 -> https://biji.com/note/$NOTE_ID"
  # 自动归入 AI情报简报知识库
  TOPIC_PAYLOAD="$(python3 - "$TOPIC_ID" "$NOTE_ID" <<'PY'
import json, sys
topic_id, note_id = sys.argv[1:3]
print(json.dumps({"topic_id": topic_id, "note_ids": [note_id]}, ensure_ascii=False))
PY
)"
  TOPIC_RESP="$(post_json "https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add" "$TOPIC_PAYLOAD")"
  TOPIC_OK="$(printf '%s' "$TOPIC_RESP" | parse_json_field success 2>/dev/null || echo "false")"
  if [ "$TOPIC_OK" = "true" ]; then
    echo "已归入知识库（$TOPIC_ID）"
  else
    echo "归入知识库失败:" >&2
    printf '%s\n' "$TOPIC_RESP" | python3 -m json.tool 2>/dev/null || printf '%s\n' "$TOPIC_RESP" >&2
    exit 1
  fi
else
  echo "保存失败:" >&2
  printf '%s\n' "$RESPONSE" | python3 -m json.tool 2>/dev/null || printf '%s\n' "$RESPONSE" >&2
  exit 1
fi
