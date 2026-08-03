#!/usr/bin/env python3
"""Audit an OpenClaw AI-report trace and its rendered Markdown.

The auditor is intentionally read-only and uses deterministic checks only.
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}
REQUIRED_CANDIDATE_COLUMNS = {
    "事件键": ("事件键",),
    "事件与时间": ("事件与时间",),
    "前一状态": ("前一状态",),
    "当前状态": ("当前状态", "当前发布状态"),
    "实质增量": ("实质增量",),
    "主要来源": ("主要来源",),
    "决策影响": ("决策影响",),
    "缺口": ("缺口", "事实缺口"),
    "评分": ("评分",),
    "Verification": ("Verification", "验证状态"),
    "处理": ("处理", "唯一主栏目", "剔除原因"),
}
LOW_SIGNAL_FORBIDDEN_HEADINGS = ("值得跟踪", "值得尝试", "可以忽略", "行动清单")


@dataclass
class Finding:
    rule_id: str
    severity: str
    title: str
    evidence: str
    recommendation: str


def walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def strings_for_keys(data, keys):
    values = []
    for value in walk(data):
        if not isinstance(value, dict):
            continue
        for key in keys:
            item = value.get(key)
            if isinstance(item, str) and item not in values:
                values.append(item)
    return values


def combined_model_input(data):
    return "\n".join(strings_for_keys(data, ("GenAIInput", "gen_ai.input")))


def combined_model_output(data):
    return "\n".join(strings_for_keys(data, ("GenAIOutput", "gen_ai.output")))


def tool_records(data):
    records = []
    for value in walk(data):
        if not isinstance(value, dict):
            continue
        identifiers = []
        for key, item in value.items():
            normalized = key.lower().replace(".", "_")
            if not isinstance(item, str):
                continue
            if normalized in {
                "tool_name", "name", "operation_name", "call_api_name",
                "call_resource_name", "call_service_name", "span_name",
            } or normalized.endswith(("tool_name", "operation_name")):
                identifiers.append(item.lower())
        identity = " ".join(identifiers)
        if not any(token in identity for token in ("tavily", "tool_call", "mcp", "__tavily_")):
            continue
        records.append(value)
    return records


def count_tools(records, pattern):
    matcher = re.compile(pattern, re.IGNORECASE)
    return sum(bool(matcher.search(json.dumps(record, ensure_ascii=False))) for record in records)


def candidate_headers(text):
    lines = text.splitlines()
    for index, line in enumerate(lines[:-1]):
        if "候选筛选表" not in "\n".join(lines[max(0, index - 2):index + 1]):
            continue
        if line.count("|") < 2:
            continue
        next_line = lines[index + 1]
        if re.fullmatch(r"[|:\- ]+", next_line.strip()):
            return [part.strip() for part in line.strip().strip("|").split("|")]
    return []


def headings(markdown):
    return [match.group(1).strip() for match in re.finditer(r"^#{2,6}\s+(.+)$", markdown, re.MULTILINE)]


def add(findings, rule_id, severity, title, evidence, recommendation):
    findings.append(Finding(rule_id, severity, title, evidence, recommendation))


def audit(data, report):
    findings = []
    model_input = combined_model_input(data)
    model_output = combined_model_output(data)
    records = tool_records(data)
    search_count = count_tools(records, r"tavily[^\n\"]*search|__tavily_search")
    extract_count = count_tools(records, r"tavily[^\n\"]*extract|__tavily_extract")

    if not records:
        add(
            findings, "TRACE001", "error", "Trace 缺少工具子调用",
            "输入中只有模型请求/响应，无法核验搜索、提取、读取和发布调用。",
            "按 trace_id 导出完整 Trace，包含 MCP/tool client spans。",
        )

    if "Discovery complete" in model_output and search_count == 0:
        add(
            findings, "TRACE002", "error", "Discovery 完成声明无工具证据",
            "模型声明 Discovery complete，但 Trace 中未找到 tavily_search 子调用。",
            "不得以模型阶段声明代替五个主题层的实际搜索记录。",
        )

    verification_claimed = bool(re.search(r"verification (?:is )?(?:essentially )?complete|验证完成|均完成逐项核验", model_output, re.IGNORECASE))
    if verification_claimed and extract_count == 0:
        add(
            findings, "TRACE003", "error", "Verification 完成声明无提取证据",
            "模型声明 Verification 完成，但 Trace 中未找到 tavily_extract 子调用。",
            "导出提取子 Span；若确无调用，则不能标记证据验证通过。",
        )

    template_positions = [match.start() for match in re.finditer(r"reading the writing template|读取写作模板", model_output, re.IGNORECASE)]
    later_verification = [match.start() for match in re.finditer(r"now verifying|cross-source check|核验", model_output, re.IGNORECASE)]
    if template_positions and any(position > template_positions[0] for position in later_verification):
        add(
            findings, "PHASE001", "error", "写作模板读取过早",
            "模型在声明读取写作模板后仍继续验证候选或补充来源。",
            "全部候选表和原子事实记录完成后才可读取写作模板。",
        )

    headers = candidate_headers(model_output)
    if not headers:
        add(
            findings, "CAND001", "error", "缺少可解析的候选筛选表",
            "模型输出中未找到 Markdown 候选筛选表。",
            "保存结构化候选记录，并在审计输入中包含该产物。",
        )
    else:
        missing = [
            label for label, aliases in REQUIRED_CANDIDATE_COLUMNS.items()
            if not any(alias in headers for alias in aliases)
        ]
        if missing:
            add(
                findings, "CAND002", "error", "候选筛选表字段不完整",
                "缺少字段：" + "、".join(missing) + "。",
                "补齐候选契约字段后再允许写作。",
            )

    atomic_summary = re.search(r"原子事实证据记录.{0,800}", model_output, re.DOTALL)
    if atomic_summary and not all(token in atomic_summary.group(0) for token in ("URL", "证据原文", "验证结果")):
        add(
            findings, "EVID001", "error", "原子事实记录不可核验",
            "只找到汇总声明，缺少逐项 URL、证据原文或准确释义、验证结果。",
            "每个正文核心事实保存一条结构化证据记录。",
        )

    if report:
        report_headings = headings(report)
        low_signal = "低信号" in report
        forbidden = [heading for heading in report_headings if any(token in heading for token in LOW_SIGNAL_FORBIDDEN_HEADINGS)]
        if low_signal and forbidden:
            add(
                findings, "REPORT001", "error", "低信号正文保留了常规栏目",
                "检测到栏目：" + "、".join(forbidden) + "。",
                "低信号期只保留结论、扫描依据和时间底注。",
            )

    if "最新最多 7 期" in model_input and "每日 AI 情报简报" in model_input:
        add(
            findings, "DRIFT001", "warning", "日报历史对照规则可能漂移",
            "Cron 输入要求日报读取最新最多 7 期；当前规则应为最多 3 期。",
            "重新部署 references/task-descriptions.md 中的当前日报任务文本。",
        )
    if "两个实例均不可用时才可用 web_fetch" in model_input:
        add(
            findings, "DRIFT002", "warning", "Tavily 失败降级规则已过期",
            "Cron 输入仍允许两个实例失败后使用 web_fetch。",
            "同步当前规则：两个实例均不可用时终止任务。",
        )

    if "发布成功" in model_output and not re.search(r"https://biji\.com/note/\d+", model_output):
        add(
            findings, "PUBLISH001", "error", "发布成功声明缺少有效链接",
            "模型声称发布成功，但输出中没有 Get笔记访问链接。",
            "仅在保存、知识库归档、本地副本均成功后记录链接。",
        )

    findings.sort(key=lambda item: (SEVERITY_ORDER[item.severity], item.rule_id))
    status = "fail" if any(item.severity == "error" for item in findings) else "pass"

    def dimension(prefixes):
        selected = [item for item in findings if item.rule_id.startswith(prefixes)]
        if any(item.severity == "error" for item in selected):
            return "fail"
        if any(item.severity == "warning" for item in selected):
            return "warning"
        return "pass"

    return {
        "status": status,
        "dimensions": {
            "execution_status": dimension(("TRACE", "PHASE")),
            "evidence_status": dimension(("CAND", "EVID")),
            "content_status": dimension(("REPORT",)),
            "publish_status": dimension(("PUBLISH",)),
            "configuration_status": dimension(("DRIFT",)),
        },
        "summary": {
            "errors": sum(item.severity == "error" for item in findings),
            "warnings": sum(item.severity == "warning" for item in findings),
            "tool_records": len(records),
            "tavily_search_records": search_count,
            "tavily_extract_records": extract_count,
        },
        "findings": [asdict(item) for item in findings],
    }


def markdown_result(result):
    lines = [
        "# AI 简报执行审计",
        "",
        f"- 状态：`{result['status']}`",
        f"- 执行：`{result['dimensions']['execution_status']}`",
        f"- 证据：`{result['dimensions']['evidence_status']}`",
        f"- 正文：`{result['dimensions']['content_status']}`",
        f"- 发布：`{result['dimensions']['publish_status']}`",
        f"- 配置：`{result['dimensions']['configuration_status']}`",
        f"- 错误：{result['summary']['errors']}",
        f"- 警告：{result['summary']['warnings']}",
        f"- 工具记录：{result['summary']['tool_records']}",
        "",
    ]
    for item in result["findings"]:
        lines.extend((
            f"## [{item['severity'].upper()}] {item['rule_id']} — {item['title']}",
            "",
            f"- 证据：{item['evidence']}",
            f"- 建议：{item['recommendation']}",
            "",
        ))
    if not result["findings"]:
        lines.extend(("未发现规则违规。", ""))
    return "\n".join(lines)


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path, help="APM/OpenTelemetry Trace JSON")
    parser.add_argument("--report", type=Path, help="最终日报或周报 Markdown")
    parser.add_argument("--json-out", type=Path, help="结构化审计结果路径")
    parser.add_argument("--markdown-out", type=Path, help="人类可读审计结果路径")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    try:
        data = json.loads(args.trace.read_text(encoding="utf-8"))
        report = args.report.read_text(encoding="utf-8") if args.report else ""
    except (OSError, json.JSONDecodeError) as exc:
        print(f"读取审计输入失败: {exc}", file=sys.stderr)
        return 2

    result = audit(data, report)
    json_text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    markdown_text = markdown_result(result)
    if args.json_out:
        args.json_out.write_text(json_text, encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.write_text(markdown_text, encoding="utf-8")
    if not args.json_out and not args.markdown_out:
        print(markdown_text, end="")
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
