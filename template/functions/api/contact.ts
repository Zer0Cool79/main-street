// POST /api/contact: contact form handler (Cloudflare Pages Function).
// Sends via Resend. Gracefully degrades when RESEND_API_KEY is not set.

interface Env {
  RESEND_API_KEY?: string;
  FROM_EMAIL?: string; // optional override; defaults to noreply@<site domain>
  CONTACT_TO_EMAIL?: string; // where messages are delivered; set in Pages env vars
}

interface Payload {
  name?: unknown;
  email?: unknown;
  message?: unknown;
  website?: unknown; // honeypot: must stay empty
  startedAt?: unknown; // ms timestamp of when the form was shown
}

const json = (data: Record<string, unknown>, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } });

function friendlyError(): Response {
  return json(
    { ok: false, error: "Email is not set up yet. Please email us directly and we will get right back to you." },
    503,
  );
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;

  let body: Payload;
  try {
    body = (await request.json()) as Payload;
  } catch {
    return json({ ok: false, error: "Could not read your message. Please try again." }, 400);
  }

  const name = String(body.name ?? "").trim();
  const email = String(body.email ?? "").trim();
  const message = String(body.message ?? "").trim();

  // Bot signals: honeypot filled, or submitted faster than a human can type.
  if (String(body.website ?? "").trim() !== "") return json({ ok: true }); // pretend success
  const elapsed = Date.now() - Number(body.startedAt ?? 0);
  if (Number.isFinite(elapsed) && elapsed < 3000) return json({ ok: true }); // pretend success

  if (!name || !email || !message) {
    return json({ ok: false, error: "Please fill in your name, email, and message." }, 400);
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) {
    return json({ ok: false, error: "That email address does not look right. Please check it." }, 400);
  }
  if (message.length > 5000) {
    return json({ ok: false, error: "Please keep your message under 5000 characters." }, 400);
  }

  const apiKey = env.RESEND_API_KEY;
  const to = env.CONTACT_TO_EMAIL;
  if (!apiKey || !to) return friendlyError();

  const from = env.FROM_EMAIL ?? `noreply@${new URL(request.url).hostname.replace(/^www\./, "")}`;

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: email,
        subject: `Website message from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\n\n${message}`,
      }),
    });
    if (!res.ok) return friendlyError();
  } catch {
    return friendlyError();
  }

  return json({ ok: true });
};
