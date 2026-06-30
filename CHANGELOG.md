# Changelog

本文件记录每次提交对应的变更说明。之后修改 skill、脚本、参考资料或打包产物时，必须同步更新本文件。

## 2026-06-30

### Phase reference loading by workflow stage

- 将运行期 reference 文件按职责重命名：`source-quality.md` -> `event-quality.md`，`search-keywords.md` -> `discovery-framework.md`，`template.md` -> `writing-template.md`，`output-checklist.md` -> `publishing-checklist.md`。
- 更新 `SKILL.md`，要求按阶段读取 reference：Discovery 前只读取 discovery / quality / personal，写作前才读取 template，发布前才读取 checklist。
- 更新 `references/task-descriptions.md`，让每日和每周定时任务描述携带同样的阶段化读取硬约束。
- 更新 `scripts/validate-skill.sh` 和 `ai-daily-report-openclaw-skill.zip`，确保发布包使用新文件名并通过一致性验证。

## 2026-06-29

### Remove GetNote shell wrapper

- 删除 `scripts/save-to-getnote.sh`，避免保存入口重复和后续路径漂移。
- 将 `SKILL.md`、`references/task-descriptions.md` 和 `references/output-checklist.md` 统一改为直接执行 `python3 scripts/save-to-getnote.py`。
- 更新 `scripts/validate-skill.sh`，只验证 Python 保存入口、打包脚本和验证脚本。
- 重建 `ai-daily-report-openclaw-skill.zip`，确保发布包不再包含 shell wrapper。

### Simplify GetNote save flow with Python

- 将 Get笔记保存主逻辑从 Bash 迁移到 `scripts/save-to-getnote.py`，集中处理配置读取、JSON payload、HTTP 调用和响应判定。
- 将 `scripts/save-to-getnote.sh` 简化为兼容入口，保持原有调用方式不变。
- 更新 `scripts/validate-skill.sh`，纳入 Python 语法检查和响应解析函数回归检查。
- 重建 `ai-daily-report-openclaw-skill.zip`，确保发布包包含新的 Python 保存脚本。

### Fix GetNote response parser

- 修复 `scripts/save-to-getnote.sh` 中 JSON 响应解析函数的 stdin 冲突问题，避免 Get笔记返回 `success: true` 和 `note_id` 时仍被误判为保存失败。
- 在 `scripts/validate-skill.sh` 中增加本地 JSON 解析回归检查，覆盖 `success` 和 `note_id` 提取。
- 重建 `ai-daily-report-openclaw-skill.zip`，确保发布包包含修复后的脚本。

### Add changelog for tracked changes

- 新增 `CHANGELOG.md`，要求之后每次修改 skill、脚本、参考资料或打包产物时，同步提交变更说明。
- 回填当前仓库已有两个提交的变更摘要，便于后续审查按提交追踪上下文。

### da44330 — Tighten AI daily report skill workflow

- 修正 `趋势判断` 的执行语义：信号不足时允许省略，或明确写明无足够独立信号，不再强写趋势。
- 明确 Get笔记发布失败时的任务状态：本地 Markdown 只作为故障保底，不算任务成功。
- 增加候选事件筛选表要求，覆盖事件、来源、评分、证据类型、Verification 状态、入选栏目或剔除原因。
- 新增 `references/personal-priorities.md`，把通用 AI 简报收敛到个人关注方向和行动偏好。
- 强化 `scripts/save-to-getnote.sh`：增加 HTTP 失败判定、超时参数和业务成功字段检查。
- 新增 `scripts/package-skill.sh` 和 `scripts/validate-skill.sh`，用于稳定打包和静态验证。
- 重建 `ai-daily-report-openclaw-skill.zip`，并通过包内容一致性验证。

### 20306a0 — Initial ai-daily-report skill snapshot

- 初始化 Git 仓库并提交 skill baseline。
- 添加 `.gitignore`，忽略 `.DS_Store`。
- 纳入 `SKILL.md`、`references/`、`scripts/save-to-getnote.sh` 和初始 OpenClaw skill zip。
