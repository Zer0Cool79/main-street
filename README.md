# Main Street

**The $12/year website stack.** A GitHub template that gives any small business a fast, professional website they can update themselves with AI, for the price of a domain name.

No page builders. No monthly SaaS fees. No developer on retainer. You get your own website, in your own GitHub repo, and any AI chat assistant as your web developer: plain-English requests, handled in chat. Use muse.ai, claude.ai, chatgpt.com, or whichever you already use.

## How it works

1. **Click "Use this template."** You get your own repo. Your site lives there, separate from this template, under your control.
2. **Answer a few questions.** `npm run setup` asks for your business name, hours, and what kind of business you run, then configures everything.
3. **Connect Cloudflare (free).** Your repo auto-deploys: push to `main` and your site is live in about a minute. Every other change gets a preview link first.
4. **Update it by talking.** Your AI chat assistant is your web developer. Point it at your repo (muse.ai, claude.ai, chatgpt.com, or others) and say things like "we're closed Thanksgiving week" or "add a photo gallery." It makes the change, you approve the preview, it goes live. Nothing to install, no terminal.

## What it costs

| What | Cost |
|---|---|
| Domain name (Cloudflare Registrar) | ~$10/year |
| Hosting, CDN, SSL (Cloudflare Pages) | $0 |
| Contact form email (Resend) | $0 |
| Business email forwarding (Cloudflare Email Routing) | $0 |
| Analytics, privacy-friendly (Cloudflare Web Analytics) | $0 |
| Spam protection (Cloudflare Turnstile) | $0 |
| Database, if you ever need one (Supabase) | $0 |
| **Total** | **~$10–12/year** |

The full honest breakdown, including free-tier limits: [docs/the-12-dollar-stack.md](docs/the-12-dollar-stack.md).

## What's inside

- **A starter site** (Vite, plain HTML/CSS, no framework) for a fictional bakery, so you can see the end state on day one. Replace the content, keep the structure.
- **A brain, not just a site.** `CLAUDE.md` is a lightweight dispatcher: it tells your AI assistant how your site works and points it at focused rule files in `rules/` only when they're relevant. (`AGENTS.md` gives non-Claude assistants the same instructions.) Read [how the AI side works](docs/owner-quickstart.md).
- **Features you can turn on.** Photo gallery, menu/price list, testimonials, FAQ, blog, booking links, email signup. Each is a switch in `site.config.json` plus its own guide in `features/`. Say "turn on the gallery" and it's done.
- **Business presets.** `npm run preset restaurant` (or bakery, home-services, salon-wellness, professional) applies a sensible feature bundle for your kind of business. See [presets/](presets/).
- **A deployment pipeline with guardrails.** Push to `main` = live site. Every change first gets a preview URL you approve with your eyes. One-click rollback from the Cloudflare dashboard, no terminal required. The rules are in [rules/deploy.md](rules/deploy.md).
- **Local SEO baked in.** LocalBusiness structured data, sitemap, robots.txt, and a Google Business Profile checklist in [rules/seo.md](rules/seo.md).

## New here? Start here

**[START-HERE.md](START-HERE.md)** is the first-run checklist. It assumes you've never used GitHub before.

Then read, in this order:

1. [docs/setup-guide.md](docs/setup-guide.md) — domain, Cloudflare, email, going live. Step by step.
2. [docs/owner-quickstart.md](docs/owner-quickstart.md) — how to work with your AI web developer, with example requests.
3. [docs/editing-in-browser.md](docs/editing-in-browser.md) — the simplest update path of all: edit text on GitHub.com, no tools installed.

## For freelancers and agencies

You can spin up a client site from this template in under an hour and hand the client a site they can actually run themselves. [docs/for-agencies.md](docs/for-agencies.md) covers the per-client playbook: cloning, white-labeling the AI instructions, and what to charge for.

## The idea in one paragraph

Small businesses don't have a technology problem, they have a maintenance problem. A beautiful site is cheap to build and expensive to keep current, so it rots. This template fixes the maintenance side: the site lives in version control, deploys itself, and carries its own operating manual for AI, so the owner can say what they want in plain English and watch it happen. The $12/year part just removes the last excuse.

---

Built from real production setups. The patterns here (the dispatcher-style `CLAUDE.md`, the reference docs, the post-deploy audit, the graceful degradation when secrets are missing) were refined running actual business sites on this exact stack.
