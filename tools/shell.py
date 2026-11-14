"""The parts every generated page shares with the home page: the icon sprite, the header, the phone menu, the footer
and the <head>. They are copied out of index.html, so the header and footer stay one. Used by tools/templates.py and
tools/legal.py."""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://tryclaritia.com"
SITE_CSS_V = 14
SITE_JS_V = 8
FONT_CSS = "https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..700&amp;display=swap"

INDEX = (ROOT / "index.html").read_text()
esc = lambda s: html.escape(str(s), quote=True)


def block(start: str, end: str) -> str:
    i = INDEX.index(start)
    j = INDEX.index(end, i) + len(end)
    return INDEX[i:j]


def absolute(s: str) -> str:
    """Home-page anchors (href="#pricing") point back at the home page; icon references (<use href="#mark">) stay."""
    return re.sub(r'(<a\b[^>]*?\bhref=")#', r"\1/#", s)


# The dark "last prompt" box that closes the pricing and product pages. It used to be copied out of the home page;
# the home page no longer has it, so it lives in tools/last-prompt.html.
LAST_PROMPT = absolute((ROOT / "tools" / "last-prompt.html").read_text().rstrip("\n"))

SPRITE = block('<svg width="0" height="0"', "</svg>\n")
HEADER = absolute(block('<header class="site-header">', "</header>"))
SHEET = absolute(block('<div class="sheet">', "</div>\n</div>\n"))
FOOTER = absolute(block('<footer class="site-footer">', "</footer>"))
CLOSE_MARK = (
    '<svg class="close__mark" viewBox="0 0 88 88" aria-hidden="true">'
    '<path class="b" pathLength="1" d="M4 28V4h24"/><path class="b" pathLength="1" d="M60 4h24v24"/>'
    '<path class="b" pathLength="1" d="M84 60v24H60"/><path class="b" pathLength="1" d="M28 84H4V60"/>'
    '<path class="c" pathLength="1" d="M29 45l10 10 21-24"/></svg>'
)


def head(title: str, desc: str, path: str, extra: str = "", og: bool = True, og_image: str | None = None, og_type: str = "website") -> str:
    """Everything from <!doctype> to </head>. `extra` is more <link>, <style> or <script> lines."""
    url = f"{SITE}{path}"
    social = (
        f"""<meta property="og:site_name" content="Claritia">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image or SITE + "/assets/brand/og-image.png"}">
<meta name="twitter:card" content="summary_large_image">
"""
        if og
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{social}<link rel="icon" href="/assets/brand/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/brand/claritia-mark-small.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<meta name="theme-color" content="#fafaf5">
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT_CSS}">
<link rel="stylesheet" href="/assets/site.css?v={SITE_CSS_V}">
{extra}<script>document.documentElement.classList.add("js");setTimeout(function(){{if(!document.documentElement.classList.contains("rv-on"))document.querySelectorAll(".reveal").forEach(function(e){{e.classList.add("is-in")}})}},2500);</script>
</head>"""


def body(main: str, scripts: str = "", main_attrs: str = 'id="main"') -> str:
    """The page body: skip link, sprite, header, phone menu, the page's main, the footer and the scripts."""
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>

{SPRITE}
{HEADER}
{SHEET}
<main {main_attrs}>
{main}
</main>

{FOOTER}

<script src="/assets/site.js?v={SITE_JS_V}" defer></script>
{scripts}</body>
</html>
"""
