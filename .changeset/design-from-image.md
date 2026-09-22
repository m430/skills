---
"m430-skills": minor
---

新增 `design-from-image`（user-invoked）：在 shadcn/ui 底座上，按一张设计参考图改出项目级设计系统，产出仓库根目录的 `design.md`。

- 底座是 shadcn/ui，参考图只负责改参数：令牌槽位、组件、字阶与间距刻度都用现成的，图里读到的往槽位里填，图上没有的一律继承仓库现状。产出因此是一份改动清单，而不是一份从零编出来的完整规范。仓库接没接底座看 `components.json`，找不到就停下让用户先 `npx shadcn@latest init`，不退回去自造一套平行令牌。
- 四条纪律：每条令牌与规则标来源（`观察到` / `裁定` / `继承` / `推断`，能用继承就别用推断）；读控件不读页面；颜色必须由 `scripts/sample_colors.py` 按像素采样得出，不许目测报色；只记与底座不同的部分，不抄底座的出厂默认。
- 八步流程：确认底座与现状 → 读图与清点 → 提取（取色与测尺寸）→ 填槽并归纳 → 缺口提问（`AskUserQuestion`，最多 5 个、一次一个）→ 一次性核对页确认 → 写 `design.md` → 在 `## Agent skills` 块登记。
- `scripts/sample_colors.py` 四个子命令：`info` 尺寸、`palette` 主色聚类、`sample` 定点取色（坐标支持百分比）、`scan` 沿线扫描输出颜色分段与像素长度（用来量控件高度、内边距、圆角）。颜色同时输出 hex 与 oklch，oklch 一列与 shadcn 写主题令牌的格式相同，直接抄进 CSS，不用手工换算。
- 附带 `references/shadcn-base.md`（底座的构成、槽位清单与角色对照、字阶与间距刻度、改动怎么应用）、`references/extraction.md`（输入类型判断与各类令牌的测量方法）、`references/design-md-template.md`（`design.md` 骨架、填写纪律、四个常见错误）、`references/gap-questions.md`（图答不了的决策提问库，底座答得了的不问）、`templates/style-guide.html`（中性外壳的一次性核对页，按槽位铺色板，未定状态用虚线框占位）。
- 与既有技能的边界：`design.md` 是设计系统的唯一事实来源，不另发 `tokens.css`，可粘贴的 `:root` / `.dark` 块是本文件的一节；要复刻参考图页面或验证 UI 想法分别走直接实现与 `prototype`；项目已有 `design.md` 时先读再问增补还是重写。
- `setup-skills` 同步接上设计系统：探索阶段看 `design.md` 与 shadcn 信号（`components.json`），新增的 C 节只在 shadcn 项目出现，`## Agent skills` 块模板多一节「设计系统」（产物还没出来时写的是「先跑 `/design-from-image`」），完成时提醒带图跑一次。`design-from-image` 的 Step 8 会原地替换这一节，不新增重复节。
