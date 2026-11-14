"""Builds the product pages: /products, /products/forms, /products/meetings and /products/routing. Laid out like
Arrowsterr's platform pages: a centered hero with the app drawn in HTML, the tools it works with, the old way next to
the Claritia way, four features each beside a small part of the app, how it works, templates and the dark close. All
static, nothing to operate. Styles in assets/products.css. Plan tags follow docs/pricing.md in the app repo.
Run: python3 tools/products.py"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shell  # noqa: E402
import templates as tpl  # noqa: E402

PX_V = 2
esc = shell.esc
APP = "https://app.tryclaritia.com"
BY = {t["slug"]: t for t in tpl.T}
I = lambda name, cls="i": f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'
PEOPLE = {"MO": ("#0c8c5e", "Maya Ortiz"), "LK": ("#3b6fd8", "Lena Koch"), "SB": ("#c2410c", "Sam Brooks"), "RJ": ("#7c3aed", "Rae Jin")}
person = lambda k: f'<span class="person"><span class="av" style="background:{PEOPLE[k][0]}">{k}</span>{PEOPLE[k][1]}</span>'
logo = lambda f, n: f'<img src="/assets/logos/{f}" alt="" width="18" height="18" loading="lazy">'
band = lambda: '<div class="band"><div class="frame"></div></div>'
frame = lambda inner: f'  <div class="frame">\n{inner}\n  </div>\n  {band()}\n'


# The app, drawn -------------------------------------------------------------------------------------------------

def app(url, on, head, inner, one=False):
    nav = [("form", "Forms"), ("cal", "Meetings"), ("flow", "Workflows")]
    items = "".join(f'<span class="pd-nav{" is-on" if n == on else ""}">{I(ic)}{n}</span>' for ic, n in nav)
    return f"""<div class="pd-app" aria-hidden="true">
        <div class="pd-app__bar"><i></i><i></i><i></i><span>{esc(url)}</span></div>
        <div class="pd-app__body">
          <div class="pd-side"><div class="pd-side__ws"><svg aria-hidden="true"><use href="#mark"/></svg>Acme</div>{items}<span class="pd-nav pd-nav--end">{I("side")}Settings</span></div>
          <div class="pd-main">
            <div class="pd-main__head">{head}</div>
            <div class="pd-main__in{' pd-main__in--one' if one else ''}">{inner}</div>
          </div>
        </div>
      </div>"""


def tabs(items, on):
    return '<div class="pd-tabs">' + "".join(f'<span{" class=\"is-on\"" if t == on else ""}>{t}</span>' for t in items) + "</div>"


def card(title, body, note=""):
    return f'<div class="pd-card" aria-hidden="true"><div class="pd-card__h">{title}{f"<small>{note}</small>" if note else ""}</div>{body}</div>'


TIA = f"""<div class="chat" style="margin-top:0">
      <div class="bubble">Build a demo request form that books a call with sales</div>
      <div class="tia"><span class="tia-av">{I("spark", "i s12")}</span>Tia built your form</div>
      <div class="steps">
        <div>{I("check", "i s14")}Added 8 questions over 2 pages</div>
        <div>{I("check", "i s14")}Linked the Sales demo meeting</div>
        <div>{I("check", "i s14")}Drafted a follow-up email</div>
        <div>{I("check", "i s14")}Matched your site's fonts and colors</div>
      </div>
    </div>"""

FORM = """<div class="fcard">
      <h4>Book a demo</h4>
      <div class="q">How big is your team?</div>
      <div class="opts"><span class="opt"><i></i>Just me</span><span class="opt on"><i></i>2 to 10</span><span class="opt"><i></i>11 to 50</span><span class="opt"><i></i>51 or more</span></div>
      <div class="q">Pick a time</div>
      <div class="slots2"><span class="btn btn--ghost">9:00</span><span class="btn btn--ghost">10:30</span><span class="btn btn--ghost">13:00</span><span class="btn btn--ghost">15:30</span></div>
    </div>"""

CAL = """<div class="pd-cal">
      <div class="cal7"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span>
        <b>2</b><b>3</b><b class="av2">4</b><b class="av2">5</b><b class="av2">6</b><b>7</b><b>8</b>
        <b class="av2">9</b><b class="sel">10</b><b class="av2">11</b><b>12</b><b class="av2">13</b><b>14</b><b>15</b>
        <b class="av2">16</b><b class="av2">17</b><b>18</b><b class="av2">19</b><b class="av2">20</b><b>21</b><b>22</b></div>
      <div class="pd-times"><b>Tue, Nov 10</b><span>9:00 AM</span><span class="on">10:30 AM</span><span>1:00 PM</span><span>3:30 PM</span></div>
    </div>"""

RULES = f"""<div class="rules">
      <div class="rule"><span class="w">If</span> Team size <span class="w">is</span> <span class="tag tag--kind">51 or more</span>{I("arrow", "i s14")}Book <span class="tag tag--green">Enterprise demo</span></div>
      <div class="rule"><span class="w">If</span> Country <span class="w">is</span> <span class="tag tag--kind">Germany</span>{I("arrow", "i s14")}Book with {person("LK")}</div>
      <div class="rule"><span class="w">If</span> Budget <span class="w">is under</span> <span class="tag tag--kind">$1,000</span>{I("arrow", "i s14")}Send <span class="tag tag--purple">Starter guide</span></div>
      <div class="rule"><span class="w">Everyone else</span>{I("arrow", "i s14")}<span class="tag tag--gray">Sales team, round robin</span></div>
      <div class="rule"><span class="w">Always</span>{I("arrow", "i s14")}Add to <span class="tag tag--orange">HubSpot</span></div>
    </div>"""

WHY = f"""<div class="pd-log">
      <div>{I("check")}Country is Germany</div>
      <div>{I("check")}Rule 2 picked {person("LK")}</div>
      <div>{I("check")}Free at 10:30 on Tue, Nov 10</div>
      <div>{I("check")}3 of 8 meetings this week</div>
    </div>"""

POOL = """<div class="pd-bars">
      <div class="pd-bar"><span>Maya Ortiz</span><i style="--w:62%"></i><span>5 of 8</span></div>
      <div class="pd-bar"><span>Lena Koch</span><i style="--w:38%"></i><span>3 of 8</span></div>
      <div class="pd-bar"><span>Sam Brooks</span><i style="--w:50%"></i><span>4 of 8</span></div>
      <div class="pd-bar"><span>Rae Jin</span><i style="--w:0%"></i><span>Away</span></div>
    </div>"""

REMIND = f"""<div class="flow">
      <div class="node"><span class="itile" style="width:26px;height:26px">{I("cal", "i s14")}</span>A meeting is booked<small>Start</small></div><div class="link"></div>
      <div class="node">{I("mail")}Confirmation with the invite<small>Now</small></div><div class="link"></div>
      <div class="node">{I("clock")}Reminder<small>1 day before</small></div><div class="link"></div>
      <div class="node">{I("clock")}Reminder<small>1 hour before</small></div>
    </div>"""


def rows(items):
    return '<div class="pd-rows">' + "".join(f"<div>{x}</div>" for x in items) + "</div>"


# Page parts -------------------------------------------------------------------------------------------------------

def hero(icon, name, title, sub, second, shot):
    return f"""    <section class="pd-hero" aria-labelledby="pp-h">
      <span class="eyebrow">{I(icon, "i s12")}{esc(name)}</span>
      <h1 id="pp-h">{esc(title)}</h1>
      <p class="sub">{esc(sub)}</p>
      <div class="pd-ctas">
        <a class="btn btn--primary btn--lg" href="{APP}/signup">Start free {I("arrow", "i s14 arr")}</a>
        <a class="btn btn--ghost btn--lg" href="{second[1]}">{esc(second[0])}</a>
      </div>
      <p class="pd-note">Free plan. No card needed.</p>
      {shot}
    </section>
    <div class="pd-logos">
      <p>Works with</p>
      <ul>{"".join(f'<li>{logo(f, n)}{esc(n)}</li>' for f, n in WORKS[name])}</ul>
    </div>"""


WORKS = {
    "Forms": [("hubspot.svg", "HubSpot"), ("salesforce.svg", "Salesforce"), ("slack.svg", "Slack"), ("stripe.svg", "Stripe"), ("webflow.svg", "Webflow"), ("wordpress.svg", "WordPress"), ("framer.svg", "Framer"), ("typeform.svg", "Typeform")],
    "Meetings": [("calendar.svg", "Google Calendar"), ("outlook.jpg", "Outlook"), ("meet.svg", "Google Meet"), ("teams.png", "Microsoft Teams"), ("zoom.svg", "Zoom"), ("stripe.svg", "Stripe"), ("calendly.svg", "Calendly")],
    "Routing": [("hubspot.svg", "HubSpot"), ("salesforce.svg", "Salesforce"), ("omniscient.svg", "Omniscient"), ("slack.svg", "Slack"), ("calendar.svg", "Google Calendar"), ("outlook.jpg", "Outlook")],
}


def then_now(title_h, sub, old, new):
    o = "<i></i>".join(f"<div>{I(ic)}{esc(t)}<small>{esc(n)}</small></div>" for ic, t, n in old)
    w = "<i></i>".join(f"<div>{I(ic)}{esc(t)}<small>{esc(n)}</small></div>" for ic, t, n in new)
    return f"""    <section class="pd-sec" aria-labelledby="then-h">
      <div class="pd-head"><span class="eyebrow">{I("bolt", "i s12")}Why Claritia</span><h2 class="h2" id="then-h">{title_h}</h2><p class="sub">{esc(sub)}</p></div>
      <div class="pd-then">
        <div><h3>Before</h3><div class="pd-chain pd-chain--old">{o}</div></div>
        <div><h3>With Claritia</h3><div class="pd-chain pd-chain--new">{w}</div></div>
      </div>
    </section>"""


def features(title_h, items):
    out = []
    for n, (h, p, plan, vis) in enumerate(items):
        tag = f'<span class="tag tag--green">{esc(plan)}</span>' if plan else ""
        out.append(f'<div class="pd-feat{" pd-feat--flip" if n % 2 else ""}"><div class="pd-feat__text">{tag}<h3>{esc(h)}</h3><p>{esc(p)}</p></div>{vis}</div>')
    return f"""    <section class="pd-sec" aria-labelledby="feat-h">
      <div class="pd-head"><span class="eyebrow">{I("check", "i s12")}Features</span><h2 class="h2" id="feat-h">{title_h}</h2></div>
      <div class="pd-feats">{"".join(out)}</div>
    </section>"""


def how(title_h, steps, vis):
    li = "".join(f'<li><b>0{i + 1}</b><h3>{esc(h)}</h3><p>{esc(p)}</p></li>' for i, (h, p) in enumerate(steps))
    return f"""    <section class="pd-sec" aria-labelledby="how-h">
      <div class="pd-head"><span class="eyebrow">{I("flow", "i s12")}How it works</span><h2 class="h2" id="how-h">{title_h}</h2></div>
      <div class="pd-how"><ol class="pd-steps">{li}</ol>{vis}</div>
    </section>"""


def shelf(title_h, sub, slugs, more_label, more_href):
    items = []
    for s in slugs:
        t = BY[s]
        pages = len(t["schema"]["pages"])
        meta = f"{tpl.questions(t)} questions" + (f", {pages} pages" if pages > 1 else "")
        items.append(f'<a class="pd-tpl" href="/templates/{s}">{tpl.thumb(t)}<b>{esc(t["name"])}</b><span class="pd-meta">{esc(meta)}</span></a>')
    return f"""    <section class="pd-sec" aria-labelledby="tpl-h">
      <div class="pd-head"><span class="eyebrow">{I("form", "i s12")}Templates</span><h2 class="h2" id="tpl-h">{title_h}</h2><p class="sub">{esc(sub)}</p></div>
      <div class="pd-shelf">{"".join(items)}</div>
      <div class="pd-more"><a class="btn btn--ghost btn--lg" href="{more_href}">{esc(more_label)} {I("arrow", "i s14 arr")}</a></div>
    </section>"""


def cta():
    return shell.LAST_PROMPT


def page(slug, title, desc, main):
    extra = (f'<link rel="stylesheet" href="{tpl.FONTS_URL}">\n<link rel="stylesheet" href="/assets/forms.css?v={tpl.CSS_V}">\n'
             f'<link rel="stylesheet" href="/assets/themes.css?v={tpl.CSS_V}">\n<link rel="stylesheet" href="/assets/products.css?v={PX_V}">\n')
    return shell.head(title, desc, slug, extra) + "\n" + shell.body(main)


# Forms -----------------------------------------------------------------------------------------------------------

def forms_page():
    shot = app("app.tryclaritia.com/forms", "Forms",
               f'<b>Demo request</b>{tabs(["Build", "Submissions", "Share", "Settings"], "Build")}<span class="pd-main__end"><span class="tag tag--green">Live</span><span class="pd-pill">Publish</span></span>',
               card("Tia", TIA) + card("Preview", FORM, "Midnight style"))
    hogan = rows([
        f'<span class="grow"><b>Priya Raman</b><small>2 to 10, Germany</small></span>{person("LK")}<span class="tag tag--green">Booked</span>',
        f'<span class="grow"><b>Jonas Weber</b><small>51 or more, United States</small></span>{person("MO")}<span class="tag tag--green">Booked</span>',
        f'<span class="grow"><b>Ana Souza</b><small>Catering quote, $2,480</small></span>{logo("stripe.svg", "")}<span class="tag tag--orange">Deposit paid</span>',
        f'<span class="grow"><b>Tom Hall</b><small>Under $1,000</small></span>{logo("hubspot.svg", "")}<span class="tag tag--gray">Guide sent</span>',
    ])
    price = rows([
        '<span class="grow">Guests</span><span class="pd-num">40</span>',
        '<span class="grow">Plated dinner<small>$52 a guest</small></span><span class="pd-num">$2,080</span>',
        '<span class="grow">Open bar<small>Shown if Bar is Yes</small></span><span class="pd-num">$480</span>',
        '<span class="grow"><b>Total</b></span><b>$2,560</b>',
        '<span class="grow">Deposit today<small>20%, with Stripe</small></span><b style="color:var(--green-ink)">$512</b>',
    ])
    brand = ('<span class="pd-label">Colors</span><div class="pd-sw"><i style="background:#0f1630"></i><i style="background:#5b8cff"></i><i style="background:#f4f6ff"></i><i style="background:#ffffff"></i></div>'
             '<span class="pd-label">Font</span><div class="pd-field"><span>Inter, 15px</span></div>'
             '<span class="pd-label">Buttons</span><div class="pd-field"><span>Rounded, filled, white text</span></div>'
             '<span class="pd-label">Fields</span><div class="pd-field"><span>8px corners, soft line</span></div>')
    share = ('<span class="pd-label">Link</span><div class="pd-field"><span>forms.tryclaritia.com/acme/demo-request</span></div>'
             '<span class="pd-label">Embed</span><div class="pd-code">&lt;script src="https://app.tryclaritia.com/forms/v1.js" async&gt;&lt;/script&gt;\n&lt;claritia-form form-id="demo-request"&gt;&lt;/claritia-form&gt;</div>'
             '<span class="pd-label">Shows as</span><div class="pd-tabs"><span class="is-on">In the page</span><span>Popup</span><span>Slide in</span><span>Corner button</span><span>Side tab</span></div>')
    main = (
        frame(hero("form", "Forms", "Forms that turn visitors into leads", "Describe the form you need and Tia builds it in your brand, with pages, logic, prices and payments, and the meeting booked at the end.", ("See all templates", "/templates"), shot))
        + frame(then_now("Instead of a form tool, a scheduler and a spreadsheet, one place for every lead", "Each answer, booking and follow-up stays on the same record.",
                         [("form", "Build the form in one tool", "Copy and paste"), ("cal", "Send a booking link by email", "Half never book"), ("table", "Paste answers into a sheet", "By hand"), ("mail", "Write each follow-up", "Often late")],
                         [("spark", "Tia builds the form", "In minutes"), ("cal", "The calendar is the last page", "Booked on the page"), ("table", "Every answer saved and synced", "On its own"), ("mail", "Follow-ups go out", "On time")]))
        + frame(features("Everything you need to turn a visit into a lead", [
            ("Describe it, and Tia builds it", "Say what the form is for. Tia asks what's missing, writes the questions and pages, links a meeting and drafts the follow-ups. Change anything by asking.", None, card("Tia", TIA)),
            ("Logic, prices and payments", "Show a question only when an earlier answer calls for it. Price every option as people answer, and take a payment or a deposit with Stripe.", "Payments on Starter", card("Catering quote", price, "Example")),
            ("It looks like your website", "Tia reads your site and copies its colors, fonts, buttons and fields. Or start from one of 18 styles.", None, card("Read from acme.com", brand)),
            ("Every answer, ready to use", "Each fill is saved with the page and campaign it came from, then sent to HubSpot, Salesforce, Google Sheets, Slack or your email list.", None, card("Submissions", hogan, "Example data")),
        ]))
        + frame(how("From one sentence to live in minutes", [
            ("Describe the form", "Tell Tia who it's for and what it needs to ask. Or pick one of 435 templates."),
            ("Make it yours", "Your style, your logic, your thank-you screen and the meeting it books."),
            ("Share it or put it on your site", "A link, a QR code, or one line of code for any website."),
            ("Watch the leads come in", "Answers land in Submissions and in the tools you connect."),
        ], card("Share", share)))
        + frame(shelf("Start from a template", "Real forms in 85 categories, each free on every plan.", ["food-catering-calculator", "agency-project-inquiry", "healthcare-patient-intake", "construction-roof-inspection", "creative-photo-session", "events-registration"], f"See all {len(tpl.T)} templates", "/templates"))
        + cta()
    )
    return page("/products/forms", "Forms · Claritia", f"Claritia Forms: describe a form and Tia builds it in your brand, with steps, logic, prices, payments and booking at the end. {len(tpl.T)} free templates.", main)


# Meetings ----------------------------------------------------------------------------------------------------------

def meetings_page():
    upcoming = rows([
        f'<span class="pd-num">Tue 9:30</span><span class="grow"><b>Priya Raman</b><small>Sales demo</small></span>{person("LK")}<span class="tag tag--green">Confirmed</span>',
        f'<span class="pd-num">Tue 11:00</span><span class="grow"><b>Jonas Weber</b><small>Enterprise demo</small></span>{person("MO")}<span class="tag tag--green">Confirmed</span>',
        f'<span class="pd-num">Wed 2:00</span><span class="grow"><b>Weekly group demo</b><small>12 of 20 seats</small></span>{person("SB")}<span class="tag tag--kind">Group</span>',
        f'<span class="pd-num">Thu 10:30</span><span class="grow"><b>Mei Tanaka</b><small>Intro call</small></span>{person("RJ")}<span class="tag tag--gray">Moved</span>',
    ])
    stats = '<div class="pd-stats"><div class="pd-stat"><small>Booked this week</small><b>24</b></div><div class="pd-stat"><small>Held</small><b>19</b></div><div class="pd-stat"><small>From forms</small><b>17</b></div></div>'
    shot = app("app.tryclaritia.com/meetings", "Meetings",
               f'<b>Meetings</b>{tabs(["Upcoming", "Meeting types", "Availability", "Booking page"], "Upcoming")}<span class="pd-main__end"><span class="tag">Example data</span></span>',
               stats + card("Upcoming", upcoming), one=True)
    types = rows([
        f'<span class="grow"><b>Intro call</b><small>One person, 15 min, Google Meet</small></span>{person("MO")}',
        f'<span class="grow"><b>Sales demo</b><small>Round robin, 30 min</small></span>{person("LK")}{person("SB")}',
        f'<span class="grow"><b>Onboarding</b><small>Everyone free, 45 min, Zoom</small></span>{person("MO")}{person("RJ")}',
        '<span class="grow"><b>Weekly group demo</b><small>Group, 20 seats</small></span><span class="tag tag--green">12 booked</span>',
    ])
    endform = ('<div class="fcard"><h4>Thanks, Priya. Pick a time.</h4><div class="q">With Lena Koch, 30 min on Google Meet</div></div>' + CAL)
    hours = rows([
        f'<span class="grow">{logo("calendar.svg", "")} Google Calendar<small>priya@acme.com</small></span><span class="tag tag--green">Connected</span>',
        '<span class="grow">Monday to Thursday</span><span class="pd-num">9:00 AM to 5:00 PM</span>',
        '<span class="grow">Friday</span><span class="pd-num">9:00 AM to 1:00 PM</span>',
        '<span class="grow">Weekend</span><span class="pd-num">Off</span>',
        '<span class="grow">Buffer and notice</span><span class="pd-num">10 min, 4 hours</span>',
    ])
    main = (
        frame(hero("cal", "Meetings", "Meetings that book themselves", "Booking pages, team meetings and booking right inside your forms, on Google and Outlook, with reminders that go out on their own.", ("See booking templates", "/templates/group/booking"), shot))
        + frame(then_now("Instead of booking links in emails, the meeting booked on the spot", "Leads pick a time while they're still on your page, with the right person.",
                         [("mail", "Reply with a booking link", "Hours later"), ("users", "Check whose turn it is", "In a spreadsheet"), ("clock", "Send reminders by hand", "Or forget"), ("refresh", "Chase the no-shows", "One by one")],
                         [("form", "The form ends on the calendar", "Booked now"), ("route", "The right person is picked", "Fairly"), ("mail", "Reminders send themselves", "Day and hour before"), ("refresh", "No-shows get the reschedule link", "On their own")]))
        + frame(features("Everything you need to fill the calendar", [
            ("A booking page that looks like you", "A page for each person and the team, in your brand. Times show in the visitor's own time zone and language.", None, card("Sales demo", CAL, "30 min, Google Meet")),
            ("Every kind of meeting", "One person, round robin, everyone free, or a group with a seat limit. Add polls, one-off times and paid meetings.", "Team meetings on Pro", card("Meeting types", types)),
            ("Booked inside the form", "The form picks the meeting and the meeting picks the person, so the calendar opens right after they answer, with name and email filled in.", None, card("Thank-you screen", endform)),
            ("Reminders that send themselves", "A confirmation with the invite, then reminders a day and an hour before. They stop if the meeting moves or is canceled.", None, card("After booking", REMIND)),
        ]))
        + frame(how("Set up once, booked every day", [
            ("Connect your calendar", "Google or Outlook in one click. Busy times stay fresh."),
            ("Set your hours", "Working hours, buffers, notice and daily caps."),
            ("Create a meeting type", "Who hosts it, how long it runs and where it happens."),
            ("Share it, or add it to a form", "A booking page, a link in an email, or the last page of a form."),
        ], card("Availability", hours)))
        + frame(shelf("Forms that book a meeting", "Each one ends on the calendar. Open one and try it.", ["general-book-a-call", "wellness-new-patient", "education-course-inquiry", "pets-grooming", "education-tutoring", "hospitality-group-booking"], "See all booking templates", "/templates/group/booking"))
        + cta()
    )
    return page("/products/meetings", "Meetings · Claritia", "Claritia Meetings: booking pages, round robin, group meetings, polls and booking inside forms, on Google and Outlook, with reminders built in.", main)


# Routing ------------------------------------------------------------------------------------------------------------

def routing_page():
    shot = app("app.tryclaritia.com/forms/demo-request", "Forms",
               f'<b>Demo request</b>{tabs(["Build", "On submission", "Submissions", "Share"], "On submission")}<span class="pd-main__end"><span class="pd-pill">Publish</span></span>',
               card("Routing", RULES) + '<div style="display:flex;flex-direction:column;gap:20px;min-width:0">' + card("Why Lena got this lead", WHY) + card("Sales team", POOL, "This week") + "</div>")
    owner = rows([
        '<span class="grow"><b>dana@acme.com</b><small>Filled the demo request</small></span>',
        f'<span class="grow">Owner in HubSpot</span>{logo("hubspot.svg", "")}{person("MO")}',
        '<span class="grow">Maya is free Tue at 10:30</span><span class="tag tag--green">Booked</span>',
        '<span class="grow">Maya is away</span><span class="tag tag--gray">Sales team takes turns</span>',
    ])
    team = rows([
        f'<span class="grow">{person("MO")}</span><span class="pd-num">Weight 2</span><span class="tag tag--green">Available</span>',
        f'<span class="grow">{person("LK")}</span><span class="pd-num">Weight 1</span><span class="tag tag--green">Available</span>',
        f'<span class="grow">{person("SB")}</span><span class="pd-num">Weight 1</span><span class="tag tag--green">Available</span>',
        f'<span class="grow">{person("RJ")}</span><span class="pd-num">Weight 1</span><span class="tag tag--orange">Away until Mon</span>',
        '<span class="grow">Caps</span><span class="pd-num">6 a day, 25 a week</span>',
    ])
    main = (
        frame(hero("route", "Routing", "The right person, every time", "Each answer picks the meeting and the person, then the team takes turns fairly. Every lead keeps a note of why.", ("See pricing", "/pricing"), shot))
        + frame(then_now("Instead of sorting leads by hand, rules that decide in a second", "No inbox to watch and no list of whose turn it is.",
                         [("mail", "Leads land in a shared inbox", "Someone reads them"), ("table", "Check the territory sheet", "Out of date"), ("users", "Ask whose turn it is", "In chat"), ("clock", "The lead waits", "Often a day")],
                         [("form", "The answers come in", "Right away"), ("route", "A rule picks the meeting", "First match wins"), ("users", "The team takes turns", "Weighted, fair"), ("cal", "The lead books on the spot", "With the right person")]))
        + frame(features("Everything you need to route every lead", [
            ("Route by any answer", "Rules read the answers in order. The first that matches books a meeting, books a person or sends something. Everyone else goes to a team.", "Pro", card("On submission", RULES)),
            ("Take turns, fairly", "Round robin with weights and priority. People who are away or at their cap are skipped, and the most due person gets the next lead.", "Pro", card("Sales team", POOL, "This week")),
            ("Known leads go to their owner", "Someone who's already in your CRM books with their owner, or with whoever they met before. If the owner is away, the team takes over.", "Business", card("Owner first", owner)),
            ("See why, every time", "Every meeting shows the rule that matched and why that person was picked. Fix a rule and the next lead follows it.", "Pro", card("Why Lena got this lead", WHY)),
        ]))
        + frame(how("Set the rules once, route every lead", [
            ("Ask what you need to know", "Team size, country, budget or anything else, right in the form."),
            ("Add rules in On submission", "If an answer is this, book that meeting or that person."),
            ("Build your team", "Who takes turns, their weights, caps and away days."),
            ("Leads book with the right person", "On the spot, with a Slack note to the host."),
        ], card("Team in Availability", team)))
        + frame(shelf("Forms built to qualify", "Each asks what routing needs, then books the right meeting.", ["saas-enterprise-demo", "agency-marketing-audit", "consulting-consultation", "real-estate-buyer-inquiry", "saas-data-maturity-scorecard", "coaching-discovery-call"], "See all qualification templates", "/templates/category/qualify"))
        + cta()
    )
    return page("/products/routing", "Routing · Claritia", "Claritia Routing: each lead's answers pick the meeting and the person, with round robin, team pools, owner first and a note of why for every lead.", main)


# The index ------------------------------------------------------------------------------------------------------------

def index_page():
    items = [("01", "forms", "Forms", "Describe a form and Tia builds it in your brand, with pages, logic, prices and payments."),
             ("02", "meetings", "Meetings", "Booking pages, team meetings and a calendar inside your forms, with reminders built in."),
             ("03", "routing", "Routing", "Each answer picks the meeting and the person, and the team takes turns fairly.")]
    trio = "".join(f'<a href="/products/{k}"><b>{n}</b><h2>{t}</h2><p>{esc(line)}</p><em>See {t} {I("arrow", "i s14 arr")}</em></a>' for n, k, t, line in items)
    main = frame(f"""    <section class="pd-hero" aria-labelledby="pp-h" style="padding-bottom:40px">
      <span class="eyebrow">{I("grid", "i s12")}Product</span>
      <h1 id="pp-h">From first click to booked call</h1>
      <p class="sub">Forms, meetings and routing that share one record for every lead.</p>
      <div class="pd-ctas"><a class="btn btn--primary btn--lg" href="{APP}/signup">Start free {I("arrow", "i s14 arr")}</a><a class="btn btn--ghost btn--lg" href="/pricing">See pricing</a></div>
      <p class="pd-note">Free plan. No card needed.</p>
      <div class="pd-trio">{trio}</div>
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
