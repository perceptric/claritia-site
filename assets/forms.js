// The form template gallery and the live forms on each template page (tools/templates.py). No library.
// Without this file every form still shows in full and every card still links to its page.

// Gallery: search words and filter chips, in place. Chips in one menu widen the results; two menus narrow them. ---
(function () {
  var grid = document.querySelector("[data-grid]");
  var search = document.querySelector("[data-search]");
  if (!grid || !search) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll(".tcard"));
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip[data-m]"));
  var count = document.querySelector("[data-count]");
  var none = document.querySelector("[data-none]");
  var on = {};
  var q = new URLSearchParams(location.search);
  if (q.get("q")) search.value = q.get("q");

  function fits(c) {
    for (var m in on) {
      if (!on[m].length) continue;
      var have = " " + (c.getAttribute("data-" + m) || "") + " ";
      if (!on[m].some(function (v) { return have.indexOf(" " + v + " ") > -1; })) return false;
    }
    return true;
  }
  function apply() {
    var words = search.value.toLowerCase().split(/\s+/).filter(Boolean);
    var n = 0;
    cards.forEach(function (c) {
      var hay = c.getAttribute("data-words");
      var ok = fits(c) && words.every(function (w) { return hay.indexOf(w) > -1; });
      c.hidden = !ok;
      if (ok) n++;
    });
    if (count) count.textContent = n;
    if (none) none.hidden = n > 0;
  }
  search.addEventListener("input", apply);
  chips.forEach(function (ch) {
    ch.addEventListener("click", function () {
      var m = ch.getAttribute("data-m");
      var v = ch.getAttribute("data-v");
      var list = on[m] || (on[m] = []);
      var i = list.indexOf(v);
      if (i > -1) list.splice(i, 1);
      else list.push(v);
      var pressed = i < 0;
      ch.classList.toggle("is-on", pressed);
      ch.setAttribute("aria-pressed", pressed ? "true" : "false");
      apply();
    });
  });
  var clear = document.querySelector("[data-clear]");
  if (clear)
    clear.addEventListener("click", function () {
      search.value = "";
      on = {};
      chips.forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-pressed", "false"); });
      apply();
      search.focus();
    });
  apply();
})();

// Describe your form: the words find the closest templates on the page first; Build with AI opens the app. ---------
(function () {
  var box = document.querySelector("[data-desc]");
  if (!box) return;
  var input = box.querySelector("input");
  var out = box.querySelector("[data-desc-picks]");
  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-grid] .tcard"));
  var STOP = " a an the for and or to of my our we need want form forms that with from in on is are be can people who where when they their it so like some get let make ";
  var t;
  input.addEventListener("input", function () {
    clearTimeout(t);
    t = setTimeout(function () {
      var words = input.value.toLowerCase().replace(/[^a-z0-9\s-]/g, " ").split(/\s+/).filter(function (w) { return w.length > 2 && STOP.indexOf(" " + w + " ") < 0; });
      var best = words.length
        ? cards
            .map(function (c, i) { var h = c.getAttribute("data-words"); return { c: c, i: i, n: words.filter(function (w) { return h.indexOf(w) > -1; }).length }; })
            .filter(function (x) { return x.n >= Math.min(2, words.length); })
            .sort(function (a, b) { return b.n - a.n || a.i - b.i; })
            .slice(0, 3)
        : [];
      out.innerHTML = "";
      best.forEach(function (x) {
        var a = document.createElement("a");
        a.className = "chip";
        a.href = x.c.getAttribute("href");
        a.textContent = "Start from " + x.c.querySelector(".tcard__name").textContent;
        out.appendChild(a);
      });
      out.hidden = !best.length;
    }, 250);
  });
})();

// Live forms ---------------------------------------------------------------------------------------------------
(function () {
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Calculations: the app's small formula language (numbers, + - * /, comparisons, and, or, min, max, sum, round,
  // ceil, floor, abs, if, ifempty, other answers as {key}). Read by this parser, never eval. An empty answer is null and
  // null carries through, the same as in the app.
  function calc(src, get) {
    var toks = (src.match(/\s+|\d+(?:\.\d+)?|\.\d+|\{[^}]*\}|[a-z]+|<=|>=|==|!=|[-+*\/(),<>]|./gi) || []).filter(function (t) { return t.trim(); });
    var i = 0;
    var peek = function () { return toks[i]; };
    var take = function () { return toks[i++]; };
    var num = function (x) { return x == null || !isFinite(x) ? null : x; };
    var both = function (a, b, fn) { return a == null || b == null ? null : num(fn(a, b)); };
    function bin(next, ops, fn) {
      return function () {
        var a = next();
        while (ops.indexOf(String(peek()).toLowerCase()) > -1) { var op = take().toLowerCase(); a = fn(op, a, next()); }
        return a;
      };
    }
    function primary() {
      var t = take();
      if (t === undefined) throw 0;
      if (t === "(") { var x = orx(); take(); return x; }
      if (t === "-") { var y = primary(); return y == null ? null : -y; }
      if (/^[\d.]/.test(t)) return Number(t);
      if (t[0] === "{") return get(t.slice(1, -1));
      var name = t.toLowerCase();
      take();
      var args = [];
      if (peek() !== ")") { args.push(orx()); while (peek() === ",") { take(); args.push(orx()); } }
      take();
      var nums = args.filter(function (a) { return a != null; });
      switch (name) {
        case "min": return nums.length ? Math.min.apply(null, nums) : null;
        case "max": return nums.length ? Math.max.apply(null, nums) : null;
        case "sum": return nums.reduce(function (a, b) { return a + b; }, 0);
        case "round": return args[0] == null ? null : Math.round(args[0] * Math.pow(10, args[1] || 0)) / Math.pow(10, args[1] || 0);
        case "ceil": return args[0] == null ? null : Math.ceil(args[0]);
        case "floor": return args[0] == null ? null : Math.floor(args[0]);
        case "abs": return args[0] == null ? null : Math.abs(args[0]);
        case "if": return args[0] == null ? null : args[0] ? args[1] : args[2];
        case "ifempty": return args[0] == null ? args[1] : args[0];
        default: throw 0;
      }
    }
    var mul = bin(primary, ["*", "/"], function (op, a, b) { return both(a, b, function (x, y) { return op === "*" ? x * y : y === 0 ? NaN : x / y; }); });
    var add = bin(mul, ["+", "-"], function (op, a, b) { return both(a, b, function (x, y) { return op === "+" ? x + y : x - y; }); });
    var cmp = bin(add, ["<", ">", "<=", ">=", "==", "!="], function (op, a, b) {
      return both(a, b, function (x, y) { return { "<": x < y, ">": x > y, "<=": x <= y, ">=": x >= y, "==": x === y, "!=": x !== y }[op] ? 1 : 0; });
    });
    var andx = bin(cmp, ["and"], function (op, a, b) { return both(a, b, function (x, y) { return x && y ? 1 : 0; }); });
    var orx = bin(andx, ["or"], function (op, a, b) { return both(a, b, function (x, y) { return x || y ? 1 : 0; }); });
    try { var out = orx(); return i < toks.length ? null : num(out); } catch (e) { return null; }
  }
  var SYM = { USD: "$", EUR: "€", GBP: "£", CAD: "$", AUD: "$", NZD: "$" };
  function shown(n, format, cur) {
    if (n == null) return format === "money" ? (SYM[cur] || "") + "0" : "0";
    if (format === "money") return (SYM[cur] || cur + " ") + Math.round(n).toLocaleString("en-US");
    if (format === "percent") return (Math.round(n * 10) / 10).toLocaleString("en-US") + "%";
    return (Math.round(n * 100) / 100).toLocaleString("en-US");
  }

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
        case "group": {
          // Each row that has an answer, by its questions' labels.
          var rowsOut = [];
          Array.prototype.forEach.call(el.querySelectorAll(".cf__row"), function (row) {
            var o = {}, any = false;
            Array.prototype.forEach.call(row.querySelectorAll("input"), function (x, i) {
              var v = x.value.trim();
              if (v) { o[f.parts && f.parts[i] ? f.parts[i].label : String(i)] = v; any = true; }
            });
            if (any) rowsOut.push(o);
          });
          return rowsOut.length ? rowsOut : undefined;
        }
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
    // The pages this person will see, in order: Next, or a page's paths by answer, then its skip; "end" stops.
    function livePages(v) {
      var out = [], i = 0, n = s.pages.length, guard = 0;
      while (i < n && guard++ < 64) {
        var p = s.pages[i];
        if (p.fields.some(function (f) { return v.shown[f.key] && f.kind !== "hidden"; })) out.push(i);
        var to = i + 1;
        var j = (p.jumps || []).filter(function (x) { return meets(x.when, v.vals); })[0];
        if (j) to = j.to;
        else if (p.skip && meets(p.skip.when, v.vals)) to = p.skip.to;
        i = to > i ? to : i + 1;
      }
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

    // An answer as a number for a formula: a choice reads its points, pick many adds them up, numbers read as numbers.
    function numOf(f, a, calcs) {
      if (f.kind === "calc") return calcs[f.key] == null ? null : calcs[f.key];
      if (a == null) return null;
      var pts = function (p) { var i = (f.options || []).findIndex(function (o) { return o.toLowerCase() === String(p).toLowerCase(); }); return i > -1 && f.points ? f.points[i] || 0 : isFinite(Number(p)) ? Number(p) : null; };
      if (Array.isArray(a)) return a.reduce(function (t, p) { var n = pts(p); return t + (n || 0); }, 0);
      if (typeof a === "boolean") return f.points ? f.points[a ? 0 : 1] || 0 : a ? 1 : 0;
      if (typeof a === "number") return a;
      if (f.kind === "single" || f.kind === "dropdown") return pts(a);
      var n = Number(String(a).replace(/[,\s$€£]/g, ""));
      return isFinite(n) ? n : null;
    }
    function calcs(v) {
      var out = {};
      all.forEach(function (x) {
        if (x.f.kind !== "calc") return;
        out[x.f.key] = calc(x.f.formula || "0", function (k) {
          var src = all.find(function (y) { return y.f.key === k; });
          return src && v.shown[k] ? numOf(src.f, v.vals[k], out) : null;
        });
      });
      Array.prototype.forEach.call(form.querySelectorAll("[data-calc]"), function (o) { o.textContent = shown(out[o.getAttribute("data-calc")], o.getAttribute("data-format"), o.getAttribute("data-cur")); });
      Array.prototype.forEach.call(form.querySelectorAll("[data-pay]"), function (o) {
        var fixed = o.getAttribute("data-amount");
        o.textContent = shown(fixed ? Number(fixed) : out[o.getAttribute("data-pay")], "money", o.getAttribute("data-cur"));
      });
      return out;
    }

    function render() {
      var v = view();
      calcs(v);
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

    // Checks the fields on these pages (a page number, or a list of the pages someone will see).
    function validate(onlyPage) {
      var st = view(), bad = null;
      var on = function (pg) { return onlyPage == null || (Array.isArray(onlyPage) ? onlyPage.indexOf(pg) > -1 : pg === onlyPage); };
      all.forEach(function (x) {
        if (!st.shown[x.f.key] || !on(x.page)) return;
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

    // Booking templates: a sample calendar on the end screen, the next three weekdays.
    function booking() {
      var b = form.querySelector("[data-book]");
      if (!b) return;
      var days = b.querySelector(".cf__days");
      days.innerHTML = "";
      var d = new Date();
      var n = 0;
      while (n < 3) {
        d.setDate(d.getDate() + 1);
        if (d.getDay() === 0 || d.getDay() === 6) continue;
        var btn = document.createElement("button");
        btn.type = "button";
        btn.textContent = d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
        if (!n) btn.className = "is-on";
        days.appendChild(btn);
        n++;
      }
      b.querySelector(".cf__book-note").hidden = true;
      Array.prototype.forEach.call(b.querySelectorAll(".cf__times button"), function (x) { x.classList.remove("is-on"); });
    }
    form.addEventListener("click", function (e) {
      var btn = e.target.closest && e.target.closest(".cf__days button, .cf__times button");
      if (!btn) return;
      Array.prototype.forEach.call(btn.parentNode.children, function (x) { x.classList.toggle("is-on", x === btn); });
      if (btn.parentNode.classList.contains("cf__times")) form.querySelector(".cf__book-note").hidden = false;
    });

    function finish() {
      booking();
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
      var bad = validate(st.last ? st.lp : at);
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
    // A cover screen: the form waits behind it until Start.
    var cover = form.querySelector("[data-cover]");
    if (cover) {
      form.classList.add("has-cover");
      cover.querySelector("[data-start]").addEventListener("click", function () { form.classList.remove("has-cover"); render(); top(); });
    }
    // Repeating groups: one more row, up to the most the question allows.
    form.querySelectorAll("[data-add]").forEach(function (btn) {
      var rows = btn.closest(".cf__f").querySelector(".cf__rows");
      var most = Number(rows.getAttribute("data-max")) || 10;
      btn.addEventListener("click", function () {
        var list = rows.querySelectorAll(".cf__row");
        if (list.length >= most) return;
        var n = list.length, row = list[0].cloneNode(true);
        row.querySelectorAll("input").forEach(function (x) {
          x.value = "";
          x.removeAttribute("id");
          x.name = x.name.replace(/\.\d+\.(\d+)$/, "." + n + ".$1");
          x.setAttribute("aria-label", x.getAttribute("placeholder") + ", row " + (n + 1));
        });
        rows.appendChild(row);
        btn.hidden = n + 1 >= most;
        row.querySelector("input").focus();
      });
    });
    // Save and finish later: on the live form it emails a link; here it says so.
    var later = form.querySelector("[data-later]");
    if (later) later.addEventListener("click", function () { var note = form.querySelector(".cf__later-note"); note.hidden = !note.hidden; });
    form.querySelector(".cf__restart").addEventListener("click", function () {
      form.reset();
      Object.keys(sigs).forEach(function (k) { sigs[k] = false; var c = form.querySelector('canvas[data-sig="' + k + '"]'); c.getContext("2d").clearRect(0, 0, c.width, c.height); });
      form.querySelectorAll(".cf__files").forEach(function (u) { u.innerHTML = ""; });
      form.querySelectorAll(".cf__dd").forEach(resetDd);
      form.querySelectorAll(".cf__rows").forEach(function (r) { Array.prototype.slice.call(r.querySelectorAll(".cf__row"), 1).forEach(function (x) { x.remove(); }); });
      form.querySelectorAll("[data-add]").forEach(function (b) { b.hidden = false; });
      form.querySelectorAll(".cf__stars").forEach(paintStars);
      form.querySelectorAll(".is-bad").forEach(function (x) { x.classList.remove("is-bad"); });
      form.querySelectorAll(".cf__err").forEach(function (x) { x.hidden = true; });
      form.classList.remove("is-done");
      if (cover) form.classList.add("has-cover");
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
        if (on) keepInView(dd.querySelector(".cf__dd-list"));
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

// A menu that just opened slides sideways until it sits fully on screen, 12px from each edge.
function keepInView(el) {
  el.style.transform = "";
  var r = el.getBoundingClientRect(), vw = document.documentElement.clientWidth, dx = 0;
  if (r.right > vw - 12) dx = vw - 12 - r.right;
  if (r.left + dx < 12) dx = 12 - r.left;
  if (dx) el.style.transform = "translateX(" + Math.round(dx) + "px)";
}

// Styles: the style menu, Shuffle and the style tiles ------------------------------------------------------------
(function () {
  var bars = Array.prototype.slice.call(document.querySelectorAll("[data-styles]"));
  if (!bars.length) return;
  var meta = JSON.parse(bars[0].querySelector(".tsty__data").textContent);
  var ids = Object.keys(meta);

  function paint(el, id) {
    var m = meta[id];
    if (!m) return;
    el.className = el.className.replace(/\bth-[a-z]+\b/, "th-" + id);
    el.setAttribute("data-layout", m.layout);
    el.setAttribute("data-input", m.input);
    el.setAttribute("data-shadow", m.shadow);
    el.setAttribute("data-pattern", m.pattern);
    if (m.dark) el.setAttribute("data-dark", ""); else el.removeAttribute("data-dark");
  }

  function setup(bar) {
    var own = bar.hasAttribute("data-own");
    var btn = bar.querySelector(".tsty__btn");
    var list = bar.querySelector(".tsty__list");
    var items = Array.prototype.slice.call(list.querySelectorAll("li"));
    var active = 0;
    var current = (items.filter(function (li) { return li.getAttribute("aria-selected") === "true"; })[0] || items[0]).getAttribute("data-theme");

    function apply(id, quiet) {
      current = id;
      items.forEach(function (li) { li.setAttribute("aria-selected", li.getAttribute("data-theme") === id ? "true" : "false"); });
      var li = items.filter(function (x) { return x.getAttribute("data-theme") === id; })[0];
      if (li) {
        var sw = li.querySelector(".sw").cloneNode(true);
        btn.innerHTML = "";
        btn.appendChild(sw);
        var b = document.createElement("b");
        b.textContent = li.querySelector("b").textContent;
        btn.appendChild(b);
        btn.insertAdjacentHTML("beforeend", '<svg class="tsty__chev" aria-hidden="true"><use href="#i-chev"/></svg>');
      }
      if (own) {
        document.querySelectorAll(".tcard .tp").forEach(function (tp) { paint(tp, id || tp.getAttribute("data-own")); });
      } else {
        var stage = document.querySelector("[data-stage]");
        if (stage) paint(stage, id);
        document.querySelectorAll("[data-use]").forEach(function (a) { a.href = a.getAttribute("data-use") + "?theme=" + id; });
        document.querySelectorAll(".tlook[data-pick]").forEach(function (x) { x.classList.toggle("is-on", x.getAttribute("data-pick") === id); });
      }
      document.querySelectorAll(".tlook[data-global]").forEach(function (x) { x.classList.toggle("is-on", own && x.getAttribute("data-global") === id); });
      if (!quiet) {
        var u = new URL(location.href);
        if (id && !(own && !id)) u.searchParams.set("style", id); else u.searchParams.delete("style");
        history.replaceState(null, "", u.pathname + u.search + u.hash);
      }
    }
    function open(on) {
      bar.classList.toggle("is-open", on);
      btn.setAttribute("aria-expanded", on ? "true" : "false");
      if (on) { keepInView(list); active = Math.max(0, items.findIndex(function (li) { return li.getAttribute("data-theme") === current; })); mark(); }
    }
    function mark() {
      items.forEach(function (li, i) { li.classList.toggle("is-active", i === active); });
      if (items[active]) items[active].scrollIntoView({ block: "nearest" });
    }
    btn.addEventListener("click", function () { open(!bar.classList.contains("is-open")); });
    items.forEach(function (li, i) {
      li.addEventListener("mousedown", function (e) { e.preventDefault(); });
      li.addEventListener("click", function () { apply(li.getAttribute("data-theme")); open(false); btn.focus(); });
      li.addEventListener("mouseenter", function () { active = i; mark(); });
    });
    btn.addEventListener("keydown", function (e) {
      var isOpen = bar.classList.contains("is-open");
      if (!isOpen && ["ArrowDown", "ArrowUp", "Enter", " "].indexOf(e.key) > -1) { e.preventDefault(); open(true); return; }
      if (!isOpen) return;
      if (e.key === "Escape" || e.key === "Tab") open(false);
      else if (e.key === "ArrowDown") { e.preventDefault(); active = Math.min(items.length - 1, active + 1); mark(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); active = Math.max(0, active - 1); mark(); }
      else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); apply(items[active].getAttribute("data-theme")); open(false); }
    });
    document.addEventListener("mousedown", function (e) { if (!bar.contains(e.target)) open(false); });
    bar.querySelector("[data-shuffle]").addEventListener("click", function () {
      var pool = ids.filter(function (x) { return x !== current; });
      apply(pool[Math.floor(Math.random() * pool.length)]);
    });

    // Style tiles below: one switches the form above, or the whole gallery.
    document.querySelectorAll(own ? ".tlook[data-global]" : ".tlook[data-pick]").forEach(function (x) {
      x.addEventListener("click", function () {
        apply(x.getAttribute(own ? "data-global" : "data-pick"));
        var to = document.getElementById(own ? "all" : "try");
        if (to) to.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
      });
    });

    var want = new URLSearchParams(location.search).get("style");
    if (want && meta[want]) apply(want, true);
  }
  bars.forEach(setup);
})();
