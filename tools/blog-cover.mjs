// Draws a blog cover: node tools/blog-cover.mjs '<json>' out.png
// The JSON is {title, category, kind, logo, name} (tools/blog-cover.html). Uses the Playwright that's installed.
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const [json, out] = process.argv.slice(2);
if (!json || !out) {
  console.error("usage: node tools/blog-cover.mjs '<json>' out.png");
  process.exit(1);
}
const data = JSON.parse(json);
// A logo path from the site (/assets/logos/x.svg) is read from the folder.
if (data.logo?.startsWith("/")) data.logo = pathToFileURL(path.resolve(import.meta.dirname, "..", "." + data.logo)).href;
const page = pathToFileURL(path.join(import.meta.dirname, "blog-cover.html")).href + "#" + encodeURIComponent(JSON.stringify(data));

const browser = await chromium.launch();
const tab = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 2 });
await tab.goto(page, { waitUntil: "networkidle" });
await tab.waitForSelector("body[data-ready]");
await tab.screenshot({ path: out, type: out.endsWith(".jpg") ? "jpeg" : "png", quality: out.endsWith(".jpg") ? 88 : undefined });
await browser.close();
