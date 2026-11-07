"""Live cards and the daily quote for the profile README.

    python scripts/cards.py live dist        # profile scan + contribution graph (needs GITHUB_TOKEN + Pillow)
    python scripts/cards.py quote README.md  # rewrite the quote block between the quote markers

Each card is a standalone animated SVG. Base styles are the final state, so a
renderer without CSS animation (or with reduced motion) still shows the card.
The quote is plain Markdown so it reads like normal text on the profile.
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

LANGUAGES = "Python · TypeScript · JavaScript"
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
]


QUOTE_START, QUOTE_END = "<!-- quote:start -->", "<!-- quote:end -->"


def quote_markdown(today=None):
    today = today or datetime.date.today()
    text, author = QUOTES[today.toordinal() % len(QUOTES)]
    return f"> {text}\n>\n> — {author}"


def update_quote(readme):
    body = readme.read_text(encoding="utf-8")
    head, rest = body.split(QUOTE_START, 1)
    _, tail = rest.split(QUOTE_END, 1)
    new = f"{head}{QUOTE_START}\n{quote_markdown()}\n{QUOTE_END}{tail}"
    if new != body:
        readme.write_text(new, encoding="utf-8")
    print(f"{readme}: {'updated' if new != body else 'unchanged'}")


# ------------------------------------------------------------------ main

def main():
    mode, target = sys.argv[1], Path(sys.argv[2])
    if mode == "quote":
        update_quote(target)
        return
    target.mkdir(parents=True, exist_ok=True)
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
        "scan.svg": scan(user, stats),
        "contrib.svg": contrib(cal["weeks"], cal["totalContributions"]),
    }
    for name, content in cards.items():
        (target / name).write_text(content, encoding="utf-8")
        print(f"{target / name}: {len(content) // 1024} KB")


if __name__ == "__main__":
    main()
