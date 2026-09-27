// Reads site.config.json and transforms every .html page:
//   1. strips <!-- feature:name --> blocks whose flag is off
//   2. replaces {{dot.path}} tokens (plus {{hours}}, {{jsonld}}, {{year}})
//   3. on build, emits sitemap.xml and robots.txt into dist/
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import type { OutputOptions } from "rollup";
import type { Plugin } from "vite";

type Config = Record<string, any>;

function loadConfig(root: string): Config {
  return JSON.parse(readFileSync(resolve(root, "site.config.json"), "utf8"));
}

function getPath(obj: any, path: string): any {
  return path.split(".").reduce((o, k) => (o == null ? o : o[k]), obj);
}

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// "Monday – Friday" -> ["Monday",...]; "7:00 AM – 6:00 PM" -> "07:00-18:00"
const DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
const DAY_CODE: Record<string, string> = { Monday: "Mo", Tuesday: "Tu", Wednesday: "We", Thursday: "Th", Friday: "Fr", Saturday: "Sa", Sunday: "Su" };

function to24(t: string): string {
  const m = t.trim().match(/^(\d{1,2})(?::(\d{2}))?\s*(AM|PM)$/i);
  if (!m) return t.trim();
  let h = parseInt(m[1], 10) % 12;
  if (/pm/i.test(m[3])) h += 12;
  return `${String(h).padStart(2, "0")}:${m[2] ?? "00"}`;
}

function openingHours(hours: Array<{ days: string; time: string }>): string[] {
  const out: string[] = [];
  for (const h of hours) {
    if (/closed/i.test(h.time)) continue;
    const range = h.days.split(/–|-/).map((d) => d.trim());
    let days = range;
    if (range.length === 2) {
      const a = DAY_ORDER.indexOf(range[0]);
      const b = DAY_ORDER.indexOf(range[1]);
      if (a >= 0 && b >= a) days = DAY_ORDER.slice(a, b + 1);
    }
    const [open, close] = h.time.split(/–|-/).map((t) => t.trim());
    if (open && close) out.push(`${days.map((d) => DAY_CODE[d] ?? d).join(",")} ${to24(open)}-${to24(close)}`);
  }
  return out;
}

function jsonLd(cfg: Config): string {
  const b = cfg.business ?? {};
  const a = b.address ?? {};
  const data = {
    "@context": "https://schema.org",
    "@type": b.type || "LocalBusiness",
    name: b.name,
    description: cfg.site?.description,
    telephone: b.phone,
    email: b.email,
    url: `https://${cfg.site?.domain}`,
    foundingDate: b.founded,
    address: {
      "@type": "PostalAddress",
      streetAddress: a.street,
      addressLocality: a.city,
      addressRegion: a.state,
      postalCode: a.zip,
    },
    openingHours: openingHours(b.hours ?? []),
  };
  const json = JSON.stringify(data).replace(/</g, "\\u003c");
  return `<script type="application/ld+json">${json}</script>`;
}

// Build FAQPage JSON-LD from native <details> blocks (summary = question).
function faqJsonLd(html: string): string {
  const items: string[] = [];
  const re = /<details[^>]*>\s*<summary[^>]*>([\s\S]*?)<\/summary>\s*<div[^>]*>([\s\S]*?)<\/div>\s*<\/details>/gi;
  let m: RegExpExecArray | null;
  while ((m = re.exec(html))) {
    const q = m[1].replace(/<[^>]+>/g, "").trim();
    const a = m[2].replace(/<[^>]+>/g, "").trim();
    if (q && a) items.push(JSON.stringify({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } }));
  }
  if (!items.length) return "";
  return `<script type="application/ld+json">${JSON.stringify({ "@context": "https://schema.org", "@type": "FAQPage", mainEntity: items.map((i) => JSON.parse(i)) }).replace(/</g, "\\u003c")}</script>`;
}

function stripFeatures(html: string, cfg: Config): string {
  return html.replace(/<!--\s*feature:([A-Za-z]+)\s*-->([\s\S]*?)<!--\s*\/feature:\1\s*-->/g, (match, name, body) => {
    const on = Boolean(cfg.features?.[name]);
    if (name === "announcementBanner") return on && String(cfg.site?.announcement ?? "").trim() ? body : "";
    if (name === "analytics") return on && String(cfg.integrations?.cloudflareAnalyticsToken ?? "").trim() ? body : "";
    return on ? body : "";
  });
}

function hoursHtml(hours: Array<{ days: string; time: string }>): string {
  return `<dl class="hours">\n${hours.map((h) => `  <div><dt>${esc(h.days)}</dt><dd>${esc(h.time)}</dd></div>`).join("\n")}\n</dl>`;
}

function hoursPlain(hours: Array<{ days: string; time: string }>): string {
  return hours.map((h) => `- ${h.days}: ${h.time}`).join("\n");
}

function replaceTokensPlain(text: string, cfg: Config): string {
  return text.replace(/\{\{([a-zA-Z0-9_.]+)\}\}/g, (match, path) => {
    if (path === "year") return String(new Date().getFullYear());
    if (path === "business.hours") return hoursPlain(cfg.business?.hours ?? []);
    if (path === "jsonld" || path === "faqJsonld") return "";
    const v = getPath(cfg, path);
    return v == null ? "" : String(v);
  });
}

function replaceTokens(html: string, cfg: Config): string {
  return html.replace(/\{\{([a-zA-Z0-9_.]+)\}\}/g, (match, path) => {
    if (path === "year") return String(new Date().getFullYear());
    if (path === "jsonld") return jsonLd(cfg);
    if (path === "business.hours") return hoursHtml(cfg.business?.hours ?? []);
    if (path === "faqJsonld") return faqJsonLd(html);
    const v = getPath(cfg, path);
    return v == null ? "" : esc(String(v));
  });
}

export function siteConfig(): Plugin {
  let root = "";
  return {
    name: "site-config",
    configResolved(c) {
      root = c.root;
    },
    transformIndexHtml(html) {
      const cfg = loadConfig(root);
      return replaceTokens(stripFeatures(html, cfg), cfg);
    },
    writeBundle(options: OutputOptions) {
      // Build-only: write sitemap.xml, robots.txt, and the token-filled
      // llms.txt straight to the output dir, overwriting the public/ templates.
      const cfg = loadConfig(root);
      const domain = cfg.site?.domain ?? "example.com";
      const outDir = options.dir ?? resolve(root, "dist");
      const pages = ["", "privacy-policy/", "terms-of-service/"];
      const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map((p) => `  <url><loc>https://${domain}/${p}</loc></url>`).join("\n")}\n</urlset>\n`;
      const robots = `User-agent: *\nAllow: /\n\nSitemap: https://${domain}/sitemap.xml\n`;
      writeFileSync(resolve(outDir, "sitemap.xml"), sitemap);
      writeFileSync(resolve(outDir, "robots.txt"), robots);
      // llms.txt uses plain-text token replacement (no HTML escaping).
      try {
        const llms = readFileSync(resolve(root, "public/llms.txt"), "utf8");
        writeFileSync(resolve(outDir, "llms.txt"), replaceTokensPlain(llms, cfg));
      } catch {
        // No llms.txt in public/: nothing to do.
      }
    },
  };
}
