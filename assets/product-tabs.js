/* Home page product tabs: each panel plays its story when it is shown.
   The HTML in index.html is each panel's finished state. This script resets a panel to its start and plays it
   forward, then restores the finished HTML when the panel is left. With JavaScript off, reduced motion on, or
   ?still=1 in the address, nothing here runs and the finished panels show as they are.
   While the panel is on screen the tabs move on by themselves, with a progress line under the active tab.
   The first click or arrow key on a tab turns that off. */
(function () {
  var section = document.getElementById('product');
  if (!section || !window.hSelectTab) return;
  if (/[?&]still=/.test(location.search) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var HOLD = 2600; // time on the finished state before the next tab
  var tabs = [].slice.call(section.querySelectorAll('.h-tab'));
  var panels = {};
  tabs.forEach(function (t) {
    var id = t.getAttribute('aria-controls'), p = document.getElementById(id), st = p && p.querySelector('.h-stage');
    if (st) panels[id] = { stage: st, html: st.innerHTML };
    var bar = document.createElement('span');
    bar.className = 'pt-prog';
    bar.setAttribute('aria-hidden', 'true');
    t.appendChild(bar);
  });

  var timers = [], current = null, auto = true, inView = false, started = false, advanceTimer = null, advancing = false, busyUntil = 0;
  function at(ms, fn) { timers.push(setTimeout(fn, ms)); }
  function clear() { timers.forEach(clearTimeout); timers = []; }
  function all(root, sel) { return [].slice.call(root.querySelectorAll(sel)); }
  function hide(el) { el.classList.add('pt-a', 'pt-hide'); }
  function show(el) { el.classList.remove('pt-hide'); }
  function pop(el) { el.classList.remove('pt-pop'); void el.offsetWidth; el.classList.add('pt-pop'); }
  function ease(x) { return 1 - Math.pow(1 - x, 3); }
  function type(el, text, per, start, caret) {
    at(start, function () { el.textContent = ''; if (caret) el.classList.add('pt-caret'); });
    for (var i = 1; i <= text.length; i++) (function (i) { at(start + i * per, function () { el.textContent = text.slice(0, i); }); })(i);
    if (caret) at(start + text.length * per + 250, function () { el.classList.remove('pt-caret'); });
    return start + text.length * per;
  }
  function count(el, from, to, suffix, start, dur) {
    var steps = Math.max(1, Math.round(dur / 40));
    for (var k = 1; k <= steps; k++) (function (k) {
      at(start + k * dur / steps, function () { el.textContent = Math.round(from + (to - from) * ease(k / steps)) + suffix; });
    })(k);
  }

  /* A fake cursor inside a panel window. Targets can be elements or functions that return one. */
  function cursor(win) {
    var c = document.createElement('span');
    c.className = 'pt-cursor';
    c.setAttribute('aria-hidden', 'true');
    c.innerHTML = '<svg viewBox="0 0 17 20"><path d="M1 1 L1 15.5 L4.8 12 L7.5 18 L10 17 L7.4 11.2 L12.5 11 Z"/></svg>';
    win.appendChild(c);
    function place(target, fx, fy) {
      var el = typeof target === 'function' ? target() : target;
      if (!el) return;
      var w = win.getBoundingClientRect(), r = el.getBoundingClientRect();
      c.style.transform = 'translate(' + (r.left - w.left + r.width * (fx == null ? .55 : fx)) + 'px,' + (r.top - w.top + r.height * (fy == null ? .6 : fy)) + 'px)';
    }
    return {
      show: function (ms, target, fx, fy) {
        at(ms, function () { c.style.transition = 'none'; place(target, fx, fy); void c.offsetWidth; c.style.transition = ''; c.classList.add('pt-on'); });
      },
      move: function (ms, target, fx, fy) { at(ms, function () { place(target, fx, fy); }); },
      press: function (ms) {
        at(ms, function () { c.classList.add('pt-down'); });
        at(ms + 160, function () { c.classList.remove('pt-down'); });
      },
      hide: function (ms) { at(ms, function () { c.classList.remove('pt-on'); }); }
    };
  }

  /* Each panel sets its start state right away, schedules its steps, and returns how long they take (ms). */
  var RUN = {
    'p-forms': function (st) {
      var win = st.querySelector('.h-window'), kids = [].slice.call(st.querySelector('.h-chat').children);
      var prompt = kids[0], ready = kids[1], metas = kids.slice(2, 5), ask2 = kids[5], done = kids[6], ask = kids[7];
      var card = st.querySelector('.h-formcard'), parts = [].slice.call(card.children);
      var opts = all(card, '.h-opt'), pick = card.querySelector('.h-opt.h-on'), input = card.querySelector('.h-f-input');
      var hl = card.querySelector('.h-highlight'), em = hl.querySelector('em');
      var promptText = prompt.textContent.trim(), inputText = input.textContent, ask2Text = ask2.textContent.trim();
      var askLabel = document.createElement('span');
      askLabel.textContent = ask.firstChild.textContent.trim();
      ask.replaceChild(askLabel, ask.firstChild);
      var send = ask.querySelector('b');
      [ready, ask2, done].concat(metas, parts, opts, [em]).forEach(hide);
      prompt.textContent = '';
      pick.classList.remove('h-on');
      card.classList.remove('h-rl');
      hl.classList.add('pt-nohl');
      input.textContent = '';
      var c = cursor(win);

      var t = type(prompt, promptText, 13, 250, true) + 300;
      at(t, function () { show(ready); });
      t += 300;
      at(t, function () { show(metas[0]); show(parts[0]); show(parts[1]); show(parts[2]); });
      opts.forEach(function (o, i) { at(t + 120 + i * 80, function () { show(o); }); });
      t += 500;
      at(t, function () { show(metas[1]); show(parts[3]); show(parts[4]); });
      t += 500;
      at(t, function () { show(metas[2]); card.classList.add('h-rl'); show(parts[5]); show(parts[6]); });
      t += 750;
      at(t, function () { askLabel.classList.add('pt-typed'); });
      t = type(askLabel, ask2Text, 32, t, true) + 300;
      at(t, function () { pop(send); askLabel.classList.remove('pt-typed'); askLabel.textContent = 'Ask for a change...'; show(ask2); });
      t += 500;
      at(t, function () { show(done); hl.classList.remove('pt-nohl'); hl.classList.add('pt-glow'); show(em); pop(em); });
      t += 750;
      c.show(t, card, .9, .95);
      c.move(t + 60, pick);
      t += 650;
      c.press(t);
      at(t, function () { pick.classList.add('h-on'); pop(pick); });
      t += 400;
      c.move(t, input, .3, .55);
      t += 600;
      c.press(t);
      t = type(input, inputText, 70, t + 120, true) + 500;
      c.hide(t);
      return t + 300;
    },

    'p-meet': function (st) {
      var win = st.querySelector('.h-window'), host = st.querySelector('.h-host');
      var days = all(st, '.h-cal-grid .h-d'), sel = st.querySelector('.h-cal-grid .h-sel');
      var open = days.filter(function (d) { return d.classList.contains('h-av') || d === sel; });
      var slotKids = [].slice.call(st.querySelector('.h-slots').children), pick = st.querySelector('.h-slot.h-pick');
      var pickHTML = pick.innerHTML;
      hide(host);
      open.forEach(function (d) { d.classList.remove('h-av', 'h-sel'); });
      slotKids.forEach(hide);
      pick.classList.remove('h-pick');
      pick.textContent = '10:30 am';
      var toast = document.createElement('div');
      toast.className = 'pt-toast';
      toast.innerHTML = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>Invite sent · Meet link added';
      hide(toast);
      win.appendChild(toast);
      var c = cursor(win);

      var t = 150;
      at(t, function () { show(host); });
      t += 350;
      open.forEach(function (d, i) { at(t + i * 45, function () { d.classList.add('h-av'); pop(d); }); });
      t += open.length * 45 + 350;
      c.show(t, host, .95, .5);
      c.move(t + 60, sel);
      t += 650;
      c.press(t);
      at(t, function () { sel.classList.remove('h-av'); sel.classList.add('h-sel'); pop(sel); });
      t += 250;
      slotKids.forEach(function (s, i) { at(t + i * 90, function () { show(s); }); });
      t += slotKids.length * 90 + 350;
      c.move(t, pick);
      t += 600;
      c.press(t);
      at(t, function () { pick.classList.add('h-pick'); pick.innerHTML = pickHTML; pop(pick); });
      t += 500;
      c.move(t, function () { return pick.lastElementChild; });
      t += 550;
      c.press(t);
      at(t, function () { pick.classList.remove('h-pick'); pick.classList.add('pt-booked'); pick.textContent = 'Booked · 10:30 am'; pop(pick); });
      t += 300;
      at(t, function () { show(toast); });
      c.hide(t + 250);
      return t + 900;
    },

    'p-route': function (st) {
      var lead = st.querySelector('.h-rt-lead'), mark = lead.querySelector('mark'), line = st.querySelector('.h-rt .h-fline');
      var ifNode = st.querySelector('.h-rt-if'), rows = all(st, '.h-rt-br'), hit = st.querySelector('.h-rt-br.h-hit');
      var tag = hit.querySelector('.h-tag'), rep = hit.querySelector('.h-rt-rep');
      [lead, ifNode, tag].concat(rows).forEach(hide);
      line.classList.remove('h-done');
      hit.classList.remove('h-hit');
      mark.classList.add('pt-m');

      var t = 200;
      at(t, function () { show(lead); });
      t += 450;
      at(t, function () { mark.classList.add('pt-on'); });
      t += 350;
      at(t, function () { line.classList.add('h-done'); });
      t += 300;
      at(t, function () { show(ifNode); ifNode.classList.add('pt-ring'); });
      t += 350;
      rows.forEach(function (r, i) { at(t + i * 150, function () { show(r); }); });
      t += rows.length * 150 + 350;
      rows.forEach(function (r, i) {
        if (r === hit) return;
        at(t + i * 220, function () { r.classList.add('pt-skip'); });
      });
      at(t + 220, function () { ifNode.classList.remove('pt-ring'); hit.classList.add('h-hit'); pop(rep); });
      t += 700;
      at(t, function () { show(tag); pop(tag); });
      return t + 1000;
    },

    'p-mail': function (st) {
      var win = st.querySelector('.h-window'), flow = st.querySelector('.h-wf');
      var nodes = all(flow, ':scope > .h-fnode'), lines = all(flow, '.h-fline'), pair = all(flow, '.h-fpair .h-fnode');
      var split = flow.querySelector('.h-fsplit');
      var tags = nodes.map(function (n) { return n.querySelector(':scope > .h-tag'); });
      var ai = nodes[2], aiSmall = ai.querySelector('small'), aiTag = tags[2], aiText = aiSmall.textContent;
      var waitNode = nodes[3];
      nodes.concat(pair).forEach(function (n) { n.classList.add('pt-dim'); });
      split.classList.add('pt-dim');
      tags.forEach(function (g) { if (g) hide(g); });
      lines.forEach(function (l) { l.classList.remove('h-done'); });
      var c = cursor(win);
      function light(i, ms) { at(ms, function () { nodes.forEach(function (n) { n.classList.remove('pt-ring'); }); nodes[i].classList.remove('pt-dim'); nodes[i].classList.add('pt-ring'); pop(nodes[i]); }); }
      function tagTo(g, text, tone, ms) {
        at(ms, function () { g.textContent = text; g.className = 'h-tag' + (tone ? ' ' + tone : '') + ' pt-a'; pop(g); });
      }

      var t = 200;
      light(0, t);
      at(t + 250, function () { show(tags[0]); pop(tags[0]); });
      t += 650;
      at(t, function () { lines[0].classList.add('h-done'); });
      t += 300;
      light(1, t);
      at(t + 300, function () { show(tags[1]); pop(tags[1]); });
      t += 700;
      at(t, function () { lines[1].classList.add('h-done'); });
      t += 300;
      light(2, t);
      tagTo(aiTag, 'Writing', 'h-p pt-shimmer', t + 150);
      t = type(aiSmall, 'Hi Priya, thanks for booking Tuesday at 10:30...', 22, t + 200, true) + 250;
      tagTo(aiTag, 'Needs approval', 'h-o', t);
      var approve = document.createElement('span');
      approve.className = 'pt-approve';
      approve.textContent = 'Approve';
      at(t, function () { ai.insertBefore(approve, aiTag); pop(approve); });
      c.show(t + 100, ai, .35, 1.6);
      c.move(t + 200, approve);
      t += 800;
      c.press(t);
      at(t, function () { approve.remove(); aiSmall.textContent = aiText; });
      tagTo(aiTag, 'Sent', 'h-g', t);
      c.hide(t + 350);
      t += 450;
      at(t, function () { lines[2].classList.add('h-done'); });
      t += 300;
      light(3, t);
      at(t + 200, function () { show(tags[3]); pop(tags[3]); waitNode.classList.add('pt-tick'); });
      t += 1100;
      at(t, function () {
        waitNode.classList.remove('pt-ring');
        nodes[4].classList.remove('pt-dim');
        show(tags[4]);
        split.classList.remove('pt-dim');
        pair.forEach(function (n) { n.classList.remove('pt-dim'); });
      });
      return t + 900;
    },

    'p-stats': function (st) {
      var win = st.querySelector('.h-window'), kb = all(st, '.h-kpi b'), rows = all(st, '.h-bar-row'), hint = st.querySelector('.h-hint');
      st.querySelector('.h-bars').classList.add('pt-bars');
      var vals = kb.map(function (b) { return b.textContent; });
      var fills = rows.map(function (r) { return r.querySelector('.h-bar-fill'); });
      var nums = rows.map(function (r) { return r.querySelector('b'); });
      var widths = fills.map(function (f) { return parseInt(f.style.width, 10); });
      var warn = st.querySelector('.h-bar-row.h-warn'), wi = rows.indexOf(warn);
      kb.forEach(function (b, i) { b.textContent = vals[i].indexOf('%') > -1 ? '0%' : '0'; });
      fills.forEach(function (f) { f.style.width = '0%'; });
      nums.forEach(function (n) { n.textContent = '0%'; });
      warn.classList.remove('h-warn');
      var hintText = hint.lastChild;
      var fix = document.createElement('span');
      fix.className = 'pt-fix';
      fix.textContent = 'Make optional';
      hint.appendChild(fix);
      hide(hint);
      var c = cursor(win);

      var t = 200;
      kb.forEach(function (b, i) { count(b, 0, parseInt(vals[i], 10), vals[i].indexOf('%') > -1 ? '%' : '', t, 900); });
      t += 500;
      rows.forEach(function (r, i) {
        at(t + i * 170, function () { fills[i].style.width = widths[i] + '%'; });
        count(nums[i], 0, widths[i], '%', t + i * 170, 600);
      });
      t += rows.length * 170 + 500;
      at(t, function () { warn.classList.add('h-warn', 'pt-pulse'); });
      t += 500;
      at(t, function () { show(hint); });
      t += 800;
      c.show(t, hint, .4, .6);
      c.move(t + 60, fix);
      t += 650;
      c.press(t);
      at(t, function () {
        fix.textContent = 'Optional now';
        fix.classList.add('pt-done');
        pop(fix);
        hintText.textContent = 'Phone number is optional now. More people reach Pick a time.';
        hint.classList.add('pt-good');
        warn.classList.remove('h-warn');
      });
      t += 300;
      var after = { }; after[wi] = 90; after[wi + 1] = 86; after[wi + 2] = 83;
      Object.keys(after).forEach(function (k, j) {
        k = +k;
        if (!rows[k]) return;
        at(t + j * 120, function () { fills[k].style.width = after[k] + '%'; });
        count(nums[k], widths[k], after[k], '%', t + j * 120, 600);
      });
      if (kb[1]) count(kb[1], parseInt(vals[1], 10), 118, '', t, 800);
      c.hide(t + 500);
      return t + 1300;
    }
  };

  function restore(id) { var p = panels[id]; if (p) p.stage.innerHTML = p.html; }
  function progress(tab, ms) {
    tabs.forEach(function (t) {
      var b = t.querySelector('.pt-prog');
      b.classList.remove('pt-run');
      b.style.transitionDuration = '';
    });
    if (!tab) return;
    var bar = tab.querySelector('.pt-prog');
    void bar.offsetWidth;
    bar.style.transitionDuration = ms + 'ms';
    bar.classList.add('pt-run');
  }
  function scheduleAdvance(id, ms) {
    clearTimeout(advanceTimer);
    advancing = false;
    progress(null);
    if (!auto || !inView) return;
    var i = tabs.findIndex(function (t) { return t.getAttribute('aria-controls') === id; });
    var total = ms + HOLD;
    advancing = true;
    progress(tabs[i], total);
    advanceTimer = setTimeout(function () {
      advancing = false;
      if (!auto || !inView || document.hidden) return;
      window.hSelectTab(tabs[(i + 1) % tabs.length]);
    }, total);
  }
  function play(id) {
    clear();
    if (current && current !== id) restore(current);
    current = id;
    restore(id);
    var run = RUN[id], ms = 0;
    if (run) {
      try { ms = run(panels[id].stage); } catch (e) { clear(); restore(id); ms = 0; }
    }
    busyUntil = Date.now() + ms;
    scheduleAdvance(id, ms);
  }
  function stop() {
    clear();
    clearTimeout(advanceTimer);
    advancing = false;
    progress(null);
    if (current) restore(current);
  }
  function selectedId() {
    var t = tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[0];
    return t.getAttribute('aria-controls');
  }
  function keepTabInView(tab) {
    var sc = section.querySelector('.h-tabs-scroll');
    if (!sc || sc.scrollWidth <= sc.clientWidth) return;
    sc.scrollTo({ left: tab.offsetLeft - (sc.clientWidth - tab.offsetWidth) / 2, behavior: 'smooth' });
  }

  window.hTabMotion = {
    onSelect: function (tab, byUser) {
      if (byUser) auto = false;
      else keepTabInView(tab);
      started = true;
      play(tab.getAttribute('aria-controls'));
    }
  };

  // Watch the panel windows, so a phone only plays a panel once its window is on screen.
  if ('IntersectionObserver' in window) {
    var vis = {};
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { vis[e.target.getAttribute('data-pt')] = e.isIntersecting; });
      var now = !!vis[current || selectedId()];
      if (now === inView) return;
      inView = now;
      if (!inView) { clearTimeout(advanceTimer); advancing = false; progress(null); return; }
      if (!started) { started = true; play(selectedId()); }
      else if (auto && !advancing) scheduleAdvance(current, Math.max(0, busyUntil - Date.now()));
    }, { threshold: 0.3 });
    Object.keys(panels).forEach(function (id) { panels[id].stage.setAttribute('data-pt', id); io.observe(panels[id].stage); });
  }
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop();
    else if (inView && current) play(current);
  });
})();
