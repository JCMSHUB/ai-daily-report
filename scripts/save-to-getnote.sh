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

RESPONSE="$(curl -s -X POST "https://openapi.biji.com/open/api/v1/resource/note/save" \
  -H "Authorization: $API_KEY" \
  -H "X-Client-ID: $CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")"

NOTE_ID="$(printf '%s' "$RESPONSE" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
else:
    print(data.get("data", {}).get("note_id", ""))
' 2>/dev/null || true)"

if [ -n "$NOTE_ID" ]; then
  echo "已将 Markdown 内容保存到 Get笔记 -> https://biji.com/note/$NOTE_ID"
  # 自动归入 AI情报简报知识库
  TOPIC_RESP="$(curl -s -X POST "https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add" \
    -H "Authorization: $API_KEY" \
    -H "X-Client-ID: $CLIENT_ID" \
    -H "Content-Type: application/json" \
    -d "{\"topic_id\":\"$TOPIC_ID\",\"note_ids\":[\"$NOTE_ID\"]}")"
  TOPIC_OK="$(printf '%s' "$TOPIC_RESP" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("success",False))' 2>/dev/null || echo "false")"
  if [ "$TOPIC_OK" = "True" ]; then
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
