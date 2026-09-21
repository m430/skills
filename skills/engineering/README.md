# Engineering

Skills I use daily for code work.

## User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[grill-with-docs](./grill-with-docs/SKILL.md)**: Grilling session that also builds your project's domain model, sharpening terminology and updating `CONTEXT.md` and ADRs inline.
- **[add-backlog](./add-backlog/SKILL.md)**: Record an idea from the conversation as an unnumbered backlog requirement under `sprints/backlog/`, waiting to be planned into a sprint.
- **[add-sprint](./add-sprint/SKILL.md)**: Open a new sprint: confirm the previous one is closed, ask for the iteration goal, then scaffold `sprints/sprint-NN/` and its `SPRINT.md`.
- **[plan-sprint](./plan-sprint/SKILL.md)**: Recommend backlog requirements that fit the sprint goal, break it into a story list you confirm, then write one numbered story file per story.
- **[add-story](./add-story/SKILL.md)**: Add a story to the current sprint and update `SPRINT.md`.
- **[delete-story](./delete-story/SKILL.md)**: Remove a story from the current sprint, cleaning up `SPRINT.md` and any blocking edges that point at it.
- **[implement-story](./implement-story/SKILL.md)**: Build the work one story file describes, driving `/tdd` at pre-agreed seams and closing out with `/code-review` before committing, then update the story's status.
- **[close-sprint](./close-sprint/SKILL.md)**: Assess the sprint's completion into `SPRINT.md` and close it, deciding where each unfinished story goes.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)**: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **[setup-skills](./setup-skills/SKILL.md)**: Configure this repo for the engineering skills (issue tracker, domain doc layout). Run once per repo.
- **[to-tickets](./to-tickets/SKILL.md)**: Break any plan, spec, or conversation into a set of vertical-slice tickets, each declaring its blocking edges, whether as text in a local file or as native blocking links on a real tracker.
- **[implement](./implement/SKILL.md)**: Build the work described by a spec or set of tickets, driving `/tdd` at pre-agreed seams and closing out with `/code-review` before committing.
- **[wayfinder](./wayfinder/SKILL.md)**: Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on the issue tracker, resolved one at a time until the way to the destination is clear.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[prototype](./prototype/SKILL.md)**: Build a throwaway prototype to answer a design question: a single shareable HTML file for state/logic, or several toggleable UI variations.

- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)**: Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./research/SKILL.md)**: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.
- **[tdd](./tdd/SKILL.md)**: Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[domain-modeling](./domain-modeling/SKILL.md)**: Actively build and sharpen a project's domain model by challenging terms, stress-testing with scenarios, and updating `CONTEXT.md` and ADRs inline.
- **[codebase-design](./codebase-design/SKILL.md)**: Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.
- **[code-review](./code-review/SKILL.md)**: Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/spec?), run as parallel sub-agents.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)**: Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation, never `--abort`.
- **[wizard](./wizard/SKILL.md)**: Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.
