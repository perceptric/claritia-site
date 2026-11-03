"""Builds the product pages: /products, /products/forms, /products/meetings and /products/routing. Each is an open
page (no boxed cards) built around demos that really run: Forms has Tia building real templates you can fill in, in
any style, plus a price that adds up and the embed code for every way; Meetings has a booking calendar on real dates in
the visitor's time zone, the reminder line and a live booking form; Routing has a router you answer like a lead and a
round robin you can weight. Each links to the best templates for it. The demos are in assets/products.js and the
styles in assets/products.css. Plan tags follow docs/pricing.md in the app repo. Run: python3 tools/products.py"""
import json, pathlib, re, sys, zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shell  # noqa: E402
import templates as tpl  # noqa: E402

PX_V = 1
esc = shell.esc
APP = "https://app.tryclaritia.com"
BY = {t["slug"]: t for t in tpl.T}
I = lambda name, cls="i": f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'
CHECK = '<svg aria-hidden="true"><use href="#i-check"/></svg>'
PEOPLE = {"MO": ["#0c8c5e", "Maya Ortiz"], "LK": ["#3b6fd8", "Lena Koch"], "SB": ["#c2410c", "Sam Brooks"], "RJ": ["#7c3aed", "Rae Jin"]}
person = lambda k: f'<span class="person"><span class="av" style="background:{PEOPLE[k][0]}">{k}</span>{PEOPLE[k][1]}</span>'
band = lambda: '<div class="band"><div class="frame"></div></div>'


def frame(inner: str) -> str:
    return f'  <div class="frame">\n{inner}\n  </div>\n  {band()}\n'


def head_block(eyebrow, icon, title, sub, h_id, center=False):
    return f"""<div class="px-sec__head{' px-sec__head--center' if center else ''}">
        <span class="eyebrow">{I(icon, "i s12")}{esc(eyebrow)}</span>
        <h2 class="h2" id="{h_id}">{title}</h2>
        <p class="sub">{esc(sub)}</p>
      </div>"""


def ctas(second=("See pricing", "/pricing")):
    return f"""<div class="px-ctas">
        <a class="btn btn--primary btn--lg" href="{APP}">Start free {I("arrow", "i s14 arr")}</a>
        <a class="btn btn--ghost btn--lg" href="{second[1]}">{esc(second[0])}</a>
      </div>
      <p class="px-note">Free plan. No card needed.</p>"""


# Live forms and template links --------------------------------------------------------------------------------

def unique_ids(html: str, p: str) -> str:
    """Several live forms on one page: each one's ids (and the labels and descriptions pointing at them) get a prefix."""
    def fix(m):
        return m.group(1) + re.sub(r'(^|\s)f-', lambda x: x.group(1) + f"{p}f-", m.group(2)) + '"'
    return re.sub(r'((?:id|for|aria-labelledby|aria-describedby)=")([^"]*)"', fix, html)


def live(slug: str, shown: bool = True) -> str:
    t = BY[slug]
    stage = tpl.stage(t, t["theme"]).replace(" data-stage>", f' data-tpl="{slug}" data-own="{t["theme"]}"{"" if shown else " hidden"}>', 1)
    return unique_ids(stage, "x" + format(zlib.crc32(slug.encode()) % 46656, "x") + "-")


def theme_data() -> str:
    data = {x["id"]: {k: x[k] for k in ("layout", "input", "shadow", "pattern", "dark")} for x in tpl.THEMES}
    return f'<script type="application/json" id="px-themes">{json.dumps(data)}</script>'


def build_steps(t) -> list[str]:
    s = t["schema"]
    pages = len(s["pages"])
    out = [f"Added {tpl.questions(t)} questions" + (f" over {pages} pages" if pages > 1 else "")]
    f = set(t["features"])
    if "logic" in f:
        out.append("Skipped what doesn't apply")
    if "calculator" in f:
        out.append("Priced every option")
    if "payment" in f:
        out.append("Took payment with Stripe")
    if "signature" in f:
        out.append("Added a signature")
    if "file" in f:
        out.append("Took photos and files")
    if "booking" in f:
        out.append("Linked a meeting to the end")
    if "follow-up" in t["does"]:
        out.append("Drafted a follow-up email")
    out.append(f"Styled it {tpl.TH[t['theme']]['name']}")
    return out


def shelf(slugs, more_label, more_href):
    items = []
    for s in slugs:
        t = BY[s]
        pages = len(t["schema"]["pages"])
        meta = f"{tpl.questions(t)} questions" + (f", {pages} pages" if pages > 1 else "")
        items.append(
            f'<a class="px-tpl" href="/templates/{s}">{tpl.thumb(t)}'
            f'<span class="px-tpl__name"><b>{esc(t["name"])}</b><span>{esc(meta)}</span></span><p>{esc(t["blurb"])}</p></a>'
        )
    return f"""<div class="px-shelf">{"".join(items)}</div>
      <div class="px-more"><a class="btn btn--ghost btn--lg" href="{more_href}">{esc(more_label)} {I("arrow", "i s14 arr")}</a></div>"""


def caps(items):
    out = []
    for ic, title, line, plan in items:
        tag = f'<span class="tag tag--green">{plan}</span>' if plan else ""
        out.append(f'<div class="px-cap"><div class="px-cap__top">{I(ic)}<h3>{esc(title)}</h3>{tag}</div><p>{esc(line)}</p></div>')
    return f'<div class="px-caps">{"".join(out)}</div>'


def faq(items):
    plus = '<svg aria-hidden="true"><use href="#i-plus"/></svg>'
    qa = "".join(f"<details><summary>{esc(q)} {plus}</summary><p>{esc(a)}</p></details>" for q, a in items)
    return f"""  <div class="frame px-faq">
    <section class="px-sec" aria-labelledby="faq-h">
      <div class="faq">
        <div class="faq__head">
          <h2 class="h2" id="faq-h">Questions</h2>
          <p class="lead">Something else? <a href="mailto:hello@tryclaritia.com">hello@tryclaritia.com</a></p>
        </div>
        <div class="qa">{qa}</div>
      </div>
    </section>
  </div>
"""


def cta():
    return shell.absolute(shell.block("<!-- The last prompt, on dark -->", "</section>\n    </div>\n  </div>"))


def page(slug, title, desc, main, forms=True, live_forms=False):
    extra = ""
    if forms:
        extra += f'<link rel="stylesheet" href="{tpl.FONTS_URL}">\n<link rel="stylesheet" href="/assets/forms.css?v={tpl.CSS_V}">\n<link rel="stylesheet" href="/assets/themes.css?v={tpl.CSS_V}">\n'
    extra += f'<link rel="stylesheet" href="/assets/products.css?v={PX_V}">\n'
    scripts = (f'<script src="/assets/forms.js?v={tpl.JS_V}" defer></script>\n' if live_forms else "") + f'<script src="/assets/products.js?v={PX_V}" defer></script>\n'
    return shell.head(title, desc, slug, extra) + "\n" + shell.body(main, scripts)


# Forms -----------------------------------------------------------------------------------------------------------

BUILDS = [
    ("saas-demo-request", "Book a demo with sales", "Build a demo request form that books a call with sales"),
    ("food-catering-calculator", "Catering quote with a deposit", "Build a catering quote with a price for each guest and a deposit"),
    ("construction-roof-inspection", "Roof inspection with photos", "Build a roof inspection request with photos and a visit booked at the end"),
    ("healthcare-patient-intake", "Patient intake with a signature", "Build a new patient intake with insurance, history and a signature"),
]
SWATCHES = ["midnight", "paper", "coral", "grove", "editorial", "terminal", "bubblegum", "gilded"]

EMBEDS = [
    ("inline", "In the page", '<claritia-form form-id="FORM_ID"></claritia-form>'),
    ("popup", "Popup", '<claritia-form form-id="FORM_ID" popup="click"></claritia-form>\n<button data-claritia-open="FORM_ID">Get a quote</button>'),
    ("slider", "Slide in", '<claritia-form form-id="FORM_ID" popup="click" slider="right"></claritia-form>'),
    ("popover", "Corner button", '<claritia-form form-id="FORM_ID" popover icon="form"></claritia-form>'),
    ("tab", "Side tab", '<claritia-form form-id="FORM_ID" side-tab="Contact us"></claritia-form>'),
]
SCRIPT_TAG = '<script src="https://app.tryclaritia.com/forms/v1.js" async></script>'


def forms_page():
    first = BUILDS[0]
    chips = "".join(
        f'<button type="button" data-ask="{s}" data-text="{esc(text)}" data-list="{esc(json.dumps(build_steps(BY[s])))}" aria-pressed="{"true" if i == 0 else "false"}">{I("spark")}{esc(label)}</button>'
        for i, (s, label, text) in enumerate(BUILDS)
    )
    stages = "".join(live(s, i == 0) for i, (s, _, _) in enumerate(BUILDS))
    sw = "".join(f'<button type="button" data-swatch="{x}" aria-label="{esc(tpl.TH[x]["name"])} style" aria-pressed="false">{tpl.swatch(x)}</button>' for x in SWATCHES)
    first_steps = "".join(f"<li>{CHECK}{esc(x)}</li>" for x in build_steps(BY[first[0]]))
    hero = f"""    <section class="px-hero px-top" aria-labelledby="pp-h">
      <div class="px-copy">
        <span class="eyebrow">{I("form", "i s12")}Forms</span>
        <h1 id="pp-h">Forms that turn visitors into leads</h1>
        <p class="sub">Say what you need and Tia builds it in your brand: steps, logic, prices, payments and a meeting booked at the end. Try one right here.</p>
        {ctas(("See all templates", "/templates"))}
      </div>
      <div class="px-build" data-build>
        <form class="px-ask" action="{APP}/forms/new" method="get">
          <label class="sr-only" for="px-ask">Describe the form you need</label>
          <textarea id="px-ask" name="ask" maxlength="300" rows="2">{esc(first[2])}</textarea>
          <button class="btn btn--green" type="submit">Build it {I("arrow", "i s14 arr")}</button>
        </form>
        <div class="px-chips" role="group" aria-label="Try one" data-js>{chips}</div>
        <ul class="px-steps" data-steps aria-live="polite">{first_steps}</ul>
        <div class="px-live">{stages}</div>
        <div class="px-styles" data-js><span class="px-label">Style</span>{sw}<button type="button" data-shuffle>{I("i-shuffle")}Shuffle</button><a href="/templates/{first[0]}" data-use-tpl>Open this template {I("arrow-up")}</a></div>
      </div>
    </section>"""

    nums = f"""    <section class="px-sec" style="padding-top:88px" aria-label="Forms in numbers">
      <div class="px-nums">
        <div><b>{len(tpl.T)}</b><span>form templates</span></div>
        <div><b>{len(tpl.THEMES)}</b><span>styles to start from</span></div>
        <div><b>15</b><span>field types</span></div>
        <div><b>1</b><span>line to put it on your site</span></div>
      </div>
    </section>"""

    calc = f"""    <section class="px-sec" aria-labelledby="calc-h">
      {head_block("Prices", "grid", "Prices that add up as they answer", "Quotes, estimates and deposits work out on their own. Change the order and watch it.", "calc-h")}
      <div class="px-calc" data-px-calc>
        <p class="px-say">Catering for <span class="px-step" data-js><button type="button" data-less aria-label="Fewer guests">&minus;</button><output data-guests aria-live="polite">40</output><button type="button" data-more aria-label="More guests">+</button></span><noscript>40</noscript> guests, served as a
          <span class="px-chips" role="group" aria-label="Service" data-js><button type="button" data-per="38" aria-pressed="true">Buffet</button><button type="button" data-per="52" aria-pressed="false">Plated dinner</button><button type="button" data-per="45" aria-pressed="false">Family style</button></span><noscript>buffet</noscript>
          and <span class="px-chips" data-js><button type="button" data-bar aria-pressed="true">an open bar</button></span><noscript>an open bar</noscript></p>
        <div class="px-sum" aria-live="polite">
          <span>Total, at <span data-each>$50</span> a guest</span>
          <b data-total>$2,000</b>
          <span><em data-deposit>$400</em> deposit taken now with Stripe</span>
          <a class="btn btn--ghost" style="margin-top:12px;align-self:flex-start" href="/templates/food-catering-calculator">Try the full calculator {I("arrow", "i s14 arr")}</a>
        </div>
      </div>
    </section>"""

    modes = "".join(
        f'<button type="button" data-mode="{m}" data-snippet="{esc(SCRIPT_TAG + chr(10) + code)}" aria-pressed="{"true" if i == 0 else "false"}">{esc(label)}</button>'
        for i, (m, label, code) in enumerate(EMBEDS)
    )
    embed = f"""    <section class="px-sec" aria-labelledby="emb-h">
      <div class="px-embed" data-px-embed>
        <div class="px-embed__side">
          <span class="eyebrow">{I("globe", "i s12")}Share</span>
          <h2 class="h2" id="emb-h">Put it anywhere</h2>
          <p class="sub" style="margin:0">One script, then pick how it shows: in the page, as a popup, sliding in, behind a corner button or on a side tab. Or just share the link.</p>
          <div class="px-chips" role="group" aria-label="How it shows" data-js>{modes}</div>
          <pre class="px-code"><code data-code>{esc(SCRIPT_TAG + chr(10) + EMBEDS[0][2])}</code><button type="button" data-copy data-js>Copy</button></pre>
          <p class="px-note">Works on Webflow, WordPress, Framer, Shopify and plain HTML.</p>
        </div>
        <div class="px-site" data-px-site data-show="inline" aria-hidden="true">
          <div class="px-site__bar"><i></i><i></i><i></i></div>
          <div class="px-site__body"><p class="h"></p><p style="width:82%"></p><p style="width:74%"></p><p style="width:64%"></p></div>
          <div class="px-dim"></div>
          <div class="px-mini"><b>Get a quote</b><i></i><i></i><i></i><s></s></div>
          <span class="px-pop px-pop--corner">{I("form")}</span>
          <span class="px-pop px-pop--tab">Contact us</span>
        </div>
      </div>
    </section>"""

    features = caps([
        ("spark", "Built from a sentence", "Tell Tia what you need. She writes the questions, the steps and the ending, and you change anything by asking.", None),
        ("type", "15 field types", "Text, email, phone, choices, dates, ratings, scales, addresses, file uploads and consent.", None),
        ("route", "Logic that skips ahead", "Show a question or skip a step from any earlier answer.", None),
        ("grid", "Prices and scores", "Quotes, estimates and scores that add up as people answer.", None),
        ("card", "Payments", "Take a full payment or a deposit with Stripe.", "Starter"),
        ("sign", "Signatures", "People sign right in the form, on any screen.", "Starter"),
        ("cal", "Booking at the end", "The calendar is the last step, so a lead picks a time before leaving.", None),
        ("globe", "Your brand, copied in", "Tia reads your site and matches its fonts, colors and buttons.", None),
        ("lang", "Spam stays out", "Cloudflare Turnstile, a hidden trap and limits keep bots away. Consent is saved with the exact words.", None),
    ])
    main = (
        frame(hero) + frame(nums) + frame(calc) + frame(embed)
        + frame(f"""    <section class="px-sec" aria-labelledby="feat-h">
      {head_block("Everything", "check", "Everything in Forms", "Tags show the plan a feature starts on. The rest is on every plan, Free included.", "feat-h")}
      {features}
    </section>""")
        + frame(f"""    <section class="px-sec" aria-labelledby="tpl-h">
      {head_block("Templates", "form", "Start from a template", "Every one is a real form you can fill in now. Open one, try it, then make it yours.", "tpl-h")}
      {shelf(["food-catering-calculator", "saas-demo-request", "healthcare-patient-intake", "construction-roof-inspection", "creative-photo-session", "events-registration"], f"See all {len(tpl.T)} templates", "/templates")}
    </section>""")
        + faq([
            ("Can I keep my current forms?", "Yes. Fills from HubSpot, Webflow, Typeform and Tally forms can come into Claritia, so they book and follow up the same way."),
            ("Where do the answers go?", "Into Claritia first, then to the tools you connect: HubSpot, Salesforce, Google Sheets, Airtable, Notion, Slack, email lists and webhooks."),
            ("How many forms can I make?", "As many as you like, on every plan. Plans differ by submissions a month: 250 on Free, 2,000 on Starter, 5,000 on Pro and unlimited on Business."),
            ("Are the templates free?", f"Yes. All {len(tpl.T)} are free on every plan, including Free."),
        ])
        + theme_data() + "\n" + cta()
    )
    return page("/products/forms", "Forms · Claritia", f"Claritia Forms: describe a form and Tia builds it in your brand, with steps, logic, prices, payments and booking at the end. {len(tpl.T)} free templates.", main, live_forms=True)


# Meetings ----------------------------------------------------------------------------------------------------------

KINDS = {
    "one": {"name": "Intro call", "line": "15 min on Google Meet, with Maya", "hosts": ["MO"]},
    "rr": {"name": "Sales demo", "line": "30 min on Google Meet, with Lena or Sam, whoever is free", "hosts": ["LK", "SB"]},
    "group": {"name": "Weekly group demo", "line": "60 min on Zoom, up to 20 people", "hosts": ["MO"], "group": True},
}


def meetings_page():
    widget = f"""<div class="px-build" data-book-demo>
        <div class="px-chips" role="group" aria-label="Kind of meeting" data-js>
          <button type="button" data-kind="one" aria-pressed="true">{I("user")}One person</button>
          <button type="button" data-kind="rr" aria-pressed="false">{I("users")}Round robin</button>
          <button type="button" data-kind="group" aria-pressed="false">{I("grid")}Group</button>
        </div>
        <div class="px-bk">
          <script type="application/json" data-people>{json.dumps(PEOPLE)}</script>
          <script type="application/json" data-kinds>{json.dumps(KINDS)}</script>
          <div class="px-bk__head" data-head data-js></div>
          <div class="px-bk__pickwrap" data-step="pick" data-js>
            <div class="px-bk__pick"><div class="px-bk__cal" data-cal></div><div class="px-bk__times" data-times></div></div>
            <div class="px-bk__zones" data-zones role="group" aria-label="Time zone"></div>
          </div>
          <form data-step="details" hidden novalidate>
            <p class="px-bk__when" data-when></p>
            <label class="px-in">Name<input name="name" autocomplete="name"></label>
            <label class="px-in">Email<input name="email" type="email" autocomplete="email"></label>
            <p class="px-err" data-err hidden>Add your name and an email address.</p>
            <div class="px-row"><button type="button" class="btn btn--ghost" data-back>Back</button><button type="submit" class="btn btn--green">Book it</button></div>
          </form>
          <div class="px-bk__done" data-step="done" hidden role="status">
            <h3>{I("check")}You're booked</h3>
            <p class="px-bk__when" data-done-when></p>
            <ol class="px-tl" data-done-line></ol>
            <p class="px-demo-note">This is a demo, so nothing was booked or sent.</p>
            <div class="px-row"><button type="button" class="btn btn--ghost" data-again>Book another</button><a class="btn btn--primary" href="{APP}">Set up yours {I("arrow", "i s14 arr")}</a></div>
          </div>
          <p class="px-nojs">Pick a day and a time, add a name and an email, and the meeting lands on both calendars with a video link.</p>
        </div>
      </div>"""
    hero = f"""    <section class="px-hero" aria-labelledby="pp-h">
      <div class="px-copy">
        <span class="eyebrow">{I("cal", "i s12")}Meetings</span>
        <h1 id="pp-h">Meetings that book themselves</h1>
        <p class="sub">Booking pages, team meetings and booking right inside your forms, on Google and Outlook. Go ahead, book one. These are real dates in your time zone.</p>
        {ctas(("See booking templates", "/templates/group/booking"))}
      </div>
      {widget}
    </section>"""

    stops = [
        ("Mon, 9:12 AM", "Booked", "It lands on both calendars with a video link."),
        ("Right away", "Confirmation", "The invite and the link, in their inbox."),
        ("A day before", "Reminder", "With a link to move or cancel."),
        ("An hour before", "Reminder", "So the call starts on time."),
        ("Tue, 10:30 AM", "The meeting", "Mark it held or a no-show."),
        ("After", "Follow-up", "A thank-you, or the reschedule link after a no-show."),
    ]
    line = "".join(f'<div class="px-stop"><b>{esc(a)}</b><span>{esc(b)}</span><small>{esc(c)}</small></div>' for a, b, c in stops)
    remind = f"""    <section class="px-sec" aria-labelledby="line-h">
      {head_block("Reminders", "mail", "From booked to held, on its own", "Confirmations and reminders go out the moment a call is booked, and stop if it moves or is canceled.", "line-h")}
      <div class="px-line" data-inview>{line}</div>
    </section>"""

    inform = f"""    <section class="px-sec" aria-labelledby="inform-h">
      <div class="px-split px-top">
        <div class="px-copy">
          <span class="eyebrow">{I("form", "i s12")}In the form</span>
          <h2 class="h2" id="inform-h">The calendar is the last step</h2>
          <p class="sub">Most leads leave before they book. Put the calendar inside the form and they pick a time while they're still here. Fill this one in to see.</p>
          <ul class="px-list">{"".join(f'<li>{I("check")}{esc(x)}</li>' for x in ["Name and email filled in for them", "The form picks the meeting, the meeting picks the person", "No second page, no second tool"])}</ul>
        </div>
        <div class="px-live">{live("general-book-a-call")}</div>
      </div>
    </section>"""

    features = caps([
        ("cal", "Google and Outlook", "Connect a calendar in one click. Busy times stay fresh on every calendar you pick.", None),
        ("video", "Video links", "Google Meet, Microsoft Teams or Zoom links on every meeting.", None),
        ("globe", "Their time zone and language", "Times and dates show the way the visitor reads them.", None),
        ("users", "Team meetings", "Round robin with weights, or everyone needed in one meeting.", "Pro"),
        ("grid", "Group meetings", "One host, many guests and a seat limit, like a weekly demo.", "Starter"),
        ("check", "Polls and one-off times", "Offer a few times to a group and book the one that works.", "Starter"),
        ("card", "Paid meetings", "Guests pay with Stripe to book.", "Starter"),
        ("clock", "Hours that fit", "Buffers, notice, a booking window, daily and weekly caps and away days.", None),
        ("hook", "Pages and links", "A page for each person and the team, secret types and single-use links.", "Starter"),
    ])
    main = (
        frame(hero) + frame(remind) + frame(inform)
        + frame(f"""    <section class="px-sec" aria-labelledby="feat-h">
      {head_block("Everything", "check", "Everything in Meetings", "Tags show the plan a feature starts on. The rest is on every plan, Free included.", "feat-h")}
      {features}
    </section>""")
        + frame(f"""    <section class="px-sec" aria-labelledby="tpl-h">
      {head_block("Templates", "form", "Forms that book a meeting", "Each one ends on the calendar. Open one and book a time to see.", "tpl-h")}
      {shelf(["general-book-a-call", "wellness-new-patient", "education-course-inquiry", "beauty-spa-day", "legal-consultation-booking", "hospitality-group-booking"], "See all booking templates", "/templates/group/booking")}
    </section>""")
        + faq([
            ("Which calendars work?", "Google Calendar and Microsoft Outlook, connected in one click. Zoom connects for video links."),
            ("Can I move from Calendly or Cal.com?", "Yes. Bookings from Calendly and Cal.com can come into Claritia while you switch over."),
            ("What is a host?", "Anyone people can book. Each plan includes 1 host, and each extra host is a small monthly price. Everyone else on the team is free."),
            ("Can guests pay to book?", "Yes, on Starter and up. Connect Stripe and set a price on the meeting type."),
        ])
        + theme_data() + "\n" + cta()
    )
    return page("/products/meetings", "Meetings · Claritia", "Claritia Meetings: booking pages, round robin, group meetings, polls and booking inside forms, on Google and Outlook, with reminders built in. Try the live calendar.", main, live_forms=True)


# Routing ------------------------------------------------------------------------------------------------------------

def routing_page():
    q = lambda key, label, opts, on: (
        f'<div class="px-q"><span class="px-label">{esc(label)}</span><div class="px-chips" role="group" aria-label="{esc(label)}" data-q="{key}">'
        + "".join(f'<button type="button" data-v="{v}" aria-pressed="{"true" if v == on else "false"}">{esc(t)}</button>' for v, t in opts)
        + "</div></div>"
    )
    arrow = I("arrow")
    demo = f"""<div class="px-rt" data-route-demo>
        <script type="application/json" data-people>{json.dumps(PEOPLE)}</script>
        <div class="px-rt__lead">
          <span class="eyebrow">{I("user", "i s12")}The lead's answers</span>
          {q("size", "How big is your team?", [("solo", "Just me"), ("small", "2 to 10"), ("mid", "11 to 50"), ("large", "51 or more")], "small")}
          {q("country", "Where are you based?", [("us", "United States"), ("de", "Germany"), ("uk", "United Kingdom")], "us")}
          {q("budget", "What's your budget?", [("low", "Under $1,000"), ("mid", "$1,000 to $10,000"), ("high", "Over $10,000")], "mid")}
          <div class="px-ctas" data-js><button type="button" class="btn btn--primary btn--lg" data-send>Send this lead {I("arrow", "i s14 arr")}</button></div>
        </div>
        <div>
          <span class="eyebrow">{I("route", "i s12")}On submission</span>
          <div class="px-rules" style="margin-top:16px">
            <div class="px-rule is-miss" data-rule><span class="n">1</span><span class="w">If</span>Team size <span class="w">is</span><span class="tag tag--kind">51 or more</span>{arrow}Book <span class="tag tag--green">Enterprise demo</span><span class="w">with the enterprise team</span></div>
            <div class="px-rule is-miss" data-rule><span class="n">2</span><span class="w">If</span>Country <span class="w">is</span><span class="tag tag--kind">Germany</span>{arrow}Book with {person("LK")}</div>
            <div class="px-rule is-miss" data-rule><span class="n">3</span><span class="w">If</span>Budget <span class="w">is</span><span class="tag tag--kind">Under $1,000</span>{arrow}Send the <span class="tag tag--purple">Starter guide</span></div>
            <div class="px-rule is-hit" data-rule><span class="n">4</span><span class="w">Everyone else</span>{arrow}Book <span class="tag tag--green">Sales demo</span><span class="w">and the sales team takes turns</span></div>
            <div class="px-rule px-rule--always"><span class="n">{I("check")}</span><span class="w">Always</span>{arrow}Add to <span class="tag tag--orange">HubSpot</span></div>
          </div>
          <div class="px-out" aria-live="polite">
            <span class="px-label">This lead</span>
            <p class="px-out__what" data-result>Books Sales demo with {person("SB")}</p>
            <p class="px-out__why" data-why>No rule above matched, so the sales team takes turns. Sam Brooks has the fewest meetings this week, and Rae is away.</p>
          </div>
          <div class="px-run" data-js>
            <div><span class="px-label">Sales team this week</span><ul class="px-team" data-team style="margin-top:8px"></ul></div>
            <div><span class="px-label">Leads you sent</span><ul class="px-log" data-log style="margin-top:8px"></ul></div>
          </div>
        </div>
      </div>"""
    hero = f"""    <section class="px-hero px-hero--wide" aria-labelledby="pp-h">
      <div class="px-copy">
        <span class="eyebrow">{I("route", "i s12")}Routing</span>
        <h1 id="pp-h">The right person, every time</h1>
        <p class="sub">Each answer picks the meeting and the person, then the team takes turns fairly. Answer like a lead below and watch the rules decide.</p>
        {ctas()}
      </div>
      {demo}
    </section>"""

    reps = "".join(
        f"""<div class="px-rep" data-rep>
          <span>{person(k)}</span>
          <span class="px-step" role="group" aria-label="{PEOPLE[k][1]}'s weight"><button type="button" data-wless aria-label="Lower weight">&minus;</button><output data-w>1</output><button type="button" data-wmore aria-label="Higher weight">+</button></span>
          <button type="button" data-away aria-pressed="false">Away</button>
          <span class="px-bar"><i data-fill></i></span>
          <span data-n>0</span>
        </div>"""
        for k in ["MO", "LK", "SB", "RJ"]
    )
    rr = f"""    <section class="px-sec" aria-labelledby="rr-h">
      {head_block("Round robin", "users", "Taking turns, fairly", "Give someone a bigger share, mark someone away, then send leads. The person most due gets the next one.", "rr-h")}
      <div class="px-rr" data-rr data-js>
        {reps}
        <div class="px-rr__acts">
          <button type="button" class="btn btn--primary" data-send20>Send 20 leads</button>
          <button type="button" class="btn btn--ghost" data-send1>Send 1</button>
          <button type="button" class="btn btn--plain" data-reset>Reset</button>
          <span>Sent <b data-total>0</b></span>
        </div>
      </div>
      <p class="px-nojs">Weights from 1 to 10 give someone a bigger share. Away days and caps skip them. The person most due gets the next lead.</p>
    </section>"""

    features = caps([
        ("route", "Route by any answer", "Pick the meeting and the person from team size, country, budget or anything else.", "Pro"),
        ("refresh", "Route by past fills", "Someone who filled a form before goes to the same person.", "Pro"),
        ("users", "Round robin", "Even, weighted or by who's free first, with priority tiers.", "Pro"),
        ("grid", "Team pools", "Teams in one place, reused by every meeting that needs them.", "Pro"),
        ("user", "Owner first", "A known lead books with their owner in your CRM, else the pool.", "Business"),
        ("hook", "Two teams at once", "Double round robin books one person from each of two teams.", "Business"),
        ("clock", "Caps and away days", "Limits for a day and a week, and a backup when someone is out.", "Pro"),
        ("search", "A log of every decision", "See which rule picked each person, and why.", "Pro"),
        ("plug", "Always do", "Add every lead to HubSpot, send a guide or post in Slack.", None),
    ])
    main = (
        frame(hero) + frame(rr)
        + frame(f"""    <section class="px-sec" aria-labelledby="feat-h">
      {head_block("Everything", "check", "Everything in Routing", "Tags show the plan a feature starts on. The rest is on every plan, Free included.", "feat-h")}
      {features}
    </section>""")
        + frame(f"""    <section class="px-sec" aria-labelledby="tpl-h">
      {head_block("Templates", "form", "Forms built to qualify", "Each asks what routing needs, then books the right meeting. Open one and try it.", "tpl-h")}
      {shelf(["saas-enterprise-demo", "saas-contact-sales", "agency-project-inquiry", "real-estate-buyer-inquiry", "saas-data-maturity-scorecard", "coaching-discovery-call"], "See all qualification templates", "/templates/category/qualify")}
    </section>""")
        + faq([
            ("Do I need a CRM to route?", "No. Rules read the form's answers. Connect HubSpot or Salesforce on Business to route known leads to their owner."),
            ("Which plan has routing?", "Routing by answer, round robin and team pools are on Pro and up. Owner first and double round robin are on Business."),
            ("What if nobody is free?", "The lead can pick a later time, and the team gets a reminder if a routed lead hasn't booked."),
            ("Can I see why someone got a lead?", "Yes. Every meeting shows the rule that matched and why that person was picked."),
        ])
        + cta()
    )
    return page("/products/routing", "Routing · Claritia", "Claritia Routing: each lead's answers pick the meeting and the person, with round robin, team pools, owner first and a log of every decision. Try the live router.", main)


# The index ------------------------------------------------------------------------------------------------------------

def index_page():
    rows = [
        ("01", "forms", "Forms", "Say what you need and Tia builds it in your brand, with steps, logic, prices and payments.", "Build a form"),
        ("02", "meetings", "Meetings", "Booking pages, team meetings and a calendar inside your forms, with reminders built in.", "Book a meeting"),
        ("03", "routing", "Routing", "Each answer picks the meeting and the person, and the team takes turns fairly.", "Route a lead"),
    ]
    trio = "".join(f'<a href="/products/{k}"><b>{n}</b><h2>{t}</h2><p>{esc(line)}</p><em>{esc(go)} {I("arrow", "i s14 arr")}</em></a>' for n, k, t, line, go in rows)
    main = frame(f"""    <section class="px-hero px-hero--wide" aria-labelledby="pp-h">
      <div class="px-copy">
        <span class="eyebrow">{I("grid", "i s12")}Product</span>
        <h1 id="pp-h">From first click to booked call</h1>
        <p class="sub">Three parts that share one record for every lead. Each page has a demo you can use right now.</p>
        {ctas()}
      </div>
      <div class="px-trio" style="text-align:left">{trio}</div>
    </section>""") + frame(f"""    <section class="px-sec" aria-labelledby="tpl-h">
      {head_block("Templates", "form", "Or start from a template", "Real forms you can fill in now.", "tpl-h")}
      {shelf(["saas-demo-request", "food-catering-calculator", "general-book-a-call"], f"See all {len(tpl.T)} templates", "/templates")}
    </section>""") + cta()
    return page("/products", "Product · Claritia", "Claritia's products: Forms, Meetings and Routing. Forms that turn visitors into leads, meetings that book them and routing that picks the right person.", main)


if __name__ == "__main__":
    (ROOT / "products").mkdir(exist_ok=True)
    (ROOT / "products" / "index.html").write_text(index_page())
    for k, fn in [("forms", forms_page), ("meetings", meetings_page), ("routing", routing_page)]:
        d = ROOT / "products" / k
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(fn())
    print("wrote products/, products/forms, products/meetings, products/routing")
