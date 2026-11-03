"""Builds the integration pages: /integrations (the hub) and one page per tool at /integrations/<slug>. Each tool page
targets "<tool> form integration" or "<tool> scheduling integration" and the searches around it (docs: the keyword
plan in the chat that started this, volumes from Arrowsterr). Every workflow on a page is one the app really does
today: check claritia/docs/integrations-plan.md and the code before adding a line. Plan tags follow docs/pricing.md in
the app repo. Uses the product pages' layout (tools/products.py: how, shelf, cta; assets/products.css) plus
assets/integrations.css. Run: python3 tools/integrations.py"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shell  # noqa: E402
import templates as tpl  # noqa: E402
import products as px  # noqa: E402

IX_V = 2
LASTMOD = "2026-11-03"
esc, I, APP, frame = px.esc, px.I, px.APP, px.frame


def head_block(eyebrow, icon, title, sub, h_id):
    return f'<div class="pd-head"><span class="eyebrow">{I(icon, "i s12")}{esc(eyebrow)}</span><h2 class="h2" id="{h_id}">{title}</h2><p class="sub">{esc(sub)}</p></div>'


def caps(items):
    out = []
    for ic, title, line, plan in items:
        tag = f'<span class="tag tag--green">{esc(plan)}</span>' if plan else ""
        out.append(f'<div class="ix-cap"><div class="ix-cap__top">{I(ic)}<h3>{esc(title)}</h3>{tag}</div><p>{esc(line)}</p></div>')
    return f'<div class="ix-caps">{"".join(out)}</div>'


def faq(items):
    plus = '<svg aria-hidden="true"><use href="#i-plus"/></svg>'
    qa = "".join(f"<details><summary>{esc(q)} {plus}</summary><p>{esc(a)}</p></details>" for q, a in items)
    return f"""  <div class="frame ix-faq">
    <section class="pd-sec" aria-labelledby="faq-h">
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


SCRIPT_TAG = '<script src="https://app.tryclaritia.com/forms/v1.js" async></script>'
EMBED = '<claritia-form form-id="FORM_ID"></claritia-form>'
SITE = shell.SITE
CHEV = I("chev-r")
ARROW = I("arrow")

# Drawn product parts ---------------------------------------------------------------------------------------------

def seg(options, on):
    return '<span class="ix-seg">' + "".join(f'<span class="{"on" if o == on else ""}">{esc(o)}</span>' for o in options) + "</span>"


def tog(on=True):
    return f'<span class="ix-tog{"" if on else " off"}"></span>'


def val(text, icon=None):
    return f'<span class="ix-val">{I(icon) if icon else ""}{esc(text)}</span>'


def row(label, value, sub=None):
    s = f"<small>{esc(sub)}</small>" if sub else ""
    return f'<div class="ix-row"><span>{esc(label)}{s}</span>{value}</div>'


def maps(pairs):
    return "".join(f'<div class="ix-row"><div class="ix-map"><span>{esc(a)}</span>{ARROW}<span>{esc(b)}</span></div></div>' for a, b in pairs)


def panel(logo, title, note, inner):
    return f"""<div class="ix-panel">
        <div class="ix-panel__head"><img src="/assets/logos/{logo}" alt="" width="22" height="22"><b>{esc(title)}</b><small>{esc(note)}</small></div>
        <div class="ix-rows">{inner}</div>
      </div>"""


def crm_panel(name, logo, extra_first=""):
    return panel(logo, f"Send to {name}", "Demo request", extra_first
        + row(f"When the email is already in {name}", seg(["Update it", "Leave it"], "Update it"), "Matched by email")
        + row("Owner", seg(["Routing's pick", f"{name} decides"], "Routing's pick"))
        + row("Send email consent", tog())
        + maps([("Work email", "Email"), ("Full name", "First and last name"), ("Company", "Company"), ("Phone", "Phone")]))


def calendar_panel(logo, name, cals, where, place):
    rows = "".join(row(c, tog(on)) for c, on in cals)
    return panel(logo, name, "Calendars", f'<div class="ix-row"><span><b style="font-weight:500">Check these for busy times</b></span></div>{rows}'
        + row("Add new meetings to", val(where, "cal"))
        + row("Location", val(place, "video")))


# Pages -----------------------------------------------------------------------------------------------------------
# keys: name, logo, group, kind ("form" or "scheduling"), plan, h1, title, desc, sub, caps, steps, vis, faq, tpls, also

TOOLS = {
    "hubspot": {
        "name": "HubSpot", "logo": "hubspot.svg", "group": "CRM", "plan": "Starter",
        "h1": "HubSpot form integration",
        "desc": "Connect Claritia forms to HubSpot: each fill becomes a HubSpot contact with fields mapped and no duplicates, then the lead books with the right rep. On Starter, from $15 a month.",
        "sub": "Send every form fill to HubSpot as a contact, with fields mapped and no duplicates. Then each lead books a meeting with the right rep before leaving the page.",
        "caps": [
            ("user", "Create or update a contact", "Each fill makes a HubSpot contact, or updates the one with that email.", "Starter"),
            ("table", "Map every field", "Match each question to a HubSpot contact property, like email, phone, company or job title.", "Starter"),
            ("route", "Set the owner", "Use the person Routing picks, or let HubSpot's own rules decide. Contacts that have an owner keep theirs.", "Starter"),
            ("cal", "Book with the contact owner", "A lead HubSpot already knows books with their owner first. New leads go to the team's round robin.", "Business"),
            ("form", "Keep your HubSpot forms", "Claritia hears your HubSpot form send and opens the right calendar on the same page.", None),
            ("clock", "Fills on the timeline", "Each fill shows on the contact's timeline in HubSpot, so reps see what the lead asked for.", "Starter"),
        ],
        "steps": [
            ("Connect HubSpot", "Go to Settings, then Integrations, and sign in with HubSpot. No API keys."),
            ("Pick it on a form", "Open the form's Sync tab, add HubSpot and match each question to a property."),
            ("Publish", "New fills go to HubSpot as they come in. A send that fails tries again, and the sync log shows each one."),
        ],
        "vis": lambda: crm_panel("HubSpot", "hubspot.svg"),
        "faq": [
            ("Which plan has the HubSpot integration?", "Starter and up, from $15 a month. Booking with the contact owner is on Business. On Free, fills can go out by webhook or CSV."),
            ("Does it make duplicate contacts?", "No. Claritia matches each fill to HubSpot by email. You pick whether a match is updated or left as it is."),
            ("Can I route HubSpot form leads to the contact owner?", "Yes, on Business. A lead HubSpot knows books with their owner first, and anyone new goes to the team's round robin."),
            ("Can I keep my HubSpot forms?", "Yes. Add the Claritia script to the page and point it at your HubSpot form. When the form sends, the calendar opens and the lead books."),
            ("Does the consent box go to HubSpot?", "Yes. When it's on, the consent answer sets the contact's email subscription status in HubSpot."),
            ("What happens if HubSpot is down?", "Every fill is saved in Claritia first. The send to HubSpot tries again on its own with longer waits."),
        ],
        "tpls": ["saas-demo-request", "saas-contact-sales", "general-book-a-call"],
    },
    "salesforce": {
        "name": "Salesforce", "logo": "salesforce.svg", "group": "CRM", "plan": "Business",
        "h1": "Salesforce form integration",
        "desc": "Connect Claritia forms to Salesforce: each fill becomes a lead or contact, matched by email, with fields mapped and the meeting booked with the right owner. On Business.",
        "sub": "Turn every form fill into a Salesforce lead or contact, matched by email, and book the meeting with the right owner before the lead leaves.",
        "caps": [
            ("user", "Leads or contacts", "Pick what new people become. An email Salesforce already has links to that record.", "Business"),
            ("table", "Map fields, custom ones too", "Match each question to a Salesforce field, including custom fields that end in __c.", "Business"),
            ("route", "Set the owner", "Use the person Routing picks, or let Salesforce assignment rules decide.", "Business"),
            ("cal", "Book with the record owner", "A lead Salesforce already knows books with its owner first. New leads go to the team's round robin.", "Business"),
            ("check", "Fills as tasks", "Each fill shows as a completed task on the lead or contact.", "Business"),
            ("form", "More than web-to-lead", "Steps, logic, spam checks and a booked meeting, with the same lead landing in Salesforce.", "Business"),
        ],
        "steps": [
            ("Connect Salesforce", "Go to Settings, then Integrations, and sign in with Salesforce. No API keys."),
            ("Pick it on a form", "Open the form's Sync tab, add Salesforce, pick leads or contacts and match each field."),
            ("Publish", "New fills go to Salesforce as they come in. A send that fails tries again, and the sync log shows each one."),
        ],
        "vis": lambda: crm_panel("Salesforce", "salesforce.svg", row("Make them as", seg(["Leads", "Contacts"], "Leads"))),
        "faq": [
            ("Which plan has the Salesforce integration?", "Business, at $79 a month with 1 host. Each extra host is $25 a month, or $20 billed yearly."),
            ("Can a Claritia form replace a Salesforce web-to-lead form?", "Yes. It sends the same lead to Salesforce, and adds steps, show-if logic, spam checks and a meeting booked at the end."),
            ("Does it make duplicate leads?", "No. When Salesforce already has the email, the fill links to that lead or contact. Only new emails make new records."),
            ("Can Salesforce assignment rules pick the owner?", "Yes. Pick Salesforce decides, and its assignment rules run on each new record."),
            ("What happens if Salesforce is down?", "Every fill is saved in Claritia first. The send to Salesforce tries again on its own with longer waits."),
        ],
        "tpls": ["saas-enterprise-demo", "saas-demo-request", "saas-contact-sales"],
    },
    "google-calendar": {
        "name": "Google Calendar", "logo": "calendar.svg", "group": "Calendars", "kind": "scheduling", "plan": "Free",
        "h1": "Google Calendar scheduling integration",
        "desc": "Connect Google Calendar to Claritia in one click: leads only see times you're free, and each booking lands on your calendar with a Google Meet link. On every plan, Free included.",
        "sub": "Connect Google Calendar in one click. Leads only see times you're free, and each booking lands on your calendar with a Google Meet link.",
        "caps": [
            ("refresh", "Busy times stay fresh", "Google tells Claritia the moment your calendar changes, so a taken time never shows.", None),
            ("eyeoff", "Your events stay private", "Claritia reads only when you're busy. It never reads event titles.", None),
            ("video", "Google Meet links", "Each meeting gets its own Meet link on the event.", None),
            ("grid", "More than one calendar", "Count work and personal calendars as busy, and pick where new meetings go.", "Starter"),
            ("users", "Team meetings", "Round robin and everyone-free meetings read each person's Google Calendar.", "Pro"),
            ("mail", "One invite, from you", "Guests get Claritia's invite in your words, so Google doesn't send them a second one.", None),
        ],
        "steps": [
            ("Connect Google", "Sign in with Google from Meetings. Google Workspace and Gmail accounts both work."),
            ("Pick your calendars", "Choose which calendars count as busy and which one gets new meetings."),
            ("Share your booking page", "Put it in a form, on your site or in an email. Guests book open times only."),
        ],
        "vis": lambda: calendar_panel("calendar.svg", "Google Calendar", [("Work", True), ("Personal", True), ("Team holidays", False)], "Work", "Google Meet"),
        "faq": [
            ("Is the Google Calendar integration free?", "Yes, on every plan, Free included. Free connects 1 calendar per host, Starter 3, Pro 10 and Business as many as you like."),
            ("Can Claritia see my events?", "No. It reads only the start and end of busy times. Titles, guests and notes stay in Google."),
            ("Does it add Google Meet links?", "Yes. Pick Google Meet as the location and every booking gets its own link."),
            ("Do guests need a Google account?", "No. Guests book from any browser and get a calendar invite that works in Google, Outlook and Apple Calendar."),
        ],
        "tpls": ["general-book-a-call", "consulting-consultation", "saas-quick-demo"],
    },
    "outlook": {
        "name": "Outlook", "logo": "outlook.jpg", "group": "Calendars", "kind": "scheduling", "plan": "Free",
        "h1": "Outlook scheduling integration",
        "desc": "Connect Outlook and Microsoft 365 to Claritia in one click: leads book open times, out of office counts as busy, and meetings get a Teams link. On every plan, Free included.",
        "sub": "Connect Outlook or Microsoft 365 in one click. Leads book only open times, and each meeting lands on your calendar with a Teams link.",
        "caps": [
            ("refresh", "Busy times stay fresh", "Outlook tells Claritia the moment your calendar changes, so a taken time never shows.", None),
            ("clock", "Out of office counts", "Time you mark out of office is blocked too.", None),
            ("video", "Teams links", "Work and school accounts get a Microsoft Teams link on each meeting.", None),
            ("grid", "More than one calendar", "Count several calendars as busy, and pick where new meetings go.", "Starter"),
            ("users", "Team meetings", "Round robin and everyone-free meetings read each person's Outlook calendar.", "Pro"),
            ("mail", "Invites done right", "Guests get Claritia's invite. Co-hosts on your team get Outlook's own invite and cancel notice.", None),
        ],
        "steps": [
            ("Connect Microsoft", "Sign in with Microsoft from Meetings. Microsoft 365 and Outlook.com accounts both work."),
            ("Pick your calendars", "Choose which calendars count as busy and which one gets new meetings."),
            ("Share your booking page", "Put it in a form, on your site or in an email. Guests book open times only."),
        ],
        "vis": lambda: calendar_panel("outlook.jpg", "Outlook", [("Calendar", True), ("Team calendar", True), ("Birthdays", False)], "Calendar", "Microsoft Teams"),
        "faq": [
            ("Is the Outlook integration free?", "Yes, on every plan, Free included. Free connects 1 calendar per host, Starter 3, Pro 10 and Business as many as you like."),
            ("Does it work with a personal Outlook.com account?", "Yes, for booking. Teams links need a work or school Microsoft 365 account, so personal accounts book without one."),
            ("Can I use Zoom with Outlook?", "Yes. Connect Zoom and pick it as the meeting's location. The Zoom link goes on the Outlook event."),
            ("Do guests need Outlook?", "No. Guests book from any browser and get a calendar invite that works in Outlook, Google and Apple Calendar."),
        ],
        "tpls": ["general-book-a-call", "consulting-consultation", "education-info-session"],
    },
    "zoom": {
        "name": "Zoom", "logo": "zoom.svg", "group": "Video", "kind": "scheduling", "plan": "Free",
        "h1": "Zoom scheduling integration",
        "desc": "Connect Zoom to Claritia: every booked meeting gets its own Zoom link, made on the host's own account and added to the calendar invite. On every plan, Free included.",
        "sub": "Every booked meeting gets its own Zoom link, made on the host's own Zoom account and added to the calendar invite.",
        "caps": [
            ("video", "A link for each meeting", "Each booking makes a new Zoom meeting on the host's own account.", None),
            ("cal", "On the invite", "The join link goes on the calendar event and the guest's invite.", None),
            ("refresh", "Google or Outlook", "Zoom works with either calendar. Pick Zoom as the location on any meeting type.", None),
            ("users", "Team meetings", "In a round robin, the Zoom meeting is made on the account of the person who gets the lead.", "Pro"),
            ("check", "Never two links", "If a step has to run again, Claritia reuses the Zoom meeting it already made.", None),
            ("mail", "Reminders built in", "Confirmations go out at once, then reminders a day and an hour before.", None),
        ],
        "steps": [
            ("Connect Zoom", "Each host signs in with Zoom once, from Meetings."),
            ("Pick Zoom as the location", "Open a meeting type and set its location to Zoom."),
            ("Share your booking page", "Each booking now gets its own Zoom meeting and link."),
        ],
        "vis": lambda: panel("zoom.svg", "Sales demo", "Meeting type",
            row("Length", seg(["15 min", "30 min", "45 min"], "30 min"))
            + row("Location", val("Zoom", "video"))
            + row("Hosts", '<span class="ix-val">' + px.person("LK") + px.person("SB") + "</span>", "Round robin")
            + row("Reminders", val("1 day and 1 hour before", "clock"))),
        "faq": [
            ("Is the Zoom integration free?", "Yes. Zoom, Google Meet and Teams links are on every plan, Free included."),
            ("Does each host need a Zoom account?", "Yes. Each host connects their own Zoom, so meetings run under their name."),
            ("Do free Zoom accounts work?", "Yes. Zoom's own limits for free accounts, like the meeting time limit, still apply."),
            ("Does it work with Outlook and Google Calendar?", "Yes. The Zoom link goes on the event in whichever calendar the host connected."),
        ],
        "tpls": ["saas-demo-request", "coaching-discovery-call", "general-webinar-registration"],
    },
    "slack": {
        "name": "Slack", "logo": "slack.svg", "group": "Chat", "plan": "Starter",
        "h1": "Slack form integration",
        "desc": "Connect Claritia to Slack: post new form leads in a channel, message the rep who gets each lead, and book a meeting for any lead with /book. On Starter, from $15 a month.",
        "sub": "Post every new lead in Slack, message the rep who gets it, and book a meeting for any lead right from Slack with /book.",
        "caps": [
            ("bolt", "New lead alerts", "A team channel gets each fill as it comes in.", "Starter"),
            ("user", "A message to the rep", "The rep who gets the lead hears about it in Slack right away.", "Starter"),
            ("check", "Mark contacted", "Reps tap Mark contacted right in the message.", "Starter"),
            ("cal", "/book from Slack", "Type /book and an email to get a single-use booking link for that lead.", "Starter"),
            ("flow", "A Slack step in workflows", "Post to Slack from any workflow, like when a meeting is booked.", "Starter"),
            ("clock", "Speed-to-lead nudges", "A rep who hasn't reached a routed lead yet gets a reminder.", "Pro"),
        ],
        "steps": [
            ("Add to Slack", "Go to Settings, then Integrations, and click Add to Slack."),
            ("Pick what posts", "Turn on alerts for a form, or add a Slack step to a workflow."),
            ("Work from Slack", "Reps get their leads in Slack and book with /book."),
        ],
        "vis": lambda: f"""<div class="ix-panel">
        <div class="ix-panel__head"><img src="/assets/logos/slack.svg" alt="" width="22" height="22"><b># inbound-leads</b><small>Example</small></div>
        <div class="ix-msg"><span class="av" style="background:var(--green-strong)">{I("mark")}</span><div>
          <b>Claritia<small>10:31 AM</small></b>
          <p>New lead from Book a demo: Priya Raman, 2 to 10 people, Germany. Booked Tue, Nov 10 at 10:30 AM with Lena Koch.</p>
          <div class="ix-btns"><span>Open lead</span><span class="on">Mark contacted</span></div>
        </div></div>
        <div class="ix-cmd">/book jonas@example.com demo</div>
      </div>""",
        "faq": [
            ("Which plan has the Slack integration?", "Starter and up, from $15 a month. Speed-to-lead nudges for routed leads are on Pro."),
            ("How do I connect Slack?", "One click: Add to Slack in Settings, then Integrations. No webhook addresses to paste."),
            ("How does /book work?", "Type /book and the lead's email. Only you see the answer: a single-use booking link with the lead's owner, or with you when the lead has none."),
            ("Who gets the direct message?", "The rep Routing picks for the lead, found in Slack by their email."),
        ],
        "tpls": ["saas-demo-request", "general-contact-us", "general-callback-request"],
    },
    "webflow": {
        "name": "Webflow", "logo": "webflow.svg", "group": "Website", "plan": "Free",
        "h1": "Webflow form integration",
        "desc": "Add Claritia forms to Webflow with one Embed element, or keep your Webflow form and book a meeting the moment it's sent. Multi-step forms and logic with no custom code.",
        "sub": "Put a Claritia form on your Webflow site with one Embed element, or keep your Webflow form and book a meeting the moment it's sent.",
        "caps": [
            ("globe", "One embed", "Paste one snippet into a Webflow Embed element. It works on every page and on phones.", None),
            ("form", "Keep your Webflow form", "Claritia hears your Webflow form send and opens the right calendar on the same page.", None),
            ("route", "Multi-step forms and logic", "Steps, show-if logic and prices, with no custom code.", None),
            ("type", "Your site's look", "Tia reads your Webflow site and matches its fonts, colors and buttons.", "Pro"),
            ("hook", "Fills from Webflow forms", "Webflow form fills come into Claritia by webhook, so they book and follow up the same way.", "Starter"),
            ("eyeoff", "Spam stays out", "Cloudflare Turnstile and a hidden trap keep bots off your forms.", None),
        ],
        "steps": [
            ("Build or pick a form", "Describe it to Tia, start from a template, or point Claritia at your Webflow form."),
            ("Add an Embed element", "In Webflow, drop an Embed element where the form goes and paste the snippet."),
            ("Publish your site", "Fills land in Claritia and go on to your CRM, sheets and Slack."),
        ],
        "vis": lambda: f'<pre class="ix-code"><code>{esc(SCRIPT_TAG + chr(10) + EMBED)}</code></pre>',
        "faq": [
            ("How do I add a Claritia form to Webflow?", "Drop an Embed element where the form goes, paste the snippet from the form's Share tab, then publish."),
            ("Can I make a multi-step form in Webflow?", "Yes. Build the steps and show-if logic in Claritia and embed it. No custom code in Webflow."),
            ("Can I keep my Webflow form?", "Yes. Add the Claritia script and point it at your Webflow form. When the form sends, the calendar opens and the lead books."),
            ("Will it slow my site down?", "No. The script loads after the page, so your Webflow page draws first."),
            ("Where do the answers go?", "Into Claritia first, then to the tools you connect: HubSpot, Salesforce, Google Sheets, Airtable, Notion, Slack, email lists and webhooks."),
        ],
        "tpls": ["saas-demo-request", "agency-project-inquiry", "general-contact-us"],
    },
    "stripe": {
        "name": "Stripe", "logo": "stripe.svg", "group": "Payments", "plan": "Starter",
        "h1": "Stripe form integration",
        "desc": "Connect Stripe to Claritia: take payments and deposits in forms and charge for meetings, paid straight to your own Stripe account. On Starter, from $15 a month.",
        "sub": "Take payments and deposits in your forms, and charge for meetings, with the money paid straight to your own Stripe account.",
        "caps": [
            ("card", "Payments in forms", "Take a full payment or a deposit at the end of a form.", "Starter"),
            ("grid", "Prices that add up", "Quotes and order totals work out from the answers, and Stripe charges that amount.", "Starter"),
            ("cal", "Paid meetings", "Guests pay to book any meeting type you put a price on.", "Starter"),
            ("clock", "The time is held", "While a guest pays, their time is held for 10 minutes so nobody else takes it.", "Starter"),
            ("refresh", "Refunds on their own", "If the time is gone when the payment clears, the payment is refunded at once.", "Starter"),
            ("user", "Your own Stripe account", "Guests pay you directly. Stripe's fees are yours, and Claritia never holds the money.", "Starter"),
        ],
        "steps": [
            ("Connect Stripe", "Go to Settings, then Integrations, and sign in with Stripe."),
            ("Add a price", "Add a payment block to a form, or set a price on a meeting type."),
            ("Get paid", "Payments go to your Stripe account and show on each fill or booking."),
        ],
        "vis": lambda: f"""<div class="ix-panel">
        <div class="ix-panel__head"><img src="/assets/logos/stripe.svg" alt="" width="22" height="22"><b>Catering quote</b><small>Example</small></div>
        <div class="ix-rows">{row("40 guests, buffet", val("$1,520"))}{row("Open bar", val("$480"))}</div>
        <div class="ix-total"><span>Total</span><b>$2,000</b></div>
        <div class="ix-total" style="padding-top:0;border-top:0"><span>Deposit now, 20%</span><b style="font-size:20px">$400</b></div>
        <div class="ix-pay">Pay $400</div>
      </div>""",
        "faq": [
            ("Which plan has Stripe payments?", "Starter and up, from $15 a month. Price calculations work on every plan, Free included."),
            ("Who holds the money?", "You do. Guests pay your own Stripe account directly, and Stripe's fees are yours."),
            ("Can I take a deposit?", "Yes. Charge the full amount or a part of it, like 20% now."),
            ("What if a paid time gets taken?", "The time is held for 10 minutes while the guest pays. If it's gone anyway, the payment is refunded at once."),
        ],
        "tpls": ["food-catering-calculator", "general-invoice-payment", "fitness-private-session"],
    },
}
ORDER = ["hubspot", "salesforce", "google-calendar", "outlook", "zoom", "slack", "webflow", "stripe"]
GROUPS = ["CRM", "Calendars", "Video", "Chat", "Payments", "Website"]
GROUP_LINE = {
    "CRM": "Every fill becomes a contact, and each lead books with its owner.",
    "Calendars": "Busy times stay fresh, and every booking lands on the calendar.",
    "Video": "A meeting link made for each booking.",
    "Chat": "New leads where your team already talks.",
    "Payments": "Payments and deposits, paid to your own account.",
    "Website": "Forms on your site with one line, or keep the ones you have.",
}
SHORT = {
    "hubspot": "Contacts, owners and booking",
    "salesforce": "Leads, contacts and owners",
    "google-calendar": "Busy times and Meet links",
    "outlook": "Busy times and Teams links",
    "zoom": "A link for each meeting",
    "slack": "Lead alerts and /book",
    "webflow": "Embeds and your own forms",
    "stripe": "Payments and paid meetings",
}
# Built and on the pricing page, without their own page yet (Tier 2 and 3 in the keyword plan).
ALSO = [
    ("Omniscient", "omniscient.svg"), ("Google Sheets", None), ("Airtable", None), ("Notion", None), ("Mailchimp", None),
    ("Klaviyo", None), ("ActiveCampaign", None), ("Brevo", None), ("Kit", None), ("MailerLite", None),
    ("Google Meet", "meet.svg"), ("Microsoft Teams", "teams.png"), ("Typeform", "typeform.svg"), ("Tally", None),
    ("Calendly", "calendly.svg"), ("Cal.com", None), ("Webhooks", None),
]


def tool_link(k):
    t = TOOLS[k]
    return (f'<a class="ix-tool" href="/integrations/{k}"><span class="ix-logo"><img src="/assets/logos/{t["logo"]}" alt="" width="22" height="22" loading="lazy"></span>'
            f'<b>{esc(t["name"])}</b><span>{esc(SHORT[k])}</span></a>')


def ld(data) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": name, "item": f"{SITE}{path}"} for n, (name, path) in enumerate(items)]}


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def page(path, title, desc, main, extra_ld=""):
    extra = (f'<link rel="stylesheet" href="{tpl.FONTS_URL}">\n<link rel="stylesheet" href="/assets/forms.css?v={tpl.CSS_V}">\n'
             f'<link rel="stylesheet" href="/assets/themes.css?v={tpl.CSS_V}">\n<link rel="stylesheet" href="/assets/products.css?v={px.PX_V}">\n'
             f'<link rel="stylesheet" href="/assets/integrations.css?v={IX_V}">\n' + extra_ld)
    return shell.head(title, desc, path, extra) + "\n" + shell.body(main)


def tool_page(k):
    t = TOOLS[k]
    kind = t.get("kind", "form")
    plan = t["plan"]
    plan_line = "On every plan, Free included" if plan == "Free" else f"On {plan} and up"
    crumb = f"""<nav class="ix-crumb" aria-label="Breadcrumb"><a href="/integrations">Integrations</a>{CHEV}<a href="/integrations#{t["group"].lower()}">{esc(t["group"])}</a>{CHEV}<span aria-current="page">{esc(t["name"])}</span></nav>"""
    hero = f"""    <section class="pd-hero ix-hero" aria-labelledby="ix-h">
      <div class="ix-copy">
        {crumb}
        <div class="ix-pair" aria-hidden="true"><span class="itl"><img src="/assets/brand/claritia-mark.svg" alt="" width="34" height="34"></span><span class="ix-pair__link"></span><span class="itl"><img src="/assets/logos/{t["logo"]}" alt="" width="34" height="34"></span></div>
        <h1 id="ix-h">{esc(t["h1"])}</h1>
        <p class="sub">{esc(t["sub"])}</p>
        <div class="pd-ctas">
          <a class="btn btn--primary btn--lg" href="{APP}">Connect {esc(t["name"])} {I("arrow", "i s14 arr")}</a>
          <a class="btn btn--ghost btn--lg" href="/integrations">All integrations</a>
        </div>
        <p class="ix-plan"><span class="tag tag--green">{esc(plan)}</span>{esc(plan_line)}. Free plan, no card needed.</p>
      </div>
    </section>"""
    workflows = f"""    <section class="pd-sec" aria-labelledby="wf-h">
      {head_block("Workflows", "flow", f"What you can do with {esc(t['name'])}", "Tags show the plan a workflow starts on.", "wf-h")}
      {caps(t["caps"])}
    </section>"""
    steps = "".join(f"<li><b>{esc(a)}</b><span>{esc(b)}</span></li>" for a, b in t["steps"])
    connect = px.how(f"Connect {esc(t['name'])} in a few minutes", t["steps"], f'<div class="ix-vis" aria-hidden="true">{t["vis"]()}</div>')
    tpls = px.shelf("Forms to start with", f"Each one is a real form you can fill in now, ready to send to {t['name']}." if kind == "form" else "Each one is a real form you can fill in now, with booking at the end.", t["tpls"], f"See all {len(tpl.T)} templates", "/templates")
    others = "".join(tool_link(o) for o in ORDER if o != k)
    more = f"""    <section class="pd-sec" aria-labelledby="more-h">
      {head_block("Integrations", "plug", "Works with the rest of your tools", "Every lead goes to Claritia first, then to each tool you connect.", "more-h")}
      <div class="ix-tools">{others}</div>
    </section>"""
    main = frame(hero) + frame(workflows) + frame(connect) + frame(tpls) + frame(more) + faq(t["faq"]) + px.cta()
    title = f"{t['h1']} · Claritia"
    lds = ld(crumbs_ld([("Integrations", "/integrations"), (t["name"], f"/integrations/{k}")])) + ld(faq_ld(t["faq"]))
    return page(f"/integrations/{k}", title, t["desc"], main, lds)


def hub_page():
    groups = []
    for g in GROUPS:
        keys = [k for k in ORDER if TOOLS[k]["group"] == g]
        groups.append(f"""<div class="ix-group" id="{g.lower()}"><h2>{esc(g)}</h2><p class="sub" style="margin:-8px 0 18px">{esc(GROUP_LINE[g])}</p><div class="ix-tools">{"".join(tool_link(k) for k in keys)}</div></div>""")
    def chip(n, logo):
        pic = f'<img src="/assets/logos/{logo}" alt="" width="18" height="18" loading="lazy">' if logo else I("plug")
        return f"<li>{pic}{esc(n)}</li>"
    also = "".join(chip(n, logo) for n, logo in ALSO)
    main = frame(f"""    <section class="pd-hero ix-hero" aria-labelledby="ix-h">
      <div class="ix-copy">
        <span class="eyebrow">{I("plug", "i s12")}Integrations</span>
        <h1 id="ix-h">Connect Claritia to the tools you use</h1>
        <p class="sub">Send each lead to your CRM, book it on your calendar and tell your team in Slack. Every connection is one click.</p>
        <div class="pd-ctas">
          <a class="btn btn--primary btn--lg" href="{APP}">Start free {I("arrow", "i s14 arr")}</a>
          <a class="btn btn--ghost btn--lg" href="/pricing">See pricing</a>
        </div>
        <p class="pd-note">Free plan. No card needed.</p>
      </div>
    </section>""") + frame(f"""    <section class="pd-sec" style="padding-top:72px" aria-label="Integrations by kind">
      <div class="ix-groups">{"".join(groups)}</div>
    </section>""") + frame(f"""    <section class="pd-sec" aria-labelledby="also-h">
      {head_block("More", "plug", "Also works with", "Sheets, email lists, form and booking tools, and webhooks for anything else.", "also-h")}
      <ul class="ix-also" style="margin-top:40px">{also}</ul>
    </section>""") + px.cta()
    desc = "Claritia integrations: HubSpot, Salesforce, Google Calendar, Outlook, Zoom, Slack, Webflow and Stripe, plus Google Sheets, Airtable, Notion, email lists and webhooks."
    lds = ld(crumbs_ld([("Integrations", "/integrations")]))
    return page("/integrations", "Integrations · Claritia", desc, main, lds)


def sitemap():
    """The integration pages go in their own block of sitemap.xml, right after /pricing."""
    sm = ROOT / "sitemap.xml"
    text = re.sub(r"\s*<!-- integrations:start -->.*?<!-- integrations:end -->", "", sm.read_text(), flags=re.S)
    lines = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{LASTMOD}</lastmod></url>" for u in ["/integrations"] + [f"/integrations/{k}" for k in ORDER])
    anchor = f"<url><loc>{SITE}/pricing</loc>"
    i = text.index("\n", text.index(anchor))
    sm.write_text(text[:i] + f"\n  <!-- integrations:start -->\n{lines}\n  <!-- integrations:end -->" + text[i:])


if __name__ == "__main__":
    out = ROOT / "integrations"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(hub_page())
    for k in ORDER:
        (out / k).mkdir(exist_ok=True)
        (out / k / "index.html").write_text(tool_page(k))
    sitemap()
    print("wrote integrations/ and", ", ".join(f"integrations/{k}" for k in ORDER))
