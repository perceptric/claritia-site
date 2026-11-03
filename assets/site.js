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
