---
name: claude-handoff
description: 把当前对话移交给一个全新的后台代理（background agent），让它立即接手工作。
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

为当前对话写一份交接摘要，让一个全新的代理能够继续这项工作。不要把它保存下来，而是启动一个后台代理，用这份摘要作为它的提示词：`claude --bg --name "<descriptive name>" "<handoff summary>"`。它在当前工作目录中启动并立即返回；用户用 `claude agents` 管理它。

始终带上 `-n`/`--name` 和一个描述性名称（例如 `--name "Fix login bug"`）；它用于设置显示在任务列表、会话选择器和终端标题中的名称。

在摘要中加入一节"suggested skills（建议技能）"，指明下一个代理应当为哪些技能调用 Skill 工具。

不要重复已经在其他产物中记录过的内容，例如规格（spec）、计划、ADR、issue、commit、diff；改为通过路径或 URL 引用它们。

对任何敏感信息做脱敏处理，例如 API 密钥、密码或个人身份信息，因为摘要会成为代理的提示词。

如果用户传入了参数，把它们视为对下一个会话关注点的描述，并据此调整摘要。
