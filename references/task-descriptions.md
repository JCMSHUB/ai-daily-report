# OpenClaw 定时任务描述

本文件用于保存 OpenClaw 定时任务中可直接使用的任务描述。任务描述必须与 `SKILL.md`、`references/writing-template.md`、`references/event-quality.md`、`references/discovery-framework.md`、`references/publishing-checklist.md` 和 `references/personal-priorities.md` 保持一致。

---

# 每日 AI 情报简报任务

执行时间：

每天 20:30（Asia/Shanghai / CST）

任务描述：

```text
使用 ai-daily-report skill 生成今日 AI 个人情报简报。

执行时间：每天 20:30（Asia/Shanghai / CST）

必须严格按 skill 工作流执行，不得自由改写流程：

1. 每次运行都必须按阶段重新读取对应 reference，不得因为上一轮、昨天或同一会话中已读过而跳过。启动时读取 SKILL.md 和 references/personal-priorities.md（若存在）；Discovery 前只读取 references/discovery-framework.md 与 references/event-quality.md；写作前才读取 references/writing-template.md；发布前审核时才读取 references/publishing-checklist.md。
2. 使用 Tavily MCP 分批进行 Discovery 与 Verification；优先使用 tavily-remote。遇到 429 时将并发度降到 1，短暂退避后重试 1 次，再失败则切换 tavily-remote-2；遇到 432 或 433 时立即切换 tavily-remote-2。两个 Tavily 实例均不可用时，才允许使用 web_fetch 补充检索。
3. Discovery 与 Verification 阶段不得提前读取 references/writing-template.md 或 references/publishing-checklist.md，避免检索上下文被写作和发布规则占用。
4. Discovery 固定组织 5 个主题综合查询，每个主题层 1 次，默认使用 basic 或 fast、time_range=day、max_results=6~8，并关闭 raw content。同批查询尽量并发执行，建议并发度不超过 3；不得把示例关键词逐条串行搜索。
5. 将值得跟踪、值得尝试的行动意图合并进主题查询；可以忽略优先从 Discovery 的高热度低质量结果中产生，不固定追加噪音查询。若没有明显占据信息流且值得专门解释的噪音，允许省略可以忽略，不得为保留栏目追加搜索。
6. Discovery 后必须按底层事件去重和初筛，只保留约 6~8 个候选；写作前必须形成候选事件筛选表，包含事件、来源、评分、证据类型、Verification 状态、入选栏目或剔除原因；优先对已知原始 URL 批量调用 tavily_extract。只有缺少原始来源、商业事件缺第二信源或高风险事实仍不明确时，才使用 advanced、max_results=3~5 执行 1~3 次定向 Verification。
7. 目标 Tavily 总调用量为 7~9 次；仅当事实质量门槛未满足时允许超出，不得为了减少调用跳过必要验证。
8. 默认检索最近约 24 小时的 AI 领域高信号变化，重点服务个人注意力分配、工具选择、学习重点和后续行动。
9. 搜索目标不是收集新闻数量，而是筛选：值得跟踪的信息、值得尝试的工具/模型/论文/repo/API、可以忽略的高热度噪音，以及可形成趋势判断的信号。
10. 所有核心事实必须有可信来源，优先使用官方公告、GitHub、Hugging Face、arXiv、API 文档、监管机构文件或 Reuters/Bloomberg/FT/The Information/SemiAnalysis 等高质量信源。无法验证的内容必须剔除。
11. 写作前读取并严格使用 references/writing-template.md 的 Markdown 结构输出：今日结论、值得跟踪、值得尝试、可以忽略、趋势判断、我的行动清单、底部数据截止时间；模板允许省略的栏目可以省略。趋势判断信号不足时不得强写。
12. 推荐正文长度 2500-6000 个中文字符，最高不超过 8000。低于推荐范围不视为失败，事实质量、信息密度和行动价值优先。禁止为满足字数扩写、重复表达、加入空泛分析，或把数字改写成中文表达来凑字数。
13. 保存前必须读取 references/publishing-checklist.md 并完成自检；不合格内容必须删除、降级或补充验证。
14. 最终必须以标准 Markdown 保存到 Get笔记，并归档到指定知识库。优先执行 `python3 scripts/save-to-getnote.py`；脚本或 Get笔记保存失败时，本次任务不得视为成功。本地保存只是故障保底，不算任务成功。
15. 输出结果需返回 Get笔记有效访问链接，并明确数据截止时间。
```

---

# 每周 AI 情报周报任务

建议执行时间：

每周日 21:00（Asia/Shanghai / CST）

任务描述：

```text
使用 ai-daily-report skill 生成本周 AI 个人情报周报。

执行时间：每周日 21:00（Asia/Shanghai / CST）

必须严格按 skill 工作流执行，不得自由改写流程：

1. 每次运行都必须按阶段重新读取对应 reference，不得因为上一轮、昨天或同一会话中已读过而跳过。启动时读取 SKILL.md 和 references/personal-priorities.md（若存在）；补充检索和事实复核前只读取 references/discovery-framework.md 与 references/event-quality.md；写作前才读取 references/writing-template.md；发布前审核时才读取 references/publishing-checklist.md。
2. 周报不是七篇日报的简单拼接，而是对最近 7 天 AI 高信号事件的再筛选、去重、归纳和判断。
3. 补充检索、事实复核和 Verification 阶段不得提前读取 references/writing-template.md 或 references/publishing-checklist.md，避免检索上下文被写作和发布规则占用。
4. 使用 Tavily MCP 进行补充检索与事实复核；优先复用本周简报中的原始 URL 并批量调用 tavily_extract，只对缺口执行定向 advanced Verification。可并发的独立查询应同批执行，建议并发度不超过 3。优先使用 tavily-remote；遇到 429 时降低并发并退避重试，遇到 432 或 433 时立即切换 tavily-remote-2。两个 Tavily 实例均不可用时，才允许使用 web_fetch 补充检索。
5. 优先整合本周已经生成的 AI 简报内容；若本周 Get笔记或本地简报可访问，应先读取本周记录，再补充检索缺失信息。
6. 搜索和筛选目标是回答：本周哪些变化值得持续跟踪，哪些工具/模型/论文/repo/API 值得尝试，哪些热闹信息可以忽略，下周应该采取什么行动。
7. 所有核心事实必须有可信来源，优先使用官方公告、GitHub、Hugging Face、arXiv、API 文档、监管机构文件或 Reuters/Bloomberg/FT/The Information/SemiAnalysis 等高质量信源。无法验证的内容必须剔除。
8. 写作前读取并严格使用 references/writing-template.md 的周报变体：标题为「AI 情报周报 — YYYY-Www」，将「今日结论」改为「本周结论」，将「我的行动清单」改为「下周行动清单」，其余结构保持一致。
9. 推荐正文长度 3500-7000 个中文字符，最高不超过 9000。低于推荐范围不视为失败，事实质量、信息密度和行动价值优先。禁止为满足字数扩写、重复表达、加入空泛分析，或把数字改写成中文表达来凑字数。
10. 保存前必须读取 references/publishing-checklist.md 并完成自检；不合格内容必须删除、降级或补充验证。
11. 最终必须以标准 Markdown 保存到 Get笔记，并归档到指定知识库。优先执行 `python3 scripts/save-to-getnote.py`；脚本或 Get笔记保存失败时，本次任务不得视为成功。本地保存只是故障保底，不算任务成功。
12. 输出结果需返回 Get笔记有效访问链接，并明确本周统计周期和数据截止时间。
```
