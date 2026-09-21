# m430 Skills

面向真实工程实践的 AI 编程技能集（中文版）。fork 自 [mattpocock/skills](https://github.com/mattpocock/skills)（MIT），全部技能文档已译成中文并按自身需要独立维护。

## 这套技能解决什么问题

AI 编码代理最常见的四个失败模式，各自对应一类技能：

1. **代理没做出你想要的**。修复方式是拷问（grilling）：让代理就你要做的东西对你展开细致追问，对齐之后再动手。见 `/grill-me` 与 `/grill-with-docs`。
2. **代理话太多**。修复方式是共享语言：一份 `CONTEXT.md` 词汇表，让代理用 1 个词说清原本要 20 个词的事。内置于 `/grill-with-docs`。
3. **代码跑不起来**。修复方式是反馈环：静态类型、浏览器访问、自动化测试，尤其 red-green-refactor。见 `/tdd` 与 `/diagnosing-bugs`。
4. **写出了一团泥球**。修复方式是每天关心代码设计。见 `/codebase-design` 与 `/improve-codebase-architecture`。

## 安装

两条路线二选一，都装会得到重复的两份技能。

### Claude Code 插件

本仓库自身即一个单插件 marketplace：

```bash
/plugin marketplace add m430/skills
```

然后在会话内：

```bash
/plugin install m430-skills@m430
```

### 其他 agent（Codex 等）：skills.sh

```bash
npx skills@latest add m430/skills
```

安装器允许挑选技能与目标 agent。**务必把 `setup-skills` 选上。**

也可以按单个技能安装：

```bash
npx skills@latest add m430/skills --skill=<name>
```

### 本地维护本仓库时

```bash
scripts/link-skills.sh
```

把技能以软链方式接入 `~/.claude/skills` 与 `~/.agents/skills`，`git pull` 即保持最新；新增、删除或重命名技能后重新运行。

## 快速开始

1. 在你的项目里运行 `/setup-skills`（每个仓库一次）：选择 issue tracker、文档位置。
2. 想到要做的事：用 `/add-backlog` 记进需求池（`sprints/backlog/`）。
3. 按迭代交付：`/add-sprint` 开迭代，`/plan-sprint` 拆 story，`/implement-story` 逐条实现，`/close-sprint` 收尾。

## 按阶段看技能（工作流地图）

技能组织成一条主线：一个想法被**磨锐**（需求）、**试出答案**（设计）、**排进迭代拆成 story**（计划）、**构建出来**（开发）、**检查过**（评审）。三条旁路是独立入口，产出汇入主线；另外一组技能垫在所有阶段下面。

```mermaid
flowchart LR
    P0["阶段 0 · 准备<br/>setup-skills"] --> P1["阶段 1 · 需求<br/>grill-with-docs"]
    P1 -->|设计问题需要一个可运行的答案| P2["阶段 2 · 设计<br/>prototype"]
    P2 -->|带着结论回来| P1
    P1 -->|多会话构建| P3["阶段 3 · 计划<br/>add-sprint → plan-sprint"]
    P1 -->|一个小上下文装得下| P4["阶段 4 · 开发<br/>implement-story"]
    P3 -->|每条 story 从全新上下文开始| P4
    P4 -->|提交前收尾| P5["阶段 5 · 评审<br/>code-review"]
```

主线上的上下文纪律：阶段 1 到 3 保持在**同一个上下文窗口**里（拆 story 前不 compact 也不 clear），让拷问、迭代目标和 story 建立在同一份思考上；每次实现从全新上下文开始，只带一条 story。

### 阶段 0 · 准备（每仓库一次）

技能：[setup-skills](./skills/engineering/setup-skills/SKILL.md)

```mermaid
flowchart LR
    A["探索仓库现状<br/>git remote、AGENTS.md、CONTEXT.md、docs/adr/"] --> B["逐节确认<br/>issue tracker → 领域文档布局"]
    B --> C["展示草稿，确认后写入"]
    C --> O["产出：docs/agents/ 下的配置<br/>+ AGENTS.md 的 Agent skills 块"]
```

**产出**：一份仓库级配置（issue 存在哪、领域文档在哪）。`to-tickets`、`code-review`、`wayfinder` 等技能之后都从这里读约定。

### 阶段 1 · 需求（把想法磨锐）

技能：[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)（主入口）、[grilling](./skills/productivity/grilling/SKILL.md)、[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)、[research](./skills/engineering/research/SKILL.md)、[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)、[grill-me](./skills/productivity/grill-me/SKILL.md)

```mermaid
flowchart LR
    I["一个想法"] --> G["grill-with-docs<br/>内部跑 grilling + domain-modeling"]
    R["research<br/>后台代理查一手来源"] --> G
    TQ["to-questionnaire<br/>去问知道的人"] --> G
    G --> Q{"纸面上还答得了吗"}
    Q -->|继续问下一个| G
    Q -->|纸面答不了| P["阶段 2 · prototype"]
    P -->|带着结论回来| G
    Q -->|前沿清空| O["产出：对齐的共同理解<br/>+ CONTEXT.md 术语 + ADR"]
```

在某个工作目录里干活时用 `grill-with-docs`；完全没有工作目录时改用 `grill-me`（同一套访谈，无状态、不落文档）。访谈中术语敲定就写进 `CONTEXT.md`，难逆转的决定记成 ADR。`research` 的产物和问卷回收的答案是这一阶段的输入。

**产出**：一棵清空的决策树（你与代理对齐的共同理解），以及 `CONTEXT.md` 的新术语与新增 ADR。

### 阶段 2 · 设计（回答纸面回答不了的问题）

技能：[prototype](./skills/engineering/prototype/SKILL.md)、[codebase-design](./skills/engineering/codebase-design/SKILL.md)

```mermaid
flowchart LR
    Q["纸面上难以推定的设计问题"] --> B{"要回答哪个问题"}
    B -->|逻辑与状态模型| L["单个可分享 HTML<br/>自由操作按钮 + 引导流程"]
    B -->|UI 该长什么样| U["单路由多变体<br/>URL 参数 + 浮动底栏切换"]
    L --> V["让用户亲手驱动，推过纸面推不动的案例"]
    U --> V
    V --> D["验证过的决策合入真实代码"]
    D --> O["产出：被验证的设计决策<br/>+ prototype 分支作为一手资料"]
    CD["codebase-design 词汇<br/>module / interface / depth / seam"] -.-> Q
```

这是主线上的一次**绕道**，不是必经步骤：拷问中遇到“必须跑一下才知道”的问题（状态模型手感、UI 长相）时才进入，答案带回阶段 1。模块与接口形状本身存疑时，用 `codebase-design` 的词汇把问题说准。

**产出**：被验证的设计决策（合入真实代码或写进规格）；原型本身提交到 `prototype/<name>` 分支，作为一手资料由实现 issue 指向。

### 阶段 3 · 计划（迭代与 story）

技能：[add-backlog](./skills/engineering/add-backlog/SKILL.md)、[add-sprint](./skills/engineering/add-sprint/SKILL.md)、[plan-sprint](./skills/engineering/plan-sprint/SKILL.md)、[add-story](./skills/engineering/add-story/SKILL.md)、[delete-story](./skills/engineering/delete-story/SKILL.md)

```mermaid
flowchart LR
    C["阶段 1 与 2 谈清楚的东西"] --> AB["add-backlog<br/>待规划需求进 sprints/backlog/"]
    AB --> AS["add-sprint<br/>确认上个迭代已关闭，定迭代目标"]
    AS --> PS["plan-sprint<br/>推荐 backlog 需求，拆出 story 清单"]
    PS --> SF["每条 story 一个文件<br/>sprints/sprint-NN/story-NN-*.md"]
    SF --> O["产出：SPRINT.md + 一组<br/>带序号的 story 文件"]
    AS -.->|迭代中途增删| ED["add-story / delete-story"]
    ED -.-> SF
```

只有**多会话的构建**需要这一步；一个上下文装得下的小改动从阶段 1 直接进阶段 4。需求先进 `sprints/backlog/`（一条一个文件，不编号），开迭代时定目标，再按目标从 backlog 推荐需求、拆成 story：每条是垂直切片，自带验收标准与任务清单，声明被谁阻塞。

**产出**：一份 `SPRINT.md`（迭代目标与 story 清单）和一组 `sprints/sprint-NN/story-NN-*.md`。此后逐条推进：阻塞者已完成的 story 就可以领走。

需要把工作发布到真实 issue tracker（GitHub、Linear）而不是本地文件时，仍可用 `to-tickets` 拆成带阻塞边的工单。

### 阶段 4 · 开发（逐条 story 实现）

技能：[implement-story](./skills/engineering/implement-story/SKILL.md)、[tdd](./skills/engineering/tdd/SKILL.md)、[wizard](./skills/engineering/wizard/SKILL.md)、[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)、[handoff](./skills/productivity/handoff/SKILL.md)

```mermaid
flowchart LR
    T["领一条可开始的 story<br/>全新上下文"] --> IM["implement-story"]
    IM --> TD["tdd<br/>一次一个 red-green 垂直切片"]
    TD --> CK["定期类型检查<br/>先单文件测试，最后全量"]
    CK --> CR["收尾：code-review（阶段 5）"]
    CR --> CM["提交到当前分支"]
    CM -->|下一条 story| T
    WZ["wizard<br/>只有人类能做的步骤"] -.-> IM
    RC["resolving-merge-conflicts<br/>已在冲突中时"] -.-> IM
    HD["handoff<br/>换会话、换目录、换人"] -.-> IM
    CM --> O["产出：每条 story 一个可独立验证的<br/>垂直切片 + 测试 + 提交"]
```

每条 story 自包含：实现完一条 `/clear`，再领下一条。测试只在**预先约定的接缝**上写。撞上只有人类能做的步骤（开通服务、配置凭据）时，让 `wizard` 生成一个交互式 bash 向导。

**产出**：每条 story 一个可独立验证的垂直切片：可运行的行为、通过的测试、可追溯的提交。

### 阶段 5 · 评审（双轴验收）

技能：[code-review](./skills/engineering/code-review/SKILL.md)

```mermaid
flowchart LR
    F["确定固定点<br/>commit、分支、tag 或 merge-base"] --> DF["git diff 固定点...HEAD"]
    DF --> A1["Standards 子代理<br/>成文标准 + Fowler 坏味道基线"]
    DF --> A2["Spec 子代理<br/>缺失的需求、范围蔓延、实现有误"]
    A1 --> R["并排呈现两条轴<br/>不合并、不跨轴排序"]
    A2 --> R
    R --> O["产出：双轴评审报告<br/>提交与合并前的质量门"]
```

`implement-story` 在提交前自动进这一阶段收尾；也可以对任意分支或 PR 独立运行（给一个固定点即可）。两条轴在并行子代理里跑，互不污染上下文：**Standards** 查代码是否遵循仓库标准，**Spec** 查代码是否忠实实现了源 story 或规格。

**产出**：两条轴分开的评审报告（每条轴的发现数与最严重项），作为提交或合并前的质量门。

### 旁路（独立入口，产出汇入主线）

```mermaid
flowchart LR
    WF["wayfinder<br/>一个会话装不下的迷雾"] --> B2["决策地图，逐张解决决策"] --> X3["收拢成计划，汇入阶段 3"]
    IA["improve-codebase-architecture<br/>扫描深化机会"] --> R2["HTML 报告 + 对选中者的拷问"] --> X1["汇入阶段 1"]
    DB["diagnosing-bugs<br/>难缠 bug 与性能回归"] --> R3["反馈环 → 修复 + 回归测试"]
    R3 -->|接缝缺失时转交| IA
```

- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**：认知负担最重的入口，只用于一个会话装不下的巨大事项。**产出**：决策地图与逐个解决的决策，收拢成可建造的计划后汇入阶段 3。
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**：难 bug 与性能回归。拿到紧凑的反馈循环之前拒绝空谈理论。**产出**：修复、回归测试，以及被证实正确的假设（写进提交消息）。发现没有可锁死 bug 的接缝时，转交 `improve-codebase-architecture`。
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**：代码库保养。**产出**：深化机会报告；选中一个就生成想法，从阶段 1 进入主线。

### 贯穿与独立技能

| 技能 | 什么时候用 |
|---|---|
| [grilling](./skills/productivity/grilling/SKILL.md) | 访谈原语本身：一次一个问题，事实归代理查、决定归你拍板。`grill-me`、`grill-with-docs`、`wayfinder`、`improve-codebase-architecture` 内部都在跑它 |
| [domain-modeling](./skills/engineering/domain-modeling/SKILL.md) | 领域词汇的维护纪律：挑战模糊术语，当场更新 `CONTEXT.md`，适时记 ADR |
| [codebase-design](./skills/engineering/codebase-design/SKILL.md) | 深模块词汇（module、interface、depth、seam、adapter、leverage、locality），任何设计或评审接口与接缝的场合 |
| [handoff](./skills/productivity/handoff/SKILL.md) | 阶段边界上要换 harness、换目录、换人，或中途开一条支线时，写一份可携带的交接文档 |
| [wait-what](./skills/productivity/wait-what/SKILL.md) | 上一条消息没接住时，让它补齐上下文、用平实语言重讲 |
| [resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md) | 已经身处 merge 或 rebase 冲突中时，逐 hunk 按意图解决并完成操作，绝不 `--abort` |
| [grill-me](./skills/productivity/grill-me/SKILL.md) | 不在任何工作目录里干活时的访谈入口：同一套访谈，无状态 |
| [teach](./skills/productivity/teach/SKILL.md) | 把当前目录当学习工作区，跨多个会话教一个主题 |
| [writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md) | 写技能、`AGENTS.md` 或其他给代理消费的文档时的写作参考 |

## 技能参考

按"谁能调用"分两类。**User-invoked** 只能由你输入斜杠命令触发，负责编排流程；**Model-invoked** 可被你调用，也可由代理在任务匹配时自动触发，承载可复用的纪律。User-invoked 技能可以调用 Model-invoked 技能，反之不行。

### Engineering

日常代码工作使用。

**User-invoked**

- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: 拷问式访谈，同时构建项目领域模型，现场打磨术语并更新 `CONTEXT.md` 与 ADR。
- **[add-backlog](./skills/engineering/add-backlog/SKILL.md)**: 把讨论中冒出来的想法记成一条待规划需求，写进 `sprints/backlog/`；不编号，不归属任何迭代。
- **[add-sprint](./skills/engineering/add-sprint/SKILL.md)**: 开启一个新迭代：确认上一个已关闭，问清迭代目标，初始化 `sprints/sprint-NN/` 与 `SPRINT.md`。
- **[plan-sprint](./skills/engineering/plan-sprint/SKILL.md)**: 按迭代目标推荐 backlog 里的相关需求，拆出 story 清单经你确认后，为每条生成带序号的 story 文件。
- **[add-story](./skills/engineering/add-story/SKILL.md)**: 给当前迭代补一条 story，同步更新 `SPRINT.md`。
- **[delete-story](./skills/engineering/delete-story/SKILL.md)**: 从当前迭代删掉一条 story，同步清理 `SPRINT.md` 与其他 story 里指向它的阻塞边。
- **[implement-story](./skills/engineering/implement-story/SKILL.md)**: 实现一条 story，在预先约定的接缝（seam）驱动 `/tdd`，收尾跑 `/code-review` 后提交，完成后更新 story 状态。
- **[close-sprint](./skills/engineering/close-sprint/SKILL.md)**: 评估迭代完成情况并写入 `SPRINT.md`，关闭迭代；未完成的 story 逐条定好去向。
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，选定后进入拷问循环。
- **[setup-skills](./skills/engineering/setup-skills/SKILL.md)**: 为本仓库配置工程技能（issue tracker、领域文档布局）。使用其他工程技能前每仓库运行一次。
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: 把任意计划、规格或对话拆成一组垂直切片（vertical slice）工单，各自声明阻塞边，写入本地文件或真实 tracker 的原生阻塞链接。
- **[implement](./skills/engineering/implement/SKILL.md)**: 实现规格或工单描述的工作，在预先约定的接缝（seam）驱动 `/tdd`，收尾跑 `/code-review` 后提交。
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**: 把超出单会话容量的巨大工作规划为 issue tracker 上的共享决策地图，逐个解决决策工单，直到通往终点的路清晰可见。

**Model-invoked**

- **[prototype](./skills/engineering/prototype/SKILL.md)**: 构建一次性原型回答设计问题：状态/逻辑问题用单个可分享 HTML 文件，UI 问题用一条路由可切换的多个差异巨大的变体。
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: 硬 bug 与性能回归的纪律化诊断环：建一条对该 bug 变红的反馈环，最小化，列假设，插桩，修复，回归测试。
- **[research](./skills/engineering/research/SKILL.md)**: 以后台代理按高可信一手来源调研问题，把结论沉淀为仓库中带引用的 Markdown 文件。
- **[tdd](./skills/engineering/tdd/SKILL.md)**: 测试驱动开发，red-green-refactor 循环，一次一个垂直切片地构建功能或修复 bug。
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)**: 主动构建并打磨项目领域模型：对照词汇表挑战术语，用边界场景压测，当场更新 `CONTEXT.md` 与 ADR。
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**: 设计深模块的共享纪律与词汇：小接口背后藏大量行为，落在干净的接缝上，经由接口可测。
- **[code-review](./skills/engineering/code-review/SKILL.md)**: 对固定点以来的 diff 做双轴评审：Standards（仓库编码标准加 Fowler 坏味道基线）与 Spec（是否忠实实现来源 issue/规格），以并行子代理运行互不污染。
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)**: 逐 hunk 处理进行中的 git merge 或 rebase 冲突，按追溯到的两侧一手来源意图解决，然后完成操作（绝不 `--abort`）。
- **[wizard](./skills/engineering/wizard/SKILL.md)**: 生成交互式 bash 向导，引导人类完成只有他们能做的步骤：开通基础设施、配置凭据或 CI secrets、走不熟悉的第三方后台、执行一次性迁移。

### Productivity

通用工作流工具，不限于代码。

**User-invoked**

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: 就一个计划或设计被毫不松口地访谈，直到设计树的每条分支都解决。
- **[handoff](./skills/productivity/handoff/SKILL.md)**: 把当前对话压缩成交接文档，让另一个代理继续这项工作。
- **[teach](./skills/productivity/teach/SKILL.md)**: 以当前目录为有状态教学工作区，跨多个会话教用户一项新技能或概念。
- **[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)**: 把你独自答不了的决策变成 Markdown 问卷，交给唯一能答的人异步填写或会上共同完成。它拷问的是发送侧（发给谁、要拿回什么），不是主题本身。
- **[wait-what](./skills/productivity/wait-what/SKILL.md)**: 上一条消息没接住时立刻触发。代理会补齐你缺的上下文，用平实语言和 `CONTEXT.md` 的词汇重新表达。

**Model-invoked**

- **[grilling](./skills/productivity/grilling/SKILL.md)**: 就计划、决策或想法对用户毫不松口地访谈，直到设计树每条分支解决。`grill-me`、`grill-with-docs`、`wayfinder`、`improve-codebase-architecture` 背后可复用的访谈原语。
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)**: 写给代理消费的文档：技能、`AGENTS.md`/`CLAUDE.md`，以及代理经指针到达的任何文档。

## 致谢

本仓库 fork 自 [Matt Pocock 的 skills 仓库](https://github.com/mattpocock/skills)，原项目以 MIT 许可发布，感谢其出色的工程实践沉淀。
