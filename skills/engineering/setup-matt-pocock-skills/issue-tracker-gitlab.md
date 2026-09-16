# Issue tracker：GitLab

本仓库的 issue 和规格（spec）以 GitLab issue 形式存放。所有操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 约定

- **创建 issue**：`glab issue create --title "..." --description "..."`。多行 description 使用 heredoc。传 `--description -` 打开编辑器。
- **读取 issue**：`glab issue view <number> --comments`。需要机器可读输出时用 `-F json`。
- **列出 issue**：`glab issue list -F json`，配合适当的 `--label` 过滤器。
- **评论 issue**：`glab issue note <number> --message "..."`。GitLab 把评论称为 "notes"。
- **添加 / 移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可用逗号分隔或重复该标志。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受关闭评论，所以先用 `glab issue note <number> --message "..."` 发布说明，然后关闭。
- **Merge request**：GitLab 把 PR 称为 "merge request"。使用 `glab mr create`、`glab mr view`、`glab mr note` 等，形状与 `gh pr ...` 相同，`mr` 代替 `pr`，`note`/`--message` 代替 `comment`/`--body`。

从 `git remote -v` 推断仓库；在克隆目录内运行时 `glab` 会自动完成。

## Merge request 作为 triage 入口

**MRs 作为 request surface：否。** _(如果本仓库把外部 merge request 视为功能请求，则设为 `yes`；`/triage` 读取此标志。)_

设为 `yes` 时，MR 走与 issue 相同的标签和状态，使用 `glab mr` 的对应命令：

- **读取 MR**：`glab mr view <number> --comments`，diff 用 `glab mr diff <number>`。
- **列出待 triage 的外部 MR**：`glab mr list -F json`，然后只保留作者不是项目成员/所有者的 MR（是贡献者的 MR，不是维护者进行中的工作）。
- **评论 / 打标签 / 关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

与 GitHub 不同，GitLab 对 issue 和 MR 分别编号，所以一旦知道维护者指的是哪一类，`#42` 就没有歧义。

## 当技能说 "publish to the issue tracker" 时

创建一个 GitLab issue。

## 当技能说 "fetch the relevant ticket" 时

运行 `glab issue view <number> --comments`。

## Wayfinding 操作

由 `/wayfinder` 使用。**map** 是一个 issue，以**子（child）** issue 作为工单。

- **Map**：一个带有 `wayfinder:map` 标签的 issue，正文承载 Notes / Decisions-so-far / Fog。`glab issue create --label wayfinder:map`。（在带原生 epic 的 GitLab 层级上，map 可以改由 epic 承载；带标签的 issue 在任何层级都可行。）
- **子工单**：description 顶部带 `Part of #<map>`、标签为 `wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）的 issue。一旦被认领，工单就分配给主导工作的开发者。
- **阻塞**：GitLab 的**原生阻塞链接（blocking link）**，这是规范的、UI 可见的表示。用 `/blocked_by #<n>` 快捷操作添加，以 note 形式发布（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生阻塞链接是 Premium/Ultimate 功能；在免费版（或不可用处）退回到在 description 顶部写一行 `Blocked by: #<n>, #<n>`。当每个阻塞者都关闭时，工单解除阻塞。
- **边界（frontier）查询**：`glab issue list -F json`，范围限定在 map 的子工单，丢弃任何有未关闭阻塞者的：指向未关闭 issue 的原生 `blocked_by` 链接（`glab api projects/:id/issues/:iid/links`）、`Blocked by` 行中有未关闭 issue、或已有受理人；按 map 顺序取第一个。
- **认领**：`glab issue update <n> --assignee @me`，这是会话的第一次写入。
- **解决**：`glab issue note <n> --message "<answer>"`，然后 `glab issue close <n>`，再把上下文指针（gist + 链接）追加到 map 的 Decisions-so-far。
