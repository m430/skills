---
name: design-from-image
description: "从一张设计参考图提取项目级的设计系统，产出项目根目录的 design.md。每个仓库做一次，产物是后续所有 UI 工作的规范来源。"
disable-model-invocation: true
---

# 从设计图提取设计系统

输入一张设计参考图，产出项目根目录的 `design.md`：后续所有 UI 工作都先读它。

**一张图给不出整套设计系统。** 图里有颜色、字阶、尺寸的一部分；交互状态、暗色模式、响应式、动效全都不在图上。本技能的做法是：图里有的严格提取，图里没有的当面问清，问不出来的如实留白。做不到“从一张图变出完整规范”，也不假装做得到，一份诚实标了缺口的 `design.md` 比一份写满猜测的更有用。

## 四条纪律

1. **每条都标来源。** 三选一，每条令牌、每条规则都要带：`观察到`（图里直接读到的，附出处控件）、`裁定`（图里没有，用户在第 4 步拍板的）、`推断`（图里没有、用户也没答，按惯例补的，必须写清推断依据）。三者都不属于的，进「缺口」章节留白。
2. **读控件，不读页面。** 提取的是控件与配色规律，不是参考图的页面排版。不照着参考图复刻布局；页面背景、留白、状态栏、装饰插画、icon 图形与 logo 内容都不纳入分析，带 icon 的控件只取容器样式。
3. **颜色来自像素。** 任何 hex 值必须由 `scripts/sample_colors.py` 采样得出，禁止目测报色。目测出来的 hex 看着很像，用起来全错。
4. **收敛成系统。** 终点是一套克制、成体系的令牌，不是把图上每个像素记下来。颜色超过 12 个、字阶超过 8 级、间距刻度超过 8 档，多半是没归纳，回去合并。

## 流程

- [ ] Step 1: 读图与清点
- [ ] Step 2: 提取（取色与测尺寸）
- [ ] Step 3: 归纳令牌并命名
- [ ] Step 4: 缺口提问
- [ ] Step 5: 核对页并确认
- [ ] Step 6: 写 design.md
- [ ] Step 7: 注册进仓库约定

### Step 1: 读图与清点

1. 读参考图，判断输入类型（控件展示板 / App 截图 / 网页截图 / 拍屏 / 设计稿导出）。类型特征与处理差异见 [references/extraction.md](references/extraction.md)；图里没有 UI 控件就停下，告诉用户这张图提不出设计系统。
2. 记录整体语境：平台、设计语言（Material / iOS HIG / 自定义）、信息密度、明暗模式。这些是「观察到」。
3. 枚举每个可独立识别的控件（按钮、输入框、卡片、列表行、Tab、Chip 等），记下类别与大致区域。这份清单是后面逐项提取与核对页的底稿。
4. 排除非控件区域：页面背景、留白、状态栏、装饰插画、icon 图形。

### Step 2: 提取（取色与测尺寸）

用脚本，不用眼睛。四个子命令，详细用法见脚本头部：

```bash
python3 scripts/sample_colors.py info 参考图.png
python3 scripts/sample_colors.py palette 参考图.png --top 16
python3 scripts/sample_colors.py sample 参考图.png --points "12,240;18,246"
python3 scripts/sample_colors.py scan 参考图.png --line "40,180,40,320"
```

`palette` 出全图主色，`sample` 按坐标取一点的颜色（坐标写像素或百分比），`scan` 沿一条线输出颜色分段与各段像素长度，用来量控件高度、内边距、圆角半径。坐标在图上看不准就先用 `info` 拿尺寸，再改用百分比。

采样点必须落在控件的纯色区域中心，离边框至少 2px，避开抗锯齿边缘与阴影渐变。

提取项与各项的测量方法见 [references/extraction.md](references/extraction.md)：颜色按角色分类（背景 / 文字 / 交互 / 语义 / 强调 / 分隔）、字阶、间距基准单位、圆角刻度、阴影层级、边框。每一项都记下它出现在哪个控件上。

### Step 3: 归纳令牌并命名

把各控件的共性收敛成语义令牌（token），按固定词汇命名，写进 [references/design-md-template.md](references/design-md-template.md) 的令牌表。用描述用途的名字（`--color-bg`、`--color-text-muted`、`--color-danger`），不用描述外观的名字（`--blue-500`、`--gray-2`）。

多个控件量到相近但不等的值时，判断哪些是实现抖动、哪些是真实的不同档位。实现抖动合并，真实档位保留。

### Step 4: 缺口提问

图答不了的问题在这里当面问清。从 [references/gap-questions.md](references/gap-questions.md) 里挑与本项目相关的，**最多 5 个，一次一个**。

运行环境提供结构化提问工具（`AskUserQuestion`）时用它提问，选项即候选答案、推荐项放首位；不可用时退回文本。用户答的记 `裁定`，跳过或答不上来的记 `推断` 或留在「缺口」。

按项目裁剪，别照着清单念：图里画了暗色模式的就跳过暗色问题，纯静态页跳过动效问题。

### Step 5: 核对页并确认

按 [templates/style-guide.html](templates/style-guide.html) 生成一份一次性核对页，把提取到的色板、字阶、间距刻度、控件样式铺开，打开浏览器让用户对着参考图比对。

用户指出偏差就回 Step 2 重新采样，不要就地改数字。

**核对页是一次性的，不进版本库。** 它只是令牌的一次渲染，事实来源是 `design.md` 和用户手里的参考图。确认后删掉，用户要留就自己留。

### Step 6: 写 design.md

按 [references/design-md-template.md](references/design-md-template.md) 的骨架写到项目根目录的 `design.md`。这一份是设计系统的唯一事实来源：不另发 `tokens.css`，不另发配色 JSON，令牌名直接写成 CSS 变量名供实现照抄。

写完走查一遍：有没有哪一条既不是「观察到」也不是「裁定」，却写成了肯定句。

### Step 7: 注册进仓库约定

让后来的会话知道该读 `design.md`：在项目 `CLAUDE.md` 或 `AGENTS.md` 的 `## Agent skills` 块里放一节。选文件规则同 `setup-skills`：`CLAUDE.md` 存在就改它，否则改 `AGENTS.md`，两者绝不同时创建。

**块里已有「设计系统」节就原地改成下面这段，不要新增重复节。** 那一节可能是 `setup-skills` 留下的前置说明（「写 UI 之前先跑 `/design-from-image`」），`design.md` 一旦产出，它就该换成读文件的说法。

```markdown
### 设计系统

写任何 UI 之前先读 `design.md`：颜色、排版、间距、组件规范都在里面。新样式一律走其中定义的令牌，不要在组件里写死色值。
```

`## Agent skills` 块不存在时不要自己造，告诉用户先运行 `/setup-skills`。

## 产物

- `design.md`（项目根目录）：设计系统规范，唯一事实来源
- 一次性核对页：确认后删除

## 边界

- 要的是**照参考图复刻页面**，不是提取规范 → 不是本技能，直接照图写 UI 就行。
- 要的是**验证某个 UI 想法** → 转 `prototype` 的 UI 分支。
- 项目已有 `design.md` → 先读出来，问清这次是增补还是重写，不要默默覆盖。

## 资源

- [references/extraction.md](references/extraction.md)：输入类型判断，每类令牌的提取与测量方法，边界情况
- [references/design-md-template.md](references/design-md-template.md)：`design.md` 骨架、令牌命名固定词汇、常见错误
- [references/gap-questions.md](references/gap-questions.md)：图答不了的决策提问库
- [templates/style-guide.html](templates/style-guide.html)：一次性核对页模板
- [scripts/sample_colors.py](scripts/sample_colors.py)：取色与测距脚本
