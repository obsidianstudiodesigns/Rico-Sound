# Rico's Sound

Online shop for Rico's Sound (Rico's Sound & ML Customs), a car audio, accessories and customs shop at 48 Operman Street, Witbank (Emalahleni): subwoofers, speakers, amps and mono blocks, radios, lights, mags, tyres, decals, gauges, mufflers, 4x4 accessories, body kits, air suspension and installs.

Live: https://obsidianstudiodesigns.github.io/Rico-Sound/

## What's on the site

- `index.html`: hero (the client's landing wallpaper, recoloured to brand red), brand marquee, "On special now" (Rico's own flyers as a swipeable rail), the shop with category filters, search and sort, installs and customs, how ordering works, and the visit section with the real shop front
- Cart and checkout: the cart is kept in the visitor's browser (`localStorage`). Checkout writes the order, the vehicle and the chosen fulfilment (collect, fit it for me, courier) into a WhatsApp message to 082 638 0403. Products can have options (model, size, stud pattern) and "Quote" items with no price. There is no backend and no online payment.
- `orders.html`, `privacy.html` (POPIA), `terms.html` (ECTA s43 disclosure, fitment, cooling-off, CPA returns), `404.html`
- SEO and sharing: canonical URLs, Open Graph and Twitter tags with `og-image.jpg` (1200 x 630) for WhatsApp previews, AutoPartsStore JSON-LD, `sitemap.xml`, `robots.txt`, favicon set and web manifest
- Lighthouse (mobile): Accessibility 100, Best Practices 100, SEO 100

## Editing products

All products live in `assets/js/products.js`: name, category, price (or `null` for a quote), unit, image, description, optional `options`, and `flyer` / `special` for flyer specials. Add a square image to `assets/img/products/` (720 x 720 webp) and a new entry to `PRODUCTS`. New flyers go in `assets/img/flyers/` at 1000 px high; add their width to `FLYER_W` in `assets/js/main.js`.

## Content sources

- Logo: lifted off the shop sign in the storefront photo (`tools/extract-logo.py`), with SOUND tinted brand red. Favicon: slanted R badge like the one on the "Feel every beat" flyer.
- Real products and prices from Rico's flyers: Pride TS-1820HD 18" sub (R1 150), Audiobahn AS96V 6x9 (R650 a set), Nakamichi 9" player (R3 500), Targa / Bass Station amps (R1 500 each), Land Cruiser mud flaps (R3 500 a set), TTX LC70 body kit (R59 999 incl. VAT, special until end October 2026), plus air suspension, TTX floor mats and the nudge bar with spotlights (no price on the flyers, so they are "Quote" items).
- Address, second number and Instagram from the MLcustomsRicossound Facebook page.
- Product photos are generated photoreal studio shots (Figma AI) in one consistent style. The LC70 card and the installs photos are cropped from the client's flyers; the air suspension photo is the client's own workshop job.
- **Sample products** (marked SAMPLE in `products.js`): 12" sub in ported box, component speakers, mono block, single-DIN radio, wiring kit, capacitor, gauges, LED spotlights, light bar, LED bulbs, 17" mags, all-terrain tyre, sports muffler.

## To confirm with Rico's Sound before promoting the site

- **Sample prices and products.** Every product marked SAMPLE has an invented price. Replace with real stock and prices, or remove.
- Trading hours (shown as Mon to Fri 08:00 to 17:00, Sat 08:00 to 13:00), marked `TO CONFIRM` in the HTML.
- Which number should receive WhatsApp orders (set to 082 638 0403, the number on most flyers; 064 908 5759 is listed for customs and installs).
- Payment methods, deposits for body kits, courier areas and fees.
- Legal status and VAT number for the ECTA disclosure in `terms.html`.
- Street name spelling ("Operman Street" as listed on Facebook).
- No reviews or testimonials are on the site. Add real ones if the client supplies them.

## Tools

- `tools/extract-logo.py`: lifts the logo off the storefront sign into `research/logo-alpha.png`
- `tools/make-assets.py`: builds the logo, favicons, recoloured hero, product, flyer and work photos and the brush stroke from the client's files (local only, not committed) and `research/`
- `tools/make-pages.py`: writes the legal pages and 404 from one template
- `tools/og.html` + `tools/make-og.sh`: renders `og-image.jpg` with headless Chrome

## Local preview

```bash
python -m http.server 5193
```

## Deploying

GitHub Pages serves the `main` branch root. Commit and push to `main`.

Website designed by [Obsidian Studio Designs](https://obsidianstudiodesigns.co.za/).
