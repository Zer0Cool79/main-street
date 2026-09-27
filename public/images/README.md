# Site photos go here

Drop your real photos in this folder as JPG, PNG, or WebP files.

Guidelines that keep the site fast:

- Aim for under 400 KB per file and no wider than 1600 px. Phone photos are usually fine after a quick export at 80% quality.
- Name files descriptively: `hero.jpg`, `gallery-croissants.jpg`, not `IMG_4829.jpg`.
- Every photo shown on the site needs descriptive `alt` text in the HTML (it is how screen readers and Google "see" the image).

Then run `npm run optimize-images`. If the `sharp` package is available it will convert everything to WebP and resize oversized files automatically. If not, the script prints a plain-English report of what needs shrinking, and you can ask your AI assistant to handle it.
