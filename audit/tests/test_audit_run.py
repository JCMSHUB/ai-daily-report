import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "audit_run.py"
SPEC = importlib.util.spec_from_file_location("audit_run", MODULE_PATH)
audit_run = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_run)


class AuditRunTests(unittest.TestCase):
    def test_root_span_exposes_missing_evidence_and_phase_violation(self):
        data = {
            "operation_name": "openclaw_request",
            "GenAIInput": "每日 AI 情报简报 最新最多 7 期 两个实例均不可用时才可用 web_fetch",
            "GenAIOutput": (
                "Discovery complete. All verification complete. "
                "Now reading the writing template before composing. "
                "Now verifying two additional candidates.\n\n"
                "候选筛选表（内部记录）\n"
                "| 事件键 | 事件与时间 | 前一状态 | 当前状态 | 实质增量 | 主要来源 | 评分 | Verification | 处理 |\n"
                "|---|---|---|---|---|---|---|---|---|\n"
                "| A | now | old | new | yes | official | 80 | PASS | 跟踪 |\n\n"
                "原子事实证据记录：均完成逐项核验。\n"
                "发布成功 https://biji.com/note/123"
            ),
        }
        report = "# 日报\n\n## 今日结论\n\n低信号日。\n\n## 值得跟踪\n\n旧事件。\n"
        result = audit_run.audit(data, report)
        ids = {item["rule_id"] for item in result["findings"]}
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["dimensions"]["execution_status"], "fail")
        self.assertEqual(result["dimensions"]["evidence_status"], "fail")
        self.assertEqual(result["dimensions"]["content_status"], "fail")
        self.assertEqual(result["dimensions"]["configuration_status"], "warning")
        self.assertTrue({
            "TRACE001", "TRACE002", "TRACE003", "PHASE001", "CAND002",
            "EVID001", "REPORT001", "DRIFT001", "DRIFT002",
        }.issubset(ids))

    def test_minimal_trace_and_complete_candidate_table_pass(self):
        columns = " | ".join(alias[0] for alias in audit_run.REQUIRED_CANDIDATE_COLUMNS.values())
        data = {
            "spans": [
                {"tool_name": "tavily-remote__tavily_search", "request": {"query": "release last day"}},
                {"tool_name": "tavily-remote__tavily_extract", "request": {"url": "https://example.com"}},
            ],
            "GenAIOutput": (
                "Discovery complete. Verification complete.\n\n"
                "候选筛选表\n"
                f"| {columns} |\n"
                f"| {' | '.join(['---'] * len(audit_run.REQUIRED_CANDIDATE_COLUMNS))} |\n"
                f"| {' | '.join(['ok'] * len(audit_run.REQUIRED_CANDIDATE_COLUMNS))} |\n\n"
                "原子事实证据记录：URL；证据原文；验证结果。\n"
                "发布成功 https://biji.com/note/123"
            ),
        }
        result = audit_run.audit(data, "# 日报\n\n## 今日结论\n\n有信号。\n")
        self.assertEqual(result["status"], "pass", result["findings"])
        self.assertTrue(all(status == "pass" for status in result["dimensions"].values()))


if __name__ == "__main__":
    unittest.main()
