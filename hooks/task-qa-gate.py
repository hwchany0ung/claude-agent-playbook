#!/usr/bin/env python3
"""
Stop Hook — warn when implementation phase ends without QA verification.
Reads bkit PDCA state to detect Do-phase completion without gap-detector.

Remove or adapt if not using bkit PDCA.

Setup in .claude/settings.json:
  "Stop": [{ "hooks": [{ "type": "command", "command": "python3 /path/to/task-qa-gate.py", "timeout": 10 }] }]
"""
import sys
import json
import os

try:
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
except Exception:
    data = {}

stop_reason = data.get("stop_reason", "end_turn")

# Only check on normal completion
if stop_reason != "end_turn":
    sys.exit(0)

# ── Customize: path to your PDCA state file ───────────────────────────────────
# bkit stores PDCA state here by default
PDCA_STATE_PATH = os.environ.get(
    "PDCA_STATE_PATH",
    os.path.join(os.getcwd(), ".bkit", "state", "pdca-status.json")
)
# ──────────────────────────────────────────────────────────────────────────────

try:
    with open(PDCA_STATE_PATH, "r", encoding="utf-8") as f:
        pdca = json.load(f)
except Exception:
    sys.exit(0)  # No PDCA state — skip

features = pdca.get("features", {})
for feature_name, feature_data in features.items():
    if feature_data.get("phase") == "do" and not feature_data.get("analyzed", False):
        print(
            f"[task-qa-gate] WARNING: '{feature_name}' is in Do phase.\n"
            f"  Do not declare completion without gap-detector verification.\n"
            f"  Run '/pdca analyze' or gap-detector agent first.",
            file=sys.stderr
        )

sys.exit(0)
