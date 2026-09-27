# Connector rules

Connectors are **optional extras, never the default path**. The core setup (an AI tool plus a domain name) gets the owner far on cheap. Suggest a connector only when the owner asks for something beyond the basics that the chat AI can't produce natively: a logo or promo images (Canva), a short video (Higgsfield), selling products online (Shopify). Never pitch connectors unprompted and never frame them as required. If the owner can simply attach a file they already have, that's simpler than a new account, say so.

## What's verified (September 2026)

- **Canva**: official AI Connector, a hosted MCP server at `mcp.canva.com/mcp`. Works with ChatGPT (Settings → Apps & Connectors), Claude (Connectors), Cursor, Claude Code, and other MCP-capable assistants. Creates designs, autofills templates, finds existing designs, exports PDF/image. Requires **Canva Pro/Teams/Business/Nonprofit**; does NOT work on the free plan. OAuth sign-in, no API key.
- **Higgsfield**: MCP server at `https://mcp.higgsfield.ai/mcp`. 30+ image and video models, clips up to ~15 seconds, images up to 4K. Add as a custom connector in Claude (Settings → Connectors → Add custom connector) or any MCP-capable client. OAuth sign-in with a Higgsfield account, no API key. New accounts get free credits; heavy use is paid. Say so before generating a lot.
- **Shopify**: every store exposes an official Storefront MCP endpoint at `https://{shop}.myshopify.com/api/mcp` (no auth). Tools cover catalog search, product details, cart operations, checkout, and store policies. This is a *storefront* API: it lets the assistant read the catalog and link products. It does NOT put a cart inside the static site.

Anything else (Figma, Notion, other MCP servers the owner names): verify it exists before promising it. Connector menus differ per platform and change often; if you're unsure what's available on the owner's platform, say "let me check what's available on yours" and walk them through their platform's current steps instead of reciting click paths from memory.

## Shopify on a static site: honest boundaries

- **Do**: link products to the Shopify store; embed Shopify Buy Buttons (created in the Shopify admin) for checkout; pull product names, prices, and images into product pages via the Storefront MCP.
- **Don't**: promise in-site cart/checkout, inventory sync, or order management inside the static site. Checkout happens on Shopify. Say this plainly before the owner imagines otherwise.
- If the owner doesn't have Shopify yet and wants to sell online: Shopify is a paid monthly service. State the cost before they sign up.

## Rules

- **Tool-agnostic.** Never assume which assistant or platform the owner uses. "Ask your AI" beats a stale click path.
- **Cost honesty first.** Name the account or plan requirement before the owner signs up for anything: Canva Pro or higher, Higgsfield paid beyond free credits, Shopify monthly.
- **Secrets rule still applies.** Connecting uses OAuth sign-in buttons, never pasted keys. If a connector flow asks for an API key in chat, stop and find the official way.
- **Generated assets go through the normal loop.** Run `npm run optimize-images` after adding any image, then stage, owner approves on the preview copy, then ship.
- **Graceful fallback.** If the platform truly has no connector support, the owner makes the asset in the app and attaches the file. The connector is a convenience, never a blocker.
- Keep owner-facing wording in `docs/connectors.md` jargon-free and em dash free. "MCP" never appears in owner docs; it's "a plug-in" there.
