---
name: handoff
description: 把当前对话压缩成一份交接文档，供另一个代理接手。
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

写一份交接文档，总结当前对话，让一个全新的代理能继续这项工作。保存到用户操作系统的临时目录，不要存到当前工作区。

在文档中加入一节 "suggested skills"（建议技能），指明下一个代理应当用 Skill 工具调用哪些技能。

不要重复其他工件（规格（spec）、计划、ADR、issue、commit、diff）中已经记录的内容，改用路径或 URL 引用它们。

对任何敏感信息做脱敏处理，例如 API key、密码或个人身份信息。

如果用户传入了参数，把它们当作对下一个会话重点的描述，并据此调整文档。
