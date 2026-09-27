# Connect your AI: use the subscription you already pay for

Your AI assistant is your web developer. It runs on the chat subscription you already have (Claude, ChatGPT, or similar). You do **not** need API keys, API credits, or any usage-based billing. If an AI ever asks you for an API key, say no and tell it to proceed without one.

There are two ways to connect. Path A is the full experience. Path B needs nothing installed.

## Path A: an AI app with access to your site folder (recommended)

This is the setup where the golden loop works exactly as described: you talk, your AI edits the site, you get a preview link, you say "ship it."

1. Install your AI provider's coding app on your computer. (For Claude, that's Claude Code. Your ChatGPT subscription has an equivalent. Names change; your AI chat can tell you the current one.)
2. Sign in **with your existing subscription**. Not an API key. There is nothing extra to buy and no per-message meter running.
3. Open your website's folder in the app.
4. Say: **"read CLAUDE.md."** That's the whole setup. CLAUDE.md is the operating manual your site carries for exactly this moment.

From here, every update is a conversation. Your AI can edit files, run the checks, and put changes on your staging site for your approval.

## Path B: web chat plus GitHub in your browser (nothing to install)

If you'd rather not install anything, this works with plain claude.ai or chatgpt.com in your browser.

1. Open a new chat. Attach your site's `CLAUDE.md` (and the specific file you're asking about, if you know it). Some plans can also connect to your GitHub repo directly; if yours offers that, connect it.
2. Say: "read CLAUDE.md in the files I attached. You're my web developer."
3. Ask for your change in plain English. Your AI will draft it and show you exactly what changed.
4. You apply it with GitHub's edit button: [editing-in-browser.md](editing-in-browser.md) walks through it click by click. Always edit the `staging` branch first, check the preview link, then say "ship it."

Path B is slower for big changes (you're the hands), but it needs zero setup and works from any computer, including a Chromebook or a library PC.

## Which AI do you use? (interface map)

The contract is the same everywhere: `CLAUDE.md` + `rules/` tell any AI its job. Only the *write path* changes: can it put the change on your staging site itself, or does it hand you the change to apply?

| Your AI | How it sees your files | What happens when you ask for a change |
|---|---|---|
| **Claude Code** (terminal app, Claude subscription) | Opens your site folder directly | Full loop: it edits, commits, pushes; you approve the preview and say "ship it" |
| **Claude Cowork** (Claude app, paid plans) | You grant it your site folder; it reads and writes files, no terminal | It edits files directly; sync the folder to GitHub with the bridge below |
| **muse.ai** (this chat) | Full access while you work here | Full loop: edits, preview branches, deploys, all handled in chat |
| **ChatGPT app / agent mode** | Varies by version: a local folder or the GitHub connector | If it edits files directly, sync with the bridge below; otherwise it drafts and you apply it |
| **claude.ai or chatgpt.com in the browser** | Attach files, or connect your GitHub repo if your plan offers it | It drafts the change; you apply it with GitHub's edit button ([Path B](#path-b-web-chat-plus-github-in-your-browser-nothing-to-install)) |

**The no-terminal bridge:** if your AI edits files on your computer but can't push to GitHub itself, install GitHub Desktop (free, from GitHub). It syncs your folder with one click, no commands. Your AI will tell you when to press it.

**Interfaces change fast.** If yours isn't listed or the menus moved, the two questions that matter are: *can it see my files?* and *can it get changes to GitHub?* Tell your AI the answers and say "get me to the staging preview."

## Copy-paste first message

```
I just set you up with my website files. Read CLAUDE.md first, then tell me
in one or two plain sentences what you understood your job to be.
```

If its answer sounds right (changes go to the staging preview first, nothing goes live without my "ship it"), you're connected.

## If something's confusing

- **"I don't know which app to install."** Ask your AI chat: "I pay for [Claude/ChatGPT]. What app do I install so you can work directly in my website folder, using my subscription and no API keys?"
- **"The menus look different from the guide."** They move. Tell your AI where you are ("I'm on the settings page and I don't see...") and it will guide you from there.
- **"My AI can't see my repo."** Attach `CLAUDE.md` to the chat yourself. That file plus your question is enough for most tasks.
- **"It asked me for an API key."** It doesn't need one. Say: "No API keys. Work with my chat subscription." If it insists, it's confused; start a fresh chat.
