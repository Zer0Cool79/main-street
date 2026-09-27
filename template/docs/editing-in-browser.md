# Editing in your browser — the simplest update path

You don't need anything installed to update your site. GitHub's website has an edit button, and saving an edit redeploys your site automatically. For text changes, this is often the fastest path of all.

## How it works

1. Go to your repo on **github.com**.
2. Click through to the file you want to change (e.g. `index.html`, or `site.config.json`).
3. Click the **pencil icon** (Edit this file) at the top right.
4. Make your change in the text box.
5. Click **Commit changes** (the green button). Leave the defaults.
6. Cloudflare sees the commit, rebuilds, and deploys. Your change is live in about a minute.

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
- This path skips the preview-link step, so stick to small text edits here. Anything bigger goes through your AI assistant with a preview.
