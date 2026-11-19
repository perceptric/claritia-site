---
title: What Is Lead Scoring? Models, Examples and How It Works (2026)
description: What is lead scoring? Learn how fit and interest scores work, copy a simple point model, and see how each score decides routing and follow-up.
category: Routing
kind: logic
date: 2026-11-19
---

Your form brings in twenty leads this week. One is a director at a company that fits you well and asked for a demo. Another is a student writing a paper. If both land in the same inbox, your reps answer them in the order they arrived, and the best lead waits behind the student.

Lead scoring fixes the order. Each lead gets points for who they are and what they do, and the total tells your team who to call first, who to nurture and who to leave alone. A short list of rules on one page is enough to start.

> **[Try Claritia free](https://app.tryclaritia.com/signup)** to qualify each lead inside the form and book the good fits with the right rep on the same page.

Below, we explain how a scoring model works, give you a simple point model to copy, and show how the score drives routing and follow-up.

## Main points

- Lead scoring gives each lead points for fit (who they are) and interest (what they do), then uses the total to pick the next step.
- A good model also takes points away: for bad fits like students or competitors, and for interest that has gone cold, called score decay.
- Predictive or AI scoring learns from your past won and lost leads, but it needs enough history to work.
- A score only helps when it triggers something: a rep, a meeting, a nurture email or nothing at all.
- Tools to look at: [Claritia](/) for scoring and routing form leads, [HubSpot](https://www.hubspot.com/) and [Salesforce Sales Cloud](https://www.salesforce.com/sales/).

## What is lead scoring?

Lead scoring is a way to rank leads by giving each one points for how well they fit your ideal customer and how interested they seem. The total score tells your team which leads to contact first and which to nurture until they're ready.

It's one part of [lead qualification](/blog/lead-qualification). Qualification asks "is this a good lead?" Scoring turns the answer into a number, so software can sort hundreds of leads the way a careful rep would sort ten.

## How lead scoring works

Most scoring follows the same six steps, in a spreadsheet or in a CRM:

1. **Describe your best customers.** Look at the deals you won. What size were those companies, who bought, and what did they do first?
2. **Turn those traits into rules.** Each rule is one fact you can check, such as "company has 20 to 200 employees" or "visited the pricing page".
3. **Give each rule points.** Strong signals get more points. Signs of a bad fit take points away.
4. **Add up the score.** Each time a lead's details change or they do something, the score updates.
5. **Set thresholds.** Decide what score makes a lead hot, warm or cold, and what happens at each level.
6. **Check it against results.** After a month or two, see which scores became meetings and deals, and adjust the points.

## Types of lead scoring

### Fit score

A fit score looks at who the lead is: company size, industry, country, job title or budget. This data comes from your form answers, your CRM or an enrichment service. A high fit score means "this is the kind of company we sell to."

### Interest score

An interest score, also called an engagement or behavior score, looks at what the lead does. Asking for a demo, visiting the pricing page, opening emails and coming to a webinar all add points. A high interest score means "they're paying attention right now."

### Combined score

Most teams use both. A combined score adds fit and interest together, or keeps them side by side. Keeping them apart helps: a perfect fit with no interest needs nurture, while a poor fit with lots of interest might be a student.

### Negative scoring

Negative scoring takes points away. Common examples are a personal email address on a B2B form, a job title like student or job seeker, a competitor's domain, a country you don't sell to, or an unsubscribe. Without negative rules, a curious student who reads every blog post can outscore a real buyer.

### Score decay

Interest fades. A pricing page visit last week means more than one a year ago. Score decay lowers interest points as time passes, for example by half after 30 days. Fit points usually don't decay, since a company's size rarely changes month to month.

### Predictive or AI scoring

Predictive scoring, sometimes called AI lead scoring, skips the hand-written rules. A model looks at leads that became customers and leads that didn't, finds what they had in common, and scores new leads by how much they look like past winners.

It needs history to learn from. In HubSpot, for example, an AI score needs at least 50 contacts to train on, with 25 that converted and 25 that didn't. A new team with few deals is better off with simple rules.

## A simple lead scoring model

Here's a starting model for a small B2B team. Change the rules to match your own customers.

| Rule | Type | Points |
|---|---|---|
| Company has 20 to 200 employees | Fit | +20 |
| Job title is founder, head of, director or VP | Fit | +15 |
| Based in a country you sell to | Fit | +10 |
| Uses a tool you connect with | Fit | +5 |
| Asked for a demo or a quote | Interest | +30 |
| Visited the pricing page | Interest | +10 |
| Came to a webinar | Interest | +10 |
| Opened 3 or more emails in 30 days | Interest | +5 |
| Personal email address on a B2B form | Negative | -10 |
| Unsubscribed from emails | Negative | -20 |
| Student or job seeker | Negative | -30 |
| Works at a competitor | Negative | -50 |

Then set three thresholds:

- **60 or more, hot:** Route to a rep and offer a meeting right away.
- **30 to 59, warm:** Send nurture emails and score again as they act.
- **Under 30, cold:** Keep them on the newsletter and spend no rep time.

Two leads show how it plays out. Jane is an operations director at an 80-person firm in a country you sell to, and she asks for a demo. She scores 20 + 15 + 10 + 30 = 75, so she's hot and goes straight to a rep.

Tom signs up with a personal email, visits the pricing page and opens a few emails. He scores -10 + 10 + 5 = 5, so he stays on the newsletter until he does more.

## How a score drives routing and follow-up

A score sitting in a CRM field does nothing. It pays off when each threshold starts a clear action:

- **Hot leads go to a rep fast.** The lead gets an owner, the rep gets an alert, and in the best setups the lead books a meeting on the spot. Read more on [what lead routing is](/blog/what-is-lead-routing).
- **The score picks the team.** High fit scores can go to senior reps, while smaller leads go to a shared round robin.
- **Warm leads get nurture.** Useful emails until their interest score crosses the line.
- **Crossing a threshold is an event.** When a score jumps past 60, a workflow can assign an owner, so a lead that warms up slowly isn't missed.

Speed matters most at the top. A hot lead who waits a day may already be talking to someone else.

## Best practices

- **Start with five to ten rules.** A short model takes two minutes to explain to a rep.
- **Ask for what scoring needs.** If company size matters, ask for it on the form with set choices.
- **Keep fit and interest apart.** Two numbers tell you more than one.
- **Agree on thresholds with sales.** When both teams sign off on what "hot" means, reps trust the leads they get.
- **Review every quarter.** Compare scores with meetings held and deals won, then move the points.

## Common mistakes

- **Scoring everything.** Points for every page view make the score noisy. Ten blog posts don't make a lead ten times more likely to buy.
- **No negative rules.** Students and competitors climb the list and waste rep time.
- **No decay.** Leads who were active a year ago stay "hot" forever.
- **A score with no action.** If nothing happens when a lead turns hot, the scoring work was wasted.

## Tools for lead scoring

Lead scoring is built into many CRMs, often on their higher plans. For prices and more tools, see our list of the [best lead scoring software](/blog/best-lead-scoring-software).

### Claritia

[Claritia](/) is a forms, scheduling and follow-up app built for small B2B teams that want every lead from their website to reach the right rep and book a meeting before they leave the page.

It builds forms from a sentence or one of 840 templates, opens the right person's calendar the moment the form is sent, routes each lead by its answers, and drafts follow-up emails in your brand's voice for you to approve.

It keeps segments and lead scoring next to your contacts, and its AI qualify step only picks an outcome you set. In forms, calculations can add up points as a lead answers, on every plan.

Routing by any answer to a meeting and a person starts on Pro, with a log of why each lead went where it did. See how [Claritia routing](/products/routing) works.

![Claritia routing rules that book large teams into an enterprise demo and send small budgets a starter guide](/assets/blog/ui/ui-routing-routing.webp)

*Caption: Claritia's routing rules act on form answers, such as team size, country and budget, to pick the next step.*

### HubSpot

[HubSpot](https://www.hubspot.com/) is a customer platform for businesses of all sizes that want their marketing, sales and customer service teams to work from the same customer data. It is built around a shared CRM and adds separate products, called hubs, for marketing, sales, service, content, data management, and quotes and billing.

Teams use it to capture leads with forms and chat, send email campaigns, manage deals, run a help desk, build web pages and set up AI agents.

Its lead scoring tool builds fit, engagement and combined scores with group limits, negative points and score decay. It needs Marketing Hub or Sales Hub Professional or Enterprise, and AI-built contact scores need Marketing Hub Enterprise. Our guide to [HubSpot lead scoring](/blog/hubspot-lead-scoring) walks through the setup.

### Salesforce Sales Cloud

[Salesforce Sales Cloud](https://www.salesforce.com/sales/) is a sales CRM for companies of every size that want their sellers to track every account, deal and conversation in one place and hit their number. It captures calls, emails and meetings on each record, manages pipelines and forecasts, and adds AI agents that research prospects, prep deals and watch accounts.

Its lead scoring is predictive: it studies your data, predicts which leads are most likely to convert and shows the factors behind each score. Salesforce's pricing page lists it on the Advanced and Max editions, and as a paid extra on Core. Prices checked November 2026.

## Questions

### What is a lead scoring model?

A lead scoring model is the set of rules and points you use to score leads, plus the thresholds that say what each score means. A simple model has five to ten fit and interest rules, a few negative rules and three levels: hot, warm and cold.

### What is a good lead score?

There's no universal number. A good score is one that, in your own data, turns into meetings and deals more often than lower scores. Check after a month which scores became customers.

### What is the difference between fit and interest scores?

A fit score measures who the lead is, like company size or job title. An interest score measures what they do, like asking for a demo or visiting your pricing page. Most teams use both.

### How is lead scoring different from lead qualification?

Lead qualification decides whether a lead is worth sales time. Lead scoring is one way to decide, by adding up points. Frameworks like BANT are another, and many teams use both.

### Do small teams need lead scoring?

If a rep can read every lead each day, a few clear questions on your form may be enough. Scoring earns its place when leads pile up faster than your team can read them.

## Get started

Write five fit rules, five interest rules and a few negative ones. Set three thresholds, decide what happens at each, and check the results after a month.

> **[Try Claritia free](https://app.tryclaritia.com/signup)** to build a form that qualifies each lead and books the hot ones with the right rep before they leave.

You can also read about [lead qualification](/blog/lead-qualification) or how [lead routing](/blog/what-is-lead-routing) sends each lead to the right person.
