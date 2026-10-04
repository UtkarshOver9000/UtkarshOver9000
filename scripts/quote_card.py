"""Render the daily dev-quote card in the GitSkins aurora style.

Stdlib only, so the workflow needs no installs. The quote is picked by date,
so every run on the same day produces the same card.

    python scripts/quote_card.py dist/dev-quote.svg
"""

import datetime
import sys
import textwrap
from html import escape
from pathlib import Path

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

W = 860
WRAP = 58  # characters per line at 24px in the card's text column
LINE_H = 34


def render(quote: str, author: str, number: int) -> str:
    lines = textwrap.wrap(f"“{quote}”", WRAP)
    h = 150 + LINE_H * len(lines)
    text = "\n".join(
        f'<tspan x="56" dy="{0 if i == 0 else LINE_H}">{escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    author_y = 112 + LINE_H * len(lines)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="Dev quote of the day: {escape(quote)} by {escape(author)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b2a2b"/><stop offset=".55" stop-color="#0a1b1f"/><stop offset="1" stop-color="#0f2a36"/>
  </linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>
  <clipPath id="clip"><rect width="{W}" height="{h}" rx="16"/></clipPath>
</defs>
<style>
  .label {{ font: 700 12px 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Noto Sans', Helvetica, Arial, sans-serif; letter-spacing: 4px; fill: #5eead4; }}
  .cmd {{ font: 600 13px ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace; fill: #5eead4; }}
  .quote {{ font: 600 24px 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Noto Sans', Helvetica, Arial, sans-serif; fill: #e6fffa; }}
  .author {{ font: 500 14px ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace; fill: #5eead4; }}
  .meta {{ font: 500 11px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #5eead4; opacity: .55; }}
  .orb {{ animation: drift 14s ease-in-out infinite alternate; }}
  .orb2 {{ animation-duration: 18s; animation-direction: alternate-reverse; }}
  .cursor {{ animation: blink 1s steps(1) infinite; }}
  .reveal {{ animation: rise .9s ease-out both; }}
  .reveal2 {{ animation-delay: .5s; }}
  .ring {{ animation: spin 24s linear infinite; transform-origin: 770px 66px; }}
  @keyframes drift {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(60px, 20px); }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{h}" fill="url(#bg)"/>
  <circle class="orb" cx="120" cy="10" r="120" fill="#14b8a6" opacity=".45" filter="url(#blur)"/>
  <circle class="orb orb2" cx="560" cy="{h}" r="130" fill="#3b82f6" opacity=".35" filter="url(#blur)"/>
  <circle class="orb" cx="840" cy="{h // 2}" r="90" fill="#2dd4bf" opacity=".3" filter="url(#blur)"/>
  <rect x="24" y="22" width="{W - 48}" height="{h - 44}" rx="14" fill="#0a1f22" fill-opacity=".55" stroke="#2dd4bf" stroke-opacity=".35"/>
  <g class="ring" opacity=".35" fill="none" stroke="#5eead4">
    <circle cx="770" cy="66" r="30"/><circle cx="770" cy="66" r="18"/><circle cx="800" cy="66" r="3" fill="#5eead4"/>
  </g>
  <text class="label" x="56" y="58">DEV QUOTE</text>
  <text class="cmd" x="590" y="58">&gt; quote.random<tspan class="cursor"> _</tspan></text>
  <text class="quote reveal" x="56" y="98">{text}</text>
  <text class="author reveal reveal2" x="56" y="{author_y}">— {escape(author)}</text>
  <text class="meta" x="{W - 40}" y="{h - 12}" text-anchor="end">#{number:02d} · refreshed daily</text>
</g>
</svg>
"""


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "dist/dev-quote.svg")
    index = datetime.date.today().toordinal() % len(QUOTES)
    quote, author = QUOTES[index]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(quote, author, index + 1), encoding="utf-8")
    print(f"{out}: #{index + 1} {author}")


if __name__ == "__main__":
    main()
