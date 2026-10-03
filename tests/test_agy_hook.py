"""Agy-port hook tests: PreInvocation injectSteps contract."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "hooks.json").read_text())
SCRIPT = ROOT / "scripts/session_restore.py"


class AgyHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vibe-wise-agy-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / "project with spaces"
        self.project.mkdir()
        (self.project / ".git").mkdir()

    def state(self, project=None, mode="active"):
        directory = (project or self.project) / ".vibe-wise"
        directory.mkdir(exist_ok=True)
        (directory / "profile.md").write_text(
            f"# Learner Profile\nLearning mode: {mode}\nOnboarding: complete\n", encoding="utf-8"
        )
        (directory / "project-map.md").write_text("# Project Map\nCLI -> service\n", encoding="utf-8")
        (directory / "progress.md").write_text("# Learning Progress\n## Queues\nNeeds reinforcement.\n",
                                               encoding="utf-8")
        return directory

    def run_hook(self, payload=None, cwd_arg=None):
        cmd = [sys.executable, "-B", str(SCRIPT)]
        if cwd_arg:
            cmd += ["--cwd", str(cwd_arg)]
        payload = payload if payload is not None else {
            "workspacePaths": [str(self.project)],
            "conversationId": "test-conv",
            "invocationNum": 0,
        }
        result = subprocess.run(
            cmd, input=json.dumps(payload), text=True, capture_output=True, timeout=5,
            env={"PATH": os.pathsep.join((str(Path(sys.executable).parent), os.defpath))},
            cwd=self.root,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout) if result.stdout else None

    def test_hooks_json_uses_preinvocation(self):
        self.assertIn("vibe-wise-restore", CONFIG)
        self.assertIn("PreInvocation", CONFIG["vibe-wise-restore"])
        self.assertNotIn("SessionStart", json.dumps(CONFIG))

    def test_skill_name(self):
        text = (ROOT / "skills/vibe-wise-learn-agy/SKILL.md").read_text()
        self.assertIn("name: vibe-wise-learn-agy", text)
        self.assertNotIn("disable-model-invocation", text)

    def test_fresh_project_emits_nothing(self):
        self.assertIsNone(self.run_hook())
        self.assertEqual(list(self.project.iterdir()), [self.project / ".git"])

    def test_active_project_injects_ephemeral_message(self):
        state = self.state()
        out = self.run_hook()
        msg = out["injectSteps"][0]["ephemeralMessage"]
        self.assertIn(str(ROOT / "skills/vibe-wise-learn-agy/SKILL.md"), msg)
        self.assertIn(str(state), msg)
        self.assertIn("Search the entire progress.md", msg)
        self.assertNotIn("hookSpecificOutput", json.dumps(out))

    def test_paused_stays_silent(self):
        self.state(mode="paused")
        self.assertIsNone(self.run_hook())

    def test_legacy_and_boundaries(self):
        state = self.state()
        legacy = state.with_name(".sensible-vibes")
        state.rename(legacy)
        out = self.run_hook()
        self.assertIn(str(legacy), out["injectSteps"][0]["ephemeralMessage"])
        child = self.project / "worktree"
        child.mkdir()
        (child / ".git").write_text("gitdir: /other/.git/worktrees/t")
        self.assertIsNone(self.run_hook({"workspacePaths": [str(child)]}))

    def test_malformed_inputs_exit_cleanly(self):
        for raw in ("", "{", "[]", "null"):
            r = subprocess.run([sys.executable, "-B", str(SCRIPT)], input=raw,
                               text=True, capture_output=True, timeout=5, cwd=self.root)
            self.assertEqual(r.returncode, 0)
            self.assertEqual(r.stdout, "")


if __name__ == "__main__":
    unittest.main()
