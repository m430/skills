---
name: setup-matt-pocock-skills
description: "为本仓库配置工程技能：设置 issue tracker、triage 标签词表和领域文档布局。在首次使用其他工程技能之前运行一次。"
disable-model-invocation: true
---

# 设置 Matt Pocock 技能

搭建工程技能所假设的每仓库配置：

- **Issue tracker**：issue 的存放位置（默认 GitHub；开箱即支持本地 markdown）
- **Triage 标签**：五个标准 triage 角色所用的字符串
- **领域文档**：`CONTEXT.md` 和 ADR 的存放位置，以及读取它们的消费规则

这是一个由提示驱动的技能，不是确定性脚本。先探索，呈现发现，与用户确认，然后写入。

## 流程

### 1. 探索

查看当前仓库，了解其起始状态。有什么读什么，不要假设：

- `git remote -v` 和 `.git/config`：这是 GitHub 仓库吗？是哪一个？
- 仓库根目录的 `AGENTS.md` 和 `CLAUDE.md`：两者存在吗？其中是否已有 `## Agent skills` 章节？
- 仓库根目录的 `CONTEXT.md` 和 `CONTEXT-MAP.md`
- `docs/adr/` 以及任何 `src/*/docs/adr/` 目录
- `docs/agents/`：本技能此前的产出是否已存在？
- `.scratch/`：本地 markdown issue tracker 约定已在使用的迹象
- `triage` 技能是否已安装？（本技能旁边的 `triage` 技能文件夹，或你可用技能中的 `triage`。）这决定 B 节是否运行。
- Monorepo 信号：存在 `pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 字段，或装满内容且自带 `src/` 的 `packages/*`。这些只出现在真正的大型多包仓库中；没有它们就意味着单一上下文（single-context），而几乎所有仓库都是如此。

### 2. 呈现发现并提问

总结已存在和缺失的内容。然后按顺序处理各节。一节、一个回答，再进入下一节。

每节以推荐答案开头，让用户一个词就能接受。只有当选项真正分叉时才给一行说明；探索已经定案时整节跳过（`triage` 未安装时跳过 B 节，无 monorepo 时跳过 C 节）。

**A 节：issue tracker。**

> 说明："issue tracker" 是本仓库 issue 的存放位置。`to-tickets`、`triage` 和 `to-spec` 等技能会读写它。它们需要知道是调用 `gh issue create`，还是在 `.scratch/` 下写 markdown 文件，还是遵循你描述的其他工作流。选择你实际用来跟踪本仓库工作的地方。

默认姿态：这些技能是为 GitHub 设计的。如果 `git remote` 指向 GitHub，就提议 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自托管主机），就提议 GitLab。否则（或用户另有偏好时），提供以下选项：

- **GitHub**：issue 存放在仓库的 GitHub Issues 中（使用 `gh` CLI）
- **GitLab**：issue 存放在仓库的 GitLab Issues 中（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 markdown**：issue 以文件形式存放在本仓库的 `.scratch/<feature>/` 下（适合单人项目或没有远端的仓库）
- **其他**（Jira、Linear 等）：请用户用一段话描述工作流；技能会将其记录为自由格式散文

把选择记录在 `docs/agents/issue-tracker.md`。GitHub 和 GitLab 模板带有一个 "PRs as a request surface" 标志，默认**关闭**。保持关闭且不要主动提起：想把外部 PR 纳入 triage 队列的用户可以稍后自行在文件中翻转该标志。

**B 节：triage 标签词表。** 如果 `triage` 技能未安装（探索已告知你），整节跳过，因为未安装的技能不需要标签。

如果已安装，只问一个问题：

> 你想保留默认 triage 标签吗？（推荐：**是**）

默认值是五个标准角色，每个标签字符串与其名称相同：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。用户回答**是**时，原样写入。只有当用户说不时（通常因为其 tracker 已使用其他名称，例如用 `bug:triage` 表示 `needs-triage`），才收集覆盖项，让 `triage` 应用现有标签而不是创建重复标签。

**C 节：领域文档。** 默认**单一上下文（single-context）**（仓库根目录一个 `CONTEXT.md` + `docs/adr/`）。这适用于几乎所有仓库；直接写入，无需询问。

仅当探索发现 monorepo 信号时，才提供**多上下文（multi-context）**（根目录 `CONTEXT-MAP.md` 指向各上下文的 `CONTEXT.md`）。然后确认他们想要哪种布局。

### 3. 确认并编辑

向用户展示以下内容的草稿：

- 要添加到 `CLAUDE.md` / `AGENTS.md`（选择规则见第 4 步）中的 `## Agent skills` 块
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 和 `docs/agents/triage-labels.md` 的内容（最后一项仅在 `triage` 已安装时）

让他们在写入前编辑。

### 4. 写入

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则如果 `AGENTS.md` 存在，编辑它。
- 如果两者都不存在，询问用户创建哪一个；不要替他们选。

`CLAUDE.md` 已存在时绝不要创建 `AGENTS.md`（反之亦然）；总是编辑已存在的那个。

如果所选文件中已有 `## Agent skills` 块，原地更新其内容，而不是追加重复块。不要覆盖用户对周围章节的编辑。

该块：

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

仅当 `triage` 已安装且 B 节已运行时，才包含 `### Triage labels` 子块并写入 `docs/agents/triage-labels.md`。否则两者都省略。

然后以本技能文件夹中的种子模板为起点写入文档文件：

- [issue-tracker-github.md](./issue-tracker-github.md)：GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)：GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md)：本地 markdown issue tracker
- [triage-labels.md](./triage-labels.md)：标签映射（仅当 `triage` 已安装时）
- [domain.md](./domain.md)：领域文档消费规则 + 布局

对于"其他" issue tracker，使用用户的描述从头编写 `docs/agents/issue-tracker.md`。

### 5. 完成

告诉用户设置已完成，以及哪些工程技能将从现在起读取这些文件。提醒他们之后可以直接编辑 `docs/agents/*.md`；只有想切换 issue tracker 或从零重来时才需要重新运行本技能。
