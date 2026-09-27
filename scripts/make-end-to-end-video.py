#!/usr/bin/env python3
"""Build the end-to-end motion video: Cedar and Pine Barbershop, idea to live site.

Sibling to make-journey-video.py. Same visual language (cream background, ink
text, terracotta accent, gold highlight, serif display headlines, clean sans
body) and same technique: every on-screen word is an exact string below, drawn
with PIL, assembled with ffmpeg. Concept beats use the slide layout with
animated motifs; command-line beats use a dark monospace terminal card with
typed commands. No sound.

House rules baked in: no em dashes anywhere on screen, plain language,
no jargon.

The story follows the real dogfood run (see
~/workspace/dogfood/video-notes/JOURNEY.md): a non-technical barbershop owner
goes from a Facebook page to a live site.

Outputs (defaults):
  template/docs/assets/end-to-end.mp4
  template/docs/assets/end-to-end-poster.png

Regenerate with:  python3 scripts/make-end-to-end-video.py
Requires: Pillow, ffmpeg on PATH.
"""

import argparse
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette ---
CREAM = (250, 246, 239)
CREAM_DEEP = (243, 236, 223)
INK = (46, 38, 32)
INK_SOFT = (92, 81, 72)
ACCENT = (180, 85, 45)
ACCENT_DEEP = (143, 63, 32)
ACCENT_SOFT = (240, 221, 208)
GOLD = (201, 154, 46)
LINE = (229, 217, 200)
CARD = (255, 253, 248)
WHITE = (255, 255, 255)

TERM_BG = (38, 30, 26)
TERM_CREAM = (250, 246, 239)
TERM_DIM = (198, 186, 170)
TERM_GREEN = (150, 190, 140)
TERM_GOLD = (201, 154, 46)
TERM_ERR = (226, 142, 102)

W, H = 1280, 720
FPS = 30

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_B = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
SANS_R = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")
MONO_R = os.path.join(FONT_DIR, "NotoSansMono-Regular.ttf")

for p in (SERIF_B, SERIF_R, SANS_B, SANS_R, MONO_R):
    if not os.path.exists(p):
        sys.exit(f"missing font: {p}")


def font(path, size):
    return ImageFont.truetype(path, size)


# ------------------------------------------------------------------- story --
# kind, seconds, kicker, headline, sub, motif-or-terminal-lines.
# Terminal lines: (kind, text) with kind in cmd/out/err/ok/warn.
BEATS = [
    (
        "slide", 7.0, "STEP 1 OF 8",
        "It starts with a Facebook page",
        "No website yet, just a Facebook page. The owner finds Main Street on GitHub and opens the plain-English checklist.",
        "browser",
    ),
    (
        "term", 8.5, "STEP 2 OF 8",
        "A helpful mistake",
        "The first command forgets the ../. The script explains the fix in plain English, with the exact command to run.",
        [
            ("cmd", "node scripts/new-site.mjs cedar-pine"),
            ("err", 'Could not create the site: "cedar-pine" is'),
            ("err", "inside the toolkit folder. Your site needs its"),
            ("err", "own folder NEXT TO the toolkit. Run this instead:"),
            ("out", "  node scripts/new-site.mjs ../cedar-pine"),
            ("cmd", "node scripts/new-site.mjs ../cedar-pine"),
        ],
    ),
    (
        "term", 6.0, "STEP 3 OF 8",
        "The site is born",
        "The template copies over, everything gets named, git starts. About two minutes.",
        [
            ("cmd", "node scripts/new-site.mjs ../cedar-pine"),
            ("out", "Copying the site template..."),
            ("out", "Verifying the copy: every file present."),
            ("out", "Naming everything cedar-pine. Starting git."),
            ("ok", "Done! Your new site is ready."),
            ("out", "Next: cd ../cedar-pine, then npm install"),
        ],
    ),
    (
        "term", 8.5, "STEP 4 OF 8",
        "Plain questions, honest answers",
        "The wizard asks about the business. The salon preset fits barbers. Missing keys never break the page.",
        [
            ("cmd", "npm run setup"),
            ("out", "Business name: Cedar and Pine Barbershop"),
            ("out", "Tagline: Sharp cuts, honest prices, zero rush."),
            ("out", "Business type: salon-wellness (salons, spas, barbers)"),
            ("out", "Integrations status:"),
            ("warn", "  Contact form email: NOT SET UP"),
            ("out", "  Visitors see your email address instead."),
            ("out", "  The page never breaks."),
        ],
    ),
    (
        "slide", 7.0, "STEP 5 OF 8",
        "Fill the shoebox",
        "One folder for everything about the business. A phone photo, a few answers. Skipping the rest is fine.",
        "box",
    ),
    (
        "slide", 8.0, "STEP 6 OF 8",
        "The AI builds from the shoebox",
        "Photo optimized. Homepage rewritten in the owner's own words. Real hours asked, never invented. Build takes under a second.",
        "chat",
    ),
    (
        "term", 6.5, "STEP 7 OF 8",
        "Eight out of eight",
        "The audit checks the site the way visitors and search engines see it. All green before anything goes online.",
        [
            ("cmd", "node scripts/audit-site.mjs"),
            ("ok", "  pass: homepage returns 200"),
            ("ok", "  pass: legal pages return 200"),
            ("ok", "  pass: missing pages return a true 404"),
            ("ok", "  pass: search engines can find every page"),
            ("ok", "  8/8 checks passed"),
        ],
    ),
    (
        "slide", 8.0, "STEP 8 OF 8",
        'Push, preview, "ship it"',
        "Pushed to GitHub. Cloudflare builds the preview copy. The owner checks it on a phone, says ship it, and the site goes live.",
        "plane",
    ),
]

TITLE_LEN = 5.0
END_LEN = 5.5
FADE = 0.35

TITLE_KICKER = "MAIN STREET IN ACTION"
TITLE_HEAD = "Cedar and Pine Barbershop"
TITLE_SUB = "From idea to live site. The whole journey, in about a minute."

END_HEAD = "The $12/year website stack"
END_SUB = "About $12 a year for the domain name. Everything else is free."
END_TAG = "PREVIEW FIRST, SHIP IT AFTER"


# ------------------------------------------------------------------ helpers --
def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3


def clamp01(t):
    return max(0.0, min(1.0, t))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_alpha(base, draw_fn):
    """Run draw_fn(ctx) on a transparent overlay, then composite it."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ctx = ImageDraw.Draw(layer)
    draw_fn(ctx)
    base.alpha_composite(layer)


def text_fade(img, xy, s, fnt, fill, alpha, anchor="la"):
    if alpha <= 0:
        return
    a = int(255 * clamp01(alpha))
    draw_alpha(img, lambda c: c.text(xy, s, font=fnt, fill=fill + (a,), anchor=anchor))


def kicker_letterspaced(img, d, text, x, y, fnt, fill, alpha):
    kx = x
    for ch in text:
        text_fade(img, (kx, y), ch, fnt, fill, alpha)
        kx += d.textlength(ch, font=fnt) + 6


# ------------------------------------------------------------- terminal -----
TYPE_CPS = 45.0   # typed characters per second for commands
OUT_SLOT = 0.55   # seconds per output line
TERM_X0, TERM_Y0, TERM_X1, TERM_Y1 = 80, 352, 1200, 692
TERM_TX, TERM_TY = 114, 384
TERM_LH = 32


class TermScript:
    """Precomputes a timeline of terminal events: (start, kind, text, dur)."""

    def __init__(self, lines):
        self.events = []
        t = 0.55  # beat before the first keystroke
        for kind, text in lines:
            if kind == "cmd":
                dur = len(text) / TYPE_CPS
                self.events.append((t, kind, text, dur))
                t += dur + 0.5
            else:
                self.events.append((t, kind, text, OUT_SLOT))
                t += OUT_SLOT
        self.total = t


TERM_COLORS = {
    "out": TERM_DIM,
    "err": TERM_ERR,
    "ok": TERM_GREEN,
    "warn": TERM_GOLD,
}


def draw_terminal(img, script, t):
    d = ImageDraw.Draw(img)
    draw_alpha(img, lambda c: c.rounded_rectangle(
        [TERM_X0, TERM_Y0, TERM_X1, TERM_Y1], 20, fill=TERM_BG + (255,)))
    mf = font(MONO_R, 23)
    y = TERM_TY
    for start, kind, text, dur in script.events:
        if t < start or y > TERM_Y1 - 20:
            continue
        if kind == "cmd":
            nchars = min(len(text), int((t - start) * TYPE_CPS))
            # prompt
            d.text((TERM_TX, y), "$", font=mf, fill=TERM_GOLD)
            px = TERM_TX + d.textlength("$ ", font=mf)
            if nchars > 0:
                d.text((px, y), text[:nchars], font=mf, fill=TERM_CREAM)
            # blinking block cursor while typing
            if nchars < len(text) and (t * 2.2) % 1 < 0.62:
                cx = px + d.textlength(text[:nchars], font=mf)
                d.rectangle([cx + 2, y + 4, cx + 14, y + 26], fill=TERM_GOLD)
        else:
            a = clamp01((t - start) / 0.12)
            if a > 0:
                draw_alpha(img, lambda c, yy=y, tt=text, kk=kind, aa=a:
                           c.text((TERM_TX, yy), tt, font=mf,
                                  fill=TERM_COLORS[kk] + (int(255 * aa),)))
        y += TERM_LH

# ------------------------------------------------------------------ motifs ---
def motif_chat(img, box, prog):
    x0, y0, x1, y1 = box
    draw_alpha(img, lambda c: (
        c.rounded_rectangle([x0, y0, x0 + 200, y0 + 110], 26, fill=ACCENT_SOFT),
        c.rounded_rectangle([x1 - 200, y0 + 150, x1, y0 + 260], 26, fill=ACCENT + (255,)),
        c.polygon([(x0 + 40, y0 + 108), (x0 + 20, y0 + 150), (x0 + 70, y0 + 108)], fill=ACCENT_SOFT),
        c.polygon([(x1 - 40, y0 + 258), (x1 - 20, y0 + 300), (x1 - 70, y0 + 258)], fill=ACCENT),
    ))
    for i in range(3):
        dx = x1 - 130 + i * 34
        dy = y0 + 205
        r = 11 + 3 * math.sin(prog * 6 + i * 1.2)
        draw_alpha(img, lambda c, dx=dx, dy=dy, r=r: c.ellipse([dx - r, dy - r, dx + r, dy + r], fill=WHITE))


def motif_browser(img, box, prog):
    x0, y0, x1, y1 = box
    draw_alpha(img, lambda c: (
        c.rounded_rectangle([x0, y0, x1, y1], 24, fill=WHITE, outline=LINE, width=3),
        c.rounded_rectangle([x0, y0, x1, y0 + 64], 24, fill=CREAM_DEEP),
        c.rectangle([x0, y0 + 40, x1, y0 + 64], fill=CREAM_DEEP),
    ))
    for i, col in enumerate((ACCENT, GOLD, (120, 160, 120))):
        dx = x0 + 34 + i * 30
        draw_alpha(img, lambda c, dx=dx, col=col: c.ellipse([dx, y0 + 22, dx + 20, y0 + 42], fill=col))
    widths = [0.82, 0.66, 0.74, 0.5]
    for i, wf in enumerate(widths):
        yy = y0 + 110 + i * 44
        ww = (x1 - x0 - 90) * wf * clamp01(prog * 2 - i * 0.15)
        if ww >= 20:
            col = ACCENT_SOFT if i == 0 else LINE
            draw_alpha(img, lambda c, yy=yy, ww=ww, col=col: c.rounded_rectangle([x0 + 45, yy, x0 + 45 + ww, yy + 18], 9, fill=col))


def motif_plane(img, box, prog):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for i in range(5):
        tx = cx - 190 + i * 44
        ty = cy + 60 - i * 26
        a = clamp01(prog * 2 - i * 0.18)
        if a > 0:
            draw_alpha(img, lambda c, tx=tx, ty=ty, a=a: c.ellipse([tx - 7, ty - 7, tx + 7, ty + 7], fill=ACCENT + (int(200 * a),)))
    px, py = cx + 20 * ease_out_cubic(prog), cy - 10 * ease_out_cubic(prog)
    sail = [(px + 85, py - 55), (px - 95, py + 45), (px - 45, py - 5)]
    fold = [(px + 85, py - 55), (px - 45, py - 5), (px - 25, py - 38)]
    draw_alpha(img, lambda c: c.polygon(sail, fill=ACCENT))
    draw_alpha(img, lambda c: c.polygon(fold, fill=ACCENT_DEEP))


def motif_box(img, box, prog):
    """The shoebox: photo cards rising out of an open box."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    # photo cards float up out of the box
    rise = 120 * ease_out_cubic(clamp01(prog * 1.5))
    for i, dx in enumerate((-135, 0, 135)):
        cw, chh = 118, 148
        bx0, bx1 = cx + dx - cw / 2, cx + dx + cw / 2
        by1 = y0 + 300 - rise - i * 8
        by0 = by1 - chh
        a = clamp01(prog * 2 - i * 0.2)
        if a > 0:
            draw_alpha(img, lambda c, bx0=bx0, by0=by0, bx1=bx1, by1=by1, a=a: (
                c.rounded_rectangle([bx0, by0, bx1, by1], 10, fill=WHITE + (int(255 * a),)),
                c.rounded_rectangle([bx0 + 12, by0 + 12, bx1 - 12, by0 + 74], 6, fill=ACCENT_SOFT + (int(255 * a),)),
                c.rounded_rectangle([bx0 + 12, by0 + 88, bx1 - 12, by0 + 100], 5, fill=LINE + (int(255 * a),)),
                c.rounded_rectangle([bx0 + 12, by0 + 108, bx1 - 40, by0 + 120], 5, fill=LINE + (int(255 * a),)),
            ))
    # box body
    draw_alpha(img, lambda c: (
        c.rounded_rectangle([x0 + 60, y0 + 240, x1 - 60, y1 - 24], 18, fill=CREAM_DEEP),
        c.rounded_rectangle([x0 + 60, y0 + 240, x1 - 60, y1 - 24], 18, outline=LINE, width=3),
        # dark opening at the top
        c.rounded_rectangle([x0 + 84, y0 + 240, x1 - 84, y0 + 282], 12, fill=(110, 95, 82)),
        # side flaps
        c.polygon([(x0 + 60, y0 + 244), (x0 + 18, y0 + 190), (x0 + 84, y0 + 244)], fill=CREAM_DEEP, outline=LINE),
        c.polygon([(x1 - 60, y0 + 244), (x1 - 18, y0 + 190), (x1 - 84, y0 + 244)], fill=CREAM_DEEP, outline=LINE),
    ))
    # little tag on the front
    f = font(SANS_B, 30)
    tmp = ImageDraw.Draw(img)
    tw = tmp.textlength("brand", font=f)
    a = clamp01(prog * 2 - 0.5)
    if a > 0:
        draw_alpha(img, lambda c: c.rounded_rectangle(
            [cx - tw / 2 - 22, y0 + 330, cx + tw / 2 + 22, y0 + 384], 14, fill=ACCENT + (int(255 * a),)))
        text_fade(img, (cx - tw / 2, y0 + 338), "brand", f, WHITE, a)


MOTIFS = {
    "chat": motif_chat,
    "browser": motif_browser,
    "plane": motif_plane,
    "box": motif_box,
}


# ------------------------------------------------------------------ frames ---
KICKER_F = lambda: font(SANS_B, 30)  # noqa: E731
HEAD_F = lambda: font(SERIF_B, 78)  # noqa: E731
SUB_F = lambda: font(SANS_R, 31)  # noqa: E731


def progress_bar(img, idx, local_t, dur):
    n = len(BEATS)
    d = ImageDraw.Draw(img)
    label = f"Step {idx + 1} of {n}"
    f = KICKER_F()
    d.text((80, 52), label, font=f, fill=ACCENT)
    total_w, gap, seg_h, y = 1120, 18, 10, 100
    seg_w = (total_w - gap * (n - 1)) / n
    for i in range(n):
        x0 = 80 + i * (seg_w + gap)
        x1 = x0 + seg_w
        d.rounded_rectangle([x0, y, x1, y + seg_h], 5, fill=LINE)
        if i < idx:
            d.rounded_rectangle([x0, y, x1, y + seg_h], 5, fill=ACCENT)
        elif i == idx:
            fill_w = seg_w * clamp01(local_t / dur)
            if fill_w >= 2:
                d.rectangle([x0, y, x0 + fill_w, y + seg_h], fill=ACCENT)


def slide_frame(beat_idx, t):
    kind, dur, kicker, headline, sub, motif_name = BEATS[beat_idx]
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)

    progress_bar(img, beat_idx, t, dur)

    tx, ty = 80, 175
    kf = KICKER_F()
    kicker_letterspaced(img, d, kicker, tx, ty, kf, ACCENT, clamp01(t / 0.4))

    hy = ty + 62
    hf = HEAD_F()
    lines = wrap(d, headline, hf, 640)
    y = hy
    for li, line in enumerate(lines):
        words = line.split()
        x = tx
        for wi, w_ in enumerate(words):
            start = 0.25 + (li * 4 + wi) * 0.09
            p = ease_out_cubic((t - start) / 0.55)
            if p > 0:
                text_fade(img, (x, y + 44 * (1 - p)), w_ + " ", hf, INK, p)
            x += d.textlength(w_ + " ", font=hf)
        y += 92

    sf = SUB_F()
    sub_lines = wrap(d, sub, sf, 640)
    sy = y + 18
    for j, line in enumerate(sub_lines):
        p = clamp01((t - 0.85 - j * 0.12) / 0.6)
        if p > 0:
            text_fade(img, (tx, sy + 26 * (1 - ease_out_cubic(p))), line, sf, INK_SOFT, p)
        sy += 46

    mp = ease_out_cubic(clamp01((t - 0.5) / 0.6))
    if mp > 0:
        mx = 790 + 70 * (1 - mp)
        card = [mx, 160, 1210, 610]
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ldraw = ImageDraw.Draw(layer)
        ldraw.rounded_rectangle(card, 28, fill=CARD + (255,), outline=LINE + (255,), width=3)
        inner = [mx + 55, 215, 1155, 555]
        MOTIFS[motif_name](layer, inner, mp)
        a = layer.split()[3].point(lambda v: int(v * mp))
        layer.putalpha(a)
        img.alpha_composite(layer)

    edge = min(clamp01(t / FADE), clamp01((dur - t) / FADE))
    if edge < 1:
        veil = Image.new("RGBA", (W, H), CREAM + (int(255 * (1 - edge)),))
        img.alpha_composite(veil)
    return img.convert("RGB")


def term_frame(beat_idx, t, script):
    kind, dur, kicker, headline, sub, _lines = BEATS[beat_idx]
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)

    progress_bar(img, beat_idx, t, dur)

    kf = KICKER_F()
    kicker_letterspaced(img, d, kicker, 80, 150, kf, ACCENT, clamp01(t / 0.4))

    hf = font(SERIF_B, 54)
    p = ease_out_cubic(clamp01((t - 0.25) / 0.55))
    if p > 0:
        text_fade(img, (80, 196 + 40 * (1 - p)), headline, hf, INK, p)

    sf = font(SANS_R, 26)
    sub_lines = wrap(d, sub, sf, 1120)
    sy = 268
    for j, line in enumerate(sub_lines):
        q = clamp01((t - 0.7 - j * 0.12) / 0.6)
        if q > 0:
            text_fade(img, (80, sy + 22 * (1 - ease_out_cubic(q))), line, sf, INK_SOFT, q)
        sy += 38

    draw_terminal(img, script, t)

    edge = min(clamp01(t / FADE), clamp01((dur - t) / FADE))
    if edge < 1:
        veil = Image.new("RGBA", (W, H), CREAM + (int(255 * (1 - edge)),))
        img.alpha_composite(veil)
    return img.convert("RGB")


def title_frame(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    cx = W / 2
    p0 = clamp01(t / 0.4)
    kf = KICKER_F()
    tw = sum(d.textlength(ch, font=kf) + 6 for ch in TITLE_KICKER)
    kicker_letterspaced(img, d, TITLE_KICKER, cx - tw / 2, 218, kf, ACCENT, p0)
    p1 = ease_out_cubic(clamp01((t - 0.25) / 0.6))
    if p1 > 0:
        hf = font(SERIF_B, 88)
        tw = d.textlength(TITLE_HEAD, font=hf)
        text_fade(img, (cx - tw / 2, 292 + 44 * (1 - p1)), TITLE_HEAD, hf, INK, p1)
    p2 = clamp01((t - 0.85) / 0.6)
    if p2 > 0:
        rw = 120 * ease_out_cubic(p2)
        d.rounded_rectangle([cx - rw / 2, 448, cx + rw / 2, 454], 3, fill=GOLD)
        sf = font(SANS_R, 33)
        sub_lines = wrap(d, TITLE_SUB, sf, 900)
        sy = 486
        for line in sub_lines:
            lw = d.textlength(line, font=sf)
            text_fade(img, (cx - lw / 2, sy), line, sf, INK_SOFT, p2)
            sy += 50
    edge = min(clamp01(t / FADE), clamp01((TITLE_LEN - t) / FADE))
    if edge < 1:
        veil = Image.new("RGBA", (W, H), CREAM + (int(255 * (1 - edge)),))
        img.alpha_composite(veil)
    return img.convert("RGB")


def close_frame(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    cx = W / 2
    p1 = ease_out_cubic(clamp01((t - 0.2) / 0.6))
    if p1 > 0:
        hf = font(SERIF_B, 88)
        tw = d.textlength(END_HEAD, font=hf)
        text_fade(img, (cx - tw / 2, 250 + 40 * (1 - p1)), END_HEAD, hf, INK, p1)
    p2 = clamp01((t - 0.8) / 0.6)
    if p2 > 0:
        rw = 120 * ease_out_cubic(p2)
        d.rounded_rectangle([cx - rw / 2, 392, cx + rw / 2, 398], 3, fill=GOLD)
        sf = font(SANS_R, 33)
        sub_lines = wrap(d, END_SUB, sf, 900)
        sy = 430
        for line in sub_lines:
            lw = d.textlength(line, font=sf)
            text_fade(img, (cx - lw / 2, sy), line, sf, INK_SOFT, p2)
            sy += 50
    p3 = clamp01((t - 1.6) / 0.6)
    if p3 > 0:
        f = font(SANS_B, 24)
        tw = sum(d.textlength(ch, font=f) + 6 for ch in END_TAG)
        x = cx - tw / 2
        for ch in END_TAG:
            text_fade(img, (x, 560), ch, f, ACCENT_DEEP, p3)
            x += d.textlength(ch, font=f) + 6
    edge = min(clamp01(t / FADE), clamp01((END_LEN - t) / FADE))
    if edge < 1:
        veil = Image.new("RGBA", (W, H), CREAM + (int(255 * (1 - edge)),))
        img.alpha_composite(veil)
    return img.convert("RGB")


# ------------------------------------------------------------------- build ---
def scene_list():
    """Return list of (render_fn, duration) in order."""
    out = []
    out.append((lambda t: title_frame(t), TITLE_LEN))
    scripts = {}
    for idx, beat in enumerate(BEATS):
        kind, dur = beat[0], beat[1]
        if kind == "term":
            scripts[idx] = TermScript(beat[5])
            out.append((lambda t, i=idx: term_frame(i, t, scripts[i]), dur))
        else:
            out.append((lambda t, i=idx: slide_frame(i, t), dur))
    out.append((lambda t: close_frame(t), END_LEN))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mp4", default="template/docs/assets/end-to-end.mp4")
    ap.add_argument("--poster", default="template/docs/assets/end-to-end-poster.png")
    ap.add_argument("--crf", type=int, default=23)
    args = ap.parse_args()

    for p in (args.mp4, args.poster):
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)

    scenes = scene_list()
    total = sum(int(dur * FPS) for _, dur in scenes)
    print(f"rendering {total} frames ({total / FPS:.1f}s @ {FPS}fps) ...", flush=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", str(args.crf),
        "-preset", "medium", "-movflags", "+faststart",
        args.mp4,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    i = 0
    for render_fn, dur in scenes:
        n = int(dur * FPS)
        for f in range(n):
            proc.stdin.write(render_fn(f / FPS).tobytes())
            i += 1
            if i % 150 == 0:
                print(f"  {i}/{total}", flush=True)
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        sys.exit("ffmpeg failed")

    # poster: beat 1 slide, settled (title card is also fine; beat 1 shows the story)
    slide_frame(0, BEATS[0][1] * 0.62).save(args.poster)
    print("wrote", args.mp4)
    print("wrote", args.poster)


if __name__ == "__main__":
    main()
