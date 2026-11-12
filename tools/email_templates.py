"""Builds the email template gallery: /email-templates and one page per template, each with the email itself at
/email-templates/<slug>/email.html for the preview frames.

The templates come from the app (dev-arrowsterr/claritia, src/lib/design/email/library.ts). Refresh the data there with
  node scripts/export-email-templates.ts > ../claritia-site/tools/email-templates.json
then run here:
  python3 tools/email_templates.py
"""
import html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shell  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "email-templates.json").read_text())
SITE = "https://tryclaritia.com"
APP = "https://app.tryclaritia.com"
T = DATA["templates"]
FOLDERS = DATA["folders"]
esc = lambda s: html.escape(str(s), quote=True)

STYLE = """<style>
.et-hero{padding:64px 0 32px}.et-hero .lead{max-width:560px}
.et-folders{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.et-sec{padding:28px 0}.et-sec h2{font-size:22px;font-weight:500;letter-spacing:-.02em;margin:0 0 4px}.et-sec>.wrap>p{color:var(--body);margin:0 0 18px}
.et-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}
.et-card{display:flex;flex-direction:column;gap:10px;color:inherit;text-decoration:none}
.et-thumb{position:relative;height:290px;overflow:hidden;border-radius:12px;background:var(--surface);box-shadow:var(--sh-rest,0 0 0 1px rgba(0,0,0,.06));transition:transform .15s ease,box-shadow .15s ease}
.et-card:hover .et-thumb{transform:translateY(-2px)}
.et-thumb iframe{position:absolute;top:0;left:50%;width:640px;height:820px;border:0;transform:translateX(-50%) scale(.36);transform-origin:top center;pointer-events:none;background:#fff}
.et-card b{font-weight:500;color:var(--ink);font-size:15px}.et-card span{color:var(--body);font-size:14px;line-height:1.4}
.et-page{padding:8px 0 64px}.et-page .wrap{display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start}
.et-main{flex:999 1 560px;min-width:0}.et-side{flex:1 1 280px;min-width:0;display:flex;flex-direction:column;gap:16px}
.et-frame{width:100%;height:900px;border:0;border-radius:16px;background:var(--surface);box-shadow:var(--sh-rest,0 0 0 1px rgba(0,0,0,.06))}
.et-box{background:var(--surface);border-radius:12px;padding:16px 18px;box-shadow:var(--sh-rest,0 0 0 1px rgba(0,0,0,.06))}
.et-box h2{font-size:14px;font-weight:500;margin:0 0 8px;color:var(--meta)}.et-box p{margin:0;color:var(--ink);font-size:14.5px;line-height:1.5}
.et-box ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:8px}.et-box li a{color:var(--ink);font-size:14.5px}
@media (max-width:640px){.et-frame{height:720px}}
</style>
"""


def page(path: str, title: str, desc: str, body: str, ld: list) -> None:
    extra = '<link rel="stylesheet" href="/assets/forms.css?v=12">\n' + STYLE + "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    out = shell.head(title, desc, path, extra) + "\n" + shell.body(body)
    dest = ROOT / path.strip("/") / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out)


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}{p}"} for i, (n, p) in enumerate(items)]}


def card(t) -> str:
    return f"""<a class="et-card" href="/email-templates/{t['slug']}"><span class="et-thumb"><iframe title="" aria-hidden="true" tabindex="-1" loading="lazy" src="/email-templates/{t['slug']}/email.html"></iframe></span><b>{esc(t['name'])}</b><span>{esc(t['blurb'])}</span></a>"""


def index_page():
    chips = "".join(f'<a class="tag tag--link" href="#{f["slug"]}">{esc(f["name"])}</a>' for f in FOLDERS)
    secs = []
    for f in FOLDERS:
        items = [t for t in T if t["group"] == f["name"]]
        secs.append(f"""<section class="et-sec" id="{f['slug']}"><div class="wrap"><h2>{esc(f['name'])}</h2><p>{len(items)} templates</p><div class="et-grid">{''.join(card(t) for t in items)}</div></div></section>""")
    body = f"""<section class="et-hero">
    <div class="wrap">
      <h1 class="h2">Email templates</h1>
      <p class="lead">{len(T)} free email templates for newsletters, events, welcomes, follow-ups, meetings and more. Each one arrives in your brand, and Tia can fill it in for you.</p>
      <div class="et-folders">{chips}</div>
    </div>
  </section>
  {''.join(secs)}"""
    ld = [crumbs([("Email templates", "/email-templates")]), {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Email templates", "url": f"{SITE}/email-templates"}]
    page("/email-templates", "Free email templates | Claritia", f"{len(T)} free email templates for newsletters, events, welcomes, follow-ups and meetings, in your brand.", body, ld)


def template_page(t):
    path = f"/email-templates/{t['slug']}"
    folder = next(f for f in FOLDERS if f["name"] == t["group"])
    use = f"{APP}/emails/templates?use={t['slug']}"
    related = [x for x in T if x["group"] == t["group"] and x["key"] != t["key"]][:8]
    nm = t["name"]
    title_h = nm if nm.lower().endswith("template") else f"{nm} email template"
    body = f"""<section class="thero thero--tpl">
    <div class="wrap">
      <nav class="tcrumb" aria-label="Breadcrumb"><a href="/email-templates">Email templates</a><span aria-hidden="true">/</span><a href="/email-templates#{folder['slug']}">{esc(t['group'])}</a><span aria-hidden="true">/</span><span>{esc(nm)}</span></nav>
      <div class="tpl__top">
        <div class="tpl__copy">
          <h1 class="h2">{esc(title_h)}</h1>
          <p class="lead">{esc(t['blurb'])} It arrives in your brand's colors and fonts, and Tia can write it for you from one sentence.</p>
          <div class="tpl__tags"><span class="tag tag--sig">Free</span><a class="tag tag--link" href="/email-templates#{folder['slug']}">{esc(t['group'])}</a></div>
        </div>
        <div class="tpl__ctas"><a class="btn btn--primary btn--lg" href="{use}">Use this template <span class="nudge" aria-hidden="true">&rarr;</span></a></div>
      </div>
    </div>
  </section>
  <section class="et-page">
    <div class="wrap">
      <div class="et-main"><iframe class="et-frame" title="{esc(nm)} preview" loading="lazy" src="/email-templates/{t['slug']}/email.html"></iframe></div>
      <aside class="et-side">
        <div class="et-box"><h2>Preview text</h2><p>{esc(t['preheader'] or 'Set your own.')}</p></div>
        <div class="et-box"><h2>What you can change</h2><p>Every word, block and color. Send it as a one-off campaign or as an email in an automation, and see the meetings and forms it leads to.</p></div>
        <div class="et-box"><h2>More in {esc(t['group'])}</h2><ul>{''.join(f'<li><a href="/email-templates/{x["slug"]}">{esc(x["name"])}</a></li>' for x in related)}</ul></div>
      </aside>
    </div>
  </section>"""
    ld = [crumbs([("Email templates", "/email-templates"), (t["group"], f"/email-templates#{folder['slug']}"), (nm, path)])]
    page(path, f"{title_h} (free) | Claritia", f"{t['blurb']} A free email template in your brand.", body, ld)
    # The email itself, for the preview frames: never indexed.
    email = re.sub(r"<head>", '<head><meta name="robots" content="noindex">', t["html"], count=1)
    (ROOT / path.strip("/") / "email.html").write_text(email)


def sitemap():
    sm = ROOT / "sitemap.xml"
    text = sm.read_text()
    text = re.sub(r"\s*<!-- email-templates:start -->.*?<!-- email-templates:end -->", "", text, flags=re.S)
    urls = ["/email-templates"] + [f"/email-templates/{t['slug']}" for t in T]
    lines = "\n".join(f"  <url><loc>{SITE}{u}</loc></url>" for u in urls)
    text = text.replace("</urlset>", f"  <!-- email-templates:start -->\n{lines}\n  <!-- email-templates:end -->\n</urlset>")
    sm.write_text(text)


if __name__ == "__main__":
    slugs = [t["slug"] for t in T]
    assert len(set(slugs)) == len(slugs), "template slugs repeat"
    index_page()
    for t in T:
        template_page(t)
    sitemap()
    print(f"wrote /email-templates and {len(T)} template pages")
