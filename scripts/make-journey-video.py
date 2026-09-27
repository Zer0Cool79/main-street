#!/usr/bin/env python3
"""Build the owner-journey walkthrough video (programmatic kinetic typography).

Every on-screen word is drawn from exact strings below, so nothing can be
model-garbled. Visual language borrows from template/src/styles.css:
cream background, ink text, terracotta accent, gold highlight, serif display
headlines with a clean sans body.

House rules baked in: no em dashes anywhere on screen, no jargon
("preview copy" and "ship it" only).

Outputs (defaults):
  template/docs/assets/journey.mp4
  template/docs/assets/journey-poster.png

Regenerate with:  python3 scripts/make-journey-video.py
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
GOLD = (201, 154, 46)
LINE = (229, 217, 200)
CARD = (255, 253, 248)
WHITE = (255, 255, 255)

W, H = 1280, 720
FPS = 30

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_B = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
SANS_R = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")

for p in (SERIF_B, SERIF_R, SANS_B, SANS_R):
    if not os.path.exists(p):
        sys.exit(f"missing font: {p}")


def font(path, size):
    return ImageFont.truetype(path, size)


# ------------------------------------------------------------------ scenes ---
# (kicker, headline, sub, motif). No em dashes, no jargon.
SCENES = [
    (
        "Answer a few questions",
        "The setup wizard asks about your business in plain language. About ten minutes, no experience needed.",
        "chat",
    ),
    (
        "Preview your site",
        "See your real name, hours, and photos before anyone else does.",
        "browser",
    ),
    (
        "Your AI prepares a preview copy",
        "Every change lands on a private preview first. Nothing goes live until you approve it.",
        "layers",
    ),
    (
        "Open the preview link on your phone",
        "One permanent address, bookmarked. Check it over coffee.",
        "phone",
    ),
    (
        'Say "ship it"',
        "Two words. Your approved preview becomes the live site.",
        "plane",
    ),
    (
        "Your site is live",
        "At your own domain. Fast, findable, and yours.",
        "check",
    ),
]
SCENE_LEN = 5.0   # seconds per scene
END_LEN = 6.0     # end card
FADE = 0.35       # dip-to-cream at scene edges

END_HEAD = "The $12/year stack"
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


# ------------------------------------------------------------------ motifs ---
def motif_chat(img, box, prog):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    draw_alpha(img, lambda c: (
        c.rounded_rectangle([x0, y0, x0 + 200, y0 + 110], 26, fill=ACCENT_SOFT),
        c.rounded_rectangle([x1 - 200, y0 + 150, x1, y0 + 260], 26, fill=ACCENT + (255,)),
        c.polygon([(x0 + 40, y0 + 108), (x0 + 20, y0 + 150), (x0 + 70, y0 + 108)], fill=ACCENT_SOFT),
        c.polygon([(x1 - 40, y0 + 258), (x1 - 20, y0 + 300), (x1 - 70, y0 + 258)], fill=ACCENT),
    ))
    # three dots typing in the accent bubble
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
    # body lines, staggered widths
    widths = [0.82, 0.66, 0.74, 0.5]
    for i, wf in enumerate(widths):
        yy = y0 + 110 + i * 44
        ww = (x1 - x0 - 90) * wf * clamp01(prog * 2 - i * 0.15)
        if ww >= 20:
            col = ACCENT_SOFT if i == 0 else LINE
            draw_alpha(img, lambda c, yy=yy, ww=ww, col=col: c.rounded_rectangle([x0 + 45, yy, x0 + 45 + ww, yy + 18], 9, fill=col))


def motif_layers(img, box, prog):
    x0, y0, x1, y1 = box
    off = 26 * ease_out_cubic(prog)
    draw_alpha(img, lambda c: (
        c.rounded_rectangle([x0 + 40 + off, y0 + 60 + off, x1 - 40 + off, y1 - 60 + off], 24, fill=CREAM_DEEP, outline=LINE, width=3),
        c.rounded_rectangle([x0 + 40 - off, y0 + 60 - off, x1 - 40 - off, y1 - 60 - off], 24, fill=WHITE, outline=ACCENT, width=4),
    ))
    f = font(SANS_B, 38)
    tmp = ImageDraw.Draw(img)
    # center on the white (top) card, which sits `off` up-left of the box center
    ccx = (x0 + x1) / 2 - off
    ccy = (y0 + y1) / 2 - off
    tw = tmp.textlength("preview", font=f)
    text_fade(img, (ccx - tw / 2, ccy - 82), "preview", f, INK_SOFT, clamp01(prog * 1.6 - 0.4))


def motif_phone(img, box, prog):
    x0, y0, x1, y1 = box
    w = x1 - x0
    px0, px1 = x0 + w * 0.30, x1 - w * 0.30
    draw_alpha(img, lambda c: (
        c.rounded_rectangle([px0, y0 + 10, px1, y1 - 10], 44, fill=INK),
        c.rounded_rectangle([px0 + 12, y0 + 60, px1 - 12, y1 - 60], 10, fill=CREAM),
        c.rounded_rectangle([px0 + 12, y0 + 60, px1 - 12, y0 + 150], 10, fill=ACCENT),
        c.rectangle([px0 + 12, y0 + 130, px1 - 12, y0 + 150], fill=ACCENT),
        c.ellipse([(px0 + px1) / 2 - 14, y1 - 46, (px0 + px1) / 2 + 14, y1 - 18], outline=LINE, width=4),
    ))
    # link bar sliding in on the screen
    yy = y0 + 200
    for i, wf in enumerate((0.7, 0.5)):
        ww = (px1 - px0 - 56) * wf * clamp01(prog * 2 - i * 0.2)
        if ww >= 20:
            draw_alpha(img, lambda c, yy=yy + i * 44, ww=ww: c.rounded_rectangle([px0 + 28, yy, px0 + 28 + ww, yy + 18], 9, fill=LINE))


def motif_plane(img, box, prog):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = 1.0
    # dashed trail
    for i in range(5):
        tx = cx - 190 + i * 44
        ty = cy + 60 - i * 26
        a = clamp01(prog * 2 - i * 0.18)
        if a > 0:
            draw_alpha(img, lambda c, tx=tx, ty=ty, a=a: c.ellipse([tx - 7, ty - 7, tx + 7, ty + 7], fill=ACCENT + (int(200 * a),)))
    px, py = cx + 20 * ease_out_cubic(prog), cy - 10 * ease_out_cubic(prog)
    # paper plane pointing up-right: main sail + folded underside
    sail = [(px + 85, py - 55), (px - 95, py + 45), (px - 45, py - 5)]
    fold = [(px + 85, py - 55), (px - 45, py - 5), (px - 25, py - 38)]
    draw_alpha(img, lambda c: c.polygon(sail, fill=ACCENT))
    draw_alpha(img, lambda c: c.polygon(fold, fill=ACCENT_DEEP))


def motif_check(img, box, prog):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = 110 * ease_out_cubic(clamp01(prog * 1.4))
    if r > 2:
        draw_alpha(img, lambda c: c.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD))
    a = clamp01(prog * 2 - 0.6)
    if a > 0:
        w_ = 26
        draw_alpha(img, lambda c: (
            c.line([cx - 52, cy + 2, cx - 12, cy + 44], fill=WHITE, width=w_, joint="curve"),
            c.line([cx - 12, cy + 44, cx + 58, cy - 44], fill=WHITE, width=w_, joint="curve"),
        ))


MOTIFS = {
    "chat": motif_chat,
    "browser": motif_browser,
    "layers": motif_layers,
    "phone": motif_phone,
    "plane": motif_plane,
    "check": motif_check,
}
ACCENT_SOFT = (240, 221, 208)


# ------------------------------------------------------------------ frames ---
KICKER_F = lambda: font(SANS_B, 30)  # noqa: E731
HEAD_F = lambda: font(SERIF_B, 78)  # noqa: E731
SUB_F = lambda: font(SANS_R, 31)  # noqa: E731
SMALL_F = lambda: font(SANS_B, 24)  # noqa: E731


def progress_bar(img, idx, local_t):
    """Top progress indicator: 'Step N of 6' + six segments."""
    n = len(SCENES)
    d = ImageDraw.Draw(img)
    label = f"Step {idx + 1} of {n}"
    f = KICKER_F()
    d.text((80, 52), label, font=f, fill=ACCENT)
    # segments
    total_w, gap, seg_h, y = 1120, 18, 10, 100
    seg_w = (total_w - gap * (n - 1)) / n
    for i in range(n):
        x0 = 80 + i * (seg_w + gap)
        x1 = x0 + seg_w
        d.rounded_rectangle([x0, y, x1, y + seg_h], 5, fill=LINE)
        if i < idx:
            d.rounded_rectangle([x0, y, x1, y + seg_h], 5, fill=ACCENT)
        elif i == idx:
            fill_w = seg_w * clamp01(local_t / SCENE_LEN)
            if fill_w >= 2:
                d.rectangle([x0, y, x0 + fill_w, y + seg_h], fill=ACCENT)


def scene_frame(idx, t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    headline, sub, motif_name = SCENES[idx]

    progress_bar(img, idx, t)

    # ---- text block (left) ----
    tx, ty = 80, 175
    kicker = f"STEP {idx + 1} OF {len(SCENES)}"
    kf = KICKER_F()
    # letter-spaced kicker
    kx = tx
    ka = clamp01(t / 0.4)
    for ch in kicker:
        text_fade(img, (kx, ty), ch, kf, ACCENT, ka)
        kx += d.textlength(ch, font=kf) + 6

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

    # ---- motif card (right) ----
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

    # dip to cream at edges
    edge = min(clamp01(t / FADE), clamp01((SCENE_LEN - t) / FADE))
    if edge < 1:
        veil = Image.new("RGBA", (W, H), CREAM + (int(255 * (1 - edge)),))
        img.alpha_composite(veil)
    return img.convert("RGB")


def end_frame(t):
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
        # gold rule
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
        f = SMALL_F()
        tw = 0
        for ch in END_TAG:
            tw += d.textlength(ch, font=f) + 6
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
def iter_frames():
    for idx in range(len(SCENES)):
        n = int(SCENE_LEN * FPS)
        for f in range(n):
            yield scene_frame(idx, f / FPS)
    n = int(END_LEN * FPS)
    for f in range(n):
        yield end_frame(f / FPS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mp4", default="template/docs/assets/journey.mp4")
    ap.add_argument("--poster", default="template/docs/assets/journey-poster.png")
    ap.add_argument("--crf", type=int, default=23)
    args = ap.parse_args()

    for p in (args.mp4, args.poster):
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)

    total = int((SCENE_LEN * len(SCENES) + END_LEN) * FPS)
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
    for i, frame in enumerate(iter_frames()):
        proc.stdin.write(frame.tobytes())
        if i % 150 == 0:
            print(f"  {i}/{total}", flush=True)
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        sys.exit("ffmpeg failed")

    end_frame(END_LEN / 2).save(args.poster)
    print("wrote", args.mp4)
    print("wrote", args.poster)


if __name__ == "__main__":
    main()
