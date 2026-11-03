"""Builds the product pages: /products (all three), /products/forms, /products/meetings and /products/routing. Each
shows the product drawn in HTML (the same pieces as the home page), what it does, how it fits the other two, and
questions. Plan tags follow docs/pricing.md in the app repo. Run: python3 tools/products.py"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shell  # noqa: E402

esc = shell.esc
I = lambda name, cls="i": f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'
CHECK = '<svg aria-hidden="true"><use href="#i-check"/></svg>'

STYLE = """<style>
.pp-hero{padding:120px var(--frame-pad) 72px;text-align:center}
.pp-hero .display{margin:24px auto 0;max-width:880px}
.pp-hero .sub{margin:20px auto 0;max-width:560px}
.pp-cta{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:32px}
.pp-stage{position:relative;margin-top:56px;padding:40px;border-radius:var(--r-3xl);background:var(--green-100);text-align:left}
.pp-stage__in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;max-width:980px;margin:0 auto}
.pp-card{min-width:0;padding:20px;border-radius:var(--r-lg);background:var(--surface);box-shadow:var(--sh-rest),0 30px 60px -24px rgba(8,60,40,.18)}
.pp-card h4{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:15px;font-weight:500;color:var(--ink)}
.pp-card h4 small{margin-left:auto;font-size:13px;font-weight:400;color:var(--meta)}
.pp-card .fcard{max-width:none;padding:0;box-shadow:none}
.pp-card .rules,.pp-card .flow{max-width:none}
.pp-card .rule{box-shadow:0 0 0 1px rgba(0,0,0,.06)}
.pp-stack{display:flex;flex-direction:column;gap:16px;min-width:0}
.pp-sec{padding:112px var(--frame-pad) 40px}
.pp-sec .shead{margin-bottom:48px}
.pp-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.pp-f{display:flex;flex-direction:column;gap:10px;min-width:0;padding:20px;border-radius:var(--r-lg);background:var(--surface);box-shadow:var(--sh-rest)}
.pp-f__top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.pp-f h3{font-size:16px;line-height:22px;font-weight:500;color:var(--ink)}
.pp-f p{font-size:15px;line-height:22px;color:var(--body);text-wrap:pretty}
.pp-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);align-items:center;gap:56px;padding:96px var(--frame-pad) 40px}
.pp-row--flip .pp-row__text{order:2}
.pp-row__text{display:flex;flex-direction:column;align-items:flex-start;gap:20px;min-width:0}
.pp-row__text .sub{margin-top:-6px}
.pp-list{display:flex;flex-direction:column;gap:10px;margin-top:4px}
.pp-list li{display:flex;align-items:flex-start;gap:10px;font-size:15px;line-height:22px;color:var(--text)}
.pp-list svg{width:16px;height:16px;flex:none;margin-top:3px;color:var(--green)}
.pp-vis{min-width:0;padding:28px;border-radius:var(--r-2xl);background:var(--surface-3);box-shadow:0 0 0 1px rgba(0,0,0,.06);background-image:radial-gradient(circle at 1px 1px,#d9d9d4 1px,transparent 1.2px);background-size:12px 12px}
.pp-vis .pp-card{box-shadow:var(--sh-rest)}
.pp-cal{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:16px;margin-top:14px}
.pp-cal .cal7{margin-top:0}
.pp-times{display:flex;flex-direction:column;gap:6px}
.pp-times b{font-size:13px;font-weight:500;color:var(--text)}
.pp-times button{height:34px;border-radius:var(--r-sm);background:var(--surface);box-shadow:var(--sh-input);font-size:13px;color:var(--text)}
.pp-times button.on{background:var(--green-strong);color:#fff;box-shadow:var(--sh-green)}
.pp-types{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.pp-type{display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding:10px 12px;border-radius:var(--r-md);box-shadow:0 0 0 1px rgba(0,0,0,.06);font-size:14px;color:var(--text)}
.pp-type .grow{flex:1;min-width:120px}
.pp-type small{color:var(--meta);font-size:13px}
.pp-log{display:flex;flex-direction:column;gap:8px;margin-top:14px}
.pp-log div{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:14px;color:var(--text)}
.pp-log svg{width:14px;height:14px;color:var(--green)}
.pp-bars{display:flex;flex-direction:column;gap:12px;margin-top:14px}
.pp-bar{display:grid;grid-template-columns:120px minmax(0,1fr) 44px;align-items:center;gap:10px;font-size:13px;color:var(--text)}
.pp-bar i{display:block;height:8px;border-radius:999px;background:var(--surface-2);overflow:hidden}
.pp-bar i::before{content:"";display:block;height:100%;width:var(--w);border-radius:999px;background:var(--green)}
.pp-bar span:last-child{color:var(--meta);text-align:right;font-variant-numeric:tabular-nums}
.pp-next{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.pp-next a{display:flex;flex-direction:column;gap:10px;min-width:0;padding:20px;border-radius:var(--r-lg);background:var(--surface);box-shadow:var(--sh-rest);transition:box-shadow var(--fast) var(--ease)}
.pp-next a:hover{box-shadow:var(--sh-hover)}
.pp-next b{font-size:16px;font-weight:500;color:var(--ink)}
.pp-next span{font-size:15px;line-height:22px;color:var(--body)}
.pp-next em{margin-top:auto;font-style:normal;font-size:14px;color:var(--ink);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--line-strong)}
.pp-faq .faq{grid-template-columns:minmax(0,1fr)}
@media (min-width:900px){.pp-faq .faq{grid-template-columns:minmax(0,1fr) minmax(0,1.6fr)}}
@media (max-width:1100px){.pp-grid,.pp-next{grid-template-columns:repeat(2,minmax(0,1fr))}.pp-row{gap:32px}}
@media (max-width:900px){
.pp-hero{padding-top:96px}
.pp-stage{padding:16px;margin-top:40px}
.pp-stage__in,.pp-row,.pp-cal{grid-template-columns:minmax(0,1fr)}
.pp-row--flip .pp-row__text{order:0}
.pp-grid,.pp-next{grid-template-columns:minmax(0,1fr)}
.pp-vis{padding:16px}
}
@media (max-width:560px){.pp-hero .display{font-size:40px;line-height:42px}.pp-bar{grid-template-columns:90px minmax(0,1fr) 36px}}
</style>
"""

# Product drawings ---------------------------------------------------------------------------------------------

PERSON = {"MO": ("#0c8c5e", "Maya Ortiz"), "LK": ("#3b6fd8", "Lena Koch"), "SB": ("#c2410c", "Sam Brooks"), "RJ": ("#7c3aed", "Rae Jin")}
person = lambda k: f'<span class="person"><span class="av" style="background:{PERSON[k][0]}">{k}</span>{PERSON[k][1]}</span>'

FORM_CARD = """<div class="pp-card"><div class="fcard">
  <h4>Book a demo</h4>
  <div class="q">How big is your team?</div>
  <div class="opts"><span class="opt"><i></i>Just me</span><span class="opt on"><i></i>2 to 10</span><span class="opt"><i></i>11 to 50</span><span class="opt"><i></i>51 or more</span></div>
  <div class="q">Pick a time</div>
  <div class="slots2"><span class="btn btn--ghost">9:00</span><span class="btn btn--ghost">10:30</span><span class="btn btn--ghost">13:00</span><span class="btn btn--ghost">15:30</span></div>
</div></div>"""

TIA_CARD = f"""<div class="pp-card"><h4><span class="tia-av">{I("spark", "i s12")}</span>Tia</h4>
  <div class="chat" style="margin-top:14px">
    <div class="bubble">Build a catering quote with a price calculator and a deposit</div>
    <div class="tia"><span class="tia-av">{I("spark", "i s12")}</span>Tia built your form</div>
    <div class="steps">
      <div>{I("check", "i s14")}Added 9 questions over 3 steps</div>
      <div>{I("check", "i s14")}Priced each guest and add-on</div>
      <div>{I("check", "i s14")}Took a 20% deposit with Stripe</div>
      <div>{I("check", "i s14")}Matched your site's fonts and colors</div>
    </div>
  </div></div>"""

def CAL_CARD(title="Sales demo", who="30 min, Google Meet"):
    return f"""<div class="pp-card"><h4>{title}<small>{who}</small></h4>
  <div class="pp-cal">
    <div class="cal7"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span>
      <b>2</b><b>3</b><b class="av2">4</b><b class="av2">5</b><b class="av2">6</b><b>7</b><b>8</b>
      <b class="av2">9</b><b class="sel">10</b><b class="av2">11</b><b>12</b><b class="av2">13</b><b>14</b><b>15</b>
      <b class="av2">16</b><b class="av2">17</b><b>18</b><b class="av2">19</b><b class="av2">20</b><b>21</b><b>22</b></div>
    <div class="pp-times"><b>Tue, Nov 10</b><button type="button" tabindex="-1">9:00 AM</button><button type="button" class="on" tabindex="-1">10:30 AM</button><button type="button" tabindex="-1">1:00 PM</button><button type="button" tabindex="-1">3:30 PM</button></div>
  </div></div>"""

TYPES_CARD = f"""<div class="pp-card"><h4>Meeting types</h4>
  <div class="pp-types">
    <div class="pp-type"><span class="grow">Intro call<br><small>One person, 15 min</small></span>{person("MO")}</div>
    <div class="pp-type"><span class="grow">Sales demo<br><small>Round robin, 30 min</small></span>{person("LK")}{person("SB")}</div>
    <div class="pp-type"><span class="grow">Onboarding<br><small>Everyone free, 45 min</small></span>{person("MO")}{person("RJ")}</div>
    <div class="pp-type"><span class="grow">Weekly group demo<br><small>Group, 20 seats</small></span><span class="tag tag--green">12 booked</span></div>
  </div></div>"""

REMIND_CARD = f"""<div class="pp-card"><h4>After booking</h4>
  <div class="flow" style="margin-top:14px">
    <div class="node"><span class="itile" style="width:26px;height:26px">{I("cal", "i s14")}</span>A meeting is booked<small>Start</small></div><div class="link"></div>
    <div class="node">{I("mail")}Confirmation with the invite<small>Now</small></div><div class="link"></div>
    <div class="node">{I("clock")}Reminder<small>1 day before</small></div><div class="link"></div>
    <div class="node">{I("clock")}Reminder<small>1 hour before</small></div>
  </div></div>"""

RULES_CARD = f"""<div class="pp-card"><h4>On submission<small>Demo request</small></h4>
  <div class="rules" style="margin-top:14px">
    <div class="rule"><span class="w">If</span> Team size <span class="w">is</span> <span class="tag tag--kind">51 or more</span>{I("arrow", "i s14")}Book <span class="tag tag--green">Enterprise demo</span></div>
    <div class="rule"><span class="w">If</span> Country <span class="w">is</span> <span class="tag tag--kind">Germany</span>{I("arrow", "i s14")}Book with {person("LK")}</div>
    <div class="rule"><span class="w">If</span> Budget <span class="w">is under</span> <span class="tag tag--kind">$1,000</span>{I("arrow", "i s14")}Send <span class="tag tag--purple">Starter guide</span></div>
    <div class="rule"><span class="w">Everyone else</span>{I("arrow", "i s14")}<span class="tag tag--gray">Sales team, round robin</span></div>
    <div class="rule"><span class="w">Always</span>{I("arrow", "i s14")}Add to <span class="tag tag--orange">HubSpot</span></div>
  </div></div>"""

WHY_CARD = f"""<div class="pp-card"><h4>Why Lena got this lead</h4>
  <div class="pp-log">
    <div>{I("check")}Country is Germany</div>
    <div>{I("check")}Rule 2 picked {person("LK")}</div>
    <div>{I("check")}Free at 10:30 on Tue, Nov 10</div>
    <div>{I("check")}3 of 8 meetings this week</div>
  </div></div>"""

POOL_CARD = """<div class="pp-card"><h4>Sales team<small>Round robin this week</small></h4>
  <div class="pp-bars">
    <div class="pp-bar"><span>Maya Ortiz</span><i style="--w:62%"></i><span>5 of 8</span></div>
    <div class="pp-bar"><span>Lena Koch</span><i style="--w:38%"></i><span>3 of 8</span></div>
    <div class="pp-bar"><span>Sam Brooks</span><i style="--w:50%"></i><span>4 of 8</span></div>
    <div class="pp-bar"><span>Rae Jin</span><i style="--w:0%"></i><span>Away</span></div>
  </div></div>"""

RESULTS_CARD = f"""<div class="pp-card"><h4>{I("table", "i s14")}Submissions<small>Example data</small></h4>
  <div class="pp-types">
    <div class="pp-type"><span class="grow">Priya Raman<br><small>2 to 10, Germany</small></span><span class="tag tag--green">Booked</span></div>
    <div class="pp-type"><span class="grow">Jonas Weber<br><small>51 or more, US</small></span><span class="tag tag--green">Booked</span></div>
    <div class="pp-type"><span class="grow">Ana Souza<br><small>Catering quote, $2,480</small></span><span class="tag tag--orange">Deposit paid</span></div>
    <div class="pp-type"><span class="grow">Tom Hall<br><small>Left at step 2</small></span><span class="tag tag--gray">Left early</span></div>
  </div></div>"""

# Pages ----------------------------------------------------------------------------------------------------------

PAGES = {
    "forms": {
        "name": "Forms", "icon": "form", "menu": "Steps, logic and prices",
        "title": "Forms that turn visitors into leads",
        "sub": "Describe the form you need and Tia builds it in your brand. Steps, logic, prices and payments, with the meeting booked before they leave.",
        "desc": "Claritia Forms: describe a form and get it built in your brand, with steps, logic, prices, payments, signatures and booking inside the form. Free to start.",
        "stage": [TIA_CARD, FORM_CARD],
        "features": [
            ("spark", "Built from a sentence", "Tell Tia what you need. She writes the questions, the steps and the ending.", None),
            ("type", "15 field types", "Text, email, phone, choices, dates, ratings, scales, addresses, file uploads and consent.", None),
            ("route", "Logic that skips ahead", "Show a question or skip a step from any earlier answer.", None),
            ("grid", "Prices and calculations", "Quotes, estimates and scores that add up as people answer.", None),
            ("card", "Payments", "Take a full payment or a deposit with Stripe.", "Starter"),
            ("sign", "Signatures", "People sign right in the form.", "Starter"),
            ("cal", "Booking inside the form", "The calendar is the last step, so a lead picks a time before leaving.", None),
            ("globe", "Your brand, copied in", "Tia reads your site and matches its fonts, colors and buttons.", None),
            ("table", "435 templates", "Demo requests, quotes, intake, applications and more, in 18 styles.", None),
        ],
        "rows": [
            ("Build", "spark", "Describe it. Tia builds it.", "Say what the form is for. Tia asks what's missing, then writes it, links a meeting and drafts the follow-ups.",
             ["One chat per form, kept with the form", "Change anything by asking, or edit it by hand", "Translate a form in one step", "Start from 435 templates in 85 categories"], TIA_CARD),
            ("Share", "globe", "Put it anywhere", "One link, one script tag or a popup. It looks like your site wherever it goes.",
             ["A share link and a QR code", "Embed inline or as a popup with one line", "Your own domain on Business", "Works on phones and by keyboard"], FORM_CARD),
            ("Results", "table", "Every answer in one place", "Each fill is saved with the page it came from, the UTM tags and what happened next.",
             ["Views, starts and fills for each form", "Spam held back by Cloudflare Turnstile and a honeypot", "Consent saved with the exact wording shown", "CSV export, and Left early on Business"], RESULTS_CARD),
        ],
        "faq": [
            ("Can I keep my current forms?", "Yes. Fills from HubSpot, Webflow, Typeform and Tally forms can come into Claritia, so they book and follow up the same way."),
            ("Where do the answers go?", "Into Claritia first, then to the tools you connect: HubSpot, Salesforce, Google Sheets, Airtable, Notion, Slack, email lists and webhooks."),
            ("How many forms can I make?", "As many as you like, on every plan. Plans differ by submissions a month: 250 on Free, 2,000 on Starter, 5,000 on Pro and unlimited on Business."),
            ("Does it stop spam?", "Yes. Cloudflare Turnstile, a hidden honeypot, a limit per network and disposable email checks hold spam back for you to review."),
        ],
    },
    "meetings": {
        "name": "Meetings", "icon": "cal", "menu": "Booking pages and team pools",
        "title": "Meetings that book themselves",
        "sub": "Booking pages, team meetings and booking right inside your forms, on Google and Outlook calendars, with reminders that go out on their own.",
        "desc": "Claritia Meetings: booking pages, round robin, group meetings, polls and booking inside forms, on Google and Outlook, with reminders built in. Free to start.",
        "stage": [CAL_CARD(), TYPES_CARD],
        "features": [
            ("cal", "Google and Outlook", "Connect a calendar in one click. Busy times stay fresh on every calendar you pick.", None),
            ("video", "Video links", "Google Meet, Microsoft Teams or Zoom links added to every meeting.", None),
            ("form", "Booking inside forms", "The form picks the meeting, so leads book before they leave the page.", None),
            ("users", "Team meetings", "Round robin with weights, or everyone needed in one meeting.", "Pro"),
            ("grid", "Group meetings", "One host, many guests and a seat limit, like a weekly demo.", "Starter"),
            ("check", "Polls and one-off times", "Offer a few times to a group and book the one that works.", "Starter"),
            ("card", "Paid meetings", "Guests pay with Stripe to book.", "Starter"),
            ("clock", "Hours that fit", "Buffers, notice, a booking window, daily and weekly caps and away days.", None),
            ("mail", "Reminders built in", "A confirmation with the invite, then reminders a day and an hour before.", None),
        ],
        "rows": [
            ("Book", "cal", "A booking page that looks like you", "Each person and each team gets a page. Times show in the visitor's own time zone and language.",
             ["Pages for each person and the whole team", "Secret meeting types shared only by link", "Single-use links for one lead", "Copy open times into an email"], CAL_CARD("Onboarding", "45 min, Zoom")),
            ("Types", "users", "Every kind of meeting", "One person, round robin, everyone free, owner first or a group. Pick the length, place and questions.",
             ["Lengths the guest can pick from", "Google Meet, Teams, Zoom, phone or in person", "Questions on the booking page, skipped when the form asked", "Reschedule with the same host or anyone in the pool"], TYPES_CARD),
            ("Remind", "mail", "No more no-shows", "Confirmations and reminders go out the moment a call is booked, and stop if it moves or is canceled.",
             ["Your own wording and times on Starter and up", "A follow-up after the meeting", "A no-show email with the reschedule link on Pro", "Workflows for anything else"], REMIND_CARD),
        ],
        "faq": [
            ("Which calendars work?", "Google Calendar and Microsoft Outlook, connected in one click. Zoom connects for video links."),
            ("Can I move from Calendly or Cal.com?", "Yes. Bookings from Calendly and Cal.com can come into Claritia while you switch over."),
            ("What is a host?", "Anyone people can book. Each plan includes 1 host, and each extra host is a small monthly price. Everyone else on the team is free."),
            ("Can guests pay to book?", "Yes, on Starter and up. Connect Stripe and set a price on the meeting type."),
        ],
    },
    "routing": {
        "name": "Routing", "icon": "route", "menu": "The right person every time",
        "title": "The right person every time",
        "sub": "Send each lead to the right meeting and the right person from what they wrote, then share the work fairly across your team.",
        "desc": "Claritia Routing: route each lead by its answers to the right meeting and person, with round robin, team pools, owner first and a log of every decision.",
        "stage": [RULES_CARD, '<div class="pp-stack">' + WHY_CARD + POOL_CARD + "</div>"],
        "features": [
            ("route", "Route by any answer", "Pick the meeting and the person from team size, country, budget or anything else.", "Pro"),
            ("refresh", "Route by past fills", "Someone who filled a form before goes to the same person.", "Pro"),
            ("users", "Round robin", "Even, weighted or by who's free first, with priority tiers.", "Pro"),
            ("grid", "Team pools", "Teams in one place, reused by every meeting that needs them.", "Pro"),
            ("user", "Owner first", "A known lead books with their owner in your CRM, else the pool.", "Business"),
            ("users", "Two teams at once", "Double round robin books one person from each of two teams.", "Business"),
            ("clock", "Caps and away days", "Limits for a day and a week, and a backup when someone is out.", "Pro"),
            ("search", "A log of every decision", "See which rule picked each person, and why.", "Pro"),
            ("plug", "Always do", "Add every lead to HubSpot, send a guide or post in Slack.", None),
        ],
        "rows": [
            ("Rules", "route", "The form picks the meeting", "Rules read the answers in order. The first that matches decides the meeting, the person or the next step.",
             ["Is, is not, filled and empty on any field", "Book, book with a person, or send something", "Everyone else goes to a team", "Always do runs for every lead"], RULES_CARD),
            ("Teams", "users", "The meeting picks the person", "A team meeting takes turns fairly, and skips anyone who's away or at their cap.",
             ["Weights from 1 to 10 and priority tiers", "Flexible shows every free time, strict shows the next in line", "Caps for a day and a week", "Away days with a backup"], POOL_CARD),
            ("Trust", "search", "See why, every time", "Every lead keeps a short log of the rule that matched and the person it picked.",
             ["On the meeting's own page", "A Slack note to the host", "A reminder when a routed lead hasn't booked", "Fix a rule and the next lead follows it"], WHY_CARD),
        ],
        "faq": [
            ("Do I need a CRM to route?", "No. Rules read the form's answers. Connect HubSpot or Salesforce on Business to route known leads to their owner."),
            ("Which plan has routing?", "Routing by answer, round robin and team pools are on Pro and up. Owner first and double round robin are on Business."),
            ("What if nobody is free?", "The lead can pick a later time, and the team gets a reminder if a routed lead hasn't booked."),
            ("Can I see why someone got a lead?", "Yes. Every meeting shows the rule that matched and why that person was picked."),
        ],
    },
}
ORDER = ["forms", "meetings", "routing"]


def tag(plan):
    return f'<span class="tag tag--green">{plan}</span>' if plan else ""


def head_block(eyebrow, icon, title, sub, h_id):
    return f"""<div class="shead">
        <span class="eyebrow">{I(icon, "i s12")}{esc(eyebrow)}</span>
        <h2 class="h2" id="{h_id}">{title}</h2>
        <p class="sub">{esc(sub)}</p>
      </div>"""


def faq_html(items):
    plus = '<svg aria-hidden="true"><use href="#i-plus"/></svg>'
    return "".join(f"<details><summary>{esc(q)} {plus}</summary><p>{esc(a)}</p></details>" for q, a in items)


def next_cards(skip):
    cards = []
    for k in ORDER:
        if k == skip:
            continue
        p = PAGES[k]
        cards.append(f'<a href="/products/{k}"><span class="itile">{I(p["icon"])}</span><b>{p["name"]}</b><span>{esc(p["menu"])}</span><em>See {p["name"]}</em></a>')
    cards.append(f'<a href="/pricing"><span class="itile">{I("card")}</span><b>Pricing</b><span>Free for one host. Pay for hosts, not seats.</span><em>See pricing</em></a>')
    return "".join(cards)


def band():
    return '<div class="band"><div class="frame"></div></div>'


def cta():
    return shell.absolute(shell.block("<!-- The last prompt, on dark -->", "</section>\n    </div>\n  </div>"))


def product_page(key):
    p = PAGES[key]
    feats = "".join(
        f'<article class="pp-f"><div class="pp-f__top"><span class="itile">{I(ic)}</span>{tag(plan)}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></article>'
        for ic, t, d, plan in p["features"]
    )
    rows = []
    for n, (eb, ic, h, sub, items, vis) in enumerate(p["rows"]):
        lis = "".join(f"<li>{CHECK}{esc(x)}</li>" for x in items)
        rows.append(f"""  <div class="frame">
    <section class="pp-row{' pp-row--flip' if n % 2 else ''}" aria-labelledby="row-{n}">
      <div class="pp-row__text">
        <span class="eyebrow">{I(ic, "i s12")}{esc(eb)}</span>
        <h2 class="h2" id="row-{n}">{esc(h)}</h2>
        <p class="sub">{esc(sub)}</p>
        <ul class="pp-list">{lis}</ul>
      </div>
      <div class="pp-vis" aria-hidden="true">{vis}</div>
    </section>
  </div>
  {band()}""")
    main = f"""  <div class="frame">
    <section class="pp-hero" aria-labelledby="pp-h">
      <span class="eyebrow">{I(p["icon"], "i s12")}{p["name"]}</span>
      <h1 class="display" id="pp-h">{esc(p["title"])}</h1>
      <p class="sub">{esc(p["sub"])}</p>
      <div class="pp-cta">
        <a class="btn btn--primary btn--lg" href="https://app.tryclaritia.com">Start free {I("arrow", "i s14 arr")}</a>
        <a class="btn btn--ghost btn--lg" href="/pricing">See pricing</a>
      </div>
      <div class="pp-stage" aria-hidden="true"><div class="pp-stage__in">{"".join(p["stage"])}</div></div>
    </section>
  </div>
  {band()}

  <div class="frame">
    <section class="pp-sec" aria-labelledby="feat-h">
      {head_block("What you get", "check", f"Everything in {p['name']}", "Tags show the plan a feature starts on. The rest is on every plan, Free included.", "feat-h")}
      <div class="pp-grid">{feats}</div>
    </section>
  </div>
  {band()}

{chr(10).join(rows)}

  <div class="frame">
    <section class="pp-sec" aria-labelledby="next-h">
      {head_block("One product", "bolt", "Works with the rest of Claritia", "Forms, meetings and routing share one record for every lead.", "next-h")}
      <div class="pp-next">{next_cards(key)}</div>
    </section>
  </div>
  {band()}

  <div class="frame pp-faq">
    <section class="pp-sec" aria-labelledby="faq-h">
      <div class="faq">
        <div class="faq__head">
          <h2 class="h2" id="faq-h">Questions</h2>
          <p class="lead">Something else? <a href="mailto:hello@tryclaritia.com">hello@tryclaritia.com</a></p>
        </div>
        <div class="qa">{faq_html(p["faq"])}</div>
      </div>
    </section>
  </div>

{cta()}"""
    return shell.head(f"{p['name']} · Claritia", p["desc"], f"/products/{key}", STYLE) + "\n" + shell.body(main)


def index_page():
    cards = "".join(
        f'<a href="/products/{k}"><span class="itile">{I(PAGES[k]["icon"])}</span><b>{PAGES[k]["name"]}</b><span>{esc(PAGES[k]["sub"])}</span><em>See {PAGES[k]["name"]}</em></a>'
        for k in ORDER
    )
    main = f"""  <div class="frame">
    <section class="pp-hero" aria-labelledby="pp-h">
      <span class="eyebrow">{I("grid", "i s12")}Product</span>
      <h1 class="display" id="pp-h">From first click to booked call</h1>
      <p class="sub">Forms that turn visitors into leads, meetings that book them with the right person, and routing that picks who.</p>
      <div class="pp-cta">
        <a class="btn btn--primary btn--lg" href="https://app.tryclaritia.com">Start free {I("arrow", "i s14 arr")}</a>
        <a class="btn btn--ghost btn--lg" href="/pricing">See pricing</a>
      </div>
      <div class="pp-next" style="margin-top:56px;text-align:left">{cards}</div>
      <div class="pp-stage" aria-hidden="true"><div class="pp-stage__in">{FORM_CARD}{RULES_CARD}</div></div>
    </section>
  </div>

{cta()}"""
    desc = "Claritia's products: Forms, Meetings and Routing. Forms that turn visitors into leads, meetings that book them and routing that picks the right person."
    return shell.head("Product · Claritia", desc, "/products", STYLE) + "\n" + shell.body(main)


if __name__ == "__main__":
    (ROOT / "products").mkdir(exist_ok=True)
    (ROOT / "products" / "index.html").write_text(index_page())
    for k in ORDER:
        d = ROOT / "products" / k
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(product_page(k))
    print("wrote products/ and", ", ".join(f"products/{k}" for k in ORDER))
