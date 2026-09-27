# Photo gallery

A simple photo grid: real photos of the real business. **On by default.**

## How to turn it on/off

Flag: `gallery` in `site.config.json`. Photos live in `public/images/gallery/`.

## Adding photos

1. Drop JPG or PNG files into `public/images/gallery/`. Descriptive filenames (`storefront-morning.jpg`).
2. Run `npm run optimize-images`. It resizes and converts to WebP.
3. Add each photo to the gallery markup with real alt text ("Our baker pulling sourdough from the oven").
4. Ship via preview so the owner can see the photos in place.

That's it. No CMS, no admin panel, no image service. Files in a folder.

## Rules

- **Real photos only.** The actual shop, the actual people, the actual product. One honest photo beats five stock shots (see `rules/core.md`).
- Get the owner's explicit okay for any photo showing customers or staff faces.
- Keep it curated: 6 to 12 photos. A gallery of 40 is a storage unit, not a showcase.
- Every image gets alt text. Decorative-only images don't belong in a gallery.

## What can go wrong

- Giant files slowing the page: the optimize script catches this; run it after every addition.
- "The photos look wrong on my phone": check at 390px before approving. Grid layouts break there first.
