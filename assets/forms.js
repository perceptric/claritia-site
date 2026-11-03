// The form template gallery and the live forms on each template page (tools/templates.py). No library.
// Without this file every form still shows in full and every card still links to its page.

// Gallery: search words and use-case chips, in place --------------------------------------------------------------
(function () {
  var grid = document.querySelector("[data-grid]");
  var search = document.querySelector("[data-search]");
  if (!grid || !search) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll(".tcard"));
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));
  var count = document.querySelector("[data-count]");
  var none = document.querySelector("[data-none]");
  var tag = "all";
  var q = new URLSearchParams(location.search);
  if (q.get("q")) search.value = q.get("q");

  function apply() {
    var words = search.value.toLowerCase().split(/\s+/).filter(Boolean);
    var n = 0;
    cards.forEach(function (c) {
      var hay = c.getAttribute("data-words");
      var ok = (tag === "all" || (" " + c.getAttribute("data-tags") + " ").indexOf(" " + tag + " ") > -1) && words.every(function (w) { return hay.indexOf(w) > -1; });
      c.hidden = !ok;
      if (ok) n++;
    });
    if (count) count.textContent = n;
    if (none) none.hidden = n > 0;
  }
  search.addEventListener("input", apply);
  chips.forEach(function (ch) {
    ch.addEventListener("click", function () {
      tag = ch.getAttribute("data-tag");
      chips.forEach(function (x) { var on = x === ch; x.classList.toggle("is-on", on); x.setAttribute("aria-pressed", on ? "true" : "false"); });
      apply();
    });
  });
  var clear = document.querySelector("[data-clear]");
  if (clear) clear.addEventListener("click", function () { search.value = ""; chips[0] && chips[0].click(); apply(); search.focus(); });
  apply();
})();

// Live forms ---------------------------------------------------------------------------------------------------
(function () {
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function setup(form) {
    var data = JSON.parse(form.querySelector(".cf__data").textContent);
    var s = data.schema;
    var all = [];
    s.pages.forEach(function (p, i) { p.fields.forEach(function (f) { all.push({ f: f, page: i }); }); });
    var pages = Array.prototype.slice.call(form.querySelectorAll(".cf__page"));
    var prog = form.querySelector(".cf__prog");
    var back = form.querySelector("[data-back]");
    var next = form.querySelector("[data-next]");
    var end = form.querySelector(".cf__end");
    var at = 0;
    var sigs = {};
    var wrapOf = function (key) { return form.querySelector('.cf__f[data-key="' + key + '"]'); };

    // Values, read from the inputs the way the app stores them.
    function value(f) {
      var k = f.key, el = wrapOf(k);
      if (!el) return undefined;
      var q = function (sel) { return el.querySelector(sel); };
      var named = function (n) { var x = el.querySelector('[name="' + n + '"]'); return x ? x.value.trim() : ""; };
      switch (f.kind) {
        case "single": case "dropdown": {
          var c = q("input:checked");
          if (!c) return undefined;
          if (c.value === "__other") return named(k + ".other") || undefined;
          return c.value;
        }
        case "multi": {
          var list = Array.prototype.map.call(el.querySelectorAll("input:checked"), function (x) { return x.value; });
          return list.length ? list : undefined;
        }
        case "yes_no": { var y = q("input:checked"); return y ? y.value === "yes" : undefined; }
        case "agree": return q("input").checked ? true : undefined;
        case "rating": case "nps": case "scale": { var r = q("input:checked"); return r ? Number(r.value) : undefined; }
        case "name": { var a = named(k + ".first"), b = named(k + ".last"); return a || b ? { first: a, last: b } : undefined; }
        case "address": {
          var o = {}, any = false;
          ["line1", "line2", "city", "region", "postal", "country"].forEach(function (p) { var v = named(k + "." + p); if (v) { o[p] = v; any = true; } });
          return any ? o : undefined;
        }
        case "date_range": { var fr = named(k + ".from"), to = named(k + ".to"); return fr || to ? { from: fr, to: to } : undefined; }
        case "matrix": {
          var m = {}, has = false;
          Array.prototype.forEach.call(el.querySelectorAll("input:checked"), function (x) { m[x.name.split("::")[1]] = x.value; has = true; });
          return has ? m : undefined;
        }
        case "ranking": return Array.prototype.map.call(el.querySelectorAll("li"), function (li) { return li.getAttribute("data-value"); });
        case "file": { var fi = q("input"); return fi.files && fi.files.length ? Array.prototype.slice.call(fi.files) : undefined; }
        case "signature": return sigs[k] ? true : undefined;
        case "statement": return undefined;
        default: { var t = named(k); return t || undefined; }
      }
    }

    function has(v) {
      if (v == null) return false;
      if (typeof v === "string") return v.trim() !== "";
      if (Array.isArray(v)) return v.length > 0;
      if (typeof v === "object") return Object.keys(v).some(function (x) { return String(v[x]).trim() !== ""; });
      return true;
    }
    function same(a, b) {
      if (typeof a === "boolean") return a === (b === true || b === "yes" || b === "Yes");
      return String(a).toLowerCase() === String(b).toLowerCase();
    }
    function is(a, b) {
      if (!has(a)) return false;
      if (Array.isArray(a)) return a.some(function (x) { return same(x, b); });
      return same(a, b);
    }
    function meets(c, vals) {
      var a = vals[c.key];
      switch (c.op) {
        case "answered": return has(a);
        case "empty": return !has(a);
        case "is": return is(a, c.value);
        case "not": return !is(a, c.value);
        case "any": return [].concat(c.value).some(function (v) { return is(a, v); });
        case "gte": return typeof a === "number" && a >= Number(c.value);
        case "lte": return typeof a === "number" && a <= Number(c.value);
        default: return true;
      }
    }
    // Which fields show: a hidden field counts as empty for every field after it.
    function view() {
      var vals = {}, shown = {};
      all.forEach(function (x) {
        if (x.f.show && !meets(x.f.show, vals)) return;
        shown[x.f.key] = true;
        var v = value(x.f);
        if (v !== undefined) vals[x.f.key] = v;
      });
      return { shown: shown, vals: vals };
    }
    function livePages(v) {
      var out = [];
      s.pages.forEach(function (p, i) { if (p.fields.some(function (f) { return v.shown[f.key] && f.kind !== "hidden"; })) out.push(i); });
      return out.length ? out : [0];
    }

    function check(f, v) {
      if (!has(v) || (f.kind === "agree" && v !== true)) {
        if (!f.required) return "";
        return { single: "Pick one.", dropdown: "Pick one.", multi: "Pick at least one.", yes_no: "Pick yes or no.", agree: "Tick the box to go on.", rating: "Pick a rating.", nps: "Pick a score.", scale: "Pick a value.", file: "Add a file.", signature: "Sign here.", matrix: "Answer each row." }[f.kind] || "Fill this in.";
      }
      if (f.required && f.kind === "name" && !v.first) return "Fill this in.";
      if (f.required && f.kind === "address" && !(v.line1 && v.city)) return "Fill this in.";
      if (f.required && f.kind === "matrix" && (f.rows || []).some(function (r) { return !v[r]; })) return "Answer each row.";
      if (f.kind === "email" && !EMAIL.test(v)) return "Enter a valid email.";
      if (f.kind === "phone") { var d = v.replace(/\D/g, ""); if (!/^[+\d\s().\-/]+$/.test(v) || d.length < 6 || d.length > 16) return "Enter a valid phone number."; }
      if (f.kind === "url" && !/^(https?:\/\/)?[a-z0-9-]+(\.[a-z0-9-]+)+(\/\S*)?$/i.test(v)) return "Enter a website like acme.com.";
      if (f.kind === "number" || f.kind === "money") {
        var n = Number(String(v).replace(/[,\s$€£]/g, ""));
        if (!isFinite(n)) return "Enter a number.";
        if (f.min != null && n < f.min) return "Enter " + f.min + " or more.";
        if (f.max != null && n > f.max) return "Enter " + f.max + " or less.";
      }
      if (f.kind === "date_range" && v.from && v.to && v.from > v.to) return "The end comes before the start.";
      if (f.kind === "file" && v.some(function (x) { return x.size > 10 * 1024 * 1024; })) return "Files can be up to 10 MB.";
      return "";
    }
    function showErr(key, msg) {
      var el = wrapOf(key);
      if (!el) return;
      var e = el.querySelector(".cf__err");
      el.classList.toggle("is-bad", !!msg);
      if (e) { e.textContent = msg; e.hidden = !msg; }
    }

    function render() {
      var v = view();
      all.forEach(function (x) { var el = wrapOf(x.f.key); if (el) el.hidden = !v.shown[x.f.key]; });
      var lp = livePages(v);
      if (lp.indexOf(at) < 0) at = lp.filter(function (p) { return p < at; }).pop() || lp[0];
      pages.forEach(function (p, i) { p.hidden = i !== at; });
      var i = lp.indexOf(at);
      var last = i >= lp.length - 1;
      back.hidden = i <= 0;
      next.textContent = last ? next.getAttribute("data-submit-label") : "Next";
      if (prog) {
        prog.hidden = lp.length < 2;
        prog.querySelector(".cf__prog-l").textContent = s.pages[at].title || "Step " + (i + 1);
        prog.querySelector(".cf__prog-n").textContent = i + 1 + " / " + lp.length;
        prog.querySelector(".cf__bar i").style.width = ((i + 1) / lp.length) * 100 + "%";
      }
      form.querySelector(".cf__notice") && (form.querySelector(".cf__notice").hidden = !last);
      return { v: v, lp: lp, i: i, last: last };
    }

    function validate(onlyPage) {
      var st = view(), bad = null;
      all.forEach(function (x) {
        if (!st.shown[x.f.key] || (onlyPage != null && x.page !== onlyPage)) return;
        var msg = check(x.f, value(x.f));
        showErr(x.f.key, msg);
        if (msg && !bad) bad = x;
      });
      return bad;
    }
    function focus(x) {
      var el = wrapOf(x.f.key);
      if (!el) return;
      var t = el.querySelector("input:not([type=radio]):not([type=checkbox]), textarea, button, input");
      el.scrollIntoView({ block: "center", behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
      if (t) t.focus({ preventScroll: true });
    }
    function top() { form.scrollIntoView({ block: "start", behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" }); }

    function score(v) {
      var total = 0, max = 0, any = false;
      all.forEach(function (x) {
        var f = x.f;
        if (!f.points || !f.options || !v.shown[f.key]) return;
        any = true;
        max += f.kind === "multi" ? f.points.filter(function (p) { return p > 0; }).reduce(function (a, b) { return a + b; }, 0) : Math.max.apply(null, [0].concat(f.points));
        var a = v.vals[f.key];
        var picked = Array.isArray(a) ? a : typeof a === "boolean" ? [a ? f.options[0] : f.options[1]] : a != null ? [a] : [];
        picked.forEach(function (p) { var i = f.options.findIndex(function (o) { return o.toLowerCase() === String(p).toLowerCase(); }); if (i > -1) total += f.points[i] || 0; });
      });
      return any ? { total: total, max: max } : null;
    }

    function finish() {
      var v = view();
      var sc = score(v), box = form.querySelector(".cf__score");
      box.hidden = true;
      if (sc && s.end.score && s.end.score.length) {
        var band = s.end.score.slice().sort(function (a, b) { return b.min - a.min; }).filter(function (b) { return sc.total >= b.min; })[0];
        box.innerHTML = "";
        var sm = document.createElement("small"); sm.textContent = "Score " + sc.total + " of " + sc.max; box.appendChild(sm);
        if (band) {
          var b = document.createElement("b"); b.textContent = band.title; box.appendChild(b);
          var sp = document.createElement("span"); sp.textContent = band.text; box.appendChild(sp);
        }
        box.hidden = false;
      }
      form.classList.add("is-done");
      end.hidden = false;
      top();
      end.setAttribute("tabindex", "-1");
      end.focus({ preventScroll: true });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var st = render();
      var bad = validate(st.last ? null : at);
      if (bad) {
        if (bad.page !== at) { at = bad.page; render(); validate(at); }
        focus(bad);
        return;
      }
      if (!st.last) { at = st.lp[st.i + 1]; render(); top(); return; }
      finish();
    });
    next.type = "submit";
    back.addEventListener("click", function () { var st = render(); if (st.i > 0) { at = st.lp[st.i - 1]; render(); top(); } });
    form.querySelector(".cf__restart").addEventListener("click", function () {
      form.reset();
      Object.keys(sigs).forEach(function (k) { sigs[k] = false; var c = form.querySelector('canvas[data-sig="' + k + '"]'); c.getContext("2d").clearRect(0, 0, c.width, c.height); });
      form.querySelectorAll(".cf__files").forEach(function (u) { u.innerHTML = ""; });
      form.querySelectorAll(".cf__dd").forEach(resetDd);
      form.querySelectorAll(".cf__stars").forEach(paintStars);
      form.querySelectorAll(".is-bad").forEach(function (x) { x.classList.remove("is-bad"); });
      form.querySelectorAll(".cf__err").forEach(function (x) { x.hidden = true; });
      form.classList.remove("is-done");
      end.hidden = true;
      at = 0;
      render();
      top();
    });
    form.addEventListener("input", function (e) {
      var w = e.target.closest(".cf__f");
      if (w && w.classList.contains("is-bad")) showErr(w.getAttribute("data-key"), "");
      render();
    });
    form.addEventListener("change", function (e) {
      var t = e.target;
      if (t.type === "radio" && t.value === "__other") { var o = t.closest(".cf__f").querySelector(".cf__other"); o.hidden = false; o.focus(); }
      else if (t.type === "radio" && t.closest(".cf__opts")) { var oth = t.closest(".cf__f").querySelector(".cf__other"); if (oth) oth.hidden = true; }
      if (t.type === "file") {
        var ul = t.closest(".cf__f").querySelector(".cf__files");
        ul.innerHTML = "";
        Array.prototype.forEach.call(t.files, function (x) { var li = document.createElement("li"); li.textContent = x.name; ul.appendChild(li); });
      }
      if (t.closest(".cf__stars")) paintStars(t.closest(".cf__stars"));
      var w = t.closest(".cf__f");
      if (w && w.classList.contains("is-bad")) showErr(w.getAttribute("data-key"), "");
      render();
    });

    // Stars fill up to the one picked.
    function paintStars(box) {
      var v = 0;
      var c = box.querySelector("input:checked");
      if (c) v = Number(c.value);
      box.querySelectorAll(".cf__star").forEach(function (l, i) { l.classList.toggle("is-on", i < v); });
    }

    // Ranking: move up and down.
    form.querySelectorAll(".cf__rank").forEach(function (ol) {
      function paint() {
        var lis = ol.querySelectorAll("li");
        lis.forEach(function (li, i) {
          li.querySelector(".cf__rank-n").textContent = i + 1;
          li.querySelector('[data-move="-1"]').disabled = i === 0;
          li.querySelector('[data-move="1"]').disabled = i === lis.length - 1;
        });
      }
      ol.addEventListener("click", function (e) {
        var b = e.target.closest("[data-move]");
        if (!b) return;
        var li = b.closest("li");
        if (b.getAttribute("data-move") === "-1" && li.previousElementSibling) ol.insertBefore(li, li.previousElementSibling);
        else if (b.getAttribute("data-move") === "1" && li.nextElementSibling) ol.insertBefore(li.nextElementSibling, li);
        paint();
        b.focus();
      });
      paint();
    });

    // Dropdowns: the form's own list, with the keyboard.
    function resetDd(dd) {
      var btn = dd.querySelector(".cf__dd-btn");
      dd.classList.remove("has-val");
      dd.querySelector(".cf__dd-val").textContent = btn.getAttribute("data-ph");
      dd.querySelectorAll("li").forEach(function (li) { li.setAttribute("aria-selected", "false"); });
    }
    form.querySelectorAll(".cf__dd").forEach(function (dd) {
      var btn = dd.querySelector(".cf__dd-btn");
      var items = Array.prototype.slice.call(dd.querySelectorAll("li"));
      var active = -1;
      btn.setAttribute("data-ph", dd.querySelector(".cf__dd-val").textContent);
      function open(on) {
        dd.classList.toggle("is-open", on);
        btn.setAttribute("aria-expanded", on ? "true" : "false");
        if (on) { active = Math.max(0, items.findIndex(function (li) { return li.getAttribute("aria-selected") === "true"; })); mark(); }
      }
      function mark() {
        items.forEach(function (li, i) { li.classList.toggle("is-active", i === active); });
        if (items[active]) items[active].scrollIntoView({ block: "nearest" });
      }
      function pick(i) {
        var li = items[i];
        if (!li) return;
        var input = li.querySelector("input");
        input.checked = true;
        items.forEach(function (x) { x.setAttribute("aria-selected", x === li ? "true" : "false"); });
        dd.querySelector(".cf__dd-val").textContent = li.getAttribute("data-value");
        dd.classList.add("has-val");
        open(false);
        btn.focus();
        input.dispatchEvent(new Event("change", { bubbles: true }));
      }
      btn.addEventListener("click", function () { open(!dd.classList.contains("is-open")); });
      items.forEach(function (li, i) {
        li.addEventListener("mousedown", function (e) { e.preventDefault(); });
        li.addEventListener("click", function (e) { e.preventDefault(); pick(i); });
        li.addEventListener("mouseenter", function () { active = i; mark(); });
      });
      btn.addEventListener("keydown", function (e) {
        var isOpen = dd.classList.contains("is-open");
        if (!isOpen && ["ArrowDown", "ArrowUp", "Enter", " "].indexOf(e.key) > -1) { e.preventDefault(); open(true); return; }
        if (!isOpen) return;
        if (e.key === "Escape" || e.key === "Tab") open(false);
        else if (e.key === "ArrowDown") { e.preventDefault(); active = Math.min(items.length - 1, active + 1); mark(); }
        else if (e.key === "ArrowUp") { e.preventDefault(); active = Math.max(0, active - 1); mark(); }
        else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(active); }
        else if (e.key.length === 1) {
          var j = items.findIndex(function (li) { return li.getAttribute("data-value").toLowerCase().indexOf(e.key.toLowerCase()) === 0; });
          if (j > -1) { active = j; mark(); }
        }
      });
      document.addEventListener("mousedown", function (e) { if (!dd.contains(e.target)) open(false); });
    });

    // Signature pads.
    form.querySelectorAll("canvas[data-sig]").forEach(function (c) {
      var key = c.getAttribute("data-sig"), ctx = c.getContext("2d"), down = false;
      function fit() {
        var r = c.getBoundingClientRect(), d = window.devicePixelRatio || 1;
        if (!r.width) return;
        c.width = r.width * d; c.height = r.height * d;
        ctx.setTransform(d, 0, 0, d, 0, 0);
        ctx.lineWidth = 2; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = "#0a0a0a";
      }
      fit();
      var pt = function (e) { var r = c.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; };
      c.addEventListener("pointerdown", function (e) { if (!c.width) fit(); down = true; c.setPointerCapture(e.pointerId); var p = pt(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + 0.1, p.y + 0.1); ctx.stroke(); });
      c.addEventListener("pointermove", function (e) { if (!down) return; var p = pt(e); ctx.lineTo(p.x, p.y); ctx.stroke(); });
      var stop = function () { if (!down) return; down = false; sigs[key] = true; showErr(key, ""); render(); };
      c.addEventListener("pointerup", stop);
      c.addEventListener("pointerleave", stop);
      c.parentNode.querySelector(".cf__sig-clear").addEventListener("click", function () { ctx.clearRect(0, 0, c.width, c.height); sigs[key] = false; render(); });
    });

    render();
  }

  document.querySelectorAll("form[data-cf]").forEach(setup);
})();
