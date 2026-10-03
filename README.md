# vibe-wise-agy

Antigravity CLI (`agy`) plugin with two skills: `vibe-wise-learn-agy` and `reset`.

Fork of [vibe-wise](https://github.com/nykooi1/vibe-wise) (MIT, © 2026 Noah Kim),
ported from Claude Code to Antigravity. Not affiliated with Google or Anthropic.

`vibe-wise-learn-agy` requires the user to provide a design approach before the
agent writes code. It uses Build / Design / Implementation checkpoints and stores
state in the project's `.vibe-wise/` directory. `reset` backs up that state and
restarts onboarding.

## Requirements

* `agy` 1.2.16+
* Python 3.8+ (standard library only)

## Install

```sh
git clone git@github.com:adith-p/vibe-wise-agy.git
agy plugin install ./vibe-wise-agy
agy plugin list
```

To update: pull and re-run `agy plugin install`.

Workspace-local install (scoped to one project):

```sh
mkdir -p .agents/plugins
cp -r vibe-wise-agy .agents/plugins/vibe-wise-agy
```

Verify in the `agy` TUI: `/hooks` lists `vibe-wise-restore`,
`/vibe-wise-learn-agy` starts onboarding, `/reset` shows a Cancel / Reset
confirmation.

## Usage

* `/vibe-wise-learn-agy` — start or resume. State: `.vibe-wise/profile.md`,
  `progress.md`, `project-map.md`. Add `.vibe-wise/` to `.gitignore`.
* `/reset` — previews notes, asks Cancel / Reset learning, backs up originals
  to `.vibe-wise/backups/` on confirm. Source code is not modified.

## Notes

* Root `hooks.json` registers `PreInvocation` → `scripts/session_restore.py`,
  which returns `{injectSteps: [{ephemeralMessage}]}`. Antigravity has no
  `SessionStart` event, so after `/resume`, restart, or compaction, re-run
  `/vibe-wise-learn-agy` if a pending checkpoint is not restored.
* `SKILL.md` frontmatter is `name` + `description` only.
* `rules/vibe-wise-core.md` is a fallback reminder when the hook does not fire.

## Checks

```sh
agy plugin validate .
python3 -B -m unittest discover -s tests -v
git diff --check
```

## License

MIT — see `LICENSE`. Original © 2026 Noah Kim.
