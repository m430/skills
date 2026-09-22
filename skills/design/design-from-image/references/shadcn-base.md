# shadcn/ui 底座

本技能不做从零发明设计系统这件事。底座是 shadcn/ui，参考图只负责改参数：图里读到的落进底座的槽位，图上没有的一律继承底座现状。

## 底座的三层

| 层 | 是什么 | 在哪 |
|---|---|---|
| Tailwind | 字阶、间距、阴影、断点的刻度 | 工具类，以及样式文件里的 `@theme inline` |
| 语义令牌 | 颜色与圆角的槽位，CSS 变量 | 样式文件的 `:root` 与 `.dark` |
| 组件 | 可用的控件集合，源码直接落在仓库里 | `components/ui/*.tsx` 之类的目录 |

令牌的值用 oklch 写。`@theme inline` 把每个令牌暴露成 Tailwind 工具类（`--color-background` 对应 `bg-background` 一类），这一段是底座给你的，不要动，除非确实新增了令牌。

## 槽位清单

图上读到的颜色往这些槽位里填。槽位名不要改，也不要另造平行的一套：`:root` 里只写 `--background`、`--primary` 这样的名字，`--color-*` 只出现在 `@theme inline` 的映射里，不往那里新增。

| 槽位 | 角色 | 图上通常对应 |
|---|---|---|
| `--background` | 页面底色 | 页面底 |
| `--foreground` | 主文字 | 标题与正文 |
| `--card` / `--card-foreground` | 卡片的面与面上的文字 | 卡片填充 |
| `--popover` / `--popover-foreground` | 弹层、下拉、菜单的面 | 气泡、下拉面板 |
| `--primary` / `--primary-foreground` | 主操作 | 主按钮底色 |
| `--secondary` / `--secondary-foreground` | 次操作 | 次要按钮 |
| `--muted` / `--muted-foreground` | 弱化的面与次要文字 | 占位符、说明文字、副标题 |
| `--accent` / `--accent-foreground` | 悬浮与选中的底 | 列表行 hover、选中项 |
| `--destructive` | 破坏性操作 | 删除按钮、错误提示 |
| `--border` | 边框与分隔线 | 卡片描边、列表分隔线 |
| `--input` | 输入框的描边 | 输入框边框 |
| `--ring` | 聚焦环 | 图上通常没有，留继承 |
| `--chart-1` 到 `--chart-5` | 图表配色 | 图上有图表才定 |
| `--sidebar-*` | 侧栏一整套 | 图上有侧栏才定 |
| `--radius` | 全站圆角的唯一基准 | 卡片与按钮的圆角 |

**填槽的纪律**：

- 一个图上角色对应一个槽位，不要让两个槽位写同一个值只是为了「看起来完整」。
- 图上有第四个中性面、而槽位里没有对得上的，先看能不能并进 `--muted` 或 `--accent`；确实要新增令牌，才同时写进 `:root`、`.dark` 与 `@theme inline` 三处。
- 「字色」槽位（`--*-foreground`）填的是画在那个面上的文字颜色：主按钮上的白字读出来填 `--primary-foreground`，不是按钮底色。这类槽位多为底座的对比关系，图上没有明显不同就留继承。

## 组件

**以仓库里的实际文件为准，不要背 shadcn 的默认样式。** 组件源码已经复制进仓库了，用户可能改过默认值、加过变体、删过尺寸档。要写某个组件的规范之前，先读 `components/ui/` 下那个文件。

图上控件与组件的常见对应：

| 图上控件 | 组件 |
|---|---|
| 按钮 | `Button`（变体与尺寸档看组件文件） |
| 输入框、多行输入 | `Input` / `Textarea` |
| 卡片 | `Card` |
| 标签、Chip | `Badge` |
| 开关、勾选 | `Switch` / `Checkbox` |
| 分段、Tab | `Tabs` |
| 弹层、气泡 | `Dialog` / `Popover` / `Tooltip` |
| 下拉选择 | `Select` / `DropdownMenu` |
| 表格、列表 | `Table` / 列表行多为组合 |

**只记与仓库现状的差异。** 图上按钮明显比默认矮，就写「`Button` 用 `size="sm"`」；图上卡片没有描边，就写「`Card` 去掉默认的 `border`」。与现状一致的不写。

图标图形不纳入提取（见纪律 2），图标库沿用项目现有设置，不照图上的 icon 形状换库。

## 字阶、间距、阴影

这三样都用 Tailwind 的现成刻度，不要另造令牌。

- **字体**：`--font-sans` 与 `--font-mono` 两个变量。换字体是换这两个变量的值，并在 `layout` 里接上字体加载。
- **字阶**：用 Tailwind 档位，默认 `text-xs` 12px、`text-sm` 14px、`text-base` 16px、`text-lg` 18px、`text-xl` 20px、`text-2xl` 24px、`text-3xl` 30px、`text-4xl` 36px。项目裁过刻度的话以项目实际值为准。
- **间距**：Tailwind 的基准是 `--spacing: 0.25rem`，`p-1` 4px、`p-2` 8px、`p-3` 12px、`p-4` 16px、`p-6` 24px、`p-8` 32px，以此类推。图上量到的间距落到最近的档位，不要写裸像素。
- **阴影**：用 Tailwind 的档位（`shadow-xs`、`shadow-sm`、`shadow-md` 这些），不写裸 `box-shadow` 值。
- **圆角**：只改 `--radius` 一个基准。`--radius-sm` 这些派生档位由样式文件里既有的 calc 行算出来，不要动那些行，也不要另写一套圆角变量。

## 应用改动

产物是 `design.md` 里的一段 CSS（`:root` 与 `.dark` 两个块），应用方式是替换样式文件里现有的同名两块。位置从 `components.json` 的 `tailwind.css` 字段读。

**`npx shadcn@latest apply` 会整体重装组件并覆盖主题、颜色、字体、图标。** 手工改过的令牌会被它冲掉。要换预设之前先备份这两个块，这一点在 `design.md` 里也提醒一句。

## 探测与读现状

Step 1 要用到的东西：

- `components.json`（仓库根或其上层）：存在就是 shadcn 项目。记下 `style`（现在取值只有 `new-york`，`default` 已弃用）、`tailwind.baseColor`（`neutral` / `stone` / `zinc` / `mauve` / `olive` / `mist` / `taupe`）、`tailwind.css`（样式文件路径）、`aliases`，其余字段一并读一遍。
- 样式文件里的 `:root` 与 `.dark`：这是改动的起点。要替换的值从这里抄，不要凭记忆写 shadcn 的默认值，仓库可能早就改过了。
- `components/ui/`：组件现状。

**不是 shadcn 项目就停下**：找不到 `components.json`，或样式文件里没有 `--background`、`--primary` 这类槽位，说明这个仓库还没接底座。告诉用户先运行 `npx shadcn@latest init`，不要退回去自造一套平行的令牌。

## 官方资源

改动细节以一手文档为准，本文件只记与提取流程有关的部分：

- 主题与令牌：<https://ui.shadcn.com/docs/theming>
- CLI 与 `components.json`：<https://ui.shadcn.com/docs/cli>、<https://ui.shadcn.com/docs/components-json>
- shadcn 自己也维护一份 agent skill（`shadcn-ui/ui` 仓库的 `skills/shadcn/`），装了的话命令细节以它为准。
