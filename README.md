# Claude Agent Playbook

Claude Code 멀티에이전트 시스템 구성 가이드. 실제 프로덕션 프로젝트에서 검증된 에이전트·훅·스킬·커맨드 모음.

## 구성 개요

```
claude-agent-playbook/
├── agents/      # Claude Code 서브에이전트 정의 (.claude/agents/)
├── hooks/       # 자동 실행 훅 스크립트 (.claude/hooks/)
├── skills/      # 로컬 스킬 정의 (local-skills 플러그인)
├── commands/    # 슬래시 커맨드 (.claude/commands/)
├── settings/    # settings.json 예시 (시크릿 제외)
└── docs/        # 아키텍처·워크플로우 가이드
```

## 에이전트 구조 (7인 + 확장)

```
Orchestrators ──── manager-orchestrator  (소규모, specialist ≤2)
                   team-orchestrator     (대규모, Team API)

Implementation ─── architect-designer    (구조 설계)
                   frontend-specialist   (React/Vite/Tailwind)
                   backend-specialist    (FastAPI/Express)
                   flutter-developer     (Flutter/Riverpod)
                   supabase-specialist   (DB/RLS)
                   infra-specialist      (CI/CD/Terraform/AWS)
                   api-designer          (OpenAPI/Contract-first)

QA ────────────── code-reviewer          (품질·성능·보안)
                   security-auditor      (OWASP Top 10, 읽기전용)
                   performance-analyst   (번들·Lighthouse, 읽기전용)
                   mobile-qa-tester      (Flutter E2E)
                   web-qa-tester         (브라우저 E2E)
                   bug-fixer             (빌드/테스트 실패 수정)

Ops ───────────── docs-writer            (README·API 문서)
                   telegram-notifier     (작업 완료 알림)
```

## 오케스트레이터 선택 규칙

| 조건 | 선택 |
|------|------|
| specialist **2개 이하** | manager-orchestrator 단독 |
| specialist **3개 이상** | team-orchestrator + 팀 풀 |

## 필수 검증 워크플로우 (코딩·디버깅)

```
구현 완료
    ↓
[1차] code-reviewer / security-auditor
    ↓ 통과
[2차] 오케스트레이터 최종 승인
    ↓
완료 (루프 최대 3회)
```

## 훅 동작

| 훅 | 이벤트 | 역할 |
|----|--------|------|
| validate-commit | PreToolUse(Bash) | 커밋 메시지 컨벤션 강제 |
| pre-push-qa | PreToolUse(Bash) | push 전 테스트 통과 강제 |
| no-localstorage | PreToolUse(Write/Edit) | 민감 데이터 localStorage 차단 |
| subagent-verify | PreToolUse(Agent) | 미등록 에이전트 경고 |
| usage-tracker | PostToolUse(Agent) | opus/sonnet 사용량 기록 |
| task-qa-gate | Stop | QA 미검증 완료 선언 경고 |

## 스킬 목록

| 스킬 | 용도 |
|------|------|
| qa-scenario-gen | Phase 2.5 .qa-evidence.json 자동 생성 |
| vulnerability-scanner | OWASP 자동 코드 스캔 |
| prompt-engineering | Claude API 프롬프트 최적화 |
| reducing-entropy | 코드 복잡도 점진적 감소 |
| changelog-gen | git log 기반 릴리스 노트 생성 |
| parallel-agents | 병렬 에이전트 실행 패턴 가이드 |

## 커맨드

| 커맨드 | 기능 |
|--------|------|
| `/scenario-test` | .qa-evidence.json 시나리오 실행 |
| `/impl-validator` | 설계-구현 빠른 검증 |
| `/cc-sync` | 에이전트·훅·설정 백업/복원 |

## 설치

```bash
# 1. 에이전트 복사
cp agents/*.md <project>/.claude/agents/

# 2. 훅 복사
cp hooks/*.py <project>/.claude/hooks/

# 3. 커맨드 복사
cp commands/*.md <project>/.claude/commands/

# 4. 스킬 설치 (local-skills 플러그인 경로)
mkdir -p ~/.claude/plugins/local-skills/skills
for skill in skills/*/; do
  cp -r "$skill" ~/.claude/plugins/local-skills/skills/
done

# 5. settings.json 적용
# settings/project-settings.example.json 참고하여 .claude/settings.json 작성
```

## 레퍼런스

- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Subagents Guide](https://docs.anthropic.com/claude-code/sub-agents)
- [Hooks Guide](https://docs.anthropic.com/claude-code/hooks)

## 라이선스

MIT
