# tryclaritia.com

Static site for Claritia. Plain HTML, CSS and a little JavaScript: no WordPress, no build step, no library.
Push to `main` and Hostinger deploys it.

The home page shows the product: forms, meetings, workflows and routing, a sample of the app, the tools it connects,
form templates, pricing and questions. The look is calm and light (`BRAND.md`).

## How it's laid out

| Path | What |
|---|---|
| `index.html` | The home page: hero with the prompt, why, how it works, compare, tools, integrations, templates, numbers, pricing, questions and the last prompt. It also holds the header, phone menu and footer every page shares. |
| `404.html`, `privacy/`, `terms/` | Page not found and the legal pages. Written by `tools/legal.py`. |
| `assets/site.css` | Tokens, type, buttons, chips, tags, the header, phone menu, footer, and every home section. |
| `assets/site.js` | Menus, the phone menu, scroll reveals and the pricing switch. |
| `assets/home.js` | Home only: the blinking tiles, prompt suggestions, the How it works steps and the Compare switch. |
| `assets/logos/` | Logos of the tools Claritia works with. |
| `assets/brand/` | Mark, favicon, Apple touch icon and the share image (`og-image.png`). |
| `tools/shell.py` | Copies the sprite, header, phone menu and footer out of `index.html` and writes the shared `<head>`. |
| `templates/` | The form template gallery: `/templates`, list pages and one page per template, each with the form to try. Written by `tools/templates.py`. |
| `tools/templates.py`, `tools/templates.json` | Writes `templates/` and its lines in `sitemap.xml` from the template data, which comes from the app (`node scripts/export-templates.ts` in `dev-arrowsterr/claritia`). |
| `assets/forms.css`, `assets/forms.js` | The gallery's search and filters, the style menu and Shuffle, and the live forms: pages, show-if logic, checks and the end screen. |
| `assets/themes.css`, `assets/form-art/` | The 18 form styles and their drawings. Written by `tools/templates.py` from the app's `src/lib/forms/themes.ts`. |
| `llms.txt`, `pricing.md` | Short guides for AI tools. |
| `.htaccess` | https and www redirects, the 404 page, app links, cache times. |

## Editing

- **Words on the home page:** edit `index.html`.
- **The header, phone menu or footer:** edit them in `index.html`, then run `python3 tools/templates.py && python3 tools/legal.py`
  so every page gets them.
- **CSS or JS:** edit the file, then raise `?v=` on its link in `index.html` and `SITE_CSS_V` or `SITE_JS_V` in
  `tools/shell.py`, and run the two tools above.
- **Form templates:** templates are written in the app repo. To refresh the site, run
  `node scripts/export-templates.ts > ../claritia-site/tools/templates.json` there, then `python3 tools/templates.py` here.
  Don't edit `templates/` by hand. For `forms.css` or `forms.js`, raise `CSS_V` or `JS_V` in `tools/templates.py`.
- **Prices:** the plans in `index.html` and `pricing.md` follow `docs/pricing.md` in the app repo.

Preview locally: `python3 -m http.server 8000`, then open http://localhost:8000.

## Running cost

$0 added at Beta (50 teams) and at Growth (500 teams). The site is static on the existing Hostinger plan, and so are
the 700 gallery pages.
Fonts come from Google Fonts for free. No new paid service.
