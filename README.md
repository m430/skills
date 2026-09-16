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

1. 在你的项目里运行 `/setup-skills`（每个仓库一次）：选择 issue tracker、triage 标签、文档位置。
2. 主流程：`/grill-with-docs` 打磨想法，`/to-spec` 产出规格，`/to-tickets` 拆成工单，`/implement` 逐单实现。
3. 随时用 `/ask-me` 问路：它会根据你的处境推荐该走哪条流程。

## 技能参考

按"谁能调用"分两类。**User-invoked** 只能由你输入斜杠命令触发，负责编排流程；**Model-invoked** 可被你调用，也可由代理在任务匹配时自动触发，承载可复用的纪律。User-invoked 技能可以调用 Model-invoked 技能，反之不行。

### Engineering

日常代码工作使用。

**User-invoked**

- **[ask-me](./skills/engineering/ask-me/SKILL.md)**: 问哪种技能或流程适合你的处境。覆盖本仓库技能的路由器。
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: 拷问式访谈，同时构建项目领域模型，现场打磨术语并更新 `CONTEXT.md` 与 ADR。
- **[triage](./skills/engineering/triage/SKILL.md)**: 把 issue 按分诊状态机推进流转。
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，选定后进入拷问循环。
- **[setup-skills](./skills/engineering/setup-skills/SKILL.md)**: 为本仓库配置工程技能（issue tracker、triage 标签、领域文档布局）。使用其他工程技能前每仓库运行一次。
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: 把当前对话综合成规格（spec）并发布到 issue tracker。不做访谈，只综合已讨论过的内容。
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: 把任意计划、规格或对话拆成一组曳光弹（tracer bullet）工单，各自声明阻塞边，写入本地文件或真实 tracker 的原生阻塞链接。
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

- **[grilling](./skills/productivity/grilling/SKILL.md)**: 就计划、决策或想法对用户毫不松口地访谈，直到设计树每条分支解决。`grill-me`、`grill-with-docs`、`triage`、`wayfinder`、`improve-codebase-architecture` 背后可复用的访谈原语。
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)**: 写给代理消费的文档：技能、`AGENTS.md`/`CLAUDE.md`，以及代理经指针到达的任何文档。

## 致谢

本仓库 fork 自 [Matt Pocock 的 skills 仓库](https://github.com/mattpocock/skills)，原项目以 MIT 许可发布，感谢其出色的工程实践沉淀。
