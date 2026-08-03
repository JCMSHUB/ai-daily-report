# AI Daily Report

面向个人注意力分配的中文 AI 情报简报 skill。它通过 Tavily MCP 发现近期事件，以一手来源验证事实增量，生成日报或周报，并发布到 Get笔记。

这个项目追求的不是新闻覆盖率，而是回答三个问题：

- 什么新事实会改变判断；
- 接下来值得跟踪或尝试什么；
- 哪些高热度信息没有决策增量，可以忽略。

## 核心特性

- 按前沿模型、Agent Runtime、推理基础设施、开源生态和治理监管五层发现候选事件；
- 严格区分预告、预览、可用、权重发布和 GA 等状态；
- 使用候选筛选表、原子事实证据和一手来源控制正文准入；
- 对近期本地简报做定向检索，避免旧事件重复占位；
- 支持低信号日提前收敛，不以栏目或篇幅为目标；
- 发布到 Get笔记，并保留有期限的本地 Markdown 历史；
- 提供独立的确定性执行审计器，不依赖执行模型自评。

## 仓库结构

```text
.
├── SKILL.md                         # Skill 入口与不可跳过的执行契约
├── references/                      # 分阶段读取的发现、证据、写作和发布规则
├── scripts/
│   ├── save-to-getnote.py           # 发布、知识库归档和本地历史保存
│   ├── package-skill.sh             # 构建 OpenClaw skill ZIP
│   └── validate-skill.sh            # 静态与回归验证
├── audit/                            # 独立执行审计器，不进入 skill ZIP
├── ai-daily-report-openclaw-skill.zip
└── CHANGELOG.md
```

## 运行要求

- OpenClaw；
- Python 3；
- 已注册的 `tavily-remote__*` MCP 工具；可选备用实例为 `tavily-remote-2__*`；
- Get笔记 API 凭证：`GETNOTE_API_KEY` 与 `GETNOTE_CLIENT_ID`。

Get笔记凭证可以通过环境变量提供，也可以保存在 OpenClaw 配置的 `skills.entries.getnote.env` 中。

## 部署 Skill

可以直接使用仓库中的 `ai-daily-report-openclaw-skill.zip` 部署，也可以将以下内容复制到 OpenClaw skill 目录：

```text
SKILL.md
references/
scripts/
```

默认部署路径为：

```text
/root/.openclaw/workspace/skills/ai-daily-report/
```

每日和每周定时任务的精简配置文本位于 [`references/task-descriptions.md`](references/task-descriptions.md)。完整工作流只维护在 `SKILL.md` 与阶段 reference 中，避免 Cron 配置复制并漂移。

## 验证与打包

修改 skill、脚本或 reference 后执行：

```bash
bash scripts/package-skill.sh
bash scripts/validate-skill.sh
```

验证脚本会检查必需文件、ZIP 与工作区一致性、过期契约、Python 源码、Get笔记响应解析以及本地历史保留逻辑。

## 发布简报

Skill 正常运行时会自动调用发布脚本。也可以对已有 Markdown 手动执行：

```bash
python3 scripts/save-to-getnote.py ai-daily-report-YYYY-MM-DD.md
```

成功条件包括：远端笔记保存、知识库归档和本地近期副本全部完成。默认本地目录为：

```text
~/.openclaw/ai-daily-report/recent-reports
```

可用以下环境变量覆盖：

- `AI_DAILY_REPORT_LOCAL_DIR`：本地近期简报目录；
- `AI_DAILY_REPORT_RETENTION_DAYS`：保留天数，默认为 14；
- `GETNOTE_TOPIC_ID`：目标知识库；
- `GETNOTE_NOTE_TYPE`：笔记类型；
- `GETNOTE_MAX_TIME`：HTTP 超时时间。

## 执行审计

审计器读取 APM/OpenTelemetry Trace JSON 和可选的最终 Markdown，检查工具证据、阶段顺序、候选表、原子事实、低信号格式、规则漂移和发布状态：

```bash
python3 audit/audit_run.py trace.json \
  --report ai-daily-report-2026-07-31.md \
  --json-out audit-result.json \
  --markdown-out audit-result.md
```

详细说明见 [`audit/README.md`](audit/README.md)。审计器位于 skill 发布包之外，保持执行与审计相互独立。

## 测试

```bash
python3 -m unittest discover -s audit/tests -v
```

项目变更记录见 [`CHANGELOG.md`](CHANGELOG.md)。
