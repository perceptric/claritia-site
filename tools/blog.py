"""Builds the blog: /blog and one page per post at /blog/<slug>, each with its cover drawn from tools/blog-cover.html.

A post is a Markdown file in blog/posts/<slug>.md that starts with a few lines between --- marks:

    ---
    title: How to route demo requests to the right rep
    description: One or two sentences for search results and link previews.
    category: Routing
    kind: meeting            # the cover's scene: form, meeting, workflow, integration or check
    date: 2026-11-06
    author: Vincent Nguyen
    logo: /assets/logos/hubspot.svg   # integration covers only
    name: HubSpot                     # integration covers only
    ---

Then the post in plain Markdown: ## headings, paragraphs, - and 1. lists, **bold**, *italic*, [links](...), `code`,
> quotes and ![pictures](...). Run: python3 tools/blog.py (it draws a cover only when the post's cover lines change)."""
import datetime, hashlib, html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shell  # noqa: E402
import products as px  # noqa: E402

esc, I, frame = px.esc, px.I, px.frame
SITE = shell.SITE
BLOG_V = 1
POSTS = ROOT / "blog" / "posts"


# Markdown, the small part posts use ------------------------------------------------------------------------------

def inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img src="\2" alt="\1" loading="lazy">', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    return t


def md(text: str):
    """The post's HTML and its headings (for the contents list)."""
    out, heads, para, lst = [], [], [], None

    def flush():
        nonlocal para, lst
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []
        if lst:
            tag, items = lst
            out.append(f"<{tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{tag}>")
            lst = None

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush(); continue
        m = re.match(r"^(#{2,4})\s+(.*)$", line)
        if m:
            flush()
            level, words = len(m.group(1)), m.group(2).strip()
            hid = re.sub(r"[^a-z0-9]+", "-", words.lower()).strip("-")
            if level == 2:
                heads.append((hid, words))
            out.append(f'<h{level} id="{hid}">{inline(words)}</h{level}>')
            continue
        m = re.match(r"^\s*(?:[-*]|(\d+)\.)\s+(.*)$", line)
        if m:
            if para:
                flush()
            tag = "ol" if m.group(1) else "ul"
            if not lst or lst[0] != tag:
                flush(); lst = (tag, [])
            lst[1].append(m.group(2)); continue
        if line.startswith(">"):
            flush(); out.append(f"<blockquote><p>{inline(line.lstrip('> ').strip())}</p></blockquote>"); continue
        if lst:
            flush()
        para.append(line.strip())
    flush()
    return "\n".join(out), heads


def read(path: pathlib.Path) -> dict:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"{path.name}: start with --- lines (title, description, category, kind, date)")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = re.sub(r"\s+#.*$", "", v).strip().strip('"')
    for need in ("title", "description", "date"):
        if not meta.get(need):
            raise SystemExit(f"{path.name}: needs a {need}")
    body, heads = md(m.group(2))
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return {**meta, "slug": path.stem, "body": body, "heads": heads, "minutes": max(1, round(words / 230)),
            "category": meta.get("category", "Guides"), "kind": meta.get("kind", "check"),
            "day": datetime.date.fromisoformat(meta["date"])}


# Covers ----------------------------------------------------------------------------------------------------------

def cover(p: dict) -> str:
    """Draws the post's cover when its lines changed; answers its address."""
    data = {k: p[k] for k in ("title", "category", "kind", "logo", "name") if p.get(k)}
    key = hashlib.sha1((json.dumps(data, sort_keys=True) + (ROOT / "tools" / "blog-cover.html").read_text()).encode()).hexdigest()[:10]
    folder = ROOT / "blog" / p["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    png, stamp = folder / "cover.png", folder / ".cover"
    if not png.exists() or not stamp.exists() or stamp.read_text() != key:
        subprocess.run(["node", str(ROOT / "tools" / "blog-cover.mjs"), json.dumps(data), str(png)], check=True)
        stamp.write_text(key)
    return f"/blog/{p['slug']}/cover.png?v={key}"


# Pages -----------------------------------------------------------------------------------------------------------

def page(path, title, desc, main, og_image=None, og_type="website", extra_ld=""):
    extra = f'<link rel="stylesheet" href="/assets/products.css?v={px.PX_V}">\n<link rel="stylesheet" href="/assets/blog.css?v={BLOG_V}">\n' + extra_ld
    return shell.head(title, desc, path, extra, og_image=og_image, og_type=og_type) + "\n" + shell.body(main)


def when(d: datetime.date) -> str:
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def card(p: dict, big=False) -> str:
    return (f'<a class="bl-card{" bl-card--big" if big else ""}" href="/blog/{p["slug"]}">'
            f'<span class="bl-card__img"><img src="{p["cover"]}" alt="" width="1200" height="630" loading="lazy"></span>'
            f'<span class="bl-card__t"><span class="bl-meta"><b>{esc(p["category"])}</b>{esc(when(p["day"]))}</span>'
            f'<b class="bl-card__h">{esc(p["title"])}</b>' + (f'<span class="bl-card__d">{esc(p["description"])}</span>' if big else "") + "</span></a>")


def index(posts: list) -> str:
    head = f"""    <section class="pd-hero bl-hero" aria-labelledby="bl-h">
      <span class="eyebrow">{I("type", "i s12")}Blog</span>
      <h1 id="bl-h">Notes on forms, booking and follow-up</h1>
      <p class="sub">How small teams turn visitors into booked meetings, from the people who build Claritia.</p>
    </section>"""
    if posts:
        cats = sorted({p["category"] for p in posts})
        chips = "".join(f'<button type="button" data-bl-cat="{esc(c)}">{esc(c)}</button>' for c in cats)
        grid = f"""    <div class="bl-list">
      {card(posts[0], big=True)}
      {'<div class="bl-chips" role="group" aria-label="Topics"><button type="button" data-bl-cat="" aria-pressed="true">All</button>' + chips + '</div>' if len(cats) > 1 else ''}
      <div class="bl-grid">{"".join(card(p) for p in posts[1:])}</div>
    </div>"""
    else:
        grid = f"""    <div class="bl-empty">
      <p>The first posts are on the way.</p>
      <div class="pd-ctas"><a class="btn btn--primary btn--lg" href="/templates">Browse form templates {I("arrow", "i s14 arr")}</a><a class="btn btn--ghost btn--lg" href="/integrations">See integrations</a></div>
    </div>"""
    script = """<script>(function(){var b=document.querySelectorAll('[data-bl-cat]');b.forEach(function(x){x.addEventListener('click',function(){var c=x.getAttribute('data-bl-cat');b.forEach(function(y){y.setAttribute('aria-pressed',y===x?'true':'false')});document.querySelectorAll('.bl-grid .bl-card').forEach(function(k){k.hidden=!!c&&k.querySelector('.bl-meta b').textContent!==c})})})})();</script>"""
    main = frame(head) + frame(grid) + px.cta() + (script if posts else "")
    return page("/blog", "Blog · Claritia", "Notes on forms, booking and follow-up for small teams, from the people who build Claritia.", main)


def post_page(p: dict, others: list) -> str:
    toc = "".join(f'<a href="#{h}">{esc(t)}</a>' for h, t in p["heads"])
    by = f'<span>{esc(p["author"])}</span>' if p.get("author") else ""
    related = "".join(card(o) for o in others[:3])
    main = frame(f"""    <article class="bl-post">
      <nav class="bl-crumb" aria-label="Breadcrumb"><a href="/blog">Blog</a>{I("chev-r")}<span>{esc(p["category"])}</span></nav>
      <h1>{esc(p["title"])}</h1>
      <p class="bl-lead">{esc(p["description"])}</p>
      <div class="bl-by">{by}<time datetime="{p["day"].isoformat()}">{esc(when(p["day"]))}</time><span>{p["minutes"]} min read</span></div>
      <img class="bl-cover" src="{p["cover"]}" alt="" width="1200" height="630">
      <div class="bl-body-wrap">
        {f'<aside class="bl-toc" aria-label="On this page"><b>On this page</b>{toc}</aside>' if len(p["heads"]) > 1 else ""}
        <div class="bl-body">{p["body"]}</div>
      </div>
    </article>""") + (frame(f"""    <section class="bl-more" aria-labelledby="more-h"><h2 id="more-h">More from the blog</h2><div class="bl-grid">{related}</div></section>""") if related else "") + px.cta()
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"],
          "datePublished": p["day"].isoformat(), "image": SITE + p["cover"].split("?")[0], "mainEntityOfPage": f"{SITE}/blog/{p['slug']}",
          "author": {"@type": "Person", "name": p.get("author", "Claritia")}, "publisher": {"@type": "Organization", "name": "Claritia", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/brand/claritia-app-icon.png"}}}
    lds = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"
    return page(f"/blog/{p['slug']}", f"{p['title']} · Claritia", p["description"], main, og_image=SITE + p["cover"].split("?")[0], og_type="article", extra_ld=lds)


def sitemap(posts: list):
    sm = ROOT / "sitemap.xml"
    text = re.sub(r"\s*<!-- blog:start -->.*?<!-- blog:end -->", "", sm.read_text(), flags=re.S)
    today = datetime.date.today().isoformat()
    lines = "\n".join([f"  <url><loc>{SITE}/blog</loc><lastmod>{posts[0]['date'] if posts else today}</lastmod></url>"]
                      + [f"  <url><loc>{SITE}/blog/{p['slug']}</loc><lastmod>{p['date']}</lastmod></url>" for p in posts])
    i = text.rindex("</urlset>")
    sm.write_text(text[:i].rstrip() + f"\n  <!-- blog:start -->\n{lines}\n  <!-- blog:end -->\n" + text[i:])


if __name__ == "__main__":
    POSTS.mkdir(parents=True, exist_ok=True)
    posts = sorted((read(f) for f in POSTS.glob("*.md")), key=lambda p: p["day"], reverse=True)
    for p in posts:
        p["cover"] = cover(p)
    (ROOT / "blog" / "index.html").write_text(index(posts))
    for p in posts:
        (ROOT / "blog" / p["slug"] / "index.html").write_text(post_page(p, [o for o in posts if o is not p]))
    sitemap(posts)
    print(f"wrote blog/ with {len(posts)} post{'s' if len(posts) != 1 else ''}")
