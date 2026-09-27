#!/usr/bin/env node
// Beginner setup wizard. Asks plain questions, writes site.config.json.
// Usage: npm run setup
import { createInterface } from "node:readline";
import { readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { PRESETS, applyPreset } from "./preset.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const configPath = resolve(root, "site.config.json");

const rl = createInterface({ input: process.stdin, output: process.stdout });
// Pull lines via async iterator: each prompt consumes the next line, and a
// closed stdin cleanly yields "" (so defaults apply) instead of hanging.
const lineIterator = rl[Symbol.asyncIterator]();
const ask = async (q) => {
  process.stdout.write(q);
  const { value, done } = await lineIterator.next();
  return done ? "" : String(value ?? "").trim();
};

async function prompt(label, def = "") {
  const hint = def ? ` [${def}]` : "";
  const answer = await ask(`  ${label}${hint}: `);
  return answer || def;
}

async function promptValid(label, def, validate, retryMsg) {
  for (;;) {
    const answer = await prompt(label, def);
    if (validate(answer)) return answer;
    console.log(`  ${retryMsg}`);
  }
}

const isEmail = (s) => /.+@.+\..+/.test(s);
const isDomain = (s) => /^[a-z0-9-]+(\.[a-z0-9-]+)+$/i.test(s);
const cleanDomain = (s) => s.replace(/^https?:\/\//i, "").replace(/^www\./i, "").split("/")[0];

console.log("\nWelcome to Main Street! Let us set up your website.");
console.log("Press Enter to accept the answer in [brackets].\n");

const config = JSON.parse(readFileSync(configPath, "utf8"));
const b = config.business ?? {};
const s = config.site ?? {};
const addr = b.address ?? {};

console.log("Step 1 of 3: your business");
b.name = await prompt("Business name", b.name);
b.tagline = await prompt("Tagline (one short sentence)", b.tagline);
b.phone = await prompt("Phone number", b.phone);
b.email = await promptValid("Contact email", b.email, isEmail, "That does not look like an email address, try again.");
const founded = await prompt("Year founded (optional, Enter to skip)", "");
if (founded.trim()) b.founded = founded.trim(); else delete b.founded;

console.log("\nStep 2 of 3: your address and domain");
addr.street = await prompt("Street address", addr.street);
addr.city = await prompt("City", addr.city);
addr.state = await prompt("State (2 letters)", addr.state);
addr.zip = await prompt("ZIP code", addr.zip);
b.address = addr;
const rawDomain = await promptValid("Domain name (example: acmebakery.com)", s.domain, (d) => isDomain(cleanDomain(d)), "That does not look like a domain, try again (example: acmebakery.com).");
s.domain = cleanDomain(rawDomain);
s.description = `${b.name}: ${b.tagline}. Located at ${addr.street}, ${addr.city}, ${addr.state}.`;
config.business = b;
config.site = s;

console.log("\nStep 3 of 3: pick a starting preset (sets which features are on)");
const names = Object.keys(PRESETS);
names.forEach((n, i) => console.log(`  ${i + 1}. ${n}`));
console.log(`  ${names.length + 1}. Skip (keep current features)`);
const choice = await prompt("Choice", String(names.length + 1));
const idx = parseInt(choice, 10) - 1;
if (idx >= 0 && idx < names.length) {
  const changed = applyPreset(config, names[idx]);
  console.log(`\nPreset "${names[idx]}" applied (${changed.length} feature flag${changed.length === 1 ? "" : "s"} changed).`);
} else {
  console.log("\nKeeping your current feature flags.");
}

writeFileSync(configPath, JSON.stringify(config, null, 2) + "\n");
rl.close();

console.log("\nDone! site.config.json is updated.");
console.log("One more step: the page copy still describes the demo bakery.");
console.log("Ask your AI assistant: \"rewrite the homepage copy for my business, keeping the layout.\"");
console.log("\nNext steps:");
console.log("  1. npm run dev      Preview your site at http://localhost:5173");
console.log("  2. Edit copy in index.html, or ask your AI assistant to do it");
console.log("  3. Push to GitHub and connect the repo to Cloudflare Pages (free)");
console.log("  4. Add your domain in Cloudflare, and you are live\n");
