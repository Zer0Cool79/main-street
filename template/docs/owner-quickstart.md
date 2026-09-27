# Owner quickstart: working with your AI web developer

Your repo contains its own operating manual (`CLAUDE.md` + `rules/`). Your AI assistant reads it automatically and acts as your web developer, whichever chat you use: muse.ai, claude.ai, chatgpt.com, or others. This guide is about *you*: how to ask, what to expect, and the rhythm of getting things done.

**Watch first** (36 seconds, no sound needed): the whole journey, step by step.

<video controls poster="assets/journey-poster.png" width="1280" src="assets/journey.mp4"></video>

[Watch the walkthrough video](assets/journey.mp4) (MP4, 36 seconds)

## Getting started

Your AI needs to see your website's files before it can help. The person who set up your site (Marcus, an agency, whoever) connects your AI chat to your site's files. Every AI does this a little differently (a GitHub connection, uploading files, or a small app on your computer). Ask them: "connect my AI to my website repo."

Once it's connected, open your AI chat and say: **"read CLAUDE.md in my website repo."** That's the whole setup. (If it ever seems lost later, say "read CLAUDE.md" again, that file is its operating manual.)

## The rhythm: change → staging → approve → live

Every task follows the same beat. Your site has two copies: a **staging site** (`staging.yourdomain.com`) where changes appear first, and your **live site** that customers see.

1. **You ask**, in plain English.
2. **It puts** the change on your staging site and sends you the link.
3. **You look** at the staging site on your phone. This is your approval step. There is no approve button; your words are the button ("looks good, ship it").
4. **It publishes.** Your approved preview copy becomes the live site (your AI "merges staging to main"; Cloudflare publishes it in about a minute).
5. **It tells you** what changed and reminds you how to undo it.

If any step is skipped, ask for it: "send me the staging link first."

## Example requests that work well

**Content updates:**
- "Change our Saturday hours to 8am to 4pm."
- "Add a banner: we're closed Thanksgiving week, reopening Monday."
- "Update the price list: the basic service call is now $89, and add drain cleaning for $129."
- "Rewrite the about section. Here's what I want it to say: ..." (then dictate)

**Photos:**
- "Add these photos to the gallery." (attach them) "Put the storefront one first."

**Features:**
- "Turn on the blog. I'll write the first post; show me how."
- "Turn off the testimonials for now."
- "Add a booking button that goes to [your booking URL]."

**Questions:**
- "What would you change about the homepage?"
- "Why is the contact form not sending me emails?"
- "Ask it to run the site audit and explain the results in plain English."

**Undo:**
- "Roll back the last change." (Or do it yourself: Cloudflare dashboard → Workers & Pages → your site → Deployments → find the last good one → **Rollback**.)

## What good looks like

- It explains what it's about to do *before* doing it, in one or two plain sentences.
- It never uses git jargon without translating it.
- Every change ends with a link you can open on your phone.
- It confirms before anything irreversible (deleting, DNS, email changes).
- It tells you how to undo what it just did.

If your assistant isn't doing these things, say so: "Explain it like I'm new to this" works remarkably well. The repo's `rules/beginner-mode.md` also instructs it, but a nudge never hurts.

## Things worth knowing

- **You can't break the money.** Every service here is free-tier. There is no bill to accidentally run up.
- **Almost everything is undoable.** The rollback button in Cloudflare undoes any deployment in one click.
- **Small asks are best.** "Change the headline" beats "redesign the site." Big changes still work; they just get more preview rounds.
- **Your words win.** If you dictate copy, it goes in verbatim. If the assistant rewrites your voice, tell it: "use my words exactly."
- **Photos are your superpower.** Real photos of your real business improve the site more than any design tweak. Keep sending them.
- **The shoebox.** Everything about your business lives in `content/brand/`: photos, videos, logo, and your answers in `brief.md`. The more you put in, the better your site looks. See [docs/gather-your-stuff.md](gather-your-stuff.md). Nothing in it is required.
- **Your AI can borrow other apps.** For a logo, promo images, a short video, or selling online, your AI can plug into apps like Canva, Higgsfield, or Shopify. See [docs/connectors.md](connectors.md) for what to ask.

## When something's wrong

1. Tell the assistant what you see, in plain words. ("The phone number on the homepage is wrong.")
2. Ask: "What changed recently, and how do we undo it?"
3. If it's urgent and the assistant is stuck: Cloudflare dashboard → Workers & Pages → your site → Deployments → roll back to yesterday. Then investigate calmly.
