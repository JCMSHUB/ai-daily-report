# AI 个人情报简报 — 搜索与发现框架

Version: 3.3

---

# Purpose

本文件定义 AI 个人情报简报的信息发现策略。

目标：

- 稳定发现高信号信息。
- 降低热点、PR、SEO 和转载噪音。
- 为 `值得跟踪`、`值得尝试`、`可以忽略`、`趋势判断` 和 `我的行动清单` 提供候选材料。
- 避免 Agent 在定时任务中自由发挥导致搜索漂移。

---

# Core Principle

搜索目标不是收集“今天谁发布了什么”，而是发现能影响个人判断和行动的信号。

优先寻找：

- 会改变工具选择的信息。
- 值得亲自试用的工具、模型、框架、repo、API、论文或产品。
- 需要持续跟踪的生态变化、监管变化、价格变化或基础设施变化。
- 热度很高但实际不值得投入注意力的噪音。

目标是发现：

```text
Signal for attention and action
```

而不是：

```text
News volume
```

---

# Discovery Layers

每日搜索固定覆盖以下方向。每个主题层只组织 1 个综合查询，共 5 个基础查询；本文件中的示例查询是构造素材，不是必须逐条执行的查询清单。

默认使用 `search_depth: basic`、`time_range: day`、`max_results: 6~8`，并关闭 `include_raw_content`。同一批查询应并发执行，建议并发度不超过 3。

---

## Frontier Models

关注：

- OpenAI
- Anthropic
- Google DeepMind
- Meta
- DeepSeek
- Qwen
- Mistral
- xAI

搜索意图：

- 新模型。
- API 变化。
- 产品路线变化。
- 价格或商业模式变化。
- 模型能力、限制、benchmark 或 model card 更新。

示例查询：

- `OpenAI API model release pricing benchmark`
- `Anthropic Claude API release notes`
- `Google DeepMind Gemini model card benchmark`
- `DeepSeek Qwen Mistral model release GitHub Hugging Face`

---

## Agent Runtime

关注：

- Codex
- Claude Code
- MCP
- Browser Agent
- Computer Use
- Agent Runtime
- Multi-Agent System

搜索意图：

- Runtime 演进。
- Agent 平台化。
- Tool protocol 变化。
- 企业系统接入。
- 权限、沙箱、长期任务、浏览器自动化能力。

示例查询：

- `MCP agent runtime release GitHub`
- `Claude Code release notes`
- `Codex agent runtime tools update`
- `computer use browser agent API documentation`

---

## Inference Infrastructure

关注：

- NVIDIA
- CUDA
- TPU
- Rubin
- Blackwell
- vLLM
- Triton
- Datacenter
- Inference Serving

搜索意图：

- 推理成本变化。
- GPU 或加速器路线变化。
- serving 框架变化。
- 数据中心、网络、供应链或算力约束变化。

示例查询：

- `vLLM release inference serving benchmark`
- `NVIDIA Blackwell inference performance official`
- `CUDA release notes AI inference`
- `AI inference pricing GPU datacenter Reuters Bloomberg`

---

## Open Source Ecosystem

关注：

- GitHub
- Hugging Face
- Ollama
- llama.cpp
- DeepSeek
- Qwen
- Open Source Agent
- Local Inference

搜索意图：

- 开源能力跃迁。
- 本地推理生态。
- Agent 框架。
- 可直接试用的 repo、模型、工具或论文。

示例查询：

- `site:github.com AI agent framework release`
- `site:huggingface.co new open model benchmark`
- `llama.cpp release notes`
- `open source computer use agent GitHub`

---

## Governance & Regulation

关注：

- Regulation
- Copyright
- Safety
- Export Control
- Compliance
- Government AI Framework

搜索意图：

- 法规变化。
- 政策风险。
- 版权诉讼。
- 出口管制。
- 安全评估与合规框架。

示例查询：

- `AI regulation official document`
- `AI copyright litigation Reuters`
- `GPU export control AI official`
- `AI safety framework government official`

---

# Action-Oriented Queries

以下词组用于增强五个主题查询的行动导向，默认合并进对应主题查询，不单独增加固定搜索轮次。

## Try Candidates

用于发现 `值得尝试`：

- `AI tool GitHub release agent`
- `new AI model Hugging Face benchmark`
- `AI paper code release`
- `AI developer tool API docs release`

## Watch Candidates

用于发现 `值得跟踪`：

- `AI API pricing change official`
- `AI agent platform enterprise release`
- `AI inference infrastructure benchmark`
- `AI regulation update official`

## Ignore Candidates

用于发现需要解释的高热度噪音：

- `AI startup funding`
- `AI celebrity comment`
- `AI viral controversy`
- `AI gadget launch`

`可以忽略` 优先从 Discovery 已返回的高热度低质量结果中产生。只有当天某个高热话题明显占据信息流、但基础查询未覆盖时，才允许增加 1 次定向噪音查询。

---

# Candidate Processing and Verification

完成五个主题查询后：

1. 按底层事件聚类，合并转载、同源报道和重复 URL。
2. 使用 `source-quality.md` 初步评分，只保留约 6~8 个候选。
3. 对已有官方、GitHub、Hugging Face、arXiv、API 文档、release note 或监管文件 URL 的候选，优先批量调用 `tavily_extract`。
4. 已由原始材料完整支持的技术事实不再重复搜索。
5. 仅对缺少原始来源、缺第二信源或包含高风险声明的候选执行定向 Verification Search。

Verification Search 使用 `search_depth: advanced`、`max_results: 3~5`，按底层事件合并查询，通常为 1~3 次并发调用。

若某个关键方向没有合格候选，允许增加 1 次定向 `advanced` Discovery。目标总调用量为 7~9 次；事实质量门槛未满足时允许超出，不得为了节省调用跳过必要验证。

---

# Preferred Domains

优先参考：

## Official

- github.com
- huggingface.co
- arxiv.org
- openai.com
- anthropic.com
- blog.google
- deepmind.google
- nvidia.com
- microsoft.com
- meta.com
- 监管机构官网

---

## Research & Analysis

- reuters.com
- bloomberg.com
- ft.com
- theinformation.com
- semianalysis.com

---

## Developer Ecosystem

- news.ycombinator.com
- paperswithcode.com
- thenewstack.io

---

# Lower-Priority Domains

默认降权：

- medium.com
- substack.com
- SEO 聚合站
- 内容农场
- 泛 AI 资讯站
- 转载站

降权不等于屏蔽。若存在独家内容，允许保留，但必须交叉验证。

---

# Noise Filters

主动忽略：

- 无技术内容的 AI 融资新闻。
- 创业故事。
- 名人评论。
- AI 消费电子。
- SEO 内容。
- PR 宣传稿。
- 单纯观点输出。
- 社交媒体争议。

除非存在重大技术、监管、供应链或商业模式增量。

---

# Success Criteria

每日搜索结果应至少产出：

- 2-4 个 `值得跟踪` 候选。
- 1-4 个 `值得尝试` 候选；若无合格对象，可以为空。
- 0-4 个 `可以忽略` 候选；若没有明显占据信息流的高热度噪音，可以为空。
- 至少 1 个可形成 `趋势判断` 的信号组合；若信号不足，不得强写趋势。

覆盖方向优先包括以下至少两个：

- Frontier Models
- Agent Runtime
- Inference Infrastructure
- Open Source Ecosystem
- Governance & Regulation

如果当天高质量信号不足，允许输出更短简报，但不得用低质量材料凑数。

检索效率同时满足：

- 五个主题基础查询不拆成关键词级串行调用。
- 行动导向词默认合并进主题查询。
- Verification 只处理入围候选，并优先复用已知 URL。
- 后续查询不再产生新的合格事件或必要证据时立即停止。

---

# Final Rule

搜索目标不是收集新闻。

搜索目标是发现：

```text
哪些信息值得投入注意力，哪些值得行动，哪些可以忽略。
```
