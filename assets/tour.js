// Home: the product tour. No library. Same engine as tryomniscient.com.
// The tour has a tab for each part (Capture, Qualify, Route, Book). Each part is a [data-stage] with --len units and steps that
// start at its [data-go] marks. The active part plays on a clock once the tour is on screen; people can pause, step
// back and forward, jump to a step, or switch parts. Each step plays slowly, then holds for a few seconds so people
// can read it before the next one starts. When a part ends, the next one starts unless someone took the controls.
// Every [data-at] inside turns .on while at <= s < off. [data-count="from,to,at,end,fmt"] counts,
// [data-type="at,end"] types its text, [data-scrub="at,end"] sets --t, and [data-guide] (the spotlight and the
// cursor) moves onto the elements named by the last of its [at, selector] stops that has started.
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var narrow = window.matchMedia("(max-width: 899px)");
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var nums = function (el, name) { return el.getAttribute(name).split(",").map(function (x) { return x.trim(); }); };
  var all = function (el, sel) { return Array.prototype.slice.call(el.querySelectorAll(sel)); };
  var headerH = function () { return parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--header-h")) || 64; };
  var UNIT_MS = 2400;  // time for one unit of --s while a step plays
  var HOLD_MS = 3000;  // reading time at the end of every step
  var NEXT_MS = 4000;  // pause before the next part starts on its own
  if (reduce) document.documentElement.classList.add("rm");

  var tour = document.querySelector("[data-tour]");
  var tabs = tour ? all(tour, "[data-tab]") : [];

  // Canvases are drawn at a fixed size and scaled to their column. Narrow columns crop the left rail (data-crop).
  // On wide screens the canvas also fits under the tabs, so a whole part shows without scrolling.
  function fit() {
    all(document, "[data-canvas]").forEach(function (c) {
      var box = c.parentNode, w = box.parentNode.clientWidth;
      if (!w) return;
      var cw = +c.getAttribute("data-w"), ch = +c.getAttribute("data-h"), crop = +(c.getAttribute("data-crop") || 0);
      var useCrop = crop && w < cw * 0.8;
      var k = Math.min(1.2, w / (cw - (useCrop ? crop : 0)));
      if (!narrow.matches) {
        var bar = tour && tour.querySelector(".tour__tabs");
        k = Math.min(k, (window.innerHeight - headerH() - (bar ? bar.offsetHeight + 24 : 0) - 40) / ch);
      }
      if (useCrop) k = Math.max(k, 0.5);
      c.style.setProperty("--k", k);
      c.style.setProperty("--crop", (useCrop ? crop * k : 0) + "px");
      box.style.height = Math.round(ch * k) + "px";
      box.style.maxWidth = useCrop ? "" : Math.round(cw * k) + "px";
    });
  }

  // Type into mixed text: reveal characters across the element's text nodes in order.
  function typer(el) {
    var nodes = [], walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), n;
    while ((n = walk.nextNode())) nodes.push({ n: n, t: n.nodeValue });
    var total = nodes.reduce(function (a, x) { return a + x.t.length; }, 0);
    return function (t) {
      var left = Math.round(total * t);
      nodes.forEach(function (x) { var k = Math.max(0, Math.min(x.t.length, left)); x.n.nodeValue = x.t.slice(0, k); left -= x.t.length; });
      el.classList.toggle("done", t >= 1);
    };
  }

  var fmt = {
    int: function (v) { return Math.round(v).toLocaleString("en-US"); },
    money: function (v) { return "$" + Math.round(v).toLocaleString("en-US"); },
    m: function (v) { return "$" + v.toFixed(2) + "M"; }
  };

  var stages = all(document, "[data-stage]").map(function (el) {
    var st = { el: el, key: el.getAttribute("data-stage"), len: +getComputedStyle(el).getPropertyValue("--len") || 6, s: -1, p: 0 };
    st.ats = all(el, "[data-at]").map(function (e) {
      return { e: e, at: +e.getAttribute("data-at"), off: e.hasAttribute("data-off") ? +e.getAttribute("data-off") : Infinity };
    });
    st.counts = all(el, "[data-count]").map(function (e) { var a = nums(e, "data-count"); return { e: e, a: +a[0], b: +a[1], at: +a[2], end: +a[3], f: fmt[a[4] || "int"] }; });
    st.types = all(el, "[data-type]").map(function (e) { var a = nums(e, "data-type"); return { at: +a[0], end: +a[1], set: typer(e) }; });
    st.scrubs = all(el, "[data-scrub]").map(function (e) { var a = nums(e, "data-scrub"); return { e: e, at: +a[0], end: +a[1] }; });
    st.guides = all(el, "[data-guide]").map(function (e) { return { e: e, stops: JSON.parse(e.getAttribute("data-guide")) }; });
    st.steps = all(el, "[data-go]").map(function (b) { return { b: b, at: +b.getAttribute("data-go") }; });
    st.marks = st.steps.map(function (x) { return x.at; }).concat([st.len]);
    // Each step's time on the clock: its motion, then the hold
    st.weights = [];
    for (var i = 0; i < st.marks.length - 1; i++) st.weights.push((st.marks[i + 1] - st.marks[i]) * UNIT_MS + HOLD_MS);
    st.total = st.weights.reduce(function (a, b) { return a + b; }, 0);
    st.ms = st.total;
    return st;
  });
  var byKey = function (k) { return stages.filter(function (x) { return x.key === k; })[0]; };

  // p (0..1 of the clock) to s, holding at the end of each step
  function shape(st, p) {
    var acc = 0, last = st.weights.length - 1;
    for (var i = 0; i <= last; i++) {
      var f = st.weights[i] / st.total;
      if (p <= acc + f || i === last) {
        var u = clamp((p - acc) / f), d = st.marks[i + 1] - st.marks[i], play = (d * UNIT_MS) / st.weights[i];
        if (u >= play) return i === last ? st.len : st.marks[i + 1] - 0.001;
        return st.marks[i] + (u / play) * d;
      }
      acc += f;
    }
    return st.len;
  }
  function startOf(st, i) {
    var acc = 0;
    for (var j = 0; j < i; j++) acc += st.weights[j] / st.total;
    return acc;
  }
  function stepOf(st) {
    var cur = 0;
    st.steps.forEach(function (x, i) { if (st.s >= x.at - 0.002) cur = i; });
    return cur;
  }

  function render(st, s) {
    if (Math.abs(s - st.s) < 0.0005) return;
    st.s = s;
    st.el.style.setProperty("--s", s.toFixed(3));
    st.ats.forEach(function (x) { x.e.classList.toggle("on", s >= x.at && s < x.off); });
    st.counts.forEach(function (x) { x.e.textContent = x.f(x.a + (x.b - x.a) * clamp((s - x.at) / (x.end - x.at))); });
    st.types.forEach(function (x) { x.set(clamp((s - x.at) / (x.end - x.at))); });
    st.scrubs.forEach(function (x) { x.e.style.setProperty("--t", clamp((s - x.at) / (x.end - x.at)).toFixed(3)); });
    st.guides.forEach(function (g) {
      var stop = null;
      g.stops.forEach(function (x) { if (s >= x[0]) stop = x; });
      g.stop = stop && stop[1] ? stop[1] : null;
      g.e.classList.toggle("on", !!g.stop);
    });
    var cur = stepOf(st);
    st.steps.forEach(function (x, i) {
      x.b.classList.toggle("cur", i === cur);
      x.b.style.setProperty("--sp", i < cur ? 1 : i > cur ? 0 : clamp((s - x.at) / (st.marks[i + 1] - x.at)).toFixed(3));
    });
  }

  // The spotlight and the cursor measure what they point at on every frame, so they stay on it while it moves.
  function place(st) {
    var canvas = st.el.querySelector("[data-canvas]");
    if (!canvas) return;
    var k = parseFloat(canvas.style.getPropertyValue("--k")) || 1;
    st.guides.forEach(function (g) {
      if (!g.stop) return;
      var root = g.e.getAttribute("data-root") === "win" ? canvas.querySelector(".win") : canvas;
      var rr = root.getBoundingClientRect(), x1 = Infinity, y1 = Infinity, x2 = -Infinity, y2 = -Infinity;
      all(canvas, g.stop).forEach(function (t) {
        var r = t.getBoundingClientRect();
        if (!r.width && !r.height) return;
        x1 = Math.min(x1, r.left); y1 = Math.min(y1, r.top); x2 = Math.max(x2, r.right); y2 = Math.max(y2, r.bottom);
      });
      if (x1 === Infinity) return;
      x1 = (x1 - rr.left) / k; y1 = (y1 - rr.top) / k; x2 = (x2 - rr.left) / k; y2 = (y2 - rr.top) / k;
      var key = Math.round(x1) + "," + Math.round(y1) + "," + Math.round(x2) + "," + Math.round(y2);
      if (key === g.key) return;
      g.key = key;
      if (g.e.classList.contains("cursor")) {
        g.e.style.transform = "translate(" + (x1 + (x2 - x1) * 0.62) + "px," + (y1 + (y2 - y1) * 0.55) + "px)";
      } else {
        var pad = 6;
        g.e.style.transform = "translate(" + (x1 - pad) + "px," + (y1 - pad) + "px)";
        g.e.style.width = (x2 - x1 + pad * 2) + "px";
        g.e.style.height = (y2 - y1 + pad * 2) + "px";
      }
    });
  }

  // ── Playing ──
  var active = stages[0], seen = false, nextTimer = null;
  function setPlaying(st, on) {
    st.playing = on && !reduce;
    st.el.classList.toggle("is-playing", st.playing);
    st.el.classList.toggle("is-done", st.p >= 1);
  }
  function seek(st, p, play) {
    clearTimeout(nextTimer);
    st.p = clamp(p);
    render(st, reduce ? st.len : shape(st, st.p));
    setPlaying(st, play);
  }
  function activate(key, play) {
    var st = byKey(key);
    if (!st) return;
    clearTimeout(nextTimer);
    if (active && active !== st) setPlaying(active, false);
    active = st;
    stages.forEach(function (x) { x.el.hidden = x !== st; });
    tabs.forEach(function (t) {
      var on = t.getAttribute("data-tab") === key;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
    });
    fit();
    st.s = -1;
    seek(st, 0, play);
  }
  function step(st, dir) {
    st.touched = true;
    var cur = stepOf(st);
    // Back goes to the start of this step, or the one before if this one has barely started.
    var into = st.s - st.marks[cur], len = st.marks[cur + 1] - st.marks[cur];
    var to = dir < 0 ? (into < len * 0.25 ? cur - 1 : cur) : cur + 1;
    if (to >= st.steps.length) { seek(st, 1, false); return; }
    seek(st, startOf(st, Math.max(0, to)), true);
  }

  stages.forEach(function (st) {
    st.steps.forEach(function (x, i) { x.b.addEventListener("click", function () { st.touched = true; seek(st, startOf(st, i), true); }); });
    all(st.el, "[data-act]").forEach(function (b) {
      b.addEventListener("click", function () {
        var act = b.getAttribute("data-act");
        st.touched = true;
        if (act === "play") { if (st.p >= 1) seek(st, 0, true); else seek(st, st.p, !st.playing); }
        if (act === "prev") step(st, -1);
        if (act === "next") step(st, 1);
      });
    });
    all(st.el, "[data-next]").forEach(function (b) {
      b.addEventListener("click", function () { activate(b.getAttribute("data-next"), true); });
    });
  });
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { activate(t.getAttribute("data-tab"), true); });
    t.addEventListener("keydown", function (e) {
      var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!d) return;
      var n = tabs[(i + d + tabs.length) % tabs.length];
      n.focus();
      activate(n.getAttribute("data-tab"), true);
    });
  });

  // The tour starts the first time it is on screen, and waits while it is off screen.
  var onScreen = false;
  if (tour && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      onScreen = es[0].isIntersecting;
      if (onScreen && !seen) { seen = true; seek(active, 0, true); }
    }, { threshold: 0.3 }).observe(tour);
  } else if (tour) { seen = onScreen = true; }

  var last = performance.now();
  function frame(now) {
    var dt = Math.min(64, now - last);
    last = now;
    if (active) {
      if (reduce) render(active, active.len);
      else if (active.playing && onScreen) {
        active.p = clamp(active.p + dt / active.ms);
        render(active, shape(active, active.p));
        if (active.p >= 1) {
          setPlaying(active, false);
          var btn = active.el.querySelector("[data-next]");
          if (btn && !active.touched) nextTimer = setTimeout(function () { activate(btn.getAttribute("data-next"), true); }, NEXT_MS);
        }
      } else if (active.s < 0) render(active, 0);
      if (onScreen) place(active);
      var tab = tour && tour.querySelector('[data-tab="' + active.key + '"]');
      if (tab) tab.style.setProperty("--p", active.p.toFixed(3));
    }
    requestAnimationFrame(frame);
  }

  if (active) activate(active.key, false);
  if (reduce) stages.forEach(function (st) { render(st, st.len); });
  window.addEventListener("resize", fit);
  requestAnimationFrame(frame);
})();
