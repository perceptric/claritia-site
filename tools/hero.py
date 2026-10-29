# Writes the hero's Catch picture (tools/out/hero.svg) for index.html.
# Visitors drift in from every side toward the Claritia bracket; the ones that fit turn emerald.
import math, random, os
random.seed(11)
C = 260
dots = []
for i in range(46):
    a = random.uniform(0, 2 * math.pi)
    r0 = random.uniform(175, 245)
    x, y = C + r0 * math.cos(a), C + r0 * math.sin(a)
    fit = i % 4 == 0
    r1 = random.uniform(30, 70) if fit else random.uniform(128, 150)
    tx, ty = C + r1 * math.cos(a), C + r1 * math.sin(a)
    dots.append('<circle class="v%s" cx="%.1f" cy="%.1f" r="%s" style="--i:%d;--dx:%.1fpx;--dy:%.1fpx"/>' % (
        " fit" if fit else "", x, y, "3.2" if fit else "2.6", i, tx - x, ty - y))
L = 34
br = []
for (x, y, dx, dy) in [(150, 150, 1, 1), (370, 150, -1, 1), (370, 370, -1, -1), (150, 370, 1, -1)]:
    br.append('<path class="bk" d="M%d %d V%d H%d"/>' % (x, y + dy * L, y, x + dx * L))
corners = [("01", "Capture", 150, 150, -1, -1, 0), ("02", "Know", 370, 150, 1, -1, 1.44), ("03", "Route", 370, 370, 1, 1, 2.88), ("04", "Book", 150, 370, -1, 1, 4.32)]
cs = []
for n, lab, x, y, sx, sy, d in corners:
    cs.append('<rect class="corner" x="%d" y="%d" width="10" height="10" style="--d:%ss"/>' % (x - 5, y - 5, d))
    anchor = "end" if sx < 0 else "start"
    tx = x + sx * 16
    ty = y + sy * 18 + (4 if sy > 0 else 0)
    cs.append('<text class="lab clab" x="%d" y="%d" text-anchor="%s" style="--d:%ss"><tspan class="num" dx="0">%s</tspan> %s</text>' % (tx, ty, anchor, d, n, lab))
svg = '''<svg class="catch" viewBox="0 0 520 520" role="img" aria-label="Visitors drift in. One lead is caught, known, routed and booked.">
  <defs><pattern id="catch-grid" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="var(--line)"/></pattern></defs>
  <rect x="30" y="30" width="460" height="460" fill="url(#catch-grid)"/>
  <rect x="150" y="150" width="220" height="220" fill="none" stroke="var(--line-strong)" stroke-dasharray="2 4"/>
  <g>%s</g>
  <g fill="none" stroke="var(--ink)" stroke-width="1.5" stroke-linecap="square">%s</g>
  <g>%s</g>
  <circle class="runner" r="5" cx="0" cy="0"/>
  <path class="tick" pathLength="1" d="M228 262 L252 286 L296 236"/>
  <g class="booked"><rect x="176" y="392" width="168" height="28" rx="14" fill="var(--ink)"/><circle cx="194" cy="406" r="3.5" fill="var(--mint)"/><text x="206" y="410" fill="#fff" style="font:500 12px var(--font)">Booked for Thu 10:00</text></g>
</svg>''' % ("\n    ".join(dots), "".join(br), "".join(cs))
os.makedirs("tools/out", exist_ok=True)
open("tools/out/hero.svg", "w").write(svg)
print(len(svg))
