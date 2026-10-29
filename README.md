# tryclaritia.com

Static site for Claritia. Plain HTML, CSS and a little JavaScript: no WordPress, no build step, no library.
Push to `main` and Hostinger deploys it.

The home page tells one story: Dana Lee from Acme visits Lumen's pricing page (Lumen is a Claritia customer).
Claritia names her company, fills the form for her, scores and qualifies her, routes her to Sam and books the
meeting, all in about twenty seconds. The look is the same family as tryomniscient.com (`BRAND.md`).

## How it's laid out

| Path | What |
|---|---|
| `index.html` | The home page: hero, tools strip, product tour, the nine tools, AI, try it, keep your stack, reliability, the suite, pricing, questions, closing band. |
| `404.html` | Page not found. |
| `assets/site.css` | Tokens, type, buttons, tags, header, phone menu, footer and every home section except the tour. |
| `assets/tour.css`, `assets/tour.js` | The product tour (Capture, Qualify, Route, Book), played on a clock with tabs and controls. Same engine as tryomniscient.com. |
| `assets/site.js` | Menus, phone menu, header line on scroll, scroll reveals, the pricing switch and Try it. |
| `assets/img/feat-*.svg` | The nine animated product drawings. |
| `assets/logos/` | Logos of the tools Claritia works with. |
| `assets/brand/` | Mark, favicon, Apple touch icon and the share image (`og-image.png`). |
| `tools/hero.py` | Writes the hero picture (the Catch) into `index.html`. |
| `tools/tour.py` | Writes the product tour into `index.html`. Run after `tools/hero.py`. |
| `tools/feats.py` | Writes `assets/img/feat-*.svg`. |
| `llms.txt`, `pricing.md` | Short guides for AI tools. |
| `.htaccess` | https and www redirects, the 404 page, app links, cache times. |

## Editing

- **Words outside the tour:** edit `index.html`.
- **The tour or the hero picture:** edit `tools/tour.py` or `tools/hero.py`, then run
  `python3 tools/hero.py && python3 tools/tour.py`. Don't edit between the `tour:` and `catch:` marks by hand.
- **CSS or JS:** edit the file, then raise `?v=` on its link in `index.html` and `404.html`.
- **Prices:** the plans in `index.html` and `pricing.md` follow `docs/pricing.md` in the app repo.

Preview locally: `python3 -m http.server 8000`, then open http://localhost:8000.

## Running cost

$0 added at Beta (50 teams) and at Growth (500 teams). The site is static on the existing Hostinger plan.
Fonts come from Google Fonts for free. No new paid service.
