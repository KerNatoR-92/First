---
workflow: general-video
flow: automation
storyboard: no
message: "수면 시간이 불규칙해지면 피곤해진다 — 규칙적으로 자자"
destination: youtube
aspect: 1920x1080
language: ko
audience: 수면이 불규칙한 한국 직장인
length: 120s
voice: user-supplied
---

## Intent

사용자 제공 나레이션(A1.wav 45.76s + A2.wav 74.36s → narration.wav 120.12s)에
문장 단위 한글 자막과 SVG/CSS 시네마틱 밤/수면 무드 배경을 얹은 2분짜리 롱폼 도입부.
15년차 유튜브 편집자 톤: 화면당 메시지 하나, 컷 사이 짧은 크로스페이드(200~350ms),
어두운 팔레트 + 은은한 앰버/블루 하이라이트.

## Assets

- public/A1.wav — 사용자 제공 나레이션 파트 1 (24kHz mono, 45.76s)
- public/A2.wav — 사용자 제공 나레이션 파트 2 (24kHz mono, 74.36s)
- public/narration.wav — A1+A2 lossless concat (120.12s). 이것이 최종 오디오 트랙.

## Customizations

- TTS 스킵 (유저 wav 사용). 타이밍은 스크립트 글자 수 비례로 계산.
- 한글 웹폰트: Noto Sans KR (기존 office-sleep-intro에서 재사용).
- BGM 없음 (수면 주제라 무음 유지).
- 자막 온: 문장 단위, 하단 세이프존.
- 이미지 소싱 불가 (egress 정책) → SVG/CSS 시네마틱 배경으로 대체.

## Notes

- 배경 무드: 창문+달빛, 야간 침실, 늦은 밤 노트북 글로우, 시계 다이얼,
  시간축 눈금, 도시 야경. 실사 아니지만 톤은 photographic dark.
- 문장 사이 짧은 크로스페이드, 스프링 최소화.
- 34개 문장 자막, 6~8개 배경 무드로 그룹핑.
