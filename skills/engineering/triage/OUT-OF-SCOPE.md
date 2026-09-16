# Out-of-Scope 知识库

仓库中的 `.out-of-scope/` 目录保存被拒绝的功能请求的持久记录。它有两个用途：

1. **机构记忆**：记录一个功能为何被拒绝，issue 关闭之后理由也不会丢失
2. **去重**：当新 issue 进来并与既往拒绝匹配时，技能可以亮出之前的决定，而不是重新争一遍

## 目录结构

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

每个**概念**一个文件，而不是每个 issue 一个。请求同一件事的多个 issue 归入同一个文件。

## 文件格式

文件应以轻松、可读的风格书写，更像一篇短设计文档，而不是一条数据库记录。用段落、代码示例和例子把理由写清楚，让第一次接触到它的人也能看得懂、用得上。

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42: "Add dark mode support"
- #87: "Night theme for accessibility"
- #134: "Dark theme option"
```

### 给文件命名

为概念取一个简短、描述性的 kebab-case 名字：`dark-mode.md`、`plugin-system.md`、`graphql-api.md`。名字应足够好认，让浏览目录的人不用打开文件就知道被拒绝的是什么。

### 写理由

理由要有实质内容：不是“我们不想要这个”，而是为什么。好的理由会引用：

- 项目范围或哲学（“本项目专注于 X；主题化是下游消费者的事”）
- 技术约束（“支持它需要 Y，这与我们的 Z 架构冲突”）
- 战略决策（“我们选择用 A 而不是 B，因为……”）

理由应当耐久。不要引用临时情况（“我们现在太忙了”）；那些不是真正的拒绝，只是推迟。

## 何时检查 `.out-of-scope/`

分诊期间（第 1 步：收集上下文），读 `.out-of-scope/` 里的所有文件。评估新 issue 时：

- 检查请求是否匹配已有的 out-of-scope 概念
- 匹配靠概念相似度，而不是关键词：“night theme” 匹配 `dark-mode.md`
- 如果有匹配，向维护者指出：“这和 `.out-of-scope/dark-mode.md` 相似。我们之前拒绝过它，理由是 [理由]。你现在还是这么想吗？”

维护者可以：

- **确认**：把新 issue 追加到现有文件的 “Prior requests” 列表，然后关闭
- **重新考虑**：删除或更新该 out-of-scope 文件，issue 改走正常分诊流程
- **不认同**：两个 issue 相关但不同，继续正常分诊流程

## 何时写入 `.out-of-scope/`

仅当 **enhancement**（而非 bug）被*拒绝*并标记 `wontfix` 时。这条规则对 enhancement PR 与 issue 完全一致：被拒绝的 PR 也记录在这里，免得同一个请求又以新代码的形式回来。

当某件事因**已经实现**而以 `wontfix` 关闭时，**不要**写到这里。那是已建成的功能，不是被拒绝的功能；记录它会用假拒绝污染去重检查。此时关闭评论应指出该功能已经在哪里。

流程：

1. 维护者判定某个功能请求超出范围
2. 检查是否已有匹配的 `.out-of-scope/` 文件
3. 有：把新 issue 追加到 “Prior requests” 列表
4. 没有：以概念名、决定、理由和第一条既往请求创建新文件
5. 在 issue 上发一条评论，解释决定并提及 `.out-of-scope/` 文件
6. 以 `wontfix` 标签关闭 issue

## 更新或移除 out-of-scope 文件

如果维护者对之前被拒绝的概念改变了主意：

- 删除 `.out-of-scope/` 文件
- 技能不需要重开旧 issue；它们是历史记录
- 触发这次重新考虑的新 issue 走正常分诊流程
