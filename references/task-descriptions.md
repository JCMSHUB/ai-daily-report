# OpenClaw 定时任务描述

本文件保存可直接部署到 OpenClaw cron 的任务文本。`SKILL.md` 与阶段 reference 是工作流和质量规则的唯一来源；cron 只声明调度环境与不可省略的入口约束。修改 skill 行为时不得在 cron 中复制一套实现规则。

## 每日 AI 情报简报

执行时间：每天 20:30（Asia/Shanghai）
cron 配置：`timeoutSeconds: 900`

```text
使用 /root/.openclaw/workspace/skills/ai-daily-report/ 中的 ai-daily-report skill 生成今日 AI 个人情报简报。

1. 每次运行必须重新读取 SKILL.md，并严格按其中的阶段顺序读取 reference；不得用上一轮、昨天、同一会话或历史简报代替本次读取、检索和验证。
2. 使用 Cron 注入的 Asia/Shanghai 时间，默认统计最近约 24 小时。
3. 只使用已注册的 tavily-remote__* 工具；主实例缺失时直接使用 tavily-remote-2__*。429 按 skill 重试后切换，432/433 立即切换。不得用真实调用探测工具可用性。两个实例都不可用时终止任务，不得使用 web_fetch 或其他检索方式替代。
4. 检索、低信号收敛、旧闻剔除、历史对照、Verification、写作和发布全部以当前 skill 及其 reference 为准；不得为完成任务降低证据标准或补足篇幅。
5. 最终执行 python3 /root/.openclaw/workspace/skills/ai-daily-report/scripts/save-to-getnote.py <markdown_file>。远端保存、知识库归档或本地近期副本任一失败，任务均不得视为成功。
6. 最终只返回 Get笔记访问链接、数据截至时间和必要的失败/主备切换说明。执行审计由独立任务负责，本任务不生成审计日志。
```

## 每周 AI 情报周报

执行时间：每周日 21:00（Asia/Shanghai）
cron 配置：`timeoutSeconds: 900`

```text
使用 /root/.openclaw/workspace/skills/ai-daily-report/ 中的 ai-daily-report skill 生成本周 AI 个人情报周报。

1. 每次运行必须重新读取 SKILL.md，并严格按其中的阶段顺序读取 reference；不得用上周会话、旧读取或历史简报代替本次补充检索与验证。
2. 使用 Cron 注入的 Asia/Shanghai 时间，统计本周范围；周报是底层事件的本周综合，不是七篇日报的拼接。
3. 只使用已注册的 tavily-remote__* 工具；主实例缺失时直接使用 tavily-remote-2__*。429 按 skill 重试后切换，432/433 立即切换。不得用真实调用探测工具可用性。两个实例都不可用时终止任务，不得使用 web_fetch 或其他检索方式替代。
4. 历史对照、补充检索、低信号收敛、旧闻剔除、Verification、写作和发布全部以当前 skill 及其 reference 为准；不得为完成任务降低证据标准或补足篇幅。
5. 最终执行 python3 /root/.openclaw/workspace/skills/ai-daily-report/scripts/save-to-getnote.py <markdown_file>。远端保存、知识库归档或本地近期副本任一失败，任务均不得视为成功。
6. 最终只返回 Get笔记访问链接、统计周期、数据截至时间和必要的失败/主备切换说明。执行审计由独立任务负责，本任务不生成审计日志。
```
