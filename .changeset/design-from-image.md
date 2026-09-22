---
"m430-skills": minor
---

新增 `design-from-image`（user-invoked）：从一张设计参考图提取项目级设计系统，产出仓库根目录的 `design.md`。

- 四条纪律：每条令牌与规则标来源（`观察到` / `裁定` / `推断`）；读控件不读页面；hex 由 `scripts/sample_colors.py` 按像素采样得出，不许目测报色；收敛成克制的令牌集而非测量记录。
- 七步流程：读图清点 → 提取（取色与测尺寸）→ 归纳令牌并命名 → 缺口提问（`AskUserQuestion`，最多 5 个、一次一个）→ 一次性核对页确认 → 写 `design.md` → 在 `## Agent skills` 块登记。
- `scripts/sample_colors.py` 四个子命令：`info` 尺寸、`palette` 主色聚类、`sample` 定点取色（坐标支持百分比）、`scan` 沿线扫描输出颜色分段与像素长度（用来量控件高度、内边距、圆角）。
- 附带 `references/extraction.md`（输入类型判断与各类令牌的测量方法）、`references/design-md-template.md`（`design.md` 骨架、令牌命名固定词汇、四个常见错误）、`references/gap-questions.md`（图答不了的决策提问库）、`templates/style-guide.html`（中性外壳的一次性核对页，未定状态用虚线框占位）。
- 与既有技能的边界：`design.md` 是设计系统的唯一事实来源，不另发 `tokens.css`；要复刻参考图页面或验证 UI 想法分别走直接实现与 `prototype`；项目已有 `design.md` 时先读再问增补还是重写。
- `setup-skills` 同步接上设计系统：探索阶段看 `design.md` 与 UI 信号，新增的 C 节只在有 UI 的仓库出现，`## Agent skills` 块模板多一节「设计系统」（产物还没出来时写的是"先跑 `/design-from-image`"），完成时提醒带图跑一次。`design-from-image` 的 Step 7 会原地替换这一节，不新增重复节。
