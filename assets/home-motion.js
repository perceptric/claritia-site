/* Home page motion: the Branding scan and the lead record.
   The HTML in index.html is the finished state. When a section comes on screen this script resets it and plays it
   forward. With JavaScript off, reduced motion on, or ?still=1 in the address, nothing here runs. */
(function () {
  if (/[?&]still=/.test(location.search) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;

  function onView(el, fn, threshold) {
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io.disconnect(); fn(); }
    }, { threshold: threshold || 0.4 });
    io.observe(el);
  }
  function timeline() {
    var timers = [];
    return {
      at: function (ms, fn) { timers.push(setTimeout(fn, ms)); },
      clear: function () { timers.forEach(clearTimeout); timers = []; }
    };
  }
  function hide(el) { el.classList.add('pt-a', 'pt-hide'); }
  function show(el) { el.classList.remove('pt-hide'); }
  function pop(el) { el.classList.remove('pt-pop'); void el.offsetWidth; el.classList.add('pt-pop'); }

  /* ---------- Branding: read the website, pick up the brand, apply it ---------- */
  (function () {
    var field = document.querySelector('.h-b-field');
    if (!field) return;
    var bar = field.querySelector('.h-site-bar'), ok = bar && bar.querySelector('.h-ok');
    var split = field.querySelector('.h-b-split'), card = document.getElementById('o-colors');
    if (!bar || !ok || !split || !card) return;

    var urlNode = [].slice.call(bar.childNodes).filter(function (n) { return n.nodeType === 3 && n.textContent.trim(); })[0];
    if (!urlNode) return;
    var URL = urlNode.textContent.trim();
    var url = document.createElement('span');
    url.className = 'hm-url';
    url.textContent = URL;
    bar.replaceChild(url, urlNode);

    var muted = card.querySelector('.h-muted'), mutedText = muted ? muted.textContent : '';
    var sw = [].slice.call(card.querySelectorAll('.h-sw > div'));
    var fontLine = card.lastElementChild, fontText = fontLine.textContent;
    var tl = timeline(), site = null, status = null, playing = false;

    var ROOF = '<svg viewBox="0 0 300 340" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><path d="M30 190 L150 90 L270 190" fill="none" stroke="#f26b1d" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"/><path d="M70 175 V260 H230 V175" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="6"/><rect x="130" y="205" width="40" height="55" fill="rgba(255,255,255,.12)"/></svg>';
    var MARK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 13 L12 5 L21 13" fill="none" stroke="#f26b1d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 12 V19 H18 V12" fill="none" stroke="#1f2328" stroke-width="2.4"/></svg>';

    function finish() {
      tl.clear();
      playing = false;
      if (site) { site.remove(); site = null; }
      if (status) { status.remove(); status = null; }
      url.textContent = URL;
      url.classList.remove('pt-caret');
      ok.hidden = false;
      split.style.opacity = '';
      split.style.transition = '';
      if (muted) muted.textContent = mutedText;
      sw.forEach(function (d) { d.classList.remove('hm-hide'); });
      fontLine.textContent = fontText;
    }

    function play() {
      finish();
      playing = true;
      // start state
      url.textContent = '';
      ok.hidden = true;
      status = document.createElement('span');
      status.className = 'hm-st';
      status.hidden = true;
      status.innerHTML = '<i class="hm-spin"></i><span>Reading site</span>';
      bar.appendChild(status);
      split.style.transition = 'opacity 500ms var(--ease-out)';
      split.style.opacity = '0';
      if (muted) muted.textContent = 'Waiting for your website';
      sw.forEach(function (d) { d.classList.add('hm-hide'); });
      fontLine.textContent = '';

      site = document.createElement('div');
      site.className = 'hm-site pt-a pt-hide';
      site.setAttribute('aria-hidden', 'true');
      site.innerHTML =
        '<div class="hm-nav"><span class="hm-logo">' + MARK + 'Ridgeline <span>Roofing</span></span><span class="hm-links"><i></i><i></i><i></i></span><span class="hm-cta">Call 303-555-0148</span></div>' +
        '<div class="hm-hero"><div class="hm-copy"><h6>Roofs built for Colorado storms</h6><p>Family run since 1998. Straight talk, real prices and a written quote the same day.</p><span class="hm-btn">Get a free estimate</span></div>' +
        '<div class="hm-photo">' + ROOF + '</div></div><div class="hm-beam"></div>';
      site.style.left = split.offsetLeft + 'px';
      site.style.top = split.offsetTop + 'px';
      site.style.width = split.offsetWidth + 'px';
      site.style.height = split.offsetHeight + 'px';
      field.insertBefore(site, split.nextSibling);
      var beam = site.querySelector('.hm-beam');

      function pick(sel, label, place) { // place: 'side' (right of the box), 'left' or 'corner' (inside, top right)
        var el = site.querySelector(sel);
        if (!el || !el.offsetWidth) return null;
        var s = site.getBoundingClientRect(), r = el.getBoundingClientRect();
        var box = document.createElement('div');
        box.className = 'hm-pick' + (place === 'left' ? ' hm-left' : place === 'side' ? '' : ' hm-corner');
        box.style.left = (r.left - s.left - 5) + 'px';
        box.style.top = (r.top - s.top - 5) + 'px';
        box.style.width = (r.width + 10) + 'px';
        box.style.height = (r.height + 10) + 'px';
        box.innerHTML = '<b>' + label + '</b>';
        site.appendChild(box);
        void box.offsetWidth;
        box.classList.add('hm-on');
        return box;
      }
      function addSwatch(i) { if (sw[i]) { sw[i].classList.remove('hm-hide'); pop(sw[i].querySelector('i')); } }
      function typeFont(from, to, start, per) { // types fontText from character `from` up to `to`
        for (var i = from + 1; i <= to; i++) (function (i) { tl.at(start + (i - from) * per, function () { fontLine.textContent = fontText.slice(0, i); }); })(i);
      }
      var cut = fontText.indexOf(',') + 1 || fontText.length;

      var t = 250;
      tl.at(t, function () { url.classList.add('pt-caret'); });
      for (var i = 1; i <= URL.length; i++) (function (i) { tl.at(t + i * 45, function () { url.textContent = URL.slice(0, i); }); })(i);
      t += URL.length * 45 + 350;
      tl.at(t, function () { url.classList.remove('pt-caret'); status.hidden = false; pop(status); show(site); });
      t += 600;
      tl.at(t, function () { beam.classList.add('hm-run'); beam.style.transform = 'translateY(' + site.offsetHeight + 'px)'; });
      var picks = [];
      // the beam takes 2400ms from the top to the bottom; each find lands as it passes
      tl.at(t + 250, function () { picks.push(pick('.hm-logo', 'Logo', 'side')); if (muted) muted.textContent = 'Reading ' + URL; });
      tl.at(t + 500, function () { picks.push(pick('.hm-cta', 'Charcoal #1F2328', 'left')); addSwatch(1); });
      tl.at(t + 900, function () { picks.push(pick('.hm-copy h6', 'Headings: Barlow Condensed')); });
      typeFont(0, cut, t + 950, 18);
      tl.at(t + 1400, function () { picks.push(pick('.hm-copy p', 'Text: Barlow · plain, friendly voice')); });
      typeFont(cut, fontText.length, t + 1450, 18);
      tl.at(t + 1800, function () { picks.push(pick('.hm-btn', 'Button: #F26B1D')); addSwatch(0); });
      tl.at(t + 2050, function () { addSwatch(2); });
      tl.at(t + 2250, function () { addSwatch(3); });
      tl.at(t + 2450, function () { addSwatch(4); });
      t += 2900;
      tl.at(t, function () {
        picks.forEach(function (p) { if (p) p.classList.add('hm-off'); });
        status.innerHTML = '<span>Applying to your forms</span>';
        if (muted) muted.textContent = mutedText;
      });
      t += 500;
      tl.at(t, function () { site.classList.add('hm-gone'); split.style.opacity = '1'; });
      t += 600;
      tl.at(t, function () { status.remove(); status = null; ok.hidden = false; pop(ok); });
      tl.at(t + 700, function () { finish(); });
    }

    // The scan belongs to "Your colors and fonts". Picking another item stops it; picking this one again replays it.
    document.querySelectorAll('.h-acc-item').forEach(function (it) {
      it.addEventListener('click', function () {
        if (it.dataset.o === 'o-colors') { if (!playing) play(); }
        else finish();
      });
    });
    document.addEventListener('visibilitychange', function () { if (document.hidden && playing) finish(); });
    onView(field, function () { if (card.classList.contains('h-on')) play(); }, 0.45);
  })();

  /* ---------- Lead record: each step lands on the record in order ---------- */
  (function () {
    var rec = document.querySelector('.h-rec-card');
    if (!rec) return;
    var rows = [].slice.call(rec.querySelectorAll('.h-timeline li')), sync = rec.querySelector('.h-rec-sync');
    var dot = rec.querySelector('.h-live-dot'), tl = timeline();
    rows.concat(sync ? [sync] : []).forEach(hide);
    onView(rec, function () {
      if (dot) dot.classList.add('hm-pulse');
      rows.forEach(function (r, i) {
        tl.at(250 + i * 450, function () { show(r); pop(r.querySelector('.h-node')); });
      });
      if (sync) tl.at(250 + rows.length * 450 + 200, function () { show(sync); pop(sync.querySelector('svg')); });
    }, 0.3);
  })();
})();
