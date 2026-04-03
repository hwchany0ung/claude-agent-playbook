#!/usr/bin/env python3
"""
PreToolUse Hook — block direct localStorage usage for sensitive keys.

Customize ALLOWED_KEYS for your project's legitimate localStorage usage.

Setup in .claude/settings.json:
  "PreToolUse": [{ "matcher": "Write|Edit|MultiEdit", "hooks": [{ "type": "command", "command": "python3 /path/to/no-localstorage.py", "timeout": 10 }] }]
"""
import sys
import json
import re

# ── Customize: keys allowed in localStorage ───────────────────────────────────
# Add prefixes or exact keys your app legitimately stores in localStorage
# e.g., "theme" for dark mode, "sb-" for Supabase auth tokens
ALLOWED_PREFIXES = {"theme", "sb-"}  # localStorage.setItem with these keys is OK
# ──────────────────────────────────────────────────────────────────────────────

# Detect localStorage.setItem with keys NOT in the allowed list
SENSITIVE_PATTERN = re.compile(
    r"localStorage\.setItem\s*\(\s*['\"](?!"
    + "|".join(re.escape(p) for p in ALLOWED_PREFIXES)
    + r")[^'\"]*['\"]",
)

try:
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
except Exception:
    data = {}

tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

if tool_name not in ("Write", "Edit", "MultiEdit"):
    sys.exit(0)

# Only check JS/TS files
file_path = tool_input.get("file_path", "")
if not any(file_path.endswith(ext) for ext in (".js", ".jsx", ".ts", ".tsx")):
    sys.exit(0)

# Extract content to check
content = ""
if tool_name == "Write":
    content = tool_input.get("content", "")
elif tool_name == "Edit":
    content = tool_input.get("new_string", "")
elif tool_name == "MultiEdit":
    content = " ".join(e.get("new_string", "") for e in tool_input.get("edits", []))

violations = SENSITIVE_PATTERN.findall(content)

if violations:
    print(json.dumps({
        "continue": False,
        "reason": (
            f"[no-localstorage] Direct localStorage usage detected.\n"
            f"Matches: {violations[:3]}\n"
            f"Allowed prefixes: {sorted(ALLOWED_PREFIXES)}\n"
            "Store sensitive data in server-side sessions or memory state instead."
        )
    }))
    sys.exit(2)

sys.exit(0)
