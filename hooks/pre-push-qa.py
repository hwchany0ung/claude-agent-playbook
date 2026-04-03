#!/usr/bin/env python3
"""
PreToolUse Hook — run tests before git push, block on failure.

Setup in .claude/settings.json:
  "PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "python3 /path/to/pre-push-qa.py", "timeout": 120 }] }]

Customize BACKEND_TEST_CMD and FRONTEND_TEST_CMD for your project.
"""
import sys
import json
import subprocess

# ── Customize these for your project ──────────────────────────────────────────
BACKEND_DIR = "backend"
BACKEND_TEST_CMD = ["python", "-m", "pytest", "tests/unit/", "-q", "-m", "unit", "--tb=no", "--no-header"]

FRONTEND_DIR = "frontend"
FRONTEND_TEST_CMD = ["npm", "test", "--", "--run", "--reporter=dot"]
# ──────────────────────────────────────────────────────────────────────────────

try:
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
except Exception:
    data = {}

tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})
command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""

# Only intercept git push
if tool_name != "Bash" or "git push" not in command:
    sys.exit(0)

# Warn on force push but don't block
if "--force" in command or "-f" in command:
    print(json.dumps({
        "continue": True,
        "reason": "[pre-push-qa] WARNING: force push detected. Proceed carefully."
    }))
    sys.exit(0)

# Run backend unit tests
result = subprocess.run(
    BACKEND_TEST_CMD,
    capture_output=True, text=True,
    cwd=BACKEND_DIR
)

if result.returncode not in (0, 5):  # 5 = no tests collected (pytest)
    print(json.dumps({
        "continue": False,
        "reason": (
            f"[pre-push-qa] Backend tests FAILED. Push blocked.\n"
            f"{(result.stdout or result.stderr)[-500:]}"
        )
    }))
    sys.exit(2)

# Run frontend tests
fe_result = subprocess.run(
    FRONTEND_TEST_CMD,
    capture_output=True, text=True,
    cwd=FRONTEND_DIR,
    shell=(sys.platform == "win32")
)

if fe_result.returncode != 0:
    print(json.dumps({
        "continue": False,
        "reason": (
            f"[pre-push-qa] Frontend tests FAILED. Push blocked.\n"
            f"{(fe_result.stdout or fe_result.stderr)[-500:]}"
        )
    }))
    sys.exit(2)

sys.exit(0)
