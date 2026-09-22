---
"m430-skills": minor
---

新增按迭代交付的 sprint 技能组，工作流从"规格 → 工单"改成"需求池 → 迭代（sprint）→ story → task"，产物落在消费方仓库的 `sprints/` 目录：

- **`add-backlog`**：用拷问式访谈把想法梳理成**一条 story 大小**的待规划需求，写进 `sprints/backlog/`（想要什么 / 为什么 / 验收意图 / 边界）。不编号，不归属任何迭代；太大就拆成几条。
- **`add-sprint`**：开启迭代。先确认上一个迭代已关闭，再问迭代目标，初始化 `sprints/sprint-NN/` 与 `SPRINT.md`，并收拢上个迭代带回的 story 与 bug。
- **`plan-sprint`**：按迭代目标推荐 backlog 需求，拆出 story 清单让你确认，然后为每条 story 生成带序号的 `story-NN-*.md`。
- **`add-story` / `delete-story`**：迭代中途增删 story，同步 `SPRINT.md` 与指向它的阻塞边。
- **`implement-story`**：实现一条 story（一次一条），驱动 `/tdd`、收尾 `/code-review`，完成后更新 story 状态。
- **`close-sprint`**：把迭代完成情况评估写进 `SPRINT.md` 并关闭迭代，未完成的 story 与 bug 逐条定好去向，并清理悬空的阻塞边。
- **`fix-bug`**（取代 `diagnosing-bugs`）：保留完整的诊断六阶段与 `scripts/hitl-loop.template.sh`，同时把 bug 记成 `sprints/sprint-NN/bug-NN-*.md`（描述 / 解决方案 / 状态）并回填 `SPRINT.md` 的缺陷清单，迭代里因此能同时看到需求与 bug。

删除 `ask-me`（路由器）、`to-spec`、`triage`、`to-tickets`、`implement`：`to-tickets` 与 `implement` 的职责已由 `plan-sprint` 与 `implement-story` 覆盖，`diagnosing-bugs` 的职责由 `fix-bug` 覆盖。

`setup-skills` 改为按新的技能集初始化：只配置迭代工作区与领域文档布局两节，把固定的 `sprints/` 工作区约定写进 `## Agent skills` 块；triage 标签词表随 `triage` 一起移除。

整个 issue tracker 层随 `wayfinder` 一起删除：需求与 bug 都由 `sprints/` 里的 story、bug 文件跟踪，不再有外部 tracker 配置（`setup-skills` 的 B 节、三份 `issue-tracker-*.md` 种子模板、ADR 0001、`CONTEXT.md` 的 Issue tracker / Issue / Decision ticket 词条、`.out-of-scope/mainstream-issue-trackers-only.md` 全部移除），`code-review` 的规格来源收敛到 `sprints/` 的 story 文件。
