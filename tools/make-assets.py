"""Build every web image for the Rico's Sound site.

Inputs (local only, not committed): the client's flyers, storefront photo and
'landing page.png' in the project root, research/logo-alpha.png (from
tools/extract-logo.py) and research/gen/*.jpg (generated product photos).

Run from the project root:  python tools/make-assets.py
"""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
(IMG / "products").mkdir(parents=True, exist_ok=True)
(IMG / "flyers").mkdir(parents=True, exist_ok=True)
W = "WhatsApp Image 2026-10-14 at "

RED = (225, 25, 43)


def save(im, path, q=80):
    path = IMG / path
    im.save(path.with_suffix(".webp"), "WEBP", quality=q, method=6)
    return path


# ---------- Logo ----------
alpha = Image.open(ROOT / "research" / "logo-alpha.png").getchannel("A")
w, h = alpha.size
# "SOUND" sits in the lower right of the sign: tint it brand red, keep the car and script white.
tint = Image.new("L", (w, h), 0)
ImageDraw.Draw(tint).rectangle((int(w * 0.535), int(h * 0.57), w, h), fill=255)
tint = tint.filter(ImageFilter.GaussianBlur(2))
white = Image.new("RGBA", (w, h), (246, 244, 242, 0))
red = Image.new("RGBA", (w, h), RED + (0,))
logo = Image.composite(red, white, tint)
logo.putalpha(alpha)
for width, name in ((520, "logo"), (1040, "logo@2x")):
    lw = logo.resize((width, round(h * width / w)), Image.LANCZOS)
    lw.save(IMG / f"{name}.png", optimize=True)
    save(lw, f"{name}.png", 90)
print("logo", logo.size, "->", round(h * 520 / w), "high at 520")

# ---------- Favicons: a bold slanted "R" on a brand-red tile, like the R badge on the Feel Every Beat flyer ----------
from PIL import ImageFont

FONT = "C:/Windows/Fonts/impact.ttf"


def icon(size, radius=0.22):
    S = size * 4
    tile = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * radius), fill=255)
    tile.paste(Image.new("RGBA", (S, S), RED + (255,)), (0, 0), m)
    glyph = Image.new("L", (S, S), 0)
    f = ImageFont.truetype(FONT, int(S * 0.86))
    d = ImageDraw.Draw(glyph)
    bb = d.textbbox((0, 0), "R", font=f)
    d.text(((S - (bb[2] - bb[0])) / 2 - bb[0], (S - (bb[3] - bb[1])) / 2 - bb[1]), "R", font=f, fill=255)
    glyph = glyph.transform((S, S), Image.AFFINE, (1, 0.2, -S * 0.1, 0, 1, 0), Image.BICUBIC)
    white = Image.new("RGBA", (S, S), (250, 248, 246, 255))
    white.putalpha(Image.composite(glyph, Image.new("L", (S, S), 0), m))
    tile.alpha_composite(white)
    return tile.resize((size, size), Image.LANCZOS)


icon(512).save(ROOT / "icon-512.png", optimize=True)
icon(192).save(ROOT / "icon-192.png", optimize=True)
icon(180, radius=0).save(ROOT / "apple-touch-icon.png", optimize=True)
icon(32, radius=0.18).save(ROOT / "favicon-32.png", optimize=True)
icon(16, radius=0.15).save(ROOT / "favicon-16.png", optimize=True)
icon(256, radius=0.18).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# ---------- Hero wallpaper, recoloured from violet/blue to brand red ----------
src = cv2.imread(str(ROOT / "landing page.png"))
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
hh, ss, vv = cv2.split(hsv)
wgt = np.clip((ss - 30) / 80, 0, 1)
hh = np.mod((1 - wgt) * hh + wgt * 178.0, 180)
ss = np.clip(ss * 1.05, 0, 255)
red_bgr = cv2.cvtColor(cv2.merge([hh, ss, vv]).astype(np.uint8), cv2.COLOR_HSV2BGR)
red_bgr = np.clip(red_bgr.astype(np.float32) * 0.92, 0, 255).astype(np.uint8)
hero = Image.fromarray(cv2.cvtColor(red_bgr, cv2.COLOR_BGR2RGB))
save(hero, "hero.jpg", 78)
save(hero.resize((1100, round(hero.height * 1100 / hero.width)), Image.LANCZOS), "hero-md.jpg", 76)
# Phone crop: nearly square and at native resolution (no upscaling), wide enough to
# show the whole front speaker. On phones it sits in a band at the top of the hero.
hhgt = hero.height
save(hero.crop((40, 0, 1010, hhgt)), "hero-sm.jpg", 80)
print("hero", hero.size)

# ---------- Product photos ----------
for f in sorted((ROOT / "research" / "gen").glob("*.jpg")):
    im = Image.open(f).convert("RGB").resize((720, 720), Image.LANCZOS)
    save(im, f"products/{f.stem}.jpg", 80)
# The LC70 kit card uses the truck from the client's own flyer.
lc = Image.open(ROOT / (W + "11.26.24 (1).jpeg")).convert("RGB").crop((20, 500, 400, 880))
save(lc.resize((720, 720), Image.LANCZOS), "products/lc70-kit.jpg", 82)

# ---------- Flyers (the client's own specials), full flyer, fixed height ----------
flyers = {
    "pride-sub": (W + "11.26.24.jpeg", None),
    "audiobahn-6x9": (W + "11.26.25.jpeg", None),
    "nakamichi": (W + "11.26.22 (1).jpeg", None),
    "targa-bass-amps": (W + "11.26.25 (1).jpeg", None),
    "mud-flaps": (W + "11.26.23.jpeg", None),
    "lc70-kit": (W + "11.26.24 (1).jpeg", (0, 356, 738, 1246)),
    "floor-mats": (W + "11.26.24 (2).jpeg", None),
    "air-suspension": (W + "11.26.23 (1).jpeg", None),
    "ranger": (W + "11.26.22.jpeg", None),
    "feel-every-beat": (W + "11.27.30.jpeg", (0, 300, 738, 1300)),
}
for name, (f, box) in flyers.items():
    im = Image.open(ROOT / f).convert("RGB")
    if box:
        im = im.crop(box)
    H = 1000
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    save(im, f"flyers/{name}.jpg", 78)
    print("flyer", name, im.size)

# ---------- Photos for the installs and customs section ----------
shots = {
    "work-air-suspension": (W + "11.26.23 (1).jpeg", (35, 268, 1000, 600)),
    "work-lc70": (W + "11.26.24 (1).jpeg", (14, 514, 412, 868)),
    "work-ranger": (W + "11.26.22.jpeg", (44, 945, 1010, 1290)),
    "work-cruiser": (W + "11.26.23.jpeg", (40, 400, 740, 800)),
}
for name, (f, box) in shots.items():
    im = Image.open(ROOT / f).convert("RGB").crop(box)
    if im.width < 900:
        im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    save(im, f"{name}.jpg", 80)
    print("shot", name, im.size)

# ---------- Storefront ----------
store = Image.open(ROOT / "Store Front and logo.jpeg").convert("RGB")
save(store.resize((1400, round(store.height * 1400 / store.width)), Image.LANCZOS), "storefront.jpg", 78)
save(store.resize((760, round(store.height * 760 / store.width)), Image.LANCZOS), "storefront-sm.jpg", 76)

# ---------- Brush stroke (red, like the flyer headline swipes) ----------
rng = np.random.default_rng(7)
BW, BH = 1400, 300
m = np.zeros((BH, BW), np.float32)
yy, xx = np.mgrid[0:BH, 0:BW]
# slanted body with a tapering, ragged start and end
top = 46 + 22 * np.sin(xx / 260.0) - xx * 0.02
bot = BH - 40 + 12 * np.sin(xx / 190.0 + 1.3) - xx * 0.035
body = (yy > top) & (yy < bot)
m[body] = 1.0
# dry-brush streaks: horizontal gaps that run in from both ends
for _ in range(150):
    y = int(rng.uniform(20, BH - 20))
    th = int(rng.choice([1, 1, 2, 2, 3, 4]))
    from_left = rng.random() < 0.55
    length = int(rng.gamma(2.0, 140))
    if from_left:
        m[y:y + th, :length] = 0
    else:
        m[y:y + th, BW - length:] = 0
# ragged ends
ends = rng.normal(0, 1, BH).cumsum()
ends = (ends - ends.min()) / (np.ptp(ends) + 1e-6)
for y in range(BH):
    m[y, : int(20 + ends[y] * 110)] = 0
    m[y, BW - int(10 + (1 - ends[y]) * 90):] = 0
noise = cv2.GaussianBlur(rng.random((BH, BW)).astype(np.float32), (0, 0), 1.2)
m = m * (noise > 0.28)
m = cv2.GaussianBlur(m, (0, 0), 0.8)
rgba = np.zeros((BH, BW, 4), np.uint8)
rgba[..., 0], rgba[..., 1], rgba[..., 2] = RED
rgba[..., 3] = (np.clip(m, 0, 1) * 255).astype(np.uint8)
Image.fromarray(rgba, "RGBA").save(IMG / "brush.png", optimize=True)
Image.fromarray(rgba, "RGBA").save(IMG / "brush.webp", "WEBP", quality=85)
print("done")
