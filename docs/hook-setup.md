# 훅 설정 가이드

## Claude Code 훅 이벤트

| 이벤트 | 발생 시점 | 용도 |
|--------|---------|------|
| `PreToolUse` | 도구 실행 직전 | 차단 또는 경고 |
| `PostToolUse` | 도구 실행 직후 | 로깅, 추적 |
| `Stop` | Claude 응답 완료 | 완료 검증, 알림 |
| `UserPromptSubmit` | 사용자 입력 직후 | 스킬 자동 감지 |

## 훅 입출력 형식

훅 스크립트는 **stdin으로 JSON을 받고**, **exit code로 동작을 제어**합니다.

```python
import sys, json

data = json.loads(sys.stdin.read())
tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})
```

### exit code 의미
- `0`: 정상 통과
- `2`: 도구 실행 차단 (PreToolUse에서만 유효)

### 차단 메시지 형식
```python
print(json.dumps({
    "continue": False,
    "reason": "차단 이유 메시지"
}))
sys.exit(2)
```

## settings.json 훅 등록

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/hooks/validate-commit.py",
            "timeout": 10,
            "statusMessage": "커밋 메시지 검증 중..."
          }
        ]
      },
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/hooks/no-localstorage.py",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "Agent",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/hooks/subagent-verify.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Agent",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/hooks/usage-tracker.py",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/hooks/task-qa-gate.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## 훅별 상세 설명

### validate-commit
커밋 메시지가 Conventional Commits 형식인지 검사합니다.

**허용 타입:** `feat` | `fix` | `chore` | `docs` | `refactor` | `test` | `style` | `perf` | `ci` | `revert`

```
feat(auth): 비밀번호 찾기 기능 추가       ✅
fix: 로그인 버그 수정                    ✅
test message                            ❌ 차단
```

### pre-push-qa
`git push` 실행 전 단위 테스트를 강제 실행합니다. 테스트 실패 시 push를 차단합니다.

**프로젝트에 맞게 수정이 필요한 부분:**
```python
# backend 테스트 명령
result = subprocess.run(["python", "-m", "pytest", "tests/unit/", ...], cwd="backend")

# frontend 테스트 명령
fe_result = subprocess.run(["npm", "test", "--", "--run", ...], cwd="frontend")
```

### no-localstorage
JavaScript/TypeScript 파일에서 민감한 키를 `localStorage`에 저장하는 코드를 차단합니다.

**허용 예외 키 수정:**
```python
ALLOWED_KEYS = {"consent_saved", "theme", "sb-"}  # 프로젝트에 맞게 수정
```

### subagent-verify
등록되지 않은 에이전트 타입 사용 시 경고를 출력합니다. 차단하지 않고 경고만 합니다.

`KNOWN_AGENTS` 집합을 프로젝트에 맞게 업데이트하세요.

### usage-tracker
`Agent` 도구 호출 시마다 에이전트 이름과 모델 구분(opus/sonnet)을 `.jsonl` 파일에 기록합니다.

**opus로 간주할 에이전트 목록 수정:**
```python
OPUS_AGENTS = {"cto-lead", "security-architect", "gap-detector"}  # 수정
```

**로그 저장 경로 수정:**
```python
log_path = os.path.join(PROJECT_ROOT, "logs", f"{date}.usage.jsonl")
```

### task-qa-gate
Claude 응답 완료(Stop) 시 PDCA 상태를 확인하여 검증 없이 완료 선언을 경고합니다.

bkit PDCA를 사용하지 않는다면 이 훅은 제거해도 됩니다.
