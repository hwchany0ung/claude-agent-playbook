# 에이전트 아키텍처

## 설계 원칙

### 1. 관심사의 분리
- 각 에이전트는 단 하나의 역할만 수행
- 오케스트레이터는 절대 직접 코딩하지 않음 — 반드시 하위 에이전트에 위임
- 구현 에이전트는 설계 문서에 없는 기능 자의적 추가 금지

### 2. 상호 교차 검증
- 모든 구현 완료 후 code-reviewer 또는 security-auditor 검증 필수
- 구현한 에이전트가 자기 코드를 스스로 최종 승인 금지
- 검증 없이 완료 선언 금지

### 3. 무한 루프 차단 — Unstuck 5-Step 확장 (2026-05-11)
- 수정-재검증 루프 최대 3회
- 3회 소진 후 → Unstuck 5-Step 1회 실행
- Unstuck에서도 새 방향 없음 → 사용자 판단 요청

**Unstuck 5-Step (Ouroboros 패턴 차용):**

| Mind | 질문 |
|------|------|
| Socratic | 지금 무엇을 가정하고 있는가? |
| Contrarian | 반대 접근이 맞다면 무엇이 틀린 것인가? |
| Simplifier | 기능을 절반으로 줄여도 가치가 있는가? |
| Researcher | 코드베이스 안에 선행 사례가 있는가? |
| Architect | 처음부터 다시 설계하면 어떻게 달라지는가? |

### 4. 파일 기반 컨텍스트 전달
- 에이전트 간 구두 요약 전달보다 파일 경로 직접 참조 우선
- 설계 문서(`docs/02-design/`), 계획 문서(`docs/01-plan/`) 직접 읽어 전달

---

## 에이전트 레이어

```
┌─────────────────────────────────────────────┐
│              Orchestrators                   │
│  manager-orchestrator | team-orchestrator    │
└──────────────────┬──────────────────────────┘
                   │ 위임
       ┌───────────┼───────────┐
       ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Impl    │ │    QA    │ │   Ops    │
│ Agents   │ │  Agents  │ │  Agents  │
└──────────┘ └──────────┘ └──────────┘
```

### Orchestrator Layer
| 에이전트 | 사용 조건 | 권한 |
|---------|----------|------|
| manager-orchestrator | specialist ≤2 | 작업 분배, 최종 승인 |
| team-orchestrator | specialist ≥3 | Team API 활용, 대규모 병렬 |

### Implementation Layer
| 에이전트 | 전문 영역 | 제한 |
|---------|----------|------|
| architect-designer | 프로젝트 구조, 설정 파일 | 코드 구현 금지 |
| frontend-specialist | React, Next.js, Vite, Tailwind | — |
| backend-specialist | Express, NestJS, FastAPI | — |
| flutter-developer | Flutter/Dart, Riverpod, GoRouter | — |
| supabase-specialist | DB, RLS, Edge Functions, SQL | — |
| figma-designer | Figma → Flutter/React 변환 | — |
| infra-specialist | Docker, CI/CD, Terraform, Cloud | 앱 코드 구현 금지 |
| api-designer | OpenAPI 스펙, Contract-first | 구현 금지 (핸드오프만) |

### QA Layer
| 에이전트 | 전문 영역 | 제한 |
|---------|----------|------|
| code-reviewer | 중복·성능·보안 리뷰 | 읽기 전용 |
| security-auditor | OWASP Top 10, 취약점 | 읽기 전용 |
| performance-analyst | 번들·Lighthouse·프로파일링 | 읽기 전용 |
| mobile-qa-tester | Flutter E2E, 위젯 테스트 | — |
| web-qa-tester | 브라우저 E2E | — |
| bug-fixer | 빌드·테스트 실패 수정 | — |
| qa-orchestrator | QA 자동화 파이프라인 | — |

### Ops Layer
| 에이전트 | 전문 영역 |
|---------|----------|
| docs-writer | README, API 문서, 마이그레이션 가이드 |
| telegram-notifier | 작업 완료 알림 |

---

## 병렬 실행 패턴

### 병렬 가능 조건
```
A 결과가 B 입력에 필요하지 않다 → 병렬 실행
A 완료 후 B 시작해야 한다     → 순차 실행
```

### 검증된 병렬 패턴

**코드 리뷰 삼분할:**
```
code-reviewer(BE)  ─┐
code-reviewer(FE)  ─┼─→ 결과 통합 → 중복 제거 → 수정
code-reviewer(FS)  ─┘
```

**구현 병렬:**
```
backend-specialist  ──→ API 구현     ─┐
frontend-specialist ──→ UI 구현      ─┼─→ 통합 테스트
                                      ─┘
선행 조건: OpenAPI 스펙 확정 필수
```

**QA 병렬:**
```
security-auditor    ──→ 보안 리포트   ─┐
performance-analyst ──→ 성능 리포트   ─┼─→ 최종 승인
gap-detector        ──→ Match Rate   ─┘
```

---

## 모델 할당 권장

### PAL Router 3-Tier (2026-05-11 업데이트)

고정 배정 대신 태스크 복잡도 기반으로 선택합니다.

| Tier | 모델 | 적합한 태스크 |
|------|------|-------------|
| **T1** Haiku | `claude-haiku-4-5` | 상태 업데이트, 문서 기록, 단순 조회 |
| **T2** Sonnet | `claude-sonnet-4-6` | 코드 구현, 코드 리뷰, API 설계 |
| **T3** Opus | `claude-opus-4-7` | 아키텍처 결정, gap 분석, Unstuck 판정 |

에이전트별 권장 Tier:

| 에이전트 | 권장 Tier |
|---------|----------|
| 오케스트레이터, security-auditor, gap-detector | T3 Opus |
| 구현 에이전트, code-reviewer, qa-strategist | T2 Sonnet |
| report-generator, qa-monitor, 상태 기록 | T1 Haiku |
