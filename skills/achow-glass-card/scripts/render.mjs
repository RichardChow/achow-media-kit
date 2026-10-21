#!/usr/bin/env node
// Usage: node scripts/render.mjs <data.json> [out.png]
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [,, input = path.join(root, 'examples/issue01.json'), out = 'out/card.png'] = process.argv;
const data = JSON.parse(fs.readFileSync(input, 'utf8'));
const hl = data.takeaway_highlights || [];
const tag = { 'achow-editorial-card': 'span', 'achow-glass-card': 'em', 'achow-journal-card': 'b' }[path.basename(root)] || 'b';
data.takeaway_html ??= (data.takeaway_prefix || '') + hl.map(h => `<${tag}>${h}</${tag}>`).join('和');
data.tags_html ??= (data.tags || []).map(t => `<span>${t}</span>`).join('');
// tiny mustache: {{key}}, {{#list}}...{{/list}}, {{#key}}...{{/key}} (truthy section)
function fill(t, ctx) {
  t = t.replace(/{{#(\w+)}}([\s\S]*?){{\/\1}}/g, (_, k, inner) => {
    const v = ctx[k]; if (Array.isArray(v)) return v.map(x => fill(inner, { ...ctx, ...x })).join('');
    return v ? fill(inner, ctx) : '';
  });
  return t.replace(/{{(\w+)}}/g, (_, k) => ctx[k] ?? '');
}
const html = fill(fs.readFileSync(path.join(root, 'templates/card.html'), 'utf8'), data);
const tmp = path.join(root, 'templates/.render.html'); fs.writeFileSync(tmp, html);
const cands = [process.env.CHROME_PATH, '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium',
  'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'].filter(Boolean);
const exe = cands.find(p => fs.existsSync(p));
let pw; try { pw = await import('playwright-core'); } catch { pw = await import('playwright'); }
const browser = await pw.chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage({ viewport: { width: 1080, height: 1440 } });
await page.goto(pathToFileURL(tmp).href); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(200);
fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
await page.screenshot({ path: out }); await browser.close(); fs.unlinkSync(tmp);
console.log('saved', path.resolve(out), exe ? `(chrome: ${exe})` : '(bundled chromium)');
