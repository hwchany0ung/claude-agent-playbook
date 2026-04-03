#!/usr/bin/env python3
"""
PreToolUse Hook — git commit message convention validation
Blocks commits that don't follow Conventional Commits format.

Setup in .claude/settings.json:
  "PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "python3 /path/to/validate-commit.py", "timeout": 10 }] }]
"""
import sys
import json
import re

ALLOWED_TYPES = {"feat", "fix", "chore", "docs", "refactor", "test", "style", "perf", "ci", "revert"}
COMMIT_PATTERN = re.compile(r'^(feat|fix|chore|docs|refactor|test|style|perf|ci|revert)(\(.+\))?: .{3,}', re.MULTILINE)

try:
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
except Exception:
    data = {}

tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})
command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""

# Only check git commit commands
if tool_name != "Bash" or "git commit" not in command:
    sys.exit(0)

# Allow --no-edit and --amend without -m (no new message)
if "--no-edit" in command or ("--amend" in command and "-m" not in command):
    sys.exit(0)

# Extract message from -m flag
msg_match = re.search(r'-m\s+["\']([^"\']+)["\']', command)
if not msg_match:
    # HEREDOC or other pattern — cannot parse, allow through
    sys.exit(0)

commit_msg = msg_match.group(1)

if not COMMIT_PATTERN.match(commit_msg):
    print(json.dumps({
        "continue": False,
        "reason": (
            f"[validate-commit] Invalid commit message: '{commit_msg[:60]}'\n"
            f"Required format: <type>(<scope>): <description>\n"
            f"Allowed types: {', '.join(sorted(ALLOWED_TYPES))}\n"
            f"Example: feat(auth): add password reset"
        )
    }))
    sys.exit(2)

sys.exit(0)
