---
name: changelog-gen
description: Generate release notes from git commit history. Classify commits by type, convert to user-friendly language, and update CHANGELOG.md.
origin: local
---

# Changelog Generator

Analyze git history and produce structured release notes.

## When to Activate
- "changelog", "release notes", "변경 이력" requested
- After production deployment
- End of sprint documentation

## Process

### Step 1 — Collect Commits
```bash
# Since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline --no-merges

# Since date
git log --since="2026-04-01" --oneline --no-merges --format="%H %s"

# Since specific commit
git log <commit-sha>..HEAD --oneline --no-merges
```

### Step 2 — Classify by Prefix

| Prefix | Category | User-facing label |
|--------|----------|-------------------|
| feat | New Features | Added |
| fix | Bug Fixes | Fixed |
| perf | Performance | Improved |
| security | Security | Security |
| chore/ci | Internal | (omit or "Internal improvements") |
| docs | Documentation | (omit from user changelog) |

### Step 3 — CHANGELOG.md Format

```markdown
## [Unreleased] — YYYY-MM-DD

### New Features
- AI Q&A dynamic followup buttons (context-aware suggestions)
- Q&A feedback (thumbs up/down) and admin analytics

### Bug Fixes
- Fixed AI Q&A permission error caused by missing status column
- Fixed SSE streaming field mismatch (delta→chunk, done→[DONE])

### Performance & Stability
- Admin API parallelized with asyncio.gather (eliminated N+1)
- QA event aggregation moved to server-side

### Internal
- CI: 4-job structure (unit/integration/frontend/e2e), 80% coverage enforced
- Rate limiting applied to all admin and roadmap endpoints
```

### Step 4 — User-Friendly Translation
Convert technical terms:
- "SSE streaming" → "real-time responses"
- "JWT validation" → "secure authentication"
- "rate limit" → "overload protection"
- "N+1 query" → "performance optimization"

## Output
- Updated `CHANGELOG.md` (prepend new section)
- Optional: separate `RELEASE_NOTES.md` for non-technical stakeholders
