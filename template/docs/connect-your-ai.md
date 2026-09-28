# Connect your AI: use the subscription you already pay for

Your AI assistant is your web developer. It runs on the chat subscription you already have (Claude, ChatGPT, or similar). You do **not** need to buy API access or pay any usage-based billing for the AI itself. (Your site uses at most two free service keys for contact-form email and visitor stats; those are covered in [api-keys.md](api-keys.md) and have nothing to do with your AI.) If an AI ever asks you for an API key *for itself*, say no and tell it to proceed without one.

Two people make this work, and one flow serves both.

- **The owner** runs the business and, from now on, the website. After the one-time setup, they run it entirely through conversation: they talk to the AI in plain words, check the preview on their phone, and say "ship it." They never install anything, never type a command, never choose between technical options.
- **The helper** is the somewhat-savvy person who does the one-time setup: a Fiverr freelancer, a friend, a family member. They follow [setup-guide.md](setup-guide.md), connect everything once, and hand it over. (No helper? A capable AI can walk the owner through setup too; the guide says where.)

There are no paths to choose. The owner opens the AI they already use and talks. The AI reads the site's operating manual (`CLAUDE.md`) and handles the mechanics itself: if it can reach the site files, it edits directly; if it can't, it gives the owner or helper exact click-by-click steps. Nobody picks a lane.

## If you're the owner: connect in two minutes

1. Open the AI you already pay for: the Claude or ChatGPT app, their websites, or this chat.
2. Give it the operating manual: attach your site's `CLAUDE.md`, or tell it where your site folder lives. (Your helper may have already done this during setup.)
3. Say: **"read CLAUDE.md."**

Then just talk, like in [these real examples](examples.md):

```
Change my Saturday hours to 9am to 2pm.
```

The rhythm from here on: you ask, the change appears on your preview copy, you look at it on your phone, you say **"ship it."** That's the entire job. If your AI has direct access to your files, it edits them and sends you the preview link; if it doesn't, it hands you the exact clicks and paste text and you do the clicking, like in [the browser-only guide](browser-only.md). If your AI ever asks you to choose between technical options, say: "you decide, just get me the preview link."

One thing to know: in a plain browser chat, the chat forgets the manual when you start a new conversation. Re-attach `CLAUDE.md` at the start of each new chat and say "read CLAUDE.md" again.

**If all you have is this browser chat** (no coding app, no terminal, no helper): start with [docs/browser-only.md](browser-only.md). It is the complete path from a ChatGPT or Claude account to a live site, every step written out, nothing installed.

## If you're the helper: the one-time setup

You're here because the owner trusts you with the technical afternoon. It's about an hour, and [setup-guide.md](setup-guide.md) is written for you, step by step.

1. Get the site folder on GitHub and connected to Cloudflare Pages (setup guide, Steps 1 through 6).
2. Connect the owner's AI to the site: point their AI app at the site folder or repo, open `CLAUDE.md` together, and send the copy-paste message below.
3. Do one real change together while the owner watches: change a headline, open the preview link on their phone, say "ship it." Once they've seen the loop, you're done.
4. Hand it over. The owner runs day-to-day updates alone from here. They'll call you when something looks weird.

### How the AI reaches the files (mechanics reference)

The contract is the same everywhere: `CLAUDE.md` + `rules/` tell any AI its job. Only the write path varies, and the AI sorts it out on its own. This table is for you, not the owner.

| AI | How it sees the files | What happens on a change request |
|---|---|---|
| **Claude Code** (terminal app, Claude subscription) | Opens the site folder directly | Full loop: edits, commits, pushes; the owner approves the preview |
| **Claude Cowork** (Claude app, paid plans) | The owner grants it the site folder; it reads and writes files, no terminal | Edits directly; sync the folder to GitHub with the bridge below |
| **muse.ai** (this chat) | Full access while working here | Full loop: edits, preview branches, deploys, all handled in chat |
| **ChatGPT app / agent mode** | Varies by version: a local folder or the GitHub connector | If it edits files directly, sync with the bridge below; otherwise it drafts and you apply it |
| **claude.ai or chatgpt.com in the browser** | Attach files, or connect the GitHub repo if the plan offers it | It drafts the change; apply it with GitHub's edit button ([editing-in-browser.md](editing-in-browser.md)) |

**The no-terminal bridge:** if the owner's AI edits files on their computer but can't push to GitHub itself, install GitHub Desktop (free, from GitHub). It syncs the folder with one click, no commands. Tell the owner to press it when their AI says so.

## Copy-paste first message

The owner sends this to their AI:

```
I just set you up with my website files. Read CLAUDE.md first, then tell me
in one or two plain sentences what you understood your job to be.
```

If its answer sounds right (changes go to the staging preview first, nothing goes live without my "ship it"), you're connected.

## If something's confusing

- **"Which AI should the owner use?"** Whichever they already pay for. Claude, ChatGPT, muse.ai, all fine. Never make them buy something new.
- **"The menus look different from the guide."** They move. Tell the AI where you are ("I'm on the settings page and I don't see...") and it will guide you from there.
- **"The AI can't see the repo."** Attach `CLAUDE.md` to the chat. That file plus the question is enough for most tasks.
- **"It asked for an API key."** It doesn't need one for itself. Say: "No API keys for you. Work with my chat subscription." If it insists, it's confused; start a fresh chat.
