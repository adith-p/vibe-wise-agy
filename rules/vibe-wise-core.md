# VibeWise core (agy Rule, fallback reminder)

When `.vibe-wise/profile.md` exists and says `Learning mode: active`,
follow `skills/vibe-wise-learn-agy/SKILL.md` + `behavior.md`:
ask for the learner's approach first, keep guidance minimal, confirm design
before coding, and use `ask_question` for Design/Implementation confirmations.

This rule is a fallback. The `PreInvocation` hook in `hooks.json` injects the
full restore message when possible. After `/resume`, restart, or compaction,
run `/vibe-wise-learn-agy` to restore pending checkpoints.
