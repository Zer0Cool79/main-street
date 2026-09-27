# Setup guide

The complete walkthrough: from zero to a live website at your own domain. Budget about an hour, most of it waiting for DNS. If you get stuck at any step, describe where you are in plain words to your AI assistant; it can read this guide too.

## What you need

- A GitHub account (free).
- A Cloudflare account (free).
- About $10/year for the domain name.
- An AI chat subscription you already use (Claude, ChatGPT, or similar). Connect it first: [connect-your-ai.md](connect-your-ai.md). Your AI never needs API keys.
- Node.js from [nodejs.org](https://nodejs.org), only if you'll run commands on your own computer (the hands-on path in Step 2).

## Step 1: Get your site folder (5 minutes)

Your site starts as a copy of the `template/` folder in the Main Street repo.

**Easiest:** ask your AI (connected in [connect-your-ai.md](connect-your-ai.md)): "Download the Main Street template from github.com/davegelinas/main-street and scaffold my site folder." It handles the download, the copy, and the naming.

**By hand:** download the [repo zip](https://github.com/davegelinas/main-street/archive/refs/heads/main.zip), unzip it, and copy everything inside `template/` into a new folder named after your business (e.g. `acme-plumbing`). That folder is your site. Then put it on GitHub: create a new repo there and push the folder (say to your AI: "help me put my site folder on GitHub" for click-by-click help).

## Step 2: Make it yours (10 minutes)

**If your AI has access to your site folder** ([Path A](connect-your-ai.md)): say "run the setup with me." It asks for your business details in plain language, right in chat, and writes them into `site.config.json`. Pick the preset closest to your kind of business, or skip it.

**If you're in a web chat** ([Path B](connect-your-ai.md)): say "interview me for the setup." It asks the same questions here in chat, then hands you the answers to type into the wizard below.

**The hands-on way,** on your computer, from your site folder:

```bash
cd acme-plumbing
npm install
npm run setup
```

(Use your real folder name.) `npm install` downloads the build tools (one time). `npm run setup` asks plain-language questions: business name, phone, email, address, domain, what kind of business, then configures everything.

Then preview:

```bash
npm run dev
```

Open the address it prints. That's your site.

## Step 3: Domain + DNS on Cloudflare (10 minutes + waiting)

You want Cloudflare holding your DNS. That's what gives your staging site a clean address (`staging.yourdomain.com`) instead of an ugly `*.pages.dev` URL, and it makes the domain wiring automatic later.

**Buying new?** Buy it at [Cloudflare Registrar](https://www.cloudflare.com/products/registrar/): wholesale cost, no markup (~$10/year for `.com`), and DNS is already on Cloudflare. Done. Skip to Step 4.

**Already own one elsewhere?** Move its DNS to Cloudflare (free, your registrar stays as-is):

1. In Cloudflare: **Add domain**, enter it, continue. Cloudflare shows you two nameservers.
2. **Read the email warning first:** changing nameservers moves *every* DNS record. Copy your existing records (especially MX/email records) before switching. See [domains-and-dns.md](domains-and-dns.md), which your AI assistant can walk through with you.
3. At your registrar, replace the domain's nameservers with Cloudflare's two.
4. Back in Cloudflare, **Check nameservers**. Status flips to **Active** in minutes to a few hours. Go get coffee; don't keep poking it.

## Step 4: Connect Cloudflare Pages (10 minutes)

1. In Cloudflare: **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
2. Authorize GitHub if asked, and pick your repo.

   > **Repo not showing up?** ("No repositories matching") The Cloudflare Pages GitHub App is usually only allowed to see *some* of your repos. Fix it on GitHub: click your avatar → **Settings** → **Applications** → **Installed GitHub Apps** → **Cloudflare Pages** → **Configure** → under *Repository access*, choose **All repositories** (or pick your site's repo) → **Save**. Back in Cloudflare, refresh the repo list. It'll appear. (Make sure it's the **Cloudflare Pages** app, not Cloudflare Workers, they're separate.)
3. Build settings:
   - Production branch: `main`
   - Build command: `npm run build`
   - Build output directory: `dist`
   - (Leave everything else default.)
4. Click **Save and Deploy**. Cloudflare builds your site and gives it a `*.pages.dev` address. It's live already, just not at your domain yet.

From now on, **every push to `main` rebuilds and redeploys production automatically.**

## Step 5: Your live domain (5 minutes + waiting)

1. In Pages → your site → **Custom domains** → **Set up a custom domain**.
2. Enter your domain (e.g. `acmeplumbing.com`). Cloudflare adds the DNS record and provisions SSL automatically. No records to type.
3. Add the `www` version too if you want it (same screen).
4. Wait for DNS to propagate (minutes to hours). Then open your domain: that's your live site.

## Step 6: Your staging site at staging.yourdomain.com (10 minutes)

This is the preview copy where every change lands first. One permanent address, pretty enough to bookmark on your phone.

1. **Turn on staging builds.** Pages → your site → **Settings** → **Builds & deployments** → **Branch deploy controls**: choose **All non-production branches** (or otherwise make sure `staging` is included).
2. **Push the `staging` branch once.** If it doesn't exist yet: create it from `main` and push. Cloudflare builds it. The first build must succeed before the next step works. Your staging branch already has an address: `staging.<project>.pages.dev` (open it to confirm the build worked).
3. **Attach the subdomain.** **Custom domains** → **Set up a custom domain** → enter `staging.yourdomain.com` → **Continue** → **Activate domain**. Cloudflare creates the DNS record automatically.
4. **Point it at the staging branch.** Go to your domain's **DNS** settings, find the `CNAME` record named `staging`, and change its target from `<project>.pages.dev` to `staging.<project>.pages.dev` (your branch's address from step 2). **Leave it proxied** (orange cloud on). An unproxied (gray-cloud) record silently serves the *live* site on the staging address.
5. Open `staging.yourdomain.com`. That's your staging site, forever at that address.

Staging is automatically hidden from Google (it sends `X-Robots-Tag: noindex`), so customers never stumble onto the preview copy. Don't "fix" that, it's on purpose.

**No custom domain?** Everything still works: staging lives at `staging.<project>.pages.dev`. The pretty subdomain just needs DNS on Cloudflare.

## Step 7: Business email (10 minutes, recommended)

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

## Step 8: Analytics (5 minutes, optional)

Cloudflare dashboard sidebar → **Analytics & Logs** → **Web Analytics** → **Add a site**, type your domain. Cloudflare shows a code snippet. Copy just the `"token": "..."` value (about 32 characters; choose the JS-snippet option if asked). Then: Pages → your project → **Settings** → **Environment variables** → Production → add `CF_ANALYTICS_TOKEN` with the token, **Save**, and redeploy (Deployments → ⋯ → Retry deployment). The token is read at build time and never goes in the repo. The snippet only renders when the token is present. No cookies, no consent banner. Full owner walkthrough: [api-keys.md](api-keys.md).

## Step 9: Meet your AI web developer

See [connect-your-ai.md](connect-your-ai.md) and [owner-quickstart.md](owner-quickstart.md). The short version: connect your AI with the subscription you already pay for (no API keys), say "read CLAUDE.md," and talk. From here on, every update is a conversation.

## Verify everything

```bash
npm run audit https://yourdomain.com
npm run audit https://staging.yourdomain.com
```

The first checks the live site; the second checks staging (it also verifies staging is hidden from search engines). Fix anything red before announcing the site.

## What "done" looks like

- [ ] Your domain shows your site, with your business details.
- [ ] `staging.yourdomain.com` shows the staging copy (push something to the `staging` branch and watch it appear).
- [ ] The contact form sends you an email (submit a test).
- [ ] Email to `hello@yourdomain.com` lands in your inbox.
- [ ] `npm run audit` is all green on both addresses.
- [ ] You've made one change through your AI assistant using the staging link.

Welcome to the $12/year club.
