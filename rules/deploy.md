# Deploy rules — shipping a change

Two branches, two sites. Simple on purpose:

- **`staging` branch → staging site** at `staging.<project>.pages.dev`. Every change lands here first. The owner bookmarks one link and always knows where to look.
- **`main` branch → production** at their domain. Only ever updated by merging `staging` after the owner approves what they saw on staging.

Pushing to `staging` rebuilds the staging site. Merging `staging` into `main` rebuilds production. **The push is the release.** There is no other environment.

## The flow (beginner default)

1. Make the change and push it to **`staging`** (commit straight to the branch; no feature-branch ceremony for routine changes).
2. Hand the owner the staging link. In beginner-friendly words: "Here's your staging site with the change. Open it on your phone and look around."
3. **Wait for their approval.** "Looks good, ship it" or equivalent. Never assume.
4. Merge `staging` into `main` and push. Cloudflare rebuilds and deploys production in about a minute.
5. Run `npm run audit https://<their-domain>` against production and report the result.

The staging link IS the approval step. If the owner ever asks "where do I check?", the answer is always the same link.

## Before you claim it works

```bash
npm run build            # must pass with zero errors
```

Then actually open the preview URL: the changed pages, at phone width, plus one desktop check. Click every link and button you touched. Submit the contact form once if you touched it.

"Should be fine" is not verification. Say which checks ran and which didn't.

## Production differs from local

Things that pass locally and fail live:

- **`public/_headers` and `public/_redirects`** only apply on Cloudflare, not on `npm run dev`. Verify redirects and headers against the preview/production URL, not localhost.
- **Environment variables:** `RESEND_API_KEY` and friends live in Cloudflare (Pages → Settings → Environment variables), not in the repo. The contact form degrades gracefully without the key; verify the degraded state too.
- **Build-time tokens** (`{{business.name}}` etc.) resolve during `npm run build`. If a token shows up literally on a page, the build transform missed it: check the plugin, don't hardcode the value.

## Never deploy manually

Don't run `wrangler deploy`, `wrangler pages deploy`, or dashboard deploy buttons that bypass git. Manual deploys ship the working tree instead of `main`: uncommitted code goes live with nothing in git recording it, and the next push silently reverts it. If CI is down and a manual deploy looks necessary, stop and talk to the owner first.

## Rolling back

Two ways, easiest first:

1. **Dashboard (no terminal):** Cloudflare → Pages → the site → Deployments → find the last good deployment → ⋯ → **Rollback**. This is the one to teach the owner. (Works for production; staging fixes itself on the next push to `staging`.)
2. **Git:** revert the merge commit on `main` and push. The revert itself goes to staging first, like any change.

Never hand-edit production. Never "fix it live and commit later."
