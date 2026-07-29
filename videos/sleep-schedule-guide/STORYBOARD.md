---
format: 1920x1080
duration: 110s
message: "직장인의 건강은 규칙적인 수면 시간에서 시작된다"
arc: Hook → Problem → Preview → Answer → How → Rule
audience: 30-40대 직장인
mode: autonomous
music: none
---

## Frame 1 — Hook Q

- scene: 정중앙에서 굵은 질문이 한 자씩 등장. 강조 단어 "몇 시"는 노란색.
- duration: 11.01s
- transition_in: cut
- status: animated
- voiceover: "여러분은 평일과 주말에 각각 몇 시에 잠드시나요?"
- src: compositions/frames/01-hook.html
- blueprint: reveal-question
- focal: title-question
- roles: [q-text, q-highlight, watermark-lines]

시청자를 직접 조준하는 오프닝 질문. 다크 스크린에서 검은 배경에 얇은
가로 헤어라인이 위·아래에 그어지고, 그 사이로 굵은 질문 텍스트가
스텝-바이-스텝 자간 리빌. "몇 시"만 노란색으로 하이라이트.

## Frame 2 — 평일 vs 주말

- scene: 좌 "평일" 우 "주말" 2단 분할, 각 아래에 다른 취침·기상 시간이
  숫자 카운터로 낙차 있게 나타남.
- duration: 12.32s
- transition_in: crossfade
- status: animated
- voiceover: "평일에는 출근 때문에 억지로 일찍 일어나고, 주말에는 밀린 잠을 보충하느라 점심때까지 자는 분들이 많습니다."
- src: compositions/frames/02-weekday-weekend.html
- blueprint: split-compare
- focal: two-label-split
- roles: [label-weekday, label-weekend, time-weekday, time-weekend, vertical-rule]

한 화면에 두 리듬을 병치하는 스플릿. 중앙에 얇은 세로 구분선(노란 1px),
좌우로 라벨 "평일 · WEEKDAY" / "주말 · WEEKEND"가 상단에 앉고, 하단에는
각각의 취침·기상 시각이 크게 카운트업.

## Frame 3 — 새벽에 잠들고, 일찍 일어나고

- scene: 24시간 하이라인 위에 두 개의 점이 흩어져 나타나며 불규칙 리듬을 시각화
- duration: 9.96s
- transition_in: cut
- status: animated
- voiceover: "야근이나 회식이 있는 날에는 새벽에 잠들고, 다음 날 중요한 일정이 있으면 평소보다 일찍 일어나기도 합니다."
- src: compositions/frames/03-irregular-nights.html
- blueprint: timeline-scatter
- focal: 24h-timeline
- roles: [timeline-rule, tick-labels, night-late-dot, morning-early-dot, callouts]

24시간 눈금 라인이 가로로 길게 깔리고, 하루하루의 취침·기상 순간이
노란 점으로 흩어져 나타남. "야근" / "회식" / "중요한 일정" 등의
얇은 캘아웃 텍스트가 순차로 페어링.

## Frame 4 — 충분히 잤다고 생각해도 피곤

- scene: 큰 등식 "충분히 잤다? ≠ 피곤하지 않다" 가 텍스트로 조립되며 등장
- duration: 12.84s
- transition_in: crossfade
- status: animated
- voiceover: "이렇게 하루하루 자는 시간이 달라지면 우리는 충분히 잤다고 생각해도 계속 피곤할 수 있습니다."
- src: compositions/frames/04-still-tired.html
- blueprint: equation-reveal
- focal: inequality-statement
- roles: [lhs-text, neq-sign, rhs-text, subline]

방정식 형태로 반전되는 인사이트를 만듦. "잔 시간의 총량"과 "실제 컨디션"의
불일치를 ≠ 기호로 시각화. ≠는 굵은 노란색, 좌우 텍스트는 흰색.

## Frame 5 — 오늘 다룰 3가지

- scene: 세로로 넘버링된 3개의 헤드라인이 위에서 아래로 순차 등장 (01 / 02 / 03)
- duration: 10.75s
- transition_in: cut
- status: animated
- voiceover: "오늘은 직장인에게 필요한 수면 시간은 몇 시간인지, 규칙적으로 잠을 자면 무엇이 좋아지는지, 반대로 수면 시간이 불규칙하면 어떤 문제가 생기는지 알아보겠습니다."
- src: compositions/frames/05-agenda.html
- blueprint: numbered-list
- focal: three-topics
- roles: [num-01, num-02, num-03, topic-1, topic-2, topic-3, section-label]

메인 콘텐츠의 어젠다. 상단에 "AGENDA / 오늘 다룰 것" 라벨, 왼쪽에 큰
노란 넘버(01 02 03), 오른쪽에 각 주제. "필요한 수면 시간" / "규칙적 수면의 이점"
/ "불규칙 수면의 문제". 각 라인이 상→하 순으로 페이드-업.

## Frame 6 — 우선, 우리는 몇 시에?

- scene: 큰 질문 텍스트 "우선, 우리는 몇 시에 자야 할까요?" — 화면 중앙 정렬
- duration: 12.85s
- transition_in: crossfade
- status: animated
- voiceover: "그리고 잠들기 어려운 분들에게 도움이 될 수 있는 음식과 성분, 생활 습관도 함께 이야기해 보겠습니다. 우선, 우리는 몇 시에 자야 할까요?"
- src: compositions/frames/06-first-question.html
- blueprint: reveal-question
- focal: pivot-question
- roles: [q-text, q-highlight, tag]

챕터 브레이크. "SECTION 01" 소형 라벨 후, 큰 질문 텍스트가 한 줄로 뜬다.
"몇 시" 부분은 노란색 강조. 밑에는 얇은 노란 밑줄 애니메이션.

## Frame 7 — 최소 7시간

- scene: "7" 이라는 거대 숫자가 화면을 가르며 등장, 옆에 "시간 이상" 서브
- duration: 15.29s
- transition_in: cut
- status: animated
- voiceover: "성인은 일반적으로 하루에 최소 7시간 이상의 수면이 필요합니다. 개인차는 있지만 대부분의 성인은 약 7시간에서 9시간 정도 잠을 자는 것이 좋습니다."
- src: compositions/frames/07-seven-hours.html
- blueprint: hero-stat
- focal: big-number-7
- roles: [stat-value, stat-unit, stat-label, range-line, hairline]

핵심 스탯 프레임. 좌측에 거대한 노란색 "7", 우측에는 세로로 쌓인
"HOURS · MINIMUM / 최소 7시간 이상". 하단에는 7—9 범위 바 (7 ●━━━━━● 9).

## Frame 8 — 역산 (기상 시간부터)

- scene: 큰 등식 "기상 7시 − 수면 = 취침 시간" 이 좌→우로 조립됨
- duration: 12.69s
- transition_in: crossfade
- status: animated
- voiceover: "중요한 것은 자신이 일어나야 하는 시간에서 필요한 수면 시간을 거꾸로 계산하는 것입니다. 예를 들어 아침 7시에 일어나야 하는 사람이라면 밤 10시부터 12시 사이에는 잠들 수 있도록 준비하는 것이 좋습니다."
- src: compositions/frames/08-reverse-calc.html
- blueprint: equation-reveal
- focal: formula-line
- roles: [wake-time, minus-op, sleep-duration, equals, bedtime-range, subline]

핵심 계산 원리. "07:00 − 7-9h = 22:00 ~ 24:00" 을 큰 단일 라인으로 조립.
숫자는 흰색 대문자 mono, 연산자 (−, =) 는 노란색 얇은 대체.

## Frame 9 — 7 / 8 / 9시간 취침표

- scene: 3행 표가 순차 등장 — [7시간 → 자정 전] [8시간 → 11시] [9시간 → 10시]
- duration: 7.31s
- transition_in: cut
- status: animated
- voiceover: "7시간을 자려면 자정 전에 잠들어야 하고, 8시간을 자려면 밤 11시, 9시간을 자려면 밤 10시쯤 잠들어야 합니다."
- src: compositions/frames/09-schedule-table.html
- blueprint: fade-list
- focal: three-row-schedule
- roles: [row-1, row-2, row-3, arrow-1, arrow-2, arrow-3, header-label]

빠른 리듬 표. 각 행은 [수면 시간 · 라벨] → [화살표] → [취침 시간].
왼쪽 컬럼 노란 굵은 숫자, 오른쪽 컬럼 큰 흰 시간 텍스트. 3행이 
"타이핑 리듬"으로 시간 간격을 두고 순차 등장.

## Frame 10 — 규칙성이 진짜 핵심

- scene: 짧은 클로징 스테이트먼트 "매일 비슷한 시간에" 가 큰 텍스트로 페이드-인, 하단 얇은 노란 밑줄
- duration: 5.49s
- transition_in: crossfade
- status: animated
- voiceover: "실제로 잠드는 시간을 기준으로 계산하는 것이 중요합니다. 그리고 수면 시간만큼 중요한 것이 매일 비슷한 시간에 자고 일어나는 것입니다."
- src: compositions/frames/10-consistency.html
- blueprint: statement-close
- focal: closing-statement
- roles: [big-line, subline, underline-bar]

마지막 각인. 화면 중앙에 큰 흰 텍스트 "매일 비슷한 시간에", 아래에 
"자고 · 일어나기" 라는 서브라인. 노란 헤어라인이 좌→우로 그어지며 닫힘.
