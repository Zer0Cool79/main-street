# Contact form

A contact section with a working form. Submissions are emailed to the owner via Resend. **On by default.**

## How to turn it on/off

Flag: `contactForm` in `site.config.json`. The form posts to `functions/api/contact.ts`.

## What the owner needs to do

One thing: create a free Resend API key and add it as `RESEND_API_KEY` in Cloudflare (Pages → Settings → Environment variables → Production). Step-by-step in `docs/setup-guide.md`.

Until the key exists, the form **hides itself** and the section shows the business email and phone instead. This is deliberate: a form that fails on every submission is worse than no form. Verify the degraded state on the preview URL before calling it done.

## How it works

- Frontend validates (name, valid email, message), includes a honeypot field and a submission timer.
- The Pages Function rejects bots (honeypot filled, submitted in under 3 seconds), then sends via the Resend API: from the business address, `Reply-To` set to the visitor.
- On success the visitor sees a plain-words confirmation. On failure they see the direct email address. Never a stack trace.

## Costs and limits

Resend's free tier covers far more than a small business contact form will ever send. If spam becomes a real problem, add Cloudflare Turnstile (free); see `rules/email.md`. Don't add it preemptively.

## Customization

- Change the recipient: the function sends to the business email from config. If the owner wants submissions to go elsewhere, that's a config change, not a code change.
- Extra fields (party size, date): add them to the form and the function together, and test end-to-end.

## What can go wrong

- "Nobody's getting the emails": check the Resend dashboard first (deliveries log), then whether the key is set in Cloudflare's *Production* environment (not just Preview).
- Form works locally but not live: `.dev.vars` has the key but Cloudflare doesn't. See `rules/traps.md`.
