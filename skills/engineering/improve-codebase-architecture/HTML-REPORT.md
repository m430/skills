# HTML 报告格式

架构评审渲染为操作系统临时目录里的一个自包含 HTML 文件。Tailwind 和 Mermaid 都来自 CDN。图状的图表交给 Mermaid 最可靠；手工 div 和内联 SVG 负责更有编辑感的视觉（质量图、剖面图）。两者混用：别什么都压在 Mermaid 上，否则整份报告会开始显得千篇一律。

## 骨架

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 头部

仓库名、日期，外加一个紧凑的图例：实心框 = 模块，虚线 = 接缝，红色箭头 = 泄漏，粗深色框 = 深模块。不要介绍段落。直接进入候选。

## 候选卡片

图承担表达主体。文字稀少、平实，毫无客套地使用词汇表术语（来自 `/codebase-design` 技能）。

每个候选是一个 `<article>`：

- **标题**：短，点出这次深化（比如 "Collapse the Order intake pipeline"）。
- **徽章行**：建议强度（`Strong` = emerald，`Worth exploring` = amber，`Speculative` = slate），外加依赖类别的标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **文件**：等宽字体列表，`font-mono text-sm`。
- **前后对比图**：核心所在。两列并排。模式见下。
- **问题**：一句话。痛在哪。
- **解决方案**：一句话。改什么。
- **收获**：列表项，每条不超过 6 个词。比如 "Tests hit one interface"、"Pricing logic stops leaking"、"Delete 4 shallow wrappers"。
- **ADR 提示框**（如适用）：琥珀色底色框里的一句话。

不要成段的解释。如果一张图需要一段文字才能被理解，重画这张图。

## 图示模式

选贴合候选的模式。混着用。别让每张图都长一个样。多样性本身就是目的。

### Mermaid 图（依赖 / 调用流的主力）

当要点是 "X 调 Y 调 Z，看看这团乱麻" 时，用 Mermaid 的 `flowchart` 或 `graph`。外面套一张 Tailwind 样式的卡片，免得它显得像硬塞进来的。用 classDef 给泄漏边涂红、给深模块涂深。时序图很适合表达 "before: 6 次往返；after: 1 次" 这类对比。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手工盒线图（当 Mermaid 的布局跟你较劲时）

模块用带边框和标签的 `<div>`。箭头用绝对定位在 relative 容器之上的内联 SVG `<line>` 或 `<path>` 元素。当你想让 "after" 图看起来像一个粗边框的深模块、内部细节灰化时，就该用它，因为 Mermaid 画不出那种分量感。

### 剖面图（适合层次化的浅薄）

堆叠水平条带（`h-12 border-l-4`）来展示一次调用穿过的层。Before：6 条什么也不做的薄层。After：1 条厚条带，标注合并后的职责。

### 质量图（适合"接口和实现一样宽"）

每个模块两个矩形：一个表示接口面积，一个表示实现。Before：接口矩形几乎和实现矩形一样高（浅）。After：接口矩形矮、实现矩形高（深）。

### 调用图坍缩

Before：一棵渲染成嵌套盒子的函数调用树。After：同一棵树坍缩成一个盒子，如今已内化的调用在里面淡显。

## 样式指引

- 偏编辑感，不要企业仪表盘感。留白慷慨。标题可选衬线体（`font-serif` 配 stone/slate 效果很好）。
- 用色克制：一种强调色（emerald 或 indigo），另加红色表示泄漏、琥珀色表示警告。
- 图保持约 320px 高，让前后对比能舒服地并排而不用滚动。
- 图内的模块标签用 `text-xs uppercase tracking-wider`，让它们读起来像示意图而不是 UI。
- 仅有的脚本是 Tailwind CDN 和 Mermaid ESM 导入。除此之外报告是静态的：没有应用代码，除 Mermaid 自身的渲染外没有任何交互。

## 首推建议一节

一张更大的卡片。候选名、一句为什么、一条指向其卡片的锚点链接。就这些。

## 语气

平实的英语，简洁，但架构名词和动词直接取自 `/codebase-design` 技能。简洁不是漂移的借口。

**只用这些词：** module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**绝不替换为：** component、service、unit（指 module 时）· API、signature（指 interface 时）· boundary（指 seam 时）· layer、wrapper（想表达 module 时）。

**贴合风格的措辞：**

- "Order intake module is shallow: interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**收获列表项**用词汇表术语点出收获：*"locality: bugs concentrate in one module"*、*"leverage: one interface, N call sites"*、*"interface shrinks; implementation absorbs the wrappers"*。不要写 *"easier to maintain"* 或 *"cleaner code"*，这些术语不在词汇表里，配不上占的那个位置。

不闪烁其词、不清嗓子开场、不写 "it's worth noting that…"。一句话能成为列表项的，就做成列表项。一个列表项能删的，就删。一个术语不在 `/codebase-design` 词汇表里的，先从表里找一个合用的，再去发明新词。
