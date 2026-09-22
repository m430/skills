---
"m430-skills": minor
---

新增 `design/` 桶，把设计类技能从 `engineering/` 里抽出来单独管理。

- `design-from-image` 与 `prototype` 移到 `skills/design/`。`design/` 是 promoted 桶，两者仍随插件分发，斜杠命令与触发方式都不变。
- 新增 `skills/design/README.md`（英文，按 User-invoked / Model-invoked 分组）。
- 顶层 README 的「技能参考」新增 `### Design` 节，`CLAUDE.md`（`AGENTS.md` 是指向它的软链）的桶列表与 promoted 规则同步加上 `design/`。
