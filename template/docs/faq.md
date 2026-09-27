# FAQ

**Do I need to know how to code?**
No. The setup wizard asks plain-language questions, and day-to-day updates happen by talking to an AI assistant or editing text on GitHub.com. Reading this FAQ is the hardest technical thing you'll do.

**What does it actually cost?**
About $10–12/year for the domain name. Everything else is free-tier. Ask your AI assistant for the full honest breakdown (it covers free-tier limits and what could optionally cost money).

**Can I really not get a surprise bill?**
Correct. No service here bills by usage on the tiers we use. The domain renews yearly; that's the only charge.

**What if I break something?**
Cloudflare dashboard → Workers & Pages → your site → Deployments → find the last good one → ⋯ → Rollback. One click. Also, every change goes through a preview link you approve first, so breakage is rare.

**Do I own my website?**
Yes. It's your GitHub repo, your Cloudflare account, your domain. The template is just the starting point. If you stop using it, everything stays yours.

**What if the AI assistant makes a mistake?**
Tell it what you see in plain words. It can undo anything via git, and you can always roll back the deployment yourself. Mistakes here are cheap and reversible by design.

**Can I use my existing booking/scheduling tool?**
Yes. The booking feature links to Acuity, Calendly, Square, Vagaro, whatever you use. The site sends people there; it doesn't replace it.

**Does it work for online stores?**
Not really, and that's deliberate. This is for businesses where the website earns the visit or the call: restaurants, trades, salons, professional services. Real e-commerce (carts, payments, inventory) is a different product with different costs.

**Will my site show up on Google?**
The template handles the technical side (structured data, sitemap, speed, mobile). The human side matters more: claim your Google Business Profile, keep hours accurate, get reviews. See `rules/seo.md`.

**Can someone build this for me and hand it over?**
Yes. That's the normal way it happens. A freelancer (or a tech-savvy friend) sets the whole thing up in about an hour, in your accounts, and teaches you the update flow in ten minutes. From then on, it's yours.

**What happens if this template disappears?**
Nothing happens to your site. Your repo is a complete, independent copy. It builds with standard open-source tools and deploys to Cloudflare. No part of it phones home.

**Why not just use Squarespace/Wix?**
Those are fine products. This is for people who'd rather pay $12/year than $200+/year, own their site outright, and update it by having a conversation instead of wrestling a page builder.
