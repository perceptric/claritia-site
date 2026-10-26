# Claritia homepage copy

Every word for `index.html`, in page order. Written from the app's main branch on 25 Oct 2026: the four sections
(CRM, Automation, Inbound, Nurture) in `docs/unify-plan.md`, the inbound stack in `docs/inbound.md`, the router in
`docs/router.md`, meetings in `docs/meetings-scheduler.md`, and the proposed plans in `docs/pricing.md`.

Look and modules follow `docs/brand.md` in the app repo (section 5, "Marketing site"). Headlines are two tones: the
first line in `ink`, the line after the break in gray.

## What changed from the live page

| Live page says | Product today |
|---|---|
| Journeys, Pages and Reports "in build" | Pages are gone. Workflows and Reports are built. |
| Sending on Amazon SES | All email runs on Resend. |
| No scheduling or routing story | Scheduling, instant booking in forms, the router and enrichment are built. |
| Starter $299, Growth $799, Scale $1,999 | Proposed: Free $0, Starter $79, Growth $299, Scale $799 |
| Sidebar: Audience, Engage, Prove | CRM, Automation, Inbound, Nurture |

---

## Page title and meta

- **Title:** Claritia: from website visit to booked meeting
- **Description:** Claritia is the CRM and inbound stack for small B2B teams. Forms, enrichment, routing, scheduling
  and AI email in one place, live in 15 minutes.
- **Share image text:** Turn visitors into booked meetings.

---

## 1. Header

- Nav: Product, Scheduling, Routing, Pricing, Docs
- Product menu, one line each:
  - **CRM:** Contacts, companies, opportunities and meetings in one place
  - **Automation:** Workflows, routing and enrichment
  - **Inbound:** Forms, scheduling and website visitors
  - **Nurture:** Emails, segments and lead scoring
- Right side: Sign in (ghost), Book a demo (secondary), Start free (black)

---

## 2. Hero

- **Badge:** New · Workflows and reports are live →
- **Headline:**
  > Turn website visitors
  > into booked meetings.
- **Lead:** Claritia catches every lead, finds out who they are, sends them to the right rep and books the meeting
  before they leave your site. One app for small B2B teams who find HubSpot too heavy.
- **Buttons:** Start free · Book a demo
- **Small line:** Free plan, no card needed.

Other headlines to test:
- "From form fill / to booked meeting in 20 seconds."
- "Every lead, / on the right calendar."

**Picture (visitor stream, module 2):** dots flow in from the left as visitors. A few get caught by a form, turn
into named avatars and drop into a calendar slot. Caption under it: `Acme visited pricing → Dana filled the demo
form → booked with Sam, Thursday 10:00`.

---

## 3. Logo strip

- **Line:** Connects in one click.
- **Logos:** Google Calendar, Outlook, Zoom, HubSpot, Salesforce, Slack, Pipedrive, Attio, Close, Webflow, Stripe,
  Omniscient

---

## 4. One lead, start to finish

- **Eyebrow:** How it works
- **Headline:**
  > Twenty seconds
  > from form to calendar.
- **Lead:** Here is what happens when someone asks for a demo. You set it up once. Claritia runs it for every lead.

| Time | Step | What happens |
|---|---|---|
| 0:00 | **Visit** | Dana from Acme opens your pricing page. Claritia knows the company from the visit. |
| 0:05 | **Fill** | Dana types a work email. Claritia already knows Acme's size and industry, so the form drops from 6 fields to 2. |
| 0:15 | **Qualify** | Your rules pass. AI reads the "what are you looking for" answer and marks Dana qualified, with its reason. |
| 0:16 | **Route** | Acme has no owner, so the router picks the US team and hands Dana to Sam, who has room this week. |
| 0:20 | **Book** | Sam's open times show inside the form. Dana picks Thursday at 10. The invite lands on both calendars and Slack tells Sam, with a short brief. |

- **Closing line:** Reminders go out the day before and the hour before. If Dana leaves without booking, Claritia
  emails Sam's times.

---

## 5. Inbound

- **Tag:** Inbound
- **Headline:**
  > Forms that book
  > the meeting for you.
- **Lead:** Build a form by chatting with AI, or keep the forms you have. Either way, the right rep's calendar opens
  the moment the form is sent.
- **Points (accordion, module 4):**
  1. **Built by chat.** Say what the form is for. AI builds it in your site's fonts and colors.
  2. **Keep your forms.** Works with HubSpot, Webflow, Marketo, Framer, Typeform and plain HTML forms.
  3. **Booking inside the form.** Open times show in under a second. No second page to load.
  4. **See who visits.** Claritia names the companies on your site and alerts you when a target account comes back.
- **Link:** See forms →

**Picture:** a form beside a calendar. The email field is filled, two fields fade out, and Thursday 10:00 lights up.

---

## 6. Scheduling

- **Tag:** Scheduling
- **Headline:**
  > Everything Calendly does,
  > joined to your leads.
- **Lead:** Reps connect Google or Outlook in one click and set their hours. Every booking lands on the lead's record,
  with the source that brought them.
- **Points:**
  1. **Every meeting type.** One rep, round robin, the whole team, the owner first, group events and polls.
  2. **Booking links.** Share a booking page or a one-off link. Reps can also book from Slack with `/book`.
  3. **Paid meetings.** Take payment with Stripe when someone books.
  4. **No-shows tracked.** Reminders go out before every meeting, and reps mark no-shows in one click.
- **Link:** See scheduling →

**Picture:** a booking page with a week of open times and a "Booked" tag on Thursday.

---

## 7. Routing

- **Tag:** Routing
- **Headline:**
  > Every lead to the right rep,
  > with the reason in plain words.
- **Lead:** Rules, territories, owners and round robin in one router. Each decision comes with a sentence that says
  why, so nobody has to guess.
- **Points:**
  1. **Owners first.** Known accounts go straight to their owner, in Claritia or your CRM.
  2. **Fair turns.** Round robin with caps, time off and the hours each rep works.
  3. **Speed to lead.** A rep who doesn't answer in time gets a nudge, then the lead moves on.
  4. **Try before it goes live.** Send a test lead through and watch which rule picks it up.
- **Link:** See routing →

**Picture:** the router log, one line:
> Rule 3, territory US mid-market. Round robin: Sam (2 of 8 this week).

---

## 8. Automation

- **Tag:** Automation
- **Headline:**
  > The busywork after every lead,
  > done for you.
- **Lead:** Fill in missing details, qualify the lead, route it and start the follow-up. Set it up once on one canvas.
- **Points:**
  1. **Enrichment.** Claritia checks your own records first, then data vendors in order. Every value shows where it
     came from and when.
  2. **AI qualify.** AI can only pick an outcome your team set up, and it always gives its reason.
  3. **Workflows.** From trigger to goal on one canvas, with templates to start from.
  4. **Your CRM stays in step.** Two-way sync with HubSpot, Salesforce and Omniscient.
- **Link:** See workflows →

**Picture:** a workflow line drawing itself: Form sent → Enrich → Qualify → Route → Book → Email.

---

## 9. Nurture

- **Tag:** Nurture
- **Headline:**
  > AI writes the follow-up.
  > You approve it.
- **Lead:** Emails written from your own content, sent from your own domain. Nothing goes out until someone on your
  team says yes.
- **Points:**
  1. **Written from your content.** Every line points to the page it came from.
  2. **Segments that stay fresh.** Lists built from fields, visits, activity and consent update by themselves.
  3. **Lead scoring.** Fit plus engagement tells you who to call first.
  4. **Safe sending.** Consent by region, one-click unsubscribe, frequency caps and quiet hours, checked on every send.
- **Link:** See nurture →

**Picture:** a draft email with the AI tag, an "Approve and send" button, and the source page linked under one line.

---

## 10. CRM

- **Tag:** CRM
- **Headline:**
  > One clean record
  > for every person.
- **Lead:** Contacts, companies, opportunities and meetings in one place. Use it as your CRM, or keep yours and let
  Claritia sync both ways.
- **Points:**
  1. **One record per person.** Visits, forms, emails and meetings on one timeline.
  2. **Bring everything in.** Import from 20 tools or any CSV file, with undo for 30 days.
  3. **Opportunities on a board.** Drag a deal from stage to stage.
  4. **Reports where you work.** Funnel, speed to lead, reps, forms and email, inside each section.
- **Link:** See the CRM →

**Picture (before and after, module 10):** drag a handle across a messy spreadsheet to show a clean Claritia list.

---

## 11. Try it

- **Eyebrow:** Try it
- **Headline:**
  > Fill in the form.
  > Watch Claritia work.
- **Lead:** This is a real Claritia form. Type a work email and see the record fill in, the score appear and a rep's
  times open up.
- **Form fields:** Work email, What are you looking for?
- **Button:** Show me
- **Result card labels:** Company, Size, Industry, Score, Routed to, Open times

---

## 12. Numbers

| Number | Caption |
|---|---|
| 15 min | to go live, from sign-up to your first booked meeting |
| Under 1 sec | for a rep's open times to show in the form |
| 2 fields | instead of 6, when Claritia already knows the company |
| $0 | for people who only edit. You pay for hosts. |

---

## 13. Replace the pile of tools

- **Eyebrow:** One app
- **Headline:**
  > One app in place
  > of five subscriptions.
- **Lead:** Small teams end up paying for a CRM, a form tool, a scheduler, a router and a data vendor. Claritia does
  the whole path.

| You use today | Claritia does it in |
|---|---|
| HubSpot or a spreadsheet | CRM |
| Typeform or HubSpot forms | Inbound › Forms |
| Calendly or Chili Piper | Inbound › Scheduling |
| Default or LeanData | Automation › Routing |
| Clearbit or Apollo | Automation › Enrichment |

---

## 14. The suite

- **Eyebrow:** The suite
- **Headline:**
  > From AI answer
  > to won deal.
- **Lead:** Claritia is the middle of one suite. Run all three and the whole path from an AI answer to a won deal sits
  in one place.
- **Cards:**
  - **Found by Arrowsterr.** SEO and AI search, so the right buyer finds you first.
  - **Converted by Claritia.** Forms, routing, scheduling and follow-up, so the visit turns into a meeting.
  - **Closed with Omniscient.** The CRM and deal rooms where the meeting turns into revenue.
- **Small line:** Run two or more and save 20%.

---

## 15. Pricing

- **Eyebrow:** Pricing
- **Headline:**
  > Pay for the people who take meetings.
  > Everyone else is free.
- **Lead:** Billed monthly. No platform fee and no onboarding fee. Pay yearly and get 2 months free.

| | Free | Starter | Growth (featured) | Scale |
|---|---|---|---|---|
| Price | $0 | $79 a month | $299 a month | $799 a month |
| Yearly | $0 | $66 a month | $249 a month | $666 a month |
| For | Trying it out | Small teams booking demos | Teams that route and qualify | Teams with volume |
| Hosts included | 1 | 3 | 10 | 25 |
| Extra host | — | $15 | $20 | $25 |
| Contacts | 500 | 2,500 | 10,000 | 50,000 |
| Emails a month | 500 | 5,000 | 25,000 | 100,000 |
| Enrichment credits | — | 250 | 2,000 | 5,000 |
| Button | Start free | Start free | Start 14-day trial | Talk to us |

Card bullets:
- **Free:** 1 form and 1 meeting type, one-person meetings, Claritia CRM, unlimited editors
- **Starter:** Unlimited forms and booking pages, booking inside forms, round robin, HubSpot sync
- **Growth:** Rules, territories and owner lookup, AI qualify and meeting briefs, HubSpot, Salesforce and Omniscient
  sync, company reveal on your site, 3 AI journeys, Slack alerts
- **Scale:** Everything, with queues, two-way sync with every CRM, account alerts, unlimited AI journeys, SSO, audit
  log, priority support

- **Under the cards:** More contacts are $10 per 1,000. More emails are $1 per 1,000. More enrichment is $50 per
  1,000 credits.

---

## 16. FAQ

**Do I have to leave HubSpot?**
No. Claritia syncs both ways with HubSpot, Salesforce and Omniscient, and pushes leads to Pipedrive, Attio and Close.
Use Claritia as your CRM or keep yours.

**Can I keep my current forms?**
Yes. Claritia works with HubSpot, Webflow, Marketo, Framer, Typeform and plain HTML forms. Routing and booking work
the same on them.

**Who counts as a host?**
Anyone who takes meetings. People who build forms, edit workflows or read reports are free.

**How long does setup take?**
About 15 minutes. Sign up, connect your calendar, pick a form template and paste one line on your site. Your first
test fill books a real meeting.

**Where does lead data come from?**
Your own records and CRM first, then data vendors in order. Every value shows its source and date, and a person's own
edit always wins.

**Does the AI act on its own?**
AI qualify can only pick an outcome your team set up, and it shows its reason. Emails AI writes wait for your
approval before they send.

**Do I need a contract?**
No. Plans are monthly. Pay yearly if you want 2 months free.

---

## 17. Closing card

- **Headline:**
  > Your next lead is on your site right now.
  > Book them before they leave.
- **Buttons:** Start free · Book a demo
- **Small line:** Free plan, no card needed.

---

## 18. Footer

- **Line:** From website visit to booked meeting.
- **Status:** All systems running
- **Columns:**
  - Product: CRM, Automation, Inbound, Nurture, Pricing
  - Inbound: Forms, Scheduling, Routing, Visitors
  - Suite: Claritia, Arrowsterr, Omniscient
  - Company: Contact, Book a demo, Privacy, Terms, Sign in
- **Legal:** © 2026 Perceptric. Claritia is a Perceptric product.

---

## Before this goes live

1. **Prices.** `docs/pricing.md` in the app repo is still "proposed". Confirm the plans, then update `pricing.md` here
   and `src/lib/plans.ts` in the app.
2. **Numbers.** "15 min", "under 1 sec" and "2 fields" are goals from the specs. Time them on the live app first.
3. **Tool table.** Section 13 names competitors. Keep it to what each tool does, with no prices.
4. **Quotes.** There's no customer quote band yet. Add one when a design partner gives a quote you can use.
5. **llms.txt and pricing.md** still describe older versions. Update them with this copy.
