# OpenClaw 定时任务描述

本文件是定时任务的执行契约，必须与 `SKILL.md` 和各 reference 保持一致。定时任务不能以既有会话、昨日读取或历史简报代替本次规定的检索与验证。

## 每日 AI 情报简报

执行时间：每天 20:30（Asia/Shanghai / CST）

```text
使用 ai-daily-report skill 生成今日 AI 个人情报简报。

每次运行必须严格执行以下契约：

1. 按阶段重新读取 reference，不得因为上一轮、昨天或同一会话中已读过而跳过。启动时读取 SKILL.md 和 references/personal-priorities.md（存在时）；Discovery 与 Verification 前只读取 references/discovery-framework.md 和 references/event-quality.md；写作前才读取 references/writing-template.md；发布前才读取 references/publishing-checklist.md。Discovery/Verification 不得提前加载模板或 checklist。
2. 获取真实中国时间，默认检索最近约 24 小时。只有窗口内首次发布或有可验证实质更新的内容可作为当天核心事件；历史内容只能作背景。
3. Tavily 优先使用 tavily-remote。429 时并发降至 1、短暂退避重试一次，再失败切换 tavily-remote-2；432/433 立即切换。两个实例均不可用时才可用 web_fetch 补足必要证据，并说明降级。
4. Discovery 执行五个主题层各一条综合查询：Frontier Models、Agent Runtime、Inference Infrastructure、Open Source Ecosystem、Governance & Regulation。查询必须包含实体/技术锚点、实质事件词和时间/证据意图；不得逐条搜索示例关键词或用泛化 news 查询。默认 basic 或支持时 fast、time_range=day、max_results=6~8、关闭 raw content；并发建议不超过 3。
5. 搜索结果先按底层事件去重，形成内部候选筛选表：事件与时间、实质增量、来源、证据类型、决策影响、缺口、评分、Verification 状态、入选或剔除原因。候选必须先满足完整事实、窗口内增量、可追溯证据、决策相关性四个硬门槛，再按 event-quality.md 评分。可靠来源本身不能代替决策价值。
6. 只验证入围候选：优先批量 tavily_extract 已知原始 URL；仅为缺原始来源、商业事实缺独立第二来源、高风险主张不明确或趋势证据不足而执行 1~3 次按事件合并的 advanced Verification。技术事实优先原始材料；商业事实需两个独立高质量来源；治理事实优先官方文件。无法验证的内容直接剔除。
7. 不得为主题覆盖、栏目、调用预算、字数或“可以忽略”栏目补内容。没有足够信号时输出更短简报，或省略值得尝试、可以忽略、趋势判断等模板允许省略的栏目。
8. 写作严格使用 references/writing-template.md：每项按事实、判断、行动/观察区分；判断必须能指向证据，行动清单最多 3 条且有对象、目的、完成条件和时间。标准 Markdown，正文最高 8000 个中文字符，无最低长度。
9. 发布前逐项执行 references/publishing-checklist.md。最终必须用 `python3 scripts/save-to-getnote.py <markdown_file>` 保存、归档到 Get笔记并返回有效访问链接与 CST 数据截至时间。脚本或归档失败时任务未成功完成；本地文件仅是故障产物。
```

## 每周 AI 情报周报

建议执行时间：每周日 21:00（Asia/Shanghai / CST）

```text
使用 ai-daily-report skill 生成本周 AI 个人情报周报。

每次运行必须按阶段重新读取对应 reference，禁止用上周会话或旧读取跳过流程：启动读取 SKILL.md 与 personal-priorities（存在时）；补充检索和 Verification 前只读取 discovery-framework 与 event-quality；写作前读取 writing-template；发布前读取 publishing-checklist。检索和复核阶段不得提前读取模板或 checklist。

周报不是七篇日报的拼接。先读取本周可访问的简报或记录作为线索，再用 Tavily 验证仍有价值的底层事件、去重并寻找本周新增的实质证据。Tavily 实例切换、候选硬门槛、证据等级、Verification 路由、无填充原则与每日任务完全相同：技术事实以原始材料为准，商业事实需独立交叉验证，治理事实以官方文件为准，无法验证则剔除。

只保留改变下周工具、学习、部署、风险或观察优先级的事件。严格使用 writing-template 的周报变体：标题为「AI 情报周报 — YYYY-Www」，“今日结论”改为“本周结论”，“我的行动清单”改为“下周行动清单”；篇幅最高 9000 个中文字符，无最低长度。发布前逐项执行 checklist，并用 `python3 scripts/save-to-getnote.py <markdown_file>` 保存、归档到 Get笔记，返回有效链接、本周统计周期与数据截至时间；保存或归档失败时任务未成功完成。
```
