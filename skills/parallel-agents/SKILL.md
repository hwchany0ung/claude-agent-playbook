---
name: parallel-agents
description: Guide for running multiple Claude Code agents concurrently. Identifies parallelizable tasks, manages dependencies, and integrates results. Based on real multi-agent workflows.
origin: local
---

# Parallel Agents Execution

Run independent tasks concurrently across multiple agents to reduce wall-clock time.

## When to Activate
- 3+ independent tasks exist simultaneously
- "parallel", "concurrent", "simultaneously" requested
- Orchestrator planning work distribution

## Parallelization Decision

```
Is A's output needed as B's input?
  YES → Sequential (A then B)
  NO  → Parallel (A and B simultaneously)
```

## Validated Parallel Patterns

### Code Review Split (3-way)
```
code-reviewer(backend)   ─┐
code-reviewer(frontend)  ─┼─→ merge results → deduplicate → fix
code-reviewer(fullstack) ─┘
```
**Note:** Expect 5-10% false positives. Filter known false positives before fixing.

### Implementation Split (BE + FE)
```
backend-specialist  ──→ API implementation     ─┐
frontend-specialist ──→ UI implementation      ─┼─→ integration test
                                                ─┘
Prerequisite: OpenAPI spec must be finalized before starting both.
```

### QA Parallel
```
security-auditor    ──→ Security report    ─┐
performance-analyst ──→ Performance report ─┼─→ orchestrator final approval
gap-detector        ──→ Match Rate         ─┘
```

## How to Launch (Claude Code)

In a single message, invoke multiple Agent tool calls:

```
Agent(subagent_type="code-reviewer", prompt="Review backend/app/api/...")
Agent(subagent_type="code-reviewer", prompt="Review frontend/src/...")
Agent(subagent_type="security-auditor", prompt="Scan for OWASP issues...")
# All three start simultaneously
# Wait for all results before proceeding
```

## Result Integration

1. **Deduplicate:** Same file:line reported by multiple agents → keep once
2. **Escalate:** File reported by 2+ agents → increase severity
3. **Filter false positives:** Maintain a known-false-positive list
4. **Prioritize:** Critical → Important → Minor → Skip

## Anti-patterns

| Anti-pattern | Why bad |
|--------------|---------|
| Parallel when results depend on each other | Race condition, wrong results |
| Too many agents (5+) | Context overhead, harder to integrate |
| Each agent modifying same files | Merge conflicts |

## Orchestrator Selection

| Condition | Orchestrator |
|-----------|-------------|
| specialist ≤ 2 | manager-orchestrator (lightweight) |
| specialist ≥ 3 | team-orchestrator (Team API) |
