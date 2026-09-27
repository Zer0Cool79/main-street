# Deploy rules — shipping a change

Pushing to `main` deploys to the live site. Cloudflare Pages builds (`npm run build` → `dist/`) and publishes automatically. **The push is the release.** There is no staging environment.

## The flow (beginner default)

1. Make the change on a **branch**, not `main`.
2. Push the branch. Cloudflare builds a **preview URL** (`<branch>.<site>.pages.dev`).
3. Hand the owner the preview link. In beginner-friendly words: "Here's a preview copy of your site with the change. Open it on your phone and look around."
4. **Wait for their approval.** "Looks good, ship it" or equivalent. Never assume.
5. Merge to `main`. Cloudflare rebuilds and deploys in about a minute.
6. Run `npm run audit https://<their-domain>` against production and report the result.

Routine small fixes may go straight to `main` *only* once the owner is experienced and has explicitly said they want that. Default to the preview flow.

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

1. **Dashboard (no terminal):** Cloudflare → Pages → the site → Deployments → find the last good deployment → ⋯ → **Rollback**. This is the one to teach the owner.
2. **Git:** revert the merge commit on `main` and push. The revert itself gets a preview first, like any change.

Never hand-edit production. Never "fix it live and commit later."
