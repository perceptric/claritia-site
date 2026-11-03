"""Builds /pricing/index.html: the plans, a user count that prices every plan, every feature side by side and questions. The plans follow docs/pricing.md in the app repo (dev-arrowsterr/claritia). Run: python3 tools/pricing.py"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shell  # noqa: E402

esc = shell.esc

# The plans. Prices are dollars per user a month; yearly is the monthly price with 20% off, billed once a year.
PLANS = [
    {"id": "free", "name": "Free", "for": "For one person who wants to try it", "m": 0, "y": 0,
     "btn": ("Start free", "https://app.tryclaritia.com", "ghost"),
     "top": ["Unlimited forms", "250 form answers a month", "1 calendar per user", "100 AI credits a month", "1 meeting type", "435 form templates", "Google Calendar or Outlook", "Forms built by Tia from one sentence", "Booking inside your forms", "Email reminders before every call", "Spam blocking"]},
    {"id": "starter", "name": "Starter", "for": "For small teams that book calls", "m": 15, "y": 12,
     "btn": ("Start free", "https://app.tryclaritia.com", "ghost"), "plus": "Free",
     "top": ["Unlimited forms", "2,000 form answers a month", "3 calendars per user", "500 AI credits a month", "Unlimited meeting types", "Payments and deposits with Stripe", "Signatures", "Paid meetings", "Group meetings and polls", "HubSpot, Google Sheets, Slack and more", "Reminder emails in your own words"]},
    {"id": "pro", "name": "Pro", "for": "For teams that share leads", "m": 39, "y": 31, "pick": True,
     "btn": ("Start free", "https://app.tryclaritia.com", "primary"), "plus": "Starter",
     "top": ["5,000 form answers a month", "10 calendars per user", "2,000 AI credits a month", "Routing by answer", "Round robin across your team", "Meetings with everyone free", "Follow-ups after every call and no-show", "No Claritia badge", "Emails from your own domain", "A brief from Tia before each call"]},
    {"id": "business", "name": "Business", "for": "For busy teams with lots of leads", "m": 79, "y": 63,
     "btn": ("Start free", "https://app.tryclaritia.com", "ghost"), "plus": "Pro",
     "top": ["Unlimited form answers", "Unlimited calendars per user", "5,000 AI credits a month", "Owner first from your CRM", "Double round robin", "Salesforce", "Your own domain for forms and booking pages", "Partial answers from people who didn't finish", "Priority chat help"]},
]

Y, N = True, False
SOON = "soon"

# Every feature, by group. A row is (label, [free, starter, pro, business]) with True, False or a short value;
# add SOON as a third item for a feature that isn't built yet.
GROUPS = [
    ("Plan", [
        ("Price per user a month", ["$0", ("$15", "$12"), ("$39", "$31"), ("$79", "$63")]),
        ("Users", ["1", "Unlimited", "Unlimited", "Unlimited"]),
        ("Editors", ["Unlimited"] * 4),
        ("Form answers a month", ["250", "2,000", "5,000", "Unlimited"]),
        ("Extra form answers", ["–", "$5 per 1,000", "$5 per 1,000", "–"]),
        ("AI credits a month", ["100", "500", "2,000", "5,000"]),
    ]),
    ("Forms", [
        ("Unlimited forms and questions", [Y, Y, Y, Y]),
        ("Multi-page forms with a progress bar", [Y, Y, Y, Y]),
        ("15 field types", [Y, Y, Y, Y]),
        ("File uploads", [Y, Y, Y, Y]),
        ("Show-if logic and step skips", [Y, Y, Y, Y]),
        ("Answer piping", [Y, Y, Y, Y]),
        ("Calculations and prices", [Y, Y, Y, Y]),
        ("Hidden fields (UTM tags, page, referrer)", [Y, Y, Y, Y]),
        ("Pre-fill from the link", [Y, Y, Y, Y]),
        ("Checks on every field", [Y, Y, Y, Y]),
        ("Thank-you screen", [Y, Y, Y, Y]),
        ("18 form styles", [Y, Y, Y, Y]),
        ("435 form templates", [Y, Y, Y, Y]),
        ("Works on phones and by keyboard", [Y, Y, Y, Y]),
        ("Signatures", [N, Y, Y, Y]),
        ("Payments with Stripe", [N, Y, Y, Y]),
        ("Custom endings by answer", [N, Y, Y, Y]),
        ("Redirect on completion", [N, Y, Y, Y]),
        ("Your logo, colors and fonts", [N, Y, Y, Y]),
        ("Copy of the answers to the person", [N, Y, Y, Y]),
        ("Full style control", [N, N, Y, Y]),
        ("Your site's look copied in", [N, N, Y, Y]),
        ("Emails from your own domain", [N, N, Y, Y]),
        ("Form languages", [N, N, Y, Y], SOON),
        ("Block duplicate answers", [N, N, Y, Y], SOON),
        ("Partial answers", [N, N, N, Y]),
        ("Drop-off by question", [N, N, N, Y]),
        ("A/B tests", [N, N, N, Y], SOON),
        ("Ad pixels", [N, N, N, Y], SOON),
        ("Your own domain for forms and booking pages", [N, N, N, Y]),
    ]),
    ("Sharing", [
        ("Share link", [Y, Y, Y, Y]),
        ("Embed with one script tag", [Y, Y, Y, Y]),
        ("Popup embed", [Y, Y, Y, Y]),
        ("QR code", [Y, Y, Y, Y]),
        ("Claritia badge", ["Full", "Small", "None", "None"]),
    ]),
    ("Spam and consent", [
        ("Cloudflare Turnstile", [Y, Y, Y, Y]),
        ("Honeypot and rate limit", [Y, Y, Y, Y]),
        ("Disposable email blocking", [Y, Y, Y, Y]),
        ("Consent wording by region", [Y, Y, Y, Y]),
    ]),
    ("Meetings", [
        ("Calendars per user", ["1", "3", "10", "Unlimited"]),
        ("Meeting types", ["1", "Unlimited", "Unlimited", "Unlimited"]),
        ("Google Calendar and Outlook", [Y, Y, Y, Y]),
        ("Google Meet, Teams and Zoom links", [Y, Y, Y, Y]),
        ("Booking inside the form", [Y, Y, Y, Y]),
        ("Working hours, buffers, notice and daily caps", [Y, Y, Y, Y]),
        ("The visitor's time zone and language", [Y, Y, Y, Y]),
        ("Reschedule and cancel links", [Y, Y, Y, Y]),
        ("Booking pages for each person and the team", [N, Y, Y, Y]),
        ("Group meetings with a guest limit", [N, Y, Y, Y]),
        ("One-off meetings and single-use links", [N, Y, Y, Y]),
        ("Secret meeting types", [N, Y, Y, Y]),
        ("Meeting polls", [N, Y, Y, Y]),
        ("Paid meetings with Stripe", [N, Y, Y, Y]),
        ("Questions on the booking page", [N, Y, Y, Y]),
        ("Copy open times into an email", [N, Y, Y, Y]),
        ("Round robin with weights and priority", [N, N, Y, Y]),
        ("Meetings with everyone free", [N, N, Y, Y]),
        ("Team pools", [N, N, Y, Y]),
        ("Daily and weekly limits for each person", [N, N, Y, Y]),
        ("Away days", [N, N, Y, Y]),
        ("Owner first (the person's owner in your CRM)", [N, N, N, Y]),
        ("Double round robin (one from each of two teams)", [N, N, N, Y]),
    ]),
    ("Routing", [
        ("Route by any answer to a meeting and a person", [N, N, Y, Y]),
        ("Route by past answers", [N, N, Y, Y]),
        ("A log of why each lead went where", [N, N, Y, Y]),
    ]),
    ("Workflows", [
        ("Confirmation email with a calendar invite", [Y, Y, Y, Y]),
        ("Email reminders a day and an hour before", [Y, Y, Y, Y]),
        ("Emails when a meeting moves or is canceled", [Y, Y, Y, Y]),
        ("Your own wording and times", [N, Y, Y, Y]),
        ("Follow-up the next day until they book", [N, Y, Y, Y]),
        ("Thank-you after a held meeting", [N, N, Y, Y]),
        ("No-show follow-up with the reschedule link", [N, N, Y, Y]),
        ("SMS reminders", [N, N, "100 a month", "300 a month"], SOON),
    ]),
    ("Tia, the AI", [
        ("Write a form from one sentence", [Y, Y, Y, Y]),
        ("Add and fix questions", [Y, Y, Y, Y]),
        ("Write a meeting's text", [Y, Y, Y, Y]),
        ("A brief before each call", [N, N, Y, Y]),
    ]),
    ("Integrations", [
        ("Webhooks", [Y, Y, Y, Y]),
        ("CSV export", [Y, Y, Y, Y]),
        ("HubSpot", [N, Y, Y, Y]),
        ("Omniscient", [N, Y, Y, Y]),
        ("Slack", [N, Y, Y, Y]),
        ("Google Sheets, Airtable and Notion", [N, Y, Y, Y]),
        ("Mailchimp, Klaviyo, ActiveCampaign, Brevo, Kit and MailerLite", [N, Y, Y, Y]),
        ("Answers and bookings from Typeform, Tally, Webflow, Calendly and Cal.com", [N, Y, Y, Y]),
        ("Salesforce", [N, N, N, Y]),
    ]),
    ("Results", [
        ("Every answer and booking saved", [Y, Y, Y, Y]),
        ("Repeat people merged by email", [Y, Y, Y, Y]),
        ("Views, starts and answers for each form", [Y, Y, Y, Y]),
    ]),
    ("Help", [
        ("Help center", [Y, Y, Y, Y]),
        ("Email help", [Y, "Within 1 business day", "Priority", "Priority"]),
        ("Chat help", [N, N, N, Y]),
    ]),
]

FAQ = [
    ("Who counts as a user?", "A user is a teammate people can book a meeting with. Teammates who only build forms, edit workflows or read results are free, so you only pay for the people who take calls."),
    ("What happens after 250 form answers on Free?", "Your forms keep working and every answer is saved. Answers past 250 show once you upgrade, or on the 1st of the next month. No lead is lost."),
    ("What is an AI credit?", "One thing Tia does for you, like writing a form or adding questions. A small change is 1 credit and a whole new form is 10. When credits run out, Tia waits for the next month. Your forms, meetings and reminders keep running."),
    ("What if a paid plan passes its form answers?", "Every answer is saved and shows right away. Extra answers are $5 per 1,000 on Starter and Pro. Business has no limit."),
    ("How does yearly billing work?", "Pay for the year up front and save 20%. Monthly plans renew each month."),
    ("Can I change or cancel my plan?", "Yes, any time from Settings. An upgrade starts right away. A cancel takes effect at the end of the period you paid for."),
    ("What does Soon mean?", "The feature is being built. It joins your plan when it ships, at no extra cost."),
    ("Do I need a card for Free?", "No. Sign in with Google and start building."),
]

STYLE = """<style>
.pr-hero{padding:120px var(--frame-pad) 40px;text-align:center}
.pr-hero .display{margin:24px auto 0;max-width:820px}
.pr-hero .sub{margin:20px auto 0}
.pr-tools{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px 20px;margin-top:32px}
.hosts{display:inline-flex;align-items:center;gap:10px;padding:4px 4px 4px 16px;border:1px solid var(--rail);border-radius:var(--r-pill);background:var(--surface);box-shadow:var(--sh-chip);font-size:14px;font-weight:500;color:var(--body)}
.hosts button{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:var(--r-pill);font-size:18px;color:var(--ink);transition:background-color var(--fast) var(--ease)}
.hosts button:hover{background:var(--hover)}
.hosts button:disabled{color:var(--line-strong);background:none}
.hosts output{min-width:28px;text-align:center;font-size:15px;color:var(--ink);font-variant-numeric:tabular-nums}
#pricing .plans{margin-top:40px}
.pr-sec{padding:96px var(--frame-pad) 40px}
.pr-sec .shead{margin-bottom:40px}
.ftable{border-radius:var(--r-lg);background:var(--surface);box-shadow:var(--sh-rest)}
.ftable table{width:100%;border-collapse:separate;border-spacing:0;font-size:14px}
.ftable thead th{position:sticky;top:76px;z-index:2;background:var(--surface);height:64px;padding:12px 16px;border-bottom:1px solid var(--line);text-align:left;vertical-align:bottom;font-weight:500;color:var(--ink)}
.ftable thead th:first-child{border-top-left-radius:var(--r-lg)}
.ftable thead th:last-child{border-top-right-radius:var(--r-lg)}
.ftable thead small{display:block;font-size:13px;font-weight:400;color:var(--meta)}
.ftable th[scope=row],.ftable td{padding:11px 16px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;line-height:20px}
.ftable th[scope=row]{width:34%;font-weight:400;color:var(--text)}
.ftable td{width:16.5%;color:var(--text)}
.ftable .grp th{padding:28px 16px 10px;border-bottom:1px solid var(--line);font-size:13px;font-weight:500;color:var(--meta);text-align:left}
.ftable tbody tr:last-child>*{border-bottom:0}
.ftable td svg{width:16px;height:16px;color:var(--green);vertical-align:-3px}
.ftable .no{color:var(--line-strong)}
.ftable .pick{background:var(--surface);box-shadow:inset 0 0 0 999px rgba(12,140,94,.035)}
.ftable .tag{height:20px;margin-left:6px;padding:0 6px;font-size:12px;line-height:20px;vertical-align:1px}
#pricing .faq{grid-template-columns:minmax(0,1fr)}
@media (min-width:900px){#pricing .faq{grid-template-columns:minmax(0,1fr) minmax(0,1.6fr)}}
@media (max-width:1100px){#pricing .plans{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){
.pr-hero{padding-top:96px}
.ftable{overflow-x:auto}
.ftable table{min-width:680px}
.ftable thead th{position:static}
.ftable th[scope=row]{position:sticky;left:0;z-index:1;width:auto;min-width:150px;background:var(--surface);box-shadow:1px 0 0 var(--line)}
.ftable .grp th{position:sticky;left:0;background:var(--surface)}
#pricing .plans{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:560px){.pr-hero .display{font-size:40px;line-height:42px}}
</style>
"""

SCRIPT = """<script>
(function () {
  var root = document.getElementById("pricing");
  var box = document.querySelector("[data-hosts]");
  if (!root || !box) return;
  var out = box.querySelector("output"), less = box.querySelector("[data-less]"), more = box.querySelector("[data-more]");
  var n = 1, MAX = 200;
  function money(v) { return "$" + v.toLocaleString("en-US"); }
  function draw() {
    out.textContent = n;
    less.disabled = n <= 1;
    more.disabled = n >= MAX;
    var yearly = root.classList.contains("is-yearly");
    root.querySelectorAll("[data-plan]").forEach(function (p) {
      var t = p.querySelector(".plan__total");
      var base = +p.getAttribute(yearly ? "data-y" : "data-m"), extra = p.getAttribute(yearly ? "data-hy" : "data-hm");
      if (!t) return;
      if (n === 1 || extra === "") { t.classList.toggle("on", n > 1 && extra === ""); t.textContent = n > 1 ? "1 user only" : ""; return; }
      t.classList.add("on");
      t.textContent = money(n * base) + " a month for " + n + " users";
    });
  }
  less.addEventListener("click", function () { if (n > 1) { n--; draw(); } });
  more.addEventListener("click", function () { if (n < MAX) { n++; draw(); } });
  document.querySelectorAll("[data-bill-to]").forEach(function (b) { b.addEventListener("click", function () { setTimeout(draw, 0); }); });
  draw();
})();
</script>
"""

CHECK = '<svg aria-hidden="true"><use href="#i-check"/></svg>'


def price(m, y):
    if m == y:
        return f"${m}"
    return f'<span data-monthly>${m}</span><span data-yearly>${y}</span>'


def cell(v, pick):
    cls = ' class="pick"' if pick else ""
    if v is True:
        return f'<td{cls}>{CHECK}<span class="sr-only">Included</span></td>'
    if v is False or v == "–":
        return f'<td{cls}><span class="no" aria-hidden="true">–</span><span class="sr-only">Not included</span></td>'
    if isinstance(v, tuple):
        return f'<td{cls}><span data-monthly>{v[0]}</span><span data-yearly>{v[1]}</span></td>'
    return f"<td{cls}>{esc(v)}</td>"


def card(p):
    pick = p.get("pick")
    label, href, kind = p["btn"]
    per = "per user a month" if p["m"] else "a month"
    host = '<p class="plan__host">For each teammate who takes calls</p>' if p["m"] else '<p class="plan__host">1 user. No card needed.</p>'
    heading = f'<h3>Everything in {p["plus"]}, plus</h3>' if p.get("plus") else "<h3>All the basics</h3>"
    items = "".join(f"<li>{CHECK}{esc(t)}</li>" for t in p["top"])
    tag = '<span class="tag tag--green">Most picked</span>' if pick else ""
    return f"""<div class="plan{' plan--pick' if pick else ''}" data-plan="{p['id']}" data-m="{p['m']}" data-y="{p['y']}" data-hm="{p['m'] or ''}" data-hy="{p['y'] or ''}">
          <div class="plan__top"><b>{p['name']}</b>{tag}</div>
          <p class="plan__price"><b>{price(p['m'], p['y'])}</b><small>{per}</small></p>
          <p class="plan__for">{esc(p['for'])}</p>
          {host}
          <p class="plan__total" aria-live="polite"></p>
          <a class="btn btn--{kind}" href="{href}">{label}</a>
          {heading}
          <ul>{items}</ul>
          <a class="plan__all" href="#features">See every feature</a>
        </div>"""


def table():
    head = "".join(
        f'<th scope="col"{" class=\"pick\"" if p.get("pick") else ""}>{p["name"]}<small>{price(p["m"], p["y"])} a month</small></th>'
        for p in PLANS)
    rows = []
    for name, items in GROUPS:
        rows.append(f'<tr class="grp"><th colspan="5" scope="colgroup">{esc(name)}</th></tr>')
        for it in items:
            label, vals = it[0], it[1]
            soon = ' <span class="tag">Soon</span>' if len(it) > 2 else ""
            rows.append(f'<tr><th scope="row">{esc(label)}{soon}</th>' + "".join(cell(v, PLANS[i].get("pick")) for i, v in enumerate(vals)) + "</tr>")
    return f"""<div class="ftable"><table>
<caption class="sr-only">Every feature in each Claritia plan</caption>
<thead><tr><th scope="col"><span class="sr-only">Feature</span></th>{head}</tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table></div>"""


def faq():
    plus = '<svg aria-hidden="true"><use href="#i-plus"/></svg>'
    return "".join(f"<details><summary>{esc(q)} {plus}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)


def cta():
    return shell.absolute(shell.block("<!-- The last prompt, on dark -->", "</section>\n    </div>\n  </div>"))


def page():
    cards = "\n        ".join(card(p) for p in PLANS)
    main = f"""<div id="pricing">
  <div class="frame">
    <section class="pr-hero" aria-labelledby="price-h">
      <span class="eyebrow"><svg class="i s12" aria-hidden="true"><use href="#card"/></svg>Pricing</span>
      <h1 class="display" id="price-h">Start free. Pay per user as you grow.</h1>
      <p class="sub">Pay for each teammate who takes calls. Teammates who only build forms or read answers are always free.</p>
      <div class="pr-tools">
        <div class="bill js-only" data-bill role="group" aria-label="Billing period">
          <button type="button" data-bill-to="monthly" aria-pressed="true">Monthly</button>
          <button type="button" data-bill-to="yearly" aria-pressed="false">Yearly <em>Save 20%</em></button>
        </div>
        <div class="hosts js-only" data-hosts role="group" aria-label="Number of users">
          Users
          <button type="button" data-less aria-label="One less user">&minus;</button>
          <output aria-live="polite">1</output>
          <button type="button" data-more aria-label="One more user">+</button>
        </div>
      </div>
      <div class="plans">
        {cards}
      </div>
    </section>
  </div>
  <div class="band"><div class="frame"></div></div>

  <div class="frame">
    <section class="pr-sec" id="features" aria-labelledby="feat-h">
      <div class="shead">
        <span class="eyebrow"><svg class="i s12" aria-hidden="true"><use href="#i-check"/></svg>Every feature</span>
        <h2 class="h2" id="feat-h">Compare every plan</h2>
        <p class="sub">Every plan has unlimited forms and unlimited editors.</p>
      </div>
      {table()}
    </section>
  </div>
  <div class="band"><div class="frame"></div></div>

  <div class="frame">
    <section class="pr-sec" id="faq" aria-labelledby="faq-h">
      <div class="faq">
        <div class="faq__head">
          <h2 class="h2" id="faq-h">Questions</h2>
          <p class="lead">Something else? <a href="mailto:hello@tryclaritia.com">hello@tryclaritia.com</a></p>
        </div>
        <div class="qa">{faq()}</div>
      </div>
    </section>
  </div>
</div>

{cta()}"""
    title = "Pricing · Claritia"
    desc = "Free for one person. Starter $15, Pro $39 and Business $79 per user a month. Teammates who only build forms are free. Unlimited forms on every plan."
    return shell.head(title, desc, "/pricing", STYLE) + "\n" + shell.body(main, SCRIPT)


def home_cards():
    """The home page's plan cards are the same cards, so the two never drift apart."""
    home = ROOT / "index.html"
    text = home.read_text()
    i = text.index('<div class="plans">')
    j = text.index('<p class="onlink">', i)
    cards = "\n        ".join(card(p).replace('href="#features"', 'href="/pricing#features"') for p in PLANS)
    home.write_text(text[:i] + f'<div class="plans">\n        {cards}\n      </div>\n      ' + text[j:])


if __name__ == "__main__":
    home_cards()
    out = ROOT / "pricing" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page())
    print("wrote", out.relative_to(ROOT))
