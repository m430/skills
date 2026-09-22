---
name: implement-story
description: "实现一条 story：按 story 文件的描述驱动 /tdd，收尾跑 /code-review，完成后更新状态。"
disable-model-invocation: true
---

# 实现 story

一次只做一条 story，每条从全新上下文开始：实现完一条 `/clear`，再领下一条。不要一次领两条。

## 先定做哪条 story

用户点名了 story（编号或标题）就用那条。

没点名时，从当前迭代的 story 里让用户选一条：

- 列出 story 清单：编号、标题、状态。
- 运行环境提供结构化提问工具（`AskUserQuestion`）时用它提问，**一次只问一个问题**。候选是 story 标题，最多 4 条（队列最前的那些），把**编号最小、状态为"待实现"、且未被未完成 story 阻塞**的那条标成"（推荐）"放第一位；完整清单另外写在正文里，用户可以选"其他"点名其余的。不可用时退回文本。
- 「阻塞于」指向一条已放弃或已退回 backlog 的 story 时，那不算阻塞：照常推荐，但提醒用户这条边该清掉。

没有可选的 story 时，说清楚情况就停，不要自己挑：

- **没有进行中的迭代**（`sprints/` 下编号最大且 `SPRINT.md` 状态为"进行中"的 `sprint-NN/`）：让用户跑 `/add-sprint`。
- **迭代里还没有 story**：让用户跑 `/plan-sprint` 排 story，或 `/add-story` 补一条。
- **story 都已实现完**：让用户跑 `/close-sprint` 收尾迭代，再开下一个。

## 流程

1. 读 story 文件（`sprints/sprint-NN/story-NN-*.md`），以及它来源的 backlog 需求、`CONTEXT.md` 的词汇和相关 ADR。
2. 把 story 状态改成"实现中"。
3. 按"任务"清单逐项实现，在预先约定的接缝（seam）上尽可能使用 /tdd。
4. 定期跑类型检查，定期跑单个测试文件，最后完整跑一次测试套件。
5. 完成后用 /code-review 审查这项工作。
6. 提交到当前分支。
7. 回填：勾掉 story 文件里的任务与验收标准，状态改成"已完成"；`SPRINT.md` 故事清单里的那一行也勾掉（`- [ ]` 改成 `- [x]`）。

任务清单是实现时的粗稿，中途补的步骤直接写进 story 文件，它随 story 一起进入历史。

story 的状态取值只有这几个：`待实现`、`实现中`、`已完成`、`已放弃`、`已退回 backlog`、`已带回下个迭代`。本技能只写前三个，别用别的词。
