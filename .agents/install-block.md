# The canonical install block

One install story, one wording. `README.md` must say **this** and nothing else. Change it here first, then propagate.

This repo is its own single-plugin marketplace (`.claude-plugin/marketplace.json`), and every skill is also installable per-skill via [skills.sh](https://skills.sh).

## Claude Code: the plugin

```bash
/plugin marketplace add m430/skills
```

Then, from inside a session:

```bash
/plugin install m430-skills@m430
```

## Codex, and other agents: skills.sh

The plugin is Claude Code only. Everywhere else, [skills.sh](https://skills.sh) copies editable skill files into the project. Use the whole-set form on `README.md`:

```bash
npx skills@latest add m430/skills
```

Pick the skills you want, and which coding agents to install them on. **The installer lets you choose which skills to take: make sure `setup-skills` is one of them.**

…and the single-skill form wherever one skill is named on its own:

```bash
npx skills@latest add m430/skills --skill=<name>
```

```bash
npx skills@latest update <name>
```

`skills@latest` is the pinned spelling in both.

## Local development (maintainers of this repo)

```bash
scripts/link-skills.sh
```

Links every skill outside `misc/` into `~/.claude/skills` and `~/.agents/skills` as symlinks into this checkout, so a `git pull` keeps installed skills current.

## The two install routes are exclusive

The plugin is a managed bundle you install once; skills.sh writes files you own and edit. Installing both leaves the user with every skill twice: always say "pick one".
