# tryclaritia.com

Static site for Claritia. Plain HTML and CSS: no WordPress, no build step, no JavaScript. The
product menus, the accordions, the price table and the try-it form are CSS and HTML only.
It is set up the same way as perceptric.com.

The home page describes Claritia, the CRM and inbound stack for small B2B teams: it catches every
lead on your site, finds out who they are, sends them to the right rep and books the meeting. The
product plan lives in the app repo at `docs/unify-plan.md` and `docs/inbound.md`.

The visual system is a warm-paper, emerald-and-mint language with Instrument Serif at the two
biggest moments and Inter everywhere else. It is documented in full in `BRAND.md`; the values
live in `assets/tokens.css`. The reference is Mintlify's marketing site, but the copy, mark,
imagery and font files are Claritia's own.

## How it's laid out

| Path | What |
|---|---|
| `index.html` | The home page. |
| `404.html` | The "page not found" page. It uses the shared tokens and base styles, plus a small `<style>` block for the centred layout. |
| `BRAND.md` | The complete brand guide: logo, color, type, grid, components, imagery, motion, voice, accessibility and CSS usage. Hidden from the web by `.htaccess`. |
| `assets/tokens.css` | Raw palette, semantic color, type scale, spacing, radii, shadows, motion and layout tokens. The only file with raw values. |
| `assets/base.css` | Reset, typography, layout primitives, header, footer, buttons, chips and forms. |
| `assets/home.css` | The home page sections and the product fragments (the `.mini-*`, `.app-preview`, `.bento` pieces). |
| `assets/brand/` | Mark SVG, favicon, Apple touch icon and the share image (`og-image.png`). |
| `llms.txt` | A short guide to Claritia for AI tools. |
| `pricing.md` | The plans as a Markdown table. |
| `robots.txt`, `sitemap.xml` | For search engines. |
| `.htaccess` | https and www redirects, the 404 page, text file types, app links, cache times. |

## Editing

- **Home page words:** `index.html`. Each section starts with a comment, like `<!-- 9. Pricing -->`.
  The order is: hero, integrations and facts, platform bento, how it works, try it, numbers,
  replace the pile, suite, pricing, FAQ, closing. The bento cards carry ids (`#inbound`,
  `#scheduling`, `#routing`, `#automation`, `#nurture`, `#crm`) so the header and footer can link
  straight to a capability.
- **Home page look:** `assets/home.css`. Tokens and shared pieces are in `assets/tokens.css` and
  `assets/base.css`. The product pictures are the `.mini-*` and `.app-preview` classes in
  `home.css` and mirror the app. The page font size is 16px, so `1rem` is 16px. Breakpoints are
  640px, 768px, 900px, 1000px and 1024px.
- **Header and footer:** they sit in both `index.html` and `404.html`. Change both.
  With two pages there is no partials folder or layout script.
- **Brand rules:** follow `BRAND.md`. Do not introduce a raw hex value in a section stylesheet:
  add it to `assets/tokens.css` first. Buttons are 4px radius and 40px tall, cards are 12px,
  the grid is 24 columns inside 1088px, and the section tail is 160px desktop / 120px mobile.
  The old warm-paper, clay, pill-button system is gone; do not bring it back.
- **Prices and plan limits:** the cards in the `<!-- 9. Pricing -->` section of `index.html` and the
  table in `pricing.md`. Change both together, and keep them in step with `docs/pricing.md` in the app.
- **/llms.txt:** edit `llms.txt`. Keep it in step with the app's `/llms.txt`.
- **Footer year:** typed into the footer of both pages. Change it in January.
- **Brand assets:** `assets/brand/claritia-mark.svg` is the source for the favicon and Apple icon.
  Regenerate the PNG/ICO files from the mark when it changes. The share image is a 1200x630 render
  and should be updated when the hero headline changes.
- **New page:** make a folder with an `index.html` (copy `404.html` to start, since it has the header
  and footer). Give it a title, description and canonical tag, drop the `noindex` line, add it to
  `sitemap.xml`, and link `tokens.css`, `base.css` and any page stylesheet.

The brand is light-only for now. Dark tokens are documented in `BRAND.md` and reserved in
`tokens.css` under `[data-theme="dark"]`, but the site does not switch with the OS.

Preview locally: `python3 -m http.server 8000`, then open http://localhost:8000.
The local server ignores `.htaccess`, so redirects and the 404 page only work on Hostinger.

Push to `main` and Hostinger deploys it.

## Paths with no page of their own

| Path | What it does |
|---|---|
| `/llms.txt` | A real file, served as `text/plain; charset=utf-8`. |
| `/pricing.md` | A real file, served as `text/markdown; charset=utf-8`. |
| `/visitors`, `/accounts`, `/contacts`, `/segments`, `/journeys`, `/pages`, `/reports` and the other app paths | A 301 redirect to the same path on app.tryclaritia.com. The query string comes along. |
| Anything else | The 404 page. |

The app paths are listed in `.htaccess`. Add a path there when the app gets a new top-level page.
`.htaccess` also hides the `.git` folder, dot files, this README and `BRAND.md`, since Hostinger
deploys the whole repo.

## Hostinger setup

1. **Add the site.** In hPanel, go to Websites → Add website and pick tryclaritia.com.
   Choose an empty website, with no WordPress and no builder.
2. **Connect this repo.** In hPanel, open the site, then Advanced → Git.
   - Repository: this repo's GitHub address. For a private repo, add the deploy key hPanel shows to the repo
     (GitHub → Settings → Deploy keys).
   - Branch: `main`.
   - Install path: leave it empty, so the site lands in the domain's `public_html`. The folder must be empty.
   - Create, then press Deploy. Turn on auto deployment and add the webhook URL hPanel gives you to the
     GitHub repo (Settings → Webhooks), so each push to `main` deploys.
3. **Turn on SSL.** In hPanel, check that the free SSL certificate covers `tryclaritia.com` and `www.tryclaritia.com`.
   The https redirect in `.htaccess` needs it.
4. **Check.** Open `/`, `/llms.txt`, `/pricing.md`, `/nope` (it should show the 404 page) and `/contacts?x=1`
   (it should land on `app.tryclaritia.com/contacts?x=1`). Also try `http://` and `www.`: both should end on
   `https://tryclaritia.com/`. If you see an old page, purge the cache in hPanel (Performance → Cache Manager).

## DNS

The DNS for tryclaritia.com is managed in Hostinger (hPanel → Domains → tryclaritia.com → DNS).

- `tryclaritia.com` and `www.tryclaritia.com` point to Hostinger (an A record for `@` and a CNAME for `www`).
- `app.tryclaritia.com` is a CNAME to `claritia-web.fly.dev` (the app on Fly.io). Leave it as it is.
- Leave the Resend records for the test inboxes (`inbox.tryclaritia.com`) as they are.

Once `tryclaritia.com` points here, visits to it never reach the app, so the app needs no change.
The app keeps its own copy of `/llms.txt` and `/pricing.md` on app.tryclaritia.com.

## Running cost

| Item | Note |
|---|---|
| Hostinger hosting | $0 extra, on the existing Hostinger plan |
| Google Fonts, no tracking, no paid add-ons | $0 |
| Total added to the monthly bill | $0 |

The site makes no AI calls.

## Brand source note

The design language was extracted from the live Mintlify marketing site on 26 October 2026:
its 24-column 1088px grid, serif/Inter type scale, 4px controls, 12px cards, warm paper palette
and emerald/mint accent. No Mintlify copy, logo, image, font binary or stylesheet is included.
The display face on the reference is licensed Arizona Flare; this site uses Instrument Serif as
the free stand-in. See `BRAND.md` §14 for the detailed source notes.
