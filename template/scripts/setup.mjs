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
b.name = await promptValid(
  "Business name",
  b.name,
  (n) => n.trim().length > 0 && n.trim().length <= 80,
  "That is very long for a business name (over 80 characters). It breaks the site header and gets cut off in Google. Use the short version customers actually know you by."
);
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
const rawDomain = await promptValid("Domain name: your website address, like acmeplumbing.com (don't have one yet? just press Enter, your AI will help you get one later for about $12/year)", s.domain, (d) => isDomain(cleanDomain(d)), "That does not look like a domain, try again (example: acmeplumbing.com).");
s.domain = cleanDomain(rawDomain);
if (s.domain === "example.com") {
  console.log("  (Keeping the placeholder example.com, your AI will help you get a real domain later.)");
}
s.description = `${b.name}: ${b.tagline}. Located at ${addr.street}, ${addr.city}, ${addr.state}.`;
config.business = b;
config.site = s;

console.log("\nStep 3 of 3: pick a starting preset (turns the right features on for your kind of business)");
console.log("Pick the closest match, your AI can fine-tune individual features later.\n");
const presetBlurb = {
  bakery: "bakeries, cafes, food shops (menu, photo gallery, reviews)",
  restaurant: "restaurants, bars (menu, gallery, questions)",
  "home-services": "plumbers, electricians, landscapers (quote form, reviews, questions)",
  retail: "flower shops, boutiques, gift shops (photo gallery, reviews, contact form)",
  "salon-wellness": "salons, spas, barbers (gallery, booking, prices)",
  professional: "offices, consultants, agencies (reviews, questions, contact form)",
};
const names = Object.keys(PRESETS);
names.forEach((n, i) => console.log(`  ${i + 1}. ${n}: ${presetBlurb[n] ?? "feature bundle"}`));
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

console.log("\nDone! site.config.json is updated.");
console.log("The page copy is neutral placeholder text.");
console.log("Ask your AI assistant: \"rewrite the homepage copy for my business, keeping the layout.\"");

// ---- Integrations status ----
// API keys live in Cloudflare (Pages -> Settings -> Environment variables)
// and in .dev.vars for local testing. Never in this repo, never in chat.
// A missing key never breaks a page: the feature degrades gracefully.
console.log("\nIntegrations status (details: docs/api-keys.md):");
const feat = config.features ?? {};
const devVarsPath = resolve(root, ".dev.vars");
let devVars = "";
try { devVars = readFileSync(devVarsPath, "utf8"); } catch { /* no .dev.vars yet */ }
const hasResendKey = /^RESEND_API_KEY=.+/m.test(devVars);

function statusLine(name, state, note) {
  console.log(`  ${state}  ${name}: ${note}`);
}

if (!feat.contactForm) {
  statusLine("Contact form email (Resend)", "SKIPPED", "the contact form feature is off. Turn it on in site.config.json to use it.");
} else if (hasResendKey) {
  statusLine("Contact form email (Resend)", "WORKING", "key found in .dev.vars for local testing. Also add it in Cloudflare Pages -> Settings -> Environment variables for the live site.");
} else {
  statusLine("Contact form email (Resend)", "NOT SET UP", "visitors see your email address instead of the form; the page never breaks. See docs/api-keys.md.");
}

if (!feat.analytics) {
  statusLine("Visitor stats (Cloudflare Analytics)", "SKIPPED", "the analytics feature is off.");
} else if (String(process.env.CF_ANALYTICS_TOKEN ?? "").trim()) {
  statusLine("Visitor stats (Cloudflare Analytics)", "WORKING", "token found in this shell (rare, it normally lives in Cloudflare).");
} else {
  statusLine("Visitor stats (Cloudflare Analytics)", "NOT SET UP", "add CF_ANALYTICS_TOKEN in Cloudflare Pages -> Settings -> Environment variables. No visitor stats until then; the site works exactly the same. See docs/api-keys.md.");
}

// Offer to save a Resend key for local testing (optional, safe to skip).
if (feat.contactForm && !hasResendKey) {
  const key = await prompt("Paste your Resend API key to try the contact form locally (don't have one yet? just press Enter to skip, docs/api-keys.md shows how to get one)", "");
  if (key.trim()) {
    const line = `RESEND_API_KEY=${key.trim()}\n`;
    try {
      const existing = devVars.includes("RESEND_API_KEY=")
        ? devVars.replace(/^RESEND_API_KEY=.*$/m, line.trimEnd())
        : devVars + (devVars.endsWith("\n") || devVars === "" ? "" : "\n") + line;
      writeFileSync(devVarsPath, existing);
      console.log("  Saved to .dev.vars (this file is private to your computer and never committed).");
    } catch {
      console.log("  Could not write .dev.vars. You can create it by hand later; see docs/api-keys.md.");
    }
  }
}

console.log("\nYour future website addresses (once your domain is connected, your helper or AI does that part):");
console.log(`  Live:    https://${s.domain}`);
console.log(`  Staging: https://staging.${s.domain}   <- every change appears here first, for your eyes only`);
console.log("\nNext steps:");
console.log("  For you:");
console.log("    1. npm run dev      Preview your site at http://localhost:5173");
console.log("    2. Ask your AI assistant to rewrite the homepage copy for your business");
console.log("    3. Gather your stuff: photos, logo, and answers go in the shoebox at content/brand/ (see content/brand/README.md), or just ask your AI to interview you in chat. docs/gather-your-stuff.md is the weekend homework.");
console.log("  For your helper (or your AI): follow docs/setup-guide.md:");
console.log("    3. Put the site on GitHub and connect it to Cloudflare Pages (free)");
console.log("    4. Connect your domain name and set up email\n");
rl.close();
