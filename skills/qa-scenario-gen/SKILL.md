---
name: qa-scenario-gen
description: Generate QA scenarios (Phase 2.5) from design documents. Creates .qa-evidence.json with Happy Path, Edge Case, and Failure Case scenarios before implementation begins.
origin: local
---

# QA Scenario Generator

Generates contract-first QA scenarios from design documents before implementation (Do phase).

## When to Activate
- After Design phase, before implementation starts
- When "QA scenarios", "qa-evidence", or "Phase 2.5" is mentioned
- After new API endpoint design is complete

## Process

### Step 1 — Analyze Design Documents
```
docs/02-design/<feature>/
- Extract API endpoint list
- Identify data models and constraints
- Note auth/permission requirements
```

### Step 2 — Scenario Structure (3 tracks per feature)

| Track | Description |
|-------|-------------|
| Happy Path | Normal flow with valid authenticated request |
| Edge Case | Boundary values, empty strings, concurrent requests |
| Failure Case | Unauthenticated, forbidden, invalid format, server error |

### Step 3 — Generate .qa-evidence.json

Save to: `docs/archive/YYYY-MM/<feature-name>/.qa-evidence.json`

```json
{
  "feature": "<feature-name>",
  "version": "1.0",
  "created": "YYYY-MM-DD",
  "scenarios": [
    {
      "id": "SC-01",
      "name": "Successful request",
      "track": "happy_path",
      "endpoint": "POST /api/resource",
      "preconditions": ["authenticated user", "valid payload"],
      "steps": ["send request", "verify response"],
      "expected": { "status": 200, "body_contains": ["id", "created_at"] },
      "acceptance_criteria": "Response time < 2s, data persisted"
    },
    {
      "id": "SC-02",
      "name": "Unauthenticated request rejected",
      "track": "failure_case",
      "endpoint": "POST /api/resource",
      "preconditions": ["no auth token"],
      "expected": { "status": 401 }
    }
  ],
  "coverage": {
    "endpoints": [],
    "auth_flows": [],
    "error_codes": []
  }
}
```

### Step 4 — User Approval
Present scenarios and wait for approval before implementation begins.
