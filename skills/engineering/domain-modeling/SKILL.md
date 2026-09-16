---
name: domain-modeling
description: 构建并打磨项目的领域模型。在讨论代码库术语、编写或编辑 CONTEXT.md、记录或编辑 ADR 时使用。
---

# 领域建模（Domain Modeling）

在设计的同时主动构建并打磨项目的领域模型（domain model）。这是一门*主动*的纪律：挑战术语、发明边界场景，并在词汇和决策一成形时就写下来。（仅仅*阅读* `CONTEXT.md` 获取词汇不是本技能：那是一行指令任何技能都能做到的习惯。本技能用于你在改变模型，而不只是消费模型的时候。）

## 文件结构

大多数仓库只有一个上下文：

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

如果根目录存在 `CONTEXT-MAP.md`，仓库就有多个上下文。map 指向每个上下文所在的位置：

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

惰性创建文件：只在有东西可写时创建。如果 `CONTEXT.md` 不存在，在第一个术语敲定时创建它。如果 `docs/adr/` 不存在，在需要第一个 ADR 时创建它。

## 会话期间

### 对照词汇表发起挑战

当用户使用的术语与 `CONTEXT.md` 中的既有语言冲突时，立即指出。“你的词汇表把 ‘cancellation’ 定义为 X，但你的意思似乎是 Y。到底是哪个？”

### 打磨模糊语言

当用户使用模糊或多义的术语时，提出一个精确的规范术语。“你说的是 ‘account’：你指 Customer 还是 User？它们是不同的东西。”

### 讨论具体场景

当领域关系正在被讨论时，用具体场景对其做压力测试。发明能探到边界场景、迫使用户精确说清概念之间边界的场景。

### 与代码交叉验证

当用户陈述某事物如何工作时，检查代码是否一致。发现矛盾就摆出来：“你的代码取消整个 Order，但你刚说部分取消是可能的。哪个是对的？”

### 就地更新 CONTEXT.md

术语敲定时，当场更新 `CONTEXT.md`。不要攒批：发生时就捕获。格式见 [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)。

`CONTEXT.md` 应当完全不含实现细节。不要把 `CONTEXT.md` 当作规格（spec）、草稿本或实现决策的仓库。它是词汇表，仅此而已。

### 节制地提议 ADR

只有当以下三条全部成立时才提议创建 ADR：

1. **难以逆转**：日后改变主意的成本是有分量的
2. **没有上下文会令人意外**：未来的读者会疑惑“他们为什么这么做？”
3. **真实权衡的结果**：存在真正的备选项，而你出于具体理由选了其中一个

三条缺任何一条，就跳过 ADR。格式见 [ADR-FORMAT.md](./ADR-FORMAT.md)。
