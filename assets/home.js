// Home page extras. Everything here is a nicety: the page reads and works without it.
// The blinking hero tiles, the green tile field, prompt suggestions, the three steps of How it works and the
// Compare switch. Motion stops under reduced motion.
(function () {
  var rnd = Math.random;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var green = "#0c8c5e";
  var i, r, c;

  // Hero tiles: uneven columns with four fixed columns at each edge, denser toward the edges.
  var t = document.getElementById("tiles");
  if (t) {
    var cols = [], rows = [], out = "";
    for (i = 0; i < 4; i++) cols.push("39.688px");
    for (i = 0; i < 33; i++) cols.push((0.33 + rnd() * 1.45).toFixed(3) + "fr");
    for (i = 0; i < 4; i++) cols.push("39.688px");
    for (i = 0; i < 22; i++) rows.push("calc(29.2px * " + (1.14 + rnd() * 0.06).toFixed(3) + ")");
    t.style.gridTemplateColumns = cols.join(" ");
    t.style.gridTemplateRows = rows.join(" ");
    var center = (cols.length - 1) / 2;
    for (r = 1; r <= rows.length; r++) {
      for (c = 1; c <= cols.length; c++) {
        var d = Math.abs(c - 1 - center) / center;
        var p = d < 0.42 ? 0 : 0.55 * Math.pow((d - 0.42) / 0.58, 1.5);
        if (rnd() < p) {
          var span = rnd() > 0.55 ? 2 : 1;
          var mix = (6 + rnd() * (8 + 22 * d)).toFixed(1);
          out += '<span style="grid-row:' + r + ";grid-column:" + c + " / span " + span + ";background-color:color-mix(in srgb, " + green + " " + mix + "%, transparent);--d:" + (4 + rnd() * 5).toFixed(2) + "s;--o:-" + (rnd() * 8).toFixed(2) + 's"></span>';
          c += span - 1;
        }
      }
    }
    t.innerHTML = out;
  }

  // The field of soft greens behind the product; a few tiles blink.
  var f = document.getElementById("field");
  if (f) {
    var fc = [], fr = [], fo = "";
    for (i = 0; i < 26; i++) fc.push((0.5 + rnd()).toFixed(2) + "fr");
    for (i = 0; i < 18; i++) fr.push("1fr");
    f.style.gridTemplateColumns = fc.join(" ");
    f.style.gridTemplateRows = fr.join(" ");
    for (i = 0; i < 26 * 18; i++) {
      var m = rnd() < 0.12 ? 26 + rnd() * 16 : 6 + rnd() * 14;
      fo += "<span" + (rnd() < 0.08 ? ' class="b"' : "") + ' style="--m:' + m.toFixed(1) + "%;--d:" + (4 + rnd() * 5).toFixed(2) + "s;--o:-" + (rnd() * 8).toFixed(2) + 's"></span>';
    }
    f.innerHTML = fo;
  }

  // Prompt suggestions. Build it with an empty box sends the suggestion that shows.
  var sugg = [
    'Create a <span class="u">demo request</span> form that <span class="u">books a call</span> with sales',
    'Build a <span class="u">catering quote</span> with a <span class="u">price calculator</span> and a deposit',
    'Make a <span class="u">new patient</span> intake that <span class="u">routes by insurance</span>',
    'Set up <span class="u">course sign-ups</span> that send a <span class="u">welcome email</span>'
  ];
  var si = 0, sEl = document.getElementById("suggest"), form = document.querySelector("[data-prompt]");
  var btn = document.getElementById("newsug");
  if (sEl && btn) {
    btn.addEventListener("click", function () {
      si = (si + 1) % sugg.length;
      sEl.innerHTML = sugg[si];
      sEl.style.animation = "none";
      void sEl.offsetWidth;
      sEl.style.animation = "";
    });
  }
  if (form && sEl) {
    form.addEventListener("submit", function () {
      var box = form.querySelector("textarea");
      if (!box.value.trim()) box.value = sEl.textContent.trim();
    });
  }

  // How it works: the three steps take turns and switch the window.
  var cols3 = [].slice.call(document.querySelectorAll(".col3"));
  var tabs = [].slice.call(document.querySelectorAll(".win .tabb[data-tab]"));
  var panes = [].slice.call(document.querySelectorAll(".pane"));
  var step = 0, timer;
  function go(n) {
    step = n;
    cols3.forEach(function (x, k) {
      x.classList.toggle("on", k === n);
      var bar = x.querySelector(".line i");
      bar.style.animation = "none";
      void bar.offsetWidth;
      bar.style.animation = "";
    });
    tabs.forEach(function (x, k) { x.classList.toggle("on", k === n); x.setAttribute("aria-selected", k === n ? "true" : "false"); });
    panes.forEach(function (x, k) { x.classList.toggle("on", k === n); });
    clearTimeout(timer);
    if (!still) timer = setTimeout(function () { go((step + 1) % 3); }, 6000);
  }
  if (cols3.length && panes.length) {
    cols3.forEach(function (x, k) { x.addEventListener("click", function () { go(k); }); });
    tabs.forEach(function (x, k) { x.addEventListener("click", function () { go(k); }); });
    go(0);
  }

  // Choices inside the sample form
  document.querySelectorAll(".opts, .slots2").forEach(function (g) {
    g.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      g.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); });
    });
  });

  // Compare: form tools or schedulers
  var sets = [
    { a: "The calendar lives in the form", a2: "Leads pick a time before they leave the page.", b: "Every answer can route", b2: "Pick the meeting and the person from what they wrote.", c: "Reminders send themselves", c2: "Email and text before every call, with no extra tool." },
    { a: "Questions come before the booking", a2: "Know who is coming and why before the call starts.", b: "Team pools that stay fair", b2: "Round robin and rules share calls across your team.", c: "Follow-ups after every call", c2: "Thank-you notes and next steps go out on their own." }
  ];
  var seg = document.getElementById("seg"), bento = document.getElementById("bento");
  if (seg && bento) {
    seg.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      seg.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
      var s = sets[+b.getAttribute("data-set")];
      bento.querySelectorAll("[data-t]").forEach(function (el) { el.textContent = s[el.getAttribute("data-t")]; });
      bento.classList.remove("is-new");
      void bento.offsetWidth;
      bento.classList.add("is-new");
    });
  }
})();
