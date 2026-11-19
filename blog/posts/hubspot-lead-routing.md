---
title: "HubSpot Lead Routing: How to Send Every Lead to the Right Rep (2026)"
description: "HubSpot lead routing, step by step: rotate owners with workflows, add round robin meeting pages, and see which HubSpot plan each part of the setup needs."
category: Routing
kind: route
date: 2026-11-18
---

A new lead fills in your HubSpot form. Then nothing happens. The contact sits with no owner, or with whoever got the last one, and someone has to read it and pass it on. By the time a rep writes back, the lead has moved on or booked with someone else.

HubSpot can route leads on its own, but the tools are spread across workflows, meeting pages and form settings, and each one sits on a different plan. Once you know which part does what, you can set it up in an afternoon.

> **[Try Claritia free](https://app.tryclaritia.com/signup)** to route each HubSpot form lead by its answers and book the meeting with the right rep before the lead leaves the page.

In this post, you'll set up lead routing in HubSpot step by step, see which plan each step needs, and fix the most common problems.

## Main points

- HubSpot routes leads with the **Rotate record to owner** workflow action. It needs Sales Hub or Service Hub Professional or Enterprise, and every rep in the rotation needs a paid Sales or Service seat.
- Round robin meeting pages work on Sales Hub or Service Hub Starter and up, and can show a known contact's owner first.
- Sending a form straight to a meeting page with conditional logic needs Sales Hub or Service Hub Enterprise.
- If you're on a lower plan, a form tool such as [Claritia](/) can route by answer and set the HubSpot owner from Starter at $15 a seat a month.
- Other options: [Chili Piper](https://www.chilipiper.com/) for large teams and [Calendly](https://calendly.com/) Teams for routing forms on a booking link.

## What is HubSpot lead routing?

HubSpot lead routing is how a new contact or lead gets an owner in HubSpot. Rules decide which rep should take each lead, then HubSpot sets the owner property so that rep gets the record, the alert and the follow-up task. For the basics, read [what lead routing is](/blog/what-is-lead-routing).

HubSpot gives you three tools for it:

- **Workflows** that rotate the owner among a team or a list of reps.
- **Round robin meeting pages** that book the lead with the next free rep.
- **Form settings** that notify the owner, and on Enterprise, send the lead to a meeting page based on answers.

## What you need

Check these before you start. Prices are from HubSpot's pricing page, checked November 2026.

| Part of the setup | Plan it needs | Who needs a seat |
|---|---|---|
| Forms that create contacts | Every plan, free included | Anyone who edits forms |
| Rotate record to owner in a workflow | Sales Hub or Service Hub Professional or Enterprise | Every rep in the rotation needs a paid Sales or Service Professional or Enterprise seat |
| Round robin meeting pages | Sales Hub or Service Hub Starter, Professional or Enterprise | Each rep needs a Sales or Service seat and a connected calendar |
| Conditional logic on forms | Marketing Hub or Content Hub Professional or Enterprise | Anyone who edits forms |
| Form that redirects to a meeting page by answer | Sales Hub or Service Hub Enterprise | Each rep on the meeting page |

On price, HubSpot lists Sales Hub Professional from $90 a seat a month, plus a required one-time onboarding fee of $1,500. Enterprise starts at $150 a seat a month, plus a $3,500 onboarding fee. Starter costs less, but the Rotate record to owner action isn't on it.

You also need:

- **Teams set up in HubSpot**, if you want to rotate by team.
- **The fields routing needs** on your form, such as country, company size or what the lead wants.
- **Super Admin or Workflows permission** to build the workflow.

## Step 1: Write down who should get which lead

Before you touch HubSpot, write your rules on one page. Keep it short:

- Which leads go to which team? For example, companies with more than 50 people go to the enterprise team.
- Who covers which region?
- Should a lead who already has an owner keep that owner?
- Who takes a lead when no rule matches?

Each rule becomes a branch in your workflow. If you can't write a rule in one line, it's too complex for the first version.

## Step 2: Set up teams and seats

Open Settings, then Users and teams, and put your reps into teams. A workflow can rotate within a team, which is easier to keep up than a hand-picked list of names.

Check every rep's seat. HubSpot only rotates to active users with a paid Sales or Service Professional or Enterprise seat. Users with core or view-only seats are greyed out, and so are people who haven't accepted their invite. For team rotation, only main team members with the right seat get leads.

## Step 3: Ask the right questions on your form

Routing can only use what you know. Add the fields your rules need to the form, and make the key ones required. A dropdown for country or company size works better than a text box, because a workflow branch can match the exact value.

In the form's settings, turn on **Notify contact owner** if you want the owner alerted each time a contact they own sends the form. If the contact has no owner yet, no alert goes out, so the workflow in the next step matters.

## Step 4: Build a workflow that rotates the owner

1. Go to Automation, then Workflows, and create a contact-based workflow.
2. Set the enrollment trigger to a submission of your form.
3. Add a branch for each rule from Step 1, such as company size or region.
4. In each branch, add the **Rotate record to owner** action from the CRM section.
5. Pick the owner property. By default it's the contact owner.
6. Choose whether to overwrite an existing owner. Leave it off if known contacts should keep their rep.
7. Pick specific users or a team to rotate between.
8. Save the workflow and turn it on.

By default, HubSpot shares records equally within the team or list you picked. If you rotate HubSpot's lead records instead of contacts, which HubSpot marks as beta, you also get load balanced, round robin and random options, and you need Sales Hub Professional or Enterprise. Turn off the setting that syncs the lead owner with the contact or company owner first, or the two will fight.

## Step 5: Let the lead book with a rep

An owner on the record is only half the job. The lead still needs to talk to someone. Create a round robin scheduling page in the meetings tool and add the same reps. It shows the open times of everyone on the page, so the lead books with whoever is free.

On the page's welcome tab, turn on **Prioritize contact owner**. A known contact enters their email and sees their owner's calendar first. Link the meeting page on your form's thank-you message, or on Sales Hub or Service Hub Enterprise, use form conditional logic to redirect each lead to the right meeting page by answer.

## Step 6: Test it, then keep an eye on it

Send a few test entries, one for each branch. Check that each contact got the right owner, that the alert reached the rep, and that the meeting page showed the right people. Then check the workflow's history each week for the first month, so you catch leads that fell through a gap in your rules.

## Common problems

- **The lead has no owner.** If no eligible user is left in the rotation, or no team is picked, HubSpot assigns no one. Check seats and add a catch-all branch.
- **The rotation looks uneven.** Adding or removing reps from the action resets its counts, and new leads are spread evenly from that point.
- **Leads move slowly.** HubSpot lets one record through the rotate action at a time to keep it fair, so a burst of leads can queue up.
- **Owners flip back.** If the HubSpot owner property syncs to Salesforce, Salesforce may write the old owner back. Pick one system to own assignment.
- **Reps are greyed out.** They need a paid Sales or Service seat and an accepted invite.
- **The action is locked.** Free and Starter plans don't include Rotate record to owner. Use round robin meeting pages on Starter, or a form tool that sets the owner for you.

## Tools for HubSpot lead routing

HubSpot's own tools work well once you're on Professional. If you're not, or if you want the lead routed and booked in one step, these tools connect to HubSpot.

### Claritia

[Claritia](/) is a forms, scheduling and follow-up app built for small B2B teams that want every lead from their website to reach the right rep and book a meeting before they leave the page. It opens the right person's calendar the moment the form is sent, routes each lead by its answers, and drafts follow-up emails in your brand's voice for you to approve. On Starter, each fill creates or updates a HubSpot contact matched by email, and either Claritia's routing or HubSpot's own rules can pick the owner. Contacts that already have an owner keep theirs. You can also keep your HubSpot forms, since Claritia hears the form send and opens the right calendar.

- **Starter, $15 a seat a month ($12 yearly):** The [HubSpot integration](/integrations/hubspot), field mapping and fills on the contact timeline.
- **Pro, $39 a seat a month ($31 yearly):** [Routing](/products/routing) by any answer, round robin with weights, team pools and a routing log.
- **Business, $79 a seat a month ($63 yearly):** Known HubSpot contacts book with their owner first, and new leads go to the team's round robin.

Claritia is a newer tool, so its app marketplace is smaller than HubSpot's, and its Zapier and Make apps aren't listed yet.

### Chili Piper

[Chili Piper](https://www.chilipiper.com/) is a meeting booking and lead routing platform for B2B revenue teams that want inbound buyers to book with the right rep right away. When someone submits a form, it qualifies them, routes them by rules such as company size, region or account owner, and shows that rep's calendar on the spot. It also routes Salesforce records by rep workload, identifies visiting companies, runs an AI chat, blocks fake bookings and sends reps a brief before each meeting. It works with HubSpot and Salesforce, and its Growth plan adds form routing, territory and assignment rules, and fair lead distribution. Growth starts at $15,000 a year with 15 seats, all plans are billed yearly, and it fits larger sales teams.

### Calendly

[Calendly](https://calendly.com/) is scheduling software for professionals and teams who want people to book meetings without trading emails. You connect your calendars, set hours, buffers, and daily limits, and share booking links for one-on-one, multi-host, or group meetings. It sends email and text reminders, offers routing forms that send website leads to the right teammate, and collects payments. Newer tools include an AI assistant that finds times over email and a notetaker that writes meeting recaps. Its Teams plan adds routing forms and round robin at $16 a seat a month billed yearly, so a lead answers a few questions and lands on the right booking page. It suits teams who want light routing in front of a booking link.

For more options, see our list of the [best lead routing software](/blog/best-lead-routing-software).

## Questions

### Does HubSpot have lead routing?

Yes. The Rotate record to owner workflow action assigns leads to reps in turn, and round robin meeting pages book leads with the next free rep. Workflows need Sales Hub or Service Hub Professional or Enterprise.

### Can I do round robin lead assignment in HubSpot for free?

No. The free plan has forms and one-to-one meeting links, but no round robin pages and no Rotate record to owner action. Round robin meeting pages start on Sales Hub or Service Hub Starter, and workflow rotation starts on Professional.

### How do I route HubSpot form submissions to different reps?

Build a workflow triggered by the form, add a branch for each rule, and put a Rotate record to owner action in each branch. To send each lead to a meeting page by answer, you need Enterprise, or a form tool like Claritia that routes by answer on Pro.

### What is HubSpot lead form routing?

It sends a form lead to the right meeting page based on their answers. HubSpot lists Lead Form Routing as a Sales Hub Enterprise feature, and redirecting a form to a scheduling page with conditional logic needs Sales Hub or Service Hub Enterprise.

### Why didn't my HubSpot rotation assign an owner?

Most often, no one in the rotation has an active paid Sales or Service seat, or no team was picked. HubSpot then leaves the record with no owner.

### Can a known contact go to their existing owner?

Yes. Leave "overwrite existing owner" off in the workflow, and turn on Prioritize contact owner on round robin meeting pages. In Claritia, owner first does the same on Business.

## Get started

Write down your rules, check your HubSpot plan, then build the workflow and the meeting page. If your plan doesn't include the rotate action, route from the form instead.

> **[Try Claritia free](https://app.tryclaritia.com/signup)** to build a form that sends each lead to HubSpot and books the meeting with the right rep.

You can also see the [HubSpot integration](/integrations/hubspot) or compare [HubSpot Forms alternatives](/blog/best-hubspot-forms-alternatives).
