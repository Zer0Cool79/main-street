# AGENTS.md

This repo is designed to be maintained by a business owner working with **any** AI coding assistant: Claude Code, Cursor, GitHub Copilot, Codex, or similar.

**`CLAUDE.md` is the source of truth.** Despite the name, it is written tool-agnostically: the role definition, the triggers table, the hard rules, and the pointer to `rules/beginner-mode.md` apply no matter which assistant is reading. If your tool prefers `AGENTS.md`, this file tells you to go read `CLAUDE.md` and follow it exactly.

Conventions shared by all tools here:

- `site.config.json` is the source of truth for business facts and feature flags.
- `rules/` holds focused instruction files. Load them on demand per the triggers table in `CLAUDE.md`; don't preload everything.
- `features/` holds one doc per toggleable feature, plus `INDEX.md` as the catalog.
- `presets/` holds business-type bundles applied via `npm run preset <name>`.
- Every change ships as: branch → preview URL → owner approves with their eyes → merge to `main` → Cloudflare Pages deploys. Never push straight to `main` for review, never deploy manually.
- The owner may be non-technical. `rules/beginner-mode.md` governs communication and overrides default assistant habits.
