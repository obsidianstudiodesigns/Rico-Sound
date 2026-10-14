"""Build the white brand logos for the marquee in assets/img/brands/.

Sources (local only, in research/logos and the client's files):
- Brandfetch / brand websites: Kicker, Nakamichi, Hertz, Targa (transparent PNGs)
- Rico's own flyers: Audiobahn, Pride, TTX
- The storefront photo: T1 Audio (the sign beside the shop)

Every logo becomes a white silhouette on transparent, trimmed and scaled to 120 px high.
Run from the project root:  python tools/make-brand-logos.py
"""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "research" / "logos"
OUT = ROOT / "assets" / "img" / "brands"
OUT.mkdir(parents=True, exist_ok=True)
W = "WhatsApp Image 2026-10-14 at "
H = 120


def smooth(x, lo, hi):
    a = np.clip((x - lo) / (hi - lo), 0, 1)
    return a * a * (3 - 2 * a)


def clean(alpha, min_area):
    n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 0.25).astype(np.uint8), 8)
    keep = np.zeros(n, bool)
    keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= min_area
    mask = cv2.dilate(keep[lab].astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    return np.where(mask, alpha, 0)


def save(name, alpha, scale=1, red=None):
    """alpha: float 0..1 array. Upscale small sources before trimming for smoother edges.
    red: optional 0..1 array of pixels to paint brand red instead of white."""
    if scale != 1:
        alpha = cv2.resize(alpha, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        alpha = np.clip(cv2.GaussianBlur(alpha, (0, 0), scale * 0.35), 0, 1)
        alpha = smooth(alpha, 0.3, 0.7)
    a8 = (alpha * 255).astype(np.uint8)
    ys, xs = np.nonzero(a8 > 10)
    box = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    a8 = a8[box]
    rgb = np.full((*a8.shape, 3), 255, np.float32)
    if red is not None:
        r = red[box][..., None]
        rgb = rgb * (1 - r) + np.array([225, 25, 43], np.float32) * r
    img = Image.fromarray(np.dstack([rgb.astype(np.uint8), a8]), "RGBA")
    w = round(img.width * H / img.height)
    img = img.resize((w, H), Image.LANCZOS)
    img.save(OUT / f"{name}.png", optimize=True)
    print(name, img.size)


def from_alpha(file):
    return np.asarray(Image.open(SRC / file).convert("RGBA"), np.float32)[..., 3] / 255


def crop(file, box):
    return np.asarray(Image.open(ROOT / file).convert("RGB").crop(box), np.float32)


# Transparent PNGs from the brands
save("kicker", from_alpha("kicker-site.png"), scale=4)
save("targa", from_alpha("targa-light.png"), scale=3)
save("hertz", from_alpha("hertz.png"))
save("nakamichi", from_alpha("nakamichi-usa.png"))

# Audiobahn: white wordmark with a red dot on a dark flyer background
rgb = crop(W + "11.26.25.jpeg", (60, 14, 1000, 166))
a = smooth(rgb.max(axis=2), 120, 190)
a[:39] = 0  # the red brush stroke above the wordmark
dot = smooth(rgb[..., 0] - rgb[..., 1:].max(axis=2), 60, 120)
save("audiobahn", clean(a, 30), red=dot)

# Pride: red italic wordmark
rgb = crop(W + "11.26.24.jpeg", (20, 1185, 360, 1252))
red = rgb[..., 0] - rgb[..., 1:].max(axis=2)
save("pride", clean(smooth(red, 50, 110), 30), scale=3)

# TTX: white letters with a blue outline (floor mats flyer)
rgb = crop(W + "11.26.24 (2).jpeg", (40, 1228, 176, 1274))
lum = rgb.mean(axis=2)
sat = rgb.max(axis=2) - rgb.min(axis=2)
save("ttx", clean(smooth(lum, 150, 205) * (sat < 70), 60), scale=4)

# T1 Audio: grey sign beside the shop, lifted off its panel like the Rico's logo
g = crop("Store Front and logo.jpeg", (226, 326, 476, 404)).mean(axis=2)
bg = cv2.GaussianBlur(cv2.morphologyEx(g, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))), (0, 0), 6)
save("t1-audio", clean(smooth(g - bg, 18, 45), 45), scale=4)
