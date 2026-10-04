"""Aurora-style animated cards for the profile README (GitSkins look).

    python scripts/cards.py live dist      # hero, scan, contrib, quote: needs GITHUB_TOKEN + Pillow
    python scripts/cards.py static assets  # wordmark, tech stack: fetches Simple Icons once

Every card is a standalone animated SVG. Base styles are the final state, so a
renderer without CSS animation (or with reduced motion) still shows the card.
"""

import base64
import datetime
import io
import json
import os
import random
import sys
import textwrap
import urllib.request
from html import escape
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "UtkarshOver9000")
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
TEAL, MINT, INK, SOFT = "#2dd4bf", "#5eead4", "#e6fffa", "#99f6e4"

LANGUAGES = "Python · C++ · C · Java · JS · TS"
FOCUS = "ML · Security · Energy"
STATUS = "Building · Learning · Shipping"

BASE_CSS = f"""
text{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.label{{font:700 12px {SANS};letter-spacing:4px;fill:{MINT}}}
.orb{{animation:drift 14s ease-in-out infinite alternate}}
.orb2{{animation-duration:18s;animation-direction:alternate-reverse}}
.cursor{{animation:blink 1s steps(1) infinite}}
.rise{{animation:rise .7s ease-out both}}
@keyframes drift{{to{{transform:translate(60px,20px)}}}}
@keyframes blink{{50%{{opacity:0;fill-opacity:0}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


def pct(t, d):
    return f"{100 * t / d:.3f}%"


def svg(w, h, aria, css, inner, defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(aria)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b2a2b"/><stop offset=".55" stop-color="#0a1b1f"/><stop offset="1" stop-color="#0f2a36"/></linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{MINT}" stroke-opacity=".05"/></pattern>
  <clipPath id="clip"><rect width="{w}" height="{h}" rx="16"/></clipPath>
  {defs}
</defs>
<style>{BASE_CSS}{css}</style>
<g clip-path="url(#clip)">
{inner}
</g>
</svg>
"""


def orbs(w, h):
    return f"""<rect width="{w}" height="{h}" fill="url(#bg)"/>
<circle class="orb" cx="120" cy="10" r="120" fill="#14b8a6" opacity=".45" filter="url(#blur)"/>
<circle class="orb orb2" cx="{w * .65:.0f}" cy="{h}" r="130" fill="#3b82f6" opacity=".35" filter="url(#blur)"/>
<circle class="orb" cx="{w - 20}" cy="{h // 2}" r="90" fill="#2dd4bf" opacity=".3" filter="url(#blur)"/>"""


def aurora(w, h, aria, body, css="", defs=""):
    inner = f"""{orbs(w, h)}
<rect x="20" y="20" width="{w - 40}" height="{h - 40}" rx="14" fill="#0a1f22" fill-opacity=".55" stroke="{TEAL}" stroke-opacity=".35"/>
{body}
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{TEAL}" stroke-opacity=".45"/>"""
    return svg(w, h, aria, css, inner, defs)


def terminal(w, h, title, aria, body, css="", defs="", live=False):
    badge = ""
    if live:
        badge = (f'<circle class="cursor" cx="{w - 70}" cy="20" r="4" fill="{TEAL}"/>'
                 f'<text x="{w - 58}" y="24" class="mono" font-size="11" font-weight="700" letter-spacing="2" fill="{MINT}">LIVE</text>')
    inner = f"""{orbs(w, h)}
<rect width="{w}" height="{h}" fill="url(#grid)"/>
<rect width="{w}" height="40" fill="#0b1517" fill-opacity=".92"/>
<path d="M0 40.5H{w}" stroke="{TEAL}" stroke-opacity=".4"/>
<circle cx="22" cy="20" r="6" fill="#ff5f57"/><circle cx="42" cy="20" r="6" fill="#febc2e"/><circle cx="62" cy="20" r="6" fill="#28c840"/>
<text x="{w / 2}" y="25" text-anchor="middle" class="mono" font-size="13" fill="{MINT}">{escape(title)}</text>
{badge}
{body}
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{TEAL}" stroke-opacity=".55"/>"""
    return svg(w, h, aria, css, inner, defs)


# --------------------------------------------------------------- wordmark

FONT = {
    "U": ["1...1", "1...1", "1...1", "1...1", "1...1", "1...1", ".111."],
    "T": ["11111", "..1..", "..1..", "..1..", "..1..", "..1..", "..1.."],
    "K": ["1...1", "1..1.", "1.1..", "11...", "1.1..", "1..1.", "1...1"],
    "A": [".111.", "1...1", "1...1", "11111", "1...1", "1...1", "1...1"],
    "R": ["1111.", "1...1", "1...1", "1111.", "1.1..", "1..1.", "1...1"],
    "S": [".1111", "1....", "1....", ".111.", "....1", "....1", "1111."],
    "H": ["1...1", "1...1", "1...1", "11111", "1...1", "1...1", "1...1"],
}


def wordmark(text="UTKARSH"):
    w, h, pitch, size = 860, 280, 19, 15
    cols = len(text) * 6 - 1
    x0, y0 = (w - (cols * pitch - (pitch - size))) // 2, 80
    deep, mid, top = [], [], []
    for li, ch in enumerate(text):
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit != "1":
                    continue
                col = li * 6 + c
                x, y = x0 + col * pitch, y0 + r * pitch
                drop = 0.2 + li * 0.16 + r * 0.035
                wave = drop + 0.8 + col * 0.05
                tile = f'width="{size}" height="{size}" rx="3"'
                deep.append(f'<rect x="{x + 7}" y="{y + 7}" {tile} style="animation-delay:{drop:.2f}s"/>')
                mid.append(f'<rect x="{x + 3.5}" y="{y + 3.5}" {tile} style="animation-delay:{drop:.2f}s"/>')
                top.append(f'<rect x="{x}" y="{y}" {tile} style="animation-delay:{drop:.2f}s,{wave:.2f}s"/>')
    css = f"""
.deep rect,.mid rect{{animation:drop .55s cubic-bezier(.2,.9,.3,1.25) both}}
.top rect{{fill:{TEAL};animation:drop .55s cubic-bezier(.2,.9,.3,1.25) both,wave 4s ease-in-out infinite}}
@keyframes drop{{from{{opacity:0;transform:translateY(-34px)}}}}
@keyframes wave{{0%,60%,100%{{fill:{TEAL}}}25%{{fill:#ecfeff}}}}
.tag{{animation:rise .8s ease-out 1.6s both}}
"""
    body = f"""
<g class="deep" fill="#06302c">{''.join(deep)}</g>
<g class="mid" fill="#0f766e">{''.join(mid)}</g>
<g class="top">{''.join(top)}</g>
<text class="mono tag" x="{w / 2}" y="{y0 + 7 * pitch + 44}" text-anchor="middle" font-size="15" fill="{MINT}">&gt; ml · security · energy — always over 9000<tspan class="cursor">_</tspan></text>"""
    return terminal(w, h, "utkarshover9000@github: ~$ ./wordmark.sh --name", text, body, css)


# ------------------------------------------------------------ tech stack

STACK = [
    ("LANGUAGES", [("python", "Python", "#5a9fd4"), ("cplusplus", "C++", "#659ad2"), ("c", "C", "#a8b9cc"),
                   ("openjdk", "Java", "#f89820"), ("javascript", "JavaScript", "#f7df1e"), ("typescript", "TypeScript", "#4a90e2")]),
    ("ML & DATA", [("pytorch", "PyTorch", "#ee4c2c"), ("tensorflow", "TensorFlow", "#ff6f00"), ("scikitlearn", "scikit-learn", "#f7931e"),
                   ("numpy", "NumPy", "#4dabcf"), ("pandas", "pandas", "#e70488"), ("jupyter", "Jupyter", "#f37626")]),
    ("BUILD & SHIP", [("fastapi", "FastAPI", "#05b3a0"), ("react", "React", "#61dafb"), ("nextdotjs", "Next.js", "#ffffff"),
                      ("docker", "Docker", "#2496ed"), ("git", "Git", "#f05032"), ("linux", "Linux", "#fcc624")]),
]


def icon_path(slug):
    url = f"https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{slug}.svg"
    raw = urllib.request.urlopen(url, timeout=30).read().decode()
    return raw.split(' d="', 1)[1].split('"', 1)[0]


def tech_stack():
    w, h, tile, gap, x0 = 860, 440, 76, 26, 206
    parts, n = [], 0
    for gi, (group, items) in enumerate(STACK):
        y = 104 + gi * 108
        parts.append(f'<text class="mono rise" x="48" y="{y + 42}" font-size="11" font-weight="700" letter-spacing="2" fill="{MINT}" style="animation-delay:{.2 + gi * .3:.1f}s">{escape(group)}</text>')
        for i, (slug, name, color) in enumerate(items):
            x = x0 + i * (tile + gap)
            d = icon_path(slug)
            delay = 0.3 + n * 0.07
            parts.append(f"""<g class="tile" style="animation-delay:{delay:.2f}s,{delay + 1:.2f}s">
  <rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="16" fill="#0b2624" stroke="{color}" stroke-opacity=".45"/>
  <rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="16" fill="{color}" opacity=".07"/>
  <path transform="translate({x + 20} {y + 20}) scale(1.5)" d="{d}" fill="{color}"/>
  <text x="{x + tile / 2}" y="{y + tile + 17}" text-anchor="middle" font-size="12" font-weight="600" fill="#ccfbf1">{escape(name)}</text>
</g>""")
            n += 1
    css = """
.tile{animation:pop .6s cubic-bezier(.2,.9,.3,1.3) both,float 5s ease-in-out infinite}
@keyframes pop{from{opacity:0;transform:translateY(14px) scale(.9)}}
@keyframes float{50%{transform:translateY(-3px)}}
"""
    body = f"""
<text x="48" y="66" font-size="26" font-weight="800" fill="{INK}">Tech Stack</text>
<text class="mono" x="{w - 48}" y="64" text-anchor="end" font-size="13" font-weight="600" fill="{MINT}">&gt; stack.scan<tspan class="cursor"> _</tspan></text>
{''.join(parts)}"""
    names = ", ".join(n for _, items in STACK for _, n, _ in items)
    return aurora(w, h, f"Tech stack: {names}", body, css)


# ------------------------------------------------------------------ data

QUERY = """{ user(login:"%s"){ login name bio websiteUrl avatarUrl followers{totalCount}
  repositories(ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC, first:100){ totalCount nodes{ stargazerCount } }
  contributionsCollection{ contributionCalendar{ totalContributions
    weeks{ contributionDays{ contributionCount contributionLevel weekday } } } } } }"""


def fetch_profile():
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY % USER}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-cards"},
    )
    user = json.load(urllib.request.urlopen(req, timeout=60))["data"]["user"]
    sep = "&" if "?" in user["avatarUrl"] else "?"
    raw = urllib.request.urlopen(f"{user['avatarUrl']}{sep}s=240", timeout=60).read()
    user["avatar_raw"] = raw
    from PIL import Image

    buf = io.BytesIO()
    Image.open(io.BytesIO(raw)).convert("RGB").save(buf, "JPEG", quality=86)
    user["avatar"] = buf.getvalue()
    return user


def data_uri(img):
    kind = "image/jpeg" if img[:3] == b"\xff\xd8\xff" else "image/png"
    return f"data:{kind};base64,{base64.b64encode(img).decode()}"


def contact(user):
    site = (user.get("websiteUrl") or "").split("://")[-1].removeprefix("www.").rstrip("/")
    return site or f"github.com/{user['login']}"


# ------------------------------------------------------------------ hero

def hero(user):
    w, h = 860, 250
    name = user["name"] or user["login"]
    bio = textwrap.wrap(user["bio"] or "", 52)[:2]
    bio_lines = "".join(f'<tspan x="206" dy="{0 if i == 0 else 22}">{escape(line)}</tspan>' for i, line in enumerate(bio))
    css = f"""
.spin{{animation:spin 18s linear infinite;transform-origin:110px 125px}}
.spin2{{animation:spin 26s linear infinite reverse;transform-origin:762px 118px}}
.pulse{{animation:pulse 2.6s ease-in-out infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes pulse{{50%{{opacity:.55}}}}
"""
    defs = '<clipPath id="av"><circle cx="110" cy="125" r="60"/></clipPath>'
    body = f"""
<circle cx="110" cy="125" r="70" fill="none" stroke="{TEAL}" stroke-opacity=".25" stroke-width="2"/>
<circle class="spin" cx="110" cy="125" r="70" fill="none" stroke="{MINT}" stroke-width="2.5" stroke-dasharray="60 380" stroke-linecap="round"/>
<image href="{data_uri(user['avatar'])}" x="50" y="65" width="120" height="120" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>
<circle cx="110" cy="125" r="60" fill="none" stroke="{TEAL}" stroke-width="2"/>
<text class="mono rise" x="208" y="74" font-size="14" font-weight="700" letter-spacing="2" fill="{MINT}">@{escape(user['login'].lower())}</text>
<text class="rise" x="204" y="126" font-size="46" font-weight="800" fill="{INK}" style="animation-delay:.15s">{escape(name)}</text>
<text class="rise" x="206" y="158" font-size="16" fill="{SOFT}" style="animation-delay:.3s">{bio_lines}</text>
<text class="mono rise" x="206" y="{158 + 22 * len(bio) + 18}" font-size="13" fill="{MINT}" style="animation-delay:.45s">&gt; {STATUS.lower()}<tspan class="cursor">_</tspan></text>
<g opacity=".55" fill="none" stroke="{MINT}"><circle cx="762" cy="118" r="62" stroke-opacity=".25"/><circle cx="762" cy="118" r="46" stroke-opacity=".35"/></g>
<g class="spin2"><circle cx="824" cy="118" r="4" fill="{MINT}"/></g>
<text class="pulse" x="762" y="120" text-anchor="middle" font-size="30" font-weight="800" fill="{MINT}">9000+</text>
<text x="762" y="142" text-anchor="middle" font-size="10" font-weight="700" letter-spacing="3" fill="{MINT}">POWER LEVEL</text>"""
    return aurora(w, h, f"{name}: {user['bio'] or ''}", body, css, defs)


# ------------------------------------------------------------------ scan

def ascii_rows(img, x, y, size, n=46):
    from PIL import Image

    im = Image.open(io.BytesIO(img)).convert("RGB").resize((n, n), Image.LANCZOS)
    ramp = " .:-=+*#%@"
    step = size / n
    out = []
    for r in range(n):
        spans, color, buf = [], None, ""
        for c in range(n):
            px = im.getpixel((c, r))
            lum = ((0.2126 * px[0] + 0.7152 * px[1] + 0.0722 * px[2]) / 255) ** 0.6
            ch = ramp[min(len(ramp) - 1, int(lum * len(ramp) * 1.15))]
            col = "#" + "".join(f"{min(255, int(v * 1.35) + 40) // 24 * 24 + 8:02x}" for v in px)
            if col != color and buf:
                spans.append(f'<tspan fill="{color}">{buf}</tspan>')
                buf = ""
            color = col
            buf += " " if ch == " " else escape(ch)
        spans.append(f'<tspan fill="{color}">{buf}</tspan>')
        out.append(f'<text class="mono" x="{x}" y="{y + (r + 1) * step - 1.2:.2f}" textLength="{size}" '
                   f'lengthAdjust="spacing" font-size="{step * 1.12:.2f}" font-weight="700">{"".join(spans)}</text>')
    return "\n".join(out)


def scan(user, stats):
    w, h = 860, 480
    ax, ay, a = 46, 92, 268
    rows = [
        ("Subject", user["name"] or user["login"]),
        ("Handle", "@" + user["login"].lower()),
        *[("Role" if i == 0 else "", line) for i, line in enumerate(textwrap.wrap(user["bio"] or "-", 38)[:2])],
        ("Status", STATUS),
        ("Languages", LANGUAGES),
        ("Focus", FOCUS),
        ("Repositories", stats["repos"]),
        ("Contributions", stats["contributions"]),
        ("Stars", stats["stars"]),
        ("Followers", user["followers"]["totalCount"]),
        ("Active days", stats["active"]),
        ("Contact", contact(user)),
    ]
    info = []
    for i, (key, value) in enumerate(rows):
        y = 104 + i * 26
        leader = f'<path d="M466 {y - 4}H540" stroke="{MINT}" stroke-opacity=".35" stroke-dasharray="2 4"/>' if key else ""
        info.append(f"""<g class="rise" style="animation-delay:{.4 + i * .12:.2f}s">
  <text x="376" y="{y}" font-size="13.5" font-weight="700" fill="{MINT}">{escape(key)}</text>{leader}
  <text x="552" y="{y}" font-size="13" fill="{INK}">{escape(str(value))}</text>
</g>""")
    css = f"""
.ascii{{animation:ascii 12s ease-in-out infinite}}
@keyframes ascii{{0%,22%{{opacity:1}}32%,86%{{opacity:0}}96%,100%{{opacity:1}}}}
.beam{{animation:beam 3s linear infinite}}
@keyframes beam{{from{{transform:translateY(-40px)}}to{{transform:translateY({a}px)}}}}
.bar{{transform-box:fill-box;transform-origin:left;animation:bar 12s ease-in-out infinite}}
@keyframes bar{{0%{{transform:scaleX(.02)}}28%,100%{{transform:scaleX(1)}}}}
.resolving{{animation:ascii 12s ease-in-out infinite}}
.resolved{{animation:resolved 12s ease-in-out infinite}}
@keyframes resolved{{0%,22%{{opacity:0}}32%,86%{{opacity:1}}96%,100%{{opacity:0}}}}
"""
    defs = f"""<clipPath id="pic"><rect x="{ax}" y="{ay}" width="{a}" height="{a}" rx="10"/></clipPath>
<linearGradient id="beamg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MINT}" stop-opacity="0"/><stop offset=".5" stop-color="{MINT}" stop-opacity=".45"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></linearGradient>"""
    hud = "".join(
        f'<path d="M{x} {y + dy * 18}V{y}H{x + dx * 18}" fill="none" stroke="{MINT}" stroke-width="2.5"/>'
        for x, y, dx, dy in [(ax - 8, ay - 8, 1, 1), (ax + a + 8, ay - 8, -1, 1), (ax - 8, ay + a + 8, 1, -1), (ax + a + 8, ay + a + 8, -1, -1)]
    )
    body = f"""
<rect x="20" y="56" width="330" height="404" rx="14" fill="#06191b" fill-opacity=".6" stroke="{TEAL}" stroke-opacity=".5"/>
<rect x="362" y="56" width="478" height="404" rx="14" fill="#06191b" fill-opacity=".6" stroke="{TEAL}" stroke-opacity=".5"/>
<text class="mono" x="36" y="78" font-size="11" font-weight="700" letter-spacing="2" fill="{MINT}">VISUAL.MAP</text>
<text class="mono" x="378" y="78" font-size="11" font-weight="700" letter-spacing="2" fill="{MINT}">SYSTEM.INFO</text>
<g clip-path="url(#pic)">
  <image href="{data_uri(user['avatar'])}" x="{ax}" y="{ay}" width="{a}" height="{a}" preserveAspectRatio="xMidYMid slice"/>
  <rect x="{ax}" y="{ay}" width="{a}" height="{a}" fill="{TEAL}" opacity=".08"/>
  <g class="ascii"><rect x="{ax}" y="{ay}" width="{a}" height="{a}" fill="#041213"/>{ascii_rows(user['avatar'], ax, ay, a)}</g>
  <rect class="beam" x="{ax}" y="{ay}" width="{a}" height="40" fill="url(#beamg)"/>
</g>
{hud}
<text class="mono resolving" x="{ax}" y="{ay + a + 34}" font-size="11" fill="{MINT}">&gt; resolving portrait...</text>
<text class="mono resolved" x="{ax}" y="{ay + a + 34}" font-size="11" fill="{MINT}">&gt; subject identified ✓</text>
<rect x="{ax}" y="{ay + a + 44}" width="{a}" height="5" rx="2.5" fill="{MINT}" opacity=".15"/>
<rect class="bar" x="{ax}" y="{ay + a + 44}" width="{a}" height="5" rx="2.5" fill="{MINT}"/>
{''.join(info)}"""
    return terminal(w, h, f"{user['login'].lower()}@github ~ $ ./profile-scan --live", "Profile scan", body, css, defs, live=True)


# --------------------------------------------------------- contributions

LEVEL = {"FIRST_QUARTILE": "#1d6b62", "SECOND_QUARTILE": "#23a08f", "THIRD_QUARTILE": "#2dd4bf", "FOURTH_QUARTILE": "#99f6e4"}
SHIP = (f'<path d="M0 -14L7 2L14 6L14 10L4 8L0 12L-4 8L-14 10L-14 6L-7 2Z" fill="#60a5fa"/>'
        f'<path d="M0 -8L3 1H-3Z" fill="{INK}"/>'
        f'<path d="M-6 6H6" stroke="{MINT}" stroke-width="2"/>'
        '<path class="flame" d="M-3 12L0 22L3 12Z" fill="#fb923c"/>')
ERASER = ('<g class="wiggle"><rect x="-11" y="-6" width="22" height="12" rx="2.5" fill="#f9a8d4"/>'
          '<rect x="3" y="-6" width="8" height="12" rx="2" fill="#60a5fa"/>'
          '<rect x="-11" y="-6" width="22" height="12" rx="2.5" fill="none" stroke="#fff" stroke-opacity=".5"/></g>')


def contrib(weeks, total):
    w, h, pitch, size = 860, 330, 14, 11
    x0 = (w - len(weeks) * pitch) // 2
    y0, ship_y = 112, 274
    cells, active_cols = [], []
    for c, week in enumerate(weeks):
        rows = []
        for day in week["contributionDays"]:
            r = day["weekday"]
            x, y = x0 + c * pitch, y0 + r * pitch
            cells.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="2.5" fill="#123a37" fill-opacity=".7"/>')
            if day["contributionCount"]:
                rows.append((r, LEVEL.get(day["contributionLevel"], TEAL)))
        if rows:
            active_cols.append((c, rows))

    days = sum(len(rows) for _, rows in active_cols)
    T, tail = 1.0, 2.6
    D = max(len(active_cols) * T + tail, 4)
    regrow0, regrow1 = D - 1.4, D - 0.4
    css, live, lasers, dust, counters = [], [], [], [], []
    ship_frames = []
    rnd = random.Random(7)
    done = 0
    first_x = x0 + (active_cols[0][0] if active_cols else 0) * pitch + size / 2
    ship_frames.append(f"0%{{transform:translate({first_x:.1f}px,{ship_y}px)}}")
    eraser_frames = [f"0%{{opacity:0;transform:translate({first_x:.1f}px,{y0}px)}}"]
    prev_x = first_x
    for j, (c, rows) in enumerate(active_cols):
        s = j * T
        xc = x0 + c * pitch + size / 2
        rmin, rmax = min(r for r, _ in rows), max(r for r, _ in rows)
        ytop, ybot = y0 + rmin * pitch + size / 2, y0 + rmax * pitch + size / 2
        ship_frames += [f"{pct(s, D)}{{transform:translate({prev_x:.1f}px,{ship_y}px)}}",
                        f"{pct(s + .35, D)}{{transform:translate({xc:.1f}px,{ship_y}px)}}"]
        prev_x = xc
        eraser_frames += [f"{pct(s + .43, D)}{{opacity:0;transform:translate({xc:.1f}px,{ytop:.1f}px)}}",
                          f"{pct(s + .45, D)}{{opacity:1;transform:translate({xc:.1f}px,{ytop:.1f}px)}}",
                          f"{pct(s + .9, D)}{{opacity:1;transform:translate({xc:.1f}px,{ybot:.1f}px)}}",
                          f"{pct(s + .95, D)}{{opacity:0;transform:translate({xc:.1f}px,{ybot:.1f}px)}}"]
        css.append(f"@keyframes l{j}{{0%,{pct(s + .34, D)}{{opacity:0}}{pct(s + .37, D)}{{opacity:1}}{pct(s + .5, D)}{{opacity:1}}{pct(s + .58, D)}{{opacity:0}}100%{{opacity:0}}}}")
        lasers.append(f'<rect x="{xc - 1:.1f}" y="{ytop:.1f}" width="2" height="{ship_y - 16 - ytop:.1f}" rx="1" fill="#facc15" '
                      f'style="opacity:0;animation:l{j} {D:.2f}s linear infinite"/>')
        for r, color in rows:
            te = s + .45 + .45 * ((r - rmin) / max(1, rmax - rmin))
            k = f"c{c}_{r}"
            css.append(f"@keyframes {k}{{0%,{pct(te, D)}{{opacity:1;transform:scale(1)}}{pct(te + .12, D)}{{opacity:0;transform:scale(.2)}}"
                       f"{pct(regrow0, D)}{{opacity:0;transform:scale(.2)}}{pct(regrow1, D)},100%{{opacity:1;transform:scale(1)}}}}")
            live.append(f'<rect class="cell" x="{x0 + c * pitch}" y="{y0 + r * pitch}" width="{size}" height="{size}" rx="2.5" '
                        f'fill="{color}" style="animation:{k} {D:.2f}s linear infinite"/>')
            cx, cy = x0 + c * pitch + size / 2, y0 + r * pitch + size / 2
            for p in range(5):
                dx, dy = rnd.uniform(-16, 16), rnd.uniform(-14, 10)
                kd = f"d{c}_{r}_{p}"
                css.append(f"@keyframes {kd}{{0%,{pct(te, D)}{{opacity:0;transform:translate(0,0)}}{pct(te + .03, D)}{{opacity:1}}"
                           f"{pct(te + .55, D)}{{opacity:0;transform:translate({dx:.1f}px,{dy:.1f}px)}}100%{{opacity:0}}}}")
                dust.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rnd.uniform(.8, 1.8):.1f}" fill="#ccfbf1" style="opacity:0;animation:{kd} {D:.2f}s linear infinite"/>')
        start = s + .95
        end = (j + 1) * T + .95 if j + 1 < len(active_cols) else regrow1
        done += len(rows)
        css.append(f"@keyframes n{j}{{0%,{pct(start - .01, D)}{{opacity:0}}{pct(start, D)},{pct(end - .01, D)}{{opacity:1}}{pct(end, D)},100%{{opacity:0}}}}")
        counters.append(f'<text class="mono count" x="812" y="66" style="opacity:0;animation:n{j} {D:.2f}s linear infinite">{done} / {days} days erased</text>')
    first_end = .95 if active_cols else D
    css.append(f"@keyframes n_{{0%,{pct(first_end - .01, D)}{{opacity:1}}{pct(first_end, D)},{pct(regrow1 - .01, D)}{{opacity:0}}{pct(regrow1, D)},100%{{opacity:1}}}}")
    counters.insert(0, f'<text class="mono count" x="812" y="66" style="animation:n_ {D:.2f}s linear infinite">0 / {days} days erased</text>')
    ship_frames += [f"{pct(regrow0, D)}{{transform:translate({prev_x:.1f}px,{ship_y}px)}}",
                    f"{pct(regrow1, D)},100%{{transform:translate({first_x:.1f}px,{ship_y}px)}}"]
    eraser_frames.append("100%{opacity:0}")

    stars = "".join(
        f'<circle class="tw" cx="{rnd.uniform(40, w - 40):.0f}" cy="{rnd.uniform(222, h - 34):.0f}" r="{rnd.uniform(.5, 1.3):.1f}" '
        f'fill="#fff" style="animation-delay:{rnd.uniform(0, 3):.1f}s"/>' for _ in range(40))
    style = f"""
.cell{{transform-box:fill-box;transform-origin:center}}
.count{{font-size:13px;font-weight:700;fill:{MINT};text-anchor:end}}
.ship{{animation:ship {D:.2f}s ease-in-out infinite}}
@keyframes ship{{{''.join(ship_frames)}}}
.eraser{{opacity:0;animation:eraser {D:.2f}s linear infinite}}
@keyframes eraser{{{''.join(eraser_frames)}}}
.wiggle{{animation:wiggle .18s ease-in-out infinite alternate}}
@keyframes wiggle{{from{{transform:rotate(-34deg)}}to{{transform:rotate(-16deg)}}}}
.flame{{animation:blink .25s steps(1) infinite}}
.tw{{animation:blink 2.4s steps(1) infinite}}
{''.join(css)}
"""
    body = f"""
<text x="48" y="66" font-size="26" font-weight="800" fill="{INK}">Contribution Activity</text>
<text x="48" y="90" font-size="13" font-weight="600" letter-spacing=".5" fill="{MINT}">{total} contributions in the last year · ship + eraser mode</text>
{''.join(counters)}
{stars}
{''.join(cells)}
{''.join(live)}
{''.join(lasers)}
{''.join(dust)}
<g class="eraser">{ERASER}</g>
<g class="ship" style="transform:translate({first_x:.1f}px,{ship_y}px)">{SHIP}</g>"""
    return aurora(w, h, f"Contribution graph: {total} contributions, erased by a ship and an eraser", body, style)


# ----------------------------------------------------------------- quote

QUOTES = [
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("All models are wrong, but some are useful.", "George Box"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Program testing can be used to show the presence of bugs, but never to show their absence.", "Edsger W. Dijkstra"),
    ("The first principle is that you must not fool yourself, and you are the easiest person to fool.", "Richard Feynman"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("If you torture the data long enough, it will confess.", "Ronald Coase"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Security is a process, not a product.", "Bruce Schneier"),
    ("In God we trust. All others must bring data.", "W. Edwards Deming"),
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Debugging is twice as hard as writing the code in the first place.", "Brian Kernighan"),
    ("Simple things should be simple, complex things should be possible.", "Alan Kay"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("Fix the cause, not the symptom.", "Steve Maguire"),
    ("Without data, you're just another person with an opinion.", "W. Edwards Deming"),
    ("Amateurs hack systems, professionals hack people.", "Bruce Schneier"),
    ("The most dangerous phrase in the language is: we've always done it this way.", "Grace Hopper"),
    ("It's harder to read code than to write it.", "Joel Spolsky"),
    ("Measuring programming progress by lines of code is like measuring aircraft building progress by weight.", "Bill Gates"),
    ("Truth can only be found in one place: the code.", "Robert C. Martin"),
    ("Correlation does not imply causation.", "Statistics 101"),
    ("It's over 9000!", "Vegeta"),
]


def quote():
    index = datetime.date.today().toordinal() % len(QUOTES)
    text, author = QUOTES[index]
    lines = textwrap.wrap(f"“{text}”", 58)
    w, h = 860, 150 + 34 * len(lines)
    spans = "".join(f'<tspan x="56" dy="{0 if i == 0 else 34}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    css = ".ring{animation:spin 24s linear infinite;transform-origin:770px 66px}@keyframes spin{to{transform:rotate(360deg)}}"
    body = f"""
<g class="ring" opacity=".35" fill="none" stroke="{MINT}"><circle cx="770" cy="66" r="30"/><circle cx="770" cy="66" r="18"/><circle cx="800" cy="66" r="3" fill="{MINT}"/></g>
<text class="label" x="56" y="58">DEV QUOTE</text>
<text class="mono" x="590" y="58" font-size="13" font-weight="600" fill="{MINT}">&gt; quote.random<tspan class="cursor"> _</tspan></text>
<text class="rise" x="56" y="98" font-size="24" font-weight="600" fill="{INK}">{spans}</text>
<text class="mono rise" x="56" y="{112 + 34 * len(lines)}" font-size="14" fill="{MINT}" style="animation-delay:.5s">— {escape(author)}</text>
<text class="mono" x="{w - 40}" y="{h - 12}" text-anchor="end" font-size="11" fill="{MINT}" opacity=".55">#{index + 1:02d} · refreshed daily</text>"""
    return aurora(w, h, f"Dev quote of the day: {text} by {author}", body, css)


# ------------------------------------------------------------------ main

def main():
    mode, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    if mode == "static":
        cards = {"wordmark.svg": wordmark(), "tech-stack.svg": tech_stack()}
    else:
        user = fetch_profile()
        cal = user["contributionsCollection"]["contributionCalendar"]
        days = [d for wk in cal["weeks"] for d in wk["contributionDays"]]
        stats = {
            "repos": user["repositories"]["totalCount"],
            "stars": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
            "contributions": cal["totalContributions"],
            "active": sum(1 for d in days if d["contributionCount"]),
        }
        cards = {
            "hero.svg": hero(user),
            "scan.svg": scan(user, stats),
            "contrib.svg": contrib(cal["weeks"], cal["totalContributions"]),
            "dev-quote.svg": quote(),
        }
    for name, content in cards.items():
        (out / name).write_text(content, encoding="utf-8")
        print(f"{out / name}: {len(content) // 1024} KB")


if __name__ == "__main__":
    main()
