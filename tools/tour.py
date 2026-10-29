# Writes the home page's product tour and the hero picture into index.html, between the
# <!-- tour:start --> / <!-- tour:end --> and <!-- catch:start --> / <!-- catch:end --> marks.
# One lead, Dana Lee from Acme, visits Lumen's pricing page (Lumen is the Claritia customer).
# Run: python3 tools/hero.py && python3 tools/tour.py
import json, re

ICONS = {
  "home": '<path d="M3 10.5 12 3l9 7.5V21h-6v-6H9v6H3z"/>',
  "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
  "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
  "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
  "flow": '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M6 9v3a3 3 0 0 0 3 3h6"/>',
  "route": '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="12" cy="19" r="2.5"/><path d="M6 8.5v1a4 4 0 0 0 4 4h4a4 4 0 0 0 4-4v-1M12 13.5v3"/>',
  "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
  "form": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
  "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
  "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
  "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14.5a6.5 6.5 0 0 1 3.5 5.5"/>',
  "gauge": '<path d="M4 18a8 8 0 1 1 16 0"/><path d="m12 14 4-5"/>',
  "filter": '<path d="M3 6h18M7 12h10M10 18h4"/>',
  "plus": '<path d="M12 5v14M5 12h14"/>',
  "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
  "video": '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="m16 10 5-3v10l-5-3"/>',
  "sparkle": '<path d="M12 3c.6 4.2 2.8 6.4 7 7-4.2.6-6.4 2.8-7 7-.6-4.2-2.8-6.4-7-7 4.2-.6 6.4-2.8 7-7z" fill="currentColor" stroke="none"/>',
}
SYMBOLS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(
  '<symbol id="t-%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">%s</symbol>' % (k, v)
  for k, v in ICONS.items()) + '</defs></svg>'

def ic(name, cls=""):
  return '<svg%s aria-hidden="true"><use href="#t-%s"/></svg>' % (' class="%s"' % cls if cls else "", name)

MARK = ('<svg class="side__mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="6" fill="var(--signal)"/>'
        '<path d="M7 12V7h5M20 7h5v5M25 20v5h-5M12 25H7v-5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M11.5 16.5l3 3 6-7" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')

NAV = [("CRM", [("user", "Contacts"), ("building", "Companies"), ("target", "Opportunities"), ("cal", "Meetings")]),
       ("Automation", [("flow", "Workflows"), ("route", "Routing"), ("spark", "Enrichment")]),
       ("Inbound", [("form", "Forms"), ("clock", "Scheduling"), ("eye", "Visitors")]),
       ("Nurture", [("mail", "Emails"), ("users", "Segments"), ("gauge", "Lead scoring")])]

def side(cur):
  out = ['<div class="side"><div class="side__ws">%sLumen<span class="side__plan">Growth</span></div>' % MARK]
  for lab, items in NAV:
    out.append('<div class="side__lab">%s</div>' % lab)
    for icon, name in items:
      out.append('<div class="side__i%s">%s%s</div>' % (" cur" if name == cur else "", ic(icon), name))
  out.append("</div>")
  return "".join(out)

def bar(crumb, last, chips=""):
  return '<div class="bar"><span class="bar__crumb">%s / <b>%s</b></span><span class="bar__sp"></span>%s</div>' % (crumb, last, chips)

def win(cur, crumb, last, chips, body, x=20, y=20, w=960, h=540, extra=""):
  return '<div class="win" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"%s>%s%s<div class="body">%s</div></div>' % (
    x, y, w, h, extra, side(cur), bar(crumb, last, chips), body)

def canvas(inner, w=1000, h=580, crop=204):
  return ('<div class="canvas-wrap" aria-hidden="true"><div class="canvas" data-canvas data-w="%d" data-h="%d" data-crop="%d" style="width:%dpx;height:%dpx">'
          '<div class="ground"></div>%s</div></div>') % (w, h, crop, w, h, inner)

CURSOR = ('<svg class="cursor" data-guide=\'%s\' viewBox="0 0 18 22" aria-hidden="true"><path d="M1 1v17l4.5-4.2 3 6.7 3-1.4-3-6.6H15z" fill="#0a0a0a" stroke="#fff" stroke-width="1.2" stroke-linejoin="round"/></svg>')

def cursor(stops):
  return CURSOR % json.dumps(stops)

def site_page(url, inner, x=60, y=34, w=880, h=520, at=None, off=None, cls="view"):
  a = ' data-at="%s"' % at if at is not None else ""
  o = ' data-off="%s"' % off if off is not None else ""
  return ('<div class="win %s"%s%s style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;z-index:2"><div class="site-page"><div class="site-page__bar"><i></i><i></i><i></i>'
          '<span class="site-page__url">%s</span></div>%s</div></div>') % (cls, a, o, x, y, w, h, url, inner)

LUMEN_PRICING = '''
<div class="abs" style="left:28px;top:52px;right:28px;display:flex;align-items:center;gap:20px">
  <b style="font-size:15px;letter-spacing:-.02em">&#9670; Lumen</b><span class="mut">Product</span><span>Pricing</span><span class="mut">Customers</span>
  <span class="bar__sp"></span><span class="btnx">Book a demo</span></div>
<div class="abs" style="left:28px;top:116px"><p class="mono fnt" style="font-size:11px;letter-spacing:.08em">PRICING</p>
  <p style="font-size:30px;line-height:36px;font-weight:500;letter-spacing:-.035em;margin-top:6px">Plans for every team</p></div>
<div class="abs" style="left:28px;top:204px;right:28px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px">
  <div class="card" style="position:relative;height:200px;padding:16px"><b>Team</b><p class="mut" style="margin-top:4px">$40 a month</p></div>
  <div class="card" style="position:relative;height:200px;padding:16px;border-color:var(--ink)"><b>Business</b><p class="mut" style="margin-top:4px">$120 a month</p></div>
  <div class="card" style="position:relative;height:200px;padding:16px"><b>Enterprise</b><p class="mut" style="margin-top:4px">Talk to us</p></div>
</div>'''

def tsteps(steps):
  li = []
  for i, (at, t, cap) in enumerate(steps):
    li.append('<li><button type="button" data-go="%s"><span class="tsteps__n">%02d</span><span class="tsteps__t"><b>%s</b><small>%s</small></span><i class="tsteps__bar"></i></button></li>' % (at, i + 1, t, cap))
  caps = []
  for i, (at, t, cap) in enumerate(steps):
    off = ' data-off="%s"' % steps[i + 1][0] if i + 1 < len(steps) else ""
    caps.append('<p class="tcap fade" data-at="%s"%s>%s</p>' % (at, off, cap))
  return '<ol class="tsteps">%s</ol><div class="tcaps" aria-live="polite">%s</div>' % ("".join(li), "".join(caps))

CTL = '''<div class="ctl">
        <button type="button" class="ctl__btn" data-act="prev" aria-label="Previous step"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6 9 12l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <button type="button" class="ctl__btn ctl__btn--main" data-act="play" aria-label="Play or pause"><svg class="ctl__play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg><svg class="ctl__pause" viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="5.5" width="3.5" height="13" rx="1" fill="currentColor"/><rect x="13.5" y="5.5" width="3.5" height="13" rx="1" fill="currentColor"/></svg><svg class="ctl__again" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4h4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <button type="button" class="ctl__btn" data-act="next" aria-label="Next step"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        %s
      </div>'''

def stage(key, length, eyebrow, h1, h2, steps, view, nxt):
  nb = '<button type="button" class="tour__next" data-next="%s">Next: %s <span aria-hidden="true">&rarr;</span></button>' % (nxt[0], nxt[1]) if nxt else ""
  return ('<section class="dstage" data-stage="%s" id="%s" style="--len:%s" role="tabpanel" aria-labelledby="tab-%s"><div class="stage__grid"><div class="stage__rail">'
          '<div class="stage__title"><p class="eyebrow">%s</p><h3 class="stage__h">%s<br><span class="two">%s</span></h3></div>%s%s</div>'
          '<div class="stage__view">%s</div></div></section>') % (key, key, length, key, eyebrow, h1, h2, tsteps(steps), CTL % nb, view)

# ─── 1. Capture ───
ROWS = [("N", "Northwind", "northwind.io", "3 pages", "9m", "tagx", "Browsing"),
        ("G", "Globex", "globex.com", "1 page", "14m", "tagx", "Browsing"),
        ("I", "Initech", "initech.co", "5 pages", "31m", "tagx tagx--warn", "Returning"),
        ("H", "Hooli", "hooli.xyz", "2 pages", "1h", "tagx", "Browsing"),
        ("V", "Vandelay", "vandelay.com", "4 pages", "2h", "tagx", "Browsing")]
def vrow(r, extra_cls="", at=None):
  a = ' data-at="%s"' % at if at is not None else ""
  return ('<div class="tb__r %s"%s style="grid-template-columns:minmax(0,1.4fr) 110px 80px 110px"><span class="co"><i class="lg">%s</i><span>%s<small class="mut" style="display:block;font-weight:400;font-size:11.5px;line-height:14px">%s</small></span></span>'
          '<span class="mut">%s</span><span class="mut mono">%s</span><span><span class="%s">%s</span></span></div>') % (extra_cls, a, r[0], r[1], r[2], r[3], r[4], r[5], r[6])

capture_body = (
  '<div class="tb" style="left:0;top:0"><div class="tb__h" style="grid-template-columns:minmax(0,1.4fr) 110px 80px 110px"><span>Company</span><span>Pages</span><span>Seen</span><span>Intent</span></div>'
  + '<div class="drop" data-at="0.3">' + vrow(("A", "Acme", "acme.com/pricing", "2 pages", "now", "tagx tagx--sig", "High"), "openable r-acme", "1.5") + '</div>'
  + '<div class="push" data-at="0.3">' + "".join(vrow(r) for r in ROWS) + '</div></div>'
  + '<div class="panel slide p-acme" data-at="1.5" style="width:330px;padding:18px 18px">'
    '<div style="display:flex;align-items:center;gap:12px"><i class="lg" style="width:36px;height:36px;border-radius:9px;font-size:15px">A</i><div><b style="font-size:15px">Acme</b><p class="mut" style="font-size:12px">acme.com, 201&ndash;500, SaaS</p></div>'
    '<span class="tagx tagx--sig" style="margin-left:auto">High intent</span></div>'
    '<p class="mono fnt" style="font-size:10px;letter-spacing:.08em;margin-top:22px">PAGES READ</p>'
    '<ol class="tl" style="margin-top:6px">'
      '<li class="sig rise" data-at="1.8" style="--i:0"><b>/pricing</b><small>Twice, 3 min</small></li>'
      '<li class="rise" data-at="1.8" style="--i:1"><b>/product/routing</b><small>2 min</small></li>'
      '<li class="rise" data-at="1.8" style="--i:2"><b>/customers</b><small>40 sec</small></li></ol>'
    '<p class="mono fnt" style="font-size:10px;letter-spacing:.08em;margin-top:16px">PERSON</p>'
    '<p class="mut" style="margin-top:6px">Not known yet</p></div>'
)
capture_view = canvas(
  win("Visitors", "Visitors", "Feed", '<span class="chip"><span class="point point--live" style="width:6px;height:6px;box-shadow:0 0 0 3px var(--signal-soft)"></span>Live</span><span class="chip">%sFilter</span>' % ic("filter"), capture_body)
  + site_page("lumen.io/pricing", LUMEN_PRICING +
      '<div class="card card--pop" style="left:250px;top:70px;width:380px;padding:22px;z-index:2">'
        '<div style="display:flex;align-items:center;justify-content:space-between"><b style="font-size:16px">Book a demo</b><span class="tagx">Step 1 of 2</span></div>'
        '<div class="fld2" style="margin-top:16px"><label>Work email</label><div class="in f-email"><span class="typing" data-type="3.0,3.7">dana@acme.com</span></div></div>'
        '<div class="fld2" style="margin-top:12px"><label>What are you looking for?</label><div class="in"><span class="typing" data-type="3.9,4.5">Routing for three sales teams</span></div></div>'
        '<div class="f-auto" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px">'
          '<div class="fld2 fade" data-at="3.75"><label>Company</label><div class="in auto"><b>Acme</b></div></div>'
          '<div class="fld2 fade" data-at="3.85"><label>Size</label><div class="in auto"><b>201&ndash;500</b></div></div></div>'
        '<p class="fade" data-at="3.9" style="display:flex;align-items:center;gap:6px;margin-top:10px;font-size:11.5px;color:var(--signal-text)">%s Filled by Claritia. Two fields instead of six.</p>'
        '<span class="btnx press f-send" data-at="5" style="width:100%%;height:34px;margin-top:16px">Continue &rarr;</span>'
      '</div>' % ic("sparkle", "sparkle"), at="2.7")
  + '<div class="card card--pop rise" data-at="5.3" style="left:640px;top:470px;width:300px;padding:12px 14px;z-index:4;display:flex;gap:10px;align-items:center"><span class="point"></span><span><b>New lead</b> <span class="mut">Dana Lee, Acme</span></span></div>'
  + cursor([[4.5, ".f-send"], [5.4, ""]])
)

# ─── 2. Qualify ───
FIELDS = [("Email", "dana@acme.com", "Form", None), ("Title", "Head of RevOps", "Vendor", 0.4), ("Company", "Acme", "Website", 0.6),
          ("Size", "201&ndash;500", "Vendor", 0.8), ("Industry", "SaaS", "Vendor", 1.0), ("Region", "United States", "Visit", 1.2), ("Tech", "HubSpot, Slack", "Website", 1.4)]
def kv(lab, val, src, at):
  if at is None:
    return '<div class="kv"><span>%s</span><b>%s</b><span class="src">%s</span></div>' % (lab, val, src)
  return ('<div class="kv flash" data-at="%s"><span>%s</span><span class="swap" data-at="%s"><span class="swap__old fnt">Empty</span><b class="swap__new">%s</b></span><span class="src fade" data-at="%s">%s</span></div>') % (at, lab, at, val, at, src)

qualify_body = (
  '<div class="abs" style="left:0;top:0;width:430px;bottom:0;border-right:1px solid var(--line-light)">'
    '<div style="display:flex;align-items:center;gap:12px;padding:18px 16px"><span class="av" style="width:40px;height:40px;font-size:15px">D</span>'
      '<div><b style="font-size:16px">Dana Lee</b><p class="mut" style="font-size:12px"><span class="swap" data-at="0.4"><span class="swap__old">dana@acme.com</span><span class="swap__new">Head of RevOps at Acme</span></span></p></div></div>'
    + "".join(kv(*f) for f in FIELDS) +
  '</div>'
  '<div class="abs" style="left:450px;top:18px;right:18px">'
    '<div class="card q-score" style="position:relative;padding:16px;display:flex;align-items:center;gap:18px">'
      '<svg width="84" height="84" viewBox="0 0 84 84" aria-hidden="true"><circle class="ring" cx="42" cy="42" r="34"/><circle class="ring ring--on" data-scrub="1.7,2.8" pathLength="1" cx="42" cy="42" r="34" transform="rotate(-90 42 42)"/>'
      '<text x="42" y="48" text-anchor="middle" style="font:500 20px var(--font);fill:var(--ink)" data-count="0,92,1.7,2.8">92</text></svg>'
      '<div style="flex:1"><p class="mono fnt" style="font-size:10px;letter-spacing:.08em">LEAD SCORE</p>'
        '<p style="display:flex;justify-content:space-between;margin-top:8px;font-size:12px"><span>Fit</span><b class="mono" data-count="0,46,1.7,2.6">46</b></p><div class="bar2" data-scrub="1.7,2.6" style="--w:92%"><i></i></div>'
        '<p style="display:flex;justify-content:space-between;margin-top:8px;font-size:12px"><span>Intent</span><b class="mono" data-count="0,46,1.9,2.8">46</b></p><div class="bar2" data-scrub="1.9,2.8" style="--w:92%"><i></i></div></div></div>'
    '<div class="card card--pop rise q-ai" data-at="3.1" style="position:relative;margin-top:12px;padding:16px">'
      '<p style="display:flex;align-items:center;gap:8px;font-weight:500">%s Qualify</p>'
      '<div style="display:flex;gap:6px;margin-top:12px"><span class="tagx tagx--ink pop" data-at="3.6">Qualified</span><span class="tagx">Nurture</span><span class="tagx">Not a fit</span></div>'
      '<p style="margin-top:12px;color:var(--ink-2);line-height:19px"><span class="typing" data-type="3.7,4.7">Fits your ideal customer: SaaS, 201 to 500 people, US. Read pricing twice and asked about routing.</span></p>'
      '<p class="fnt fade" data-at="4.7" style="margin-top:10px;font-size:11.5px">Picked from the outcomes you set</p></div>'
  '</div>').replace("%s", ic("sparkle", "sparkle"), 1)
qualify_view = canvas(win("Contacts", "Contacts", "Dana Lee", '<span class="chip">%sEnrich</span><span class="chip chip--ink">Open in HubSpot</span>' % ic("spark"), qualify_body)
  + '<div class="focus" data-guide=\'%s\'></div>' % json.dumps([[0.3, ".kv.flash"], [1.7, ".q-score"], [3.1, ".q-ai"], [4.9, ""]]))

# ─── 3. Route ───
def rnode(x, y, icon, small, big, cls="", at=None, extra=""):
  a = ' data-at="%s"' % at if at is not None else ""
  return '<div class="abs rnode %s"%s style="left:%dpx;top:%dpx;%s"><span class="rnode__ic">%s</span><span><small>%s</small><b>%s</b></span></div>' % (cls, a, x, y, extra, ic(icon), small, big)

route_body = (
  '<svg class="over" width="776" height="492">'
    '<path class="edge edge--ink wire" pathLength="1" d="M126 82 V128" data-at="0.3"/>'
    '<path class="edge edge--ink wire" pathLength="1" d="M126 182 V228" data-at="0.8"/>'
    '<path class="edge edge--ink wire" pathLength="1" d="M126 282 V328" data-at="1.3"/>'
    '<path class="edge edge--sig wire" pathLength="1" d="M252 355 C300 355 300 120 420 120" data-at="1.7"/>'
  '</svg>'
  '<span class="abs mono fnt" style="left:136px;top:198px;font-size:10px">NO OWNER</span>'
  '<span class="abs mono fnt" style="left:136px;top:298px;font-size:10px">MATCHED</span>'
  + rnode(24, 30, "user", "New lead", "Dana Lee, Acme", "pick on", None)
  + rnode(24, 130, "building", "Rule 1", "Has an owner in HubSpot?", "rise", "0.3")
  + rnode(24, 230, "route", "Rule 2", "US and 200+ people", "rise pick", "0.8")
  + rnode(24, 330, "users", "Send to", "US mid-market team", "rise", "1.3")
  + '<div class="card rise" data-at="1.8" style="left:420px;top:40px;width:330px;padding:14px">'
    '<p style="display:flex;justify-content:space-between"><b>US mid-market</b><span class="fnt">Round robin</span></p>'
    + "".join('<div class="who %s" style="margin-top:12px%s"><span class="av">%s</span><span style="flex:1"><b>%s</b><small>%s</small></span>%s</div>' % (c, st, a, n, sm, t)
       for a, n, sm, t, c, st in [
         ("S", "Sam Rivera", "2 of 8 meetings this week", '<span class="tagx tagx--sig pop" data-at="2.5">Picked</span>', "t-sam", ""),
         ("L", "Lena Park", "Out today", '<span class="tagx tagx--warn">Away</span>', "", ";opacity:.55"),
         ("O", "Omar Haddad", "5 of 8 meetings this week", "", "", "")])
    + '<div class="bar2" data-scrub="1.9,2.6" style="--w:25%;margin-top:14px"><i></i></div></div>'
  + '<div class="card rise" data-at="2.8" style="left:420px;top:258px;width:330px;padding:12px 14px;background:var(--tint)">'
    '<p class="mono fnt" style="font-size:10px;letter-spacing:.08em">WHY</p><p style="margin-top:4px;line-height:19px">No owner. Rule 2 matched: US, 201 to 500 people. Lena is away, and Sam has the fewest meetings this week.</p></div>'
  + '<div class="card card--pop rise r-slack" data-at="3.4" style="left:420px;top:370px;width:330px;padding:12px 14px">'
    '<div class="slack"><span class="slack__av" style="background:var(--tint)"><img src="/assets/logos/slack.svg" width="18" height="18" alt=""></span>'
    '<div><p><b>Claritia</b><small>10:02</small></p><p style="line-height:19px">Sam, a new lead is yours: Dana Lee, Acme. Score 92. She is picking a time now.</p></div></div></div>'
)
route_view = canvas(win("Routing", "Routing", "Inbound demo", '<span class="chip">Try a contact</span><span class="chip chip--ink">Make live</span>', route_body)
  + '<div class="dot6 fly" data-at="1.7" data-off="3.4" style="offset-path:path(\'M456 423 C504 423 504 188 624 188\')"></div>')

# ─── 4. Book ───
SLOTS = ["09:00", "10:00", "11:30", "14:00", "15:30", "16:30"]
book_form = (
  '<div class="card card--pop" style="left:240px;top:58px;width:400px;padding:22px;z-index:2">'
    '<div class="view" data-at="0" data-off="3">'
      '<div style="display:flex;align-items:center;gap:10px"><span class="av" style="width:32px;height:32px">S</span><div><b>Pick a time with Sam</b><p class="mut" style="font-size:12px">30 min, Google Meet</p></div><span class="tagx" style="margin-left:auto">Step 2 of 2</span></div>'
      '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:16px">'
        + "".join('<span class="day%s"><span>%s<b>%s</b></span></span>' % (" cur" if d == "Thu" else "", d, n) for d, n in [("Mon", 2), ("Tue", 3), ("Wed", 4), ("Thu", 5), ("Fri", 6)])
      + '</div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:12px">'
        + "".join('<span class="slot%s"%s>%s</span>' % (" b-slot" if s == "10:00" else "", ' data-at="1.9"' if s == "10:00" else "", s) for s in SLOTS)
      + '</div><span class="btnx press b-ok" data-at="2.7" style="width:100%;height:34px;margin-top:16px">Book Thu 10:00</span></div>'
    '<div class="view" data-at="3" style="position:absolute;inset:22px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px">'
      '<svg width="52" height="52" viewBox="0 0 52 52" aria-hidden="true"><rect x="1" y="1" width="50" height="50" rx="12" fill="var(--signal)"/><path d="M15 27l7 7 15-16" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
      '<b style="font-size:17px;margin-top:6px">You are booked with Sam</b><p class="mut">Thursday, Nov 5 at 10:00</p><p class="fnt" style="font-size:12px">The invite is in your inbox.</p>'
      '<span class="burst" data-at="3.05" style="position:absolute;left:50%;top:40px">'
        + "".join('<i style="--dx:%dpx;--dy:%dpx"></i>' % d for d in [(-60, -30), (54, -36), (-40, 30), (66, 24), (-74, 2), (10, -54), (30, 46), (-20, -50)])
      + '</span></div>'
  '</div>')
TL = [("Visited pricing", "Twice, 3 min", False), ("Filled Book a demo", "Two fields", False), ("Qualified, score 92", "Fits your ideal customer", False),
      ("Routed to Sam Rivera", "Rule 2, round robin", False), ("Meeting booked", "Thu 10:00, Google Meet", True)]
record_body = (
  '<div class="abs" style="left:0;top:0;width:430px;bottom:0;border-right:1px solid var(--line-light);padding:18px 16px">'
    '<div style="display:flex;align-items:center;gap:12px"><span class="av" style="width:40px;height:40px;font-size:15px">D</span><div><b style="font-size:16px">Dana Lee</b><p class="mut" style="font-size:12px">Head of RevOps at Acme</p></div>'
    '<span class="tagx tagx--sig" style="margin-left:auto">Meeting booked</span></div>'
    '<p class="mono fnt" style="font-size:10px;letter-spacing:.08em;margin-top:22px">TIMELINE</p><ol class="tl" style="margin-top:6px">'
      + "".join('<li class="rise%s" data-at="4.3" style="--i:%d"><b>%s</b><small>%s</small></li>' % (" sig" if s else "", i, t, sm) for i, (t, sm, s) in enumerate(TL))
    + '</ol></div>'
  '<div class="abs" style="left:450px;top:18px;right:18px">'
    '<div class="card rise" data-at="4.9" style="position:relative;padding:14px"><p class="mono fnt" style="font-size:10px;letter-spacing:.08em">MEETING</p>'
      '<p style="margin-top:6px"><b>Acme demo</b></p><p class="mut">Thu, Nov 5, 10:00 to 10:30</p>'
      '<div class="who" style="margin-top:10px"><span class="av">S</span><span>Sam Rivera</span><img src="/assets/logos/meet.svg" width="16" height="16" alt="" style="margin-left:auto"></div></div>'
    '<div class="card rise" data-at="5.3" style="position:relative;margin-top:12px;padding:14px"><p class="mono fnt" style="font-size:10px;letter-spacing:.08em">SYNCED</p>'
      '<div class="who" style="margin-top:10px"><i class="lg"><img src="/assets/logos/hubspot.svg" width="13" height="13" alt=""></i><span style="flex:1">HubSpot</span><span class="tagx tagx--sig">Updated</span></div>'
      '<div class="who" style="margin-top:8px"><i class="lg"><img src="/assets/logos/omniscient.svg" width="13" height="13" alt=""></i><span style="flex:1">Omniscient</span><span class="tagx tagx--sig">Updated</span></div></div>'
  '</div>')
book_view = canvas(
  win("Contacts", "Contacts", "Dana Lee", '<span class="chip">%sMeetings</span>' % ic("cal"), record_body)
  + site_page("lumen.io/pricing", LUMEN_PRICING + book_form, cls="view", at="0", off="4.3")
  + cursor([[1.1, ".b-slot"], [2.2, ".b-ok"], [3.0, ""]])
)

TABS = [("capture", "Capture", "Forms that know who is there"), ("qualify", "Qualify", "Enrich, score and decide"),
        ("route", "Route", "The right rep, with a reason"), ("book", "Book", "The meeting, before they leave")]
tabs = '<div class="tour__tabs" role="tablist" aria-label="Product tour">' + "".join(
  '<button type="button" role="tab" id="tab-%s" data-tab="%s" aria-selected="%s" aria-controls="%s"><span class="tour__n">%02d</span><b>%s</b><small>%s</small><i class="tour__prog"></i></button>' % (
    k, k, "true" if i == 0 else "false", k, i + 1, t, s) for i, (k, t, s) in enumerate(TABS)) + "</div>"

stages = [
  stage("capture", 6, "Capture", "Catch every visit.", "Name the company first.", [
    ("0", "Visit", "Dana opens Lumen's pricing page. Claritia names her company before she types."),
    ("1.5", "Name", "Acme, 201 to 500 people, SaaS. Pages read, and how long."),
    ("2.7", "Form", "She types her email. Claritia fills the rest, so the form asks two things."),
    ("4.5", "Send", "One click, and she is a lead.")], capture_view, ("qualify", "Qualify")),
  stage("qualify", 5, "Qualify", "Know who it is.", "Decide in a second.", [
    ("0", "Enrich", "Every empty field fills from your records first, then vendors. Each value keeps its source."),
    ("1.7", "Score", "Fit and intent add up to one score."),
    ("3.1", "Decide", "AI picks one of your outcomes and says why.")], qualify_view, ("route", "Route")),
  stage("route", 5, "Route", "Send it to the right rep.", "Every choice has a reason.", [
    ("0", "Rules", "Owners first, then territories, written as plain rules."),
    ("1.7", "Pick", "Round robin skips people who are away and keeps the load even."),
    ("3.2", "Tell", "Sam hears about it in Slack while Dana is still on the page.")], route_view, ("book", "Book")),
  stage("book", 6, "Book", "Book the meeting.", "Before they leave the page.", [
    ("0", "Open", "Sam's open times show inside the form."),
    ("1.1", "Pick", "Dana picks Thursday at 10:00."),
    ("3", "Booked", "The invite goes out. Twenty seconds from visit to meeting."),
    ("4.4", "Record", "The whole path lands on the record and syncs to your CRM.")], book_view, None),
]

tour = ('''<section class="tour" id="tour" data-tour>
    <div class="wrap">
      <div class="tour__head reveal">
        <p class="eyebrow">Product tour</p>
        <h2 class="h2">One lead, twenty seconds.<br><span class="two">Press play.</span></h2>
      </div>
      ''' + tabs + "\n      " + "\n      ".join(stages) + '''
    </div>
  </section>''')

page = open("index.html").read()
page = re.sub(r"(<!-- tour:start -->).*?(<!-- tour:end -->)", lambda m: m.group(1) + "\n  " + SYMBOLS + "\n  " + tour + "\n  " + m.group(2), page, flags=re.S)
page = re.sub(r"(<!-- catch:start -->).*?(<!-- catch:end -->)", lambda m: m.group(1) + "\n" + open("tools/out/hero.svg").read() + "\n" + m.group(2), page, flags=re.S)
open("index.html", "w").write(page)
print("ok", len(page))
