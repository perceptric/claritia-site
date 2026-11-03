// The product pages' demos (tools/products.py): Tia building a form, form styles, a price that adds up, the embed
// code for each way, a booking calendar on real dates in the visitor's time zone, the reminder line, the router and
// round robin. Plain JavaScript; each demo finds its own root and does nothing when it isn't on the page. Without
// JavaScript every section still shows its static version.

(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (root, sel) { return root.querySelector(sel); };
  var $$ = function (root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); };
  var press = function (btns, on) { btns.forEach(function (b) { b.setAttribute("aria-pressed", b === on ? "true" : "false"); }); };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };

  // Form styles: paint a form stage in another style, using the same flags the template pages use.
  var THEMES = {};
  var themeData = document.getElementById("px-themes");
  if (themeData) { try { THEMES = JSON.parse(themeData.textContent); } catch (e) {} }
  function paint(el, id) {
    var m = THEMES[id];
    if (!el || !m) return;
    el.className = el.className.replace(/\bth-[a-z]+\b/, "th-" + id);
    el.setAttribute("data-layout", m.layout);
    el.setAttribute("data-input", m.input);
    el.setAttribute("data-shadow", m.shadow);
    el.setAttribute("data-pattern", m.pattern);
    if (m.dark) el.setAttribute("data-dark", ""); else el.removeAttribute("data-dark");
  }

  // Forms: describe it, Tia builds it ---------------------------------------------------------------------------
  $$(document, "[data-build]").forEach(function (root) {
    var box = $(root, "textarea");
    var chips = $$(root, "[data-ask]");
    var steps = $(root, "ul[data-steps]");
    var stages = $$(root, "[data-tpl]");
    var swatches = $$(root, "[data-swatch]");
    var shuffle = $(root, "[data-shuffle]");
    var use = $(root, "[data-use-tpl]");
    var picked = null; // a style the visitor chose, kept as forms change
    var run = 0;
    var shown = function () { return stages.filter(function (s) { return !s.hidden; })[0]; };

    function showStage(slug) {
      stages.forEach(function (s) {
        var on = s.getAttribute("data-tpl") === slug;
        s.hidden = !on;
        if (on) {
          s.classList.remove("is-new");
          void s.offsetWidth;
          s.classList.add("is-new");
          paint(s, picked || s.getAttribute("data-own"));
        }
      });
      if (use) use.href = "/templates/" + slug;
      markSwatch(picked || (shown() && shown().getAttribute("data-own")));
    }
    function markSwatch(id) { swatches.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-swatch") === id ? "true" : "false"); }); }

    function build(chip) {
      var my = ++run;
      press(chips, chip);
      var text = chip.getAttribute("data-text");
      var list = JSON.parse(chip.getAttribute("data-list"));
      steps.innerHTML = "";
      steps.hidden = false;
      root.classList.add("is-building");
      var i = 0;
      function addSteps() {
        if (my !== run) return;
        if (i >= list.length) {
          root.classList.remove("is-building");
          showStage(chip.getAttribute("data-ask"));
          return;
        }
        var li = document.createElement("li");
        li.innerHTML = '<svg aria-hidden="true"><use href="#i-check"/></svg>';
        li.appendChild(document.createTextNode(list[i++]));
        steps.appendChild(li);
        setTimeout(addSteps, reduce ? 0 : 320);
      }
      if (reduce) { box.value = text; addSteps(); return; }
      box.value = "";
      var n = 0;
      (function type() {
        if (my !== run) return;
        box.value = text.slice(0, ++n);
        if (n < text.length) setTimeout(type, 18); else setTimeout(addSteps, 200);
      })();
    }
    chips.forEach(function (c) { c.addEventListener("click", function () { build(c); }); });
    swatches.forEach(function (b) {
      b.addEventListener("click", function () {
        picked = b.getAttribute("data-swatch");
        paint(shown(), picked);
        markSwatch(picked);
      });
    });
    if (shuffle) shuffle.addEventListener("click", function () {
      var ids = Object.keys(THEMES).filter(function (x) { return x !== (picked || (shown() && shown().getAttribute("data-own"))); });
      picked = ids[Math.floor(Math.random() * ids.length)];
      paint(shown(), picked);
      markSwatch(picked);
    });
    markSwatch(shown() && shown().getAttribute("data-own"));
  });

  // Forms: a price that adds up ----------------------------------------------------------------------------------
  $$(document, "[data-px-calc]").forEach(function (root) {
    var guests = 40, per = 38, bar = true;
    var out = $(root, "[data-guests]");
    var total = $(root, "[data-total]");
    var deposit = $(root, "[data-deposit]");
    var each = $(root, "[data-each]");
    function draw() {
      out.textContent = guests;
      var t = guests * (per + (bar ? 12 : 0));
      total.textContent = money(t);
      deposit.textContent = money(t * 0.2);
      each.textContent = money(per + (bar ? 12 : 0));
    }
    $(root, "[data-less]").addEventListener("click", function () { guests = Math.max(10, guests - 5); draw(); });
    $(root, "[data-more]").addEventListener("click", function () { guests = Math.min(400, guests + 5); draw(); });
    var serve = $$(root, "[data-per]");
    serve.forEach(function (b) { b.addEventListener("click", function () { per = +b.getAttribute("data-per"); press(serve, b); draw(); }); });
    var barBtn = $(root, "[data-bar]");
    barBtn.addEventListener("click", function () { bar = !bar; barBtn.setAttribute("aria-pressed", bar ? "true" : "false"); draw(); });
    draw();
  });

  // Forms: one script, every way ---------------------------------------------------------------------------------
  $$(document, "[data-px-embed]").forEach(function (root) {
    var modes = $$(root, "[data-mode]");
    var code = $(root, "[data-code]");
    var page = $(root, "[data-px-site]");
    var copy = $(root, "[data-copy]");
    modes.forEach(function (b) {
      b.addEventListener("click", function () {
        press(modes, b);
        page.setAttribute("data-show", b.getAttribute("data-mode"));
        code.textContent = b.getAttribute("data-snippet");
      });
    });
    if (copy) copy.addEventListener("click", function () {
      var done = function () { copy.textContent = "Copied"; setTimeout(function () { copy.textContent = "Copy"; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(code.textContent).then(done, function () {}); else done();
    });
  });

  // Meetings: a booking calendar on real dates -----------------------------------------------------------------
  function offsetMin(ms, tz) {
    var p = new Intl.DateTimeFormat("en-US", { timeZone: tz, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" }).formatToParts(new Date(ms));
    var g = function (t) { return +p.filter(function (x) { return x.type === t; })[0].value; };
    return (Date.UTC(g("year"), g("month") - 1, g("day"), g("hour") % 24, g("minute"), g("second")) - ms) / 60000;
  }
  function zoned(y, m, d, h, min, tz) {
    var guess = Date.UTC(y, m, d, h, min);
    var off = offsetMin(guess, tz);
    var ms = guess - off * 60000;
    var off2 = offsetMin(ms, tz);
    return off2 === off ? ms : guess - off2 * 60000;
  }
  var dayKey = function (ms, tz) { return new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date(ms)); };
  var hash = function (n) { n = (n ^ 61) ^ (n >>> 16); n = n + (n << 3); n = n ^ (n >>> 4); n = n * 0x27d4eb2d; return (n ^ (n >>> 15)) >>> 0; };

  $$(document, "[data-book-demo]").forEach(function (root) {
    var HOST_TZ = "America/New_York";
    var PEOPLE = JSON.parse($(root, "[data-people]").textContent);
    var KINDS = JSON.parse($(root, "[data-kinds]").textContent);
    var mine = (Intl.DateTimeFormat().resolvedOptions().timeZone) || "UTC";
    var zones = [[mine, "Your time"], ["America/New_York", "New York"], ["Europe/London", "London"], ["Asia/Tokyo", "Tokyo"]].filter(function (z, i, all) { return all.findIndex(function (x) { return x[0] === z[0]; }) === i; });
    var kind = "one", tz = mine, month = null, day = null, slot = null;
    var head = $(root, "[data-head]"), cal = $(root, "[data-cal]"), times = $(root, "[data-times]"), zoneBox = $(root, "[data-zones]");
    var pick = $(root, "[data-step='pick']"), form = $(root, "[data-step='details']"), done = $(root, "[data-step='done']");
    var kindBtns = $$(root, "[data-kind]");
    var counts = { LK: 3, SB: 4, MO: 5 };

    function slots() {
      var k = KINDS[kind], out = [], now = Date.now(), soonest = now + 4 * 3600e3;
      var start = new Date(now);
      for (var i = 0; i < 42; i++) {
        var d = new Date(Date.UTC(start.getUTCFullYear(), start.getUTCMonth(), start.getUTCDate() + i));
        var wd = d.getUTCDay();
        if (wd === 0 || wd === 6) continue;
        var y = d.getUTCFullYear(), m = d.getUTCMonth(), dd = d.getUTCDate(), dn = Math.floor(d.getTime() / 864e5);
        if (k.group) {
          if (wd !== 4) continue;
          var at = zoned(y, m, dd, 11, 0, HOST_TZ);
          if (at > soonest) out.push({ at: at, host: k.hosts[0], seats: 20 - (9 + (hash(dn) % 9)) });
          continue;
        }
        if (hash(dn * 7) % 9 === 0) continue; // a fully booked day now and then
        for (var h = 9; h < 17; h++) for (var mm = 0; mm < 60; mm += 30) {
          var ms = zoned(y, m, dd, h, mm, HOST_TZ);
          if (ms < soonest) continue;
          var free = k.hosts.filter(function (p, j) { return hash(dn * 97 + h * 13 + mm + j * 7919) % 4 !== 0; });
          if (!free.length) continue;
          // Round robin: the free host with the fewest meetings this week takes it.
          free.sort(function (a, b) { return (counts[a] || 0) - (counts[b] || 0); });
          out.push({ at: ms, host: free[0] });
        }
      }
      return out;
    }
    var fmt = function (ms, o) { return new Intl.DateTimeFormat("en-US", Object.assign({ timeZone: tz }, o)).format(new Date(ms)); };
    function person(k) { var p = PEOPLE[k]; return '<span class="person"><span class="av" style="background:' + p[0] + '">' + k + "</span>" + p[1] + "</span>"; }

    function drawHead() {
      var k = KINDS[kind];
      head.innerHTML = '<div class="px-bk__who">' + k.hosts.map(function (h) { return '<span class="av av--lg" style="background:' + PEOPLE[h][0] + '">' + h + "</span>"; }).join("") + "</div>" +
        "<div><b>" + k.name + "</b><small>" + k.line + "</small></div>";
    }
    function draw() {
      var all = slots();
      var byDay = {};
      all.forEach(function (s) { (byDay[dayKey(s.at, tz)] = byDay[dayKey(s.at, tz)] || []).push(s); });
      var keys = Object.keys(byDay).sort();
      if (!month) month = keys[0] ? keys[0].slice(0, 7) : dayKey(Date.now(), tz).slice(0, 7);
      if (!day || !byDay[day]) day = keys.filter(function (k) { return k.slice(0, 7) === month; })[0] || null;
      var y = +month.slice(0, 4), m = +month.slice(5, 7) - 1;
      var first = new Date(Date.UTC(y, m, 1)), lead = (first.getUTCDay() + 6) % 7, len = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
      var today = dayKey(Date.now(), tz);
      var months = Array.from(new Set(keys.map(function (k) { return k.slice(0, 7); })));
      var mi = months.indexOf(month);
      var html = '<div class="px-bk__mh"><b>' + new Intl.DateTimeFormat("en-US", { month: "long", year: "numeric", timeZone: "UTC" }).format(first) + "</b>" +
        '<span><button type="button" data-mon="-1" aria-label="Earlier month"' + (mi <= 0 ? " disabled" : "") + '>&lsaquo;</button><button type="button" data-mon="1" aria-label="Later month"' + (mi < 0 || mi >= months.length - 1 ? " disabled" : "") + ">&rsaquo;</button></span></div>" +
        '<div class="px-bk__grid" role="grid"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span>';
      for (var i = 0; i < lead; i++) html += "<i></i>";
      for (var d = 1; d <= len; d++) {
        var k = month + "-" + (d < 10 ? "0" : "") + d;
        var open = !!byDay[k];
        html += '<button type="button" data-day="' + k + '"' + (open ? "" : " disabled") + (k === day ? ' aria-pressed="true"' : "") + (k === today ? ' class="is-today"' : "") + ">" + d + "</button>";
      }
      cal.innerHTML = html + "</div>";
      $$(cal, "[data-day]").forEach(function (b) { b.addEventListener("click", function () { day = b.getAttribute("data-day"); slot = null; draw(); }); });
      $$(cal, "[data-mon]").forEach(function (b) { b.addEventListener("click", function () { month = months[mi + +b.getAttribute("data-mon")]; day = null; draw(); }); });
      var list = day ? byDay[day] : [];
      var label = day ? fmt(list[0].at, { weekday: "long", month: "short", day: "numeric" }) : "No times this month";
      times.innerHTML = "<b>" + label + "</b>" + list.map(function (s, j) {
        return '<button type="button" data-slot="' + j + '">' + fmt(s.at, { hour: "numeric", minute: "2-digit" }) + (s.seats != null ? "<small>" + s.seats + " seats left</small>" : "") + "</button>";
      }).join("");
      $$(times, "[data-slot]").forEach(function (b) {
        b.addEventListener("click", function () {
          slot = list[+b.getAttribute("data-slot")];
          pick.hidden = true;
          form.hidden = false;
          $(form, "[data-when]").innerHTML = fmt(slot.at, { weekday: "long", month: "long", day: "numeric" }) + ", " + fmt(slot.at, { hour: "numeric", minute: "2-digit", timeZoneName: "short" }) + "<br>with " + person(slot.host);
          var input = $(form, "input");
          if (input) input.focus({ preventScroll: true });
        });
      });
      zoneBox.innerHTML = zones.map(function (z) {
        var city = z[0].split("/").pop().replace(/_/g, " ");
        return '<button type="button" data-tz="' + z[0] + '" aria-pressed="' + (z[0] === tz) + '">' + (z[1] === "Your time" ? "Your time (" + city + ")" : z[1]) + "</button>";
      }).join("");
      $$(zoneBox, "[data-tz]").forEach(function (b) { b.addEventListener("click", function () { tz = b.getAttribute("data-tz"); month = null; day = null; draw(); }); });
    }
    kindBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        kind = b.getAttribute("data-kind");
        press(kindBtns, b);
        month = null; day = null; slot = null;
        pick.hidden = false; form.hidden = true; done.hidden = true;
        drawHead(); draw();
      });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = $(form, "[name=name]").value.trim(), email = $(form, "[name=email]").value.trim();
      var err = $(form, "[data-err]");
      if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { err.hidden = false; return; }
      err.hidden = true;
      if (counts[slot.host] != null) counts[slot.host]++;
      form.hidden = true;
      done.hidden = false;
      var dayBefore = slot.at - 864e5, hourBefore = slot.at - 3600e3;
      $(done, "[data-done-when]").innerHTML = fmt(slot.at, { weekday: "long", month: "long", day: "numeric" }) + ", " + fmt(slot.at, { hour: "numeric", minute: "2-digit", timeZoneName: "short" }) + " with " + person(slot.host);
      $(done, "[data-done-line]").innerHTML =
        "<li><b>Now</b>Confirmation to " + email.replace(/[<>&"]/g, "") + ", with the invite and a Google Meet link</li>" +
        "<li><b>" + fmt(dayBefore, { weekday: "short", hour: "numeric", minute: "2-digit" }) + "</b>Reminder, a day before</li>" +
        "<li><b>" + fmt(hourBefore, { hour: "numeric", minute: "2-digit" }) + "</b>Reminder, an hour before</li>" +
        "<li><b>" + fmt(slot.at, { hour: "numeric", minute: "2-digit" }) + "</b>The meeting</li>";
    });
    $(form, "[data-back]").addEventListener("click", function () { form.hidden = true; pick.hidden = false; });
    $(done, "[data-again]").addEventListener("click", function () { done.hidden = true; pick.hidden = false; slot = null; draw(); });
    drawHead();
    draw();
  });

  // Meetings: the reminder line runs when it comes into view ---------------------------------------------------
  var seen = $$(document, "[data-inview]");
  if (seen.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } }); }, { threshold: 0.35 });
    seen.forEach(function (el) { io.observe(el); });
  } else seen.forEach(function (el) { el.classList.add("is-in"); });

  // Routing: answer like a lead, watch the rule decide ---------------------------------------------------------
  $$(document, "[data-route-demo]").forEach(function (root) {
    var PEOPLE = JSON.parse($(root, "[data-people]").textContent);
    var counts = { MO: 5, LK: 3, SB: 4, RJ: 2 };
    var away = { RJ: true };
    var a = { size: "small", country: "us", budget: "mid" };
    var rules = $$(root, "[data-rule]");
    var result = $(root, "[data-result]"), why = $(root, "[data-why]"), log = $(root, "[data-log]"), team = $(root, "[data-team]");
    var n = 0;
    var person = function (k) { var p = PEOPLE[k]; return '<span class="person"><span class="av" style="background:' + p[0] + '">' + k + "</span>" + p[1] + "</span>"; };
    function turn(pool) {
      var free = pool.filter(function (k) { return !away[k]; });
      free.sort(function (x, y) { return counts[x] - counts[y]; });
      return free[0];
    }
    function decide() {
      if (a.size === "large") { var p1 = turn(["MO", "SB"]); return { rule: 0, what: "Books Enterprise demo with " + person(p1), who: p1, why: "Rule 1: 51 or more people goes to the enterprise team. " + PEOPLE[p1][1] + " has the fewest meetings there this week." }; }
      if (a.country === "de") return { rule: 1, what: "Books Sales demo with " + person("LK"), who: "LK", why: "Rule 2: leads in Germany book with Lena, who speaks German." };
      if (a.budget === "low") return { rule: 2, what: "Gets the Starter guide by email", who: null, why: "Rule 3: budgets under $1,000 get the guide instead of a call." };
      var p4 = turn(["MO", "SB", "RJ"]);
      return { rule: 3, what: "Books Sales demo with " + person(p4), who: p4, why: "No rule above matched, so the sales team takes turns. " + PEOPLE[p4][1] + " has the fewest meetings this week" + (away.RJ ? ", and Rae is away." : ".") };
    }
    function drawTeam() {
      team.innerHTML = Object.keys(counts).map(function (k) {
        return '<li class="' + (away[k] ? "is-away" : "") + '">' + person(k) + "<b>" + counts[k] + "</b><small>" + (away[k] ? "Away" : "this week") + "</small></li>";
      }).join("");
    }
    function draw() {
      var d = decide();
      rules.forEach(function (r, i) {
        r.classList.toggle("is-hit", i === d.rule);
        r.classList.toggle("is-miss", i < d.rule);
        r.classList.toggle("is-later", i > d.rule);
      });
      result.innerHTML = d.what;
      why.textContent = d.why;
      result.classList.remove("is-new"); void result.offsetWidth; result.classList.add("is-new");
      return d;
    }
    $$(root, "[data-q]").forEach(function (group) {
      var btns = $$(group, "button");
      btns.forEach(function (b) { b.addEventListener("click", function () { a[group.getAttribute("data-q")] = b.getAttribute("data-v"); press(btns, b); draw(); }); });
    });
    $(root, "[data-send]").addEventListener("click", function () {
      var d = draw();
      n++;
      if (d.who) counts[d.who]++;
      var li = document.createElement("li");
      li.innerHTML = "<b>Lead " + n + "</b>" + d.what.replace(/^Books |^Gets /, "") + "<small>Rule " + (d.rule + 1) + "</small>";
      log.insertBefore(li, log.firstChild);
      while (log.children.length > 4) log.removeChild(log.lastChild);
      drawTeam();
      draw();
    });
    drawTeam();
    draw();
  });

  // Routing: round robin with weights and away days ------------------------------------------------------------
  $$(document, "[data-rr]").forEach(function (root) {
    var rows = $$(root, "[data-rep]");
    var reps = rows.map(function (r) { return { el: r, w: 1, n: 0, away: false }; });
    var timer = null;
    function draw(last) {
      var max = Math.max.apply(null, reps.map(function (r) { return r.n; }).concat([1]));
      reps.forEach(function (r, i) {
        $(r.el, "[data-w]").textContent = r.w;
        $(r.el, "[data-n]").textContent = r.n;
        $(r.el, "[data-fill]").style.width = (r.n / max) * 100 + "%";
        r.el.classList.toggle("is-away", r.away);
        r.el.classList.toggle("is-last", i === last);
        $(r.el, "[data-away]").setAttribute("aria-pressed", r.away ? "true" : "false");
      });
      $(root, "[data-total]").textContent = reps.reduce(function (s, r) { return s + r.n; }, 0);
    }
    function one() {
      var free = reps.map(function (r, i) { return { r: r, i: i }; }).filter(function (x) { return !x.r.away; });
      if (!free.length) return -1;
      // The most due: fewest leads for their weight; ties go to whoever has fewer, then the order on the list.
      free.sort(function (x, y) { return x.r.n / x.r.w - y.r.n / y.r.w || x.r.n - y.r.n || x.i - y.i; });
      free[0].r.n++;
      return free[0].i;
    }
    function send(count) {
      clearInterval(timer);
      if (reduce) { var l = -1; for (var i = 0; i < count; i++) l = one(); draw(l); return; }
      var left = count;
      timer = setInterval(function () { draw(one()); if (--left <= 0) clearInterval(timer); }, 70);
    }
    reps.forEach(function (r) {
      $(r.el, "[data-wless]").addEventListener("click", function () { r.w = Math.max(1, r.w - 1); draw(); });
      $(r.el, "[data-wmore]").addEventListener("click", function () { r.w = Math.min(10, r.w + 1); draw(); });
      $(r.el, "[data-away]").addEventListener("click", function () { r.away = !r.away; draw(); });
    });
    $(root, "[data-send1]").addEventListener("click", function () { send(1); });
    $(root, "[data-send20]").addEventListener("click", function () { send(20); });
    $(root, "[data-reset]").addEventListener("click", function () { clearInterval(timer); reps.forEach(function (r) { r.n = 0; }); draw(); });
    draw();
  });
})();
