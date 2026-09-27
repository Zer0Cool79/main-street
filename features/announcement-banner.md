# Announcement banner

A one-sentence banner at the top of every page. The owner's megaphone. **On by default.**

## How to turn it on/off

Flag: `announcementBanner` in `site.config.json`. The text is `site.announcement`. **Empty string = no banner**, even with the flag on. The build strips the block when the flag is off or the text is empty.

## Typical uses

- Holiday closures: "Closed Thanksgiving week. See you Monday, Nov 30."
- Special hours, new offerings, "we moved", limited-time items.
- Keep it to one sentence. If it needs two, it belongs on a page, not in a banner.

## Owner workflow

The owner says "put up a banner: closed next week." The assistant updates `site.announcement`, ships via preview, and asks: "Want me to take it down Monday morning, or will you tell me?" Stale banners are the #1 way a site looks abandoned. Proactively offer removal dates.

## Customization

- Style lives with the site CSS. Keep it noticeable but calm: it should read as information, not an alarm.
- For scheduled banners (sale dates, events), just set the text when the time comes. No scheduling machinery: boring is reliable.
