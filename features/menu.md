# Menu / price list

A structured list of offerings with prices. Built for restaurants and cafes, but works for any priced list: salon services, class schedules, product lines. **On by default** (demo shows a bakery menu).

## How to turn it on/off

Flag: `menu` in `site.config.json`. Items live in the page markup, grouped by category.

## Rules

- **Prices come from the owner, always.** Never guess, never carry over from an old menu without confirming. A wrong price is a broken promise.
- When prices change, change the date too if the page shows one ("Prices updated March 2026"). Customers notice stale prices.
- Keep descriptions to a line each. Ingredients that matter for allergies get named; marketing adjectives don't.
- If the business has dietary info (vegan, gluten-free), mark it consistently with a simple label, and confirm each label with the owner. This is a trust issue, not a design issue.

## For restaurants specifically

- The menu page should be readable in under 10 seconds on a phone by someone standing outside deciding whether to come in. Categories, prices, done.
- A downloadable PDF menu is optional. If the owner wants one, generate it from the same source as the page so they can't drift apart. Never maintain two menus by hand.

## What can go wrong

- Menu drift: the printed menu changes and the site doesn't. When the owner mentions new items or prices anywhere, ask "should the website match?"
