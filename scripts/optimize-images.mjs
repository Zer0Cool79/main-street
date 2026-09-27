#!/usr/bin/env node
// Scans public/images for oversized photos. If `sharp` is installed it
// converts to WebP and resizes; otherwise it prints a plain-English report.
// Usage: npm run optimize-images
// (Install sharp optionally: npm i -D sharp)
import { readdirSync, statSync } from "node:fs";
import { resolve, dirname, extname, basename } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dir = resolve(root, "public/images");
const MAX_BYTES = 400 * 1024;
const MAX_WIDTH = 1600;

let files;
try {
  files = readdirSync(dir).filter((f) => [".jpg", ".jpeg", ".png"].includes(extname(f).toLowerCase()));
} catch {
  console.log("No public/images folder found. Nothing to do.");
  process.exit(0);
}

let sharp = null;
try {
  sharp = (await import("sharp")).default;
} catch {
  // sharp is optional; fall through to report mode.
}

if (files.length === 0) {
  console.log("No JPG/PNG photos in public/images. Nothing to do.");
  process.exit(0);
}

console.log(`Checking ${files.length} photo(s) in public/images\n`);
let needsWork = 0;

for (const file of files) {
  const full = resolve(dir, file);
  const size = statSync(full).size;
  const kb = Math.round(size / 1024);
  let width = 0;
  let meta = null;
  if (sharp) {
    try {
      meta = await sharp(full).metadata();
      width = meta.width ?? 0;
    } catch { /* unreadable: report below */ }
  }
  const oversized = size > MAX_BYTES;
  const tooWide = width > MAX_WIDTH;

  if (sharp && meta && (oversized || tooWide)) {
    const out = resolve(dir, `${basename(file, extname(file))}.webp`);
    const pipeline = sharp(full).rotate();
    if (tooWide) pipeline.resize({ width: MAX_WIDTH, withoutEnlargement: true });
    await pipeline.webp({ quality: 80 }).toFile(out);
    const newKb = Math.round(statSync(out).size / 1024);
    console.log(`  OPTIMIZED  ${file} (${kb} KB${tooWide ? `, ${width}px wide` : ""}) -> ${basename(out)} (${newKb} KB)`);
    console.log(`             Update the <img> tag to use ${basename(out)}.`);
    needsWork++;
  } else if (oversized || (sharp && !meta)) {
    needsWork++;
    console.log(`  TOO BIG    ${file} (${kb} KB${tooWide ? `, ${width}px wide` : ""})`);
    if (!sharp) {
      console.log("             Re-export at 80% quality and max 1600px wide, or ask your AI assistant to handle it.");
    } else {
      console.log("             Could not read this file, check that it is a valid image.");
    }
  } else {
    console.log(`  OK         ${file} (${kb} KB${width ? `, ${width}px` : ""})`);
  }
}

console.log(needsWork === 0 ? "\nAll photos look good." : `\n${needsWork} photo(s) need attention (see above).`);
