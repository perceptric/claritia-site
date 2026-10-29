// Header menus, the phone menu, the header line on scroll, and scroll reveals. No library.
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

// Try it: a work email builds a lead record, one row at a time. Nothing is sent.
(function () {
  var form = document.querySelector("[data-try]");
  if (!form) return;
  var rec = document.querySelector("[data-rec]");
  var input = form.querySelector("input[type=email]");
  var err = form.querySelector(".try__err");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var free = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "aol.com", "proton.me", "protonmail.com", "live.com", "me.com"];
  var sizes = ["11–50", "51–200", "201–500", "501–1,000"];
  var kinds = ["SaaS", "Fintech", "Health tech", "Marketplace", "Dev tools", "Security"];
  var reps = [["Sam", "US team"], ["Lena", "EMEA team"], ["Omar", "Mid-market"], ["Priya", "Enterprise"]];
  var days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
  function hash(s) { var h = 7; for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; return h; }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function set(key, v) { var el = rec.querySelector('[data-v="' + key + '"]'); if (el) el.textContent = v; }
  var timers = [];
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = (input.value || "").trim().toLowerCase();
    var m = v.match(/^([^@\s]+)@([a-z0-9-]+(\.[a-z0-9-]+)+)$/);
    if (!m) { err.textContent = "Enter a work email, like dana@acme.com."; input.focus(); return; }
    if (free.indexOf(m[2]) > -1) { err.textContent = "Use a work email. Personal addresses don't name a company."; input.focus(); return; }
    err.textContent = "";
    var h = hash(m[2]);
    var name = m[1].split(/[._-]/).filter(Boolean).map(cap).join(" ");
    var co = cap(m[2].split(".")[0]);
    var rep = reps[h % reps.length];
    var score = 72 + (h % 25);
    var day = days[(h >> 3) % 5], hr = 9 + ((h >> 5) % 7);
    var vals = {
      name: name, co: m[2], av: name.charAt(0),
      company: co, size: sizes[(h >> 2) % sizes.length], kind: kinds[(h >> 4) % kinds.length],
      route: rep[0] + ", " + rep[1], times: day + " " + hr + ":00, " + day + " " + (hr + 1) + ":30",
      book: day + " " + hr + ":00"
    };
    timers.forEach(clearTimeout); timers = [];
    rec.classList.remove("is-wait");
    var rows = Array.prototype.slice.call(rec.querySelectorAll("[data-row]"));
    ["name", "co", "av"].forEach(function (k) { set(k, vals[k]); });
    set("score", "0");
    rows.forEach(function (r, i) {
      if (!reduce) r.style.opacity = "0.25";
      timers.push(setTimeout(function () {
        r.querySelectorAll("[data-v]").forEach(function (el) { var k = el.getAttribute("data-v"); if (vals[k]) el.textContent = vals[k]; });
        if (r.hasAttribute("data-score")) set("score", String(score));
        r.style.opacity = "";
        r.classList.remove("is-new"); void r.offsetWidth; r.classList.add("is-new");
      }, reduce ? 0 : 260 + i * 320));
    });
  });
})();
