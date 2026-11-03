// Run: python3 -m http.server 8765 (from the repo root), then
//   node tools/walk-forms.js http://localhost:8765 '[{"slug":"insurance-auto-quote","pick":{"Any claims or accidents":"No"}}]'
// Needs playwright. Exits 1 when a form doesn't reach its end screen.
// Walks a form template's live demo on the website page by page: fills what each page shows (first choice unless
// told otherwise), presses Next, and reports the pages it saw and whether it reached the end screen.
const { chromium } = require('playwright');
const fs = require('fs');
const base = process.argv[2];
const jobs = JSON.parse(process.argv[3]); // [{ slug, pick: { "Label text": "Option text" } }]
const tmp = require('path').join(require('os').tmpdir(), 'walk-upload.txt');
fs.writeFileSync(tmp, 'test');
(async () => {
  const b = await chromium.launch();
  let bad = 0;
  for (const job of jobs) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = [];
    p.on('pageerror', (e) => errs.push(e.message));
    await p.goto(`${base}/templates/${job.slug}/`, { waitUntil: 'networkidle' });
    const form = p.locator('form[data-cf]').first();
    const start = form.locator('[data-start]');
    if (await start.count() && (await start.isVisible())) await start.click();
    const seen = [];
    let done = false;
    for (let step = 0; step < 12 && !done; step++) {
      const page = form.locator('.cf__page:not([hidden])').first();
      const title = ((await page.locator('.cf__ptitle').textContent().catch(() => '')) || `p${step}`).trim();
      seen.push(title);
      // Several passes: answering one question can show another below it.
      const filled = new Set();
      for (let pass = 0; pass < 3; pass++) {
      const fields = page.locator('.cf__f:not([hidden])');
      const n = await fields.count();
      for (let i = 0; i < n; i++) {
        const f = fields.nth(i);
        if (!(await f.isVisible())) continue;
        const fkey = await f.getAttribute('data-key');
        if (filled.has(fkey)) continue;
        filled.add(fkey);
        await f.scrollIntoViewIfNeeded().catch(() => {});
        const label = ((await f.locator('.cf__label').first().textContent().catch(() => '')) || '').replace(/\*/g, '').trim();
        const want = Object.entries(job.pick || {}).find(([k]) => label.startsWith(k));
        const kind = (await f.getAttribute('data-kind')) || '';
        const dd = f.locator('.cf__dd-btn');
        if (await dd.count()) {
          await dd.click({ timeout: 2000 }).catch(() => {});
          const li = want ? f.locator('.cf__dd-list li', { hasText: want[1] }).first() : f.locator('.cf__dd-list li').first();
          await li.click({ timeout: 2000 }).catch(() => {});
          continue;
        }
        if (kind === 'number' || kind === 'money') {
          // A number inside the question's own limits, read from the form's data.
          const lim = await form.evaluate((el, k) => { const sc = JSON.parse(el.querySelector('.cf__data').textContent).schema; for (const pg of sc.pages) for (const x of pg.fields) if (x.key === k) return [x.min, x.max]; return [null, null]; }, fkey);
          const lo = lim[0] ?? 1, hi = lim[1] ?? Math.max(lo, 10);
          await f.locator('input').first().fill(want ? want[1] : String(Math.round((lo + hi) / 2))).catch(() => {});
          continue;
        }
        const radios = f.locator('input[type=radio]');
        if (await radios.count()) {
          // One pick per group (a matrix has a group per row); the wanted option when told.
          const names = [...new Set(await radios.evaluateAll((xs) => xs.map((x) => x.name)))];
          for (const nm of names) {
            if (want) {
              const opt = f.locator('label', { has: p.locator(`input[name="${nm}"]`), hasText: want[1] }).first();
              if (await opt.count()) { await opt.click({ timeout: 2000 }).catch(() => {}); continue; }
            }
            await f.locator('label', { has: p.locator(`input[name="${nm}"]`) }).first().click({ timeout: 2000 }).catch(() => {});
          }
          continue;
        }
        const boxes = f.locator('input[type=checkbox]');
        if (await boxes.count()) { await f.locator('label:has(input[type=checkbox])').first().click({ timeout: 2000 }).catch(() => {}); continue; }
        const file = f.locator('input[type=file]');
        if (await file.count()) { await file.first().setInputFiles(tmp).catch(() => {}); continue; }
        const canvas = f.locator('canvas');
        if (await canvas.count()) {
          const bb = await canvas.first().boundingBox();
          if (bb) { await p.mouse.move(bb.x + 20, bb.y + 20); await p.mouse.down(); await p.mouse.move(bb.x + 120, bb.y + 40, { steps: 5 }); await p.mouse.up(); }
          continue;
        }
        const inputs = f.locator('input:not([type=hidden]):not([type=radio]):not([type=checkbox]):not([type=file]), textarea');
        const m = await inputs.count();
        for (let k = 0; k < m; k++) {
          const el = inputs.nth(k);
          if (!(await el.isVisible())) continue;
          const type = (await el.getAttribute('type')) || 'text';
          const name = (await el.getAttribute('name')) || '';
          const v = want && m === 1 ? want[1] : type === 'email' ? 'sam@example.com' : type === 'number' ? '5' : type === 'date' ? '2027-03-04' : type === 'time' ? '10:30' : type === 'url' ? 'https://example.com' : type === 'tel' ? '5551234567' : /postal/.test(name) ? '94110' : 'Test';
          await el.fill(v, { timeout: 2000 }).catch(() => {});
        }
      }
      }
      await form.locator('[data-next]').click();
      await p.waitForTimeout(150);
      done = await form.locator('.cf__end').isVisible();
      if (!done) {
        const errVisible = await form.locator('.cf__err:not([hidden])').count();
        if (errVisible) { seen.push(`STUCK: ${await form.locator('.cf__err:not([hidden])').first().textContent()}`); break; }
      }
    }
    if (!done || errs.length) bad++;
    console.log(`${done ? 'ok   ' : 'FAIL '} ${job.slug} [${seen.join(' > ')}]${errs.length ? ' errors: ' + errs.join('; ') : ''}`);
    await p.close();
  }
  await b.close();
  process.exit(bad ? 1 : 0);
})();
