# AI 简报执行审计器

本目录提供独立于 `ai-daily-report` skill 的只读审计工具。它不修改 Trace、简报或 OpenClaw 配置，也不依赖执行模型的自评结果。

## 输入

- APM/OpenTelemetry 导出的完整 Trace JSON，最好包含根 Span 与 MCP/tool client 子 Span。
- 可选的最终日报或周报 Markdown。

只有根 Span 时仍可运行，但所有依赖工具证据的检查会失败，并提示导出完整 Trace。

## 使用

```bash
python3 audit/audit_run.py trace.json \
  --report ai-daily-report-2026-07-31.md \
  --json-out audit-result.json \
  --markdown-out audit-result.md
```

退出码：

- `0`：没有 error 级发现；
- `1`：存在 error 级发现；
- `2`：输入无法读取或 JSON 无效。

## 首版规则

- Trace 是否包含可核验的工具子调用；
- Discovery/Verification 完成声明是否有对应搜索或提取记录；
- 是否在候选与证据完成前读取写作模板；
- 候选筛选表字段是否完整；
- 原子事实是否保存 URL、证据内容和验证结果；
- 低信号正文是否错误保留常规栏目；
- Cron 注入文本是否仍包含已废弃的日报 7 期历史或 `web_fetch` 降级；
- 发布成功声明是否包含有效访问链接。

审计结果只说明可见证据是否满足规则。搜索是否漏掉现实中的重要事件仍需完整搜索结果和一手发布时间才能归因。

## 验证

```bash
python3 -m unittest discover -s audit/tests -v
```
