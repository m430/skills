# MISSION.md 格式

`MISSION.md` 位于工作区根目录。它记录用户学习这个主题的_原因_。每一个教学决策（接下来教什么、呈现哪些资源、设计哪些练习）都应能回溯到这份文档。

## 模板

```md
# Mission: {Topic}

## Why
{1-3 sentences. The concrete real-world goal the user is chasing. What changes in their life or work when they have this skill? Avoid abstract framings like "to understand X"; push for the underlying outcome.}

## Success looks like
- {A specific, observable thing the user will be able to do}
- {Another specific thing}
- {…}

## Constraints
- {Time, budget, prior commitments, learning preferences, anything that bounds the approach}

## Out of scope
- {Adjacent topics the user explicitly does not want to chase right now, protecting the zone of proximal development}
```

## 规则

- **每个工作区只有一个使命。** 如果用户想学两件互不相关的事，那就是两个工作区。
- **具体胜于抽象。** "十月前跑完半程马拉松" 好过 "变得更健康"；"给我的团队交付一个 Rust CLI" 好过 "学会 Rust"。
- **对含糊其辞要顶回去。** 如果用户说不清为什么，先追问他们再动笔。糟糕的使命不如没有使命。
- **现实变了就修订。** 使命会变。当用户的目标移动时，更新这份文件：不要让一个过时的使命继续左右后续会话。
- **保持简短。** 如果 `MISSION.md` 超出一屏，它就不再是罗盘，而变成了计划。
