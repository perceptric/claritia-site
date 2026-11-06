# Brief: "Best …" articles for the Claritia blog

Bottom-of-funnel comparison posts. A reader is choosing a tool this week. Each post ranks Claritia first and then gives
an honest, useful look at the real alternatives, so the reader trusts it even if they pick something else.

## Where the file goes

`blog/drafts/<slug>.md`, starting with these lines exactly (no other keys):

```
---
title: <the post's title, 60 to 70 characters, with the main search words near the front, plus "(2026)" at the end>
description: <one or two sentences, 140 to 160 characters, for search results>
category: <Scheduling | Forms | Routing | Workflows | Integrations>
kind: <cover scene: meeting | form | responses | workflow | integration>
date: <the date given in your task>
---
```

For an integration-kind post also add `logo: /assets/logos/<file>` and `name: <tool>` (only when told to).

Markdown the blog supports: `##` and `###` headings, paragraphs, `-` and `1.` lists, `**bold**`, `*italic*`,
`[links](/path)`, `> quotes`, and pipe tables (`| a | b |`, then `|---|---|`, then rows). Nothing else (no HTML, no
images, no footnotes, no nested lists).

## Shape of each post (1,600 to 2,300 words)

1. A short opening (2 short paragraphs): who the post is for and what to look for. No "In today's fast-paced world".
2. `## How we picked`: 4 to 6 plain criteria as a list.
3. `## The quick comparison`: one pipe table, one row per tool: Tool, Best for, Free plan, Paid from (or "See their
   pricing page"), and one stand-out column that fits the topic.
4. `## 1. Claritia` then `## 2. <Tool>` … for 7 to 10 tools in all. Each tool section has: a 2 to 3 sentence summary,
   `**Best for:**` one line, `**What stands out:**` a short list, `**Where it falls short:**` a short list (Claritia
   gets one too, honest), `**Pricing:**` one line.
5. `## How to choose` with 3 to 5 short scenarios ("If you … pick …").
6. `## Questions` with 4 to 6 `###` questions and short answers (good for search snippets).
7. A last short paragraph with a link to start: `[Start free](https://app.tryclaritia.com/signup)` and one or two
   relevant site links.

## Writing rules (strict)

- Plain words, 9th grade reading level. Short sentences. Active voice.
- Never write "not X, but Y", "not X, Y" or "X, not Y" constructions. Never use lists or phrases of exactly three
  items in a row for rhythm ("fast, simple and cheap"); two or four items are fine when they're real.
- Never use the word "quietly". No hype words: "game-changer", "seamless", "robust", "revolutionize", "unlock",
  "supercharge", "leverage", "elevate", "in today's". No emoji. No exclamation marks.
- Professional and fair about rivals. No negative words about people. Say what each tool does well.
- Second person ("you"). No first-person stories, no made-up customers, numbers, quotes, studies or survey results.

## Facts: Claritia (use only these; never add features)

Claritia is forms, meetings and workflows for small teams: forms that turn visitors into leads, meetings that book them
with the right person, and workflows that follow up. Tia is its AI form builder. Site: tryclaritia.com.

Prices per seat a month (monthly / billed yearly). A seat is a teammate people can book meetings with; teammates who
only build forms or read answers are free.
- Free $0: unlimited forms, 250 submissions a month, 1 calendar, 1 meeting type, 100 AI credits.
- Starter $15 / $12: 2,000 submissions a month, 6 calendars per seat, unlimited meeting types, 500 AI credits.
- Pro $39 / $31: 5,000 submissions a month, 2,000 AI credits, round robin, team pools, routing.
- Business $79 / $63: unlimited submissions, 5,000 AI credits, Salesforce, owner-first and double round robin,
  partial answers and drop-off by question, your own domain.

Features by plan (the pricing page's own words):
- Free: unlimited forms; multi-page forms and a progress bar; 15 field types; file uploads; conditional logic and step
  skips; calculations and formulas; hidden fields (UTM tags, page, referrer); pre-fill from the link; thank-you
  screen; 18 form styles; 435 form templates; Google Calendar and Outlook; Google Meet, Teams and Zoom links; meeting
  booking inside forms; working hours, buffers, notice and daily caps; the visitor's time zone and language;
  reschedule and cancel links; share by link, embed with one script tag, popup embed, QR code; confirmation email with
  a calendar invite; reminders a day and an hour before; Tia builds a form from a plain sentence; webhooks; CSV export;
  embeds on WordPress, Webflow, Framer, Shopify and Squarespace; Google Analytics, Google Tag Manager, Meta Pixel and
  Google Ads tags; Google Forms import; Cloudflare spam protection, honeypot and rate limit, disposable email blocking.
- Starter adds: e-signatures; Stripe payments; redirect on completion; custom brand; booking pages for each person and
  the team; group meetings; one-off meetings and single-use links; meeting polls; paid meetings with Stripe (PayPal and
  Square too); your own wording and times for emails; follow-up the next day until they book; connections to HubSpot,
  Pipedrive, Attio, Close, Zoho CRM, Dynamics 365, GoHighLevel, Freshsales, Copper, Keap, monday CRM, Slack, Microsoft
  Teams, Discord, Google Sheets, Airtable, Notion, Excel Online, PostgreSQL, MySQL, Mailchimp, Klaviyo, ActiveCampaign,
  Brevo, Kit, MailerLite, Linear, Trello, ClickUp, Zendesk, Freshdesk, Intercom, Google Docs, DocuSign, PandaDoc, Google
  Drive, OneDrive, Dropbox, Box, Amazon S3, Segment, PostHog, Mixpanel, Amplitude, Twilio (text and WhatsApp), Webex,
  Whereby; emails from your own Gmail or Outlook; answers and bookings from Typeform, Tally, Webflow, Calendly and
  Cal.com.
- Pro adds: round robin with weights and priority; meetings with everyone free; team pools; daily and weekly limits for
  each person; away days; remove Claritia branding; thank-you after a held meeting; no-show follow-up with the
  reschedule link; route by any answer to a meeting and a person; route by past answers; routing log.
- Business adds: partial answers; drop-off by question; your own domain for forms and booking pages; owner first (the
  person's owner in the CRM); double round robin; Salesforce.

Honest limits you may name: Claritia is a newer tool, so its app marketplace and community are smaller than the big
names; no native mobile app; Zapier and Make apps are on the way (not yet listed); SMS reminders on Pro and Business
are coming soon; it's built for small teams more than large enterprises.

Useful links: /products/forms, /products/meetings, /products/routing, /templates, /integrations,
/integrations/<tool> (e.g. /integrations/hubspot, /integrations/google-calendar), /pricing.

## Facts: other tools

Check every rival's price and plan facts on the vendor's own pricing page (use web search and fetch) before you write
them. If you can't confirm a price there, write "See their pricing page" instead of a number. Never guess. Known
notes to verify, from November 2026 research:
- Typeform: Basic $28, Plus $56, Business $91 a month billed yearly; response caps by plan; low free cap.
- Fillout: free plan with 1,000 responses; Starter $15, Pro $40, Business $75 a month.
- Jotform: free 5 forms and 100 submissions; Bronze $34, Silver $39, Gold $99 a month billed yearly; one user.
- Calendly: free has 1 event type; Standard $10 to $12; Teams $16 a seat yearly, $20 monthly.
- Cal.com: free for 1 user with unlimited event types; Teams $12 a user yearly.
- Chili Piper: Growth from $15,000 a year with 15 seats.
- Default: Growth from $12,000 a year.
- RevenueHero: Essentials $79 plus $25 a seat yearly.
- OnceHub, HubSpot, Google Forms, Microsoft Forms, Tally, Paperform, Zoho Forms, WPForms, Gravity Forms, Acuity,
  SavvyCal, Zcal, TidyCal, Microsoft Bookings, YouCanBookMe, LeanData, Distribution Engine: verify everything.

When done, report each file's slug, word count, and any rival facts you couldn't confirm.
