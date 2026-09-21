---
name: add-story
description: "给当前迭代补一条 story，同时更新 SPRINT.md。"
disable-model-invocation: true
---

# 补一条 story

## 流程

1. 找当前迭代：`sprints/` 下编号最大且 `SPRINT.md` 状态为"进行中"的 `sprint-NN/`。
   - 没有进行中的迭代：告诉用户先跑 `/add-sprint`。如果这个想法还没到排期那一步，改用 `/add-backlog` 记进需求池。
2. 从用户的描述里提炼 story：标题、要构建什么（端到端行为）、验收标准、阻塞于哪条、任务清单。信息不够就一次一个问题地问。
3. 写 `sprints/sprint-NN/story-NN-<slug>.md`，序号仍按全局最大值往下排（扫 `sprints/sprint-*/story-*.md`），模板与 `/plan-sprint` 的 story 模板一致。
4. 更新 `SPRINT.md` 的故事清单，一行一条。
