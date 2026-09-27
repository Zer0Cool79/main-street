# START HERE

Welcome. This checklist takes you from "I just clicked Use this template" to a live website. No experience assumed. Check each box as you go.

## 0. Understand what you just got

You clicked **Use this template** on the Main Street repo. That gave you **your own copy**: a brand-new repo under your GitHub account, with no shared history. Your website lives in **your repo**, not in the template. The template can't see your site and you can't break the template. Everything from here happens in your copy.

If you're reading this file, you're in the right place.

## 1. Make it yours (5 minutes)

**The easy way:** open your AI chat (muse.ai, claude.ai, chatgpt.com, or whichever you use) and say "run the setup with me." It asks the plain-language questions right here in chat (business name, tagline, phone, email, address, domain, what kind of business) and configures everything in your repo. Nothing to install.

**The hands-on way:** on your computer, in a terminal, inside your repo folder:

```bash
npm install
npm run setup
```

Same questions, same result. (Needs Node.js from [nodejs.org](https://nodejs.org), LTS version.) If any step confuses you, just ask Muse instead.

## 2. See your site (1 minute)

```bash
npm run dev
```

Open the address it prints (usually http://localhost:5173). That's your site, running on your computer. It currently shows a fictional bakery. Your business details from step 1 are already filled in.

## 3. Put it on the internet (15 minutes)

Full walkthrough: [docs/setup-guide.md](docs/setup-guide.md). The short version:

1. **Buy your domain** at [Cloudflare Registrar](https://www.cloudflare.com/products/registrar/) (~$10/year, no markup).
2. **Connect your repo to Cloudflare Pages**: Pages → Create → Connect to Git → pick your repo. Build command `npm run build`, output directory `dist`. That's it.
3. **Add your custom domain** in Pages → Custom domains. Cloudflare handles DNS and SSL automatically.
4. Push to `main` any time: your site rebuilds and goes live in about a minute.

From now on: **push to `main` = your live site updates.** Nothing else to do.

## 4. Get business email working (10 minutes, optional but recommended)

- **Receiving:** Cloudflare Email Routing forwards `you@yourdomain.com` to your personal Gmail, free. Setup: [docs/setup-guide.md](docs/setup-guide.md) (email section).
- **Sending (contact form):** one free Resend API key, added as a secret in Cloudflare. Until you add it, the contact form politely hides itself and shows your email address instead. Nothing breaks.

## 5. Meet your AI web developer

This is the part that changes everything. **Your AI chat assistant is your web developer now** — whichever you use: muse.ai, claude.ai, chatgpt.com, or others. Your repo already contains its operating manual (`CLAUDE.md` + `rules/`), and it reads it automatically. You just talk.

Nothing to install, no new apps, no terminal. If you can send a text message, you can run your website.

Read [docs/owner-quickstart.md](docs/owner-quickstart.md) for example requests and the approval flow.

## 6. Make your first change

Try this, verbatim, with your AI assistant:

> "Change the hero headline to something warmer, and show me a preview link before anything goes live."

What should happen: it edits the file, opens a preview branch, hands you a URL. You look at it. If you like it, you say "ship it" and it merges. Watch for that rhythm: **change → preview link → your approval → live.** That's the whole workflow, forever.

## 7. Everyday tasks cheat sheet

| You want to... | Say to your AI... |
|---|---|
| Rewrite the demo copy for your business | "Rewrite the homepage copy for my plumbing business, keeping the layout" |
| Change hours, phone, address | "Update our Saturday hours to 8 to 4" |
| Post a holiday notice | "Put up a banner: closed Thanksgiving week" |
| Add photos | "Add these photos to the gallery" (then attach them) |
| Add a page section | "Add a testimonials section with these three quotes..." |
| Turn a feature on/off | "Turn on the blog" / "Turn off the gallery" |
| Undo something | "Roll back the last change" (or one click in Cloudflare: Deployments → ⋯ → Rollback) |
| Check the site is healthy | "Run the site audit" |

## If something looks wrong

1. Don't panic. Nothing here can send you a bill and almost nothing is irreversible.
2. Ask your AI: "what just changed, and how do we undo it?"
3. The fastest undo: Cloudflare dashboard → Pages → your site → Deployments → find the last good one → ⋯ → **Rollback**. No terminal needed.
4. Still stuck? Open an issue in your repo. Describe what you see, in plain words. That's what issues are for.

---

Next: [docs/setup-guide.md](docs/setup-guide.md) for the full setup walkthrough, then [docs/owner-quickstart.md](docs/owner-quickstart.md) to meet your AI web developer.
