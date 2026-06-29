#!/usr/bin/env python3
"""Save an ai-daily-report Markdown file to Get笔记 and archive it."""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


SAVE_URL = "https://openapi.biji.com/open/api/v1/resource/note/save"
ARCHIVE_URL = "https://openapi.biji.com/open/api/v1/resource/knowledge/note/batch-add"
DEFAULT_CONFIG_FILE = "/root/.openclaw/openclaw.json"
DEFAULT_TOPIC_ID = "G0P13z4J"


def load_openclaw_env(config_file):
    if not config_file.is_file():
        return {}
    try:
        with config_file.open(encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}
    return data.get("skills", {}).get("entries", {}).get("getnote", {}).get("env", {})


def first_heading(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return "AI情报简报"


def is_success(response):
    return response.get("success") is True or response.get("code") in (0, "0", 200, "200")


def note_id_from(response):
    return str(response.get("data", {}).get("note_id", "") or "")


def post_json(url, payload, api_key, client_id):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": api_key,
            "X-Client-ID": client_id,
            "Content-Type": "application/json",
        },
    )
    timeout = float(os.environ.get("GETNOTE_MAX_TIME", "30"))
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON response: {raw}") from exc


def credentials():
    config_file = Path(os.environ.get("OPENCLAW_CONFIG_FILE", DEFAULT_CONFIG_FILE))
    config_env = load_openclaw_env(config_file)
    api_key = os.environ.get("GETNOTE_API_KEY") or config_env.get("GETNOTE_API_KEY", "")
    client_id = os.environ.get("GETNOTE_CLIENT_ID") or config_env.get("GETNOTE_CLIENT_ID", "")
    if not api_key or not client_id:
        raise RuntimeError("Get笔记凭证未配置：需要 GETNOTE_API_KEY / GETNOTE_CLIENT_ID，或 OpenClaw getnote 配置。")
    return api_key, client_id


def save(markdown_file):
    if not markdown_file.is_file():
        raise RuntimeError(f"Markdown 文件不存在: {markdown_file}")

    markdown = markdown_file.read_text(encoding="utf-8")
    api_key, client_id = credentials()
    title = first_heading(markdown)
    topic_id = os.environ.get("GETNOTE_TOPIC_ID", DEFAULT_TOPIC_ID)
    note_type = os.environ.get("GETNOTE_NOTE_TYPE", "plain_text")

    save_payload = {
        "title": title,
        "content": markdown,
        "note_type": note_type,
        "tags": ["AI情报简报"],
    }
    save_response = post_json(SAVE_URL, save_payload, api_key, client_id)
    note_id = note_id_from(save_response)
    if not is_success(save_response) or not note_id:
        raise RuntimeError("保存失败:\n" + json.dumps(save_response, ensure_ascii=False, indent=2))

    print(f"已将 Markdown 内容保存到 Get笔记 -> https://biji.com/note/{note_id}")

    archive_payload = {"topic_id": topic_id, "note_ids": [note_id]}
    archive_response = post_json(ARCHIVE_URL, archive_payload, api_key, client_id)
    if not is_success(archive_response):
        raise RuntimeError("归入知识库失败:\n" + json.dumps(archive_response, ensure_ascii=False, indent=2))

    print(f"已归入知识库（{topic_id}）")


def main(argv):
    if len(argv) != 2:
        print(f"用法: {Path(argv[0]).name} <markdown_file>", file=sys.stderr)
        return 1
    try:
        save(Path(argv[1]))
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
