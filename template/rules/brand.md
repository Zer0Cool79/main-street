# Brand rules: build from the shoebox, not from thin air

## First: read the shoebox

Before designing the site or rewriting its words from scratch:

1. Read `content/brand/brief.md` for the business story, voice, and answers.
2. List `content/brand/photos/`, `content/brand/videos/`, and `content/brand/logo/` to see what assets exist.

The brief and the real assets are the design material. Use them.

## If the brief is empty or thin: interview the owner

- Don't lecture and don't dump the whole questionnaire at once. Ask the brief questions **in chat, a few at a time, conversationally**, the way the owner answers in real life.
- After each round of answers, write them into `content/brand/brief.md` yourself. The brief is the durable record; chat is the interview.
- Start with story and services (the highest value), then voice, then the rest. Stop when you have enough to build; don't interrogate.
- The owner can also fill in `brief.md` directly or attach files in chat. All paths lead to the same filled-in brief.

## Design from what's real

- **Never ship placeholder copy or filler** when real answers exist in the brief. If the owner said what they're known for, that exact story goes on the site (see `rules/content.md`: their words, verbatim).
- **Never ship stock-looking filler.** A real phone photo of the storefront beats any generic image. If the AI platform has image generation and the owner wants art, that's a connector conversation (see `rules/connectors.md`), not a silent substitution.
- If assets or answers are **missing**, say what's missing in plain words and keep going with what's there. Missing is information, not a blocker: "I don't have a logo yet, so I set your name in large type instead. Send me one any time and I'll swap it in."

## How assets flow into the site

- `content/brand/` is the raw shoebox; the site serves images from `public/images/`. When you use a brand asset, **copy it into `public/images/`** (keep the original in the shoebox), then run `npm run optimize-images`.
- Prefer real brand assets over the `public/images/` placeholders whenever brand assets exist.
- Every image gets descriptive alt text (see `rules/content.md`).

## Ship it like everything else

Brand-driven changes still go through the normal loop: stage to the preview site, the owner approves on their phone, then ship it. A great first impression is still just an impression until the owner has seen it.
