# 시작하기

## 사전 요구사항

- Claude Code CLI 설치
- Python 3.9+
- Git

## 설치 방법

### 1단계 — 레포 클론

```bash
git clone https://github.com/<your-username>/claude-agent-playbook.git
```

### 2단계 — 에이전트 설치

에이전트 파일을 프로젝트의 `.claude/agents/` 디렉토리에 복사합니다.

```bash
# 프로젝트 루트에서
mkdir -p .claude/agents
cp path/to/claude-agent-playbook/agents/*.md .claude/agents/
```

### 3단계 — 훅 설치

```bash
mkdir -p .claude/hooks
cp path/to/claude-agent-playbook/hooks/*.py .claude/hooks/
```

### 4단계 — 커맨드 설치

```bash
mkdir -p .claude/commands
cp path/to/claude-agent-playbook/commands/*.md .claude/commands/
```

### 5단계 — 스킬 설치 (local-skills 플러그인)

`~/.claude/plugins/local-skills/` 디렉토리가 없으면 먼저 생성합니다.

```bash
mkdir -p ~/.claude/plugins/local-skills/skills

# 각 스킬 복사
for skill_dir in path/to/claude-agent-playbook/skills/*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p ~/.claude/plugins/local-skills/skills/$skill_name
  cp "$skill_dir/SKILL.md" ~/.claude/plugins/local-skills/skills/$skill_name/
done
```

### 6단계 — settings.json 설정

`settings/project-settings.example.json`을 참고하여 `.claude/settings.json`을 작성합니다.

```bash
cp settings/project-settings.example.json .claude/settings.json
# 경로를 실제 프로젝트 경로로 수정
```

**Windows:**
```json
"command": "python \"C:\\path\\to\\your\\project\\.claude\\hooks\\validate-commit.py\""
```

**macOS/Linux:**
```json
"command": "python3 /path/to/your/project/.claude/hooks/validate-commit.py"
```

---

## 훅 활성화 확인

Claude Code에서 `git commit -m "test message"`를 실행하면 `validate-commit` 훅이 동작합니다.

```
커밋 메시지 검증 중...
[validate-commit] 커밋 메시지 형식 오류: 'test message'
허용 형식: <type>(<scope>): <description>
허용 type: ci, chore, docs, feat, fix, perf, refactor, revert, style, test
```

---

## 에이전트 사용 예시

### 소규모 작업 (specialist 2개)
```
"로그인 페이지 버그 수정해줘"
→ manager-orchestrator가 bug-fixer + code-reviewer 조율
```

### 대규모 작업 (specialist 3개+)
```
"새 API 엔드포인트 설계하고 BE/FE 구현해줘"
→ team-orchestrator가 api-designer + backend-specialist + frontend-specialist + code-reviewer 병렬 조율
```

### 스킬 사용
```
/qa-scenario-gen    # QA 시나리오 생성
/vulnerability-scanner  # 보안 스캔
/changelog-gen      # 릴리스 노트 생성
```

### 커맨드 사용
```
/scenario-test      # 시나리오 테스트 실행
/impl-validator     # 구현 검증
/cc-sync status     # 현재 구성 확인
```
