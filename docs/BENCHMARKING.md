# 시장 벤치마킹 분석

## 1. 시장 현황 (5 Forces 관점)

| Force | 강도 | 근거 |
|---|---|---|
| 신규 진입 | 매우 강 | Whisper+LLM이면 누구나 진입. Base44처럼 6개월 만에 서비스 가능 |
| 기존 경쟁 | 강 | Otter, Fireflies, Circleback, Granola, tl;dv 등 수십 개 |
| 공급자 교섭력 | 강 | 모델 회사(OpenAI, Anthropic, Google)에 의존 |
| 구매자 교섭력 | 강 | 전환 비용 낮고 무료 대안 풍부 |
| 대체재 | 중 | 수작업 회의록, 기본 메모앱 |

**시사점**: PC 조립 산업과 유사 구조. 중앙(회의록 AI)이 양쪽에서 압착 → **추적/팔로업**에서 차별화해야 생존.

## 2. 경쟁사 분석

### Circleback.ai (핵심 벤치마크)
- **포지셔닝**: "AI notetaker that actually works"
- **기능**: 자동 녹화, 100+언어, 액션 추출, 20+앱 연동, 맞춤 인사이트
- **가격**: Free $0 / Pro $15 / Business $25 / Enterprise $35 (사용자/월)
- **강점**: 세련된 UX, 넓은 연동, SOC2/HIPAA 보안
- **약점**: **등록 이후 추적 없음**. 이행 여부는 외부 도구에 위임
- **비고**: API/MCP/Webhook 제공 → 언젠가 추적 기능 추가 가능. "기능이 없다"는 것만으로 부족, **왜 구조적으로 다른 제품인지** 설명 필요

### Otter.ai
- 실시간 전사, AI 요약, Salesforce 연동. 액션 리스트는 보여주지만 추적 없음

### Granola.ai
- 메모+AI 요약 결합, 맥 네이티브. 개인 도구라 팀 추적 불가

### Fireflies.ai
- 자동 참여, AskFred(회의 Q&A), CRM 연동. 추적은 Asana/Trello에 위임

### 클로바노트 / Zoom AI / Notion AI
- 각 플랫폼 내장 기능으로 요약/액션 추출. 플랫폼 종속, 추적 기능 없음

## 3. 활용 가능 n8n 템플릿

| 템플릿 | 겹치는 부분 | 빠진 부분 |
|---|---|---|
| n8n #15114 | Whisper STT + Claude 추출 + Jira/ClickUp/Linear 등록, 중복 티켓 방지 | HITL, 추적 |
| n8n #10286 | 완성도 점수, Notion 액션 DB, Calendar 리마인더 | 정기 상태 조회, 안건 |
| n8n #13771 | 웹폼 녹음 업로드 + Gemini 요약 + Notion + Slack | 확인, 추적 |
| n8n #18705 | 전사문 → 액션 JSON → Notion 등록, 파싱 실패 시 수동 검토 | STT, 추적 |
| GitHub linear-issues-from-meet | Meet 전사문 → Linear 이슈, 관리자 이메일 승인 (우리 HITL과 유사) | 추적, 안건 |
| GitHub n8n-meeting-transcription-summary | Drive 녹음 → Whisper → GPT → Docs + 메일 | 등록, 추적 |

### 뒤쪽 절반에 쓸 수 있는 조각
- **지연 처리**: 매일 Notion에서 기한 지난 미완료 태스크 조회 → 기한 미루기/stale 표시
- **리마인드**: Notion 태스크 기한별 주간 리마인드
- **HITL**: n8n 내장 기능으로 Slack/Telegram/Gmail 승인/거절

## 4. 포지셔닝 맵

```
            추출 정교함
                ↑
    Circleback  │  Action Keeper
    (추출 강자)  │  (추출+추적)
────────────────┼────────────────→ 추적 깊이
    Otter       │  (미개척 영역)
    (기본 추출)  │
```

## 5. 발표 전략

> "추출·등록은 기존 템플릿 활용, 우리는 확인·추적·평가에 집중"

- 슬라이드에 "기존 사례" 한 줄 넣으면 오히려 설득력 상승
- STAGE 1~2에서 경쟁하지 말고, 기존 도구/템플릿 위에 올라타기
- 차별점은 "기능"이 아니라 "성공 지표가 다르다"로 프레이밍
  - Circleback 성공 지표: 회의록 품질, 절약 시간
  - Action Keeper 성공 지표: **기한 내 완료율**

## 6. 질의응답 대비

**Q: "Circleback이랑 뭐가 달라요?"**
→ "Circleback은 일을 등록할 때까지 책임지고, 우리는 일이 끝날 때까지 책임집니다."

**Q: "추출은 템플릿으로 이미 되는 것 아닌가?"**
→ "맞습니다. 그래서 우리도 추출은 검증된 템플릿을 활용합니다."
→ 차별점 3가지: HITL 확인 + 닫힌 루프 추적 + 측정 가능한 이행률

**Q: "왜 n8n인가?"**
→ Wait 노드(사람 응답 대기) + Schedule + Switch = "사람과 주고받는 워크플로"에 최적
→ 셀프호스팅 가능 = 조직 맞춤 = VRIO 관점 모방 비용 상승
