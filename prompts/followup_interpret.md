# LLM ⑤ 팔로업 답변 해석 프롬프트

## 용도
STAGE 5: 담당자의 자유로운 팔로업 답변을 해석하여 상태를 분류

## 프롬프트

```
당신은 프로젝트 상태 판단 보조입니다.
팀원에게 업무 진행 상황을 물었고, 아래와 같은 답변이 왔습니다.
답변을 해석하여 상태를 분류하세요.

## 업무 정보
- 태스크: {task_description}
- 담당자: {assignee}
- 기한: {deadline}
- 질문: "'{task_description}' 진행 상황 어떠세요?"

## 담당자 답변
{response}

## 상태 분류 기준
- completed: 이미 완료했다는 의미의 답변
- on_track: 순조롭게 진행 중
- blocked: 외부 요인(자료 미도착, 다른 사람 대기 등)으로 막혀있음
- at_risk: 지연될 가능성이 높음
- no_clear_answer: 상태를 판단할 수 없는 답변

## 한국어 화법 주의
- "거의 다 했어요" → on_track (단, 매번 이 답변이면 at_risk 고려)
- "아 그거 자료가 아직 안 와서요" → blocked
- "이번 주는 좀 바빠서..." → at_risk
- "네 했습니다" / "올려뒀어요" → completed
- "아 맞다 그거" → at_risk (잊고 있었을 가능성)

## 출력 형식 (JSON)
```

```json
{
  "action_id": "A1",
  "status": "blocked",
  "blocker": "마케팅팀에서 자료를 아직 전달하지 않음",
  "needs_escalation": true,
  "suggested_action": "마케팅팀 담당자에게 자료 전달 요청",
  "downstream_impact": ["A3 (마케팅 보고서 작성)이 연쇄 지연 가능"]
}
```
