# Claritia brand guide

**Version 1.0 · 26 October 2026**
The visual system for tryclaritia.com, the app, and everything made for Claritia.

This guide is the source of truth. It is written for designers and engineers who need to make a new page, component, email or ad without guessing. The values live in code in `assets/tokens.css`; this document explains why they exist and how to use them.

The design language was extracted from the live Mintlify marketing site on 26 October 2026: its layout grid, type scale, color roles, component proportions and motion. Claritia does not use Mintlify's name, copywriting, logo, images, proprietary font files or stylesheet. The values are a starting point, not a template to clone.

---

## 1. The idea

**Calm infrastructure for inbound.**

Claritia does a noisy job — catching leads, finding out who they are, routing them, booking the meeting — and makes it feel quiet. The page should feel like the product: ordered, legible, fast, and in control. Nothing shouts. The evidence does the persuading.

The design has four jobs:

1. **Make the product visible.** Real interface fragments, real labels, real numbers. Not abstract dashboards or stock photography.
2. **Make the path obvious.** One idea per section, one primary action, a clear line from visit to booked meeting.
3. **Make the brand memorable.** Warm paper, sharp ink, one emerald signal, editorial serif at the few biggest moments.
4. **Get out of the way.** Generous space, small type, thin rules, restrained motion. The reader should feel the page breathe.

### Attributes

| We are | We are not |
|---|---|
| Precise | Clever |
| Calm | Sleepy |
| Warm | Soft |
| Direct | Blunt |
| Evidence-led | Hype-led |
| Human | Quirky |

---

## 2. Logo

### The mark

The Claritia mark is a rounded square containing four corner brackets and a check. It reads as "captured" plus "confirmed": the lead is caught, the meeting is booked.

- Tile: `#0C8C5E` emerald.
- Glyph: white, 2px corner brackets and a 2.4px check in a 32-unit viewBox.
- Tile radius: 6px at 32px; scale the radius proportionally (18.75% of the tile).
- Minimum size: 20px digital. Below that, use the tile alone without the check.
- Clear space: at least the height of the check on every side; never crowd the mark with text or a border.

The asset lives at `assets/brand/claritia-mark.svg`. The same geometry is used in the header, footer, favicon and app switcher.

### The wordmark

"Claritia" is set in **Inter 600**, sentence case, tracking `-0.03em`. At 20px it pairs with a 24px mark and a 9px gap. Do not set the wordmark in the serif, in all caps, or in a second typeface.

### Lockups

| Lockup | Use |
|---|---|
| Mark + wordmark, horizontal | Header, footer, documents |
| Mark only | Favicon, app icon, avatar, small spaces |
| Wordmark only | Co-branding where the mark is already present |

### Don'ts

- Do not recolor the mark to blue, clay, black or a gradient.
- Do not put the mark on a busy photograph or on vivid mint without a paper tile behind it.
- Do not rotate, outline, emboss or add a shadow to the mark.
- Do not stretch the mark or change the tile radius.
- Do not recreate the mark with a different check or different bracket weights.

---

## 3. Color

The palette is a warm paper ground, near-black ink, and a single emerald signal. Vivid mint and lime belong to decorative line art and dark surfaces. Other hues are status colors, not brand colors.

### Core palette

| Token | Hex | Role |
|---|---|---|
| `--bg` | `#FEFDFB` | Page ground |
| `--bg-alt` | `#FAF8F5` | Alternate band, quiet surface |
| `--bg-card` | `#F9F6F3` | Bento and content cards |
| `--bg-deep` | `#EBE9E6` | Pressed surface, table header |
| `--ink` | `#08090A` | Primary text, primary button |
| `--ink-2` | `#121715` | Display and heading alternative |
| `--text-2` | `#485450` | Body secondary, labels |
| `--text-3` | `#5F6B67` | Second heading line, muted, card descriptions |
| `--text-4` | `#69736E` | Micro labels, placeholders, metadata |
| `--line` | `#F1F0EE` | Rails, dividers, table rules |
| `--line-2` | `rgba(8,9,10,.07)` | Card borders |
| `--line-3` | `rgba(8,9,10,.15)` | Input borders, stronger rules |
| `--brand` | `#0A7A52` | Text-safe brand green: links, labels, values |
| `--brand-mark` | `#0C8C5E` | Logo tile, decorative fills |
| `--brand-strong` | `#1FA77A` | Brand hover, small fills |
| `--brand-soft` | `rgba(12,140,94,.08)` | Numeric chip wash |
| `--mint` | `#18E299` | Accent on dark grounds, line art |
| `--lime` | `#A8FB36` | Line-art gradient end |
| `--orange` | `#EB9411` | Signal: waiting, attention |
| `--blue` | `#2992E3` | Signal: information |
| `--purple` | `#D87CFF` | Signal: AI |
| `--red` | `#FB2C36` | Error, destructive |

### Dark palette (documented, not active)

The live site is light-only. These values are reserved for a future `[data-theme="dark"]` build and must not be applied by system preference until every component is audited.

| Token | Hex |
|---|---|
| `--bg` | `#0A0B0F` |
| `--bg-alt` | `#111216` |
| `--bg-card` | `#0F0F12` |
| `--ink` | `#FAF8F5` |
| `--ink-2` | `#F2EFEA` |
| `--text-2` | `#D9D7D4` |
| `--text-3` | `#CFCDCA` |
| `--text-4` | `#969E9B` |
| `--line` | `#1E1F21` |
| `--line-2` | `rgba(255,255,255,.08)` |
| `--line-3` | `rgba(255,255,255,.15)` |
| `--brand` | `#18E299` |

### Usage ratio

**80 / 15 / 5.**

- 80% paper and ink: grounds, text, borders, whitespace.
- 15% neutral surfaces: cards, alternating bands, tables.
- 5% emerald and mint: the accent tick, links, numeric chips, one line-art field, the active state.

The page should look almost monochrome at arm's length. The green is a signal, not a theme.

The mark keeps the reference emerald `#0C8C5E`. Small green text uses the slightly darker `#0A7A52` so it clears 4.5:1 on paper and cards. The muted grays were darkened for the same reason.

### Accent rules

- `--brand` green is for text and icons on light grounds. On paper it passes 4.5:1 at body sizes. The logo tile keeps `--brand-mark`, the brighter `#0C8C5E` emerald.
- `--mint` is for dark grounds and decoration. Never set mint body text on cream.
- Orange, blue and purple are for product statuses and small data marks only. Do not use them for large sections.
- No gradient text, no colored glows, no rainbow borders.
- A full-bleed color block is allowed once per page, and only for a proof or product moment. It should be a flat brand-derived color, not a gradient.

### Contrast

| Pair | Ratio | Passes |
|---|---|---|
| `#485450` on `#FEFDFB` | 7.8:1 | AAA body |
| `#5F6B67` on `#FEFDFB` | 5.5:1 | AA body |
| `#5F6B67` on `#F9F6F3` | 5.2:1 | AA body on cards |
| `#69736E` on `#FEFDFB` | 4.8:1 | AA micro labels |
| `#69736E` on `#F9F6F3` | 4.6:1 | AA micro labels on cards |
| `#08090A` on `#FEFDFB` | 19.6:1 | AAA |
| `#FFFFFF` on `#08090A` | 19.9:1 | AAA |
| `#FFFFFF` on `#0C8C5E` | 4.3:1 | Large text and logo only |
| `#0A7A52` on `#FEFDFB` | 5.3:1 | AA body |
| `#0A7A52` on `#F9F6F3` | 5.0:1 | AA body on cards |
| `#18E299` on `#0A0B0F` | 11.6:1 | AAA |

`--text-4` is only for 12px labels, placeholders and metadata; it now clears 4.5:1 on paper and cards. Never use it for body copy.

---

## 4. Typography

### Families

| Role | Family | Source | Notes |
|---|---|---|---|
| Display | **Instrument Serif** | Google Fonts, SIL Open Font License | A free stand-in for Mintlify's licensed Arizona Flare. Used only at the two biggest moments. |
| Interface | **Inter** | Google Fonts, SIL Open Font License | Everything else: headings, body, labels, navigation, buttons. |
| Mono | **Geist Mono** | Google Fonts, SIL Open Font License | Times, counters, tiny data. Never for sentences. |

Arizona Flare is a commercial typeface and is not included. If Claritia licenses it later, it can replace Instrument Serif at the same sizes and tracking without changing the layout. The rest of the system is unaffected.

Fallbacks: Instrument Serif → `Georgia, "Times New Roman", serif`; Inter → `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`; Geist Mono → `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.

### Scale

| Role | Family | Size / line-height | Weight | Tracking | Use |
|---|---|---|---|---|---|
| Display XL | Instrument Serif | 50 / 52 desktop · 40 / 44 mobile | 400 | -2px desktop · -0.8px mobile | Homepage hero only |
| Display L | Instrument Serif | 36 / 40 · 28 / 32 mobile | 400 | -0.02em | Closing CTA, 404 |
| Section H2 | Inter | 36 / 40 · 28 / 32 mobile | 500 | -0.02em | Every section heading |
| Section H3 | Inter | 28 / 32 · 24 / 30 mobile | 500 | -0.02em | Sub-sections |
| Card title | Inter | 16 / 24 | 500 | -0.01em | Bento, pricing, suite |
| Lead | Inter | 18 / 28 · 17 / 26 mobile | 400 | -0.005em | Hero and section intros |
| Body | Inter | 16 / 24 | 400 | 0 | Paragraphs |
| Small | Inter | 14 / 20 | 400 | 0 | Captions, table rows |
| Label | Inter | 14 / 20 | 500 | 0 | Buttons, field labels, nav |
| Micro | Inter | 12 / 16 | 500 | 0.02em | Chips, metadata |
| Micro mono | Geist Mono | 12 / 16 | 400 | 0.02em | Times, counters |
| Metric | Inter | 40 / 44 · 32 / 36 mobile | 500 | -0.03em | Stat bands |

### Rules

- **Serif is a moment, not a habit.** It appears in the hero and the closing statement, and nowhere else on a marketing page. Section headings are always Inter medium.
- **Two-tone headings.** When a heading breaks, the second line is `--text-3`. This is the one consistent editorial flourish. The first line carries the claim; the second carries the consequence.
- **Sentence case everywhere.** No all-caps headings, no title case in body copy.
- **Line length.** Body copy: 60–68 characters. Lead copy: 50–60. Headings: 2–3 lines maximum.
- **No faux weights.** Do not synthesize bold or italic. Use the loaded weights.
- **Numbers.** Use tabular figures (`font-variant-numeric: tabular-nums`) wherever numbers align in a column or change.
- **Mono is data.** Times (`0:15`), counters (`129,971`), scores (`92`) and code. Not labels or sentences.

---

## 5. Grid and layout

### The 24-column grid

| Property | Value |
|---|---|
| Columns | 24 |
| Max content width | 1088px |
| Column gap | 16px |
| Outer margin | 32px desktop · 16px mobile |
| Column width at max | 30px |

The page uses `.wrap` for the 1088px container and `.grid-24` for the column grid. Full-bleed elements break out of the container but keep the same 32px safe margin.

### Rails

Two 1px vertical rules mark the content edges and run from the integration band down through the page. They are `--line` and always 1px, never 2px. They are a layout scaffold, not a border around the page. The hero stays clean, and a full-bleed cream band may interrupt the rail. The 2px emerald section tick sits on the left rail.

### Section rhythm

| Zone | Desktop | Mobile |
|---|---|---|
| Section header top padding | 40px | 32px |
| Header to content | 32px | 24px |
| Between cards | 16px | 12px |
| Section tail | 160px | 120px |
| Hero top padding | 80px | 48px |

The large tail is deliberate. Mintlify's calm comes from the amount of nothing between sections. Do not fill it.

### Spacing scale

Everything is a multiple of 4px: 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80, 104, 120, 160.

Use the token names in code: `--s-1` (4px) through `--s-40` (160px). Never hard-code a one-off margin.

### Breakpoints

| Name | Width | What changes |
|---|---|---|
| Mobile | < 640px | Single column, 16px gutter, stacked nav, 40px hero |
| Small tablet | 640px | Two-column tiles, side-by-side buttons |
| Tablet | 768px | Two-column cards, section header action moves right |
| Desktop | 1024px | 24-column layout, 3-column bento, full nav |
| Wide | 1280px | Max width reached; margins grow |

### The bento

The platform section is a 3-column bento with 16px gaps and 412px row height. The first card spans 2 columns; cards 2–5 are single; the sixth spans all 3. On tablet it becomes 2 columns and the spans reset. On mobile it is one column with the natural height.

The bento is the page's main product argument. Each card holds one related interface fragment (the wide inbound card holds a form and the calendar it opens), 32px padding, a 16px title, and one 14px sentence. No card is a collage.

---

## 6. Components

### Buttons

| Variant | Ground | Text | Border | Use |
|---|---|---|---|---|
| Primary | `#08090A` | `#FFFFFF` | none | One per view; the main action |
| Secondary | `#FEFDFB` | `#08090A` | `1px rgba(0,0,0,.06)` | The alternative action |
| Ghost | transparent | `--text-2` | none | Sign in, quiet navigation |
| Dark secondary | transparent | `#FAF8F5` | `1px rgba(255,255,255,.22)` | On a dark card |

- Height: 40px (36px compact, 48px large).
- Radius: 4px. Never a pill.
- Padding: 16px left, 12px right when an arrow is present; 16px both sides without.
- Type: 14/16, weight 500, no letter-spacing.
- Arrow: 16px, 50% opacity at rest, 100% on hover, shifts 2px right. Duration 150ms.
- Hover: background moves 10% toward its neighbor; no lift, no scale, no shadow.
- Active: no bounce; a 1px inset darkening is enough.
- Focus: 2px `--brand` outline, 2px offset.
- Disabled: 40% opacity, no hover.

Primary buttons are near-black, not pure black, and not green. Green is the signal; black is the action.

### Chips

- Height 28px; padding 3px 10px 3px 4px; radius 4px; 12/16 medium.
- Default: paper fill, 1px `--line-2`, `--text-2`.
- Numeric: `--brand-soft` fill, no border, `--brand` text, mono number with tabular figures.
- No pill chips, no gradients, no icons larger than 12px.

### Cards

- Radius 12px.
- Border 1px `rgba(8,9,10,.07)`.
- Fill `#F9F6F3` (or `#FAF8F5` for quieter cards).
- Padding 32px; internal gap 16px.
- No shadow at rest. A card may lift 1px on hover with a `0 1px 0` line, but do not use a large shadow.
- The only floating surfaces are the hero product preview and the nav dropdown.

### Navigation

- Height 64px, sticky, opaque `--bg`, 1px `--line` bottom border. No blur, no transparency.
- Logo 24px mark + 20px wordmark.
- Links 14/20 medium, `--text-2`, `--ink` on hover; 8px vertical and 10px horizontal padding.
- Product uses a `<details>` dropdown: white panel, 6px radius, 1px border, shadow `0 16px 40px -24px rgba(8,9,10,.28)`, 8px padding.
- Right side: Sign in (ghost) + Start free (primary). "Book a demo" lives in the page, not the bar, on desktop; on mobile it can appear in the panel.
- Mobile: logo + Start free + a menu `<details>` with a full-width paper panel. No JavaScript.

### Inputs

- Height 40px; radius 4px; paper fill; 1px `rgba(8,9,10,.15)` border.
- Padding 0 12px; 16/24 text; placeholder `--text-4`.
- Focus: 2px `--brand` ring, no browser outline.
- Label: 12/16 medium, `--text-2`, 6px above the field.
- Error: `--red` border and 12px message; never color alone.

### Accordions

- A list of `<details>` rows separated by 1px `--line`.
- Summary: 18/28 medium, `--ink`, 20px vertical padding.
- Marker: a 16px plus that rotates 45° when open. No circle, no pill, no filled background.
- Answer: 16/24, `--text-2`, max 64ch, 0 0 20px.
- The first row may be open; never open more than two by default.

### Tables

- Full-width, 1px rules between rows.
- Header: 12/16 medium, `--text-4`, sentence case.
- Row: 14/20, 16px vertical padding.
- The Claritia column uses `--brand` for the value, not a full green row.
- On mobile, stack each row into a two-line block with the label above the value.

### Product previews

- Frame: 12px radius, 1px `--line-2`, `#FEFDFB` fill, shadow `0 24px 48px -24px rgba(8,9,10,.18), 0 8px 16px -12px rgba(8,9,10,.08)` only when floating in the hero.
- Inner UI type: 12–13px; labels 11px; line-height 1.4.
- Use real labels, real names, real times, real values. Never gray bars as placeholders.
- Active state: mint 10% wash with `--brand` text.
- No browser chrome, no laptop frame, no perspective tilt.

### Status

- A 6px dot plus 12/16 label inside a 26px paper chip with a 1px border and 4px radius.
- Green dot = all systems running.
- Do not use a status chip as a button.

### Footer

- 104px top padding, 64px bottom.
- 1px `--line` top border.
- Left: mark + wordmark, one-line description, status chip.
- Right: five columns (Product, Inbound, Suite, Company, Legal), 16px gap, 14/20 links, `--text-3` headings.
- Bottom row: 12/16 `--text-4`, copyright and contact.
- No newsletter form, no social wall, no giant wordmark.

---

## 7. Imagery and illustration

### Line art

The signature image is a bundle of thin mint-to-lime bezier curves that converge and cross, like traffic finding its way. It appears in the hero and the numbers band.

- 24–40 paths in one SVG.
- Stroke 1.15px, no fill, round caps.
- Colors step from `#18E299` through `#58E97F`, `#6DEE6B` to `#A8FB36`, with a few `#2FE688` accents.
- Curves start off-canvas, sweep through the content area, and end off-canvas. They must not cross text.
- Opacity 0.35–0.85; never a solid block.
- Static is the default. A single 700ms fade-in is allowed; no looping particle animation on the marketing page.

### Dot fields

A field of 2px dots in a 16px grid, in `--line-2` or mint at 15% on dark. Used behind a single dark card or as a quiet texture. Never behind body copy.

### Interface fragments

The product is the imagery. Build fragments in HTML/CSS from real content: a form with a known email, a calendar with a booked Thursday, a routing log with a rule number, a workflow with five nodes, an email draft with a source link, a record with a score. Crop the fragment; do not show a whole app window. The fragment must work at its true size and remain legible at 390px.

### Third-party marks

Integration names may be set as plain wordmarks in Inter 600. Do not download or embed third-party logo files without permission. Customer logos, testimonials and case studies may only be used with permission; never invent them.

### Photography

Not used on the current site. If added later: real teams, real offices, natural light, no stock handshakes, no laptop-at-a-café clichés. A photograph must earn its place next to a product fragment.

---

## 8. Motion

Motion confirms an action; it never performs.

| Token | Value | Use |
|---|---|---|
| `--ease-soft` | `cubic-bezier(.22,1,.36,1)` | Default hover, arrow, dropdown |
| `--ease-expo` | `cubic-bezier(.16,1,.3,1)` | Panels, reveals |
| `--ease-strong` | `cubic-bezier(.77,0,.175,1)` | Deliberate in-out moves |
| `--dur-1` | 100ms | Color, border |
| `--dur-2` | 150ms | Arrow, small transforms |
| `--dur-3` | 200ms | Dropdown, focus |
| `--dur-4` | 300ms | Panel open |
| `--dur-5` | 500ms | Image scale, reveal |

Recipes:

- Link or button hover: color and arrow only. 100–150ms.
- Card hover: border darkens to `--line-3`; no lift, no shadow.
- Image hover: scale 1.03 over 500ms, clipped by the card radius.
- Section reveal: 8px rise + fade over 500ms, triggered by `animation-timeline: view()` where supported. Content must be visible without it.
- Line art: fade in once over 700ms. No loop.
- Dropdown: opacity + 4px translate over 200ms.

Reduced motion: remove every transform and animation, keep color changes. The page must read identically with motion off.

---

## 9. Voice and copy

### The voice

Clear, calm, specific. Write like a good operator explaining a process to a peer. Short sentences. Active verbs. Numbers with units. No hype.

### Rules

- Sentence case for headings, labels and buttons.
- Use "you" for the reader and "we" for Claritia. Never "users" when you mean customers.
- Lead with the outcome, then the mechanism: "Book the meeting before they leave your site. Claritia routes the lead and opens the rep's calendar inside the form."
- One idea per sentence. One claim per paragraph.
- Numbers are concrete: "15 minutes", "under 1 second", "2 fields instead of 6".
- Use contractions. Avoid jargon unless the reader already uses it.
- Do not promise what the product does not do. Do not invent statistics, logos or quotes.

### Banned

Revolutionary, seamless, supercharge, game-changing, cutting-edge, next-generation, unlock, empower, leverage (as a verb), "AI-powered" as the main claim, exclamation marks, "Don't miss out".

### CTA labels

| Context | Label |
|---|---|
| Main | Start free |
| Sales | Book a demo |
| Enterprise | Talk to sales |
| Secondary | See pricing |
| Navigation | Sign in |
| Footer | hello@tryclaritia.com |

Buttons are verbs. No "Submit", "Learn more" or "Click here".

---

## 10. Page recipes

### Hero

- 24-column grid; copy in columns 1–9, product preview in 10–24.
- Mint eyebrow chip, serif display XL, 18px lead, primary + secondary buttons, 12/16 note.
- One line-art field behind the preview; it must not touch the headline.
- Preview floats with the large soft shadow and is cropped by the right rail.
- Hero bottom: 80px before the next band.

### Section header

- 2px × 24px emerald tick at the left rail.
- Heading starts at column 2, max 41.5rem.
- Second line in `--text-3`.
- Optional primary button aligned to the bottom-right of the header.
- 40px top, 32px to content.

### Bento

- 3 columns, 16px gaps, 412px rows.
- First card 2 columns; last card 3 columns.
- Each card: fragment, 16px title, 14px one-line description.
- Cards are cream on paper; no shadows.
- On mobile: one column, natural height, 12px gaps.

### Stat band

- Line art at the top, full-bleed within the rails.
- 4 columns separated by 1px rules; 40px numbers; 14px captions.
- Values may be emerald; labels are `--text-2`.
- On mobile: 2 columns, then 1 column under 480px.

### Proof table

- Two columns, 1px rules, no outer border.
- Left column `--text-3`, right column `--ink` with `--brand` values.
- Header row 12px `--text-4`.
- On mobile: stacked pair blocks with the old tool as a 12px label above the Claritia value.

### Pricing

- 4 cards, equal height, 12px radius.
- Recommended card: `#08090A` ground, `#FAF8F5` text, mint flag, dark secondary button.
- Price: 32/36 medium, tabular numbers; yearly line 13/18 `--text-3`.
- Specs: 1px rules, 13/18 rows; CTA pinned to the bottom.
- On mobile: 1 column, recommended card remains dark.

### FAQ

- Heading left, "Talk to us" button right on desktop.
- `<details>` rows with 1px rules.
- First row open; answers 16/24 at 64ch.
- No card around the list.

### Closing CTA

- Full-bleed paper band, 1px top and bottom rules.
- Serif display L, second line muted.
- Primary + dark secondary buttons.
- Line art on the right, clipped, never behind text.
- 96px vertical padding desktop / 64px mobile.

### Footer

- As specified in components. Five columns; no newsletter; no oversized logo.
- The status dot is the only green element in the footer.

---

## 11. Accessibility

- Body text is at least 16px; line-height at least 1.5.
- Text contrast: 4.5:1 minimum for body, 3:1 for large text and UI boundaries. See the contrast table.
- Do not use color alone for status. Pair a dot with a label, an error with a message.
- Focus: visible 2px emerald ring, 2px offset, on every interactive element. Never `outline: none` without a replacement.
- Tap targets: 40px minimum, 8px apart.
- Every icon has an accessible name or is `aria-hidden`.
- The mobile menu, product dropdown and FAQ use native `<details>` so they work with keyboard and without JavaScript.
- Skip link to `#main` on every page.
- Respect `prefers-reduced-motion`.
- Headings run in order: one `h1`, then `h2` per section, `h3` inside cards.
- Decorative line art and dot fields are `aria-hidden="true"`.
- Forms have labels, not just placeholders; the try-it form uses a real `<label>`.

---

## 12. CSS usage

Link the token layer before the base stylesheet:

```html
<link rel="stylesheet" href="/assets/tokens.css?v=5">
<link rel="stylesheet" href="/assets/base.css?v=5">
<link rel="stylesheet" href="/assets/home.css?v=5">
```

- `assets/tokens.css` is the only place raw colors, type sizes, spacing, radii, shadows and easings are defined.
- `assets/base.css` contains the reset, typography, layout primitives, header, footer, buttons, chips, forms and utility classes.
- `assets/home.css` contains only homepage sections.
- No component may introduce a raw hex value. Use a token.
- The site is plain HTML and CSS. No build step, no JavaScript, no framework.
- The base font size is 16px. Use `rem` for type and `px` for borders, radii and small gaps where it aids precision.
- Class naming is BEM-ish for shared components (`.site-head__in`, `.btn--primary`) and plain for page sections (`.hero`, `.bento`, `.tier`).

### Inactive dark block

`assets/tokens.css` includes a commented/`[data-theme="dark"]` block with the dark values. It is not triggered by `prefers-color-scheme`; the site stays light until the dark build is audited.

---

## 13. Do and don't

**Do**

- Use paper, ink and one emerald signal.
- Let the product fragments carry the proof.
- Keep headings to two tones and two or three lines.
- Use 4px radii for controls and 12px for cards.
- Leave 160px between sections.
- Set real numbers, real times and real labels.
- Write one clear sentence per card.
- Check the page at 390px before calling it done.

**Don't**

- Don't use pill buttons, clay, lilac, butter or the old warm-paper palette.
- Don't use the serif for section headings, buttons or body copy.
- Don't use mint text on cream.
- Don't add a gradient, glow, glass panel or heavy shadow.
- Don't fill a card with gray placeholder bars or a fake dashboard collage.
- Don't invent customers, quotes, logos or live metrics.
- Don't add JavaScript for a menu, carousel or form reveal.
- Don't copy Mintlify's copy, screenshots, logo or font files.

---

## 14. Source notes

- Reference: `https://www.mintlify.com/`, fetched 26 October 2026. Two CSS bundles and full-page desktop/mobile renders were inspected.
- Extracted values: 24-column 1088px grid, 16px gap, 32px margin; type sizes 50/52, 36/40, 28/32, 16/24, 14/20, 12/16; 4px button radius, 12px card radius; palette `#FEFDFB`, `#FAF8F5`, `#F9F6F3`, `#08090A`, `#121715`, `#485450`, `#717D79`, `#969E9B`, `#F1F0EE`, `#0C8C5E`, `#18E299`, `#A8FB36`. The muted text roles were darkened to `#5F6B67` and `#69736E`, and the text-safe green to `#0A7A52`, so every small text style clears 4.5:1; the mark keeps `#0C8C5E`.
- The display face on the reference is Arizona Flare (licensed). Claritia uses Instrument Serif as the free stand-in. No font binaries were copied.
- No Mintlify copy, imagery, logo paths or stylesheet files are included in this repository. The design language is re-expressed as Claritia's own system.
