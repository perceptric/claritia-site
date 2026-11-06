"""The rest of the integration pages: one per tool the app connects to beyond the first eight (tools/integrations.py
holds those and the page layout). Tools of a kind share their workflows, steps and questions, written once per kind
from what the app does today (claritia/docs/integrations-plan.md, its Next steps 1 to 13); each tool adds its own
facts. Plan tags follow claritia/docs/pricing.md: connected tools are on Starter, Salesforce on Business, and embeds,
webhooks, Google Meet links, browser tags and the Google Forms import on every plan."""

import products as px  # noqa: E402

esc, I = px.esc, px.I


def _h(helpers):
    """The drawn parts from tools/integrations.py, passed in to keep one copy."""
    return helpers["panel"], helpers["row"], helpers["seg"], helpers["tog"], helpers["val"], helpers["maps"]


# Kinds -----------------------------------------------------------------------------------------------------------
# Each kind: hub group, what its page targets, its six workflows, three steps, questions and a picture. {n} is the
# tool's name; a tool's own "caps", "steps" or "faq" replace its kind's.

def crm(n, t):
    record = t.get("record", "contact")
    auth = t.get("auth", "sign")
    connect = f"Go to Settings, then Integrations, and sign in with {n}. No API keys." if auth == "sign" else f"Go to Settings, then Integrations, and paste your {n} {t.get('key', 'API key')}."
    return {
        "group": "CRM", "plan": "Starter",
        "h1": f"{n} form integration",
        "desc": f"Connect Claritia forms to {n}: each fill becomes a {n} {record}, matched by email so there are no duplicates, and the lead books a meeting on the same page. On Starter, from $15/seat/month.",
        "sub": f"Send every form fill to {n} as a {record}, matched by email so there are no duplicates. Then each lead books a meeting before leaving the page.",
        "caps": [
            ("user", f"A {record} for each fill", f"Each fill makes a {n} {record}, or finds the one with that email first.", "Starter"),
            ("table", "Map the fields", f"Match each question to a {n} field, like name, email, phone and company.", "Starter"),
            ("check", "No duplicates", f"The same person filling twice is one {record} in {n}, and a send that runs again updates the one it made.", "Starter"),
            ("plug", "A link back", f"Each fill in Claritia links to its {record} in {n}.", "Starter"),
            ("cal", "Book on the same page", "After the form, the lead picks a time with the right person on your team.", None),
            ("refresh", "Never lost", f"Every fill is saved in Claritia first. If {n} is busy, the send tries again on its own.", "Starter"),
        ],
        "steps": [
            (f"Connect {n}", connect),
            ("Pick it on a form", f"Open the form's Sync tab, add {n} and match each question to a field."),
            ("Publish", f"New fills go to {n} as they come in, and the sync log shows each one."),
        ],
        "vis": lambda h: h["panel"](t["logo"], f"Send to {n}", "Demo request",
            h["row"](f"When the email is already in {n}", h["seg"](["Update it", "Leave it"], "Update it"), "Matched by email")
            + h["maps"]([("Work email", "Email"), ("Full name", "Name"), ("Company", "Company"), ("Phone", "Phone")])),
        "faq": [
            (f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month. On Free, fills can go out by webhook or CSV."),
            (f"Does it make duplicate {record}s?", f"No. Claritia looks for the email in {n} first, so the same person is one {record}."),
            (f"What does Claritia send to {n}?", f"The fields you map in the form's Sync tab, like name, email, phone and company. Each fill in Claritia links to its {record}."),
            (f"What happens if {n} is down?", f"Every fill is saved in Claritia first. The send to {n} tries again on its own, and you can send it again from the sync log."),
        ],
        "tpls": ["saas-demo-request", "general-contact-us", "general-quote-request"],
        "short": f"A {record} for each fill",
    }


def email(n, t):
    where = t.get("list", "list")
    tags = t.get("tags", False)
    return {
        "group": "Email", "plan": "Starter",
        "h1": f"{n} form integration",
        "desc": f"Connect Claritia forms to {n}: each fill joins the {where} you pick{', with tags,' if tags else ''} and only with consent when you ask for it. On Starter, from $15/seat/month.",
        "sub": f"Add every new lead to a {n} {where}{', with tags' if tags else ''}. People who tick the consent box join; the rest stay out.",
        "caps": [
            ("mail", f"Join a {where}", f"Each fill adds the person to the {n} {where} you pick for the form.", "Starter"),
            ("check", "Consent respected", "Turn on the consent box and only people who tick it join.", "Starter"),
            ("type", "Tags" if tags else "Names and fields", f"Add tags in {n} to tell where each person came from." if tags else "Name and other answers go with the email.", "Starter"),
            ("refresh", "Already there? Updated", f"Someone already in {n} is updated, never added twice.", "Starter"),
            ("form", "Any form", "Newsletter sign-ups, waitlists, downloads and demo requests.", None),
            ("flow", "Then follow up", "Claritia's own workflows can send the first email right away, too.", None),
        ],
        "steps": [
            (f"Connect {n}", f"Go to Settings, then Integrations, and {'sign in with ' + n if t.get('auth') == 'sign' else 'paste your ' + n + ' API key'}."),
            (f"Pick the {where}", f"Open the form's Sync tab, add {n} and pick the {where}{' and tags' if tags else ''}."),
            ("Publish", f"New sign-ups join {n} as they come in."),
        ],
        "vis": lambda h: h["panel"](t["logo"], f"Add to {n}", "Newsletter",
            h["row"](where.capitalize(), h["val"]("Monthly newsletter", "mail"))
            + (h["row"]("Tags", h["val"]("website, newsletter")) if tags else "")
            + h["row"]("Only with consent", h["tog"]())),
        "faq": [
            (f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month."),
            (f"Does it add people without consent?", "Not when the consent box is on. Then only people who tick it join."),
            (f"What if the person is already in {n}?", "They're updated, never added a second time."),
        ],
        "tpls": ["general-newsletter", "general-waitlist", "general-report-download"],
        "short": f"Lead joins a {where}",
    }


def rows(n, t):
    unit = t.get("unit", "row")
    place = t.get("place", "sheet")
    return {
        "group": "Sheets", "plan": "Starter",
        "h1": f"{n} form integration",
        "desc": f"Connect Claritia forms to {n}: each fill lands as a new {unit} in the {place} you pick, and new questions add their own {t.get('cols', 'columns')}. On Starter, from $15/seat/month.",
        "sub": f"Every form fill lands as a new {unit} in {n}. Add a question later and its {t.get('col', 'column')} shows up on its own.",
        "caps": [
            ("table", f"A {unit} per fill", f"Each fill adds one {unit} to the {place} you pick.", "Starter"),
            ("grid", f"New questions, new {t.get('cols', 'columns')}", t.get("grow", f"Add a question to the form and {n} gets its {t.get('col', 'column')}."), "Starter"),
            ("check", "Never twice", f"A send that runs again finds its {unit} first, so nothing is added twice.", "Starter"),
            ("clock", "When and which fill", "Each row starts with when it was sent, the fill's id and the form.", "Starter"),
            ("refresh", "Never lost", f"Every fill is saved in Claritia first. If {n} is busy, the send tries again on its own.", "Starter"),
            ("cal", "Bookings too", "Forms that end in a meeting still add the fill, with the booking after it.", None),
        ],
        "steps": [
            (f"Connect {n}", t.get("connect", f"Go to Settings, then Integrations, and sign in with {n}.")),
            (f"Pick the {place}", t.get("pick", f"Open the form's Sync tab, add {n} and pick a {place}, or make a new one.")),
            ("Publish", f"New fills land in {n} as they come in."),
        ],
        "vis": lambda h: h["panel"](t["logo"], f"Add to {n}", "Event registration",
            h["row"](place.capitalize(), h["val"](t.get("example", "Registrations"), "table"))
            + h["maps"]([("Name", "Name"), ("Email", "Email"), ("Session", "Session"), ("Sent at", "Sent at")])),
        "faq": [
            (f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month. On Free, fills can go out as a CSV."),
            (f"What happens when I add a question?", t.get("grow", f"{n} gets a new {t.get('col', 'column')} for it on the next fill.")),
            (f"Can I use a {place} I already have?", t.get("own", f"Yes. Pick it in the form's Sync tab.")),
        ],
        "tpls": ["events-registration", "general-contact-us", "general-customer-feedback"],
        "short": f"A {unit} per fill",
    }


def work(n, t):
    item = t["item"]
    place = t.get("place", "list")
    return {
        "group": "Work tools", "plan": "Starter",
        "h1": f"{n} form integration",
        "desc": f"Connect Claritia forms to {n}: each fill becomes a {n} {item} in the {place} you pick, with every answer in it and a link back. On Starter, from $15/seat/month.",
        "sub": f"Turn every form fill into a {n} {item}, with each answer in it, in the {place} your team already works from.",
        "caps": [
            ("check", f"A {item} per fill", f"Each fill becomes one {item} in the {place} you pick.", "Starter"),
            ("type", "Every answer in it", f"The title names the form and the person. The {item} holds each answer and a link to the form.", "Starter"),
            ("user", t.get("who_t", "From the person"), t.get("who", "The person's name and email come with it."), "Starter"),
            ("refresh", "Never twice", f"A send that runs again finds its {item} first, so nothing is made twice.", "Starter"),
            ("form", "Any request form", "Bug reports, support requests, briefs and onboarding forms.", None),
            ("flow", "Then follow up", "Claritia's workflows can email the person back or book a call.", None),
        ],
        "steps": [
            (f"Connect {n}", t.get("connect", f"Go to Settings, then Integrations, and paste your {n} API key.")),
            (f"Pick the {place}", f"Open the form's Sync tab, add {n} and pick the {place}."),
            ("Publish", f"Each new fill shows up in {n} as a {item}."),
        ],
        "vis": lambda h: h["panel"](t["logo"], f"Send to {n}", "Support request",
            h["row"](place.capitalize(), h["val"](t.get("example", "Inbox"), "grid"))
            + h["row"]("Title", h["val"]("Support request from Ada Park"))
            + h["row"]("Body", h["val"]("Every answer and a link to the form"))),
        "faq": [
            (f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month."),
            (f"What goes in the {item}?", f"The form's name and the person's in the title, then every answer, the fill's id and a link to it in Claritia."),
            (f"Can it make two {item}s for one fill?", f"No. A send that runs again looks for its {item} first."),
        ],
        "tpls": t.get("tpls", ["it-support-ticket", "saas-bug-report", "agency-client-intake"]),
        "short": f"A {item} per fill",
    }


def docs(n, t):
    return {
        "group": "Documents", "plan": "Starter",
        "h1": t["h1"],
        "desc": f"Connect Claritia forms to {n}: each fill {t['makes']} from your own template, with the answers filled in. On Starter, from $15/seat/month.",
        "sub": f"Each form fill {t['makes']} from your own template, with every answer in its place.",
        "caps": [
            ("sign", t["cap1_t"], t["cap1"], "Starter"),
            ("type", "Tags in your template", "Write {{Question label}} where an answer goes, plus {{name}}, {{email}} and {{date}}.", "Starter"),
            ("check", "Never twice", "A send that runs again finds the document it made, so there's never a second one.", "Starter"),
            ("plug", "A link on each fill", f"Each fill in Claritia links to its {n} document.", "Starter"),
            ("form", "Any form", "Quotes, intakes, agreements and order forms.", None),
            ("refresh", "Never lost", f"Every fill is saved in Claritia first. If {n} is busy, the send tries again.", "Starter"),
        ],
        "steps": [
            (f"Connect {n}", t["connect"]),
            ("Pick the template", t["pick"]),
            ("Publish", f"Each new fill {t['makes']}."),
        ],
        "vis": lambda h: h["panel"](t["logo"], f"Send to {n}", "Client agreement",
            h["row"]("Template", h["val"](t.get("example", "Service agreement"), "sign"))
            + h["maps"]([("Full name", "{{name}}"), ("Email", "{{email}}"), ("Start date", "{{Start date}}")])),
        "faq": t["faq"] + [(f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month.")],
        "tpls": ["general-terms-agreement", "agency-client-intake", "general-quote-request"],
        "short": t["short"],
    }


def files(n, t):
    return {
        "group": "Files", "plan": "Starter",
        "h1": f"{n} form integration",
        "desc": f"Connect Claritia forms to {n}: the files people upload in a form are copied into a {n} folder for each fill. On Starter, from $15/seat/month.",
        "sub": f"Files people upload in your forms are copied into {n}, in a folder named after each fill.",
        "caps": [
            ("side", "A folder per fill", "Each fill's files go in a folder named for the form, the day and the fill.", "Starter"),
            ("grid", "Inside the folder you pick", t["pick_line"], "Starter"),
            ("check", "Never copied twice", "A copy that runs again finds each file by name first.", "Starter"),
            ("refresh", "Big files too", t.get("big", "Large files go up in parts, and a part that fails is sent again from where it stopped."), "Starter"),
            ("eyeoff", t.get("priv_t", "Only what it needs"), t.get("priv", f"Claritia only writes into the folder you pick in {n}."), "Starter"),
            ("form", "Any upload form", "Job applications, briefs, claims and intake forms.", None),
        ],
        "steps": [
            (f"Connect {n}", t["connect"]),
            ("Pick the folder", f"Open the form's Sync tab, add {n} and pick the folder."),
            ("Publish", f"Each fill's uploads are copied to {n}."),
        ],
        "vis": lambda h: h["panel"](t["logo"], f"Copy to {n}", "Job application",
            h["row"]("Folder", h["val"]("Applications", "side"))
            + h["row"]("Each fill", h["val"]("Job application 2026-11-06 7f3a"))),
        "faq": [
            (f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month."),
            ("Where do the files go?", f"Into a new folder for each fill, inside the one you pick in {n}."),
            ("Can a file be copied twice?", "No. A copy that runs again looks for each file by name first."),
        ],
        "tpls": ["hr-job-application", "agency-client-intake", "real-estate-rental-application"],
        "short": "Uploads in a folder",
    }


def analytics(n, t):
    return {
        "group": "Analytics", "plan": "Starter",
        "h1": f"{n} form integration",
        "desc": f"Connect Claritia forms to {n}: each fill goes to {n} as a Form Submitted event, tied to the person, and workflows send any event you name. On Starter, from $15/seat/month.",
        "sub": f"Send every form fill to {n} as an event, tied to the person by email, with their answers and where they came from.",
        "caps": [
            ("bolt", "Form Submitted events", "Each fill is one event with the form, the answers and the page, UTM and click ids.", "Starter"),
            ("user", "Tied to the person", "The email is the person's id, with their name and company set on them.", "Starter"),
            ("flow", "Any event from workflows", "A workflow's Analytics event step sends the name you pick, like Meeting Booked.", "Starter"),
            ("check", "Counted once", f"Each event carries its own id, so {n} counts a send that ran again once.", "Starter"),
            ("globe", "Your region", t.get("region", "US or EU, the one your project is in."), "Starter"),
            ("refresh", "Never lost", f"If {n} is busy, the send tries again on its own.", "Starter"),
        ],
        "steps": [
            (f"Connect {n}", f"Go to Settings, then Integrations, and paste your {n} {t['key']}."),
            ("Turn it on for a form", f"Open the form's Sync tab and add {n}."),
            ("Publish", f"Each fill shows up in {n} as a Form Submitted event."),
        ],
        "vis": lambda h: h["panel"](t["logo"], f"Send to {n}", "Demo request",
            h["row"]("Event", h["val"]("Form Submitted", "bolt"))
            + h["row"]("Person", h["val"]("ada@acme.com", "user"))
            + h["row"]("With", h["val"]("Answers, page, UTM"))),
        "faq": [
            (f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month."),
            ("What's in each event?", "The form, each answer by its label, and where the fill came from: the page, UTM tags and click ids."),
            ("Can a fill be counted twice?", f"No. Each event carries its own id, and {n} counts it once."),
        ],
        "tpls": ["saas-demo-request", "saas-onboarding-survey", "general-nps"],
        "short": "Form Submitted events",
    }


def files_like(kind):
    return {"crm": crm, "email": email, "rows": rows, "work": work, "docs": docs, "files": files, "analytics": analytics}[kind]


# One-off pages ---------------------------------------------------------------------------------------------------

def chat_page(n, t):
    return {
        "group": "Chat", "plan": "Starter",
        "h1": f"{n} form integration",
        "desc": f"Connect Claritia to {n}: post each new form lead in a channel, and send {n} messages from workflows when meetings are booked or canceled. On Starter, from $15/seat/month.",
        "sub": f"Post every new lead in a {n} channel, and message the team from workflows when a meeting is booked.",
        "caps": t["caps"],
        "steps": t["steps"],
        "vis": lambda h: h["panel"](t["logo"], f"Post to {n}", "Book a demo",
            h["row"]("Channel", h["val"](t["channel"], "users"))
            + h["row"]("Message", h["val"]("New fill on Book a demo: Ada Park"))
            + h["row"]("Pings", h["val"]("Off: an answer never pings anyone"))),
        "faq": t["faq"] + [(f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month.")],
        "tpls": ["saas-demo-request", "general-contact-us", "general-callback-request"],
        "short": t["short"],
    }


def site_page(n, t):
    return {
        "group": "Website", "plan": "Free",
        "h1": f"{n} form integration",
        "desc": f"Add Claritia forms to {n} with one snippet: in the page, full page, popup or slider. Multi-page forms, logic and booking with no code. On every plan, Free included.",
        "sub": f"Put a Claritia form on your {n} site with one snippet, in the page or as a popup, and let each lead book a meeting on the spot.",
        "caps": [
            ("globe", "One snippet", t["where"], None),
            ("side", "Six ways to show it", "In the page, full page, popup, slider, popover or side tab.", None),
            ("route", "Multi-page forms and logic", "Pages, show-if logic and prices, with no custom code.", None),
            ("cal", "Booking at the end", "Leads pick a time with the right person before they leave.", None),
            ("type", "Your site's look", f"Tia reads your {n} site and matches its fonts, colors and buttons.", "Pro"),
            ("eyeoff", "Spam stays out", "Cloudflare Turnstile and a hidden trap keep bots off your forms.", None),
        ],
        "steps": [
            ("Build or pick a form", "Describe it to Tia or start from a template."),
            ("Copy the snippet", "Open the form's Share tab, pick how it shows and copy the code."),
            (f"Paste it in {n}", t["paste"]),
        ],
        "vis": lambda h: f'<pre class="ix-code"><code>{esc(h["SCRIPT_TAG"] + chr(10) + h["EMBED"])}</code></pre>',
        "faq": [
            (f"How do I add a Claritia form to {n}?", t["how"]),
            ("Will it slow my site down?", "No. The script loads after the page, so your page draws first."),
            ("Where do the answers go?", "Into Claritia first, then to the tools you connect: your CRM, sheets, Slack, email lists and webhooks."),
            ("Is it free?", "Yes. Embeds work on every plan, Free included."),
        ],
        "tpls": ["general-contact-us", "saas-demo-request", "general-quote-request"],
        "short": "Forms with one snippet",
    }


def intake_page(n, t):
    """Typeform, Tally, Calendly, Cal.com: their answers or bookings come in by webhook."""
    return {
        "group": "Forms and booking", "plan": "Starter",
        "h1": t["h1"],
        "desc": t["desc"],
        "sub": t["sub"],
        "caps": t["caps"],
        "steps": [
            (f"Add {n} in Claritia", f"Go to Settings, then Integrations, add {n} and copy the webhook address."),
            (f"Paste it in {n}", t["paste"]),
            ("Done", t["done"]),
        ],
        "vis": lambda h: h["panel"](t["logo"], n, "Webhook",
            h["row"]("Address", h["val"]("app.tryclaritia.com/api/sources/hook/…", "hook"))
            + h["row"]("Signed", h["val"]("With your secret"))),
        "faq": t["faq"] + [(f"Which plan has the {n} integration?", "Starter and up, from $15/seat/month.")],
        "tpls": t["tpls"],
        "short": t["short"],
    }


def video_page(n, t):
    return {
        "group": "Video", "kind": "scheduling", "plan": t.get("plan", "Starter"),
        "h1": f"{n} scheduling integration",
        "desc": t["desc"],
        "sub": t["sub"],
        "caps": t["caps"],
        "steps": t["steps"],
        "vis": lambda h: h["panel"](t["logo"], "Intro call", "Meeting type",
            h["row"]("Length", h["seg"](["15 min", "30 min", "45 min"], "30 min"))
            + h["row"]("Location", h["val"](n, "video"))
            + h["row"]("Reminders", h["val"]("1 day and 1 hour before", "clock"))),
        "faq": t["faq"],
        "tpls": ["general-book-a-call", "consulting-consultation", "coaching-discovery-call"],
        "short": t["short"],
    }


def pay_page(n, t):
    return {
        "group": "Payments", "plan": "Starter",
        "h1": f"{n} form integration",
        "desc": f"Connect {n} to Claritia: take payments in forms and charge for meetings, paid to your own {n} account. On Starter, from $15/seat/month.",
        "sub": f"Take payments in your forms and charge for meetings, with the money paid straight to your own {n} account.",
        "caps": [
            ("card", "Payments in forms", f"Pick {n} under Paid with in a form's payment block.", "Starter"),
            ("cal", "Paid meetings", f"Guests pay with {n} to book any meeting type you put a price on.", "Starter"),
            ("check", "The right amount", "The amount always comes from Claritia's own price, never from the page.", "Starter"),
            ("clock", "The time is held", "While a guest pays, their time is held so nobody else takes it.", "Starter"),
            ("user", f"Your own {n} account", f"Guests pay you directly. {n}'s fees are yours, and Claritia never holds the money.", "Starter"),
            ("card", "Stripe too", f"Stripe stays the default; pick {n} where you want it.", "Starter"),
        ],
        "steps": [
            (f"Connect {n}", t["connect"]),
            ("Pick it", "Choose it under Paid with, in a form's payment block or a paid meeting type's price."),
            ("Get paid", f"Payments go to your {n} account and show on each fill or booking."),
        ],
        "vis": lambda h: h["panel"](t["logo"], "Consultation", "Meeting type",
            h["row"]("Price", h["val"]("$120", "card")) + h["row"]("Paid with", h["seg"](["Stripe", n], n))),
        "faq": [
            (f"Which plan has {n} payments?", "Starter and up, from $15/seat/month."),
            ("Who holds the money?", f"You do. Guests pay your own {n} account directly."),
            (f"Can I use {n} and Stripe?", f"Yes. Stripe is the default, and you pick {n} where you want it."),
        ],
        "tpls": ["general-invoice-payment", "legal-consultation-booking", "food-catering-calculator"],
        "short": "Payments and paid meetings",
    }


# The tools -------------------------------------------------------------------------------------------------------

KEYS = {"Pipedrive": "API token", "Close": "API key", "Freshsales": "address and API key", "Copper": "API key and email", "monday CRM": "API token"}

RAW = [
    # CRM
    ("pipedrive", "Pipedrive", "pipedrive.png", "crm", {"record": "person", "auth": "sign"}),
    ("attio", "Attio", "attio.png", "crm", {"record": "person", "auth": "sign"}),
    ("close", "Close", "close.png", "crm", {"record": "lead", "auth": "key", "key": "API key"}),
    ("zoho-crm", "Zoho CRM", "zoho.svg", "crm", {"record": "lead", "auth": "sign"}),
    ("dynamics-365", "Dynamics 365", "dynamics.png", "crm", {"record": "lead", "auth": "sign"}),
    ("gohighlevel", "GoHighLevel", "gohighlevel.png", "crm", {"record": "contact", "auth": "sign"}),
    ("freshsales", "Freshsales", "freshsales.png", "crm", {"record": "contact", "auth": "key", "key": "address and API key"}),
    ("copper", "Copper", "copper.png", "crm", {"record": "person", "auth": "key", "key": "API key and email"}),
    ("keap", "Keap", "keap.png", "crm", {"record": "contact", "auth": "sign"}),
    ("monday-crm", "monday CRM", "monday.png", "crm", {"record": "lead", "auth": "key", "key": "API token"}),
    # Email lists
    ("mailchimp", "Mailchimp", "mailchimp.svg", "email", {"list": "audience", "tags": True, "auth": "sign"}),
    ("klaviyo", "Klaviyo", "klaviyo.png", "email", {"list": "list"}),
    ("activecampaign", "ActiveCampaign", "activecampaign.png", "email", {"list": "list", "tags": True}),
    ("brevo", "Brevo", "brevo.svg", "email", {"list": "list"}),
    ("kit", "Kit", "kit.svg", "email", {"list": "form", "tags": True}),
    ("mailerlite", "MailerLite", "mailerlite.png", "email", {"list": "group"}),
    # Sheets and databases
    ("google-sheets", "Google Sheets", "googlesheets.svg", "rows", {"own": "Yes. Paste its link in the form's Sync tab, or make a new sheet there.", "example": "Registrations"}),
    ("airtable", "Airtable", "airtable.svg", "rows", {"unit": "record", "place": "table", "cols": "fields", "col": "field", "grow": "Fields a form needs that the table doesn't have yet are made for you."}),
    ("notion", "Notion", "notion.svg", "rows", {"unit": "database entry", "place": "database", "cols": "properties", "col": "property", "grow": "Each answer goes in as its property's type: text, number, date, select or checkbox."}),
    ("excel-online", "Excel Online", "excel.png", "rows", {"place": "workbook", "grow": "Each fill goes in a ClaritiaFills table on its own sheet, so your other sheets stay as they are.", "own": "Yes. Pick a workbook from the list or paste its link."}),
    ("postgresql", "PostgreSQL", "postgresql.svg", "rows", {"place": "table", "connect": "Go to Settings, then Integrations, and add the database's address, name and a user.", "pick": "Open the form's Sync tab, add PostgreSQL and name the table. Claritia makes it if it's missing.", "grow": "A new question adds its column to the table on the next fill.", "own": "Yes. Name a table you have, or a new one and Claritia makes it."}),
    ("mysql", "MySQL", "mysql.svg", "rows", {"place": "table", "connect": "Go to Settings, then Integrations, and add the database's address, name and a user.", "pick": "Open the form's Sync tab, add MySQL and name the table. Claritia makes it if it's missing.", "grow": "A new question adds its column to the table on the next fill.", "own": "Yes. Name a table you have, or a new one and Claritia makes it."}),
    # Work tools
    ("linear", "Linear", "linear.svg", "work", {"item": "issue", "place": "team", "connect": "Go to Settings, then Integrations, and sign in with Linear.", "example": "Support", "tpls": ["saas-bug-report", "general-product-feedback", "it-support-ticket"]}),
    ("trello", "Trello", "trello.svg", "work", {"item": "card", "place": "list", "connect": "Go to Settings, then Integrations, and paste your Trello API key and token.", "example": "New requests"}),
    ("clickup", "ClickUp", "clickup.svg", "work", {"item": "task", "place": "list", "connect": "Go to Settings, then Integrations, and sign in with ClickUp.", "example": "Client requests"}),
    ("monday", "monday.com", "monday.png", "work", {"item": "item", "place": "board", "connect": "Go to Settings, then Integrations, and paste your monday.com API token.", "example": "Requests"}),
    ("smartsuite", "SmartSuite", "smartsuite.png", "work", {"item": "record", "place": "table", "connect": "Go to Settings, then Integrations, and paste your SmartSuite API key and workspace.", "example": "Intake"}),
    ("zendesk", "Zendesk", "zendesk.svg", "work", {"item": "ticket", "place": "group", "who_t": "From the person", "who": "The ticket comes from the person who filled the form, so replies reach them.", "connect": "Go to Settings, then Integrations, and add your Zendesk subdomain, email and API token.", "example": "Support"}),
    ("freshdesk", "Freshdesk", "freshdesk.png", "work", {"item": "ticket", "place": "group", "who_t": "From the person", "who": "The ticket comes from the person who filled the form, so replies reach them.", "connect": "Go to Settings, then Integrations, and add your Freshdesk address and API key.", "example": "Support"}),
    ("intercom", "Intercom", "intercom.svg", "work", {"item": "conversation", "place": "workspace", "who_t": "Found by email", "who": "Intercom finds the person by email, or makes a lead, and the conversation is from them.", "connect": "Go to Settings, then Integrations, and paste your Intercom access token.", "example": "Inbox"}),
    # Documents
    ("google-docs", "Google Docs", "googledocs.svg", "docs", {"h1": "Google Docs form integration", "makes": "makes a Google Doc", "short": "A doc from your template",
        "cap1_t": "A doc per fill", "cap1": "Each fill makes a new Google Doc from your template, named for the form and the person.",
        "connect": "Go to Settings, then Integrations, and sign in with Google.", "pick": "Open the form's Sync tab, add Google Docs and paste your template doc's link.",
        "faq": [("What stays from my template?", "The text with each paragraph's heading style, and bold, italic and underline. Tables, pictures, lists, colors and fonts are left out.")]}),
    ("docusign", "DocuSign", "docusign.png", "docs", {"h1": "DocuSign form integration", "makes": "sends a DocuSign envelope to sign", "short": "Send to sign",
        "cap1_t": "Sent to sign", "cap1": "Each fill sends an envelope from your template to the person as its first signer.",
        "connect": "Go to Settings, then Integrations, and sign in with DocuSign.", "pick": "Open the form's Sync tab, add DocuSign and pick the template.",
        "faq": [("Who signs?", "The person who filled the form, as the template's first signer role.")]}),
    ("pandadoc", "PandaDoc", "pandadoc.png", "docs", {"h1": "PandaDoc form integration", "makes": "sends a PandaDoc document", "short": "A document sent to the person",
        "cap1_t": "Sent to the person", "cap1": "Each fill makes a PandaDoc document from your template and sends it to the person.",
        "connect": "Go to Settings, then Integrations, and paste your PandaDoc API key.", "pick": "Open the form's Sync tab, add PandaDoc and pick the template.",
        "faq": [("Who gets the document?", "The person who filled the form, by the email they gave.")]}),
    # Files
    ("google-drive", "Google Drive", "googledrive.svg", "files", {"connect": "Go to Settings, then Integrations, and sign in with Google.", "pick_line": "Claritia makes the folder for you in your Drive.", "priv_t": "Only its own folders", "priv": "Claritia asks only for the files it makes, so it never sees the rest of your Drive."}),
    ("onedrive", "OneDrive", "onedrive.svg", "files", {"connect": "Go to Settings, then Integrations, and sign in with Microsoft.", "pick_line": "Pick a folder from the list, or make a new one."}),
    ("dropbox", "Dropbox", "dropbox.svg", "files", {"connect": "Go to Settings, then Integrations, and sign in with Dropbox.", "pick_line": "Pick a folder from the list, or make a new one."}),
    ("box", "Box", "box.svg", "files", {"connect": "Go to Settings, then Integrations, and sign in with Box.", "pick_line": "Pick a folder from the list, or make a new one.", "big": "Files up to the form's 20 MB limit go up in one piece."}),
    ("amazon-s3", "Amazon S3", "s3.png", "files", {"connect": "Go to Settings, then Integrations, and add your bucket, region, folder and an access key.", "pick_line": "Files go in the bucket and folder your connection names.", "priv_t": "Your own key", "priv": "Claritia writes with the key you give it, into the folder you name."}),
    # Analytics
    ("segment", "Segment", "segment.png", "analytics", {"key": "write key", "region": "US or EU, the one your workspace is in."}),
    ("posthog", "PostHog", "posthog.svg", "analytics", {"key": "project API key", "region": "US, EU or your own PostHog address."}),
    ("mixpanel", "Mixpanel", "mixpanel.svg", "analytics", {"key": "project token"}),
    ("amplitude", "Amplitude", "amplitude.png", "analytics", {"key": "API key"}),
]

ONE_OFF = {
    "microsoft-teams": ("Microsoft Teams", "teams.png", chat_page, {
        "channel": "Sales / Leads", "short": "Lead alerts and Teams links",
        "caps": [
            ("bolt", "New lead alerts", "Pick a team and channel, and each fill posts there with its answers.", "Starter"),
            ("flow", "A Teams step in workflows", "Post to Teams from any workflow, like when a meeting is booked or canceled.", "Starter"),
            ("eyeoff", "Long answers cut short", "Long answers are cut to fit, with a link to the full fill in Claritia.", "Starter"),
            ("check", "Clear when a channel's gone", "A deleted channel fails with what to do, never in silence.", "Starter"),
            ("video", "Teams meeting links", "Work and school accounts get a Teams link on each booked meeting.", None),
            ("refresh", "Never lost", "If Teams is busy, the post tries again on its own.", "Starter"),
        ],
        "steps": [("Connect Microsoft", "Go to Settings, then Integrations, and sign in with Microsoft."), ("Pick the channel", "Open the form's Sync tab, add Teams and pick a team and channel."), ("Publish", "New fills post in the channel as they come in.")],
        "faq": [("Does it add Teams links to meetings?", "Yes. Connect Outlook with a work or school Microsoft 365 account and pick Teams as the location."), ("Can an answer ping the whole channel?", "No. Alerts never mention anyone.")]}),
    "discord": ("Discord", "discord.svg", chat_page, {
        "channel": "#leads", "short": "Lead alerts in a channel",
        "caps": [
            ("bolt", "New lead alerts", "Each fill posts in the channel you pick, with its answers.", "Starter"),
            ("plug", "Add to Discord", "Pick the server and channel while signing in. No webhook to copy.", "Starter"),
            ("flow", "A Discord step in workflows", "Post to Discord from any workflow, like when a meeting is booked.", "Starter"),
            ("eyeoff", "No pings", "Mentions are off, so an answer can never ping a channel.", "Starter"),
            ("clock", "Rate limits handled", "When Discord says slow down, Claritia waits and posts once.", "Starter"),
            ("check", "Clear when a channel's gone", "A deleted channel or webhook fails with what to do.", "Starter"),
        ],
        "steps": [("Add to Discord", "Go to Settings, then Integrations, click Add to Discord and pick the channel."), ("Turn it on for a form", "Open the form's Sync tab and add Discord."), ("Publish", "New fills post in the channel as they come in.")],
        "faq": [("Can an answer ping @everyone?", "No. Mentions are turned off on every post."), ("Can I post from workflows?", "Yes. Add a Discord message step to any workflow.")]}),
    "wordpress": ("WordPress", "wordpress.svg", site_page, {"where": "Paste one snippet into a Custom HTML block. It works on every page and on phones.", "paste": "In the block editor, add a Custom HTML block where the form goes and paste the snippet.", "how": "Open the form's Share tab, copy the snippet, then paste it into a Custom HTML block where the form goes."}),
    "framer": ("Framer", "framer.svg", site_page, {"where": "Paste one snippet into an Embed component. It works on every page and on phones.", "paste": "In Framer, add an Embed component where the form goes and paste the snippet.", "how": "Open the form's Share tab, copy the snippet, then paste it into an Embed component in Framer."}),
    "shopify": ("Shopify", "shopify.svg", site_page, {"where": "Paste one snippet into a Custom Liquid section. It works on every page and on phones.", "paste": "In your theme editor, add a Custom Liquid section where the form goes and paste the snippet.", "how": "Open the form's Share tab, copy the snippet, then paste it into a Custom Liquid section in your theme editor."}),
    "squarespace": ("Squarespace", "squarespace.svg", site_page, {"where": "Paste one snippet into a Code block. It works on every page and on phones.", "paste": "In Squarespace, add a Code block where the form goes and paste the snippet.", "how": "Open the form's Share tab, copy the snippet, then paste it into a Code block in Squarespace."}),
    "typeform": ("Typeform", "typeform.svg", intake_page, {
        "h1": "Typeform integration", "short": "Answers come in",
        "desc": "Connect Typeform to Claritia: each Typeform answer comes into Claritia, so leads book a meeting, go to your CRM and get your follow-ups. On Starter, from $15/seat/month.",
        "sub": "Keep your Typeform. Each answer comes into Claritia, so the lead goes to your CRM, gets your follow-ups and can book a meeting.",
        "caps": [("hook", "Answers by webhook", "Each Typeform answer comes into Claritia the moment it's sent.", "Starter"), ("check", "Signed and checked", "Claritia checks each one with your Typeform secret.", "Starter"), ("user", "A contact for each", "Each answer becomes the person behind it in Claritia.", "Starter"), ("plug", "On to your tools", "From there it goes to your CRM, sheets, Slack and email lists.", "Starter"), ("flow", "Workflows follow up", "Send a reminder or a follow-up from Claritia's workflows.", "Starter"), ("form", "Or move to Claritia", "Rebuild the form in Claritia and book the meeting on the same page.", None)],
        "paste": "In Typeform, open Connect, then Webhooks, add the address and turn it on.", "done": "Each new answer comes into Claritia.",
        "faq": [("Do I have to leave Typeform?", "No. Keep your Typeform and its answers come into Claritia."), ("Is each answer checked?", "Yes. Add your Typeform webhook secret and Claritia checks every answer with it.")],
        "tpls": ["saas-demo-request", "general-customer-feedback", "general-contact-us"]}),
    "tally": ("Tally", "tally.png", intake_page, {
        "h1": "Tally integration", "short": "Answers come in",
        "desc": "Connect Tally to Claritia: each Tally answer comes into Claritia, so leads book a meeting, go to your CRM and get your follow-ups. On Starter, from $15/seat/month.",
        "sub": "Keep your Tally forms. Each answer comes into Claritia, so the lead goes to your CRM, gets your follow-ups and can book a meeting.",
        "caps": [("hook", "Answers by webhook", "Each Tally answer comes into Claritia the moment it's sent.", "Starter"), ("check", "Signed and checked", "Claritia checks each one with your Tally signing secret.", "Starter"), ("user", "A contact for each", "Each answer becomes the person behind it in Claritia.", "Starter"), ("plug", "On to your tools", "From there it goes to your CRM, sheets, Slack and email lists.", "Starter"), ("flow", "Workflows follow up", "Send a reminder or a follow-up from Claritia's workflows.", "Starter"), ("form", "Or move to Claritia", "Rebuild the form in Claritia and book the meeting on the same page.", None)],
        "paste": "In Tally, open the form's Integrations, add a webhook with the address and save.", "done": "Each new answer comes into Claritia.",
        "faq": [("Do I have to leave Tally?", "No. Keep your Tally forms and their answers come into Claritia.")],
        "tpls": ["general-contact-us", "general-waitlist", "general-customer-feedback"]}),
    "calendly": ("Calendly", "calendly.svg", intake_page, {
        "h1": "Calendly integration", "short": "Bookings come in",
        "desc": "Connect Calendly to Claritia: each Calendly booking comes in for your follow-ups, and forms can book with your Calendly. Or move your meetings to Claritia. On Starter.",
        "sub": "Keep Calendly if you like. Its bookings come into Claritia for your follow-ups, and a Claritia form can end with your Calendly page.",
        "caps": [("hook", "Bookings by webhook", "Each new Calendly booking comes into Claritia.", "Starter"), ("cal", "Book from a form", "End a Claritia form with your Calendly page.", "Starter"), ("user", "A contact for each", "Each booking becomes the person behind it in Claritia.", "Starter"), ("flow", "Workflows follow up", "Send reminders and follow-ups from Claritia's workflows.", "Starter"), ("plug", "On to your tools", "From there it goes to your CRM, sheets and Slack.", "Starter"), ("users", "Or move to Claritia", "Claritia's own scheduler has round robin, routing and team pages.", None)],
        "paste": "In Calendly, open Integrations, then Webhooks, and add the address.", "done": "Each new booking comes into Claritia.",
        "faq": [("Can I keep Calendly?", "Yes. Its bookings come into Claritia, and a form can end with your Calendly page."), ("Can Claritia replace Calendly?", "Yes. Claritia's own scheduler books on Google Calendar and Outlook, with round robin and routing.")],
        "tpls": ["general-book-a-call", "saas-demo-request", "consulting-consultation"]}),
    "cal-com": ("Cal.com", "calcom.svg", intake_page, {
        "h1": "Cal.com integration", "short": "Bookings come in",
        "desc": "Connect Cal.com to Claritia: each Cal.com booking comes in for your follow-ups, and forms can book with your Cal.com page. Or move your meetings to Claritia. On Starter.",
        "sub": "Keep Cal.com if you like. Its bookings come into Claritia for your follow-ups, and a Claritia form can end with your Cal.com page.",
        "caps": [("hook", "Bookings by webhook", "Each new Cal.com booking comes into Claritia.", "Starter"), ("cal", "Book from a form", "End a Claritia form with your Cal.com page.", "Starter"), ("user", "A contact for each", "Each booking becomes the person behind it in Claritia.", "Starter"), ("flow", "Workflows follow up", "Send reminders and follow-ups from Claritia's workflows.", "Starter"), ("plug", "On to your tools", "From there it goes to your CRM, sheets and Slack.", "Starter"), ("users", "Or move to Claritia", "Claritia's own scheduler has round robin, routing and team pages.", None)],
        "paste": "In Cal.com, open Settings, then Developer, then Webhooks, and add the address.", "done": "Each new booking comes into Claritia.",
        "faq": [("Can I keep Cal.com?", "Yes. Its bookings come into Claritia, and a form can end with your Cal.com page.")],
        "tpls": ["general-book-a-call", "saas-quick-demo", "consulting-consultation"]}),
    "google-meet": ("Google Meet", "meet.svg", video_page, {
        "plan": "Free", "short": "A Meet link for each meeting",
        "desc": "Add Google Meet to Claritia meetings: every booking gets its own Meet link on the calendar event and the invite. On every plan, Free included.",
        "sub": "Every booked meeting gets its own Google Meet link, on the host's calendar event and the guest's invite.",
        "caps": [("video", "A Meet link for each meeting", "Each booking gets its own Meet link from the host's Google Calendar.", None), ("cal", "On the invite", "The link goes on the event and the guest's invite.", None), ("users", "Team meetings", "In a round robin, the link is made on the calendar of the person who gets the lead.", "Pro"), ("refresh", "Moves keep the link", "A rescheduled meeting keeps its Meet link.", None), ("mail", "Reminders built in", "Confirmations go out at once, then reminders before the meeting.", None), ("check", "Free", "Meet links are on every plan.", None)],
        "steps": [("Connect Google Calendar", "Sign in with Google from Meetings."), ("Pick Google Meet", "Open a meeting type and set its location to Google Meet."), ("Share your booking page", "Each booking gets its own Meet link.")],
        "faq": [("Is it free?", "Yes. Google Meet links are on every plan, Free included."), ("Does the guest need Google?", "No. Anyone can join a Meet link from a browser.")]}),
    "webex": ("Webex", "webex.svg", video_page, {
        "short": "A Webex meeting for each booking",
        "desc": "Connect Webex to Claritia: every booking gets its own Webex meeting and link, moved with the booking and removed when it's canceled. On Starter, from $15/seat/month.",
        "sub": "Every booked meeting gets its own Webex meeting and link, moved when the booking moves and removed when it's canceled.",
        "caps": [("video", "A Webex meeting for each booking", "Each booking makes its own Webex meeting.", "Starter"), ("cal", "On the invite", "The join link goes on the calendar event and the guest's invite.", "Starter"), ("refresh", "Moves with the booking", "A rescheduled booking moves its Webex meeting. A cancel deletes it.", "Starter"), ("check", "Never two meetings", "If a step runs again, Claritia uses the Webex meeting it already made.", "Starter"), ("clock", "Tries again", "If the link fails to make, the booking stays and Claritia tries again.", "Starter"), ("mail", "Reminders built in", "Confirmations go out at once, then reminders before the meeting.", None)],
        "steps": [("Connect Webex", "Go to Settings, then Integrations, and sign in with Webex."), ("Pick Webex", "Open a meeting type and set its location to Webex."), ("Share your booking page", "Each booking gets its own Webex meeting.")],
        "faq": [("Which plan has Webex?", "Starter and up, from $15/seat/month."), ("What happens when a meeting moves?", "The Webex meeting moves with it. A cancel deletes it.")]}),
    "whereby": ("Whereby", "whereby.png", video_page, {
        "short": "A Whereby room for each booking",
        "desc": "Connect Whereby to Claritia: every booking gets its own Whereby room, open from the start until an hour after the end. On Starter, from $15/seat/month.",
        "sub": "Every booked meeting gets its own Whereby room, with no download for the guest.",
        "caps": [("video", "A room for each booking", "Each booking makes its own Whereby room.", "Starter"), ("cal", "On the invite", "The room's link goes on the calendar event and the guest's invite.", "Starter"), ("clock", "Open as long as needed", "Each room stays open an hour past the meeting's end.", "Starter"), ("refresh", "Moves with the booking", "A rescheduled booking gets a new room; a cancel removes it.", "Starter"), ("check", "Never two rooms", "If a step runs again, Claritia uses the room it already made.", "Starter"), ("globe", "No download", "Guests join from the browser.", None)],
        "steps": [("Connect Whereby", "Go to Settings, then Integrations, and paste your Whereby Embedded API key."), ("Pick Whereby", "Open a meeting type and set its location to Whereby."), ("Share your booking page", "Each booking gets its own Whereby room.")],
        "faq": [("Which plan has Whereby?", "Starter and up, from $15/seat/month."), ("Which Whereby key do I need?", "An Embedded API key from your Whereby account.")]}),
    "paypal": ("PayPal", "paypal.svg", pay_page, {"connect": "Go to Settings, then Integrations, and add your PayPal REST app's Client ID, Secret and Webhook ID."}),
    "square": ("Square", "square.svg", pay_page, {"connect": "Go to Settings, then Integrations, and add your Square access token, location and webhook signature key."}),
}

# Bigger one-offs, written in full.
FULL = {
    "omniscient": {"name": "Omniscient", "logo": "omniscient.svg", "group": "CRM", "plan": "Starter",
        "h1": "Omniscient form integration", "short": "Leads and owners, both ways",
        "desc": "Connect Claritia forms to Omniscient: each fill becomes an Omniscient person and opportunity, and leads book with their owner. One click on Omniscient's approve page. On Starter.",
        "sub": "Send every form fill to Omniscient, Claritia's sister CRM, with one click to connect. Each lead books with the right person on the same page.",
        "caps": [("user", "A person for each fill", "Each fill makes an Omniscient person, or finds the one with that email.", "Starter"), ("plug", "One-click connect", "Approve Claritia on Omniscient's own page. No keys.", "Starter"), ("check", "No duplicates", "The same person filling twice is one record in Omniscient.", "Starter"), ("route", "Two-way", "People in Omniscient come back into Claritia, so routing and booking know them.", "Starter"), ("cal", "Book on the same page", "After the form, the lead picks a time with the right person.", None), ("refresh", "Never lost", "Every fill is saved in Claritia first. The send tries again on its own.", "Starter")],
        "steps": [("Connect Omniscient", "Go to Settings, then Integrations, click Connect Omniscient and approve."), ("Pick it on a form", "Open the form's Sync tab and add Omniscient."), ("Publish", "New fills go to Omniscient as they come in.")],
        "vis": lambda h: h["panel"]("omniscient.svg", "Send to Omniscient", "Demo request", h["row"]("When the email is already in Omniscient", h["seg"](["Update it", "Leave it"], "Update it"), "Matched by email") + h["maps"]([("Work email", "Email"), ("Full name", "Name"), ("Company", "Company")])),
        "faq": [("Which plan has the Omniscient integration?", "Starter and up, from $15/seat/month."), ("What is Omniscient?", "A CRM with deal rooms, made by the team behind Claritia, on the same look and sign-in.")],
        "tpls": ["saas-demo-request", "saas-contact-sales", "general-book-a-call"]},
    "twilio": {"name": "Twilio", "logo": "twilio.svg", "group": "Texts", "plan": "Starter",
        "h1": "Twilio SMS and WhatsApp integration", "short": "Text and WhatsApp reminders",
        "desc": "Connect your own Twilio to Claritia: send SMS and WhatsApp reminders and follow-ups from workflows, only to people who said yes, with STOP handled. On Starter, from $15/seat/month.",
        "sub": "Send text and WhatsApp reminders and follow-ups from Claritia's workflows, through your own Twilio number, only to people who said yes.",
        "caps": [("phone", "Text message steps", "Add a Text message step to any workflow: reminders, no-show follow-ups, notes after a fill.", "Starter"), ("phone", "WhatsApp steps", "Send the same from your WhatsApp sender.", "Starter"), ("check", "Only with consent", "A text goes only to someone whose latest text consent is yes.", "Starter"), ("eyeoff", "STOP handled", "Replies like STOP turn texts off for that number at once.", "Starter"), ("mail", "Email when a text can't go", "No mobile or no consent? The reminder goes by email instead.", "Starter"), ("cal", "Reminders before meetings", "Start from the Text reminders template: a text an hour before each meeting.", "Starter")],
        "steps": [("Connect Twilio", "Go to Settings, then Integrations, and add your account SID, auth token and number."), ("Ask for consent", "Add a Text consent box to a form, or a text consent question to a booking page."), ("Add a text step", "Add a Text message or WhatsApp step to a workflow.")],
        "vis": lambda h: h["panel"]("twilio.svg", "Text reminder", "Workflow step", h["row"]("When", h["val"]("1 hour before the meeting", "clock")) + h["row"]("Message", h["val"]("See you at 3:00 PM. Reply STOP to opt out.")) + h["row"]("If it can't go", h["val"]("Send by email", "mail"))),
        "faq": [("Whose Twilio account is it?", "Yours. Texts go from your own Twilio number, and Twilio bills you for them."), ("Do people have to say yes first?", "Yes. A text goes only to someone whose latest text consent is yes."), ("What happens when someone replies STOP?", "Texts to that number stop at once."), ("Which plan has texts?", "Starter and up, from $15/seat/month.")],
        "tpls": ["healthcare-appointment", "beauty-massage-appointment", "general-book-a-call"]},
    "meta": {"name": "Meta", "logo": "meta.svg", "group": "Ads", "plan": "Starter",
        "h1": "Meta Pixel and Conversions API for forms", "short": "Pixel and Conversions API",
        "desc": "Send Claritia form views, fills and bookings to your Meta Pixel, and to the Conversions API from the server, after consent. Pixel on every plan; Conversions API on Starter.",
        "sub": "Send each form's views, fills and booked meetings to your Meta Pixel, and to the Conversions API from the server, so ad reporting counts every lead.",
        "caps": [("bolt", "Pixel events", "Views, starts, fills and bookings go to your Meta Pixel.", None), ("globe", "Conversions API", "Fills and bookings go to Meta from the server too, so ad blockers don't lose them.", "Starter"), ("check", "Counted once", "The browser and server events share an id, so Meta counts each one once.", "Starter"), ("eyeoff", "After consent", "Nothing goes to Meta until the person agrees.", None), ("cal", "Booked meetings", "A booked meeting is its own event, so you can optimize for meetings.", "Starter"), ("refresh", "Never lost", "Server events try again on their own.", "Starter")],
        "steps": [("Add your Pixel", "Open the form's Settings, then Tracking, and paste your Pixel ID."), ("Turn on Conversions API", "Connect Meta in Settings, then Integrations, with a system user token, and turn it on."), ("Publish", "Each view, fill and booking goes to Meta.")],
        "vis": lambda h: h["panel"]("meta.svg", "Tracking", "Form settings", h["row"]("Meta Pixel ID", h["val"]("1234567890")) + h["row"]("Conversions API", h["tog"]()) + h["row"]("After consent", h["tog"]())),
        "faq": [("Do I need the Conversions API?", "It's optional. It sends fills and bookings from the server, so Meta counts leads an ad blocker would hide."), ("Does it count a lead twice?", "No. The browser and server events share an id."), ("Which plan has it?", "The Pixel works on every plan. The Conversions API is on Starter and up.")],
        "tpls": ["saas-demo-request", "general-quote-request", "events-registration"]},
    "google-ads": {"name": "Google Ads", "logo": "googleads.svg", "group": "Ads", "plan": "Starter",
        "h1": "Google Ads conversion tracking for forms", "short": "Conversions and offline uploads",
        "desc": "Track Claritia form fills and booked meetings as Google Ads conversions, in the browser and as offline conversions from the server, after consent. On Starter.",
        "sub": "Count each form fill and booked meeting as a Google Ads conversion, and send them from the server too so none are lost.",
        "caps": [("bolt", "The conversion tag", "Fills and bookings fire your Google Ads conversion.", None), ("globe", "Offline conversions", "Fills and bookings go to Google Ads from the server, with the click id.", "Starter"), ("grid", "Pick from your account", "Choose the Google Ads account and conversion action from lists.", "Starter"), ("eyeoff", "After consent", "Nothing goes to Google until the person agrees, with Consent Mode.", None), ("cal", "Booked meetings", "Count meetings booked, not only fills.", "Starter"), ("refresh", "Never lost", "Offline uploads try again on their own.", "Starter")],
        "steps": [("Add the tag", "Open the form's Settings, then Tracking, and paste the conversion ID and label."), ("Turn on offline conversions", "Connect Google Ads in Settings, then Integrations, and pick the account and action."), ("Publish", "Each fill and booking counts in Google Ads.")],
        "vis": lambda h: h["panel"]("googleads.svg", "Tracking", "Form settings", h["row"]("Conversion ID", h["val"]("AW-123456789")) + h["row"]("Offline conversions", h["tog"]()) + h["row"]("Conversion action", h["val"]("Booked meeting"))),
        "faq": [("What's an offline conversion?", "A fill or booking sent to Google Ads from the server with the ad click's id, so it counts even when the browser tag was blocked."), ("Which plan has it?", "The conversion tag works on every plan. Offline conversions are on Starter and up.")],
        "tpls": ["saas-demo-request", "general-quote-request", "legal-consultation-booking"]},
    "google-analytics": {"name": "Google Analytics", "logo": "googleanalytics.svg", "group": "Ads", "plan": "Free",
        "h1": "Google Analytics form tracking", "short": "GA4 and Tag Manager events",
        "desc": "Send Claritia form views, starts, fills and bookings to Google Analytics 4 and Google Tag Manager, after consent. On every plan, Free included.",
        "sub": "See each form's views, starts, fills and booked meetings in Google Analytics 4, or push them to Google Tag Manager.",
        "caps": [("bolt", "GA4 events", "Views, starts, fills and bookings go to your GA4 property.", None), ("grid", "Google Tag Manager", "Push the same events to your dataLayer for your own tags.", None), ("eyeoff", "After consent", "Consent Mode is on, so nothing counts until the person agrees.", None), ("route", "Where they came from", "UTM tags and the page travel with each fill.", None), ("cal", "Booked meetings", "A booked meeting is its own event.", None), ("check", "Free", "On every plan.", None)],
        "steps": [("Open Tracking", "Open the form's Settings, then Tracking."), ("Paste your ID", "Paste your GA4 measurement ID, or turn on Google Tag Manager."), ("Publish", "Each view, start, fill and booking shows in Google Analytics.")],
        "vis": lambda h: h["panel"]("googleanalytics.svg", "Tracking", "Form settings", h["row"]("GA4 measurement ID", h["val"]("G-XXXXXXX")) + h["row"]("Google Tag Manager", h["tog"]()) + h["row"]("After consent", h["tog"]())),
        "faq": [("Is it free?", "Yes. Google Analytics and Tag Manager work on every plan."), ("Which events are sent?", "Views, starts, fills and booked meetings.")],
        "tpls": ["saas-demo-request", "general-contact-us", "general-newsletter"]},
    "google-forms": {"name": "Google Forms", "logo": "googleforms.svg", "group": "Forms and booking", "plan": "Free",
        "h1": "Import Google Forms to Claritia", "short": "Import a form in one step",
        "desc": "Import a Google Form into Claritia in one step: questions, options and required ones come over, ready for pages, logic, routing and booking. On every plan, Free included.",
        "sub": "Paste a Google Form's link and get the same form in Claritia, ready for pages, logic, your brand and booking at the end.",
        "caps": [("form", "Every question comes over", "Short and long text, multiple choice, checkboxes, dropdowns, scales, dates and more.", None), ("check", "Kept as it was", "Labels, help text, options and required questions stay the same.", None), ("eyeoff", "Read-only", "Claritia only reads the form. Your Google Form isn't changed.", None), ("cal", "Add booking", "End the form with a meeting booked on the right calendar.", None), ("type", "Your brand", "Tia dresses the form in your site's look.", "Pro"), ("plug", "On to your tools", "Fills go to your CRM, sheets and Slack.", "Starter")],
        "steps": [("Open Forms", "In Claritia, go to Forms and pick Import from Google Forms."), ("Paste the link", "Paste the form's edit link. The first time, sign in with Google."), ("Make it yours", "The form opens in Form Studio as a draft.")],
        "vis": lambda h: h["panel"]("googleforms.svg", "Import from Google Forms", "Forms", h["row"]("Edit link", h["val"]("docs.google.com/forms/d/…/edit")) + h["row"]("Opens as", h["val"]("A draft in Form Studio"))),
        "faq": [("Does it change my Google Form?", "No. Claritia only reads it."), ("Do answers come over?", "No. The questions come over, so new answers come to Claritia."), ("Is it free?", "Yes. The import works on every plan.")],
        "tpls": ["general-contact-us", "events-registration", "general-customer-feedback"]},
    "webhooks": {"name": "Webhooks", "logo": "webhooks.svg", "group": "Developers", "plan": "Free",
        "h1": "Form webhooks", "short": "A signed POST of each fill",
        "desc": "Send each Claritia form fill to any address as a signed webhook, from a form or a workflow step, with retries. On every plan, Free included.",
        "sub": "Send each form fill to your own address as a signed POST, from a form or from a workflow step, with retries when it fails.",
        "caps": [("hook", "A POST per fill", "Each fill goes to your address as JSON.", None), ("check", "Signed", "Each request is signed with your secret, so you know it's from Claritia.", None), ("refresh", "Retries", "A send that fails tries again with longer waits, and you can send it again.", None), ("flow", "From workflows", "A webhook step sends from any workflow, like when a meeting is booked.", None), ("table", "The sync log", "See each send, its answer and when it went.", None), ("check", "Free", "Webhooks work on every plan.", None)],
        "steps": [("Add the address", "Open the form's Sync tab and add a webhook with your address."), ("Check the signature", "Use your secret to check each request on your side."), ("Publish", "Each new fill goes to your address.")],
        "vis": lambda h: h["panel"]("webhooks.svg", "Webhook", "Demo request", h["row"]("Address", h["val"]("https://example.com/hooks/claritia", "hook")) + h["row"]("Signed", h["tog"]()) + h["row"]("Retries", h["val"]("On, with longer waits", "refresh"))),
        "faq": [("Is it free?", "Yes. Webhooks work on every plan, Free included."), ("Are requests signed?", "Yes. Each one carries a signature made with your secret."), ("What if my server is down?", "The send tries again with longer waits, and you can send it again from the sync log.")],
        "tpls": ["general-contact-us", "saas-demo-request", "general-quote-request"]},
    "gmail": {"name": "Gmail", "logo": "gmail.svg", "group": "Email", "plan": "Starter",
        "h1": "Send from Gmail with Claritia", "short": "Emails from your own Gmail",
        "desc": "Send Claritia workflow and meeting emails from your own Gmail, so replies land in your inbox. Held to Gmail's daily limit, with your team's domain as the fallback. On Starter.",
        "sub": "Send workflow follow-ups and meeting emails from your own Gmail, so guests reply to you and it lands in your inbox.",
        "caps": [("mail", "From your Gmail", "Follow-ups from you and meeting emails to your guests go from your Gmail.", "Starter"), ("cal", "Meeting emails too", "Confirmations, changes, cancels, reminders and no-show follow-ups.", "Starter"), ("clock", "Inside Gmail's limit", "Claritia keeps to the daily limit, and waits when it's reached.", "Starter"), ("refresh", "A fallback that works", "If the sign-in is gone, emails go from your team's domain and you're told once.", "Starter"), ("eyeoff", "Send only", "Claritia can send from your Gmail, never read it.", "Starter"), ("check", "Never sent twice", "An email with no clear answer is never sent again.", "Starter")],
        "steps": [("Open My calendar", "Go to Meetings, then Availability, then My calendar."), ("Connect Gmail", "Under Email from you, click Connect Gmail and sign in."), ("Done", "Your follow-ups and meeting emails now go from your Gmail.")],
        "vis": lambda h: h["panel"]("gmail.svg", "Email from you", "My calendar", h["row"]("Sending from", h["val"]("ada@acme.com", "mail")) + h["row"]("Today", h["val"]("12 of 450 sent"))),
        "faq": [("Can Claritia read my email?", "No. It can only send."), ("What if I hit Gmail's limit?", "Emails wait until there's room, then go."), ("Does it work with Outlook?", "Yes. Connect Outlook the same way.")],
        "tpls": ["general-book-a-call", "saas-demo-request", "consulting-consultation"]},
}


def build(helpers):
    """Every page here, in the shape tools/integrations.py's TOOLS uses."""
    h = dict(helpers)
    out = {}
    for slug, name, logo, kind, facts in RAW:
        t = dict(facts, logo=logo)
        page = files_like(kind)(name, t)
        page.update(name=name, logo=logo)
        page["vis"] = (lambda f: (lambda: f(h)))(page["vis"])
        out[slug] = page
    for slug, (name, logo, make, facts) in ONE_OFF.items():
        t = dict(facts, logo=logo)
        page = make(name, t)
        page.update(name=name, logo=logo)
        page["vis"] = (lambda f: (lambda: f(h)))(page["vis"])
        out[slug] = page
    for slug, page in FULL.items():
        page = dict(page)
        page["vis"] = (lambda f: (lambda: f(h)))(page["vis"])
        out[slug] = page
    return out
