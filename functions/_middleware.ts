// Staging guard (Cloudflare Pages Function middleware, runs on every route).
// Keeps every non-production hostname out of search engines: the staging
// subdomain (staging.<domain>) and all *.pages.dev preview URLs get
// X-Robots-Tag: noindex. Production (the owner's domain, apex or www) is
// untouched.
//
// Hostname heuristic on purpose: zero configuration, correct from the first
// deploy, no env var to forget. The only hostname this misclassifies is a
// production domain literally starting with "staging." — don't do that.

export function shouldNoindex(hostname: string): boolean {
  const host = hostname.toLowerCase();
  return host.endsWith(".pages.dev") || host.startsWith("staging.");
}

export const onRequest: PagesFunction = async (context) => {
  const response = await context.next();
  if (!shouldNoindex(new URL(context.request.url).hostname)) return response;
  // Rebuild the response: headers on the returned response are not
  // guaranteed mutable, so copy them explicitly.
  const headers = new Headers(response.headers);
  headers.set("X-Robots-Tag", "noindex, nofollow");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
};
