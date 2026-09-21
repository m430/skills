---
"m430-skills": minor
---

新增按迭代交付的 sprint 技能组，工作流从"规格 → 工单"改成"需求池 → 迭代（sprint）→ story → task"，产物落在消费方仓库的 `sprints/` 目录：

- **`add-backlog`**：把讨论里的想法记成一条待规划需求，写进 `sprints/backlog/`。不编号，不归属任何迭代。
- **`add-sprint`**：开启迭代。先确认上一个迭代已关闭，再问迭代目标，初始化 `sprints/sprint-NN/` 与 `SPRINT.md`。
- **`plan-sprint`**：按迭代目标推荐 backlog 需求，拆出 story 清单让你确认，然后为每条 story 生成带序号的 `story-NN-*.md`。
- **`add-story` / `delete-story`**：迭代中途增删 story，同步 `SPRINT.md` 与指向它的阻塞边。
- **`implement-story`**：实现一条 story，驱动 `/tdd`、收尾 `/code-review`，完成后更新 story 状态。
- **`close-sprint`**：把迭代完成情况评估写进 `SPRINT.md` 并关闭迭代，未完成的 story 逐条定好去向。

同时删除 `ask-me`（路由器）、`to-spec`、`triage` 三个技能。`to-tickets`、`implement`、`setup-skills` 等其余技能不动：需要把工作发布到真实 issue tracker 而不是本地 `sprints/` 文件时，仍可走 `to-tickets` 那条路。
