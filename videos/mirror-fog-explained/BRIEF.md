---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "샤워 후 거울이 뿌예지는 건 수증기가 차가운 거울에 응결되기 때문"
destination: shorts
aspect: 1080x1920
language: ko
audience: 한국어 사용자, 잡학·과학 상식 쇼츠 시청자
length: ~50s
angle: concept
style_preset: pending
---

## Intent

잡지식탁 브랜드의 쇼츠 영상. 샤워 후 거울이 뿌예지는 물리 현상(응결)을 40~55초 세로 쇼츠로 친근하게 설명한다. 톤은 브랜드 톤에 맞게 부드럽고 호기심 자극형, 반말 서술. 나레이션 오디오는 이미 제공됨(3나레이션.wav) — 재생성하지 않는다.

## Assets

- public/narration.wav — 사용자가 미리 녹음한 완성 나레이션 (원본: 3나레이션.wav). 이걸 그대로 사용한다.
- public/brand-icon.png — 잡지식탁 브랜드 아이콘 (원본: 잡지식탁_아이콘_260815.png). 오프닝/엔딩에 배치.

## Customizations

- VO_MODE: verbatim — 스크립트 원문 그대로 사용, 문장 재배열 금지.
- 나레이션은 이미 완성된 실제 녹음을 사용하므로 TTS 파이프라인을 돌리지 않는다. 오디오 파이프라인은 STT(전사)로 워드 타이밍만 뽑는다.
- BGM: 잔잔한 lofi/curious 무드 (신비로운, 학습적). 시그니처는 좋음.
- 오프닝: 잡지식탁 아이콘 + 브랜드 워드마크(왼쪽 상단 or 인트로 스팅).
- 자막(캡션): 켬. 한국어 굵은 산세리프, 강조 단어에 브랜드 컬러 하이라이트.

## Notes

- 세로 1080x1920 (쇼츠).
- 반말체 유지: "~어/야/거야" — 스크립트 그대로.
- 시각 은유: 욕실 → 수증기 파티클 → 차가운 거울 표면 → 응결 물방울 → 빛 산란. 다이어그램/타이포/추상 그래픽으로 표현.
- 실제 사진 사용 금지, 페이스리스 explainer.
