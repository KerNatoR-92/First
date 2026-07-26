---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "불규칙한 수면은 충분히 자도 계속 피곤하게 만든다"
destination: youtube
aspect: 1920x1080
language: ko
audience: 수면이 불규칙한 한국 직장인
length: 46s
angle: concept
style_preset: editorial-forest
voice: user-supplied
---

## Intent

직장인의 수면 불규칙 문제를 다루는 롱폼 영상의 도입부. 문제 제기(주말 몰아자기, 야근/회식 후 수면 시간 흔들림)를 공감형으로 던지고, "오늘 다룰 것"까지 예고하는 인트로. 톤은 차분하고 편집·타이포 위주의 미니멀 편집 감성. 15년차 유튜브 편집자의 관점 — 화면당 메시지 하나, 여백 넉넉, 강조는 색/굵기 1단계만.

## Assets

- public/A1.wav — 사용자 제공 나레이션 (24kHz mono, 45.76s). TTS 생성 금지. 이 파일이 나레이션 트랙.

## Customizations

- 사용자 나레이션 사용 (TTS 스킵). audio_meta.json은 유저 wav 기준으로 수동 조립.
- 프리셋의 라틴 서체를 한글 웹폰트로 스왑: 디스플레이는 Noto Serif KR (또는 Nanum Myeongjo), 본문/라벨은 Pretendard.
- BGM 없음 (수면 주제라 무음 유지, 나레이션에 집중).
- 자막 온: 하단 세이프존 존중, 한국어 라인 단위 가독성 우선.

## Notes

- 미니멀 원칙: 화면당 1메시지, 강조색 1개, 폰트 2웨이트 이내.
- 컷 사이는 짧은 크로스페이드 위주 (200~350ms). 스프링·바운스 최소화.
- 나레이션 리듬에 붙이되, 문장 시작보다 살짝 뒤 (150~250ms) 텍스트 리빌.
- 자는 시간이 흔들리는 감각을 시각적으로 살짝 은유 (라인/블록의 미묘한 어긋남 또는 시간 눈금 정렬).
