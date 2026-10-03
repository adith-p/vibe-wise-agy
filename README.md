# VibeWise-agy

**You build. AI writes — on Antigravity CLI (`agy`).**

Learning-first development for Antigravity. The agent asks for your approach
first, helps you examine tradeoffs, and explains unfamiliar concepts. You own
the design; the agent writes the agreed code and explains what changed.

This is a community fork of
[vibe-wise](https://github.com/nykooi1/vibe-wise) (MIT, © 2026 Noah Kim),
ported from Claude Code to Antigravity. Not affiliated with Google or Anthropic.

Command: `/vibe-wise-learn-agy` (suffixed to avoid collision with generic
`/learn` skills).

## Requirements

* Antigravity CLI (`agy`) 1.2.16+
* Python 3.8+ (no extra packages needed)

## Install

```sh
git clone https://github.com/<OWNER>/vibe-wise-agy.git
agy plugin install ./vibe-wise-agy
agy plugin list
```

Replace `<OWNER>` with the repo owner after forking. Updates: re-pull and
re-run `agy plugin install`, or enable auto-update if your surface supports it.

Workspace-local alternative (project only, committed with your repo):

```sh
mkdir -p .agents/plugins
cp -r vibe-wise-agy .agents/plugins/vibe-wise-agy
```

Global skill alternative (no plugin wrapper):

```sh
mkdir -p ~/.gemini/antigravity-cli/skills
cp -r vibe-wise-agy/skills/vibe-wise-learn-agy ~/.gemini/antigravity-cli/skills/
cp -r vibe-wise-agy/skills/reset ~/.gemini/antigravity-cli/skills/
```

Verify in the `agy` TUI:

* `/hooks` shows `vibe-wise-restore`
* `/vibe-wise-learn-agy` starts onboarding with native pickers
* `/reset` shows a Cancel / Reset learning confirmation

## Use

* `/vibe-wise-learn-agy` — start or resume learning-first development.
  State lives in your project's `.vibe-wise/` (`profile.md`, `progress.md`,
  `project-map.md`). Add `.vibe-wise/` to `.gitignore` to keep notes local.
* `/reset` — read-only preview first, then Cancel / Reset learning.
  Originals are backed up under `.vibe-wise/backups/`; source code is untouched.

Build checkpoints ask you to reason through the approach; Design checkpoints
record it without writing code; Implementation checkpoints authorize a concrete
scope. After implementation you get a short report (files, mechanics, tests,
verification results).

## Antigravity differences from the Claude Code original

* `plugin.json` at the repo root (agy manifest with `$schema`); no
  `.claude-plugin/`, no `marketplace.json`.
* `hooks.json` at the root uses `PreInvocation` → `scripts/session_restore.py`,
  emitting `{injectSteps: [{ephemeralMessage}]}`. Antigravity has no
  `SessionStart` event, so restoration is best-effort: after `/resume`,
  restart, or compaction, re-run `/vibe-wise-learn-agy` if a pending
  checkpoint isn't restored. `rules/vibe-wise-core.md` is a fallback reminder.
* `SKILL.md` frontmatter is `name` + `description` only
  (no `disable-model-invocation`).
* Tool names: `view_file`, `find_by_name`, `grep_search`, `list_dir`,
  `run_command`, `ask_question`, `write_to_file` / `replace_file_content`.
* Scripts are black boxes: run with `--help` rather than reading source.

## Development / checks

```sh
agy plugin validate .
python3 -B -m unittest discover -s tests -v
git diff --check
```

Live smoke test: install into a temp project, run `/vibe-wise-learn-agy`,
complete onboarding with defaults, request a small feature, confirm a
Build checkpoint appears before code, then `/reset` with Cancel (no changes)
and with Reset learning (backup created, onboarding restarts).

## License

MIT — see `LICENSE`. Original © 2026 Noah Kim; Antigravity port
modifications in this fork. Keep the license notice with copies.
