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

## PAL Router — 모델 배정

태스크 복잡도에 따라 모델을 선택합니다. 역할별 고정 배정보다 비용 효율적입니다.

| Tier | 모델 | 적합한 태스크 |
|------|------|-------------|
| T1 Haiku | `claude-haiku-4-5` | 상태 업데이트, 문서 기록, 단순 조회, 보고서 생성 |
| T2 Sonnet | `claude-sonnet-4-6` | 코드 구현, 코드 리뷰, API 설계, 일반 분석 |
| T3 Opus | `claude-opus-4-7` | 아키텍처 결정, gap 분석, Unstuck 판정, 보안 심층 감사 |



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

## Ouroboros 통합 패턴

[Ouroboros](https://github.com/Q00/ouroboros) Agent OS에서 채택한 7개 워크플로우 패턴.
외부 CLI 설치 없이 CLAUDE.md 파일만으로 동작합니다.

| # | 패턴 | 설명 | 적용 위치 |
|---|------|------|----------|
| 1 | **Ambiguity Score** | 모호성 수치화 게이트 — Ambiguity ≤ 0.2 이어야 코딩 진행 | `/pdca plan` 전 |
| 2 | **Locked Seed** | 핵심 결정 LOCKED 마커 표기, 변경 시 사용자 확인 필수 | Context Anchor |
| 3 | **Contrarian Check** | 구현 핵심 가정을 역으로 검증 (반대가 맞다면?) | QA 체크리스트 |
| 4 | **Stagnation Detection** | iterate 간 출력 비교, 변화 없으면 retry 차감 없이 Unstuck | iterate 2회차+ |
| 5 | **Unstuck 5-Step** | retry 3회 후 5가지 Mind 관점으로 회복 시도 | 루프 차단 확장 |
| 6 | **Wonder/Reflect** | 실패에서 가설 발산 → 최적 가설 수렴 선택 | `/pdca iterate` |
| 7 | **PAL Router** | 태스크 복잡도 기반 Haiku/Sonnet/Opus 3-tier 선택 | 모든 세션 |

### Unstuck 5-Step 상세

`retry 1 → retry 2 → retry 3 → [Unstuck] → 사용자 판단 요청`

| Mind | 질문 |
|------|------|
| Socratic | 지금 무엇을 가정하고 있는가? |
| Contrarian | 반대 접근이 맞다면 무엇이 틀린 것인가? |
| Simplifier | 기능을 절반으로 줄여도 가치가 있는가? |
| Researcher | 코드베이스 안에 선행 사례가 있는가? |
| Architect | 처음부터 다시 설계하면 어떻게 달라지는가? |

→ 1개 이상 새 방향 발견 → retry 1회 추가 (총 4회)
→ 새 방향 없음 → 사용자 판단 요청

## 레퍼런스

- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [Subagents Guide](https://docs.anthropic.com/claude-code/sub-agents)
- [Hooks Guide](https://docs.anthropic.com/claude-code/hooks)

## 라이선스

MIT
