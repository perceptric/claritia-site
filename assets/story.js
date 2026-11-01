// The product story: picks the feature from how far the tall section has scrolled, and shows its text and screen.
(function () {
  var root = document.querySelector("[data-story]");
  if (!root) return;
  var feats = root.querySelectorAll(".sfeat");
  var screens = root.querySelectorAll(".sscr");
  var links = root.querySelectorAll(".story__nav a");
  var n = feats.length;
  var cur = -1;
  function show(i) {
    if (i === cur) return;
    cur = i;
    for (var k = 0; k < n; k++) {
      feats[k].classList.toggle("on", k === i);
      if (screens[k]) screens[k].classList.toggle("on", k === i);
      if (links[k]) links[k].classList.toggle("on", k === i);
    }
  }
  function pick() {
    var r = root.getBoundingClientRect();
    var span = r.height - window.innerHeight;
    var p = span > 0 ? Math.min(Math.max(-r.top / span, 0), 0.9999) : 0;
    show(Math.floor(p * n));
  }
  // A link scrolls to the part of the section where that feature shows.
  links.forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var i = Number(a.getAttribute("data-to"));
      var top = root.getBoundingClientRect().top + window.scrollY;
      var span = root.offsetHeight - window.innerHeight;
      window.scrollTo({ top: top + span * ((i + 0.5) / n), behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
    });
  });
  // An address like /#routing opens on that feature.
  var hash = location.hash.slice(1);
  feats.forEach(function (f, i) { if (f.id === hash) setTimeout(function () { links[i] && links[i].click(); }, 50); });
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; pick(); });
  }, { passive: true });
  window.addEventListener("resize", pick);
  pick();
})();
