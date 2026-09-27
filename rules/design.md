# Design rules

## Philosophy

This site should look like the business, not like a template. Warm, confident, uncluttered. A customer should feel the place before they read a word.

## The system

- **No CSS framework.** Hand-written CSS in `src/styles.css`. The whole site's styling should stay small enough that a curious owner can read it.
- **Type:** a distinctive display face for headlines (currently Fraunces via Google Fonts) + system stack for body. Two faces max. Never more.
- **Color:** a tight palette. Cream/paper background, ink text, one confident accent. Muted, earthy tones suit most local businesses. No purple-blue gradients, no neon, no glassmorphism. If it looks like a SaaS landing page, it's wrong.
- **Space:** generous whitespace. One idea per section. Let it breathe.
- **Motion:** subtle or none. Always respect `prefers-reduced-motion`. Nothing should move for decoration alone.

## Rules

- **Mobile first.** Design at 390px, then scale up. Tap targets at least 44px. Phone number is always a `tel:` link.
- **Real HTML.** Semantic elements (`header`, `nav`, `main`, `section`, `footer`), real buttons and links, proper heading order. No div soup.
- **No stock look.** Avoid generic hero layouts (centered headline + two buttons + abstract shapes). Use the business's real photos, real voice, real details. Asymmetry and restraint beat symmetry and noise.
- **Images:** optimized (see `rules/content.md`), sized for their slot, never stretched. `loading="lazy"` below the fold.
- **Performance budget:** first load under ~100KB total on the homepage. If a change blows past that, say so before shipping.
- **Dark mode:** not required. A local business site doesn't need it; skip it rather than doing it badly.

## Changing the design

Small business sites die by a thousand "quick redesigns." Rules:

- Content changes (words, photos, hours) are always welcome and low-risk.
- Styling changes: do them on a preview branch, check phone + desktop, and get explicit approval. The owner approves with their eyes.
- Never redesign the whole site because a trend changed. This design is meant to age well.
