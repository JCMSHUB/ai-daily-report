---
name: ai-daily-report
description: 为 AI 行业从业者、研究员、投资人与技术领袖生成面向个人注意力分配的中文 AI 情报简报：通过 Tavily MCP 检索近期一手信源、验证事实、过滤低价值 PR，提炼值得跟踪、值得尝试、可以忽略的信息，并写入 Get笔记。
metadata: {"openclaw":{"emoji":"📰","requires":{},"services":[{"name":"get-note","required":true,"description":"必需。OpenClaw 云端已部署的 Get笔记能力，通过 scripts/save-to-getnote.py 保存 Markdown 简报。"}]}}
---

# AI 个人情报简报

当用户要求生成 AI 日报、AI 行业简报、AI 新闻摘要，或面向 AI 领域的个人情报简报时，使用此 skill。

---

# 强制执行契约

执行本 skill 时，以下步骤不得跳过：

1. 每次任务运行都必须重新读取 `{baseDir}/references/source-quality.md`、`{baseDir}/references/search-keywords.md`、`{baseDir}/references/template.md`、`{baseDir}/references/output-checklist.md`；若存在 `{baseDir}/references/personal-priorities.md`，也必须读取；不得因为上一轮、昨天或同一会话中已读过而跳过。
2. 必须按 `search-keywords.md` 分批执行 Discovery，再按 `source-quality.md` 评分、按底层事件去重，只对入围候选执行分级 Verification。发布前必须形成候选事件筛选表；筛选表可作为内部工作产物，不必写入最终简报。
3. 必须严格使用 `template.md` 的章节结构与 Markdown 规则生成情报简报，不得自由改写栏目；模板明确允许省略的栏目除外。
4. 保存前必须按 `output-checklist.md` 完成逐项自检；未通过则必须修改简报，不能直接发布。
5. 必须通过 `python3 {baseDir}/scripts/save-to-getnote.py` 保存到 Get笔记并归档到指定知识库；脚本失败时任务不得视为成功。

禁止：

- 不读取 reference 文件直接生成简报，或以“上一轮已读过”为由复用旧上下文。
- 只依据通用新闻摘要或模型记忆生成简报。
- 跳过 Verification 阶段。
- 跳过候选事件筛选表。
- 跳过发布前 checklist。
- 只本地保存但不保存到 Get笔记。

---

# OpenClaw 兼容性

- 这是一个兼容 AgentSkills 的 OpenClaw skill 目录，由 `SKILL.md` 和可选文本参考资料组成。
- 读取随附资料时，通过 `{baseDir}` 定位：
  - `{baseDir}/references/source-quality.md`
  - `{baseDir}/references/search-keywords.md`
  - `{baseDir}/references/template.md`
  - `{baseDir}/references/output-checklist.md`
  - `{baseDir}/references/personal-priorities.md`（可选；存在时必须读取）
  - `{baseDir}/references/task-descriptions.md`
  - `{baseDir}/scripts/save-to-getnote.py`

- 此 skill 的设计强依赖 Tavily MCP。

配置两个 Tavily MCP 实例：

- tavily-remote
- tavily-remote-2

当一个实例返回 429：

- 降低并发度到 1。
- 短暂退避后重试 1 次。
- 再次失败时切换到另一个实例。

当一个实例返回 432 或 433：

立即切换到另一个实例重试。

若两个实例均已耗尽额度：

降级使用：

- web_fetch

补充检索。

---

# 最终交付要求

最终简报必须：

- 保存到 Get笔记
- 归档到指定知识库
- 返回有效访问链接

若发布失败：

任务不得视为成功。

---

# 工作流

## 1. 确定日期窗口

从运行环境获取真实当前日期与中国时区。

如果可以执行 shell：

优先运行：

```bash
TZ=Asia/Shanghai date '+%Y-%m-%d %H:%M CST'
```

除非用户指定其他日期范围：

默认检索最近约 24 小时内容。

简报底部必须标注：

数据截止时间（CST / 中国时间）。

---

## 2. 读取参考规则

每次任务运行时，检索和写作前都必须重新读取下列文件；不得复用上一轮、昨天或同一会话中的旧上下文：

### source-quality.md

职责：

Source & Event Quality Standard

定义：

- Event Intelligence Score
- Routing Rules
- Strategic Override Rules
- Fact Quality Rules
- Actionability Rules

用于筛选高价值事件。

---

### search-keywords.md

职责：

Search & Discovery Framework

定义：

- Discovery Layers
- Preferred Domains
- Lower-Priority Domains
- Noise Filters
- Success Criteria

用于发现高价值行业信号。

---

### template.md

职责：

Output Structure

定义情报简报最终结构。

包括：

- 今日结论
- 值得跟踪
- 值得尝试
- 可以忽略
- 趋势判断
- 我的行动清单

所有简报必须遵循该结构。`值得尝试`、`可以忽略`、`趋势判断` 在信号不足且模板允许时可以省略；若保留 `趋势判断` 标题但信号不足，必须明确写“今日无足够独立信号形成趋势判断”，不得把单条新闻扩写成趋势。

---

### output-checklist.md

职责：

Final Quality Review

定义：

- Event Selection Review
- Fact Quality Review
- Actionability Review
- Formatting Review
- Publishing Review

简报发布前必须通过全部检查。

---

## 3. 两阶段 Tavily 检索

### Discovery 阶段

使用 Tavily MCP 从高信噪比信源中发现候选事件。

必须从：

search-keywords.md

定义的 Discovery Framework 开始执行。

固定覆盖：

- Frontier Models
- Agent Runtime
- Inference Infrastructure
- Open Source Ecosystem
- Governance & Regulation

执行要求：

- 每个主题层只组织 1 个综合查询，共 5 个基础查询；示例关键词用于组合查询，不得逐条全部执行。
- 将 `值得跟踪`、`值得尝试` 的行动意图合并进主题查询，不再固定追加独立查询。
- `可以忽略` 优先从 Discovery 的高热度低质量结果中产生，不为凑栏目固定搜索噪音。
- 同一批查询应并发执行；建议并发度不超过 3。若运行时不支持并发，仍保持相同查询预算。

Discovery 推荐参数：

- search_depth: basic；延迟敏感且当前 Tavily 实例支持时可用 fast
- time_range: day
- max_results: 6~8
- include_raw_content: false

优先参考：

- GitHub
- Hugging Face
- arXiv
- 官方博客
- Reuters
- Bloomberg
- FT
- The Information
- SemiAnalysis

Discovery 完成后：

- 按底层事件聚类、URL 去重并完成初筛。
- 只保留约 6~8 个高分候选进入内容提取与 Verification。
- 若某关键方向没有合格候选，才允许增加 1 次定向 `advanced` 查询。

---

### Verification 阶段

只对入围候选事件进行验证。不得机械地为每个候选再执行一次搜索。

优先复用 Discovery 已获得的原始 URL：

- 将已知 URL 合并为一次 `tavily_extract` 批量提取。
- 若当前 MCP 仅支持单 URL，则在同一批次并发提取，禁止逐条串行。
- 已由官方原始材料完整支持的技术事实，无需再次搜索同一事实。

技术类事件优先验证：

- GitHub
- API
- Benchmark
- Model Card
- Release Note
- Documentation

商业类事件：

至少两个高质量来源交叉验证。

治理类事件：

优先监管机构与官方文件。

只有在以下情况增加定向 Verification Search：

- 缺少原始来源。
- 商业事件缺少第二个独立高质量来源。
- 高风险数字、benchmark、监管命令或能力声明仍不明确。
- 趋势判断的关键支持信号不足。

Verification 推荐参数：

- search_depth: advanced
- max_results: 3~5

将需要补证的候选按底层事件合并，通常并发执行 1~3 次定向查询。Discovery、提取和 Verification 的目标总调用量为 7~9 次；仅当事实质量门槛未满足时允许超出，不能为满足调用预算降低验证标准。

无法验证的事件：

直接剔除。

---

## 4. 筛选与去重

按照：

source-quality.md

执行。

要求：

- 按底层事件去重
- 优先原始信源
- 保留技术增量
- 保留战略价值

剔除：

- PR宣传
- SEO内容
- 洗稿转载
- 无技术增量内容

发布前必须形成候选事件筛选表，至少包含：

- 事件
- 主要来源
- 综合评分
- 证据类型
- Verification 状态
- 入选栏目或剔除原因

筛选表用于执行审计，不要求写入最终简报；但若无法说明某事件为什么入选或剔除，必须重新筛选。

---

## 5. 撰写情报简报

严格遵循：

template.md

定义结构。

要求：

- 中文输出
- 专业表达
- 高信息密度
- 面向注意力分配和后续行动
- 区分事实、判断和行动建议
- 每条核心内容必须能说明证据类型：官方公告、GitHub、Hugging Face、arXiv、API 文档、监管文件、论文、模型卡或两个独立高质量报道。
- 若 `references/personal-priorities.md` 存在，选题、降权和行动清单必须优先遵循其中的个人偏好；若不存在，则使用默认主题层。

长度控制：

- 推荐 2500~6000 个中文字符
- 最大不超过 8000 个中文字符
- 低于推荐范围不视为失败；信息密度和事实质量优先于字数
- 禁止为满足字数扩写、重复表达、加入空泛分析，或将数字改写成中文大写/口语表达来凑字数

---

### 内容要求

每条核心信息应回答：

- 发生了什么
- 对我有什么判断价值
- 是否值得跟踪或尝试
- 下一步检查什么或做什么

避免：

- 模板化分析
- 空洞结论
- 重复表达
- 新闻堆砌

---

### Markdown 要求

禁止：

- HTML
- style
- iframe
- Markdown 引用块（>）

要求：

- 标题层级连续
- 标准 Markdown
- 普通列表格式

Bullet：

单条不超过 180 字。

---

## 6. 发布前最终审核

必须执行：

output-checklist.md

完整检查流程。

包括：

- 内容审核
- 事实审核
- 战略信号审核
- Markdown 审核
- 发布审核

未通过检查的内容：

必须删除、降级或补充验证。

---

## 7. 保存到 Get笔记

最终简报必须保存到 Get笔记。

优先使用：

```bash
python3 {baseDir}/scripts/save-to-getnote.py ai-daily-report-YYYY-MM-DD.md
```

脚本负责：

- 保存 Markdown
- 创建笔记
- 加入知识库
- 返回访问链接

---

### 备选方案

`scripts/save-to-getnote.py` 不可用时：

使用 curl 调用 Open API。

---

### 保底方案

脚本与 API 均失败时：

本地保存：

```text
ai-daily-report-YYYY-MM-DD.md
```

并明确说明失败原因。本地保存只是故障保底产物，不代表任务成功；最终回复必须明确“Get笔记发布失败，任务未成功完成”。

---

# 最终目标

情报简报应回答三个问题：

1. 今天哪些信息值得投入注意力？

2. 哪些信息值得跟踪、试用或忽略？

3. 下一步应该做什么？

输出重点：

- 高信号事件
- 明确判断
- 注意力分配
- 可执行行动

而不是：

- 新闻堆砌
- PR宣传
- SEO内容
- 模板化分析
