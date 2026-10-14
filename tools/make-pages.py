"""Write the legal pages and the 404 page from one shared template.

Run from the project root:  python tools/make-pages.py
Edit the page bodies below, then re-run.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://obsidianstudiodesigns.github.io/Rico-Sound/"
UPDATED = "14 October 2026"

HEAD = """<!doctype html>
<html lang="en-ZA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title} | Rico's Sound</title>
  <meta name="description" content="{desc}">
  {canonical}
  <meta name="theme-color" content="#0e0d10">
  <meta name="color-scheme" content="dark">
  <link rel="icon" href="favicon.ico" sizes="48x48">
  <link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Rico's Sound">
  <meta property="og:title" content="{title} | Rico's Sound">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{base}og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;1,700;1,800&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css">
  <link rel="stylesheet" href="assets/css/style.css?v=1">
</head>
<body>
  <header class="site-header legal-header">
    <div class="wrap header-inner">
      <a class="brand" href="./" aria-label="Rico's Sound, home page"><img src="assets/img/logo.webp" srcset="assets/img/logo.webp 520w, assets/img/logo@2x.webp 1040w" sizes="190px" alt="" width="520" height="144"></a>
      <div class="header-actions"><a class="btn btn-red" href="./#shop"><span>Shop now</span></a></div>
    </div>
  </header>
"""

FOOT = """
  <footer class="site-footer">
    <div class="wrap footer-base" style="margin-top:0;border-top:0;padding-top:0">
      <p>© <span data-year>2026</span> Rico's Sound. All rights reserved.</p>
      <nav class="legal-nav" aria-label="Legal">
        <a href="orders.html"{cur_orders}>Orders, fitment and returns</a>
        <a href="privacy.html"{cur_privacy}>Privacy policy</a>
        <a href="terms.html"{cur_terms}>Terms of use</a>
      </nav>
      <p class="credit">Website designed by <a href="https://obsidianstudiodesigns.co.za/" target="_blank" rel="noopener">Obsidian Studio Designs</a></p>
    </div>
  </footer>
  <script>document.querySelectorAll('[data-year]').forEach(function (e) {{ e.textContent = new Date().getFullYear(); }});</script>
</body>
</html>
"""

CONTACT = """<dl>
      <dt>Business</dt><dd>Rico's Sound (Rico's Sound &amp; ML Customs)</dd>
      <dt>Address</dt><dd>48 Operman Street, Witbank (Emalahleni), Mpumalanga, South Africa</dd>
      <dt>Sales and WhatsApp</dt><dd><a href="tel:+27826380403">082 638 0403</a></dd>
      <dt>Customs and installs</dt><dd><a href="tel:+27649085759">064 908 5759</a></dd>
      <dt>Website</dt><dd><a href="./">obsidianstudiodesigns.github.io/Rico-Sound</a></dd>
    </dl>"""

PAGES = {
    "privacy.html": dict(
        title="Privacy policy",
        desc="How Rico's Sound in Witbank collects, uses and protects your personal information under the Protection of Personal Information Act (POPIA).",
        body=f"""
    <p class="lead">This policy explains how Rico's Sound ("we", "us") collects, uses and protects your personal information, in line with the Protection of Personal Information Act 4 of 2013 (POPIA).</p>

    <h2>Who we are</h2>
    {CONTACT}
    <p>The owner of Rico's Sound is our Information Officer under POPIA. Contact them on the details above about anything in this policy.</p>

    <h2>What we collect</h2>
    <p>We only collect the information you choose to give us when you order, book an install or ask a question, such as:</p>
    <ul>
      <li>your name and cellphone number (WhatsApp shares your number with us when you message us)</li>
      <li>your vehicle's make, model and year, so we can check fitment</li>
      <li>the products and quantities in your order</li>
      <li>your town or address, if you ask for courier delivery</li>
      <li>anything you add in a note</li>
    </ul>
    <p>When your vehicle is booked in for an install, we may also note its registration number and photograph the work for our records and, only with your permission, for our social media.</p>

    <h2>How the cart and checkout work</h2>
    <p>Your cart is saved in your own browser's storage on your device so it is still there when you come back. It is not a cookie and it is not sent to us. You can clear it with "Start a new order" or by clearing this site's data in your browser.</p>
    <p>The checkout does not send anything to us by itself. When you press "Send order on WhatsApp", WhatsApp opens with your order already written. Nothing reaches us unless you send that message yourself.</p>

    <h2>Why we use it</h2>
    <ul>
      <li>to confirm stock, fitment, your total and how you will get your order</li>
      <li>to book and carry out installations and to contact you about your vehicle</li>
      <li>to answer product questions and send quotes you ask for</li>
      <li>to handle returns and warranty claims and keep the records the law requires</li>
    </ul>
    <p>We do not sell, rent or trade your personal information. We only send you specials if you ask us to.</p>

    <h2>Who we share it with</h2>
    <p>We only share your information when we need to in order to fill your order, for example with a courier if you choose delivery or with a supplier for a warranty claim, or when the law requires it. WhatsApp and Facebook (Meta) carry our messages under their own privacy policies.</p>

    <h2>This website, cookies and third parties</h2>
    <p>This website does not use cookies, analytics or advertising trackers. To load, your browser fetches files from these providers, which may record your IP address and browser details in their standard server logs:</p>
    <ul>
      <li>GitHub Pages, which hosts this website</li>
      <li>Google Fonts, which supplies the typefaces</li>
      <li>jsDelivr, which supplies the icons</li>
    </ul>
    <p>Links to WhatsApp, Facebook, Instagram and Google Maps take you to services with their own privacy policies.</p>

    <h2>How long we keep it</h2>
    <p>We keep order messages only as long as we need them to fill your order and deal with any return or warranty claim. Records of sales are kept for as long as tax law requires, usually five years, and then deleted.</p>

    <h2>How we protect it</h2>
    <p>We take reasonable steps to keep your information safe, including keeping it on password-protected devices and accounts and only sharing it when needed.</p>

    <h2>Your rights</h2>
    <p>Under POPIA you may:</p>
    <ul>
      <li>ask what personal information we hold about you</li>
      <li>ask us to correct or delete it</li>
      <li>object to us using it</li>
      <li>withdraw consent you have given</li>
    </ul>
    <p>Contact us on the details above and we will respond within a reasonable time. If you are unhappy with how we handle your information, you may complain to the Information Regulator of South Africa at <a href="https://inforegulator.org.za" target="_blank" rel="noopener">inforegulator.org.za</a>.</p>

    <h2>Changes to this policy</h2>
    <p>We may update this policy from time to time. The date at the top shows when it last changed.</p>
"""),
    "terms.html": dict(
        title="Terms of use",
        desc="Terms for using the Rico's Sound website and ordering online: prices, quotes, orders, payment, installation, cancellations and returns.",
        body=f"""
    <p class="lead">These terms apply to this website and to orders placed through it. By using the website or sending us an order you agree to them.</p>

    <h2>About us</h2>
    <p>As required by section 43 of the Electronic Communications and Transactions Act 25 of 2002 (ECTA):</p>
    {CONTACT}
    <!-- TO CONFIRM with the client: legal status (sole proprietor or company and registration number), VAT number if registered -->

    <h2>Products and photos</h2>
    <p>We try to describe every product accurately. Some photos on this website show a typical example of the product rather than the exact item, so finishes, branding and packaging may differ. Ask us on WhatsApp if a detail matters to you.</p>

    <h2>Fitment</h2>
    <p>Many parts only fit certain vehicles. Please give us your vehicle's make, model and year with your order. We confirm fitment before you pay, and we are not responsible for parts bought for the wrong vehicle when the details you gave us were incorrect.</p>

    <h2>Prices and quotes</h2>
    <p>Prices are in South African rand. Specials run while stock lasts or until the date shown. Prices and stock shown on this website can change without notice and may contain errors. Items marked "Quote" are priced for your vehicle. The price that applies is the one Rico's Sound confirms to you on WhatsApp before you pay.</p>

    <h2>Placing an order</h2>
    <ul>
      <li>Sending your cart on WhatsApp is an order request. Your order is accepted only when Rico's Sound replies to confirm the items, fitment, the total and how you will get them.</li>
      <li>If something is out of stock, we will tell you and offer an alternative or remove it from your order.</li>
      <li>We may decline an order, for example if a price on the website was wrong.</li>
    </ul>

    <h2>Payment</h2>
    <!-- TO CONFIRM with the client: accepted payment methods (cash, card, EFT) and deposit rules for body kits and installs -->
    <p>Payment is made in store or by EFT once we confirm your order. Large orders, body kits and special orders may need a deposit before we order stock. We never ask for card details on WhatsApp.</p>

    <h2>Installations</h2>
    <p>Installation work is booked by appointment. We will tell you the fitment cost and the time the vehicle is needed before we start. Please remove valuables from your vehicle. Workmanship problems reported to us promptly will be checked and put right.</p>

    <h2>Cancelling an order (cooling-off)</h2>
    <p>If you order through this website and we courier the goods to you, you may cancel without reason and without penalty within 7 days after you receive the goods, as allowed by section 44 of ECTA. You only pay the direct cost of returning the goods. We refund what you paid within 30 days of the cancellation. This does not apply to goods you collect and inspect in store, to goods that have been installed, or to goods ordered or made to your own specification.</p>

    <h2>Returns, warranties and faulty goods</h2>
    <p>Under the Consumer Protection Act 68 of 2008 you may return goods that are faulty, unsafe or not what you ordered within six months of receiving them, and choose a repair, replacement or refund. Some products also carry a supplier warranty. Please keep your proof of purchase. Our full returns process is set out in <a href="orders.html">Orders, fitment and returns</a>.</p>

    <h2>Use of this website</h2>
    <p>The content, logo and design of this website belong to Rico's Sound and its designers. Brand names and logos shown on flyers belong to their owners. You may not copy or reuse our content without permission. We try to keep the information correct and up to date, but we do not guarantee that it is complete or free of errors.</p>
    <p>This website links to WhatsApp, Facebook, Instagram and Google Maps. We are not responsible for their content or how they work.</p>

    <h2>Your information</h2>
    <p>How we handle personal information is set out in our <a href="privacy.html">privacy policy</a>.</p>

    <h2>Law</h2>
    <p>These terms are governed by the laws of the Republic of South Africa. Nothing in them limits your rights under the Consumer Protection Act or ECTA.</p>
"""),
    "orders.html": dict(
        title="Orders, fitment and returns",
        desc="How ordering from Rico's Sound works: fill your cart, send it on WhatsApp, then collect in Witbank, book an install or ask for courier delivery. Plus our returns policy.",
        body="""
    <p class="lead">Ordering from Rico's Sound is simple: fill your cart on this website, send it to us on WhatsApp, and we confirm stock, fitment and your total before you pay.</p>

    <h2>How to order</h2>
    <ul>
      <li>Add products to your cart and open it with the cart button. Items marked "Quote" can go in too.</li>
      <li>Add your name and your vehicle's make, model and year.</li>
      <li>Choose to collect, to have it fitted, or courier delivery.</li>
      <li>Press "Send order on WhatsApp". WhatsApp opens with your order written out. Press send.</li>
      <li>We reply to confirm stock, fitment, your total and when it is ready.</li>
    </ul>
    <p>No WhatsApp? Call us on <a href="tel:+27826380403">082 638 0403</a>.</p>

    <h2>Stock</h2>
    <p>We carry far more than we can show online, from mono blocks to mufflers. If you don't see what you need, ask us on <a href="https://wa.me/27826380403" target="_blank" rel="noopener">WhatsApp</a>.</p>

    <h2>Collection</h2>
    <!-- TO CONFIRM with the client: trading hours -->
    <p>Collect your order from the shop at 48 Operman Street, Witbank once we have confirmed it is ready.</p>

    <h2>Fitment and installs</h2>
    <p>Choose "Fit it for me" in your cart and we will book your vehicle in. We confirm the fitment cost and how long we need the vehicle before we start. Body kits include installation and colour matching where the special says so.</p>

    <h2>Courier delivery</h2>
    <!-- TO CONFIRM with the client: courier, delivery areas and fees -->
    <p>Choose "Courier to me" and tell us your town. We will let you know the cost and timing before you pay.</p>

    <h2>Returns and exchanges</h2>
    <ul>
      <li><strong>Faulty or wrong items:</strong> let us know within six months and we will repair, replace or refund, as the Consumer Protection Act allows. Supplier warranties may also apply.</li>
      <li><strong>Couriered orders:</strong> you may cancel within 7 days of receiving the goods without giving a reason (ECTA cooling-off). You pay only the direct cost of sending them back.</li>
      <li><strong>Changed your mind:</strong> contact us. Unused items in their original, undamaged packaging can usually be exchanged.</li>
      <li>Products that have been installed, cut, wired or painted to fit your vehicle can only be returned if they are faulty.</li>
    </ul>
    <p>Please keep your proof of purchase (your WhatsApp order confirmation is fine) and contact us first on <a href="tel:+27826380403">082 638 0403</a>.</p>

    <h2>More</h2>
    <p>See our <a href="terms.html">terms of use</a> and <a href="privacy.html">privacy policy</a>.</p>
"""),
}

for name, page in PAGES.items():
    cur = {k: "" for k in ("cur_orders", "cur_privacy", "cur_terms")}
    cur["cur_" + name.split(".")[0]] = ' aria-current="page"'
    html = HEAD.format(title=page["title"], desc=page["desc"], base=BASE,
                       canonical=f'<link rel="canonical" href="{BASE}{name}">')
    html += f"""
  <main class="legal" id="main">
    <div class="wrap">
      <h1>{page["title"]}</h1>
      <p class="updated">Last updated: {UPDATED}</p>
{page["body"]}    </div>
  </main>
"""
    html += FOOT.format(**cur)
    (ROOT / name).write_text(html, encoding="utf-8")

# 404: GitHub Pages serves it from any path, so every link is absolute.
html = HEAD.format(title="Page not found", desc="This page could not be found. Visit the Rico's Sound shop.", base=BASE,
                   canonical='<meta name="robots" content="noindex">')
html = html.replace("<head>\n", f'<head>\n  <base href="{BASE}">\n', 1)
html += f"""
  <main class="notfound" id="main">
    <div>
      <h1>404</h1>
      <p>That page blew a fuse. The subs, amps and specials are all still in the shop.</p>
      <a class="btn btn-red" href="{BASE}#shop"><span>Shop now</span></a>
    </div>
  </main>
"""
html += FOOT.format(cur_orders="", cur_privacy="", cur_terms="")
(ROOT / "404.html").write_text(html, encoding="utf-8")
print("pages written")
