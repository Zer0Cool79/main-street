# Content rules — words on the site

## Business facts

- Hours, prices, services, address, phone, and names come from `site.config.json` and from the owner's mouth. **Never invent them.** A wrong hour costs a customer; a wrong price costs trust.
- When the owner dictates copy, their words go in **verbatim**. Don't tighten, don't "improve," don't fix their voice. If something is factually wrong (a typo in the phone number), flag it and ask.
- Never invent testimonials, credentials, awards, statistics, or claims. If the site says "voted best in town," the owner must have given you the source.

## Announcements and holiday hours

- The announcement banner is the owner's megaphone: `site.announcement` in `site.config.json`. One sentence, plain words. Empty string = no banner.
- Typical uses: holiday closures, special hours, "we moved", limited-time offerings.
- When the owner says "we're closed next week," update the announcement AND the hours if applicable, then ask which date the banner should come down. Offer to remove it after: "Want me to take it down Monday morning, or will you tell me?"

## Images

- After adding ANY image to `public/images/`, run `npm run optimize-images`.
- Every image gets descriptive alt text. Decorative images get empty alt (`alt=""`), not missing alt.
- Prefer real photos of the real business over anything generic. One honest photo of the actual storefront beats five perfect stock shots.
- Never hotlink images from other sites. Copy the file into the repo (with the owner's right to use it).

## Editing content

- Most business facts live in `site.config.json` and render through `{{tokens}}` at build time. Edit the config, not the pages, when a token exists.
- Longer copy lives directly in the HTML pages. It's plain HTML on purpose: the owner can even edit it with the pencil icon on GitHub.com (see `docs/editing-in-browser.md`).
- Keep the reading level conversational. Short paragraphs. Real specifics over adjectives (see `rules/core.md`).

## Legal pages

- `privacy-policy/` and `terms-of-service/` are templates. They must be reviewed (ideally by the owner's lawyer, at minimum by the owner reading every line) before the site handles real customer data.
- When the site's data practices change (new form, new analytics, new signup), the privacy policy must change with them. Flag it proactively.
