# Issue tracker：本地 markdown

本仓库的 issue 和规格（spec）以 markdown 文件形式存放在 `.scratch/` 中。

## 约定

- 每个功能一个目录：`.scratch/<feature-slug>/`
- 规格是 `.scratch/<feature-slug>/spec.md`
- 实现 issue 每个工单一个文件，位于 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 开始编号，绝不用单个合并的工单文件
- triage 状态记录在每个 issue 文件顶部附近的 `Status:` 行中（角色字符串见 `triage-labels.md`）
- 评论和对话历史追加到文件底部 `## Comments` 标题之下

## 当技能说 "publish to the issue tracker" 时

在 `.scratch/<feature-slug>/` 下创建新文件（必要时创建目录）。

## 当技能说 "fetch the relevant ticket" 时

读取引用路径处的文件。用户通常会把路径或 issue 编号直接传给你。

## Wayfinding 操作

由 `/wayfinder` 使用。**map** 是一个文件，每个工单对应一个**子（child）**文件。

- **Map**：`.scratch/<effort>/map.md`（正文承载 Notes / Decisions-so-far / Fog）。
- **子工单**：`.scratch/<effort>/issues/NN-<slug>.md`，从 `01` 开始编号，正文中写明问题。`Type:` 行记录工单类型（`research`/`prototype`/`grilling`/`task`）；`Status:` 行记录 `claimed`/`resolved`。
- **阻塞**：顶部附近的 `Blocked by: NN, NN` 行。当它列出的每个文件都是 `resolved` 时，工单解除阻塞。
- **边界（frontier）**：扫描 `.scratch/<effort>/issues/`，找出打开、未阻塞且未被认领的文件；编号最小者胜出。
- **认领**：先设为 `Status: claimed` 并保存，然后才能开始任何工作。
- **解决**：在 `## Answer` 标题下追加答案，设为 `Status: resolved`，再把上下文指针（gist + 链接）追加到 `map.md` 中 map 的 Decisions-so-far。
