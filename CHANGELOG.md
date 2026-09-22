# m430-skills

## 1.3.0

### Minor Changes

- [`472a927`](https://github.com/m430/skills/commit/472a9270214be37b45fcd011af928b33dc3df17a) Thanks [@m430](https://github.com/m430)! - 新增 `design/` 桶，把设计类技能从 `engineering/` 里抽出来单独管理。

  - `design-from-image` 与 `prototype` 移到 `skills/design/`。`design/` 是 promoted 桶，两者仍随插件分发，斜杠命令与触发方式都不变。
  - 新增 `skills/design/README.md`（英文，按 User-invoked / Model-invoked 分组）。
  - 顶层 README 的「技能参考」新增 `### Design` 节，`CLAUDE.md`（`AGENTS.md` 是指向它的软链）的桶列表与 promoted 规则同步加上 `design/`。

- [`b7ba921`](https://github.com/m430/skills/commit/b7ba9217960d1c6f95c4c579f496ef9098e6dfa2) Thanks [@m430](https://github.com/m430)! - 新增 `design-from-image`（user-invoked）：在 shadcn/ui 底座上，按一张设计参考图改出项目级设计系统，产出仓库根目录的 `design.md`。

  - 底座是 shadcn/ui，参考图只负责改参数：令牌槽位、组件、字阶与间距刻度都用现成的，图里读到的往槽位里填，图上没有的一律继承仓库现状。产出因此是一份改动清单，而不是一份从零编出来的完整规范。仓库接没接底座看 `components.json`，找不到就停下让用户先 `npx shadcn@latest init`，不退回去自造一套平行令牌。
  - 四条纪律：每条令牌与规则标来源（`观察到` / `裁定` / `继承` / `推断`，能用继承就别用推断）；读控件不读页面；颜色必须由 `scripts/sample_colors.py` 按像素采样得出，不许目测报色；只记与底座不同的部分，不抄底座的出厂默认。
  - 八步流程：确认底座与现状 → 读图与清点 → 提取（取色与测尺寸）→ 填槽并归纳 → 缺口提问（`AskUserQuestion`，最多 5 个、一次一个）→ 一次性核对页确认 → 写 `design.md` → 在 `## Agent skills` 块登记。
  - `scripts/sample_colors.py` 四个子命令：`info` 尺寸、`palette` 主色聚类、`sample` 定点取色（坐标支持百分比）、`scan` 沿线扫描输出颜色分段与像素长度（用来量控件高度、内边距、圆角）。颜色同时输出 hex 与 oklch，oklch 一列与 shadcn 写主题令牌的格式相同，直接抄进 CSS，不用手工换算。
  - 附带 `references/shadcn-base.md`（底座的构成、槽位清单与角色对照、字阶与间距刻度、改动怎么应用）、`references/extraction.md`（输入类型判断与各类令牌的测量方法）、`references/design-md-template.md`（`design.md` 骨架、填写纪律、四个常见错误）、`references/gap-questions.md`（图答不了的决策提问库，底座答得了的不问）、`templates/style-guide.html`（中性外壳的一次性核对页，按槽位铺色板，未定状态用虚线框占位）。
  - 与既有技能的边界：`design.md` 是设计系统的唯一事实来源，不另发 `tokens.css`，可粘贴的 `:root` / `.dark` 块是本文件的一节；要复刻参考图页面或验证 UI 想法分别走直接实现与 `prototype`；项目已有 `design.md` 时先读再问增补还是重写。
  - `setup-skills` 同步接上设计系统：探索阶段看 `design.md` 与 shadcn 信号（`components.json`），新增的 C 节只在 shadcn 项目出现，`## Agent skills` 块模板多一节「设计系统」（产物还没出来时写的是「先跑 `/design-from-image`」），完成时提醒带图跑一次。`design-from-image` 的 Step 8 会原地替换这一节，不新增重复节。

- [`7d7a166`](https://github.com/m430/skills/commit/7d7a1663a97483c5018f1d4dedd33e72ebcf6315) Thanks [@m430](https://github.com/m430)! - 删除六个用不到的技能与整个 `in-progress/` 试验桶，收缩日常可见面：

  - **`resolving-merge-conflicts`**、**`handoff`**、**`teach`**、**`to-questionnaire`**、**`wait-what`**、**`writing-for-agents`** 从仓库移除，README 与 `plugin.json` 里的条目同步下架。
  - `in-progress/` 桶整体删除（`setup-ts-deep-modules`、`loop-me`、`writing-fragments`、`writing-shape`、`claude-handoff`、`retro`、`implement-spec`、`writing-beats`），不再随仓库分发；`CLAUDE.md` 的桶说明与 `scripts/link-skills.sh` 的注释同步收窄到 `misc/` 这一个非 promoted 桶。
  - 工作流地图相应简化：阶段 1 去掉问卷入口，阶段 4 去掉冲突处理与交接两个旁支。

- [`b681d7f`](https://github.com/m430/skills/commit/b681d7f18caa709a60d8631e39f2051ac7fc8e48) Thanks [@m430](https://github.com/m430)! - 新增按迭代交付的 sprint 技能组，工作流从"规格 → 工单"改成"需求池 → 迭代（sprint）→ story → task"，产物落在消费方仓库的 `sprints/` 目录：

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

### Patch Changes

- [`accf51c`](https://github.com/m430/skills/commit/accf51cbe90df547c155d90e4bc29dd6771549c9) Thanks [@m430](https://github.com/m430)! - grilling：提问优先使用运行环境的结构化提问工具（`AskUserQuestion`），一次一个问题、选项即候选答案、推荐项放首位；工具不可用时退回文本格式。

- [`fc74b00`](https://github.com/m430/skills/commit/fc74b0094f7160a72aab1e32f9a58246e1b02e6f) Thanks [@m430](https://github.com/m430)! - 结构化提问约定推广到 7 个技能：setup-skills、improve-codebase-architecture、writing-beats、writing-shape、to-tickets、triage、prototype 在向用户提出决策问题时优先使用 `AskUserQuestion`，一次一个问题、选项即候选答案、推荐项放首位；不可用时退回文本。

- [`b681d7f`](https://github.com/m430/skills/commit/b681d7f18caa709a60d8631e39f2051ac7fc8e48) Thanks [@m430](https://github.com/m430)! - 全库术语替换：`曳光弹（tracer bullet）` 统一改为 `垂直切片（vertical slice）`，两者指同一件事（逐层打通、端到端可独立验证的窄切片）。涉及 `to-tickets`、`tdd`、`ask-me`、`writing-for-agents`、`writing-fragments`、README 与 Codex 技能描述。

