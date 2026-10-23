#!/usr/bin/env python3
"""FollowIt (팔로잇) 중간발표 PPT v3 — v1 구조 기반 + 성공기준 표 교체

v3 방침 (발표자 피드백: v1이 더 직관적):
- 슬라이드 구조·문구는 v1 기준 (5단계: 기록/추출/배정+확인/추적/순환)
- v2에서 유지하는 것: FollowIt 네이밍(팀 확정), 회의 연결(S3 비교표 + S1 기록 카드에 태그 방식으로),
  수직 슬라이스 수행 계획(팀 피드백 반영분), 54% 출처 각주
- 성공 기준(S5): 팀 논의 결과 이미지 기반 표로 전면 교체
  (관리시간 50% 감소 / 추출 품질 정확도 90%·누락률 10% / 기한 내 이행률 전후 비교)
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── 팔레트 (v1 기준: 그린=브랜드, 코랄=페인) ──
BG = RGBColor(0x0F, 0x0F, 0x0F)
SURFACE = RGBColor(0x1A, 0x1A, 0x1A)
SURFACE2 = RGBColor(0x22, 0x22, 0x22)
BORDER = RGBColor(0x2A, 0x2A, 0x2A)
WHITE = RGBColor(0xF5, 0xF5, 0xF5)
GRAY1 = RGBColor(0x99, 0x99, 0x99)
GRAY2 = RGBColor(0x66, 0x66, 0x66)
BRAND = RGBColor(0x4A, 0xDE, 0x80)
PAIN = RGBColor(0xFF, 0x6B, 0x4A)
TEAL = RGBColor(0x4E, 0xCD, 0xC4)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H

# ── 헬퍼 ──

def bg(slide):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = BG

def txt(slide, l, t, w, h, text, sz=18, clr=WHITE, bold=False, align=PP_ALIGN.LEFT, name="Arial"):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(sz)
    p.font.color.rgb = clr
    p.font.bold = bold
    p.font.name = name
    p.alignment = align
    return box

def mtxt(slide, l, t, w, h, lines, sz=16, clr=WHITE, spacing=1.4):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(lines):
        text, ov = (item, {}) if isinstance(item, str) else (item[0], item[1] if len(item) > 1 else {})
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.font.size = Pt(ov.get("sz", sz))
        p.font.color.rgb = ov.get("clr", clr)
        p.font.bold = ov.get("bold", False)
        p.font.name = ov.get("name", "Arial")
        p.alignment = ov.get("align", PP_ALIGN.LEFT)
        p.space_after = Pt(sz * (spacing - 1) + 2)
    return box

def card(slide, l, t, w, h, fill_clr=SURFACE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_clr
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape

def divider(slide, l, t, w, clr=BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, Pt(1))
    shape.fill.solid()
    shape.fill.fore_color.rgb = clr
    shape.line.fill.background()
    shape.shadow.inherit = False

def pill(slide, l, t, text, clr=PAIN):
    w = Pt(len(text) * 14 + 30)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, Pt(28))
    shape.fill.solid()
    shape.fill.fore_color.rgb = clr
    shape.line.fill.background()
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.word_wrap = False
    tf.margin_left = Pt(10)
    tf.margin_right = Pt(10)
    tf.margin_top = Pt(2)
    tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(11)
    p.font.color.rgb = BG
    p.font.bold = True
    p.font.name = "Arial"
    p.alignment = PP_ALIGN.CENTER
    return shape

def page_num(slide, n):
    txt(slide, Inches(12.5), Inches(7.05), Inches(0.6), Inches(0.3),
        str(n), sz=10, clr=GRAY2, align=PP_ALIGN.RIGHT)


# ════════════════════════════════════════════
# S1. 표지 (v1 기준 + FollowIt)
# ════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)

txt(s, Inches(1), Inches(1.6), Inches(6), Inches(0.4),
    "KAIST IMMS  ·  2026 Fall  ·  AI Business Strategy", sz=13, clr=GRAY2)

txt(s, Inches(1), Inches(2.3), Inches(10), Inches(1.2),
    "회의 이후를\n책임지는 AI", sz=54, clr=WHITE, bold=True)

txt(s, Inches(1), Inches(4.5), Inches(8), Inches(0.5),
    "FollowIt  ·  팔로잇", sz=24, clr=BRAND, bold=True)

divider(s, Inches(1), Inches(5.3), Inches(3))

txt(s, Inches(1), Inches(5.6), Inches(10.5), Inches(0.6),
    "녹음된 회의에서 할 일 · 담당자 · 일정을 추출하고,\n일이 끝날 때까지 쫓아다니는 AI 워크플로", sz=16, clr=GRAY1)

txt(s, Inches(1), Inches(6.6), Inches(10), Inches(0.3),
    "TEAM_2 : 김신애 · 박승찬 · 신지엽 · 윤경혜", sz=13, clr=GRAY2)

page_num(s, 1)


# ════════════════════════════════════════════
# S2. 문제 ① — 핵심 페인 (v1 기준)
# ════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
pill(s, Inches(1), Inches(0.7), "문제")

txt(s, Inches(1), Inches(1.3), Inches(11), Inches(1.0),
    "회의는 끝났는데, 일은 시작되지 않는다", sz=40, clr=WHITE, bold=True)

card(s, Inches(1), Inches(2.8), Inches(4.5), Inches(2.4), SURFACE)
txt(s, Inches(1.5), Inches(3.0), Inches(3.5), Inches(1.2),
    "54%", sz=72, clr=PAIN, bold=True)
txt(s, Inches(1.5), Inches(4.3), Inches(3.6), Inches(0.8),
    "회의 후 다음 할 일·담당자를 모른 채\n자리를 뜨는 직장인 비율¹", sz=14, clr=GRAY1)

causes = [
    ("①", '주인 불명확 — "그거 누가 하기로 했죠?"'),
    ("②", '기한 모호 — "다음 주쯤", "가능한 빨리"'),
    ("③", "팔로업 부재 — 다음 회의에서 확인 없이 넘어감"),
]
for i, (num, label) in enumerate(causes):
    y = Inches(2.8) + Inches(0.85) * i
    card(s, Inches(6.2), y, Inches(6.1), Inches(0.65), SURFACE)
    txt(s, Inches(6.6), y + Inches(0.05), Inches(0.8), Inches(0.5),
        num, sz=18, clr=PAIN, bold=True)
    txt(s, Inches(7.2), y + Inches(0.05), Inches(5), Inches(0.5),
        label, sz=15, clr=WHITE)

divider(s, Inches(1), Inches(5.8), Inches(11.3))
txt(s, Inches(1), Inches(6.05), Inches(11), Inches(0.6),
    "PM이 회의록 정리 → 태스크 등록 → 진행 확인을 수작업으로 하고 있습니다.\n이 일이 누락되는 순간, 결정사항은 사라집니다.",
    sz=15, clr=GRAY1)

txt(s, Inches(1), Inches(6.85), Inches(8), Inches(0.3),
    "1. Source: Atlassian, 지식근로자 5,000명 대상 설문 (2024)", sz=10, clr=GRAY2)

page_num(s, 2)


# ════════════════════════════════════════════
# S3. 문제 ② — 기존 서비스의 한계 (v1 기준 + 회의 연결 행)
# ════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
pill(s, Inches(1), Inches(0.7), "문제")

txt(s, Inches(1), Inches(1.3), Inches(11), Inches(0.8),
    "기존 회의 AI는 '등록'에서 멈춘다", sz=40, clr=WHITE, bold=True)

card(s, Inches(1), Inches(2.5), Inches(5.5), Inches(3.4), SURFACE)
txt(s, Inches(1.4), Inches(2.65), Inches(4.5), Inches(0.4),
    "Circleback · Otter · 클로바노트 등", sz=14, clr=PAIN)
divider(s, Inches(1.4), Inches(3.2), Inches(4.7), GRAY2)

steps_existing = [
    ("녹음 → 전사", "✅"),
    ("AI 요약", "✅"),
    ("액션아이템 추출", "✅"),
    ("태스크 등록", "✅"),
    ("─── 여기서 끝 ───", ""),
]
y_pos = Inches(3.42)
for label, check in steps_existing:
    if check:
        txt(s, Inches(1.5), y_pos, Inches(3.5), Inches(0.35), label, sz=14, clr=WHITE)
        txt(s, Inches(5.2), y_pos, Inches(0.8), Inches(0.35), check, sz=14, clr=BRAND)
    else:
        txt(s, Inches(1.5), y_pos, Inches(4), Inches(0.35), label, sz=13, clr=GRAY2, align=PP_ALIGN.CENTER)
    y_pos += Inches(0.42)

card(s, Inches(6.8), Inches(2.5), Inches(5.5), Inches(3.4), SURFACE2)
txt(s, Inches(7.2), Inches(2.65), Inches(4.5), Inches(0.4),
    "FollowIt (팔로잇)", sz=14, clr=BRAND, bold=True)
divider(s, Inches(7.2), Inches(3.2), Inches(4.7), BRAND)

steps_ours = [
    ("녹음 → 전사 → 추출 → 등록", "기존 활용"),
    ("회의 연결 · 맥락 관리", "NEW"),
    ("R&R 추천 + 타임라인 역산", "NEW"),
    ("Human In The Loop 확인", "NEW"),
    ("팔로업 추적 + 답변 해석", "NEW"),
    ("미완료 → 다음 회의 안건", "NEW"),
]
y_pos = Inches(3.38)
for label, tag in steps_ours:
    txt(s, Inches(7.3), y_pos, Inches(3.9), Inches(0.35), label, sz=13.5, clr=WHITE)
    tag_clr = GRAY1 if tag == "기존 활용" else BRAND
    txt(s, Inches(11.15), y_pos, Inches(1.0), Inches(0.35), tag, sz=11, clr=tag_clr, bold=(tag == "NEW"))
    y_pos += Inches(0.41)

txt(s, Inches(1), Inches(6.2), Inches(11.5), Inches(0.5),
    '“기존 도구는 회의를 기록합니다.  우리는 회의를 완결합니다.”',
    sz=20, clr=BRAND, bold=True)

txt(s, Inches(1), Inches(6.7), Inches(11.5), Inches(0.3),
    "추출·등록은 검증된 템플릿을 활용하고, 확인 · 추적 · 완결에 집중합니다.",
    sz=13, clr=GRAY1)

page_num(s, 3)


# ════════════════════════════════════════════
# S4. 솔루션 — 5단계 워크플로 (v1 기준 + 회의 연결 태그)
# ════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
pill(s, Inches(1), Inches(0.7), "솔루션", TEAL)

txt(s, Inches(1), Inches(1.3), Inches(11), Inches(0.8),
    "녹음부터 다음 회의까지, 끊기지 않는 고리", sz=40, clr=WHITE, bold=True)

stage_data = [
    ("1", "기록", "녹음 → STT 전사\n화자 구분\n이전 회의 태그 연결"),
    ("2", "추출", "LLM 분석\n액션·담당자·기한"),
    ("3", "배정+확인", "R&R 추천\nHITL 승인"),
    ("4", "추적", "D-2 팔로업\n답변 해석"),
    ("5", "순환", "미완료 → 안건\n다음 회의 연결"),
]

cw = Inches(2.05)
gap = Inches(0.28)
sx = Inches(0.8)

for i, (num, title, body) in enumerate(stage_data):
    x = sx + (cw + gap) * i
    card(s, x, Inches(2.5), cw, Inches(2.0), SURFACE)
    txt(s, x + Pt(14), Inches(2.6), Inches(0.5), Inches(0.4),
        num, sz=28, clr=BRAND, bold=True)
    txt(s, x + Pt(14), Inches(3.1), cw - Pt(28), Inches(0.4),
        title, sz=16, clr=WHITE, bold=True)
    txt(s, x + Pt(14), Inches(3.5), cw - Pt(28), Inches(0.9),
        body, sz=11.5, clr=GRAY1)
    if i < 4:
        txt(s, x + cw, Inches(3.2), gap, Inches(0.4),
            "→", sz=20, clr=GRAY2, align=PP_ALIGN.CENTER)

txt(s, Inches(2.5), Inches(4.75), Inches(8.3), Inches(0.4),
    "↻  STAGE 5 완료 → 다음 회의 녹음 → STAGE 1  (closed loop)",
    sz=15, clr=BRAND, bold=True, align=PP_ALIGN.CENTER)

divider(s, Inches(1), Inches(5.4), Inches(11.3))
txt(s, Inches(1), Inches(5.65), Inches(6), Inches(0.3),
    "왜 AI여야 하는가 (규칙으로는 불가능한 3가지)", sz=14, clr=WHITE, bold=True)

mtxt(s, Inches(1), Inches(6.05), Inches(11.5), Inches(1.2),
     [
         ('“그건 제가 한번 볼게요”  →  액션아이템 판단 (한국어 화법 맥락)', {"sz": 13, "clr": GRAY1}),
         ('“중간발표 전까지는 돼야죠”  →  암묵적 기한을 실제 날짜로 변환', {"sz": 13, "clr": GRAY1}),
         ('“자료가 아직 안 와서요”  →  막힘(blocker) 상태 자동 분류', {"sz": 13, "clr": GRAY1}),
     ], spacing=1.5)

page_num(s, 4)


# ════════════════════════════════════════════
# S5. 성공 기준 — 평가 항목 / 목표 초안 / 측정 방법 (팀 논의 반영)
# ════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
pill(s, Inches(1), Inches(0.7), "성공 기준", TEAL)

txt(s, Inches(1), Inches(1.25), Inches(11.5), Inches(1.1),
    "관리시간과 추출 품질을 측정하고,\n기한 내 이행률을 비교합니다", sz=34, clr=WHITE, bold=True)

txt(s, Inches(1), Inches(2.45), Inches(11), Inches(0.35),
    "목표 초안이며, 초기 측정 후 확정합니다", sz=14, clr=GRAY1)

# 표 — 헤더
HX = [Inches(1), Inches(3.5), Inches(6.5)]      # 열 시작 x
HW = [Inches(2.3), Inches(2.8), Inches(5.8)]    # 열 너비
card(s, Inches(1), Inches(2.95), Inches(11.3), Inches(0.5), SURFACE2)
for x, w, label in zip(HX, HW, ["평가 항목", "목표 초안", "측정 방법"]):
    txt(s, x + Pt(16), Inches(3.02), w, Inches(0.35), label, sz=14, clr=GRAY1, bold=True)

rows = [
    ("관리시간", "50% 감소",
     "검수·수정·등록·팔로업에 사람이 쓴 시간을 수작업과 비교"),
    ("추출 품질", "정확도 ≥ 90% · 누락률 ≤ 10%",
     "팀원이 만든 정답과 대조 · 명시된 담당자·기한도 별도 점검"),
    ("기한 내 이행률", "도입 전후 비교",
     "기한이 도래한 확정 액션 중 기한 내 완료 비율 측정"),
]
for i, (item, goal, method) in enumerate(rows):
    y = Inches(3.6) + Inches(0.78) * i
    card(s, Inches(1), y, Inches(11.3), Inches(0.68), SURFACE)
    txt(s, HX[0] + Pt(16), y + Inches(0.15), HW[0], Inches(0.4), item, sz=16, clr=WHITE, bold=True)
    txt(s, HX[1] + Pt(16), y + Inches(0.16), HW[1], Inches(0.4), goal, sz=14, clr=BRAND, bold=True)
    txt(s, HX[2] + Pt(16), y + Inches(0.16), HW[2], Inches(0.4), method, sz=13, clr=GRAY1)

# 검증 규모 + 한계
divider(s, Inches(1), Inches(6.15), Inches(11.3))
txt(s, Inches(1), Inches(6.3), Inches(11.3), Inches(0.35),
    "검증 규모 — 회의 6~8회 · 액션 30건 이상 · 팀원 2명 교차 검수", sz=14, clr=WHITE, bold=True)
txt(s, Inches(1), Inches(6.7), Inches(11.3), Inches(0.3),
    "검수 시간을 포함해 측정하며, 소규모 전후 비교의 한계를 함께 보고  ·  체감 부담 변화는 설문(리커트 척도)으로 병행 확인",
    sz=12.5, clr=GRAY1)

page_num(s, 5)


# ════════════════════════════════════════════
# S6. 수행 계획 (v1 레이아웃 + 수직 슬라이스 일정 유지)
# ════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
pill(s, Inches(1), Inches(0.7), "수행 계획", TEAL)

txt(s, Inches(1), Inches(1.3), Inches(11.5), Inches(0.8),
    "직접 테스트하며 서비스를 구현할 예정입니다", sz=40, clr=WHITE, bold=True)

timeline = [
    ("10/24", "중간 발표", "문제 정의 + 설계 발표", BRAND),
    ("10/25 ~ 11/7", "최소 기능 구현", "녹음→추출→확인→등록 + 기본 팔로업 (전체 루프 최소 버전)", WHITE),
    ("11/8 ~ 11/21", "실제 사용 시작", "팀 회의 적용 · R&R·타임라인 보완 · 목표치 확정", WHITE),
    ("11/22 ~ 12/5", "사용하면서 개선", "답변 해석 · 지연 알림 · 다음 회의 안건 연결", WHITE),
    ("12/6 ~ 12/18", "최종 검증 · 분석", "관리시간 · 추출 품질 · 이행률 정리", WHITE),
    ("12/19", "기말 발표", "라이브 데모 + 실제 사용 결과", BRAND),
]

for i, (period, title, desc, clr) in enumerate(timeline):
    y = Inches(2.5) + Inches(0.62) * i
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.2), y + Pt(4), Pt(10), Pt(10))
    dot.fill.solid()
    dot.fill.fore_color.rgb = clr if clr == BRAND else GRAY2
    dot.line.fill.background()
    dot.shadow.inherit = False
    if i < len(timeline) - 1:
        line = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                  Inches(1.2) + Pt(4), y + Pt(16), Pt(2), Inches(0.5))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER
        line.line.fill.background()
        line.shadow.inherit = False
    txt(s, Inches(1.8), y, Inches(2.2), Inches(0.35), period, sz=13, clr=GRAY1)
    txt(s, Inches(4.2), y, Inches(3.3), Inches(0.35), title, sz=15, clr=clr, bold=True)
    txt(s, Inches(7.6), y, Inches(5.3), Inches(0.35), desc, sz=12.5, clr=GRAY1)

txt(s, Inches(1), Inches(6.5), Inches(11.5), Inches(0.4),
    "11월 초부터 최소 기능을 팀 회의에 적용 → 사용·개선을 병행하며 기말까지 효과 검증",
    sz=17, clr=BRAND, bold=True)

page_num(s, 6)


# ════════════════════════════════════════════
# S7. 마무리
# ════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)

txt(s, Inches(1), Inches(2.2), Inches(11), Inches(1.8),
    "기존 도구는\n회의를 기록합니다.", sz=46, clr=GRAY1, bold=True)

txt(s, Inches(1), Inches(4.2), Inches(11), Inches(1.0),
    "우리는 회의를 완결합니다.", sz=46, clr=WHITE, bold=True)

divider(s, Inches(1), Inches(5.6), Inches(2.5), BRAND)

txt(s, Inches(1), Inches(5.9), Inches(6), Inches(0.4),
    "FollowIt  ·  팔로잇", sz=18, clr=BRAND, bold=True)

txt(s, Inches(1), Inches(6.5), Inches(5), Inches(0.3),
    "감사합니다", sz=16, clr=GRAY2)

page_num(s, 7)


# ── 저장 ──
out = "/Users/sc.park/Desktop/0_ClaudeCode/3_KAIST/2026-Fall/1_Business_Strategy/3_TeamProject/docs/midterm_presentation_v3.pptx"
prs.save(out)
print(f"✅ PPT v3 생성 완료: {out}")
print(f"   총 {len(prs.slides)}장 슬라이드")
