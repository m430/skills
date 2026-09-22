# 领域文档

工程技能在探索代码库时应如何消费本仓库的领域文档（domain documentation）。

## 探索前，先读这些

- 仓库根目录的 **`CONTEXT.md`**，或
- 若存在，仓库根目录的 **`CONTEXT-MAP.md`**：它指向每个上下文（context）各自的 `CONTEXT.md`。读取与主题相关的每一份。
- **`docs/adr/`**：阅读涉及你即将工作区域的 ADR。在多上下文仓库中，还要检查 `src/<context>/docs/adr/` 中的上下文级决策。

如果这些文件不存在，**静默继续**。不要指出它们的缺失；不要建议预先创建。`/domain-modeling` 技能（通过 `/grill-with-docs` 和 `/improve-codebase-architecture` 进入）会在术语或决策真正被敲定时惰性创建它们。

## 文件结构

单一上下文仓库（大多数仓库）：

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文仓库（根目录存在 `CONTEXT-MAP.md` 时）：

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## 使用词汇表的词汇

当你的输出提到某个领域概念时（在 story 标题、重构提案、假设、测试名中），使用 `CONTEXT.md` 中定义的术语。不要漂移到词汇表明确避用的同义词。

如果你需要的概念还不在词汇表中，这是一个信号：要么你在发明项目不使用的语言（请重新考虑），要么存在真实的缺口（为 `/domain-modeling` 记下它）。

## 标记 ADR 冲突

如果你的输出与现有 ADR 矛盾，显式指出，而不是静默覆盖：

> _与 ADR-0007（event-sourced orders）矛盾，但值得重新讨论，因为……_
