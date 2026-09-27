# Editing in your browser: the simplest update path

You don't need anything installed to update your site. GitHub's website has an edit button, and saving an edit redeploys your site automatically. For text changes, this is often the fastest path of all.

## How it works

1. Go to your repo on **github.com**.
2. **Switch to the staging branch first.** At the top left there's a branch dropdown. If it says `main`, click it and choose `staging`. (This keeps the golden rule: your edit appears on your preview site first, not the live site.)
3. Click through to the file you want to change (e.g. `index.html`, or `site.config.json`).
4. Click the **pencil icon** (Edit this file) at the top right.
5. Make your change in the text box.
6. Click **Commit changes** (the green button). Leave the defaults.
7. Cloudflare sees the commit, rebuilds, and redeploys your **staging** site. Your change is on the preview link in about a minute. Look at it there. Then say "ship it" to your AI (or merge staging to main) to publish it.

That's the whole workflow. No terminal, no AI, no tools.

## What's safe to edit this way

- **Words on pages** (`index.html`): headlines, paragraphs, service descriptions. The HTML is plain and readable; change the text between the tags, leave the tags alone.
- **Business facts** (`site.config.json`): hours, phone, address, announcement banner text. Match the existing format exactly (quotes, commas). One misplaced comma breaks the file; if the site looks broken after, ask your AI assistant to fix it.
- **FAQ entries** (`index.html`): copy an existing question block, change the words.

## What to leave for your AI assistant

- Anything involving `<!-- feature: ... -->` markers, CSS, the contact function, or new pages.
- If you're unsure, you're one message away: "I want to change X, is it safe to edit in the browser?"

## Tips

- **One change per commit** while you're learning. Easier to undo.
- After committing, open your site in a private/incognito window to see the change (your browser may show the cached old version).
- Made a mistake? Every commit is reversible: ask your assistant, or find the commit in the repo's History tab and revert it.
- This path still uses your preview site (you edited the `staging` branch, remember), but there's no AI double-checking your work, so stick to small text edits here. Anything bigger goes through your AI assistant.
