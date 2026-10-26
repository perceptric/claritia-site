/* ═══════════════════════════════════════════════════════════════════════
   CLARITIA — MOTION
   Progressive enhancement only. Without this file every section is static
   and readable. Motion is one pinned story, one hero loop, one stack
   collapse and one closing draw; everything else is a quiet reveal.
   ═══════════════════════════════════════════════════════════════════════ */

(() => {
  'use strict';

  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = navigator.connection && navigator.connection.saveData;
  const lowPower = (navigator.hardwareConcurrency || 8) <= 2;
  const finePointer = window.matchMedia('(pointer: fine)').matches;
  let lenis = null;

  /* chrome works even when motion is off */
  initChrome();

  if (reduce || saveData || lowPower || !window.gsap || !window.ScrollTrigger) {
    root.classList.add('motion-off');
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  if (window.SplitText) gsap.registerPlugin(SplitText);
  gsap.defaults({ ease: 'power3.out', duration: 0.8 });
  ScrollTrigger.config({ ignoreMobileResize: true });

  if (finePointer && window.innerWidth >= 1024 && window.Lenis) initLenis();

  const mm = gsap.matchMedia();

  initHeroLines();
  initHeroLoop();
  initHeroCanvas();
  initSplitText();
  initReveals();
  initStory(mm);
  initStack(mm);
  initCounters();
  initTry();
  initClosing();
  initBilling();
  initProgress();

  document.fonts.ready.then(() => ScrollTrigger.refresh());
  window.addEventListener('load', () => ScrollTrigger.refresh(), { once: true });

  /* ── header details, anchors, smooth scroll ─────────────────────────── */
  function initChrome() {
    const header = document.querySelector('.site-head');
    if (!header) return;

    document.addEventListener('click', (event) => {
      header.querySelectorAll('details[open]').forEach((details) => {
        if (!details.contains(event.target)) details.open = false;
      });
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        header.querySelectorAll('details[open]').forEach((details) => { details.open = false; });
      }
    });

    const closeHeader = () => {
      header.querySelectorAll('details[open]').forEach((details) => { details.open = false; });
    };

    document.querySelectorAll('a[href^="#"]').forEach((link) => {
      link.addEventListener('click', (event) => {
        const hash = link.getAttribute('href');
        if (!hash || hash === '#') return;
        const target = document.querySelector(hash);
        if (!target) return;
        if (lenis) {
          event.preventDefault();
          lenis.scrollTo(target);
        }
        closeHeader();
      });
    });
  }

  function initLenis() {
    lenis = new Lenis({
      duration: 1.05,
      smoothWheel: true,
      wheelMultiplier: 0.9,
      touchMultiplier: 1.1,
      autoRaf: false
    });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
    root.classList.add('has-lenis');
  }

  /* ── hero line draw ──────────────────────────────────────────────────── */
  function initHeroLines() {
    const svg = document.querySelector('[data-hero-lines]');
    if (!svg) return;
    const paths = [...svg.querySelectorAll('path')];
    paths.forEach((path) => {
      const length = path.getTotalLength();
      path.style.strokeDasharray = String(length);
      path.style.strokeDashoffset = String(length);
    });
    gsap.to(paths, {
      strokeDashoffset: 0,
      duration: 1.8,
      ease: 'power2.out',
      stagger: 0.02,
      delay: 0.15,
      onComplete: () => paths.forEach((path) => { path.style.strokeDasharray = 'none'; })
    });
  }

  /* ── hero product loop ───────────────────────────────────────────────── */
  function initHeroLoop() {
    const preview = document.querySelector('[data-hero-preview]');
    if (!preview) return;
    const score = preview.querySelector('[data-hero-score]');
    const tag = preview.querySelector('[data-hero-tag]');
    const facts = preview.querySelectorAll('[data-hero-fact]');
    const events = preview.querySelectorAll('[data-hero-event]');
    const toast = preview.querySelector('[data-hero-toast]');
    if (!score || !tag || !toast || !events.length) return;

    const proxy = { value: 0 };
    const timeline = gsap.timeline({ repeat: -1, repeatDelay: 2.4, defaults: { ease: 'power2.out' } });

    timeline
      .set(score, { textContent: '0' })
      .set(tag, { autoAlpha: 0, y: -4 })
      .set(facts, { autoAlpha: 0.22 })
      .set(events, { autoAlpha: 0.18 })
      .set(toast, { autoAlpha: 0, y: 6 })
      .set(proxy, { value: 0 })
      .to(facts, { autoAlpha: 1, duration: 0.4, stagger: 0.08 })
      .to(events[0], { autoAlpha: 1, duration: 0.3 })
      .to(proxy, {
        value: 92,
        duration: 1.1,
        ease: 'power2.out',
        onUpdate: () => { score.textContent = String(Math.round(proxy.value)); }
      }, '-=0.15')
      .to(tag, { autoAlpha: 1, y: 0, duration: 0.3 }, '-=0.2')
      .to(events[1], { autoAlpha: 1, duration: 0.3 }, '-=0.1')
      .to(events[2], { autoAlpha: 1, duration: 0.3 }, '+=0.3')
      .to(toast, { autoAlpha: 1, y: 0, duration: 0.4 }, '-=0.1')
      .to({}, { duration: 2.2 });
  }

  /* ── hero canvas flow field ──────────────────────────────────────────── */
  function initHeroCanvas() {
    const canvas = document.querySelector('[data-hero-canvas]');
    const host = canvas && canvas.parentElement;
    const hero = canvas && canvas.closest('.hero');
    if (!canvas || !host || !hero) return;
    const context = canvas.getContext('2d');
    if (!context) return;

    const cores = navigator.hardwareConcurrency || 8;
    const count = window.innerWidth < 768 || cores <= 4 ? 18 : 32;
    const palette = [[24, 226, 153], [88, 233, 127], [109, 238, 107], [168, 251, 54]];
    const dots = [];
    const pointer = { x: 0.5, y: 0.5, active: false };
    let width = 0;
    let height = 0;
    let dpr = 1;
    let frame = 0;
    let running = true;
    let visible = true;

    const resize = () => {
      const rect = host.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      context.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (!dots.length) {
        for (let index = 0; index < count; index += 1) {
          dots.push({
            t: Math.random(),
            speed: 0.00005 + Math.random() * 0.00008,
            amplitude: 10 + Math.random() * 60,
            phase: Math.random() * Math.PI * 2,
            size: 1 + Math.random() * 1.6,
            alpha: 0.2 + Math.random() * 0.45,
            color: palette[Math.floor(Math.random() * palette.length)]
          });
        }
      }
    };

    const draw = () => {
      if (!running || !visible) {
        frame = 0;
        return;
      }
      context.clearRect(0, 0, width, height);
      for (const dot of dots) {
        dot.t += dot.speed * 16;
        if (dot.t > 1) dot.t -= 1;
        const driftX = (pointer.active ? (pointer.x - 0.5) * 20 * (1 - dot.t) : 0);
        const driftY = (pointer.active ? (pointer.y - 0.5) * 14 * (1 - dot.t) : 0);
        const x = dot.t * width + Math.sin(dot.t * 5 + dot.phase) * dot.amplitude + driftX;
        const y = height - dot.t * height + Math.cos(dot.t * 4 + dot.phase) * dot.amplitude * 0.6 + driftY;
        const [r, g, b] = dot.color;
        context.lineCap = 'round';
        context.strokeStyle = `rgba(${r},${g},${b},${dot.alpha * 0.55})`;
        context.lineWidth = dot.size;
        context.beginPath();
        context.moveTo(x - 7, y + 3.5);
        context.lineTo(x, y);
        context.stroke();
        context.beginPath();
        context.fillStyle = `rgba(${r},${g},${b},${dot.alpha})`;
        context.arc(x, y, dot.size, 0, Math.PI * 2);
        context.fill();
      }
      frame = window.requestAnimationFrame(draw);
    };

    const start = () => {
      if (!frame && running && visible) frame = window.requestAnimationFrame(draw);
    };

    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(host);
    resize();

    const intersection = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      running = visible;
      if (visible) start();
      else if (frame) { window.cancelAnimationFrame(frame); frame = 0; }
    }, { threshold: 0 });
    intersection.observe(canvas);

    document.addEventListener('visibilitychange', () => {
      running = !document.hidden;
      if (running) start();
      else if (frame) { window.cancelAnimationFrame(frame); frame = 0; }
    });

    hero.addEventListener('pointermove', (event) => {
      const rect = host.getBoundingClientRect();
      pointer.x = (event.clientX - rect.left) / rect.width;
      pointer.y = (event.clientY - rect.top) / rect.height;
      pointer.active = true;
    });
    hero.addEventListener('pointerleave', () => { pointer.active = false; });

    start();
  }

  /* ── line-mask headings ──────────────────────────────────────────────── */
  function initSplitText() {
    if (!window.SplitText) return;
    document.fonts.ready.then(() => {
      document.querySelectorAll('[data-split]').forEach((element) => {
        try {
          const split = new SplitText(element, { type: 'lines', mask: 'lines', linesClass: 'split-line' });
          gsap.from(split.lines, {
            yPercent: 110,
            duration: 1,
            ease: 'power3.out',
            stagger: 0.08,
            scrollTrigger: { trigger: element, start: 'top 88%', once: true }
          });
        } catch (error) {
          /* keep the readable heading if SplitText cannot split it */
        }
      });
      ScrollTrigger.refresh();
    });
  }

  /* ── quiet reveals ───────────────────────────────────────────────────── */
  function initReveals() {
    ScrollTrigger.batch('.sec-head, .numbers .number, .suite__card, .tier, .faq details, .try__form, .try__result, .pricing__all', {
      start: 'top 88%',
      once: true,
      onEnter: (batch) => gsap.from(batch, {
        y: 20,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out',
        stagger: 0.06,
        overwrite: true
      })
    });
  }

  /* ── the 20-second story ─────────────────────────────────────────────── */
  function initStory(mm) {
    const story = document.querySelector('[data-story]');
    if (!story) return;
    const scroll = story.querySelector('.story__scroll');
    const acts = [...story.querySelectorAll('.story-act')];
    const steps = [...story.querySelectorAll('[data-step]')];
    const clock = story.querySelector('[data-clock]');
    const railFill = story.querySelector('[data-rail-fill]');
    if (!scroll || acts.length < 5) return;

    const times = ['0:00', '0:05', '0:15', '0:16', '0:20'];
    const q = (selector) => story.querySelector(selector);
    const qa = (selector) => [...story.querySelectorAll(selector)];

    const setStoryState = (progress) => {
      const index = progress < 0.21 ? 0 : progress < 0.43 ? 1 : progress < 0.65 ? 2 : progress < 0.87 ? 3 : 4;
      steps.forEach((step, stepIndex) => step.classList.toggle('is-active', stepIndex === index));
      acts.forEach((act, actIndex) => act.classList.toggle('is-active', actIndex === index));
      if (clock) clock.textContent = times[index];
      if (railFill) railFill.style.transform = `scaleY(${Math.min(1, Math.max(0, progress))})`;
    };

    mm.add('(min-width: 1024px)', () => {
      gsap.set(acts, { autoAlpha: 0, y: 24 });
      gsap.set(acts[0], { autoAlpha: 1, y: 0 });
      gsap.set(q('[data-visit-company]'), { autoAlpha: 0, y: 10 });
      gsap.set(q('[data-visit-cursor]'), { x: 0, y: 0 });
      gsap.set(qa('[data-type]'), { clipPath: 'inset(0 100% 0 0)' });
      gsap.set(q('[data-form-calendar]'), { autoAlpha: 0, x: 20 });
      gsap.set(q('[data-ring]'), { strokeDashoffset: 327 });
      gsap.set(q('[data-score]'), { textContent: '0' });
      gsap.set(q('[data-reason]'), { clipPath: 'inset(0 100% 0 0)' });
      gsap.set(q('[data-route-token]'), { left: 0 });
      gsap.set(q('[data-book-slot]'), { scale: 0.9 });
      gsap.set(q('[data-book-toast]'), { autoAlpha: 0, y: 10 });

      story.classList.add('story-ready');
      ScrollTrigger.refresh();

      const scoreProxy = { value: 0 };
      const score = q('[data-score]');

      const timeline = gsap.timeline({
        scrollTrigger: {
          trigger: scroll,
          start: 'top 64px',
          end: 'bottom bottom',
          scrub: 1,
          invalidateOnRefresh: true,
          onUpdate: (self) => setStoryState(self.progress)
        }
      });

      timeline
        .to(q('[data-visit-cursor]'), { x: 6, y: -4, duration: 0.4, ease: 'power2.inOut' }, 0.1)
        .to(q('[data-visit-company]'), { autoAlpha: 1, y: 0, duration: 0.3, ease: 'power2.out' }, 0.2)
        .to(acts[0], { autoAlpha: 0, y: -20, duration: 0.18, ease: 'power2.in' }, 0.95)
        .to(acts[1], { autoAlpha: 1, y: 0, duration: 0.22, ease: 'power2.out' }, 0.95)
        .to(qa('[data-type]'), { clipPath: 'inset(0 0% 0 0)', duration: 0.5, stagger: 0.1, ease: 'power2.out' }, 1.05)
        .to(q('[data-ghosts]'), { autoAlpha: 0, height: 0, marginTop: 0, duration: 0.35, ease: 'power2.inOut' }, 1.45)
        .to(q('[data-form-calendar]'), { autoAlpha: 1, x: 0, duration: 0.35, ease: 'power2.out' }, 1.3)
        .to(acts[1], { autoAlpha: 0, y: -20, duration: 0.18, ease: 'power2.in' }, 1.95)
        .to(acts[2], { autoAlpha: 1, y: 0, duration: 0.22, ease: 'power2.out' }, 1.95)
        .to(q('[data-ring]'), { strokeDashoffset: 0, duration: 0.6, ease: 'power2.inOut' }, 2.05)
        .to(scoreProxy, {
          value: 92,
          duration: 0.6,
          ease: 'power2.out',
          onUpdate: () => { if (score) score.textContent = String(Math.round(scoreProxy.value)); }
        }, 2.05)
        .to(q('[data-reason]'), { clipPath: 'inset(0 0% 0 0)', duration: 0.4, ease: 'power2.out' }, 2.4)
        .to(acts[2], { autoAlpha: 0, y: -20, duration: 0.18, ease: 'power2.in' }, 2.95)
        .to(acts[3], { autoAlpha: 1, y: 0, duration: 0.22, ease: 'power2.out' }, 2.95)
        .to(q('[data-route-token]'), { left: 'calc(100% - 21px)', duration: 0.6, ease: 'power2.inOut' }, 3.05)
        .to(q('[data-route-rule]'), { scale: 1.04, duration: 0.2, yoyo: true, repeat: 1, ease: 'power2.inOut' }, 3.4)
        .to(acts[3], { autoAlpha: 0, y: -20, duration: 0.18, ease: 'power2.in' }, 3.95)
        .to(acts[4], { autoAlpha: 1, y: 0, duration: 0.22, ease: 'power2.out' }, 3.95)
        .to(q('[data-book-slot]'), { scale: 1.05, duration: 0.2, yoyo: true, repeat: 1, ease: 'power2.inOut' }, 4.05)
        .to(q('[data-book-toast]'), { autoAlpha: 1, y: 0, duration: 0.3, ease: 'power2.out' }, 4.25);

      setStoryState(0);
      return () => {
        story.classList.remove('story-ready');
        story.querySelectorAll('*').forEach((element) => element.removeAttribute('style'));
        ScrollTrigger.refresh();
      };
    });

    mm.add('(max-width: 1023px)', () => {
      acts.forEach((act) => {
        gsap.from(act, {
          y: 24,
          opacity: 0,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: { trigger: act, start: 'top 88%', once: true }
        });
      });
    });
  }

  /* ── five tools collapse ─────────────────────────────────────────────── */
  function initStack(mm) {
    const stack = document.querySelector('[data-stack]');
    if (!stack) return;
    const chips = [...stack.querySelectorAll('.tool-chip')];
    const card = stack.querySelector('[data-stack-card]');
    if (!chips.length || !card) return;

    mm.add('(min-width: 768px)', () => {
      stack.classList.add('stack-ready');
      gsap.set(card, { autoAlpha: 0, scale: 0.9 });
      ScrollTrigger.refresh();

      const timeline = gsap.timeline({
        scrollTrigger: { trigger: stack, start: 'top 68%', once: true }
      });
      timeline
        .to(chips, {
          x: (index) => (index - 2) * 42,
          y: (index) => (index % 2 ? -18 : 18),
          rotate: (index) => (index - 2) * 4,
          duration: 0.6,
          ease: 'power2.out',
          stagger: 0.05
        })
        .to(chips, {
          x: 0,
          y: 0,
          rotate: 0,
          scale: 0.2,
          autoAlpha: 0,
          filter: 'blur(6px)',
          duration: 0.8,
          ease: 'power3.inOut',
          stagger: 0.04
        }, '+=0.15')
        .to(card, { autoAlpha: 1, scale: 1, duration: 0.6, ease: 'power3.out' }, '-=0.35');

      return () => {
        stack.classList.remove('stack-ready');
        gsap.set([...chips, card], { clearProps: 'all' });
        ScrollTrigger.refresh();
      };
    });
  }

  /* ── counters and line draw ──────────────────────────────────────────── */
  function initCounters() {
    document.querySelectorAll('[data-count]').forEach((element) => {
      const to = Number(element.dataset.count);
      const from = element.dataset.from ? Number(element.dataset.from) : 0;
      const suffix = element.dataset.suffix || '';
      const proxy = { value: from };
      ScrollTrigger.create({
        trigger: element,
        start: 'top 88%',
        once: true,
        onEnter: () => {
          gsap.to(proxy, {
            value: to,
            duration: 1.2,
            ease: 'power2.out',
            onUpdate: () => { element.textContent = `${Math.round(proxy.value)}${suffix}`; }
          });
        }
      });
    });

    const paths = [...document.querySelectorAll('[data-lines="numbers"] path')];
    if (paths.length) {
      const lengths = paths.map((path) => {
        const length = path.getTotalLength();
        path.style.strokeDasharray = String(length);
        path.style.strokeDashoffset = String(length);
        return length;
      });
      gsap.to(paths, {
        strokeDashoffset: 0,
        duration: 1.4,
        stagger: 0.03,
        ease: 'power2.out',
        scrollTrigger: { trigger: '[data-numbers]', start: 'top 75%', once: true }
      });
      /* keep the lengths referenced so linting knows they are intentional */
      void lengths;
    }
  }

  /* ── live record builder ─────────────────────────────────────────────── */
  function initTry() {
    const tryBlock = document.querySelector('[data-try]');
    if (!tryBlock) return;
    const inputs = [...tryBlock.querySelectorAll('.try__input')];
    const rows = [...tryBlock.querySelectorAll('[data-try-row]')];
    const score = tryBlock.querySelector('[data-try-score]');
    const booked = tryBlock.querySelector('[data-try-booked]');
    const empty = tryBlock.querySelector('.try__empty');
    if (!inputs.length || !rows.length) return;

    let played = false;
    const build = () => {
      if (played || !inputs.some((input) => input.value.trim())) return;
      played = true;
      const proxy = { value: 0 };
      gsap.timeline()
        .set(rows, { opacity: 0, y: 6 })
        .set(empty, { display: 'none' })
        .to(rows, { opacity: 1, y: 0, duration: 0.35, stagger: 0.06, ease: 'power2.out' })
        .to(proxy, {
          value: 92,
          duration: 0.8,
          ease: 'power2.out',
          onUpdate: () => { if (score) score.textContent = String(Math.round(proxy.value)); }
        }, '-=0.3')
        .fromTo(booked, { opacity: 0, y: 6 }, { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }, '-=0.2');
    };

    inputs.forEach((input) => input.addEventListener('input', build));

    const show = tryBlock.querySelector('[data-try-show]');
    if (show) {
      show.addEventListener('click', () => {
        build();
        const empty = inputs.find((input) => !input.value.trim());
        (empty || inputs[0]).focus();
      });
    }
  }

  /* ── pricing toggle flip ─────────────────────────────────────────────── */
  function initBilling() {
    document.querySelectorAll('[data-billing] input').forEach((input) => {
      input.addEventListener('change', () => {
        if (!input.checked) return;
        const yearly = input.id === 'billing-yearly';
        const selector = yearly ? '.p-yearly' : '.p-monthly';
        const elements = [
          ...document.querySelectorAll(`.tier__price ${selector}`),
          ...document.querySelectorAll(`.tier__price small${selector}`)
        ];
        gsap.fromTo(elements, { opacity: 0, y: 6 }, {
          opacity: 1,
          y: 0,
          duration: 0.35,
          stagger: 0.02,
          ease: 'power2.out',
          overwrite: true
        });
      });
    });
  }

  /* ── closing draw + comet ────────────────────────────────────────────── */
  function initClosing() {
    const close = document.querySelector('[data-close]');
    if (!close) return;
    const paths = [...close.querySelectorAll('[data-lines="close"] path')];
    const comet = close.querySelector('[data-close-comet]');
    const stamp = close.querySelector('[data-close-stamp]');
    const check = close.querySelector('.close__check');
    if (!paths.length) return;

    paths.forEach((path) => {
      const length = path.getTotalLength();
      path.style.strokeDasharray = String(length);
      path.style.strokeDashoffset = String(length);
    });
    if (check) {
      const length = check.getTotalLength();
      check.style.strokeDasharray = String(length);
      check.style.strokeDashoffset = String(length);
    }

    ScrollTrigger.create({
      trigger: close,
      start: 'top 70%',
      once: true,
      onEnter: () => {
        gsap.to(paths, { strokeDashoffset: 0, duration: 1.6, stagger: 0.04, ease: 'power2.out' });
        if (comet) {
          gsap.fromTo(comet, { autoAlpha: 0, x: -140, y: 70 }, {
            autoAlpha: 1,
            x: 0,
            y: 0,
            duration: 1.3,
            delay: 0.2,
            ease: 'power2.inOut'
          });
        }
        if (stamp) {
          gsap.fromTo(stamp, { autoAlpha: 0, scale: 0.82 }, {
            autoAlpha: 1,
            scale: 1,
            duration: 0.5,
            delay: 1.15,
            ease: 'power3.out'
          });
        }
        if (check) {
          gsap.to(check, { strokeDashoffset: 0, duration: 0.45, delay: 1.35, ease: 'power2.out' });
        }
      }
    });
  }

  /* ── top progress line ───────────────────────────────────────────────── */
  function initProgress() {
    const bar = document.querySelector('[data-progress]');
    if (!bar) return;
    ScrollTrigger.create({
      start: 0,
      end: 'max',
      onUpdate: (self) => gsap.set(bar, { scaleX: self.progress })
    });
  }
})();
