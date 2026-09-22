# m430 Skills

A collection of agent skills (slash commands and behaviors) loaded by Claude Code. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup-skills`.

## Language

**需求（backlog item）**:
An unnumbered requirement file under `sprints/backlog/`, written by `add-backlog`, waiting to be planned into a sprint.
_Avoid_: issue, ticket

**Sprint（迭代）**:
A numbered delivery window, one directory `sprints/sprint-NN/` holding a `SPRINT.md` and its story and bug files.

**Story**:
A vertical slice of a sprint, one file `sprints/sprint-NN/story-NN-<slug>.md`, with acceptance criteria, a task list, and the stories it is blocked by. Story numbers are globally monotonic across sprints.
_Avoid_: ticket, issue

**Bug**:
A defect being fixed inside a sprint, one file `sprints/sprint-NN/bug-NN-<slug>.md`, holding its description, solution and status. Bug numbers are globally monotonic across sprints.
_Avoid_: issue, defect ticket

## Relationships

- A **Sprint** holds many **Stories** and **Bugs**; a **Story** may block another **Story**
- A **需求** becomes a **Story** (or several) when a sprint is planned
