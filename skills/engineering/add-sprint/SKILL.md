---
name: add-sprint
description: "开启一个新迭代：确认上一个已关闭，问清迭代目标，初始化 sprint 目录与 SPRINT.md。"
disable-model-invocation: true
---

# 开启迭代

## 流程

### 1. 确认上一个迭代已关闭

列出 `sprints/` 下的 `sprint-*/` 目录，找编号最大的一个：

- 没有：本次迭代是 `sprint-01`。
- 它的 `SPRINT.md` 状态是"已关闭"：本次是编号加一。
- 状态还是"进行中"：**停下**，告诉用户先跑 `/close-sprint` 收掉它。不要替他关闭，也不要跳号。

### 2. 问迭代目标

问用户这个迭代的目标是什么，一次一个问题。

目标是一句话能说完的可交付结果（例如"用户能导出报表"），不是任务清单。用户一时说不上来时，可以把 `sprints/backlog/` 里的标题念给他当参考，但不要替他定。

### 3. 初始化

1. 建目录 `sprints/sprint-NN/`，编号两位补零（`sprint-01`），这样按文件名排序就是迭代顺序。
2. 按下面的模板写 `SPRINT.md`，把目标填进去。
3. 告诉用户下一步跑 `/plan-sprint` 拆 story。

## 模板

<sprint-template>

# sprint-NN

**目标：** 一句话

**状态：** 进行中

## 故事

（`/plan-sprint` 拆出来后回填）

## 迭代评估

（`/close-sprint` 时写入）

</sprint-template>
