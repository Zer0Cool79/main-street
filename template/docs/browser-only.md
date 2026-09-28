# The browser-only path: from a ChatGPT or Claude account to a live site

This is the complete path for the person who has **nothing but a chat AI account** (claude.ai or chatgpt.com) and a web browser. No terminal, no installs, no code editor, no helper. Every step is written out; nothing is skipped, because a skipped step is where people get lost.

What you will have at the end: a live business website at your own address, which you update by chatting and clicking buttons on websites.

What you will never do: type a command, install a program, or write code. You will click buttons on the GitHub and Cloudflare websites. That is the whole toolkit.

Time: about two hours the first time, unhurried.

---

## Part 1: The three accounts (15 minutes)

You need three free accounts. You already have the first.

**1. Your AI.** Your Claude or ChatGPT account. Done.

**2. GitHub** (where your website's files live). Go to github.com, click **Sign up**, and follow the steps. Confirm your email when it arrives. Pick any username; it barely matters.

**3. Cloudflare** (the service that puts your site on the internet). Go to dash.cloudflare.com, click **Sign up**, and follow the steps. Confirm your email when it arrives.

Write your three logins somewhere safe. You will sign in to GitHub and Cloudflare several times today.

---

## Part 2: Get the website files onto GitHub (20 minutes)

Your site starts as a folder of files called the **template**. You will download it and upload it to your own GitHub repository (think of a repository as a folder with a memory: it remembers every change).

**Step 1: Download the template.**

1. Open this page in your browser: `https://github.com/davegelinas/main-street`
2. Click the green **Code** button, then click **Download ZIP**. Save the file.
3. Find the ZIP in your Downloads and **double-click it**. Your computer unzips it with built-in software; nothing to install. You now have a folder named `main-street-main`. Open it, then open the **`template`** folder inside it. Leave this window open; you will come back to it.

**Step 2: Create your repository.**

1. Go to github.com (signed in). Click the **+** at the top right, then **New repository**.
2. **Repository name:** your business name plus `-site`, all lowercase with dashes. Example: `maple-street-bakery-site`. (No spaces. Dashes are fine.)
3. Choose **Private**. Your drafts stay yours.
4. **Important:** leave **Add a README file** unchecked. An empty repository makes the next step easy.
5. Click **Create repository**.

**Step 3: Upload the template's contents.**

1. On your new (empty) repository page, click the **uploading an existing file** link.
2. Go back to the `template` folder window from Step 1. Select everything inside it (Ctrl+A on Windows, Cmd+A on Mac): the folders AND the loose files, all at once.
3. **Drag that whole selection into the GitHub upload area.** Use drag and drop, not the "choose your files" link: the link uploads every file as one flat pile and the folders are lost; dragging keeps the inside of each folder intact. (You are uploading the *contents* of the template folder, not the folder itself.)
4. Wait until every file finishes uploading (there are about 88; give it a minute or two).
5. **Check the staged list before you commit.** You should see folder paths like `docs/browser-only.md` and `content/brand/photos/`. If you see bare filenames with "dup" markers instead (two `index.html`, three `README.md`), the folders did not come along: remove every file and re-drag, making sure you drag the folders themselves, not a file picker selection.
6. Click **Commit changes** (the green button). Leave the message as is.

Note: the hidden `.github` folder often does not come along in a drag (your computer hides it even from itself). Step 4 checks for it.

**Step 4: Check the hidden folder made it.**

Scroll through your repository's file list. You should see a folder named **`.github`** (with a dot in front). It runs automatic safety checks on your changes. (Cloudflare builds every branch except the production one automatically, so your staging branch gets its preview build with no extra settings needed.)

- **If you see `.github`:** you are done with this part.
- **If you don't see it:** your computer hid it during the upload. This is normal and fixable in two minutes:
  1. In your repository, click **Add file** (top right), then **Create new file**.
  2. In the **name** box at the top, type exactly: `.github/workflows/ci.yml` (the slashes create the folders).
  3. Open the downloaded ZIP's copy of this file on your computer (in the template folder, `.github/workflows/ci.yml`). On a Mac, open TextEdit first, then use File > Open and press Cmd+Shift+Period to reveal hidden files. On Windows, in File Explorer open the folder and choose View > Show > Hidden items. Select all, copy.
  4. Paste into the big text box on GitHub. Click **Commit changes**.

**Step 5: Add the last hidden file.**

One more tiny file almost never survives the upload: `.node-version`. It tells the automatic checks which tools to use, and without it every change shows a confusing red X.

1. Click **Add file** (top right), then **Create new file**.
2. In the **name** box, type exactly: `.node-version`
3. In the big text box, type exactly: `22`
4. Click **Commit changes**.

**A word about the checks.** After each save, GitHub runs an automatic check on your files. A green check mark means everything is fine. A red X means something in the files is broken. Do not panic: copy the error text into your chat and your AI will hand you the fix. Most fixes are one paste.

Your repository now holds your entire website. Nothing is public yet; you have not connected anything.

---

## Part 3: Introduce your AI to your site (5 minutes)

Your AI has not seen your site yet. Give it the site's operating manual, then tell it your situation in one message.

**Step 1: Start a new conversation** at claude.ai or chatgpt.com.

**Step 2: Attach three files.** Click the **paperclip** (attach) button in the chat box and upload these files from the `template` folder you downloaded:

- `CLAUDE.md`
- `AGENTS.md`
- `rules/beginner-mode.md`

(These are the operating manual your site carries for any AI. Your AI will read them. If it ever needs another file from the `rules/` folder later, it will ask you to attach that one too.)

**Step 3: Send this message.** Copy and paste it exactly:

```
I just put my new business website on GitHub. I only have this browser chat:
I cannot run commands, install anything, or use a terminal. For every task,
give me steps I can do in the browser on github.com, with the complete text
to copy and paste. Never ask me to run a command.

Start by interviewing me for the site setup, one question at a time: business
name, tagline, address, phone, email, hours, services, prices, and anything
else site.config.json needs. When you have asked everything, first ask me to
open site.config.json on GitHub and paste its current contents here, so your
version keeps every section and key exactly as the template has them. Do not
invent, rename, or drop any keys. Then output the complete site.config.json
file for me to paste into GitHub.
```

---

## Part 4: Answer the setup questions, paste the config (20 minutes)

**Step 1: Answer the AI's questions.** It will ask one at a time, in plain words. Answer in plain words. For anything you don't have yet, say "skip it, I'll add it later." Nothing here is permanent.

**Step 2: Copy the AI's output.** When the questions are done, the AI will output the complete `site.config.json` file: a big block of text starting with `{` and ending with `}`. Copy the entire block.

**Step 3: Paste it into GitHub.**

1. Go to your repository on github.com. Check the branch dropdown (top left) says **`main`**.
2. Click the file **`site.config.json`**.
3. Click the **pencil icon** (Edit this file) at the top right.
4. Click inside the text box, select everything (Ctrl+A or Cmd+A), and paste (Ctrl+V or Cmd+V) the AI's text over it.
5. Click **Commit changes** (green button). Leave the defaults.

**Step 4: Tell the AI "done."** It may ask you to paste the file back so it can double-check; if it does, open the file on GitHub, copy the text, and paste it into the chat.

---

## Part 5: Add your photos (15 minutes)

Real photos beat everything. Use your phone.

**Step 1: Pick 5 to 10 photos.** Storefront, interior, your work, your team. The best photos are bright and simple. Use JPG or PNG photos: iPhones sometimes save photos as HEIC, which websites cannot display. To switch, open iPhone **Settings** → **Camera** → **Formats** → **Most Compatible** (new photos will be JPG).

**Step 2: Upload them.**

1. On github.com, in your repository, click through to the folder **`content/brand/photos/`**.
2. Click **Add file**, then **Upload files**.
3. Drag your photos in from your phone or computer. (If a photo is over 25 MB, shrink it first; phone photos are usually fine.)
4. Click **Commit changes**.

**Step 3: Tell the AI.** Go back to the chat and say: "I uploaded my photos to content/brand/photos. Here are the filenames: ..." (list what you uploaded). The AI will tell you exactly what to paste and where so the photos appear on the site, usually back in `site.config.json`.

---

## Part 6: Create your staging branch (3 minutes)

From here on, you work with **two copies** of your site:

- **`main`** is your live site, the one customers see.
- **`staging`** is your draft copy, where changes appear first so you can check them privately.

**Steps:**

1. On your repository page, click the branch dropdown (it says **`main`**).
2. Click **View all branches**.
3. Click **New branch**.
4. Type `staging` as the branch name. Make sure it says it will be created from `main`.
5. Click **Create new branch**.

---

## Part 7: Connect Cloudflare (15 minutes)

This connects your GitHub repository to the service that publishes your site.

**Step 1: Start the connection.**

1. Go to dash.cloudflare.com (signed in). Click **Workers & Pages** in the left menu.
2. Click **Create**, then choose the **Pages** option (the website option, not Worker). Then **Import an existing Git repository** → **Get started**, which takes you to **Connect to Git**.
3. GitHub will ask to authorize Cloudflare. Choose your GitHub account. When it asks for repository access, pick **Only select repositories** and choose your site repository (not everything). Click **Save** or **Install**.
4. Back in Cloudflare, select your site repository from the list and click **Begin setup**.

**Step 2: Enter the build settings exactly as follows.**

- **Project name:** your business name in lowercase with dashes (this becomes your first web address, like `maple-street-bakery.pages.dev`).
- **Production branch:** `main`
- **Framework preset:** leave at **None**. (There is no plain Vite option in the list; the similar-looking VitePress and React (Vite) are different things. Do not pick them.)
- **Build command:** `npm run build` (typing this into the box on the website is fine; the thing you never do is type into a black terminal window)
- **Build output directory:** `dist`
- Leave everything else as is. Click **Save and Deploy**.

**Step 3: Wait.** Cloudflare builds your site (one to three minutes). When you see a green checkmark, your site is live at the address shown, something like `https://maple-street-bakery.pages.dev`.

**Step 4: Know where your staging (preview) address will appear.**

1. In Cloudflare, click your project, then the **Deployments** tab. Right now there is only a `main` row. That is normal: Cloudflare builds a branch only after it changes, and your `staging` branch has not changed since before Cloudflare was connected.
2. Your first commit to `staging` (Part 8, Steps 1-2) triggers its first preview build. After that, a row whose **Branch** column says `staging` appears here. Click it.
3. Its address looks like `https://staging.maple-street-bakery.pages.dev`. **Bookmark this.** This is your preview link.

A note on privacy: the preview link is not access-protected. Anyone who has the address can open it, but it is not linked from anywhere public. That is plenty for a pre-launch preview; just do not treat it as password-protected.

---

## Part 8: Review and fix (the loop you will repeat forever)

From here on, your job is the conversation: you talk, you look at your phone, you say "ship it." Your AI handles the mechanics. On a pure browser chat it cannot click for you, so it gives you the exact clicks, a minute or two at a time.

**Step 1: Tell the AI what's wrong, in plain words.** Examples: "My phone number is wrong, it should be 555-0142." "I don't like the blue, make it green." "Add that we do emergency calls."

**Step 2: Follow the AI's paste steps.** The AI will answer with exact steps: which file to open on github.com, what to find, and the complete replacement text. **Before you paste, check the branch dropdown says `staging`, not `main`.** Then commit.

**Step 3: Open your staging preview on your phone.** The very first time, this commit is what triggers the preview build, so give Cloudflare two or three minutes, then find it: go to dash.cloudflare.com, click **Workers & Pages** in the left menu, click your project name, then the **Deployments** tab → the row whose **Branch** says `staging` → open its address. Bookmark it. Tap through every page: home, services, contact. Read every word out loud if you can; you will catch mistakes.

**Step 4: Repeat.** After each new commit to `staging`, wait a couple of minutes, then reload the staging link. If it looks unchanged, open it in a private/incognito window (your browser may be showing the old cached copy). Keep going until you love it. This loop is the whole job, now and forever.

---

## Part 9: Go live ("ship it", 5 minutes)

When the staging site looks right, you publish it with three clicks. A "pull request" is just GitHub's name for copying your staging draft into your live site. You are not asking anyone for anything.

1. On github.com, in your repository, click **Pull requests** (top menu), then **New pull request**.
2. Set the **base** dropdown to **`main`** and the **compare** dropdown to **`staging`**. (Read it as: "take what's in staging and put it into main.")
3. Click **Create pull request**, then **Merge pull request**, then **Confirm merge**. If the merge button gets stuck saying "Checking for the ability to merge" for more than a minute, reload the page.
4. Wait about a minute. Open your `pages.dev` address: your site is live.

From now on, **"ship it"** means those clicks. You can also just tell your AI "ship it" and it will walk you through them.

---

## Part 10: Your own domain (whenever you're ready)

The `pages.dev` address works, but customers expect `yourbusiness.com`. A domain costs about $10 to $15 per year, and that is the only money this whole project costs.

**The simple version:** buy the domain inside Cloudflare so everything stays in one place: dash.cloudflare.com → **Domain Registration** → search and buy. Then in your Pages project → **Custom domains** → **Set up a custom domain** → enter your domain → Activate. Cloudflare handles the rest.

**Read this before you touch DNS or email:** if you already own a domain, or your business email runs on your domain (like `you@yourbusiness.com`), **do not change DNS records without reading `docs/domains-and-dns.md` first**, or ask your AI: "I have email on my domain. What do I need to protect before connecting it?" Done wrong, this can stop your email from working. Done right, it takes ten minutes.

**Contact form emails** (so the form sends inquiries to your inbox) need one free key from Resend. It is all done in the browser: `docs/api-keys.md` walks through it, or ask your AI: "walk me through the Resend key, step by step, browser only."

---

## The 10-second pre-paste checklist

Before every paste, confirm three things:

1. The branch dropdown says **`staging`**, not `main`.
2. You are in the file the AI named.
3. You copied the AI's **complete** block, not half of it.

Put this on a sticky note until it's habit.

---

## When something goes wrong

**"I uploaded the template folder itself instead of its contents."** You'll know because your repository's file list shows a single folder named `template` instead of files like `site.config.json` and `index.html`. Easiest fix: delete the repository and start Part 2 over (repository page → **Settings** → scroll to **Danger Zone** → **Delete this repository**). Nothing is lost; nothing was connected yet.

**"I pasted and the site looks broken."** Almost always a missing comma or quote in `site.config.json`. Open the file on GitHub, copy its contents into the chat, and say: "I broke it, here's the file." The AI will hand you a fixed complete file to paste back.

**"Cloudflare says the build failed."** In Cloudflare, open the failed deployment, click **View build log**, copy the red error lines, and paste them to the AI. It will tell you the exact fix.

**"I published something bad."** In Cloudflare: your project → **Deployments** → find the last good entry → click the three dots → **Rollback**. One click, and the previous version is live again.

**"I can't find my staging link."** Cloudflare dashboard → Workers & Pages → your project → **Deployments** tab → the row whose branch says `staging`.

**"I edited the wrong branch."** It happens. Tell the AI exactly what you did ("I pasted the new hours into main instead of staging"). It will tell you the two or three clicks that fix it. Nothing is unfixable; every change is remembered and reversible.

**"My AI seems lost."** Start a fresh message with: "Read CLAUDE.md again. I am browser-only: no commands, browser steps with complete paste text." If you started a brand-new chat, re-attach `CLAUDE.md`, `AGENTS.md`, and `rules/beginner-mode.md` first.

---

## What you never need

- No terminal, no black window with text, ever.
- No programs installed for this. Your browser is the toolkit.
- No API keys for your AI. It runs on the ChatGPT or Claude subscription you already pay for.
- No git commands, no GitHub Desktop. The buttons on the GitHub website are the whole workflow.
- No choosing between technical options. If your AI ever asks you to pick a technical path, say: "You decide. Just get me the preview link."
