# Design

Skills for interface and design-system work.

## User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[design-from-image](./design-from-image/SKILL.md)**: Retune a project's design system on top of the shadcn/ui base from one reference image, into a root `design.md`: token changes mapped onto shadcn's slots, colours sampled per pixel as paste-ready oklch, and every line labelled observed / decided / inherited / inferred. Run once per shadcn project.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[prototype](./prototype/SKILL.md)**: Build a throwaway prototype to answer a design question: a single shareable HTML file for state/logic, or several toggleable UI variations.
