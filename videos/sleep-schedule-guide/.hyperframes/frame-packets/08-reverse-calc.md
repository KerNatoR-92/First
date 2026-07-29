# Frame packet: 08-reverse-calc

## Project inputs

- Project: /home/user/First/videos/sleep-schedule-guide
- Design tokens: /home/user/First/videos/sleep-schedule-guide/frame.md
- RULES_DIR: /root/.claude/skills/hyperframes-animation/rules

## Assigned storyboard block

## Frame 8 — 역산 (기상 시간부터)

- scene: 큰 등식 "기상 7시 − 수면 = 취침 시간" 이 좌→우로 조립됨
- duration: 12.69s
- transition_in: crossfade
- status: outline
- voiceover: "중요한 것은 자신이 일어나야 하는 시간에서 필요한 수면 시간을 거꾸로 계산하는 것입니다. 예를 들어 아침 7시에 일어나야 하는 사람이라면 밤 10시부터 12시 사이에는 잠들 수 있도록 준비하는 것이 좋습니다."
- src: compositions/frames/08-reverse-calc.html
- blueprint: equation-reveal
- focal: formula-line
- roles: [wake-time, minus-op, sleep-duration, equals, bedtime-range, subline]

핵심 계산 원리. "07:00 − 7-9h = 22:00 ~ 24:00" 을 큰 단일 라인으로 조립.
숫자는 흰색 대문자 mono, 연산자 (−, =) 는 노란색 얇은 대체.
