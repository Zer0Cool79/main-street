# Setup guide

The complete walkthrough: from zero to a live website at your own domain. Budget about an hour, most of it waiting for DNS. If you get stuck at any step, describe where you are in plain words to your AI assistant; it can read this guide too.

## What you need

- A GitHub account (free).
- A Cloudflare account (free).
- About $10/year for the domain name.
- Nothing installed: your AI chat assistant runs the setup with you in chat. (Node.js from [nodejs.org](https://nodejs.org) is only needed if you want to preview the site on your own computer.)

## Step 1: Get your own copy (5 minutes)

1. Open the Main Street template repo on GitHub.
2. Click the green **Use this template** button, then **Create a new repository**.
3. Name it after your business (e.g. `golden-crumb-bakery`). Make it **Public** or **Private**, your choice. (Public is fine: your repo contains no secrets. See `rules/safety.md`.)
4. Click **Create repository**. This is now *your* repo. Your site lives here.

## Step 2: Make it yours (10 minutes)

**The easy way:** open your AI chat (muse.ai, claude.ai, chatgpt.com, or whichever you use) and say "run the setup with me." It asks for your business details in plain language, right in chat, and writes them into `site.config.json`. Pick the preset closest to your kind of business, or skip it.

**The hands-on way,** on your computer:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
npm install
npm run setup
```

Then preview:

```bash
npm run dev
```

Open the address it prints. That's your site.

## Step 3: Buy your domain (5 minutes)

1. Go to [cloudflare.com/products/registrar](https://www.cloudflare.com/products/registrar/) and sign in.
2. Search for your domain, buy it. Cloudflare sells at wholesale cost with no markup (~$10/year for `.com`).
3. Why here and not GoDaddy/Namecheap: your DNS, hosting, and email all end up in one dashboard, and there's nothing to wire together later.

## Step 4: Connect Cloudflare Pages (10 minutes)

1. In Cloudflare: **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
2. Authorize GitHub if asked, and pick your repo.
3. Build settings:
   - Build command: `npm run build`
   - Build output directory: `dist`
   - (Leave everything else default.)
4. Click **Save and Deploy**. Cloudflare builds your site and gives it a `*.pages.dev` address. It's live already, just not at your domain yet.

From now on, **every push to `main` rebuilds and redeploys automatically.** Pushes to other branches get preview URLs.

## Step 5: Point your domain at the site (5 minutes + waiting)

1. In Pages → your site → **Custom domains** → **Set up a custom domain**.
2. Enter your domain (e.g. `goldencrumbbakery.com`). Cloudflare adds the DNS records and provisions SSL automatically.
3. Wait. DNS can take a few minutes to a few hours. Don't keep changing things while you wait; check with the audit script later.

Add the `www` version too if you want it (same screen).

## Step 6: Business email (10 minutes, recommended)

**Receiving** (free, Cloudflare Email Routing):

1. Cloudflare dashboard → **Email** → **Email Routing** → Enable, select your domain.
2. Add a destination address: your personal Gmail.
3. Create a custom address: `hello@yourdomain.com` → your Gmail. Add `noreply@` too if you'll use the contact form.
4. Cloudflare adds the MX records. Test: send an email to `hello@yourdomain.com` and watch it land in your Gmail.

**Sending** (free, Resend; needed for the contact form):

1. Sign up at [resend.com](https://resend.com) (free tier).
2. Add your domain, add the DNS records Resend shows you (SPF/DKIM), wait for verification.
3. Create an API key (Sending access only).
4. Cloudflare → Pages → your site → **Settings** → **Environment variables** → Production → add `RESEND_API_KEY` (mark it secret/encrypted).
5. Redeploy once (Deployments → latest → Retry deployment) so the function picks it up.

Until the key exists, the contact form hides itself and shows your email address instead. Nothing breaks.

**Replying as the business from Gmail** (optional): Gmail → Settings → Accounts → "Send mail as" → add `hello@yourdomain.com` using Resend's SMTP credentials. Now replies come from the business address.

## Step 7: Analytics (5 minutes, optional)

Cloudflare → your site → **Analytics** → **Web Analytics** → add your site. Copy the beacon token into `integrations.cloudflareAnalyticsToken` in `site.config.json`, commit, push. The snippet only renders when the token is present. No cookies, no consent banner.

## Step 8: Meet your AI web developer

See [owner-quickstart.md](owner-quickstart.md). The short version: open your AI chat, point it at your repo, and talk. The repo explains itself via `CLAUDE.md`. From here on, every update is a conversation.

## Verify everything

```bash
npm run audit https://yourdomain.com
```

It checks your pages return 200, your 404 page actually 404s, HTTPS works, SEO tags are present. Fix anything red before announcing the site.

## What "done" looks like

- [ ] Your domain shows your site, with your business details.
- [ ] The contact form sends you an email (submit a test).
- [ ] Email to `hello@yourdomain.com` lands in your inbox.
- [ ] `npm run audit` is all green.
- [ ] You've made one change through your AI assistant using a preview link.

Welcome to the $12/year club.
