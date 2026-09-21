---
name: delete-story
description: "从当前迭代删掉一条 story，并清理 SPRINT.md 与指向它的阻塞边。"
disable-model-invocation: true
---

# 删一条 story

## 流程

1. 找当前迭代，列出它的 story：编号、标题、状态。
2. 问用户删哪条。运行环境提供结构化提问工具（`AskUserQuestion`）时，用 story 标题当候选选项；不可用时退回文本。用户没点名时，说清楚只动那一条。
3. 用户确认后：
   - 删掉 `sprints/sprint-NN/story-NN-*.md`。
   - 从 `SPRINT.md` 的故事清单里移除那一行。
   - 检查其他 story 的"阻塞于"是否还指着它。有就逐条问用户：解除阻塞，还是改指别的 story？不要自作主张。
4. 只动用户点名的那一条。
