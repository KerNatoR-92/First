#!/usr/bin/env python3
"""Generate videos/sleep-broll/index.html from timings.json."""
import json, textwrap

with open("timings.json", encoding="utf-8") as f:
    T = json.load(f)

CAPS = T["captions"]
SCENES = T["scenes"]
DUR = T["narration_duration"]

# ---------- SVG background templates ----------
# Each returns SVG markup sized to 1920x1080. Static, moody, dark.

def bg_window_moon():
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <radialGradient id="g-moon" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0%" stop-color="#f3e8c8" stop-opacity="0.9"/>
          <stop offset="60%" stop-color="#e8d59a" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#0a0e14" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="g-room" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d1420"/>
          <stop offset="100%" stop-color="#050810"/>
        </linearGradient>
        <linearGradient id="g-win" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#1a2438" stop-opacity="1"/>
          <stop offset="100%" stop-color="#0d1420" stop-opacity="1"/>
        </linearGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-room)"/>
      <!-- window frame -->
      <rect x="1180" y="180" width="560" height="720" fill="url(#g-win)" stroke="#2a3550" stroke-width="6"/>
      <line x1="1460" y1="180" x2="1460" y2="900" stroke="#2a3550" stroke-width="4"/>
      <line x1="1180" y1="540" x2="1740" y2="540" stroke="#2a3550" stroke-width="4"/>
      <!-- moon glow -->
      <circle cx="1560" cy="380" r="260" fill="url(#g-moon)"/>
      <circle cx="1560" cy="380" r="82" fill="#f3e8c8" opacity="0.92"/>
      <circle cx="1590" cy="368" r="82" fill="#0d1420"/>
      <!-- floor line -->
      <line x1="0" y1="960" x2="1920" y2="960" stroke="#1a2233" stroke-width="2"/>
    </svg>
    """

def bg_bed_alarm():
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <linearGradient id="g-bg2" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d1420"/>
          <stop offset="100%" stop-color="#080b13"/>
        </linearGradient>
        <linearGradient id="g-blanket" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#1c2438"/>
          <stop offset="100%" stop-color="#141a2a"/>
        </linearGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-bg2)"/>
      <!-- headboard -->
      <rect x="180" y="480" width="1080" height="180" fill="#1a2030" rx="8"/>
      <!-- mattress -->
      <rect x="140" y="660" width="1160" height="200" fill="#151b28" rx="10"/>
      <!-- blanket lump (person) -->
      <path d="M 260 830 Q 400 700 620 720 Q 780 730 900 810 Q 950 840 940 860 L 260 860 Z" fill="url(#g-blanket)"/>
      <!-- pillow -->
      <ellipse cx="360" cy="720" rx="120" ry="50" fill="#1e2540" opacity="0.85"/>
      <!-- nightstand -->
      <rect x="1360" y="720" width="240" height="200" fill="#131824" rx="6"/>
      <!-- clock -->
      <rect x="1400" y="740" width="160" height="90" fill="#0a0d15" rx="8" stroke="#2a3550" stroke-width="2"/>
      <text x="1480" y="805" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="46" font-weight="500" fill="#f0c674">06:30</text>
      <!-- floor -->
      <line x1="0" y1="960" x2="1920" y2="960" stroke="#141a2a" stroke-width="2"/>
    </svg>
    """

def bg_laptop_glow():
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <radialGradient id="g-screen" cx="0.5" cy="0.4" r="0.6">
          <stop offset="0%" stop-color="#7ea8d8" stop-opacity="0.55"/>
          <stop offset="60%" stop-color="#3a5580" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#0a0e14" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="g-desk" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0f1420"/>
          <stop offset="100%" stop-color="#060a12"/>
        </linearGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-desk)"/>
      <!-- ambient blue glow from screen -->
      <ellipse cx="960" cy="540" rx="900" ry="500" fill="url(#g-screen)"/>
      <!-- laptop base -->
      <rect x="640" y="720" width="640" height="30" fill="#1c2438" rx="4"/>
      <!-- laptop screen -->
      <polygon points="680,720 1240,720 1180,410 740,410" fill="#0a0d15" stroke="#2a3550" stroke-width="3"/>
      <!-- screen content lines -->
      <rect x="780" y="450" width="360" height="8" fill="#7ea8d8" opacity="0.7"/>
      <rect x="780" y="480" width="280" height="8" fill="#7ea8d8" opacity="0.5"/>
      <rect x="780" y="510" width="320" height="8" fill="#7ea8d8" opacity="0.6"/>
      <rect x="780" y="540" width="180" height="8" fill="#7ea8d8" opacity="0.4"/>
      <rect x="780" y="570" width="280" height="8" fill="#7ea8d8" opacity="0.5"/>
      <rect x="780" y="600" width="220" height="8" fill="#7ea8d8" opacity="0.4"/>
      <rect x="780" y="630" width="300" height="8" fill="#7ea8d8" opacity="0.5"/>
      <rect x="780" y="660" width="140" height="8" fill="#7ea8d8" opacity="0.35"/>
      <!-- coffee cup silhouette -->
      <ellipse cx="1440" cy="770" rx="70" ry="10" fill="#1a2030" opacity="0.6"/>
      <path d="M 1380 720 Q 1380 780 1420 790 L 1460 790 Q 1500 780 1500 720 Z" fill="#1a2030" stroke="#2a3550" stroke-width="2"/>
      <path d="M 1500 730 Q 1540 740 1530 770 Q 1520 780 1500 775" fill="none" stroke="#2a3550" stroke-width="2"/>
      <!-- steam -->
      <path d="M 1410 690 Q 1420 670 1410 650 Q 1400 630 1410 615" fill="none" stroke="#f0c674" stroke-width="2" opacity="0.35"/>
      <path d="M 1440 690 Q 1450 670 1440 650 Q 1430 630 1440 615" fill="none" stroke="#f0c674" stroke-width="2" opacity="0.35"/>
      <path d="M 1470 690 Q 1480 670 1470 650 Q 1460 630 1470 615" fill="none" stroke="#f0c674" stroke-width="2" opacity="0.35"/>
    </svg>
    """

def bg_timeline_drift():
    # Irregular vertical bars representing sleep time drift day-to-day
    bars = []
    heights = [180, 260, 140, 320, 200, 380, 160]
    labels = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    start_x = 260
    step = 200
    for i, (h, lbl) in enumerate(zip(heights, labels)):
        x = start_x + i * step
        top = 540 - h
        bars.append(f'<rect x="{x}" y="{top}" width="120" height="{h}" fill="#f0c674" opacity="0.75" rx="4"/>')
        bars.append(f'<text x="{x+60}" y="820" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" font-size="24" letter-spacing="0.15em" fill="#7a8894">{lbl}</text>')
    bars_svg = "\n".join(bars)
    return f"""
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <linearGradient id="g-drift" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d1420"/>
          <stop offset="100%" stop-color="#080b13"/>
        </linearGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-drift)"/>
      <!-- baseline -->
      <line x1="200" y1="700" x2="1720" y2="700" stroke="#2a3550" stroke-width="2"/>
      <!-- dashed target line -->
      <line x1="200" y1="380" x2="1720" y2="380" stroke="#f0c674" stroke-width="2" stroke-dasharray="8,10" opacity="0.5"/>
      {bars_svg}
      <text x="200" y="360" font-family="'JetBrains Mono', monospace" font-size="22" letter-spacing="0.2em" fill="#f0c674">TARGET · 7H</text>
    </svg>
    """

def bg_title_fade():
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <radialGradient id="g-amb" cx="0.5" cy="0.55" r="0.6">
          <stop offset="0%" stop-color="#1a2438" stop-opacity="1"/>
          <stop offset="100%" stop-color="#050810" stop-opacity="1"/>
        </radialGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-amb)"/>
      <!-- accent horizontal lines -->
      <line x1="200" y1="200" x2="500" y2="200" stroke="#f0c674" stroke-width="2"/>
      <line x1="200" y1="880" x2="500" y2="880" stroke="#f0c674" stroke-width="2"/>
      <line x1="1420" y1="200" x2="1720" y2="200" stroke="#f0c674" stroke-width="2"/>
      <line x1="1420" y1="880" x2="1720" y2="880" stroke="#f0c674" stroke-width="2"/>
      <!-- corner marks -->
      <line x1="200" y1="200" x2="200" y2="240" stroke="#f0c674" stroke-width="2"/>
      <line x1="200" y1="880" x2="200" y2="840" stroke="#f0c674" stroke-width="2"/>
      <line x1="1720" y1="200" x2="1720" y2="240" stroke="#f0c674" stroke-width="2"/>
      <line x1="1720" y1="880" x2="1720" y2="840" stroke="#f0c674" stroke-width="2"/>
    </svg>
    """

def bg_number_focus():
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <radialGradient id="g-num" cx="0.5" cy="0.4" r="0.55">
          <stop offset="0%" stop-color="#f0c674" stop-opacity="0.18"/>
          <stop offset="100%" stop-color="#0a0e14" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="1920" height="1080" fill="#0a0e14"/>
      <ellipse cx="960" cy="440" rx="720" ry="360" fill="url(#g-num)"/>
      <text x="920" y="500" text-anchor="middle" font-family="'Noto Sans KR', sans-serif" font-size="340" font-weight="900" letter-spacing="-0.06em" fill="#f0c674" opacity="0.92">7–9</text>
      <text x="1180" y="500" text-anchor="middle" font-family="'Noto Sans KR', sans-serif" font-size="180" font-weight="500" letter-spacing="-0.03em" fill="#f0c674" opacity="0.92">h</text>
      <text x="960" y="620" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="26" letter-spacing="0.4em" fill="#7a8894">RECOMMENDED SLEEP</text>
    </svg>
    """

def bg_reverse_calc():
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <linearGradient id="g-rev" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d1420"/>
          <stop offset="100%" stop-color="#050810"/>
        </linearGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-rev)"/>
      <!-- Clock circle -->
      <circle cx="960" cy="480" r="260" fill="none" stroke="#2a3550" stroke-width="3"/>
      <circle cx="960" cy="480" r="240" fill="none" stroke="#1a2233" stroke-width="1"/>
      <!-- Hour ticks -->
      <g stroke="#7a8894" stroke-width="3" stroke-linecap="round">
        <line x1="960" y1="240" x2="960" y2="266"/>
        <line x1="1200" y1="480" x2="1174" y2="480"/>
        <line x1="960" y1="720" x2="960" y2="694"/>
        <line x1="720" y1="480" x2="746" y2="480"/>
      </g>
      <!-- Numbers -->
      <text x="960" y="230" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="24" fill="#7a8894">12</text>
      <text x="1250" y="490" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="24" fill="#7a8894">3</text>
      <text x="960" y="750" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="24" fill="#7a8894">6</text>
      <text x="670" y="490" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="24" fill="#7a8894">9</text>
      <!-- Reverse arrow arc -->
      <path d="M 960 260 A 200 200 0 1 0 760 460" fill="none" stroke="#f0c674" stroke-width="4" stroke-linecap="round"/>
      <polygon points="760,460 750,442 774,440" fill="#f0c674"/>
      <text x="960" y="490" text-anchor="middle" font-family="'Noto Sans KR', sans-serif" font-size="52" font-weight="700" fill="#e6ecf3">역산</text>
    </svg>
    """

def bg_clock_hands():
    # Clock face showing 7:00 wake, with dashed arcs back to 22-24 for bedtime
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <linearGradient id="g-cl" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d1420"/>
          <stop offset="100%" stop-color="#050810"/>
        </linearGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-cl)"/>
      <!-- large clock -->
      <circle cx="960" cy="500" r="300" fill="none" stroke="#2a3550" stroke-width="4"/>
      <!-- 12 hour ticks -->
      <g stroke="#7a8894" stroke-width="3" stroke-linecap="round">
        <line x1="960" y1="215" x2="960" y2="240"/>
        <line x1="1245" y1="500" x2="1220" y2="500"/>
        <line x1="960" y1="785" x2="960" y2="760"/>
        <line x1="675" y1="500" x2="700" y2="500"/>
      </g>
      <!-- Numbers 12, 3, 6, 9 -->
      <text x="960" y="200" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="28" fill="#7a8894">12</text>
      <text x="1295" y="510" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="28" fill="#7a8894">3</text>
      <text x="960" y="820" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="28" fill="#7a8894">6</text>
      <text x="625" y="510" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="28" fill="#7a8894">9</text>
      <!-- Hour hand pointing at 7 (roughly 210 degrees from top) -->
      <line x1="960" y1="500" x2="820" y2="670" stroke="#f0c674" stroke-width="8" stroke-linecap="round"/>
      <!-- Minute hand at 12 -->
      <line x1="960" y1="500" x2="960" y2="280" stroke="#e6ecf3" stroke-width="5" stroke-linecap="round"/>
      <circle cx="960" cy="500" r="12" fill="#f0c674"/>
      <!-- 7 AM label -->
      <text x="960" y="880" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="28" letter-spacing="0.3em" fill="#f0c674">WAKE · 07:00</text>
    </svg>
    """

def bg_bed_latency():
    # Bed silhouette + hourglass showing 30-min latency
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <linearGradient id="g-lat" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d1420"/>
          <stop offset="100%" stop-color="#080b13"/>
        </linearGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-lat)"/>
      <!-- Bed silhouette left -->
      <rect x="180" y="580" width="720" height="220" fill="#151b28" rx="10"/>
      <path d="M 240 720 Q 380 620 560 640 Q 720 660 830 720 L 830 780 L 240 780 Z" fill="#1c2438"/>
      <ellipse cx="320" cy="640" rx="90" ry="36" fill="#1e2540"/>
      <!-- Hourglass right -->
      <g transform="translate(1400, 400)">
        <polygon points="0,0 200,0 100,140 0,0" fill="#1a2030" stroke="#f0c674" stroke-width="3"/>
        <polygon points="0,280 200,280 100,140 0,280" fill="#1a2030" stroke="#f0c674" stroke-width="3"/>
        <!-- Sand top (halfway drained) -->
        <polygon points="20,10 180,10 100,130" fill="#f0c674" opacity="0.5"/>
        <!-- Sand bottom -->
        <polygon points="30,270 170,270 100,180" fill="#f0c674" opacity="0.85"/>
        <!-- Sand stream -->
        <line x1="100" y1="140" x2="100" y2="180" stroke="#f0c674" stroke-width="3"/>
      </g>
      <!-- Label -->
      <text x="1500" y="750" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="26" letter-spacing="0.3em" fill="#f0c674">30 MIN</text>
      <text x="1500" y="790" text-anchor="middle" font-family="'Noto Sans KR', sans-serif" font-size="26" fill="#7a8894">잠들기까지</text>
    </svg>
    """

def bg_weekly_grid():
    # 7-day dot grid showing consistent sleep pattern
    return """
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;">
      <defs>
        <linearGradient id="g-wk" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d1420"/>
          <stop offset="100%" stop-color="#050810"/>
        </linearGradient>
      </defs>
      <rect width="1920" height="1080" fill="url(#g-wk)"/>
      <!-- Header -->
      <text x="960" y="230" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="24" letter-spacing="0.35em" fill="#7a8894">WEEKLY RHYTHM</text>
      <!-- Timeline axis -->
      <line x1="260" y1="620" x2="1660" y2="620" stroke="#2a3550" stroke-width="2"/>
      <!-- 7 day columns with consistent bed/wake bars -->
      <g>
        <!-- Days as columns -->
""" + "\n".join([
        f"""        <g transform="translate({260 + i*200}, 0)">
          <text x="0" y="290" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="22" letter-spacing="0.15em" fill="#7a8894">{d}</text>
          <!-- bed time bar (consistent, ~11pm) -->
          <rect x="-32" y="370" width="64" height="240" fill="#f0c674" opacity="{0.9 if i<5 else 0.7}" rx="4"/>
          <!-- wake dot -->
          <circle cx="0" cy="620" r="9" fill="#e6ecf3"/>
        </g>"""
        for i, d in enumerate(["MON","TUE","WED","THU","FRI","SAT","SUN"])
    ]) + """
      </g>
      <text x="960" y="740" text-anchor="middle" font-family="'Noto Sans KR', sans-serif" font-size="32" font-weight="500" fill="#e6ecf3">비슷한 시간에 자고 일어나기</text>
    </svg>
    """

BG_MAP = {
    "window-moon":     bg_window_moon,
    "bed-alarm":       bg_bed_alarm,
    "laptop-glow":     bg_laptop_glow,
    "timeline-drift":  bg_timeline_drift,
    "title-fade":      bg_title_fade,
    "number-focus":    bg_number_focus,
    "reverse-calc":    bg_reverse_calc,
    "clock-hands":     bg_clock_hands,
    "bed-latency":     bg_bed_latency,
    "weekly-grid":     bg_weekly_grid,
}

# ---------- HTML assembly ----------

CSS = """
      @font-face { font-family: "Noto Sans KR"; font-weight: 400; src: url("public/fonts/NotoSansKR-400.woff2") format("woff2"); font-display: block; }
      @font-face { font-family: "Noto Sans KR"; font-weight: 500; src: url("public/fonts/NotoSansKR-500.woff2") format("woff2"); font-display: block; }
      @font-face { font-family: "Noto Sans KR"; font-weight: 700; src: url("public/fonts/NotoSansKR-700.woff2") format("woff2"); font-display: block; }
      @font-face { font-family: "Noto Sans KR"; font-weight: 900; src: url("public/fonts/NotoSansKR-900.woff2") format("woff2"); font-display: block; }
      @font-face { font-family: "JetBrains Mono"; font-weight: 500; src: url("public/fonts/JetBrainsMono-500.woff2") format("woff2"); font-display: block; }

      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body {
        width: 1920px; height: 1080px;
        overflow: hidden;
        background: #050810;
        color: #e6ecf3;
        font-family: "Noto Sans KR", sans-serif;
        -webkit-font-smoothing: antialiased;
        font-feature-settings: "kern" 1, "liga" 1;
      }
      #root {
        position: relative;
        width: 1920px; height: 1080px;
        background: #050810;
        overflow: hidden;
      }

      /* Background scenes (track 1). Each covers full canvas. */
      .scene { position: absolute; inset: 0; }
      .scene-inner { position: absolute; inset: 0; opacity: 0; will-change: opacity; }

      /* Caption band. Alternates between track 2 and track 3 to avoid overlap. */
      .caption {
        position: absolute;
        left: 160px; right: 160px;
        bottom: 118px;
        text-align: center;
      }
      .cap-inner { opacity: 0; will-change: opacity, transform; }
      .caption .box {
        display: inline-block;
        max-width: 1520px;
        padding: 22px 38px;
        background: rgba(8, 12, 20, 0.82);
        border-radius: 10px;
        border: 1px solid rgba(240, 198, 116, 0.18);
      }
      .caption .txt {
        font-family: "Noto Sans KR", sans-serif;
        font-weight: 500;
        font-size: 46px;
        line-height: 1.45;
        letter-spacing: -0.005em;
        color: #f0f4fa;
        text-shadow: 0 2px 12px rgba(0,0,0,0.7);
      }
      .caption .txt em { font-style: normal; color: #f0c674; font-weight: 700; }

      /* Chapter indicator top-left */
      .chapter {
        position: absolute;
        top: 60px; left: 120px;
        font-family: "JetBrains Mono", monospace;
        font-size: 22px;
        font-weight: 500;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: #7a8894;
      }
      .chapter-inner { opacity: 0; will-change: opacity; }
      .chapter .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #f0c674; margin-right: 14px; vertical-align: middle; }
"""

def caption_html(cap, idx):
    text = cap["text"].replace("<", "&lt;")
    # Alternate captions between track 2 (odd) and track 3 (even) to avoid overlap
    track = 2 if (idx % 2 == 1) else 3
    # 100ms crossfade between consecutive captions is intentional
    return (f'<div class="caption clip" id="cap-{idx:02d}" data-layout-allow-overlap '
            f'data-start="{cap["start"]}" data-duration="{cap["duration"]}" data-track-index="{track}">'
            f'<div class="cap-inner"><div class="box"><div class="txt">{text}</div></div></div></div>')

def scene_html(s):
    svg = BG_MAP[s["bg"]]().strip()
    # Backgrounds are decorative — captions may sit above them intentionally.
    return (f'<div class="scene clip" id="scene-{s["id"]}" data-layout-allow-overlap '
            f'data-start="{s["start"]}" data-duration="{round(s["end"]-s["start"],3)}" data-track-index="1">'
            f'<div class="scene-inner">{svg}</div></div>')

# Chapter label: A1 = 파트 1 · 문제, A2 = 파트 2 · 시간
chapters = [
    {"id":"ch1", "start": 0.0, "end": 45.76, "label": "PART 1 · 불규칙한 수면"},
    {"id":"ch2", "start": 45.76, "end": 120.118, "label": "PART 2 · 몇 시에 자야 할까"},
]

scenes_html = "\n      ".join(scene_html(s) for s in SCENES)
caps_html = "\n      ".join(caption_html(c, i+1) for i, c in enumerate(CAPS))
chapters_html = "\n      ".join(
    f'<div class="chapter clip" id="{c["id"]}" data-start="{c["start"]}" data-duration="{round(c["end"]-c["start"],3)}" data-track-index="4"><div class="chapter-inner"><span class="dot"></span>{c["label"]}</div></div>'
    for c in chapters
)

# Timeline JS: fade in each scene at start over 0.25s and fade out over 0.25s at end;
# fade each caption in/out (0.2s ease).
tl_lines = []
tl_lines.append("      // Scene fades (opacity 0 → 1 in, 1 → 0 out) on inner wrapper (clip on outer handles visibility)")
for s in SCENES:
    sel = f'"#scene-{s["id"]} .scene-inner"'
    end_t = round(s["end"]-0.28, 3)
    tl_lines.append(f'      tl.fromTo({sel}, {{opacity:0}}, {{opacity:1, duration:0.28, ease:"power1.out"}}, {s["start"]});')
    tl_lines.append(f'      tl.to({sel}, {{opacity:0, duration:0.28, ease:"power1.in"}}, {end_t});')
    tl_lines.append(f'      tl.set({sel}, {{opacity:0}}, {s["end"]});')
tl_lines.append("      // Caption fades")
for i, c in enumerate(CAPS):
    sel = f'"#cap-{i+1:02d} .cap-inner"'
    end_t = round(c["end"]-0.20, 3)
    tl_lines.append(f'      tl.fromTo({sel}, {{opacity:0, y:8}}, {{opacity:1, y:0, duration:0.22, ease:"sine.out"}}, {c["start"]});')
    tl_lines.append(f'      tl.to({sel}, {{opacity:0, duration:0.20, ease:"sine.in"}}, {end_t});')
    tl_lines.append(f'      tl.set({sel}, {{opacity:0}}, {c["end"]});')
tl_lines.append("      // Chapter labels")
for c in chapters:
    sel = f'"#{c["id"]} .chapter-inner"'
    end_t = round(c["end"]-0.4, 3)
    tl_lines.append(f'      tl.fromTo({sel}, {{opacity:0}}, {{opacity:0.85, duration:0.4}}, {c["start"]});')
    tl_lines.append(f'      tl.to({sel}, {{opacity:0, duration:0.4}}, {end_t});')
    tl_lines.append(f'      tl.set({sel}, {{opacity:0}}, {c["end"]});')

tl_js = "\n".join(tl_lines)

HTML = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
{CSS}
    </style>
  </head>
  <body>
    <div id="root"
         data-composition-id="main"
         data-start="0"
         data-duration="{DUR}"
         data-width="1920"
         data-height="1080">

      {scenes_html}

      {chapters_html}

      {caps_html}

      <audio id="narration" class="clip"
             data-start="0" data-duration="{DUR}" data-track-index="0"
             src="public/narration.wav" preload="auto"></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{paused: true, defaults: {{ease:"power2.out"}}}});

{tl_js}

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Wrote index.html · {len(HTML)} chars · {len(SCENES)} scenes · {len(CAPS)} captions · {DUR}s")
