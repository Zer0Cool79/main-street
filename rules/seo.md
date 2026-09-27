# SEO rules — be findable locally

Small businesses live on local search. Most of this is already built into the template; your job is to not break it and to complete the human parts.

## Already handled (don't break)

- **LocalBusiness JSON-LD** on every page, generated from `site.config.json` (`{{jsonld}}` token). If the business type changes (bakery → restaurant), update the schema type to match.
- **sitemap.xml** generated at build from the page list. **New pages must be added to the sitemap** or they're invisible to search. Check how the plugin builds the page list before adding a page.
- **robots.txt** allows crawling and points at the sitemap.
- **Semantic HTML, real copy in HTML** (not JS-rendered), descriptive `<title>` and meta descriptions per page, canonical URLs, OG tags.
- **llms.txt** in `public/` — a short plain-text description of the business for AI crawlers.

## Your jobs

- **Titles and descriptions** are written for humans first, search second. "Golden Crumb Bakery | Fresh bread and pastries in Maplewood, NJ" beats keyword stuffing.
- **One page per real topic.** Services, menu, about, contact. Don't merge everything into the homepage and don't splinter into thin pages.
- **URLs are permanent.** Once a URL is live and linked anywhere, it never changes without a 301 redirect in `public/_redirects`. Ever.
- **Images:** descriptive filenames (`sourdough-loaf.jpg`, not `IMG_4829.jpg`) and real alt text. Both feed image search.
- **NAP consistency:** Name, Address, Phone must be identical everywhere: this site, Google Business Profile, Yelp, Facebook. `site.config.json` is the canonical source; when it changes, remind the owner to update the other listings.

## The human checklist (give this to the owner)

These can't be done in the repo; they matter more than any meta tag:

1. **Google Business Profile:** claim it, complete every field, add real photos, keep hours in sync with the site.
2. **Reviews:** ask happy customers for Google reviews. Respond to every review.
3. **Bing Places, Apple Maps:** same NAP, same photos. Ten minutes each.
4. After launch, run `node scripts/indexnow.mjs` if present, or submit the sitemap in Google Search Console.

## AI crawler note

Cloudflare may prepend its own directives to `robots.txt` at the edge. Verify crawler behavior against the live site (`curl -A ...`), not just the repo file, before making claims about what's blocked.
