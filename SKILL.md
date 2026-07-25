---
name: ai-daily-report
description: 为 AI 行业从业者、研究员、投资人与技术领袖生成面向个人注意力分配的中文 AI 情报简报：通过 Tavily MCP 发现近期可验证的一手信号，筛选值得跟踪、试用或忽略的信息，并写入 Get笔记。
metadata: {"openclaw":{"emoji":"📰","requires":{},"services":[{"name":"get-note","required":true,"description":"必需。OpenClaw 云端已部署的 Get笔记能力，通过 scripts/save-to-getnote.py 保存 Markdown 简报，并保留本地近期副本。"}]}}
---

# AI 个人情报简报

当用户要求生成 AI 日报、AI 行业简报、AI 新闻摘要，或面向 AI 领域的个人情报简报时，使用此 skill。

目标不是覆盖新闻，而是在有限注意力内回答：什么改变了判断，下一步该做什么，什么不值得分心。

## 不可跳过的契约

1. 每次运行均按阶段重新读取所需 reference；不得复用上一轮、昨天或同一会话的读取结果。
2. Discovery 与 Verification 前只读取 `references/discovery-framework.md`、`references/event-quality.md` 和存在时的 `references/personal-priorities.md`。不得提前读取写作模板或发布 checklist。
3. Discovery 后按底层事件去重，并查询本地近期简报目录中最新最多 7 期与一手来源时间线，核对是否有新增量；历史简报只用于事件对照，不能替代本次检索和验证。
4. 先完成候选事件筛选表，再只对入围候选执行分级 Verification。最终候选的每项核心主张必须有原子事实证据记录。
5. 只有全部最终候选通过写作前证据准入，才读取 `references/writing-template.md`；保存前读取 `references/publishing-checklist.md` 并逐项自检。未通过则删除、降级或补证。
6. 最终必须调用 `python3 {baseDir}/scripts/save-to-getnote.py <markdown_file>` 保存并归档到 Get笔记。脚本或归档失败时，任务不得视为成功。

禁止：以模型记忆、通用新闻摘要或旧上下文代替检索；以结果数量、字符数或栏目完整性为目标；跳过 Verification、筛选表、写作前证据准入或发布前检查。

## 运行环境与降级

使用 `{baseDir}` 定位随附文件。此 skill 依赖 Tavily MCP，优先使用 `tavily-remote`，备用为 `tavily-remote-2`。

- 429：并发降至 1，短暂退避后重试 1 次；仍失败则切换实例。
- 432 或 433：立即切换实例。
- 两个实例都不可用：仅可用 `web_fetch` 补足必要证据，并在输出中说明检索降级。

本地近期简报目录默认为 `~/.openclaw/ai-daily-report/recent-reports`，可用 `AI_DAILY_REPORT_LOCAL_DIR` 覆盖。保存脚本在每次成功发布后写入一份 Markdown 副本，并删除超过 `AI_DAILY_REPORT_RETENTION_DAYS` 的文件；默认保留 14 天。

## 1. 确定窗口

从运行环境取得中国时区的真实当前时间。未指定范围时，默认覆盖最近约 24 小时；只有在窗口内首次发布，或有可验证的实质更新，才可作为当天核心事件。历史资料只能标为背景。

简报底部标注数据截至时间（CST / 中国时间）。

## 2. 阶段化读取

### 启动

读取 `SKILL.md` 与存在时的 `references/personal-priorities.md`，只用于确定个人优先级和降权主题。

### Discovery 与 Verification 前

重新读取：

- `references/discovery-framework.md`
- `references/event-quality.md`
- `references/personal-priorities.md`（存在时）

此阶段不得读取：

- `references/writing-template.md`
- `references/publishing-checklist.md`

### 写作前与发布前

写作前读取 `references/writing-template.md`；完成 Markdown 后才读取 `references/publishing-checklist.md`。

`references/task-descriptions.md` 是每日与每周定时任务的配置文本，修改工作流时必须同步维护。

## 3. Discovery：寻找事件增量

按照 `discovery-framework.md` 组织五个主题层的初始综合查询：Frontier Models、Agent Runtime、Inference Infrastructure、Open Source Ecosystem、Governance & Regulation。

每条查询应包含：主题实体或技术锚点、实质事件词（例如 release、pricing、benchmark、policy、security、availability）以及时间窗口。目标是找“发生了什么变化”，不是找主题页面或观点文章。

执行规则：

- 每层 1 条综合查询，同批并发，建议并发不超过 3。
- 默认 `search_depth: basic`（支持时可用 `fast`）、`time_range: day`、`max_results: 6~8`、`include_raw_content: false`。
- 优先让官方公告、GitHub、Hugging Face、arXiv、API/release 文档和监管文件进入候选池；高质量媒体用于发现或交叉验证，不能替代可获得的一手材料。
- 不把示例关键词逐条搜索；不为“可以忽略”栏目额外制造噪音查询。
- 某主题无合格候选时，最多追加 1 条带明确实体和缺口的 `advanced` 查询，不能用泛化查询补数量。

## 4. 候选筛选与 Verification

先按底层事件聚类：同一发布、同一文件、同一产品更新或同一交易只是一件事；转载数量不是独立信号。Discovery 形成候选后，列出本地近期简报目录中按修改时间排序的最新最多 7 个 Markdown，只用候选的实体、对象、版本和事件键搜索匹配内容，并读取命中段落，不整篇加载无关旧简报。再查明一手来源中的前一状态与当前状态。旧事件只有出现会改变判断或行动的新状态、新数据、新能力、新风险或新入口时才能再次入选。

每个候选先填写内部筛选表：事件键、事件与时间、前一状态、当前发布状态、相对近期简报或来源时间线的实质增量、主要来源与等级、受影响的决策、事实缺口、评分、Verification 状态、唯一主栏目或剔除原因。只有先通过以下四个门槛的候选才评分：

1. 有明确实体、动作、对象和结果。
2. 有窗口内的首次发布或实质更新证据。
3. 技术与治理事件有可获得的一手来源；确实没有公开一手材料的商业事件有两个独立 B 级来源。
4. 能改变工具选择、学习、部署判断、风险判断或后续观察对象之一。

通过门槛后，按 `event-quality.md` 评分。来源质量只衡量证据可靠性，不能单独把事件推入正文；没有行动或判断增量的可靠信息仍应剔除。

对入围候选优先把已知原始 URL 批量传给 `tavily_extract`。只在下列情况进行 1~3 次、按事件合并的 `advanced` Verification Search：需定位一手来源、商业事件缺第二个独立来源、高风险事实未明确，或趋势判断缺第二个独立事件。

验证时逐项检查最终会写入的核心主张，而不只核对标题。为每项核心主张记录：原子事实、发布状态、事件时间、证据 URL、证据原文或准确释义、来源等级和验证结果。`announced`、`preview`、`available`、`weights released` 与 `GA` 是不同状态，不得互相替换。技术事件以原始技术材料为准；商业事件需要两个独立 B 级来源，或当事方正式文件加一个独立 B 级来源；治理事件以监管、法院或政府文件为准。无法验证、时间不在窗口内、状态矛盾或没有决策增量的候选直接剔除。

写作前执行证据准入：每个最终候选必须完成候选筛选表和原子事实证据记录，所有将写入正文的事实均验证通过，且已确定唯一主栏目。任一候选存在来源缺失、事件时间不明、状态矛盾、证据无法定位或没有相对既有状态的实质增量时，不得读取写作模板；先删除候选或补齐证据。

没有足够高质量事件时，输出更短简报是正确结果；不得用低价值项目补足主题、栏目或篇幅。

## 5. 写作

通过写作前证据准入后，读取 `references/writing-template.md`，严格采用其章节结构与 Markdown 规则。模板明确允许省略的栏目可以省略。

对每项核心内容：

- 先写可追溯事实，再写基于事实的判断，最后写行动或观察。
- 事实、推断和建议不得混写为确定事实。
- 每个判断都应能回答反事实问题：若这件事没有发生，读者的选择或观察重点是否会不同？若不会，不进核心正文。
- 信源必须链接到实际支撑该主张的具体页面；高风险或商业主张按模板给出交叉来源。
- 每个底层事件只进入一个正文主栏目；结论、趋势和行动可以引用它，但不得把同一事实重新包装成多个项目。
- 趋势判断只能使用正文中已经验证的至少两个独立底层事件，不得在趋势段落引入新事件或未验证事实。

中文输出，使用标准 Markdown。以信息密度决定篇幅，最高 8000 个中文字符；没有最小长度要求。

## 6. 发布

完成正文后读取 `references/publishing-checklist.md`。任何未通过项必须修正后再发布。

执行：

```bash
python3 {baseDir}/scripts/save-to-getnote.py ai-daily-report-YYYY-MM-DD.md
```

成功条件：Markdown 已保存、知识库归档成功、返回有效访问链接，并已写入本地近期简报目录。若 API 与脚本均失败，可保留原始本地 Markdown 作为故障产物，但最终回复必须明确“Get笔记发布失败，任务未成功完成”。

## 最终交付

返回 Get笔记有效访问链接和数据截至时间。最终简报应让读者仅看“今日结论”和“我的行动清单”也能决定今天要读、试、跟踪什么，以及哪些信息可以忽略。
