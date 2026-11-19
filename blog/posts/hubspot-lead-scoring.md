---
title: "HubSpot Lead Scoring: How It Works and How to Set It Up (2026)"
description: HubSpot lead scoring, step by step. See which HubSpot plans include it, how fit, engagement and predictive scores work, and the mistakes to avoid.
category: Integrations
kind: integration
date: 2026-11-19
---

Your HubSpot account fills up with contacts from forms, chats and email sign-ups. Some are buyers ready to talk. Most are not. Without a score, reps open the newest record first, and a good lead who filled in a demo form two days ago is still waiting for a reply.

HubSpot's lead scoring tool can sort those contacts for you, but it's spread across plans and options. Contact scores, deal scores, AI scores and the predictive likelihood to close each sit on a different hub or tier. Once you know which part does what, you can build a first score in an afternoon.

> **[Try Claritia free](https://app.tryclaritia.com/signup)** to send each form answer to HubSpot as a contact property, so your fit scores have the data they need from the first fill.

In this post, you'll see how HubSpot lead scoring works, which plans include it, how to set up a score step by step, and the mistakes to avoid.

## Main points

- HubSpot's lead scoring tool needs Marketing Hub or Sales Hub Professional or Enterprise. Free and Starter don't include it.
- Contact scores need Marketing Hub, deal scores need Sales Hub, and company scores work on either.
- You can build fit, engagement or combined scores, with negative points, group limits, score decay and High, Medium and Low labels.
- Predictive lead scoring, the likelihood to close property, needs Marketing Hub or Sales Hub Enterprise. AI-built contact scores need Marketing Hub Enterprise.
- On a lower plan, a form tool such as [Claritia](/) can qualify and route leads before they reach HubSpot, from Starter at $15 a seat a month.

## How HubSpot lead scoring works

HubSpot lead scoring gives contacts, companies or deals points based on their property values and actions. Each score saves its value in a score property, which you can then use in views, segments, workflows and reports. For the basics, read [what lead scoring is](/blog/what-is-lead-scoring).

There are three types of score:

- **Fit scores** look at property values, such as job title, company size, industry or region.
- **Engagement scores** look at actions, such as form submissions, email clicks, page visits and meetings.
- **Combined scores** use both and save three values: the total, the engagement part and the fit part.

Rules sit in groups. Each rule adds or takes away points, each group can have its own limit, and the whole score has a limit too. That lets you cap low-value actions, like page views, while letting a booked meeting count for much more.

### Score decay and thresholds

For engagement and combined scores, you can turn on score decay. It cuts the points from an action by a set share every 1, 3, 6 or 12 months, so old activity counts for less. Decay doesn't work on rules filtered by frequency or time frame.

Thresholds sort records into labels. Fit and engagement scores use High, Medium and Low. Combined scores use A1 to C3, where the letter is fit and the number is engagement, so C1 means a poor fit who is very engaged.

## Which HubSpot plans include lead scoring?

Plans and prices are from HubSpot's pricing pages and knowledge base, checked November 2026.

| Plan | Lead scoring | Number of scores | What it scores |
|---|---|---|---|
| Free and Starter | No | None | None |
| Marketing Hub Professional | Yes | Up to 5 | Contacts and companies |
| Marketing Hub Enterprise | Yes, with AI scores and AI recommendations | Up to 50 | Contacts and companies |
| Sales Hub Professional | Yes | Up to 5 | Companies and deals |
| Sales Hub Enterprise | Yes | Up to 10 | Companies and deals |

On price, HubSpot lists Marketing Hub Professional from $800 a month with 3 core seats, plus a required one-time onboarding fee of $3,000. Marketing Hub Enterprise starts at $3,600 a month with 5 core seats, plus $7,000 onboarding.

Sales Hub Professional starts at $90 a seat a month with a $1,500 onboarding fee, and Sales Hub Enterprise at $150 a seat a month with a $3,500 fee.

## Predictive lead scoring in HubSpot

HubSpot has three kinds of AI scoring, and they're easy to mix up.

- **Likelihood to close.** HubSpot's predictive lead score. It estimates the chance, as a percentage, that a contact becomes a customer in the next 90 days, and you can't edit how it works. It needs Marketing Hub or Sales Hub Enterprise.
- **Contact priority.** Built from likelihood to close. It sorts contacts into Very High, High, Medium and Low, with a quarter of your contacts in each, plus Closed Won for customers.
- **AI scores in the lead scoring tool.** On Marketing Hub Enterprise, HubSpot can build a contact fit or engagement score for you from your own data. It needs at least 50 contacts to learn from, 25 that converted and 25 that didn't.

Separately, deal scores predict the chance of winning each open deal, on Sales Hub Professional and Enterprise. HubSpot notes they shouldn't be the only thing you base a decision on.

## What you need

- **The right plan:** Marketing Hub Professional or Enterprise to score contacts, or Sales Hub Professional or Enterprise to score deals.
- **Edit permissions for Lead Scoring:** View permissions only let you see scores.
- **Clean properties:** Fit rules can only score what's on the record, so job title, company size and region need real values.
- **A list of your best customers:** Ten or twenty won deals are enough to spot what good leads share.

## Step 1: Write down what a good lead looks like

Before you open HubSpot, write two short lists with your sales team. The first is fit: the company size, industry, region and roles that buy from you. The second is interest: the actions that come before a sale, like a demo request, a pricing page visit or a booked meeting.

Add a third list of bad signs, like a personal email address, a student title or a region you don't serve. These become negative rules.

## Step 2: Create the score

1. Go to Marketing, then Lead Scoring. In some accounts it sits under More.
2. Click **Create score**, or **Create score with AI** if you're on Marketing Hub Enterprise.
3. Pick the object: Contacts (Marketing Hub), Companies, or Deals (Sales Hub).
4. Pick the type: fit, engagement or combined. Deal scores are combined by default.
5. Name the score so your team knows what it's for, such as "Inbound contact score".

## Step 3: Add fit rules

1. Click **+ Add property group**.
2. Add a property rule, such as **Number of employees** is between 20 and 200.
3. Choose to add or subtract points, and enter the number.
4. Add more criteria to a rule only when all of them must be true, since criteria in one rule use AND logic.
5. Add negative rules for bad fits, such as a region you don't serve.

You can also score on segment membership. That helps with OR logic: build a segment for "any of these job titles" and give points for belonging to it.

## Step 4: Add engagement rules

1. Click **+ Add event group** and give it a clear name, like "Sales actions".
2. Add an event rule, such as a form submission on your demo form, or a meeting booked.
3. Set points for each action. A demo form should count far more than a newsletter sign-up.
4. Use **Limit to** for actions that repeat, so ten page views don't outweigh one demo request.
5. Set a group limit, so a whole group of small actions can't push a lead to the top.
6. Turn on **Decay scores** for actions that go stale, for example 50% after 3 months.

Calls only count toward scores when they're made with HubSpot's own calling tool.

## Step 5: Choose which records to score

On the Contacts, Companies or Deals tab, choose to score all records or only some. You can leave out segments, such as current customers or your own staff, so their scores don't skew your reports.

## Step 6: Set the score limit and thresholds

Pick a score limit. The ranges run from -100 to 100 up to -10,000 to 10,000. Then set the threshold ranges, for example 70 to 100 as High, 40 to 69 as Medium and anything below 40 as Low.

## Step 7: Test it, then turn it on

Use the test records option to check a few contacts you know well: a recent customer, a good open lead and a poor fit. Preview the score spread too. If almost everyone is High, your points are too generous.

When you turn the score on, HubSpot scores records from their past values and actions, then keeps updating as things change.

## Step 8: Put the score to work

A score only helps when it starts something. Some ideas HubSpot itself suggests:

- A saved view or segment of every contact with a High score.
- A workflow that assigns an owner to unworked contacts with a score over 50.
- A workflow that alerts the deal owner when a deal score goes above 75.
- A report that compares scores by the channel each contact came from.

To send high scorers to the right rep, pair the score with routing. Our guide to [HubSpot lead routing](/blog/hubspot-lead-routing) shows how to rotate owners and add round robin meeting pages.

## Common mistakes

- **Scoring every action.** Page views pile up and drown out the actions that matter. Use limits and decay.
- **No negative points.** Students and competitors climb the list.
- **Empty fit properties.** A fit rule can't score a blank field. Ask for the details on your forms and map them to properties.
- **Rules that need AND but use OR, or the other way round.** Criteria inside one rule must all match. Use a segment for "any of".
- **Changing a live score without checking.** HubSpot rescores every record when you edit a score, which can change workflows and segments that use it. Check the property's Used In tab first.
- **Expecting AI scores on a young account.** Without 25 converted and 25 non-converted contacts, HubSpot can't build an AI score.

## Tools for HubSpot lead scoring

HubSpot's own scoring works well once you're on Professional. These tools help fill the score with data, or score and route leads if you're on a lower plan.

### Claritia

[Claritia](/) is a forms, scheduling and follow-up app built for small B2B teams that want every lead from their website to reach the right rep and book a meeting before they leave the page.

It builds forms from a sentence or one of 840 templates, opens the right person's calendar the moment the form is sent, routes each lead by its answers, and drafts follow-up emails in your brand's voice for you to approve.

On Starter, each fill creates or updates a HubSpot contact matched by email, and you map each question to a contact property, so fit rules have real values to score. Fills also show on the contact's timeline.

- **Free:** Form calculations add up points as a lead answers, so you can qualify inside the form.
- **Starter, $15 a seat a month ($12 yearly):** The [HubSpot integration](/integrations/hubspot), with field mapping and owners.
- **Pro, $39 a seat a month ($31 yearly):** [Routing](/products/routing) by any answer to a meeting and a person.
- **Business, $79 a seat a month ($63 yearly):** Known HubSpot contacts book with their owner first.

Claritia also keeps segments and lead scoring of its own. It's a newer tool, so its marketplace is smaller than HubSpot's, and its Zapier and Make apps aren't listed yet.

### Zoho CRM

[Zoho CRM](https://www.zoho.com/crm/) is a sales CRM for businesses of all kinds that want to capture leads, sell as a team and automate routine work. It tracks leads, contacts and deals across pipelines, scores leads by engagement and details, assigns them by round robin or with its AI assistant Zia, and runs follow-up cadences. A free edition covers 3 users.

If HubSpot Professional is out of reach, Zoho CRM has scoring rules from its Standard edition at $14 a user a month billed yearly, and Zia's AI scores from Professional at $23.

### Freshsales

[Freshsales](https://www.freshworks.com/crm/sales/) is Freshworks' sales CRM for startups and growing businesses that want to find, qualify and close leads from one place. It captures leads from campaigns, then qualifies, routes and tracks them, with kanban pipelines, built-in chat, email and phone, and automated workflows. Its AI, Freddy, highlights the best leads and deals and writes emails.

Its Pro plan adds AI contact scoring at $39 a user a month billed yearly. For more options, see our list of the [best lead scoring software](/blog/best-lead-scoring-software).

## Questions

### Is HubSpot lead scoring free?

No. The lead scoring tool needs Marketing Hub or Sales Hub Professional or Enterprise. The free CRM and Starter plans don't include it.

### Does HubSpot have predictive lead scoring?

Yes. The likelihood to close and contact priority properties predict which contacts will become customers in the next 90 days. They need Marketing Hub or Sales Hub Enterprise.

### What is the difference between fit and engagement scores in HubSpot?

Fit scores use property values, like job title or company size. Engagement scores use actions, like form submissions, email clicks and meetings. Combined scores use both.

### How many lead scores can I create in HubSpot?

Professional plans allow up to 5 scores. Marketing Hub Enterprise allows up to 50, and Sales Hub Enterprise up to 10.

### Can HubSpot lead scores go negative?

Yes. Rules can subtract points, and a score goes below zero when more is taken away than added. If you don't want negative scores, use only rules that add points.

### Can I use lead scores in HubSpot workflows?

Yes. Each score saves its value in a score property, and you can use it in workflow triggers and branches, views, segments and reports. A common use is assigning an owner when a score passes a set number.

## Get started

Write down your fit, interest and bad-fit signals, check your HubSpot plan, then build one score and test it on records you know. Connect the score to a workflow so high scorers reach a rep fast.

> **[Try Claritia free](https://app.tryclaritia.com/signup)** to send every form answer to HubSpot and book the best leads with the right rep on the spot.

You can also see the [HubSpot integration](/integrations/hubspot) or read our guide to [HubSpot lead routing](/blog/hubspot-lead-routing).
