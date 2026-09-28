# Setup guide

The complete walkthrough: from zero to a live website at your own domain. Budget about an hour, most of it waiting for DNS. If you get stuck at any step, describe where you are in plain words to your AI assistant; it can read this guide too.

**No installs, no helper, nothing but a browser?** Skip this guide and follow [browser-only.md](browser-only.md) instead. It covers the same journey with every step written out for someone whose only tool is a ChatGPT or Claude browser tab.

## What you need

- A GitHub account (free).
- A Cloudflare account (free).
- About $10-12/year for the domain name. (Cloudflare needs a payment method on the account to buy it.)
- An AI chat subscription you already use (Claude, ChatGPT, or similar). Connect it first: [connect-your-ai.md](connect-your-ai.md). Your AI itself never needs API keys.
- Node.js 22 (match `.node-version`), only if you'll run commands on your own computer (the hands-on path in Step 2).
- Git on your computer, or GitHub Desktop (free), for the one-time push in Step 1.

**Before you start, collect from the owner:** the business details (name, tagline, address, phone, email, hours, services, prices), the domain name they want (or whether you're buying a new one), whose GitHub and Cloudflare accounts you'll use (theirs, not yours), and a Gmail address for the Email Routing destination.

## Step 1: Get your site folder (5 minutes)

Your site starts as a copy of the `template/` folder in the Main Street repo.

**Easiest (if your AI can reach files on your computer, e.g. Claude Code):** ask it: "Download the Main Street template from github.com/davegelinas/main-street and scaffold my site folder." It handles the download, the copy, and the naming. If your AI is a plain browser tab with no file access, use the by-hand path below, or the owner can follow [browser-only.md](browser-only.md).

**By hand:** download the [repo zip](https://github.com/davegelinas/main-street/archive/refs/heads/main.zip), unzip it, and copy everything inside `template/` into a new folder named after your business (e.g. `acme-plumbing`). Include hidden files: `.github/`, `.gitignore`, and `.node-version` must come along. That folder is your site.

**Put the folder on GitHub** (the scaffolder only stages files locally; nothing is on GitHub until you do this). From your site folder:

```bash
git branch -M main
git commit -m "First version of the site"
```

Then create the repo at github.com/new (same name as the folder, e.g. `acme-plumbing`), and:

```bash
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPO.git
git push -u origin main
```

(Say to your AI: "help me put my site folder on GitHub" for click-by-click help.)

## Step 2: Make it yours (10 minutes)

**Owner:** say to your AI: "run the setup with me." It asks for your business details in plain language, right in chat, and fills in the site. (If your AI can't reach the files yet, your helper runs the wizard below while you answer the same questions out loud.)

**Helper (or hands-on),** on your computer, from your site folder:

```bash
cd ../acme-plumbing
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

1. In Cloudflare: **Workers & Pages** → **Create** → **Continue to Pages** (the website option) → **Import an existing Git repository** → **Get started** → **Connect to Git**.
2. Authorize GitHub if asked, and pick your repo.

   > **Repo not showing up?** ("No repositories matching") The Cloudflare Pages GitHub App is usually only allowed to see *some* of your repos. Fix it on GitHub: click your avatar → **Settings** → **Applications** → **Installed GitHub Apps** → **Cloudflare Pages** → **Configure** → under *Repository access*, choose **All repositories** (or pick your site's repo) → **Save**. Back in Cloudflare, refresh the repo list. It'll appear. (Make sure it's the **Cloudflare Pages** app, not Cloudflare Workers, they're separate.)
3. Build settings:
   - Production branch: `main`
   - Framework preset: leave at **None**. (There is no plain Vite option in the list; the similar-looking VitePress and React (Vite) are different things. Do not pick them.)
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
2. **Push the `staging` branch once.** From your site folder:

   ```bash
   git checkout -b staging main
   git push -u origin staging
   ```

   Cloudflare builds it. The first build must succeed before the next step works. Your staging branch already has an address: `staging.<project>.pages.dev` (open it to confirm the build worked).
3. **Attach the subdomain.** **Custom domains** → **Set up a custom domain** → enter `staging.yourdomain.com` → **Continue** → **Activate domain**. Cloudflare creates the DNS record automatically.
4. **Point it at the staging branch.** Go to your domain's **DNS** settings, find the `CNAME` record named `staging`, and change its target from `<project>.pages.dev` to `staging.<project>.pages.dev` (your branch's address from step 2). **Leave it proxied** (orange cloud on). An unproxied (gray-cloud) record silently serves the *live* site on the staging address.
5. Open `staging.yourdomain.com`. That's your staging site, forever at that address.

Staging is automatically hidden from Google (it sends `X-Robots-Tag: noindex`), so customers never stumble onto the preview copy. Don't "fix" that, it's on purpose.

**No custom domain?** Everything still works: staging lives at `staging.<project>.pages.dev`. The pretty subdomain just needs DNS on Cloudflare.

**One-time safety lock (recommended):** on GitHub, open your site repo → **Settings** → **Branches** → **Add branch protection rule**. Branch name pattern: `main`. Check **Require a pull request before merging**. Save. From now on, nothing can go live without going through the preview step first, even by accident. (This closes the one hole in the golden loop: the pencil editor on GitHub could otherwise push straight to the live site.)

## Step 7: Business email (10 minutes, recommended)

**Receiving** (free, Cloudflare Email Routing):

1. Cloudflare dashboard → **Email** → **Email Routing** → Enable, select your domain.
2. Add a destination address: your personal Gmail. Cloudflare emails a verification link to that address: click it before continuing, or routing stays off.
3. Create a custom address: `hello@yourdomain.com` → your Gmail. Add `noreply@` too if you'll use the contact form.
4. Cloudflare adds the MX records. Test: send an email to `hello@yourdomain.com` and watch it land in your Gmail.

**Sending** (free, Resend; needed for the contact form):

1. Sign up at [resend.com](https://resend.com) (free tier).
2. Add your domain, add the DNS records Resend shows you (SPF/DKIM), wait for verification. Finish this before you tell customers about the form: mail from an unverified domain lands in spam.
3. Create an API key (Sending access only).
4. Cloudflare → Pages → your site → **Settings** → **Environment variables** → Production → add two variables (mark them secret/encrypted):
   - `RESEND_API_KEY`: the key from step 3.
   - `CONTACT_TO_EMAIL`: the business email address where form messages should land. Without it, the form cannot deliver.
5. Redeploy once (Deployments → latest → Retry deployment) so the function picks it up.

Until the key exists, the form still shows on the page but cannot deliver: anyone who submits sees a note saying email is not set up yet and is asked to email you directly. Nothing breaks.

**Replying as the business from Gmail** (optional): Gmail → Settings → Accounts → "Send mail as" → add `hello@yourdomain.com` with these values: SMTP server `smtp.resend.com`, port `465`, username `resend`, password: your Resend API key. Now replies come from the business address.

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
