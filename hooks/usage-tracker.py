#!/usr/bin/env python3
"""
PostToolUse Hook — track Agent tool usage for cost monitoring.
Logs each agent call with model classification to a .jsonl file.

Setup in .claude/settings.json:
  "PostToolUse": [{ "matcher": "Agent", "hooks": [{ "type": "command", "command": "python3 /path/to/usage-tracker.py", "timeout": 5 }] }]
"""
import sys
import json
import os
from datetime import datetime

# ── Customize: agents that use the expensive model ────────────────────────────
EXPENSIVE_AGENTS = {"cto-lead", "security-architect", "gap-detector"}
EXPENSIVE_MODEL = "opus"
DEFAULT_MODEL = "sonnet"

# Log directory (relative to project root or absolute)
LOG_DIR = os.environ.get("USAGE_LOG_DIR", ".logs/agent-usage")
# ──────────────────────────────────────────────────────────────────────────────

try:
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
except Exception:
    sys.exit(0)

if data.get("tool_name") != "Agent":
    sys.exit(0)

tool_input = data.get("tool_input", {})
subagent_type = tool_input.get("subagent_type", "") if isinstance(tool_input, dict) else ""

entry = {
    "ts": datetime.now().isoformat(),
    "agent": subagent_type,
    "model": EXPENSIVE_MODEL if subagent_type in EXPENSIVE_AGENTS else DEFAULT_MODEL,
    "is_expensive": subagent_type in EXPENSIVE_AGENTS,
}

log_path = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.jsonl")

try:
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
except Exception:
    pass  # Never block on logging failure

sys.exit(0)
