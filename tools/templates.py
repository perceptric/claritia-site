"""Builds the form template gallery: /templates, one page per industry and one page per template.

The templates come from the app (dev-arrowsterr/claritia, src/lib/forms/templates). Refresh the data there with
  node scripts/export-templates.ts > ../claritia-site/tools/templates.json
then run here:
  python3 tools/templates.py

Every page works without JavaScript: the forms are real HTML, and assets/forms.js adds pages, show-if logic,
checks, the end screen, search and filters on top.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "tools" / "templates.json").read_text())
SITE = "https://tryclaritia.com"
APP = "https://app.tryclaritia.com"
CSS_V, JS_V = 2, 2

T = DATA["templates"]
KIND = DATA["kinds"]
USE = {u["value"]: u["label"] for u in DATA["useCases"]}
IND = [i for i in DATA["industries"]]
esc = lambda s: html.escape(str(s), quote=True)


def ind_slug(v: str) -> str:
    return "any-business" if v == "general" else v.replace("_", "-")


THEMES = DATA["themes"]
TH = {x["id"]: x for x in THEMES}
FONTS_URL = DATA["fonts"].replace("&", "&amp;")
IND_LABEL = {i["value"]: i["label"] for i in IND}
COUNT = {i["value"]: sum(1 for t in T if t["industry"] == i["value"]) for i in IND}
ORDERED = [t for t in T if t["featured"]] + [t for t in T if not t["featured"]]


def fields_of(t):
    return [f for p in t["schema"]["pages"] for f in p["fields"]]


def questions(t):
    return sum(1 for f in fields_of(t) if f["kind"] not in ("statement", "hidden"))


# Styles: one class per style with its CSS variables, and a drawing file for the styles that have one ----------------


def write_styles() -> None:
    art = ROOT / "assets" / "form-art"
    art.mkdir(parents=True, exist_ok=True)
    rules = ["/* Form styles. Written by tools/templates.py from the app's src/lib/forms/themes.ts. */"]
    for th in THEMES:
        body = ";".join(f"{k}:{v}" for k, v in th["vars"].items())
        rules.append(f".th-{th['id']}{{{body}}}")
        if th["art"]:
            (art / f"{th['id']}.svg").write_text(th["art"])
            rules.append(f".th-{th['id']} .fart{{background-image:url(/assets/form-art/{th['id']}.svg?v={CSS_V})}}")
    (ROOT / "assets" / "themes.css").write_text("\n".join(rules) + "\n")


def th_attrs(tid: str) -> str:
    """The class and flags that put a box in a style."""
    th = TH[tid]
    return f'class="fth th-{tid}" data-layout="{th["layout"]}" data-input="{th["input"]}" data-shadow="{th["shadow"]}" data-pattern="{th["pattern"]}"' + (" data-dark" if th["dark"] else "")


def swatch(tid: str) -> str:
    return '<span class="sw" aria-hidden="true">' + "".join(f'<i style="background:{c}"></i>' for c in TH[tid]["swatch"]) + "</span>"


def style_bar(current: str, own: bool = False) -> str:
    """The style menu: the form's own style or any of the others, and Shuffle."""
    data = json.dumps({x["id"]: {k: x[k] for k in ("name", "layout", "input", "shadow", "pattern", "dark")} for x in THEMES}).replace("</", "<\\/")
    opts = []
    if own:
        opts.append(f'<li role="option" data-theme="" aria-selected="true"><span class="sw sw--own" aria-hidden="true"><i></i><i></i><i></i></span><span><b>Each template&#39;s own</b><small>Every card in its own style</small></span></li>')
    for x in THEMES:
        sel = "true" if (x["id"] == current and not own) else "false"
        opts.append(f'<li role="option" data-theme="{x["id"]}" aria-selected="{sel}">{swatch(x["id"])}<span><b>{esc(x["name"])}</b><small>{esc(x["mood"])}</small></span></li>')
    shown = '<span class="sw sw--own" aria-hidden="true"><i></i><i></i><i></i></span><b>Each template&#39;s own</b>' if own else f'{swatch(current)}<b>{esc(TH[current]["name"])}</b>'
    return f"""<div class="tsty" data-styles{" data-own" if own else ""}>
        <span class="tsty__l">Style</span>
        <div class="tsty__dd">
          <button type="button" class="tsty__btn" aria-haspopup="listbox" aria-expanded="false" aria-label="Form style">{shown}<svg class="tsty__chev" aria-hidden="true"><use href="#i-chev"/></svg></button>
          <ul class="tsty__list" role="listbox" aria-label="Form styles">{"".join(opts)}</ul>
        </div>
        <button type="button" class="tsty__shuffle" data-shuffle aria-label="Try another style"><svg aria-hidden="true"><use href="#i-shuffle"/></svg><span>Shuffle</span></button>
        <script type="application/json" class="tsty__data">{data}</script>
      </div>"""


# Shared page parts, copied from the home page so the header, menu and footer stay one --------------------------

INDEX = (ROOT / "index.html").read_text()


def block(start: str, end: str) -> str:
    i = INDEX.index(start)
    j = INDEX.index(end, i) + len(end)
    return INDEX[i:j]


def absolute(s: str) -> str:
    """Home-page anchors (href="#pricing") point back at the home page; icon references (<use href="#mark">) stay."""
    return re.sub(r'(<a\b[^>]*?\bhref=")#', r"\1/#", s)


SPRITE = block('<svg width="0" height="0"', "</svg>\n").replace(
    "</svg>\n",
    '  <symbol id="i-search" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="4.5" stroke="currentColor" stroke-width="1.5"/><path d="m10.5 10.5 3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></symbol>\n'
    '  <symbol id="i-star" viewBox="0 0 24 24"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></symbol>\n'
    '  <symbol id="i-up" viewBox="0 0 16 16" fill="none"><path d="m4 10 4-4 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></symbol>\n'
    '  <symbol id="i-shuffle" viewBox="0 0 16 16" fill="none"><path d="M2 4.5h2.5c1.7 0 2.7.8 3.6 2.2l1 1.6c.9 1.4 1.9 2.2 3.6 2.2H14M2 11.5h2.5c1 0 1.8-.3 2.4-.9M10.3 5.4c.6-.6 1.4-.9 2.4-.9H14M12 2.5l2 2-2 2M12 9.5l2 2-2 2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></symbol>\n'
    "</svg>\n",
)
HEADER = absolute(block('<header class="site-header">', "</header>"))
SHEET = absolute(block('<div class="sheet">', '</div>\n</div>\n'))
FOOTER = absolute(block('<footer class="site-footer">', "</footer>"))
CLOSE_MARK = block('<svg class="close__mark"', "</svg>")


def page(path: str, title: str, desc: str, body: str, ld: list) -> None:
    url = f"{SITE}{path}"
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="Claritia">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/brand/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/brand/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/brand/claritia-mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<meta name="theme-color" content="#ffffff">
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&amp;family=Inter:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="{FONTS_URL}">
<link rel="stylesheet" href="/assets/site.css?v=7">
<link rel="stylesheet" href="/assets/forms.css?v={CSS_V}">
<link rel="stylesheet" href="/assets/themes.css?v={CSS_V}">
<script>document.documentElement.classList.add("js");setTimeout(function(){{if(!document.documentElement.classList.contains("rv-on"))document.querySelectorAll(".reveal").forEach(function(e){{e.classList.add("is-in")}})}},2500);</script>
{"".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{SPRITE}
{HEADER}
{SHEET}
<main id="main">
{body}
</main>

{FOOTER}

<script src="/assets/site.js?v=7" defer></script>
<script src="/assets/forms.js?v={JS_V}" defer></script>
</body>
</html>
"""
    dest = ROOT / path.strip("/") / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out)


def crumbs(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}{p}"} for i, (n, p) in enumerate(items)],
    }


# Gallery card previews: a light drawing of the form's first questions ------------------------------------------


def thumb(t, tid: str | None = None) -> str:
    tid = tid or t["theme"]
    s = t["schema"]
    parts = [f'<b class="tp__title">{esc(s["title"])}</b>']
    if s.get("intro"):
        parts.append(f'<span class="tp__intro">{esc(s["intro"])}</span>')
    shown = [f for f in s["pages"][0]["fields"] if f["kind"] != "hidden"][:5]
    for f in shown:
        k = f["kind"]
        lab = f'<span class="tp__l">{esc(f["label"])}{" *" if f.get("required") else ""}</span>'
        if k in ("short_text", "email", "phone", "url", "number", "money", "date", "time"):
            body = '<span class="tp__box"></span>'
        elif k == "long_text":
            body = '<span class="tp__box tp__box--tall"></span>'
        elif k in ("name", "date_range"):
            body = '<span class="tp__row"><span class="tp__box"></span><span class="tp__box"></span></span>'
        elif k == "address":
            body = '<span class="tp__box"></span><span class="tp__row"><span class="tp__box"></span><span class="tp__box"></span></span>'
        elif k in ("single", "multi"):
            mark = "tp__dot" if k == "single" else "tp__sq"
            opts = f.get("options", [])[:3]
            body = "".join(f'<span class="tp__opt"><i class="{mark}"></i>{esc(o)}</span>' for o in opts)
        elif k == "yes_no":
            o = f.get("options") or ["Yes", "No"]
            body = f'<span class="tp__row"><span class="tp__opt"><i class="tp__dot"></i>{esc(o[0])}</span><span class="tp__opt"><i class="tp__dot"></i>{esc(o[1])}</span></span>'
        elif k == "dropdown":
            body = '<span class="tp__box tp__box--dd"></span>'
        elif k == "rating":
            body = '<span class="tp__stars">' + "".join('<svg><use href="#i-star"/></svg>' for _ in range(f.get("max", 5))) + "</span>"
        elif k in ("nps", "scale"):
            n = 11 if k == "nps" else f.get("max", 5) - f.get("min", 1) + 1
            body = '<span class="tp__steps">' + "<i></i>" * n + "</span>"
        elif k == "matrix":
            body = '<span class="tp__box tp__box--tall"></span>'
        elif k in ("file", "signature"):
            body = '<span class="tp__box tp__box--tall tp__box--dash"></span>'
        elif k == "agree":
            lab = ""
            body = f'<span class="tp__opt tp__opt--plain"><i class="tp__sq"></i>{esc(f["label"])}</span>'
        elif k == "ranking":
            body = "".join(f'<span class="tp__opt">{esc(o)}</span>' for o in f.get("options", [])[:3])
        else:  # statement
            lab = f'<span class="tp__l">{esc(f["label"])}</span>'
            body = ""
        parts.append(f'<span class="tp__f">{lab}{body}</span>')
    btn = s["submit"] if len(s["pages"]) == 1 else "Next"
    parts.append(f'<span class="tp__btn">{esc(btn)}</span>')
    attrs = th_attrs(tid).replace('class="fth ', 'class="tp fth ')
    return f'<span {attrs} data-own="{t["theme"]}" aria-hidden="true"><span class="fth__card"><span class="fart"></span><span class="tp__in">{"".join(parts)}</span></span></span>'


def card(t) -> str:
    tag = '<span class="tag tag--warn">Health</span>' if t["phi"] else ('<span class="tag">Popular</span>' if t["featured"] else "")
    words = " ".join([t["name"], t["blurb"], t["industryLabel"], " ".join(USE.get(x, x) for x in t["tags"]), " ".join(f["label"] for f in fields_of(t))]).lower()
    pages = len(t["schema"]["pages"])
    meta = f'{questions(t)} questions' + (f", {pages} pages" if pages > 1 else "")
    return (
        f'<a class="tcard" href="/templates/{t["slug"]}" data-tags="{" ".join(t["tags"])}" data-words="{esc(words)}">'
        f"{thumb(t)}"
        f'<span class="tcard__body"><span class="tcard__top"><b class="tcard__name">{esc(t["name"])}</b>{tag}</span>'
        f'<span class="tcard__blurb">{esc(t["blurb"])}</span>'
        f'<span class="tcard__meta">{esc(t["industryLabel"])} <span aria-hidden="true">/</span> {meta}</span></span></a>'
    )


# The live form on a template page ------------------------------------------------------------------------------

CUR = {"USD": "$", "EUR": "€", "GBP": "£"}


def field(f) -> str:
    k, key = f["kind"], f["key"]
    fid = f"f-{key}"
    req = f.get("required")
    star = '<span class="cf__req" aria-hidden="true"> *</span>' if req else ""
    attrs = f'data-key="{key}" data-kind="{k}"' + (" data-req" if req else "")
    if f.get("show"):
        attrs += f' data-show="{esc(json.dumps(f["show"]))}"'
    half = " cf__f--half" if f.get("half") and k in ("short_text", "email", "phone", "url", "number", "money", "date", "time", "dropdown") else ""
    help_ = f'<p class="cf__help" id="{fid}-h">{esc(f["help"])}</p>' if f.get("help") else ""
    err = f'<p class="cf__err" id="{fid}-e" hidden></p>'
    ph = f' placeholder="{esc(f["placeholder"])}"' if f.get("placeholder") else ""
    label = f'<label class="cf__label" for="{fid}">{esc(f["label"])}{star}</label>'
    group = f'<p class="cf__label" id="{fid}-l">{esc(f["label"])}{star}</p>'

    def wrap(lab, inner, cls=""):
        return f'<div class="cf__f{half}{cls}" {attrs}>{lab}{help_}{inner}{err}</div>'

    if k == "statement":
        return f'<div class="cf__f cf__f--note" {attrs}><p class="cf__note-h">{esc(f["label"])}</p>{"<p>" + esc(f["help"]) + "</p>" if f.get("help") else ""}</div>'
    if k == "hidden":
        return ""
    if k in ("short_text", "email", "phone", "url"):
        typ = {"email": "email", "phone": "tel", "url": "url"}.get(k, "text")
        ac = {"email": "email", "phone": "tel", "url": "url"}.get(k, "organization" if f.get("map") == "company" else "off")
        return wrap(label, f'<input class="cf__in" id="{fid}" name="{key}" type="{typ}" autocomplete="{ac}"{ph}>')
    if k == "long_text":
        return wrap(label, f'<textarea class="cf__in cf__in--area" id="{fid}" name="{key}" rows="4"{ph}></textarea>')
    if k in ("number", "money"):
        pre = f'<span class="cf__pre">{CUR.get(f.get("currency", "USD"), "$")}</span>' if k == "money" else ""
        return wrap(label, f'<span class="cf__money">{pre}<input class="cf__in{" cf__in--pre" if pre else ""}" id="{fid}" name="{key}" type="text" inputmode="decimal"{ph}></span>')
    if k in ("date", "time"):
        return wrap(label, f'<input class="cf__in cf__in--short" id="{fid}" name="{key}" type="{k}">')
    if k == "date_range":
        return wrap(label, f'<span class="cf__row"><input class="cf__in cf__in--short" id="{fid}" name="{key}.from" type="date" aria-label="From"><span class="cf__to">to</span><input class="cf__in cf__in--short" name="{key}.to" type="date" aria-label="To"></span>')
    if k == "name":
        return wrap(label, f'<span class="cf__grid2"><input class="cf__in" id="{fid}" name="{key}.first" autocomplete="given-name" placeholder="First name" aria-label="First name"><input class="cf__in" name="{key}.last" autocomplete="family-name" placeholder="Last name" aria-label="Last name"></span>')
    if k == "address":
        p = lambda n, phx, ac, c="": f'<input class="cf__in {c}" name="{key}.{n}" autocomplete="{ac}" placeholder="{phx}" aria-label="{phx}"' + (f' id="{fid}"' if n == "line1" else "") + ">"
        return wrap(label, f'<span class="cf__addr">{p("line1", "Street address", "address-line1", "cf__a6")}{p("line2", "Apartment, suite (optional)", "address-line2", "cf__a6")}{p("city", "City", "address-level2", "cf__a3")}{p("region", "State or region", "address-level1", "cf__a3")}{p("postal", "Postal code", "postal-code", "cf__a2")}{p("country", "Country", "country-name", "cf__a4")}</span>')
    if k in ("single", "multi", "yes_no"):
        typ = "checkbox" if k == "multi" else "radio"
        opts = f.get("options") or ["Yes", "No"]
        vals = ["yes", "no"] if k == "yes_no" else opts
        two = " cf__opts--2" if (k == "yes_no" or (len(opts) > 4 and all(len(o) < 28 for o in opts))) else ""
        items = "".join(f'<label class="cf__opt"><input type="{typ}" name="{key}" value="{esc(v)}"><span class="cf__mark cf__mark--{typ}"></span><span>{esc(o)}</span></label>' for o, v in zip(opts, vals))
        if f.get("other") and k == "single":
            items += f'<label class="cf__opt"><input type="radio" name="{key}" value="__other"><span class="cf__mark cf__mark--radio"></span><span>Other</span></label><input class="cf__in cf__other" name="{key}.other" placeholder="Type your answer" aria-label="Other" hidden>'
        return wrap(group, f'<div class="cf__opts{two}{" cf__opts--yn" if k == "yes_no" else ""}" role="{"radiogroup" if typ == "radio" else "group"}" aria-labelledby="{fid}-l">{items}</div>')
    if k == "agree":
        return f'<div class="cf__f" {attrs}><label class="cf__agree"><input type="checkbox" name="{key}" value="yes"><span class="cf__mark cf__mark--checkbox"></span><span>{esc(f["label"])}{star}</span></label>{help_}{err}</div>'
    if k == "dropdown":
        items = "".join(f'<li role="option" aria-selected="false" data-value="{esc(o)}"><label><input type="radio" name="{key}" value="{esc(o)}">{esc(o)}</label></li>' for o in f.get("options", []))
        return wrap(label, f'<div class="cf__dd"><button class="cf__in cf__dd-btn" id="{fid}" type="button" aria-haspopup="listbox" aria-expanded="false"><span class="cf__dd-val">{esc(f.get("placeholder") or "Choose…")}</span><svg aria-hidden="true"><use href="#i-chev"/></svg></button><ul class="cf__dd-list" role="listbox" aria-labelledby="{fid}">{items}</ul></div>')
    if k == "rating":
        n = f.get("max", 5)
        items = "".join(f'<label class="cf__star"><input type="radio" name="{key}" value="{i}" aria-label="{i} of {n}"><svg aria-hidden="true"><use href="#i-star"/></svg></label>' for i in range(1, n + 1))
        return wrap(group, f'<div class="cf__stars" role="radiogroup" aria-labelledby="{fid}-l">{items}</div>')
    if k in ("nps", "scale"):
        lo, hi = (0, 10) if k == "nps" else (f.get("min", 1), f.get("max", 5))
        a = f.get("minLabel") or ("Not likely" if k == "nps" else "")
        b = f.get("maxLabel") or ("Very likely" if k == "nps" else "")
        items = "".join(f'<label class="cf__step"><input type="radio" name="{key}" value="{i}"><span>{i}</span></label>' for i in range(lo, hi + 1))
        ends = f'<span class="cf__ends"><span>{esc(a)}</span><span>{esc(b)}</span></span>' if a or b else ""
        return wrap(group, f'<div class="cf__steps" role="radiogroup" aria-labelledby="{fid}-l" style="--n:{hi - lo + 1}">{items}</div>{ends}')
    if k == "ranking":
        items = "".join(f'<li data-value="{esc(o)}"><span class="cf__rank-n">{i + 1}</span><span class="cf__rank-t">{esc(o)}</span><button type="button" class="cf__rank-b" data-move="-1" aria-label="Move {esc(o)} up"><svg><use href="#i-up"/></svg></button><button type="button" class="cf__rank-b cf__rank-b--down" data-move="1" aria-label="Move {esc(o)} down"><svg><use href="#i-up"/></svg></button></li>' for i, o in enumerate(f.get("options", [])))
        return wrap(group, f'<ol class="cf__rank" aria-labelledby="{fid}-l">{items}</ol>')
    if k == "matrix":
        cols = f.get("options", [])
        head = "".join(f"<th scope=\"col\">{esc(c)}</th>" for c in cols)
        rows = "".join(f'<tr><th scope="row">{esc(r)}</th>' + "".join(f'<td><label class="cf__cell"><input type="radio" name="{key}::{esc(r)}" value="{esc(c)}" aria-label="{esc(r)}: {esc(c)}"><span class="cf__mark cf__mark--radio"></span></label></td>' for c in cols) + "</tr>" for r in f.get("rows", []))
        return wrap(group, f'<div class="cf__matrix"><table><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
    if k == "file":
        many = f.get("maxFiles", 1) > 1
        return wrap(label, f'<label class="cf__drop"><input id="{fid}" type="file" name="{key}"{" multiple" if many else ""}><span>Drop {"files" if many else "a file"} here or <u>browse</u></span><small>Up to 10 MB</small></label><ul class="cf__files"></ul>')
    if k == "signature":
        return wrap(group, f'<div class="cf__sig"><canvas aria-label="Signature pad" data-sig="{key}"></canvas><button type="button" class="cf__sig-clear">Clear</button></div>')
    return ""


def live_form(t) -> str:
    s = t["schema"]
    pages = []
    for i, p in enumerate(s["pages"]):
        title = f'<p class="cf__ptitle">{esc(p["title"])}</p>' if p.get("title") else ""
        pages.append(f'<fieldset class="cf__page" data-page="{i}"><legend class="sr-only">Step {i + 1}</legend>{title}<div class="cf__fields">{"".join(field(f) for f in p["fields"])}</div></fieldset>')
    multi = len(s["pages"]) > 1
    notice = "" if t["internal"] else '<p class="cf__notice">We\'ll use your details to reply and may email you about related products. You can unsubscribe at any time.</p>'
    end = s["end"]
    data = json.dumps({"schema": s, "use": f"{APP}/forms/templates/{t['slug']}"}, ensure_ascii=False).replace("</", "<\\/")
    return f"""<form class="cf" novalidate data-cf>
  <div class="cf__head"><h2 class="cf__title">{esc(s["title"])}</h2>{f'<p class="cf__intro">{esc(s["intro"])}</p>' if s.get("intro") else ""}</div>
  {'<div class="cf__prog" hidden><span class="cf__prog-l"></span><span class="cf__prog-n"></span><span class="cf__bar"><i></i></span></div>' if multi else ""}
  {"".join(pages)}
  <div class="cf__acts"><button type="button" class="cf__btn cf__btn--ghost" data-back hidden>Back</button><button type="button" class="cf__btn" data-next data-submit-label="{esc(s["submit"])}">{esc(s["submit"] if not multi else "Next")}</button></div>
  {notice}
  <div class="cf__end" hidden role="status"><span class="cf__end-ic"><svg aria-hidden="true"><use href="#i-check"/></svg></span><h3 class="cf__end-t">{esc(end["title"])}</h3><div class="cf__score" hidden></div>{f'<p class="cf__end-p">{esc(end["text"])}</p>' if end.get("text") else ""}<p class="cf__demo">This is a preview, so nothing was sent. <a href="{APP}/forms/templates/{t['slug']}">Use this template</a> to take real answers.</p><button type="button" class="cf__restart">Start over</button></div>
  <script type="application/json" class="cf__data">{data}</script>
</form>"""


# Pages -------------------------------------------------------------------------------------------------------

CLOSE = lambda line1, line2, href, label: f"""<section class="close">
    <div class="wrap close__in reveal">
      {CLOSE_MARK}
      <h2 class="h2">{line1}<br><span class="two">{line2}</span></h2>
      <div class="close__ctas">
        <a class="btn btn--primary btn--lg" href="{href}">{label} <span class="nudge" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn--ghost btn--lg" href="mailto:hello@tryclaritia.com?subject=Claritia%20demo">Book a demo</a>
      </div>
      <p class="small">Free plan. No card needed.</p>
    </div>
  </section>"""


def rail(current: str) -> str:
    rows = [f'<a class="trail__i{" is-on" if current == "all" else ""}" href="/templates"{" aria-current=\"page\"" if current == "all" else ""}><span>All templates</span><small>{len(T)}</small></a>']
    for i in IND:
        on = current == i["value"]
        rows.append(f'<a class="trail__i{" is-on" if on else ""}" href="/templates/{ind_slug(i["value"])}"{" aria-current=\"page\"" if on else ""}><span>{esc(i["label"])}</span><small>{COUNT[i["value"]]}</small></a>')
    return f'<nav class="trail" aria-label="Industries"><p class="trail__h">Industry</p>{"".join(rows)}</nav>'


def gallery(current: str, items) -> str:
    chips = '<button type="button" class="chip is-on" data-tag="all" aria-pressed="true">Any use</button>' + "".join(
        f'<button type="button" class="chip" data-tag="{u["value"]}" aria-pressed="false">{esc(u["label"])}</button>' for u in DATA["useCases"] if any(u["value"] in t["tags"] for t in items)
    )
    return f"""<section class="tgal">
    <div class="wrap tgal__in">
      {rail(current)}
      <div class="tgal__main">
        <div class="tfilter">
          <label class="tsearch"><span class="sr-only">Search templates</span><svg aria-hidden="true"><use href="#i-search"/></svg><input type="search" placeholder="Search {len(items)} templates" data-search></label>
          <div class="chips" role="group" aria-label="Use">{chips}</div>
        </div>
        <details class="tjump"><summary>Industry: {esc("All" if current == "all" else IND_LABEL[current])} <svg aria-hidden="true"><use href="#i-chev"/></svg></summary><div class="tjump__list"><a href="/templates">All templates</a>{"".join(f'<a href="/templates/{ind_slug(i["value"])}">{esc(i["label"])}</a>' for i in IND)}</div></details>
        <div class="tbar"><p class="tcount"><span data-count>{len(items)}</span> templates</p>{style_bar("paper", own=True)}</div>
        <div class="tgrid" data-grid>{"".join(card(t) for t in items)}</div>
        <div class="tnone" hidden data-none><p>No matches.</p><button type="button" class="more" data-clear>Clear the search</button></div>
      </div>
    </div>
  </section>"""


INTROS = {
    "general": "Contact forms, sign-ups, feedback and surveys that work for any business.",
    "saas": "Demo requests, trials, onboarding and product feedback for software teams.",
    "agency": "Project inquiries, client intake and creative briefs for agencies.",
    "consulting": "Consultation requests, discovery questions and proposals for consultants.",
    "legal": "Case reviews, client intake and document requests for law firms.",
    "accounting": "Tax intake, bookkeeping quotes and year-end checklists for accountants.",
    "finance": "Financial reviews, risk quizzes and loan applications for advisors and lenders.",
    "insurance": "Quote requests, claims and policy reviews for insurance teams.",
    "real_estate": "Home valuations, buyer inquiries, showings and rental applications for agents and landlords.",
    "construction": "Free estimates, service calls and remodel planners for contractors.",
    "solar": "Savings checks, energy audits and charger installs for energy companies.",
    "healthcare": "Appointment requests, patient intake and feedback for clinics.",
    "wellness": "New patient bookings, consultations and waivers for dental and wellness practices.",
    "fitness": "Trial classes, memberships, bookings and waivers for gyms and salons.",
    "education": "Course inquiries, applications, feedback and quizzes for schools and trainers.",
    "ecommerce": "Wholesale inquiries, product quizzes, returns and reviews for online stores.",
    "manufacturing": "Requests for quote, samples and supplier onboarding for manufacturers.",
    "logistics": "Freight quotes, carrier onboarding and driver applications for logistics teams.",
    "automotive": "Test drives, trade-ins and service bookings for dealers and shops.",
    "hospitality": "Event inquiries, catering, reservations and guest feedback for hotels and restaurants.",
    "events": "Registration, speaker calls, sponsor inquiries and post-event surveys.",
    "nonprofit": "Volunteer sign-ups, pledges, grant applications and RSVPs for nonprofits.",
    "hr": "Job applications, onboarding, engagement surveys and reviews for HR teams.",
    "it": "IT assessments, support tickets and security quizzes for IT providers.",
}


def industry_page(i):
    v = i["value"]
    items = [t for t in ORDERED if t["industry"] == v]
    path = f"/templates/{ind_slug(v)}"
    body = f"""<section class="thero thero--sm">
    <div class="wrap"><div class="thero__in">
      <nav class="tcrumb reveal" aria-label="Breadcrumb"><a href="/templates">Templates</a><span aria-hidden="true">/</span><span>{esc(i["label"])}</span></nav>
      <h1 class="h2 reveal" data-delay="1">{esc(i["label"])} form templates</h1>
      <p class="lead reveal" data-delay="2">{esc(INTROS.get(v, ""))} Try each one, then use it in a click.</p>
    </div></div>
  </section>
  {gallery(v, items)}
  {CLOSE(f"Forms for {esc(i['label'].lower() if v != 'saas' else 'SaaS and software')}.", "Live on your site in a click.", APP, "Start free")}"""
    page(
        path,
        f"{i['label']} form templates | Claritia",
        f"{len(items)} free {i['label'].lower() if v != 'saas' else 'SaaS and software'} form templates. {INTROS.get(v, '')}",
        body,
        [crumbs([("Templates", "/templates"), (i["label"], path)])],
    )


LOGOS = [("hubspot.svg", "HubSpot"), ("salesforce.svg", "Salesforce"), ("omniscient.svg", "Omniscient"), ("pipedrive.png", "Pipedrive"), ("attio.png", "Attio"),
         ("slack.svg", "Slack"), ("gmail.svg", "Gmail"), ("outlook.jpg", "Outlook"), ("calendly.svg", "Calendly"), ("zoom.svg", "Zoom"), ("meet.svg", "Google Meet"),
         ("stripe.svg", "Stripe"), ("zapier.svg", "Zapier"), ("webflow.svg", "Webflow"), ("wordpress.svg", "WordPress"), ("framer.svg", "Framer")]
KINDS_SHOWN = ["short_text", "long_text", "email", "phone", "url", "number", "money", "single", "multi", "dropdown", "yes_no", "agree", "rating", "nps",
               "scale", "ranking", "matrix", "date", "time", "date_range", "name", "address", "file", "signature", "statement", "hidden"]
FEATS = [
    ("Show-if logic", "Ask the next question only when an earlier answer calls for it."),
    ("Pages and progress", "Split long forms into steps with a progress bar."),
    ("Scores and results", "Turn answers into a score and show each person what it means."),
    ("Files and signatures", "Take uploads up to 10 MB and signatures drawn on any screen."),
    ("Booking", "Open your calendar on the thank-you screen, with name and email filled in."),
    ("Consent by region", "An opt-in box where the law asks for one, a short notice everywhere else."),
    ("Every answer a contact", "The company comes from the work email, the campaign from the link."),
    ("Spam stays out", "A hidden trap, rate limits and temporary emails refused."),
]


def stage(t, tid: str) -> str:
    return f"""<div {th_attrs(tid)} data-stage>
          <div class="fth__card"><div class="fart" aria-hidden="true"></div><div class="fth__body">
          {live_form(t)}
          </div></div>
        </div>"""


def logos() -> str:
    return '<ul class="tlogos">' + "".join(f'<li><img src="/assets/logos/{f}" alt="{esc(n)}" width="28" height="28" loading="lazy"></li>' for f, n in LOGOS) + "</ul>"


def kinds_grid() -> str:
    return '<ul class="tkinds">' + "".join(f"<li>{esc(KIND[k])}</li>" for k in KINDS_SHOWN) + "</ul>"


def feat_grid() -> str:
    return '<div class="tfeats">' + "".join(f'<div class="tfeat"><h3 class="h3">{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in FEATS) + "</div>"


def steps(use: str) -> str:
    return f"""<ol class="tsteps reveal" data-delay="1">
        <li><span class="tsteps__n">01</span><h3 class="h3">Use the template</h3><p>It opens in Claritia ready to go, in the style you picked. Answers are linked to your contact fields and the form goes live.</p></li>
        <li><span class="tsteps__n">02</span><h3 class="h3">Connect your tools</h3><p>Send answers to HubSpot, Salesforce or Omniscient, open your calendar after a booking form, and tell your team in Slack.</p></li>
        <li><span class="tsteps__n">03</span><h3 class="h3">Share it anywhere</h3><p>Send the link, or add one line to Webflow, WordPress, Framer or any page. Every answer lands as a contact.</p></li>
      </ol>"""


def short_labels(t, n=4):
    out = []
    for f in fields_of(t):
        lab = f["label"].strip()
        if f["kind"] in ("statement", "hidden", "agree", "signature") or "?" in lab or len(lab.split()) > 3:
            continue
        out.append(lab[0].lower() + lab[1:] if not lab[:2].isupper() else lab)
        if len(out) >= n:
            break
    return out


def and_list(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def describe(t) -> str:
    labs = short_labels(t)
    asks = f" It asks for {and_list(labs)}" + (f", plus {questions(t) - len(labs)} more questions" if questions(t) > len(labs) else "") + "." if labs else ""
    return f"{t['blurb']}{asks} Use this free template as it is, or change any question, the style and the thank-you screen, then share it or put it on your site."


def faqs(t):
    name = t["name"]
    low = name.lower()
    labs = short_labels(t, 6)
    qa = [
        (f"Can I customize the {low} form?", f"Yes. Add, remove and reorder questions, change the wording and options, and set which ones are required. Pick one of {len(THEMES)} styles or your own color. Tailor can also rewrite the wording for your business from one sentence."),
        (f"What does the {low} form collect?", (f"It asks for {and_list(labs)}" + (f", plus {questions(t) - len(labs)} more questions" if questions(t) > len(labs) else "") + ". You can add or remove any of them.") if labs else f"It has {questions(t)} questions, listed on this page. You can add or remove any of them."),
        (f"Is the {low} form mobile-friendly?", "Yes. Every form fits phones, tablets and computers, and works with a keyboard and screen readers."),
        (f"Is the {low} template free?", "Yes. Every template is free on every plan, including the free one. Use it, change it and share it as often as you like."),
        ("Where do the answers go?", "Each answer becomes a contact in Claritia, with the company found from the work email and the page and campaign the visitor came from. From there it can sync to HubSpot, Salesforce or Omniscient."),
        ("How do I put it on my website?", "Share the link, or paste one line of code where the form should show. It fits any website, including Webflow, WordPress, Framer and plain HTML."),
    ]
    if t["phi"]:
        qa.append(("Can it collect health information?", "This form asks for health details, so it stays a draft until your workspace confirms a signed business associate agreement (BAA) with us."))
    else:
        qa.append(("Does it ask for consent?", "Yes. Visitors in the EU, the UK and other strict regions see an opt-in box; everyone else sees a short notice. Claritia saves the exact words each person saw."))
    return qa


def faq_block(qa, head="Questions") -> str:
    return f"""<section class="section">
    <div class="wrap faq">
      <div class="faq__head reveal"><h2 class="h2">{head}</h2><p class="lead">Something else? <a href="mailto:hello@tryclaritia.com">hello@tryclaritia.com</a></p></div>
      <div class="qa reveal" data-delay="1">{"".join(f'<details><summary>{esc(q)} <svg aria-hidden="true"><use href="#i-plus"/></svg></summary><p>{esc(a)}</p></details>' for q, a in qa)}</div>
    </div>
  </section>"""


def template_page(t):
    path = f"/templates/{t['slug']}"
    ind_path = f"/templates/{ind_slug(t['industry'])}"
    use = f"{APP}/forms/templates/{t['slug']}"
    s = t["schema"]
    fl = [f for f in fields_of(t) if f["kind"] != "hidden"]
    asks = "".join(f'<li><span class="tasks__n">{n + 1}</span><span class="tasks__t">{esc(f["label"])}</span><span class="tasks__k">{esc(KIND[f["kind"]])}</span></li>' for n, f in enumerate(fl))
    pages = len(s["pages"])
    tags = "".join(f'<span class="tag">{esc(USE.get(x, x))}</span>' for x in t["tags"])
    same = [x for x in ORDERED if x["industry"] == t["industry"] and x["id"] != t["id"]]
    alike = [x for x in ORDERED if x["industry"] != t["industry"] and set(x["tags"]) & set(t["tags"])]
    related = (same + alike)[:12]
    others = [x["id"] for x in THEMES if x["id"] != t["theme"]]
    looks = [t["theme"]] + others[(T.index(t) * 5) % len(others):][:5]
    looks += [x for x in others if x not in looks][: 6 - len(looks)]
    qa = faqs(t)
    title_h = f"{t['name']} template" if not t["name"].lower().endswith("template") else t["name"]
    body = f"""<section class="thero thero--tpl">
    <div class="wrap">
      <nav class="tcrumb" aria-label="Breadcrumb"><a href="/templates">Templates</a><span aria-hidden="true">/</span><a href="{ind_path}">{esc(t["industryLabel"])}</a><span aria-hidden="true">/</span><span>{esc(t["name"])}</span></nav>
      <div class="tpl__top">
        <div class="tpl__copy">
          <h1 class="h2">{esc(title_h)}</h1>
          <p class="lead">{esc(describe(t))}</p>
          <div class="tpl__tags"><span class="tag tag--sig">Free</span>{tags}<span class="tag">{questions(t)} questions</span>{f'<span class="tag">{pages} pages</span>' if pages > 1 else ""}</div>
        </div>
        <div class="tpl__ctas"><a class="btn btn--primary btn--lg" href="{use}?theme={t["theme"]}" data-use="{use}">Use template <span class="nudge" aria-hidden="true">&rarr;</span></a><a class="btn btn--ghost btn--lg" href="#try">Explore demo</a></div>
      </div>
    </div>
  </section>
  <section class="tpl" id="try">
    <div class="wrap tpl__in">
      <div class="tpl__main">
        {style_bar(t["theme"])}
        {stage(t, t["theme"])}
      </div>
      <aside class="tpl__side">
        <div class="tbox">
          <h2 class="tbox__h">What it asks</h2>
          <ol class="tasks">{asks}</ol>
        </div>
        <div class="tbox">
          <h2 class="tbox__h">What happens to answers</h2>
          <ul class="checks tchecks">
            <li><svg aria-hidden="true"><use href="#i-check"/></svg>Each answer becomes a contact, with the company found from the email.</li>
            <li><svg aria-hidden="true"><use href="#i-check"/></svg>The page, the campaign and the consent the visitor gave are saved with it.</li>
            <li><svg aria-hidden="true"><use href="#i-check"/></svg>It can sync to HubSpot, Salesforce or Omniscient.</li>
            {'<li><svg aria-hidden="true"><use href="#i-check"/></svg>The thank-you screen opens your booking link, with the name and email filled in.</li>' if s["end"].get("booking") else ""}
            {'<li><svg aria-hidden="true"><use href="#i-check"/></svg>Each person sees their score and what it means.</li>' if s["end"].get("score") else ""}
          </ul>
        </div>
        <a class="btn btn--primary tbox__cta" href="{use}?theme={t["theme"]}" data-use="{use}">Use template <span class="nudge" aria-hidden="true">&rarr;</span></a>
      </aside>
    </div>
  </section>
  <section class="section section--tint">
    <div class="wrap">
      <div class="sec-head reveal"><p class="eyebrow">Styles</p><h2 class="h2">One form, {len(THEMES)} looks.<br><span class="two">Pick one, or bring your color.</span></h2></div>
      <div class="tlooks reveal" data-delay="1">{"".join(f'<button type="button" class="tlook" data-pick="{x}" aria-label="Show the form in {esc(TH[x]["name"])}">{thumb(t, x).replace(" data-own=", " data-fixed data-own=")}<span class="tlook__n">{swatch(x)}<b>{esc(TH[x]["name"])}</b><small>{esc(TH[x]["mood"])}</small></span></button>' for x in looks)}</div>
    </div>
  </section>
  <section class="section">
    <div class="wrap tsplit">
      <div class="sec-head reveal"><p class="eyebrow">Customize in minutes</p><h2 class="h2">Make it yours.<br><span class="two">No code.</span></h2><p class="lead">Change any question, add your own from {len(KINDS_SHOWN)} question types, and show each one only when it matters.</p></div>
      <div class="reveal" data-delay="1">{kinds_grid()}</div>
    </div>
    <div class="wrap">{feat_grid()}</div>
  </section>
  <section class="section section--tint">
    <div class="wrap">
      <div class="sec-head reveal"><p class="eyebrow">Connect to any app</p><h2 class="h2">Answers go where you work.<br><span class="two">Live in a minute.</span></h2></div>
      {steps(use)}
      <div class="reveal" data-delay="2">{logos()}</div>
    </div>
  </section>
  {faq_block(qa, "Frequently asked questions")}
  <section class="section section--tint">
    <div class="wrap">
      <div class="trel__head"><h2 class="h2">Related templates</h2><a class="more" href="{ind_path}">More for {esc(t["industryLabel"]) if t["industry"] != "general" else "any business"} <span class="nudge" aria-hidden="true">&rarr;</span></a></div>
      <div class="tgrid tgrid--3">{"".join(card(x) for x in related)}</div>
    </div>
  </section>
  {CLOSE("Make your first form in minutes.", "Start with this template.", f"{use}?theme={t['theme']}", "Use template")}"""
    ld = [
        crumbs([("Templates", "/templates"), (t["industryLabel"], ind_path), (t["name"], path)]),
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]},
    ]
    page(path, f"{title_h} (free) | Claritia", f"{t['blurb']} A free {t['name'].lower()} form with {questions(t)} questions and {len(THEMES)} styles. Try it, then use it in a click.", body, ld)


INDEX_QA = [
    ("Are the templates free?", "Yes. Every template is free on every plan, including the free one."),
    ("Can I change a template?", "Yes. Change any question, its wording and options, the order, the style and the thank-you screen. Tailor can rewrite the wording for your business from one sentence."),
    ("Can I match my brand?", f"Pick one of {len(THEMES)} styles, then set your own button color. Every style works on phones and with a keyboard."),
    ("Where do the answers go?", "Each answer becomes a contact in Claritia, with the company found from the work email. It can sync to HubSpot, Salesforce or Omniscient."),
    ("How do I add a form to my website?", "Share the link, or paste one line of code where the form should show. It fits Webflow, WordPress, Framer and plain HTML."),
    ("Do the forms ask for consent?", "Yes. An opt-in box in the EU, the UK and other strict regions, and a short notice elsewhere. The exact words each person saw are saved."),
]


def styles_strip() -> str:
    sample = next(x for x in T if x["id"] == "general.book-a-call")
    return '<div class="tlooks tlooks--all">' + "".join(
        f'<button type="button" class="tlook" data-global="{x["id"]}" aria-label="Show every template in {esc(x["name"])}">{thumb(sample, x["id"]).replace(" data-own=", " data-fixed data-own=")}<span class="tlook__n">{swatch(x["id"])}<b>{esc(x["name"])}</b><small>{esc(x["mood"])}</small></span></button>'
        for x in THEMES
    ) + "</div>"


def index_page():
    body = f"""<section class="thero">
    <div class="wrap"><div class="thero__in">
      <p class="eyebrow reveal">Form templates</p>
      <h1 class="display reveal" data-delay="1">Form templates<br><span class="two">for every industry.</span></h1>
      <p class="lead reveal" data-delay="2">{len(T)} ready forms for {len(IND)} industries in {len(THEMES)} styles: demo requests, quotes, intake, applications, surveys and quizzes. Try any of them here. Use one and it goes live on your site in a click, with every answer saved as a contact.</p>
      <div class="hero__ctas reveal" data-delay="3"><a class="btn btn--primary btn--lg" href="#all">Browse templates</a><a class="btn btn--ghost btn--lg" href="{APP}">Start free</a></div>
    </div></div>
  </section>
  <div id="all"></div>
  {gallery("all", ORDERED)}
  <section class="section section--tint" id="styles">
    <div class="wrap">
      <div class="sec-head reveal"><p class="eyebrow">Styles</p><h2 class="h2">{len(THEMES)} styles for every form.<br><span class="two">Tap one to see the whole gallery in it.</span></h2></div>
      <div class="reveal" data-delay="1">{styles_strip()}</div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="sec-head reveal"><p class="eyebrow">Built in</p><h2 class="h2">Everything a form needs.<br><span class="two">On every template.</span></h2></div>
      {feat_grid()}
    </div>
  </section>
  <section class="section section--tint">
    <div class="wrap">
      <div class="sec-head reveal"><p class="eyebrow">How it works</p><h2 class="h2">Pick it, connect it, share it.<br><span class="two">Live in a minute.</span></h2></div>
      {steps(APP)}
      <div class="reveal" data-delay="2">{logos()}</div>
    </div>
  </section>
  {faq_block(INDEX_QA)}
  {CLOSE("Make your first form in minutes.", "Free plan, live in a click.", APP, "Start free")}"""
    page(
        "/templates",
        "Free form templates for every industry | Claritia",
        f"{len(T)} free form templates for {len(IND)} industries in {len(THEMES)} styles: demo requests, quotes, intake, applications, surveys and quizzes. Try each one, then use it in a click.",
        body,
        [crumbs([("Templates", "/templates")]), {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in INDEX_QA]}],
    )


def sitemap():
    sm = ROOT / "sitemap.xml"
    text = sm.read_text()
    text = re.sub(r"\s*<!-- templates:start -->.*?<!-- templates:end -->", "", text, flags=re.S)
    urls = ["/templates"] + [f"/templates/{ind_slug(i['value'])}" for i in IND] + [f"/templates/{t['slug']}" for t in T]
    lines = "\n".join(f"  <url><loc>{SITE}{u}</loc></url>" for u in urls)
    text = text.replace("</urlset>", f"  <!-- templates:start -->\n{lines}\n  <!-- templates:end -->\n</urlset>")
    sm.write_text(text)


if __name__ == "__main__":
    slugs = [t["slug"] for t in T]
    assert len(set(slugs)) == len(slugs), "template slugs repeat"
    assert not set(slugs) & {ind_slug(i["value"]) for i in IND}, "a template and an industry share a slug"
    write_styles()
    index_page()
    for i in IND:
        industry_page(i)
    for t in T:
        template_page(t)
    sitemap()
    print(f"wrote /templates, {len(IND)} industry pages and {len(T)} template pages")
