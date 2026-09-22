---
name: setup-skills
description: "为本仓库配置工程技能：迭代工作区约定、领域文档布局、UI 项目的设计系统登记。在首次使用其他工程技能之前运行一次。"
disable-model-invocation: true
---

# 设置技能

搭建工程技能所假设的每仓库配置：

- **迭代工作区**：迭代产物固定在 `sprints/`，把它写进仓库约定
- **领域文档**：`CONTEXT.md` 和 ADR 的存放位置，以及读取它们的消费规则
- **设计系统**：UI 项目在仓库根目录留一份 `design.md`，让写 UI 的会话先读它

这是一个由提示驱动的技能，不是确定性脚本。先探索，呈现发现，与用户确认，然后写入。

## 流程

### 1. 探索

查看当前仓库，了解其起始状态。有什么读什么，不要假设：

- 仓库根目录的 `AGENTS.md` 和 `CLAUDE.md`：两者存在吗？其中是否已有 `## Agent skills` 章节？
- 仓库根目录的 `CONTEXT.md` 和 `CONTEXT-MAP.md`
- `docs/adr/` 以及任何 `src/*/docs/adr/` 目录
- `docs/agents/`：本技能此前的产出是否已存在？
- `sprints/`：迭代工作区是否已存在？
- 仓库根目录的 `design.md`：设计系统是否已存在？
- Monorepo 信号：存在 `pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 字段，或装满内容且自带 `src/` 的 `packages/*`。这些只出现在真正的大型多包仓库中；没有它们就意味着单一上下文（single-context），而几乎所有仓库都是如此。
- UI 信号：`src/components/`、`*.tsx` / `*.vue` / `*.svelte`、`index.html`、`app/` 目录（Expo、Next 等），或 Swift / Kotlin 的界面目录。没有这些信号，C 节整节跳过。

### 2. 呈现发现并提问

总结已存在和缺失的内容。然后按顺序处理各节：一节、一个回答，再进入下一节。

每节以推荐答案开头，让用户一个词就能接受。运行环境提供结构化提问工具（`AskUserQuestion`）时用它提问，一次一个问题、选项即候选答案、推荐项放第一位；不可用时退回文本。只有当选项真正分叉时才给一行说明；探索已经定案时整节跳过（无 monorepo 时跳过 B 节的多上下文选项，无 UI 信号时跳过 C 节）。

**A 节：迭代工作区。** 无需提问：迭代产物的位置固定在仓库根目录的 `sprints/`，`add-backlog`、`add-sprint`、`plan-sprint`、`implement-story`、`fix-bug`、`close-sprint` 等技能都按这个路径读写，不提供配置项。要做的只是把它写进第 4 步的 `## Agent skills` 块，让后来的人不必加载技能就知道约定在哪。目录本身不用预先创建：`sprints/backlog/` 与 `sprints/sprint-NN/` 由写第一个文件的技能按需建立。

**B 节：领域文档。** 默认**单一上下文（single-context）**（仓库根目录一个 `CONTEXT.md` + `docs/adr/`）。这适用于几乎所有仓库；直接写入，无需询问。

仅当探索发现 monorepo 信号时，才提供**多上下文（multi-context）**（根目录 `CONTEXT-MAP.md` 指向各上下文的 `CONTEXT.md`）。然后确认他们想要哪种布局。

**C 节：设计系统。** 探索到 UI 信号的仓库才有这一节，没有就整节跳过。`design.md` 的位置固定在仓库根目录，没有配置项；要定的是什么时候把它登记进约定。

- **`design.md` 已存在**：无需提问，把它写进第 4 步的块。
- **有 UI 但还没有 `design.md`**：问一个问题：现在就登记，还是等产物出来再登记。推荐现在登记，块里写的是「写 UI 之前先跑 `/design-from-image`」，而不是指向一份还不存在的文件。

### 3. 确认并编辑

向用户展示以下内容的草稿：

- 要添加到 `CLAUDE.md` / `AGENTS.md`（选择规则见第 4 步）中的 `## Agent skills` 块
- `docs/agents/domain.md` 的内容

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

### 迭代工作区

迭代产物在仓库根目录的 `sprints/`：`backlog/` 存待规划需求（不编号），`sprint-NN/` 存 `SPRINT.md` 与该迭代的 `story-NN-*.md`、`bug-NN-*.md`（编号跨迭代全局递增）。规则由 `/add-backlog`、`/plan-sprint`、`/implement-story`、`/fix-bug`、`/close-sprint` 等技能持有。

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### 设计系统

[只有 C 节成立时才有这一段，没有 UI 信号就整段删掉。`design.md` 已存在时写「写任何 UI 之前先读 `design.md`：颜色、排版、间距、组件规范都在里面。新样式一律走其中定义的令牌，不要在组件里写死色值。」尚未产出时写「写任何 UI 之前先跑 `/design-from-image` 产出 `design.md`，之后一律先读它。」`design-from-image` 写出 `design.md` 后会把这一段换成读文件的说法。]
```

然后以本技能文件夹中的种子模板为起点写入文档文件：

- [domain.md](./domain.md)：领域文档消费规则 + 布局

### 5. 完成

告诉用户设置已完成，以及哪些工程技能将从现在起读取这些文件。提醒他们之后可以直接编辑 `docs/agents/*.md`；只有想换领域文档布局或从零重来时才需要重新运行本技能。

有 UI 的仓库如果还没有 `design.md`，提一句：带一张设计参考图跑 `/design-from-image` 就能产出，它会自己把块里那一节改成读文件的说法。
