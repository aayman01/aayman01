"""Generate assets/terminal.svg: an animated, looping terminal for the profile README.

Uses CSS animation only, so it plays inside a GitHub README <img>.
Edit `script` below, then run:  python3 scripts/make_terminal.py assets/terminal.svg
"""
import html, sys

OUT = sys.argv[1]
FS, LH = 15, 27              # font size, line height
CW = FS * 0.602              # monospace character width
X0, Y0 = 30, 82              # first text baseline
W = 880
LOOP = 17.0                  # seconds per loop

# (command, [output lines]) — typed one after another
script = [
    ("whoami", ["Aayman Alfee Rahman · Full-Stack Developer · Dhaka, Bangladesh"]),
    ("cat stack.ts", ["frontend  Next.js · React · TypeScript · Tailwind CSS",
                      "backend   NestJS · Node.js · PostgreSQL · Prisma · Drizzle"]),
    ("ls ~/shipped", ["saas/   headless-commerce/   payments/   sso/   offline-pos/"]),
    ("git push origin main", ["✓ Deployed to production. Ready for your next project."]),
]

PROMPT = "aayman@dev ~ $"
px = X0 + (len(PROMPT) + 1) * CW   # where typed commands start

rows = []      # (y, kind, text, start_s, type_s)
t, y = 0.6, Y0
for cmd, outs in script:
    type_s = 0.08 * len(cmd) + 0.25
    rows.append((y, "cmd", cmd, t, type_s)); t += type_s + 0.35; y += LH
    for o in outs:
        rows.append((y, "out", o, t, 0)); t += 0.18; y += LH
    t += 0.7
final_y, final_t = y, t
H = final_y + 30
assert final_t < LOOP - 2.5, final_t

pct = lambda s: f"{s / LOOP * 100:.3f}%"
css, body = [], []
fade_out = LOOP - 0.6

for i, (ry, kind, text, start, type_s) in enumerate(rows):
    esc = html.escape(text)
    if kind == "cmd":
        n = len(text)
        width = n * CW
        # prompt fades in at start
        css.append(f".p{i}{{opacity:0;animation:p{i} {LOOP}s infinite}}"
                   f"@keyframes p{i}{{0%,{pct(start-0.01)}{{opacity:0}}{pct(start)},{pct(fade_out)}{{opacity:1}}100%{{opacity:0}}}}")
        body.append(f'<text class="prompt p{i}" x="{X0}" y="{ry}">{PROMPT}</text>')
        body.append(f'<text class="cmd p{i}" x="{px:.1f}" y="{ry}">{esc}</text>')
        # cover (background + cursor) slides right in character steps, then leaves
        done = start + type_s
        css.append(
            f".c{i}{{animation:c{i} {LOOP}s infinite}}"
            f"@keyframes c{i}{{0%{{opacity:0;transform:translateX(0);animation-timing-function:step-end}}"
            f"{pct(start)}{{opacity:1;transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"{pct(done)}{{transform:translateX({width:.1f}px);animation-timing-function:step-end}}"
            f"{pct(done+0.3)}{{transform:translateX({W}px)}}"
            f"100%{{transform:translateX({W}px)}}}}")
        body.append(f'<g class="c{i}"><rect x="{px-1:.1f}" y="{ry-FS}" width="{W}" height="{LH}" fill="#0d0d0d"/>'
                    f'<rect class="blink" x="{px:.1f}" y="{ry-FS+2}" width="{CW:.1f}" height="{FS+3}" fill="#ffffff"/></g>')
    else:
        css.append(f".o{i}{{opacity:0;animation:o{i} {LOOP}s infinite}}"
                   f"@keyframes o{i}{{0%,{pct(start-0.01)}{{opacity:0}}{pct(start)},{pct(fade_out)}{{opacity:1}}100%{{opacity:0}}}}")
        cls = "ok" if text.startswith("✓") else "out"
        body.append(f'<text class="{cls} o{i}" x="{px:.1f}" y="{ry}">{esc}</text>')

# final idle prompt with blinking cursor
css.append(f".fin{{opacity:0;animation:fin {LOOP}s infinite}}"
           f"@keyframes fin{{0%,{pct(final_t-0.01)}{{opacity:0}}{pct(final_t)},{pct(fade_out)}{{opacity:1}}100%{{opacity:0}}}}")
body.append(f'<g class="fin"><text class="prompt" x="{X0}" y="{final_y}">{PROMPT}</text>'
            f'<rect class="blink" x="{px:.1f}" y="{final_y-FS+2}" width="{CW:.1f}" height="{FS+3}" fill="#ffffff"/></g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated terminal: whoami, stack, shipped work, git push">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:{FS}px;white-space:pre}}
.prompt{{fill:#737373}} .cmd{{fill:#ffffff;font-weight:600}} .out{{fill:#a3a3a3}} .ok{{fill:#ffffff;font-weight:600}}
.title{{fill:#737373;font-size:13px}}
.blink{{animation:blink 1s step-end infinite}} @keyframes blink{{50%{{opacity:0}}}}
{"".join(css)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important;transform:none!important}}g[class^="c"]{{display:none}}}}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0d0d0d" stroke="#262626" stroke-width="1.5"/>
<path d="M1 15a14 14 0 0 1 14-14h{W-30}a14 14 0 0 1 14 14v25H1z" fill="#161616"/>
<line x1="1" y1="40" x2="{W-1}" y2="40" stroke="#262626"/>
<circle cx="24" cy="20.5" r="6" fill="#e5e5e5"/><circle cx="44" cy="20.5" r="6" fill="#a3a3a3"/><circle cx="64" cy="20.5" r="6" fill="#525252"/>
<text class="title" x="{W/2}" y="25" text-anchor="middle">aayman — zsh — 88×24</text>
<defs><clipPath id="win"><rect x="2" y="41" width="{W-4}" height="{H-43}" rx="12"/></clipPath></defs>
<g clip-path="url(#win)">{"".join(body)}</g>
</svg>
'''
open(OUT, "w").write(svg)
print(f"{W}x{H}, loop {LOOP}s, last line at {final_t:.1f}s, {len(svg)} bytes")
