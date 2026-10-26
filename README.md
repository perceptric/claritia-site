# tryclaritia.com

Static site for Claritia. Plain HTML and CSS: no WordPress, no build step, no JavaScript. The
product menus, the accordions, the price table and the try-it form are CSS and HTML only.
It is set up the same way as perceptric.com.

The home page describes Claritia, the CRM and inbound stack for small B2B teams: it catches every
lead on your site, finds out who they are, sends them to the right rep and books the meeting. The
product plan lives in the app repo at `docs/unify-plan.md` and `docs/inbound.md`.

## How it's laid out

| Path | What |
|---|---|
| `index.html` | The home page. |
| `404.html` | The "page not found" page. Its own styles sit in a `<style>` block at the top. |
| `assets/base.css` | Tokens, reset, buttons, header and footer. |
| `assets/home.css` | The home page sections and the product pictures (the `.mk-` pieces). |
| `assets/brand/` | Favicon, icon, Apple touch icon and the share image (`og-image.png`). |
| `llms.txt` | A short guide to Claritia for AI tools. |
| `pricing.md` | The plans as a Markdown table. |
| `robots.txt`, `sitemap.xml` | For search engines. |
| `.htaccess` | https and www redirects, the 404 page, text file types, app links, cache times. |

## Editing

- **Home page words:** `index.html`. Each section starts with a comment, like `<!-- 15. Pricing -->`.
  The order is the homepage copy: hero, logo strip, how it works, the six sections (Inbound,
  Scheduling, Routing, Automation, Nurture, CRM), try it, numbers, replace the pile, the suite,
  pricing, FAQ, closing card.
- **Home page look:** `assets/home.css`. Tokens and shared pieces are in `assets/base.css`.
  The product pictures are the `.mk-` classes in `home.css` and mirror the app. The page font size
  is 14px, so `1rem` is 14px. Breakpoints are 640px, 880px, 940px and 1000px.
- **Header and footer:** they sit in both `index.html` and `404.html`. Change both.
  With two pages there is no partials folder or layout script.
- **Prices and plan limits:** the cards in the `<!-- 15. Pricing -->` section of `index.html` and the
  table in `pricing.md`. Change both together, and keep them in step with `docs/pricing.md` in the app.
- **/llms.txt:** edit `llms.txt`. Keep it in step with the app's `/llms.txt`.
- **Footer year:** typed into the footer of both pages. Change it in January.
- **New page:** make a folder with an `index.html` (copy `404.html` to start, since it has the header
  and footer). Give it a title, description and canonical tag, drop the `noindex` line, and add it to
  `sitemap.xml`.

Follow `docs/brand.md` in the app repo: a warm paper background, Geist for every word, black pill
buttons, soft round cards (16px to 24px, 32px for the page panel), and calm motion. Headlines are
two tones, the line after the break in gray. The sparkle marks AI. Cards sit flat and lift on hover.
Take direction from `default.com` and the brand's modules; never copy another company's files,
images or copy.

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
`.htaccess` also hides the `.git` folder, dot files and this README, since Hostinger deploys the whole repo.

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
