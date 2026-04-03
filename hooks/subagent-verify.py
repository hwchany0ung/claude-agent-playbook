#!/usr/bin/env python3
"""
PreToolUse Hook — warn when an unknown agent type is used.
Does NOT block — warning only.

Setup in .claude/settings.json:
  "PreToolUse": [{ "matcher": "Agent", "hooks": [{ "type": "command", "command": "python3 /path/to/subagent-verify.py", "timeout": 5 }] }]
"""
import sys
import json

# ── Customize: your registered agents ─────────────────────────────────────────
KNOWN_AGENTS = {
    # Orchestrators
    "manager-orchestrator", "team-orchestrator",
    # Implementation
    "architect-designer", "frontend-specialist", "backend-specialist",
    "flutter-developer", "supabase-specialist", "figma-designer",
    "infra-specialist", "api-designer",
    # QA
    "code-reviewer", "bug-fixer", "web-qa-tester", "qa-orchestrator",
    "security-auditor", "mobile-qa-tester", "performance-analyst",
    # Ops
    "telegram-notifier", "docs-writer",
    # Claude Code built-ins
    "Explore", "Plan", "general-purpose",
    # bkit built-ins (remove if not using bkit)
    "frontend-architect", "enterprise-expert", "infra-architect",
    "product-manager", "qa-strategist", "gap-detector", "code-analyzer",
    "security-architect", "pm-lead", "pdca-iterator", "report-generator",
}
# ──────────────────────────────────────────────────────────────────────────────

try:
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
except Exception:
    sys.exit(0)

if data.get("tool_name") != "Agent":
    sys.exit(0)

tool_input = data.get("tool_input", {})
subagent_type = tool_input.get("subagent_type", "") if isinstance(tool_input, dict) else ""

if subagent_type and subagent_type not in KNOWN_AGENTS:
    print(
        f"[subagent-verify] WARNING: Unknown agent type '{subagent_type}'\n"
        f"  Registered agents: {sorted(KNOWN_AGENTS)}\n"
        f"  Verify this is intentional.",
        file=sys.stderr
    )

# Warning only — do not block
sys.exit(0)
