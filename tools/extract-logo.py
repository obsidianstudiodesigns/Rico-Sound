"""Lift the Rico's Sound logo off the shop sign in 'Store Front and logo.jpeg'.

Writes research/logo-alpha.png (white logo on transparent, 4x upscaled).
Run from the project root:  python tools/extract-logo.py
"""
import cv2
import numpy as np

src = cv2.imread("Store Front and logo.jpeg", cv2.IMREAD_GRAYSCALE)
crop = src[200:385, 690:1350].astype(np.float32)

# The sign is two panels; paint out the vertical seam between them.
prof = crop[150:185].mean(axis=0)
seam = int(np.argmax(prof[300:360] - cv2.GaussianBlur(prof.reshape(1, -1), (0, 0), 6).ravel()[300:360])) + 300
for x in range(seam - 3, seam + 4):
    crop[:, x] = np.nan
row_idx = np.arange(crop.shape[1])
for y in range(crop.shape[0]):
    row = crop[y]
    ok = ~np.isnan(row)
    crop[y] = np.interp(row_idx, row_idx[ok], row[ok])

S = 4
# Background: grey-level opening wider than any stroke, then blur, so only the lettering stands out.
bg = cv2.morphologyEx(crop, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45)))
bg = cv2.GaussianBlur(bg, (0, 0), 8)
diff = cv2.GaussianBlur(crop - bg, (0, 0), 0.6)
diff = cv2.resize(diff, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
diff = cv2.GaussianBlur(diff, (0, 0), 1.6)
lo, hi = 9.0, 38.0
a = np.clip((diff - lo) / (hi - lo), 0, 1)
a = a * a * (3 - 2 * a)
a[a < 0.04] = 0
alpha = (a * 255).astype(np.uint8)

# Seam remnants: a horizontal opening near the seam keeps the car lines and drops the vertical stroke.
x0, x1 = (seam - 14) * S, (seam + 14) * S
band = alpha[:, x0:x1]
opened = cv2.morphologyEx(band, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (31, 1)))
top = int(0.62 * alpha.shape[0])  # only above the lettering, so the apostrophe survives
alpha[:top, x0:x1] = opened[:top]

# Speckles and panel ribs: drop small connected blobs.
n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 40).astype(np.uint8), 8)
keep = np.zeros(n, bool)
keep[1:] = stats[1:, cv2.CC_STAT_AREA] > 2500
mask = keep[lab]
mask = cv2.dilate(mask.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
alpha[~mask] = 0

out = np.zeros((*alpha.shape, 4), np.uint8)
out[..., :3] = 255
out[..., 3] = alpha
ys, xs = np.nonzero(alpha > 20)
pad = 12
out = out[max(ys.min() - pad, 0):ys.max() + pad, max(xs.min() - pad, 0):xs.max() + pad]
cv2.imwrite("research/logo-alpha.png", out)
print("seam at", seam, "size", out.shape)
