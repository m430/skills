---
"m430-skills": minor
---

删除六个用不到的技能与整个 `in-progress/` 试验桶，收缩日常可见面：

- **`resolving-merge-conflicts`**、**`handoff`**、**`teach`**、**`to-questionnaire`**、**`wait-what`**、**`writing-for-agents`** 从仓库移除，README 与 `plugin.json` 里的条目同步下架。
- `in-progress/` 桶整体删除（`setup-ts-deep-modules`、`loop-me`、`writing-fragments`、`writing-shape`、`claude-handoff`、`retro`、`implement-spec`、`writing-beats`），不再随仓库分发；`CLAUDE.md` 的桶说明与 `scripts/link-skills.sh` 的注释同步收窄到 `misc/` 这一个非 promoted 桶。
- 工作流地图相应简化：阶段 1 去掉问卷入口，阶段 4 去掉冲突处理与交接两个旁支。
