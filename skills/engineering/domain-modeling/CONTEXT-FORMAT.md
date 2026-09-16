# CONTEXT.md 格式

## 结构

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## 规则

- **要有立场。**同一概念存在多个词时，挑最好的一个，把其余列在 `_Avoid_` 之下。
- **定义紧凑。**最多一两句话。定义它*是*什么，不是它*做*什么。
- **只收录本项目上下文特有的术语。**一般编程概念（超时、错误类型、工具模式）即使项目大量使用也不属于这里。添加术语前先问：这是本上下文独有的概念，还是一般编程概念？只有前者属于这里。
- **当自然聚类出现时，用子标题给术语分组。**如果所有术语属于同一个内聚区域，平铺列表也可以。

## 单一 vs 多上下文仓库

**单一上下文（大多数仓库）：**仓库根目录一个 `CONTEXT.md`。

**多个上下文：**仓库根目录的 `CONTEXT-MAP.md` 列出各上下文、它们的位置，以及彼此之间的关系：

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md): receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

技能会推断适用哪种结构：

- 如果 `CONTEXT-MAP.md` 存在，读它来找到各上下文
- 如果只有根目录 `CONTEXT.md`，单一上下文
- 如果都不存在，在第一个术语敲定时惰性创建根目录 `CONTEXT.md`

存在多个上下文时，推断当前话题与哪一个相关。不清楚就问。
