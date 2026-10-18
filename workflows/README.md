# n8n Workflows

## 워크플로 구성 (5개 서브 워크플로)

| 파일 | 단계 | 트리거 | 핵심 노드 | 상태 |
|---|---|---|---|---|
| 01_transcribe.json | STAGE 1 기록 | Google Drive Trigger | HTTP Request (STT API) | 예정 |
| 02_extract.json | STAGE 2 추출 | Execute Workflow (01에서 호출) | AI Agent / LLM 노드 | 예정 |
| 03_rnr_timeline.json | STAGE 3 R&R+타임라인 | Execute Workflow (02에서 호출) | LLM + Wait (HITL) + Notion | 예정 |
| 04_followup.json | STAGE 4 추적 | Schedule Trigger (매일 09:00) | Notion 조회 + Slack DM + LLM + Switch | 예정 |
| 05_next_agenda.json | STAGE 5 순환 | Schedule Trigger (매주 금 17:00) | Notion 조회 + LLM + Slack | 예정 |

## n8n 핵심 노드 매핑

| 단계 | n8n 노드 | 비고 |
|---|---|---|
| 트리거 | Google Drive Trigger | 새 녹음 파일 감지 |
| STT | HTTP Request → STT API | 한국어 정확도+화자 구분으로 선택 |
| 추출/R&R/타임라인 | AI Agent / OpenAI / Anthropic | JSON 스키마 강제로 구조화 출력 |
| 승인 | Slack + **Wait** (webhook 재개) | 사람이 버튼 누를 때까지 대기 |
| 등록 | Notion 노드 | DB에 태스크+관계형 필드 생성 |
| 추적 | Schedule Trigger + IF/Switch | 매일 기한 임박 태스크 조회 |
| 답변 해석 | Slack Trigger → LLM → Switch | 상태별 흐름 분기 |
| 안건 | Schedule Trigger → LLM → Notion/Slack | 회의 전날 발송 |

## 참고 템플릿

| 템플릿 | 활용 부분 | 우리가 추가할 부분 |
|---|---|---|
| n8n #13771 | 웹폼 녹음 → AI 요약 → Notion → Slack | HITL, 추적 루프 |
| n8n #18705 | 전사문 → 액션 JSON → Notion 등록 | 원문 근거, 미정 처리, 확신도 |
| n8n #15114 | Whisper → Claude → Jira 생성 | HITL, 상태 추적 |
| n8n #10286 | 완성도 점수 + Calendar 리마인더 | 지연 에스컬레이션, 안건 생성 |

## 필요 Credentials

- STT API (비교 테스트 후 선정)
- Anthropic API Key (Claude) 또는 OpenAI API Key
- Notion Integration Token
- Slack Bot Token
- Google Drive OAuth (녹음 업로드 트리거)

## 협업 규칙

1. **원본은 n8n**: n8n 화면에서 편집 → 내보내서 이 폴더에 커밋
2. **워크플로 쪼개기**: 5개 서브 워크플로를 Execute Workflow로 연결. 담당자 1명/워크플로
3. **비밀값 금지**: API 키는 n8n Credentials에만 저장. JSON에 직접 넣지 말 것
