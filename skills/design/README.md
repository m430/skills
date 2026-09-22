# Design

Skills for interface and design-system work.

## User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[design-from-image](./design-from-image/SKILL.md)**: Extract a project design system from one reference image into a root `design.md`: colours sampled from pixels, type scale, spacing, component specs, and an explicit list of the gaps the image cannot answer. Run once per repo that has UI.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[prototype](./prototype/SKILL.md)**: Build a throwaway prototype to answer a design question: a single shareable HTML file for state/logic, or several toggleable UI variations.
