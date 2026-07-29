# Frame packet: 02-weekday-weekend

## Project inputs

- Project: /home/user/First/videos/sleep-schedule-guide
- Design tokens: /home/user/First/videos/sleep-schedule-guide/frame.md
- RULES_DIR: /root/.claude/skills/hyperframes-animation/rules

## Assigned storyboard block

## Frame 2 — 평일 vs 주말

- scene: 좌 "평일" 우 "주말" 2단 분할, 각 아래에 다른 취침·기상 시간이
  숫자 카운터로 낙차 있게 나타남.
- duration: 12.32s
- transition_in: crossfade
- status: outline
- voiceover: "평일에는 출근 때문에 억지로 일찍 일어나고, 주말에는 밀린 잠을 보충하느라 점심때까지 자는 분들이 많습니다."
- src: compositions/frames/02-weekday-weekend.html
- blueprint: split-compare
- focal: two-label-split
- roles: [label-weekday, label-weekend, time-weekday, time-weekend, vertical-rule]

한 화면에 두 리듬을 병치하는 스플릿. 중앙에 얇은 세로 구분선(노란 1px),
좌우로 라벨 "평일 · WEEKDAY" / "주말 · WEEKEND"가 상단에 앉고, 하단에는
각각의 취침·기상 시각이 크게 카운트업.
