# Changelog

本文件记录每次提交对应的变更说明。之后修改 skill、脚本、参考资料或打包产物时，必须同步更新本文件。

## 2026-07-25

### Enforce evidence gates and cross-report novelty

- 根据 2026-07-17、07-20、07-21、07-24 四篇真实日报的执行结果，将近期简报与一手来源时间线纳入事件增量对照，避免同一发布跨期重复占位。
- 将候选记录扩展为事件键、前一/当前发布状态、来源等级和唯一主栏目，并要求对最终主张建立原子事实证据记录。
- 收紧技术、商业与治理事件的来源准入规则，明确区分 announced、preview、available、weights released 和 GA；来源缺失、时间不明或状态矛盾时禁止进入写作。
- 修正趋势判断漏洞：至少需要两个不同、已验证且已进入正文的底层事件；第二来源只作验证，趋势段落不得引入新事实。
- 增加“一事件一主位置”和写作前证据准入门槛，并同步更新写作模板、发布检查表及每日/每周定时任务契约。
- 保持现有两项业务脚本与打包流程不变，不为本次规则强化增加新的运行脚本。

## 2026-07-12

### Raise retrieval and brief quality from first principles

- 将 `SKILL.md` 收敛为阶段契约、事件门槛和发布流程，移除与 reference 重复的细节，降低运行期上下文负担。
- 重写 Discovery 框架：查询以实体/技术锚点、实质事件词和时间/证据意图构成；明确原始发布时间、原始证据优先、事件聚类、候选卡与停止条件。
- 重写事件质量标准：先检查完整事实、窗口内增量、可追溯证据和决策相关性，再按影响、行动性、增量、战略意义和新颖度排序；来源质量不再单独把无关事件推入正文。
- 提升写作与发布检查：每项明确区分事实、判断和行动；信源可交叉验证；行动有完成条件与时间；取消最低长度和所有凑数目标。
- 同步每日/每周定时任务，确保调度执行也遵循新的检索、验证、写作和发布约束。

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
