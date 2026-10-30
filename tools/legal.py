"""Builds /privacy/index.html and /terms/index.html from the text below. Run: python3 tools/legal.py"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
UPDATED = "October 30, 2026"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Claritia</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://tryclaritia.com/{slug}">
<link rel="icon" href="/assets/brand/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/brand/claritia-mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<meta name="theme-color" content="#ffffff">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&amp;family=Inter:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="/assets/site.css?v=7">
<style>
.legal{{width:100%;max-width:720px;margin-inline:auto;padding:96px 16px 112px;color:var(--ink-2);line-height:1.65}}
.legal h1{{color:var(--ink);margin:8px 0 6px}}
.legal .upd{{color:var(--muted);font-size:14px;margin:0 0 32px}}
.legal h2{{color:var(--ink);font-size:20px;font-weight:600;letter-spacing:-.01em;margin:40px 0 10px}}
.legal p,.legal li{{font-size:16px}}
.legal ul{{padding-left:20px;display:flex;flex-direction:column;gap:6px}}
.legal a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--light)}}
.legal table{{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0}}
.legal th,.legal td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
.legal th{{color:var(--muted);font-weight:500}}
.legal .tbl{{overflow-x:auto}}
.legal .note{{border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:var(--tint)}}
</style>
</head>
<body>
<header class="site-header">
  <div class="wrap site-header__in">
    <a class="logo" href="/" aria-label="Claritia home"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="6" fill="#0C8C5E"/><path d="M7 12V7h5M20 7h5v5M25 20v5h-5M12 25H7v-5" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M11.5 16.5l3 3 6-7" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>Claritia</a>
    <div class="site-actions">
      <a class="site-actions__signin" href="https://app.tryclaritia.com">Sign in</a>
      <a class="btn btn--primary" href="https://app.tryclaritia.com">Start free <span aria-hidden="true">&rarr;</span></a>
    </div>
  </div>
</header>
<main class="legal">
<p class="eyebrow">Legal</p>
<h1 class="h2">{title}</h1>
<p class="upd">Last updated: {updated}</p>
{body}
</main>
<footer class="site-footer">
  <div class="site-footer__base">
    <div class="wrap site-footer__base-in">
      <span>&copy; 2026 Perceptric. Claritia is a Perceptric product.</span>
      <span><a href="/privacy">Privacy</a> &nbsp; <a href="/terms">Terms</a> &nbsp; <a href="mailto:hello@tryclaritia.com">hello@tryclaritia.com</a></span>
    </div>
  </div>
</footer>
</body>
</html>
"""

def md(text: str) -> str:
    """A tiny Markdown: ## headings, - lists, | tables |, > notes, **bold**, [links](url), paragraphs."""
    out, lines, i = [], text.strip().split("\n"), 0
    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        if l.startswith("## "): out.append(f"<h2>{inline(l[3:])}</h2>"); i += 1; continue
        if l.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "): items.append(f"<li>{inline(lines[i][2:])}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"): rows.append([c.strip() for c in lines[i].strip("|").split("|")]); i += 1
            head, body = rows[0], [r for r in rows[2:]]
            out.append('<div class="tbl"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>"); continue
        if l.startswith("> "): out.append(f'<p class="note">{inline(l[2:])}</p>'); i += 1; continue
        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("## ", "- ", "|", "> ")): para.append(lines[i]); i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)

PRIVACY = """
This policy explains what personal data Claritia collects, why, and what you can do about it. Claritia is a product of Perceptric ("Claritia", "we", "us"). Questions go to [hello@tryclaritia.com](mailto:hello@tryclaritia.com).

## Who this covers

- **Customers and their team members** who use the Claritia app at app.tryclaritia.com.
- **Visitors** to tryclaritia.com.
- **Leads and visitors of our customers**: people who fill in a customer's Claritia form, book a meeting through a Claritia booking page, or visit a customer's website where the customer installed the Claritia script. For that data, our customer is the controller and we are the processor.

## What we collect

**Account data.** Your name, email address and profile picture when you sign in with Google, and your workspace and team settings.

**Workspace content.** What you and your team add to Claritia: forms, routing rules, meeting types, contacts, companies, opportunities, notes, tasks, email templates and journeys, and the answers people send through your forms.

**Connected calendars.** When a team member connects Google Calendar or Microsoft Outlook, we use it only for meeting scheduling. See "Google user data" below.

**Other connected tools.** If you connect a CRM (such as HubSpot or Salesforce), Slack, Zoom or Stripe, we store an encrypted access token and use it only for the features you turn on, such as syncing contacts or posting alerts.

**Lead and visitor data.** Answers to a customer's form, booking details (name, email, time zone, answers to booking questions), and, where a customer installs the Claritia script, page views, referrers, device type, approximate location and the company behind a visit.

**Billing data.** Your plan and invoices. Card details go straight to Stripe. We never see or store your full card number.

**Usage data.** Pages you open in the app, actions you take, errors, browser type and IP address, used to run, secure and improve the service.

## Google user data

When a team member connects Google Calendar, Claritia asks for these permissions:

- **See your calendars and free/busy times (calendar.readonly).** Claritia reads free and busy times on the calendars you connect, so booking pages and forms only offer times when you are free. It lists your calendars so you can pick which ones count as busy, and watches them for changes so your availability stays current.
- **Edit events (calendar.events).** When someone books a meeting with you, Claritia adds that meeting, with its video link, to the calendar you chose. It updates the event if the meeting is moved and removes it if the meeting is cancelled. Claritia only changes events it created.
- **See your email address (userinfo.email).** Shows which Google account you connected.

We use Google user data only to provide meeting scheduling to you. We do not sell it, do not use it for advertising, do not use it to build user profiles for other purposes, and do not use it to train AI or machine learning models. People at Claritia do not read your calendar data, except with your permission, when needed for security, or to comply with the law.

> Claritia's use and transfer of information received from Google APIs will adhere to the [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), including the Limited Use requirements.

You can disconnect your calendar at any time in Claritia, or remove Claritia's access at [myaccount.google.com/permissions](https://myaccount.google.com/permissions). When you do, Claritia stops reading your calendar, your free times leave booking pages, and we delete the stored access token.

## Why we use data

| Purpose | Legal basis (GDPR) |
| --- | --- |
| Run your account and the features you use | Contract |
| Route leads, schedule meetings and send booking emails | Contract |
| Charge for your plan and send invoices | Contract, legal obligation |
| Keep the service safe and fix errors | Legitimate interest |
| Send service emails (sign-in, alerts you turn on, receipts) | Contract |
| Send product news, if you opt in | Consent |

We do not sell personal data.

## AI features

Some features, such as writing emails, building forms and qualifying leads, send the relevant workspace content to Anthropic, our AI provider, under its API terms, which do not allow it to train on that data. Calendar data from Google is never sent to AI providers.

## Who we share data with

We use these service providers (sub-processors) to run Claritia:

| Provider | What they do | Location |
| --- | --- | --- |
| Supabase | Database and sign-in | Japan |
| Fly.io | App hosting | Japan |
| Google | Sign-in, Google Calendar and Meet | United States |
| Microsoft | Outlook calendar, when you connect it | United States |
| Zoom | Video links, when you connect it | United States |
| Resend | Sending emails | United States |
| Stripe | Payments | United States |
| Anthropic | AI features | United States |
| Coresignal and IPinfo | Company enrichment and IP to company lookups | European Union, United States |
| Cloudflare | Spam protection on forms | United States |

We also share data with tools you connect yourself (such as your CRM or Slack), and when the law requires it.

## International transfers

Some providers are outside your country. When personal data leaves the EU, UK or Switzerland, we rely on the EU Standard Contractual Clauses (and the UK addendum) or another approved transfer tool.

## How long we keep data

- Account and workspace data: while your account is open. When you delete your account or workspace, we delete its data within 30 days, and backups roll off within a further 30 days.
- Calendar data: Claritia keeps only the start and end of busy times (no event titles, guests or places), the names of the calendars you connect, and an encrypted access token. All of it is deleted when you disconnect the calendar.
- Form answers and leads: as long as your workspace keeps them. You can set a shorter retention period for each form.
- Billing records: as long as tax law requires.
- Error and security logs: up to 90 days.

## Your rights

Depending on where you live, you can ask to see, correct, delete or export your data, object to some uses, or withdraw consent. Email [hello@tryclaritia.com](mailto:hello@tryclaritia.com) and we answer within 30 days. If you are a lead of one of our customers, contact that customer first; we will help them answer. You can also complain to your local data protection authority.

## Cookies

The Claritia app uses your browser's storage to keep you signed in and remember your choices. We do not use advertising cookies.

## Security

Data is encrypted in transit (HTTPS) and at rest. Access tokens for connected tools are encrypted again on top of that. Access inside the company is limited to people who need it.

## Children

Claritia is for businesses. It is not meant for anyone under 16.

## Changes

If we make important changes, we will tell you by email or in the app before they apply.

## Contact

Perceptric, the company behind Claritia. Email: [hello@tryclaritia.com](mailto:hello@tryclaritia.com).
"""

TERMS = """
These terms are an agreement between you and Perceptric, the company behind Claritia ("Claritia", "we", "us"). By creating an account or using Claritia, you agree to them. If you use Claritia for a company, you agree for that company.

## The service

Claritia is an inbound marketing and sales platform: forms, lead routing, meeting scheduling, a CRM, email journeys and the tools around them, at app.tryclaritia.com.

## Your account

- Keep your sign-in safe. You are responsible for what happens in your account.
- You must be at least 16 and able to enter a contract.
- Give us accurate details and keep them up to date.

## Your data

- You own the content you and your team put in Claritia, including your contacts and the answers people send through your forms.
- You give us permission to store and process it only to run Claritia for you, as described in our [Privacy Policy](/privacy).
- For personal data about your leads and website visitors, you are the controller and we are the processor. You are responsible for having the right to collect it and for telling people how you use it.
- When you connect a calendar or another tool, you authorize Claritia to use it for the features you turn on. You can disconnect at any time.

## Acceptable use

Don't use Claritia to:

- send spam or messages people did not agree to receive;
- break the law or anyone's rights, including privacy and anti-spam laws;
- upload malware or try to break into the service or other accounts;
- resell or copy the service without our written permission.

We may suspend accounts that break these rules, and we will tell you why when we can.

## Plans and payment

- Paid plans are billed in advance through Stripe and renew until you cancel.
- You can cancel at any time; your plan stays active until the end of the paid period.
- Prices can change. We will tell you at least 30 days before a change applies to you.

## Third-party services

Claritia works with services such as Google, Microsoft, Zoom, Stripe, HubSpot, Salesforce and Slack. Their own terms apply to your use of them, and we are not responsible for them.

## Availability and changes

We work to keep Claritia running and your data safe, but the service is provided "as is", without warranties of any kind. We may change or remove features; if we remove something important to a paid plan, we will tell you first.

## Liability

To the extent the law allows, we are not liable for indirect or lost-profit damages, and our total liability for any claim is limited to what you paid us in the 12 months before the claim.

## Ending

You can delete your account at any time. We can end these terms if you break them, with notice when we can. When an account is deleted, we delete its data as described in the Privacy Policy.

## Changes to these terms

If we make important changes, we will tell you by email or in the app before they apply. Using Claritia after that means you accept the new terms.

## Contact

Email [hello@tryclaritia.com](mailto:hello@tryclaritia.com).
"""

for slug, title, desc, text in [("privacy", "Privacy Policy", "How Claritia collects, uses and protects personal data, including Google user data.", PRIVACY), ("terms", "Terms of Service", "The terms for using Claritia.", TERMS)]:
    (ROOT / slug / "index.html").write_text(HEAD.format(title=title, desc=desc, slug=slug, updated=UPDATED, body=md(text)))
    print("wrote", slug)
