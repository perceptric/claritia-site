# Writes the animated product drawings in assets/img/feat-*.svg (320 x 180).
# One stroke style for all: 1px lines, black for the thing, gray for the rest, emerald for what moves.
import os
HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180"><style>'
  '.e{fill:none;stroke:#d4d4d0;stroke-width:1}.k{fill:none;stroke:#0a0a0a;stroke-width:1}.s{fill:none;stroke:#0c8c5e;stroke-width:1.4}'
  '.sq{fill:#fff;stroke:#0a0a0a;stroke-width:1}.sl{fill:#fff;stroke:#d4d4d0;stroke-width:1}.n{fill:#e7e7e4}.ni{fill:#0a0a0a}.ns{fill:#0c8c5e}.nw{fill:#fff}'
  '.t{font:500 8px ui-monospace,Menlo,monospace;letter-spacing:.06em;fill:#a3a3a3}.tk{font:500 9px Inter,ui-sans-serif,system-ui,sans-serif;fill:#0a0a0a}'
  '@media (prefers-reduced-motion:reduce){*{animation:none!important}}%s</style>')
F = {}

# CRM: a record whose timeline lights up, one event at a time
F["crm"] = ("""
.ev{animation:ev 4.8s ease-out infinite}@keyframes ev{0%,10%{fill:#e7e7e4}20%,90%{fill:#0c8c5e}100%{fill:#e7e7e4}}
.ln{animation:ln 4.8s ease-out infinite;opacity:0}@keyframes ln{0%,10%{opacity:0}22%,90%{opacity:1}100%{opacity:0}}
""", """
<rect class="sq" x="64" y="30" width="192" height="120" rx="8"/>
<rect class="n" x="78" y="44" width="22" height="22" rx="6"/><path class="k" d="M108 51 H164"/><path class="e" d="M108 60 H146"/>
<path class="e" d="M78 78 H242"/><path class="e" d="M88 88 V140"/>
""" + "".join('<circle class="ev" cx="88" cy="%d" r="4" style="animation-delay:%.1fs"/><path class="e" d="M100 %d H%d"/><path class="k ln" d="M100 %d H%d" style="animation-delay:%.1fs"/>' % (y, i * 0.6, y, 200 - i * 14, y, 200 - i * 14, i * 0.6) for i, y in enumerate([92, 108, 124, 140])))

# Workflows: trigger, wait, email, goal, with a dot running the line
F["workflows"] = ("""
.mv{animation:mv 3.6s linear infinite}@keyframes mv{0%{transform:translateX(0);opacity:0}5%{opacity:1}90%{transform:translateX(204px);opacity:1}100%{transform:translateX(204px);opacity:0}}
.lit{animation:lit 3.6s steps(1) infinite}@keyframes lit{0%{fill:#fff}100%{fill:#fff}}
.g{animation:g 3.6s ease-out infinite}@keyframes g{0%,86%{fill:#fff}92%,100%{fill:#0c8c5e}}
""", """
<path class="e" d="M74 90 H246"/>
<rect class="sq" x="42" y="74" width="32" height="32" rx="8"/><path class="k" d="M51 85 H65 M51 90 H65 M51 95 H59"/>
<rect class="sq" x="112" y="74" width="32" height="32" rx="8"/><circle class="k" cx="128" cy="90" r="7"/><path class="k" d="M128 86 V90 L131 92"/>
<rect class="sq" x="178" y="74" width="32" height="32" rx="8"/><path class="k" d="M186 84 H202 V96 H186 Z M186 84 L194 91 L202 84"/>
<rect class="sq g" x="246" y="74" width="32" height="32" rx="16"/><path d="M255 90 L260 95 L269 85" fill="none" stroke="#0a0a0a" stroke-width="1.4"/>
<text class="t" x="58" y="126" text-anchor="middle">FORM</text><text class="t" x="128" y="126" text-anchor="middle">WAIT</text><text class="t" x="194" y="126" text-anchor="middle">EMAIL</text><text class="t" x="262" y="126" text-anchor="middle">GOAL</text>
<circle class="ns mv" cx="58" cy="90" r="3.5"/>
""")

# Routing: a lead comes in, the rules pick one lane of three
F["routing"] = ("""
.in{animation:in 3.6s ease-in-out infinite}@keyframes in{0%{transform:translate(0,0);opacity:0}6%{opacity:1}40%{transform:translate(80px,0)}75%{transform:translate(170px,0);opacity:1}88%,100%{transform:translate(170px,0);opacity:0}}
.lane{animation:lane 3.6s ease-out infinite}@keyframes lane{0%,40%{stroke:#d4d4d0}48%,90%{stroke:#0c8c5e}100%{stroke:#d4d4d0}}
.pk{animation:pk 3.6s ease-out infinite}@keyframes pk{0%,70%{fill:#fff;stroke:#d4d4d0}78%,94%{fill:#0a0a0a;stroke:#0a0a0a}100%{fill:#fff;stroke:#d4d4d0}}
""", """
<path class="e" d="M40 90 H120"/>
<rect class="sq" x="112" y="78" width="24" height="24" rx="5" transform="rotate(45 124 90)"/>
<path class="e" d="M136 90 C170 90 170 44 210 44"/><path class="e lane" d="M136 90 H210"/><path class="e" d="M136 90 C170 90 170 136 210 136"/>
<circle class="sl" cx="226" cy="44" r="14"/><circle class="sl pk" cx="226" cy="90" r="14"/><circle class="sl" cx="226" cy="136" r="14"/>
<text class="t" x="250" y="47">LENA</text><text class="t" x="250" y="93">SAM</text><text class="t" x="250" y="139">OMAR</text>
<circle class="ns in" cx="40" cy="90" r="4"/>
""")

# Enrichment: empty fields fill one by one, each with its source
F["enrichment"] = ("""
.fl{transform-box:fill-box;transform-origin:left;animation:fl 4.8s ease-out infinite}@keyframes fl{0%,8%{transform:scaleX(0)}22%,90%{transform:scaleX(1)}100%{transform:scaleX(0)}}
.sr{animation:sr 4.8s ease-out infinite;opacity:0}@keyframes sr{0%,18%{opacity:0}26%,90%{opacity:1}100%{opacity:0}}
""", "".join('''
<path class="e" d="M60 %d H260"/><text class="t" x="60" y="%d">%s</text><rect class="n" x="128" y="%d" width="%d" height="8" rx="4"/>
<rect class="ni fl" x="128" y="%d" width="%d" height="8" rx="4" style="animation-delay:%.1fs"/><text class="t sr" x="260" y="%d" text-anchor="end" style="animation-delay:%.1fs;fill:#0c8c5e">%s</text>''' % (
    y + 12, y + 7, lab, y, w, y, w, i * 0.5, y + 7, i * 0.5, src) for i, (y, lab, w, src) in enumerate([(36, "TITLE", 70, "FORM"), (66, "SIZE", 46, "CRM"), (96, "INDUSTRY", 58, "WEB"), (126, "TECH", 82, "VENDOR")])))

# Forms: two fields typed, the rest filled by Claritia, then the button
F["forms"] = ("""
.ty{transform-box:fill-box;transform-origin:left;animation:ty 4.8s steps(12) infinite}@keyframes ty{0%{transform:scaleX(0)}25%,92%{transform:scaleX(1)}100%{transform:scaleX(0)}}
.au{animation:au 4.8s ease-out infinite}@keyframes au{0%,30%{fill:#fff;stroke:#d4d4d0}38%,92%{fill:#e8f5ef;stroke:#b8e2cf}100%{fill:#fff;stroke:#d4d4d0}}
.av{transform-box:fill-box;transform-origin:left;animation:av 4.8s ease-out infinite}@keyframes av{0%,32%{transform:scaleX(0)}42%,92%{transform:scaleX(1)}100%{transform:scaleX(0)}}
.bt{transform-box:fill-box;transform-origin:center;animation:bt 4.8s ease-out infinite}@keyframes bt{0%,62%{transform:scale(1)}66%{transform:scale(.9)}72%,100%{transform:scale(1)}}
""", """
<rect class="sq" x="84" y="16" width="152" height="150" rx="8"/>
<path class="k" d="M98 32 H160"/>
<rect class="sl" x="98" y="44" width="124" height="18" rx="4"/><rect class="ni ty" x="104" y="51" width="64" height="4" rx="2"/>
<rect class="sl" x="98" y="68" width="124" height="18" rx="4"/><rect class="ni ty" x="104" y="75" width="44" height="4" rx="2" style="animation-delay:.4s"/>
<rect class="sl au" x="98" y="96" width="58" height="16" rx="4"/><rect class="sl au" x="164" y="96" width="58" height="16" rx="4" style="animation-delay:.15s"/>
<rect class="ns av" x="104" y="102" width="30" height="4" rx="2"/><rect class="ns av" x="170" y="102" width="36" height="4" rx="2" style="animation-delay:.15s"/>
<g class="bt"><rect class="ni" x="98" y="128" width="124" height="22" rx="11"/><path d="M152 139 H166 M161 134 L166 139 L161 144" fill="none" stroke="#fff" stroke-width="1.2"/></g>
""")

# Scheduling: open times on a week, one gets picked
F["scheduling"] = ("""
.pk{animation:pk 3.6s ease-out infinite}@keyframes pk{0%,40%{fill:#fff;stroke:#d4d4d0}48%,92%{fill:#0a0a0a;stroke:#0a0a0a}100%{fill:#fff;stroke:#d4d4d0}}
.ck{stroke-dasharray:20;stroke-dashoffset:20;animation:ck 3.6s ease-out infinite}@keyframes ck{0%,52%{stroke-dashoffset:20}64%,92%{stroke-dashoffset:0}100%{stroke-dashoffset:20}}
.cur{animation:cur 3.6s ease-in-out infinite}@keyframes cur{0%{transform:translate(40px,40px);opacity:0}10%{opacity:1}40%,90%{transform:translate(0,0);opacity:1}100%{opacity:0}}
""", "".join('<text class="t" x="%d" y="34" text-anchor="middle">%s</text>' % (76 + i * 42, d) for i, d in enumerate(["MON", "TUE", "WED", "THU", "FRI"])) +
 "".join('<rect class="sl%s" x="%d" y="%d" width="34" height="18" rx="4"/>' % (" pk" if (i, j) == (3, 1) else "", 59 + i * 42, 46 + j * 26) for i in range(5) for j in range(4) if (i + j * 2) % 3 != 0) +
 '<path class="ck" d="M193 81 L198 86 L206 76" fill="none" stroke="#18e299" stroke-width="1.6"/>'
 '<g class="cur"><path d="M204 84 L204 100 L208 96 L211 103 L214 102 L211 95 L216 95 Z" fill="#0a0a0a" stroke="#fff" stroke-width="1"/></g>')

# Visitors: a browser whose visitors get named, company by company
F["visitors"] = ("""
.rw{animation:rw 4.8s ease-out infinite;opacity:0}@keyframes rw{0%{opacity:0;transform:translateY(-6px)}10%,90%{opacity:1;transform:none}100%{opacity:0}}
.lv{animation:lv 1.6s ease-out infinite}@keyframes lv{0%{r:3;opacity:1}100%{r:9;opacity:0}}
""", """
<rect class="sq" x="40" y="24" width="240" height="134" rx="8"/><path class="e" d="M40 42 H280"/>
<circle class="n" cx="52" cy="33" r="3"/><circle class="n" cx="62" cy="33" r="3"/><circle class="n" cx="72" cy="33" r="3"/>
""" + "".join('''<g class="rw" style="animation-delay:%.1fs"><circle class="%s" cx="60" cy="%d" r="3"/><rect class="%s" x="72" y="%d" width="%d" height="6" rx="3"/><rect class="n" x="190" y="%d" width="40" height="6" rx="3"/><text class="t" x="266" y="%d" text-anchor="end">%s</text></g>''' % (
   i * 0.7, "ns" if i == 0 else "n", y, "ni" if i == 0 else "n", y - 3, w, y - 3, y + 3, t) for i, (y, w, t) in enumerate([(62, 74, "LIVE"), (86, 56, "2M"), (110, 90, "9M"), (134, 64, "1H")])) +
 '<circle class="ns lv" cx="60" cy="62" r="3" fill="none"/>')

# Emails: written, approved, sent from your domain
F["emails"] = ("""
.wr{transform-box:fill-box;transform-origin:left;animation:wr 4.8s steps(10) infinite}@keyframes wr{0%{transform:scaleX(0)}30%,94%{transform:scaleX(1)}100%{transform:scaleX(0)}}
.ap{animation:ap 4.8s ease-out infinite}@keyframes ap{0%,48%{fill:#fff;stroke:#0a0a0a}54%,94%{fill:#0a0a0a;stroke:#0a0a0a}100%{fill:#fff}}
.apt{animation:apt 4.8s ease-out infinite}@keyframes apt{0%,48%{stroke:#0a0a0a}54%,94%{stroke:#fff}100%{stroke:#0a0a0a}}
.fly{animation:fly 4.8s ease-in infinite;opacity:0}@keyframes fly{0%,60%{transform:translate(0,0);opacity:0}64%{opacity:1}86%{transform:translate(70px,-34px);opacity:1}94%,100%{transform:translate(78px,-38px);opacity:0}}
""", """
<rect class="sq" x="56" y="22" width="168" height="140" rx="8"/>
<path class="e" d="M70 40 H210"/><text class="t" x="70" y="36">TO DANA LEE</text>
<rect class="ni wr" x="70" y="54" width="110" height="5" rx="2.5"/>
<rect class="n wr" x="70" y="70" width="140" height="4" rx="2" style="animation-delay:.3s"/><rect class="n wr" x="70" y="82" width="124" height="4" rx="2" style="animation-delay:.5s"/><rect class="n wr" x="70" y="94" width="96" height="4" rx="2" style="animation-delay:.7s"/>
<rect class="sq ap" x="70" y="128" width="64" height="20" rx="10"/><path class="apt" d="M92 138 L97 143 L106 133" fill="none" stroke-width="1.4"/>
<g class="fly"><path d="M232 104 L262 92 L248 120 L244 108 Z" fill="#0c8c5e"/></g>
""")

# Lead scoring: fit and intent fill a ring
F["scoring"] = ("""
.rg{stroke-dasharray:220;stroke-dashoffset:220;animation:rg 4.2s ease-out infinite}@keyframes rg{0%,10%{stroke-dashoffset:220}50%,90%{stroke-dashoffset:18}100%{stroke-dashoffset:220}}
.br{transform-box:fill-box;transform-origin:left;animation:br 4.2s ease-out infinite}@keyframes br{0%,10%{transform:scaleX(0)}46%,90%{transform:scaleX(1)}100%{transform:scaleX(0)}}
""", """
<circle cx="104" cy="90" r="35" fill="none" stroke="#e7e7e4" stroke-width="6"/>
<circle class="rg" cx="104" cy="90" r="35" fill="none" stroke="#0c8c5e" stroke-width="6" stroke-linecap="round" transform="rotate(-90 104 90)"/>
<text x="104" y="96" text-anchor="middle" style="font:500 18px Inter,ui-sans-serif,system-ui,sans-serif;fill:#0a0a0a">92</text>
<text class="t" x="170" y="70">FIT</text><rect class="n" x="170" y="76" width="96" height="6" rx="3"/><rect class="ni br" x="170" y="76" width="88" height="6" rx="3"/>
<text class="t" x="170" y="104">INTENT</text><rect class="n" x="170" y="110" width="96" height="6" rx="3"/><rect class="ns br" x="170" y="110" width="90" height="6" rx="3" style="animation-delay:.3s"/>
""")

os.makedirs("assets/img", exist_ok=True)
for k, (css, body) in F.items():
    open("assets/img/feat-%s.svg" % k, "w").write(HEAD % css.replace("\n", "") + body.replace("\n", "") + "</svg>")
print(sorted(F))
