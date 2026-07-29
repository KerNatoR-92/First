# 프레임 타이밍 수정 가이드

이 프로젝트는 `A1.wav` 를 무음 구간 기준으로 10개 프레임으로 잘라 각 프레임 시각과 오디오를 맞춰놓았습니다. **자동 트랜스크립션이 원격 환경에서 차단되어 정확한 매핑을 만들지 못했습니다** — 그래서 아래 편집 도구로 직접 조정할 수 있게 준비했습니다.

## 준비물

- ffmpeg (프로젝트에 이미 설치되어 있음)
- node (프로젝트에 이미 설치되어 있음)
- 각 프레임의 실제 오디오 내용을 확인할 수 있는 오디오 플레이어 (macOS의 QuickTime, VS Code Audio Preview 등)

## 편집 절차

### 1. 각 프레임 오디오 미리 듣기

`assets/voice/` 밑의 파일들을 순서대로 재생합니다:

```
assets/voice/01.wav   ← Frame 1 오디오
assets/voice/02.wav   ← Frame 2 오디오
...
assets/voice/10.wav   ← Frame 10 오디오
```

각 파일이 어떤 스크립트 문장을 담고 있는지 확인하세요.

### 2. `TIMINGS.json` 수정

프로젝트 루트의 `TIMINGS.json` 을 여세요. 예시:

```json
{
  "frames": [
    { "id": "01-hook",              "start":   0.000, "end":  11.010, "text": "여러분은 평일과 주말에..." },
    { "id": "02-weekday-weekend",   "start":  11.010, "end":  23.335, "text": "평일에는 출근 때문에..." },
    ...
  ]
}
```

- **`start` / `end`** (초): 프레임의 시작·종료 시각. 다음 프레임의 `start` 는 이전 프레임의 `end` 와 같게 유지하세요.
- **`text`**: 참고용. 이 값을 바꿔도 화면 텍스트는 바뀌지 않습니다.
- **`id`**: 절대 변경하지 마세요. 각 HTML 파일과 매핑됩니다.

**예시 - 프레임 3이 실제로는 21초에 시작한다면:**

```json
{ "id": "02-weekday-weekend", "start": 11.010, "end": 21.000, "text": "..." },
{ "id": "03-irregular-nights", "start": 21.000, "end": 33.295, "text": "..." },
```

### 3. 다시 렌더링

```bash
cd videos/sleep-schedule-guide
node retime.mjs
```

이 스크립트는 자동으로:

1. `A1.wav` 를 새 시각으로 다시 자릅니다 → `assets/voice/NN.wav`
2. `STORYBOARD.md` 의 duration 을 새 값으로 업데이트
3. 각 `compositions/frames/NN-*.html` 의 root/clip data-duration 재계산
4. `audio_meta.json` 재작성
5. `assemble-index` → `transitions inject` → `check` → `snapshot` → `render` 자동 실행

## 옵션

```bash
node retime.mjs --no-render  # 렌더 없이 빌드만 (미리보기용)
node retime.mjs --dry-run    # 파일 수정 없이 계산 결과만 보기
```

## 화면 문구/디자인 변경

`TIMINGS.json` 의 `text` 는 참고용입니다. **실제 화면 문구/디자인은 각 프레임 HTML 을 직접 편집**하세요:

```
compositions/frames/01-hook.html
compositions/frames/02-weekday-weekend.html
...
```

각 파일 안의 `<div class="f01-line1">여러분은,</div>` 같은 텍스트를 원하는 문구로 바꾸면 됩니다.

편집 후 다시 렌더:

```bash
node retime.mjs --no-render   # 프레임 타이밍은 그대로 두고 빌드
npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4
```

## 자주 있는 상황

**"프레임 4의 오디오가 프레임 5에 있는 텍스트를 말한다"**
→ 프레임 4의 end 를 뒤로 밀거나, 프레임 5 의 start 를 앞으로 당기세요.

**"프레임 2가 너무 길고 3이 짧다"**
→ 프레임 2 의 end 를 앞당기고, 프레임 3 의 start 를 같은 값으로 맞추면 됩니다.

**"어떤 문장은 두 프레임에 걸쳐 있음"**
→ 문장의 자연스러운 쉼표 위치에서 자르거나, 두 프레임을 하나로 합치세요 (그 경우 HTML 하나를 삭제하고 duration 을 늘리면 됩니다 — 이는 더 복잡한 편집이니 필요하면 다시 요청해주세요).
