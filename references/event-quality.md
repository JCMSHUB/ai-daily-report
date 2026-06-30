# AI 个人情报简报 — 信源与事件质量标准

Version: 3.0

---

# Purpose

本文件定义 AI 个人情报简报的内容质量标准。

目标不是生成更多新闻，而是筛选对个人注意力分配、工具选择、学习重点和后续行动真正有用的信息。

简报必须帮助读者回答：

- 今天哪些 AI 信息值得投入注意力？
- 哪些变化值得持续跟踪？
- 哪些工具、论文、模型、框架值得亲自尝试？
- 哪些热闹信息可以忽略？
- 下一步应该做什么？

简报不是新闻聚合器，也不是为了字数完整而扩写的行业综述。

---

# Event Intelligence Score

所有候选事件均按以下标准打分。

总分：100

---

## 1. Source Quality（0-30）

评估信源可信度。

### 30

- GitHub
- Hugging Face
- arXiv
- OpenAI
- Anthropic
- Google DeepMind
- NVIDIA
- Microsoft
- Meta
- 官方技术博客
- 官方 API 文档
- 监管机构文件

### 25

- Reuters
- Bloomberg
- Financial Times
- The Information
- SemiAnalysis

### 20

- Hacker News
- Papers With Code
- The New Stack

### 15

- TechCrunch
- VentureBeat
- The Verge
- Wired
- MIT Technology Review

### 5

- Medium
- Substack
- 聚合转载站
- 自媒体资讯站

---

## 2. Actionability（0-25）

评估事件能否转化为后续动作。

高分条件：

- 有明确可阅读材料。
- 有明确可试用入口。
- 有明确后续观察指标。
- 会影响工具选型、学习计划、技术判断或产业判断。

评分参考：

### 20-25

能形成明确行动，例如阅读论文、试用工具、检查 API、跟踪监管文件或观察价格变化。

### 10-19

有跟踪价值，但短期行动不明确。

### 0-9

只能当作背景新闻，无法指导下一步动作。

---

## 3. Technical Substance（0-20）

评估技术信息密度。

高分条件：

- GitHub release
- API 发布
- benchmark
- model card
- 技术白皮书
- 架构设计
- 推理优化
- runtime 能力
- tool protocol
- agent framework
- 企业部署能力

评分参考：

### 16-20

包含明确技术细节，例如代码、benchmark、API、架构图、release notes。

### 8-15

有技术内容但细节有限。

### 0-7

仅产品宣传、市场描述或观点表达。

---

## 4. Strategic Impact（0-15）

评估对未来 6-24 个月 AI 生态的影响。

高价值方向：

- Agent runtime
- MCP
- tool protocol
- computer use
- browser agent
- multi-agent system
- 推理成本变化
- GPU 架构升级
- 企业 Agent 平台
- AI 基础设施
- 开源模型能力跃迁
- AI 治理与监管变化

评分参考：

### 12-15

可能改变行业结构、开发者生态或企业部署路径。

### 6-11

可能影响局部市场、单类工具或单个技术栈。

### 0-5

局部功能更新。

---

## 5. Novelty（0-10）

评估新颖度。

高分：

- 新 runtime
- 新协议
- 新推理架构
- 新 agent 能力
- 首次公开发布
- 首次出现可验证的商业或监管变化

低分：

- 常规版本升级
- 已有功能增强
- 重复宣传
- 二次转载

---

# Routing Rules

候选事件通过评分后，不再进入旧版固定新闻栏目，而是按读者动作分流。

---

## 值得跟踪

适合放入 `值得跟踪` 的事件必须满足：

- 综合评分 >= 75。
- 具备明确实体、动作、对象和结果。
- 具备至少一个后续观察对象。
- 不一定能立即试用，但会影响判断。

优先进入：

- Agent runtime、MCP、tool protocol、computer use。
- 推理基础设施、模型服务价格、GPU 与数据中心变化。
- 开源模型、开源 agent、开发者工具链。
- 监管、版权、出口管制、安全框架。

必须写清：

- 为什么值得跟踪。
- 观察窗口。
- 下次检查什么。

---

## 值得尝试

适合放入 `值得尝试` 的对象必须满足：

- 是工具、模型、框架、repo、API、论文或产品。
- 有可访问入口。
- 能在个人学习、开发、研究或工作流中验证价值。
- 能说明试用成本。

优先进入：

- 可运行 repo。
- 可调用 API。
- 可阅读论文或模型卡。
- 有 demo、docs 或 release notes 的工具。

禁止为了完整性硬凑本节。没有合格对象时可以省略。

---

## 可以忽略

适合放入 `可以忽略` 的信息通常具备以下特征：

- 传播热度高，但事实增量低。
- 只有 PR 叙事，没有一手信源。
- 与工具选择、学习重点或产业判断关系弱。
- 短期不可行动，也缺少后续观察指标。
- 属于融资、名人评论、社交媒体争议或消费电子噪音。

忽略不是简单删除。若当天该话题明显占据信息流，需要在本节说明为什么不值得投入注意力。

---

## 趋势判断

趋势判断只允许基于以下条件形成：

- 至少 2 个独立事件相互支持；或
- 1 个强一手信源 + 1 个交叉验证信号。

趋势判断必须包含：

- 趋势命题。
- 支持信号。
- 反证条件。
- 观察指标。

禁止把单条新闻扩写成趋势。

若信号不足，可以省略 `趋势判断`；若保留标题，必须明确写“今日无足够独立信号形成趋势判断”。

---

## 我的行动清单

行动清单只允许从正文事实中推出。

动作类型限定为：

- 阅读
- 试用
- 跟踪

每条行动必须具备：

- 具体对象。
- 明确目的。
- 可执行的下一步。

---

# Strategic Override Rules

部分治理、监管、供应链事件虽然技术细节有限，但可能对未来 AI 生态产生重大影响。

满足以下条件时：

- Strategic Impact >= 14。
- Source Quality >= 25 或 Evidence Strength 达到高可信水平。
- 存在明确后续影响或观察对象。

允许进入 `值得跟踪`。

适用场景：

- AI regulation。
- Copyright litigation。
- Export control。
- GPU export restrictions。
- National security policy。
- Government AI framework。

---

# Rejection Rules

以下内容默认剔除：

- 无技术内容的融资新闻。
- PR 宣传稿。
- SEO 内容。
- 洗稿转载。
- 无法追溯来源内容。
- 纯观点文章。
- 名人评论。
- 社交媒体争议。
- 无技术增量内容。
- 纯消费电子新闻。
- 只能提高字数但不能改善判断或行动的信息。

综合评分 < 60 时，默认不进入简报。

仅在以下情况可保留：

- 属于持续跟踪对象。
- 属于重大监管事件。
- 属于重大供应链事件。
- 属于当天需要解释为什么可以忽略的高热度噪音。

---

# Recency Rules

默认检索最近约 24 小时内容。

允许引用历史事件作为背景，但必须满足：

- 明确标注为背景。
- 不作为当天核心事件。
- 不替代当天事实增量。

对于延续性话题，只有出现新的重要长文、官方文件、release、benchmark、监管进展或可验证认知增量时，才可进入正文。

---

# Fact Quality Rules

核心事实必须包含：

1. Entity（谁）
2. Action（做了什么）
3. Object（作用对象）
4. Result（产生什么结果）

---

## Example

### Bad

MCP 生态持续发展。

### Good

Anthropic 发布 MCP Tunnels，允许 Claude Managed Agents 安全访问企业内网资源。

---

### Bad

推理成本持续下降。

### Good

某模型服务商将指定 API 价格下调，并在价格页或官方公告中给出明确生效范围与时间。

---

# Diversity Rules

每日简报应尽量覆盖以下方向中的至少两个：

- Frontier Models
- Agent Runtime
- Inference Infrastructure
- Open Source Ecosystem
- Governance & Regulation

如果当天有效高质量事件集中在单一方向，可以接受单一方向输出，但必须避免用低质量内容凑覆盖。

---

# Final Goal

简报输出应优先呈现：

- 高信号事件。
- 明确判断。
- 注意力分配。
- 后续行动。

而不是：

- 新闻堆砌。
- PR 宣传。
- 市场噪音。
- 重复信息。
- 为满足字数而扩写。

如果某条内容无法解释：

```text
这会改变我的判断、学习、工具选择或下一步行动吗？
```

则默认不应进入核心正文。
