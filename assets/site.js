// Header menus, the phone menu, scroll reveals and the pricing switch. No library.
(function () {
  // Scroll reveals. These run first and mark the page with rv-on; without it, a timer in the head shows everything.
  var reveals = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }
  document.documentElement.classList.add("rv-on");
})();

(function () {
  var header = document.querySelector(".site-header");
  if (!header) return;

  // The header gets its hairline once the page scrolls.
  var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 4); };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Product and Resources menus: hover on a mouse, click anywhere, Esc or a click outside to close.
  var groups = Array.prototype.slice.call(header.querySelectorAll(".nav__group"));
  var hoverable = window.matchMedia("(hover: hover) and (pointer: fine)");
  var timer;
  function setOpen(group, open) {
    group.classList.toggle("is-open", open);
    group.querySelector(".nav__trigger").setAttribute("aria-expanded", open ? "true" : "false");
  }
  function closeAll(except) { groups.forEach(function (g) { if (g !== except) setOpen(g, false); }); }

  groups.forEach(function (group) {
    var trigger = group.querySelector(".nav__trigger");
    trigger.addEventListener("click", function () {
      var open = !group.classList.contains("is-open");
      closeAll(group);
      setOpen(group, open);
    });
    group.addEventListener("mouseenter", function () {
      if (!hoverable.matches) return;
      clearTimeout(timer);
      timer = setTimeout(function () { closeAll(group); setOpen(group, true); }, 120);
    });
    group.addEventListener("mouseleave", function () {
      if (!hoverable.matches) return;
      clearTimeout(timer);
      timer = setTimeout(function () { setOpen(group, false); }, 160);
    });
    group.addEventListener("keydown", function (e) {
      var items = Array.prototype.slice.call(group.querySelectorAll(".nav__panel a"));
      var i = items.indexOf(document.activeElement);
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setOpen(group, true);
        items[Math.min(i + 1, items.length - 1)].focus();
      } else if (e.key === "ArrowUp" && i > -1) {
        e.preventDefault();
        if (i === 0) trigger.focus(); else items[i - 1].focus();
      }
    });
    group.addEventListener("focusout", function (e) {
      if (!group.contains(e.relatedTarget)) setOpen(group, false);
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav__group")) closeAll();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var open = groups.filter(function (g) { return g.classList.contains("is-open"); })[0];
    closeAll();
    if (open) open.querySelector(".nav__trigger").focus();
    if (header.classList.contains("is-open")) toggleSheet(false);
  });

  // Phone menu
  var menuBtn = header.querySelector(".menu-btn");
  function toggleSheet(open) {
    header.classList.toggle("is-open", open);
    document.body.classList.toggle("is-locked", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  if (menuBtn) {
    menuBtn.addEventListener("click", function () { toggleSheet(!header.classList.contains("is-open")); });
    document.querySelectorAll(".sheet a").forEach(function (a) {
      a.addEventListener("click", function () { toggleSheet(false); });
    });
    var wide = window.matchMedia("(min-width: 1024px)");
    var onWide = function (m) { if (m.matches) toggleSheet(false); };
    if (wide.addEventListener) wide.addEventListener("change", onWide); else if (wide.addListener) wide.addListener(onWide);
  }
})();

// Pricing: monthly or yearly.
(function () {
  var plans = document.querySelector("[data-bill]");
  if (!plans) return;
  var btns = Array.prototype.slice.call(plans.querySelectorAll("button"));
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      var yearly = b.getAttribute("data-bill-to") === "yearly";
      document.getElementById("pricing").classList.toggle("is-yearly", yearly);
      btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    });
  });
})();

// Cookie consent. The site only needs one cookie of its own (this choice). Any analytics tag must be written as
// <script type="text/plain" data-consent="analytics" data-src="..."> (or with inline code): it runs only after a yes.
// Other code can read window.claritiaConsent.get() or listen for the "claritia:consent" event.
(function () {
  var NAME = "cl_consent", YEAR = 31536000;
  function read() {
    var m = document.cookie.match(/(?:^|;\s*)cl_consent=([^;]*)/);
    if (!m) return null;
    var v = decodeURIComponent(m[1]).split(".");
    return v[0] === "v1" ? { analytics: v[1] === "a1" } : null;
  }
  function write(c) {
    document.cookie = NAME + "=" + encodeURIComponent("v1." + (c.analytics ? "a1" : "a0")) + "; Max-Age=" + YEAR + "; Path=/; SameSite=Lax" + (location.protocol === "https:" ? "; Secure" : "");
  }
  function run(c) {
    document.querySelectorAll('script[type="text/plain"][data-consent]').forEach(function (s) {
      if (!c[s.getAttribute("data-consent")] || s.hasAttribute("data-ran")) return;
      s.setAttribute("data-ran", "");
      var n = document.createElement("script");
      if (s.getAttribute("data-src")) { n.src = s.getAttribute("data-src"); n.async = true; } else { n.text = s.text; }
      s.parentNode.insertBefore(n, s.nextSibling);
    });
    document.dispatchEvent(new CustomEvent("claritia:consent", { detail: c }));
  }

  var box = null;
  function close() { if (box) { box.remove(); box = null; } }
  function choose(c) { write(c); close(); run(c); }
  function open(showChoices) {
    close();
    var now = read() || { analytics: false };
    box = document.createElement("section");
    box.className = "consent";
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Cookie choices");
    box.innerHTML =
      '<p class="consent__title">Cookies on Claritia</p>' +
      '<p class="consent__text">We use the cookies the site needs to work. With your OK, we\'ll also use analytics cookies to see which pages help. You can change this any time with Cookie settings at the bottom of the page. <a href="/privacy#cookies">Privacy</a></p>' +
      '<div class="consent__choices"' + (showChoices ? "" : " hidden") + '>' +
        '<label class="consent__row"><span><b>Needed</b><small>Keeps the site working and remembers this choice. Always on.</small></span><input type="checkbox" checked disabled></label>' +
        '<label class="consent__row"><span><b>Analytics</b><small>Counts visits and clicks so we can improve the site. Nothing is sold.</small></span><input type="checkbox" id="consent-analytics"' + (now.analytics ? " checked" : "") + '></label>' +
      '</div>' +
      '<div class="consent__actions">' +
        '<button type="button" class="btn btn--outline" data-c="reject">Reject all</button>' +
        '<button type="button" class="btn btn--primary" data-c="accept">Accept all</button>' +
        '<button type="button" class="btn btn--plain consent__more" data-c="' + (showChoices ? "save" : "choose") + '">' + (showChoices ? "Save choices" : "Choose") + '</button>' +
      '</div>';
    document.body.appendChild(box);
    box.addEventListener("click", function (e) {
      var b = e.target.closest("[data-c]");
      if (!b) return;
      var k = b.getAttribute("data-c");
      if (k === "accept") choose({ analytics: true });
      else if (k === "reject") choose({ analytics: false });
      else if (k === "save") choose({ analytics: box.querySelector("#consent-analytics").checked });
      else {
        box.querySelector(".consent__choices").hidden = false;
        b.setAttribute("data-c", "save");
        b.textContent = "Save choices";
        box.querySelector("#consent-analytics").focus();
      }
    });
  }

  window.claritiaConsent = { get: read, open: function () { open(true); } };

  // A Cookie settings link beside Privacy and Terms on every page.
  var legal = document.querySelector('.site-footer__base nav[aria-label="Legal"]');
  if (legal) {
    var link = document.createElement("button");
    link.type = "button";
    link.className = "consent__link";
    link.textContent = "Cookie settings";
    link.addEventListener("click", function () { open(true); var a = box && box.querySelector("#consent-analytics"); if (a) a.focus(); });
    legal.insertBefore(link, legal.children[2] || null);
  }

  var saved = read();
  if (saved) run(saved);
  else open(false);
})();

// No lone word on the last line. CSS keeps most text from ending on one word (text-wrap: pretty and balance in
// site.css); this catches what the browser leaves, like two-line paragraphs and browsers without text-wrap: the last
// two words of each paragraph, item, cell or link list entry share a no-break space, even when the last word sits in
// a link or ends in a period of its own. Short words only, so nothing gets too wide to wrap.
(function () {
  var SEL = "p, li, td, th, dd, figcaption, blockquote, summary, h1, h2, h3, h4, h5, h6, .tcard__blurb";
  var SKIP = "header, button, pre, code, [contenteditable], .nw";
  document.querySelectorAll(SEL).forEach(function (el) {
    if (el.closest(SKIP) || el.textContent.trim().split(/\s+/).length < 3) return;
    var nodes = [], walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), n;
    while ((n = walk.nextNode())) nodes.push(n);
    // From the end: skip trailing spaces, then the last word (it may run across nodes), then glue the space before it.
    var tail = "", seenWord = false;
    for (var k = nodes.length - 1; k >= 0; k--) {
      var t = nodes[k].nodeValue;
      for (var j = t.length - 1; j >= 0; j--) {
        var c = t.charAt(j);
        if (c === "\u00a0" && seenWord) return; // done already
        if (/\s/.test(c) && c !== "\u00a0") {
          if (!seenWord) continue;
          var before = (t.slice(0, j) + "").split(/\s+/).pop();
          if (tail.length > 14 || before.length + tail.length > 24) return;
          nodes[k].nodeValue = t.slice(0, j) + "\u00a0" + t.slice(j + 1);
          return;
        }
        seenWord = true;
        tail = c + tail;
      }
    }
  });
})();
