# START HERE

Welcome. This checklist takes you from "I have the toolkit" to a live small-business website. No experience assumed. If a step confuses you, open your AI chat (muse.ai, claude.ai, chatgpt.com, or whichever you use) and say "walk me through this step."

**The honest shape of this checklist:** steps 1–3 are the only terminal you'll ever touch (about 15 minutes). Everything after handover, the owner's entire life with the site, is just chatting. See [connect your AI](template/docs/connect-your-ai.md) for how the owner's side connects.

## 0. Understand what this is

This toolkit is the **generator**. It holds a pristine site template and a scaffolder script. You use it to create one **customer site**: a separate folder (and later its own GitHub repo) that belongs to the business. The business owner lives in their site with their AI assistant; they never see this toolkit.

## 1. Create the site (2 minutes)

On your computer, in a terminal, from this toolkit folder:

```bash
node scripts/new-site.mjs ../acme-plumbing
```

(Replace `../acme-plumbing` with the business's folder name.) The `../` matters: your site lives **next to** the toolkit, not inside it. The toolkit stays pristine so you can make more sites later, and your site gets its own GitHub repo. The script copies the template, names everything correctly, verifies the copy, and initializes git. It refuses to overwrite a non-empty folder without `--force`, refuses to build inside the toolkit folder, and it never touches the network.

## 2. Make it theirs (10 minutes)

```bash
cd ../acme-plumbing
npm install
npm run setup
```

`npm install` downloads the build tools (one time). `npm run setup` asks plain-language questions: business name, phone, email, address, domain, what kind of business, then configures everything. At the end it prints the status of the two free integrations (contact-form email, visitor stats) and points to the setup guide.

## 3. See the site (1 minute)

```bash
npm run dev
```

Open the address it prints (usually http://localhost:5173). The copy is neutral placeholder text right now. Ask your AI: "rewrite the homepage copy for this business, keeping the layout."

## 4. Put it on the internet (15 minutes)

Full walkthrough inside the site: `docs/setup-guide.md`. The short version:

1. **Buy the domain** at Cloudflare Registrar (~$10-12/year, no markup).
2. **Save and push the site.** The scaffolder staged everything locally; now make it real. From your site folder: `git branch -M main`, then `git commit -m "First version of the site"`. Create the repo at github.com/new (same name as the folder), then `git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPO.git` and `git push -u origin main`.
3. **Connect the site's repo to Cloudflare Pages**: Workers & Pages → Create → Continue to Pages → Import an existing Git repository → Get started → Connect to Git → pick the repo. Build command `npm run build`, output directory `dist`, framework preset None (there is no plain Vite option; do not pick the similar-looking VitePress or React (Vite)).
4. **Push to the `staging` branch** → Cloudflare builds a preview. Once you attach your custom domain (setup guide Step 6), the preview lives at `staging.yourdomain.com`; until then it's `staging.<project>.pages.dev`. The preview row appears after your first commit to `staging` once Cloudflare is connected; it will not exist before that. The owner reviews every change here.
5. **Owner says "ship it"** → merge `staging` into `main` → the live domain updates in about a minute.

## 5. Hand it over

Point the owner at their site's **README.md** and **[docs/examples.md](template/docs/examples.md)**: the "see, it's actually easy" proof. Their whole job from now on: tell their AI what they want, look at the preview link on their phone, say "ship it."

## If something looks wrong

1. Don't panic. Nothing here can send anyone a bill and almost nothing is irreversible.
2. Ask the AI: "what just changed, and how do we undo it?"
3. The fastest undo: Cloudflare dashboard → Workers & Pages → the site → Deployments → find the last good one → **Rollback**. No terminal needed.

---

Full honest cost breakdown: [docs/the-12-dollar-stack.md](docs/the-12-dollar-stack.md). The adversarial review of this whole system: [docs/pressure-test.md](docs/pressure-test.md).
