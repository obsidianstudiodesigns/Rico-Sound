/*
  Rico's Sound product list. Edit this file to add, remove or re-price products.

  id       unique, lowercase, no spaces (used in the cart)
  name     shown on the card and in the WhatsApp order
  cat      one of the keys in CATEGORIES below
  price    in rand, whole number. Use null for "price on quote" items
  unit     optional, shown after the price ("set", "each", "fitted")
  img      square image in assets/img/products/ (720 x 720 webp)
  desc     one or two short sentences
  options  optional list the buyer picks from (model, size, fitment)
  flyer    optional, the client's flyer in assets/img/flyers/ for this product
  special  true = on a current Rico's Sound flyer special (shown in "On special now")

  REAL products and prices come from Rico's Sound flyers (special: true).
  Everything marked SAMPLE is a sample product with a sample price, added so the
  shop is not empty. Replace with real stock and prices before promoting the site.
*/
window.CATEGORIES = {
  subs:     { label: "Subwoofers",         icon: "speaker-hifi" },
  speakers: { label: "Speakers",           icon: "speaker-high" },
  amps:     { label: "Amps & mono blocks", icon: "lightning" },
  radios:   { label: "Radios & screens",   icon: "monitor" },
  install:  { label: "Gauges & install",   icon: "gauge" },
  lights:   { label: "Lights",             icon: "lightbulb-filament" },
  offroad:  { label: "4x4 & body kits",    icon: "jeep" },
  wheels:   { label: "Mags & tyres",       icon: "tire" },
  exhaust:  { label: "Mufflers",           icon: "wind" }
};

window.PRODUCTS = [
  /* ---- Real flyer specials ---- */
  {
    id: "pride-ts1820hd", name: "Pride TS-1820HD 18\" subwoofer", cat: "subs", price: 1150, unit: "each",
    img: "assets/img/products/sub-18.webp", flyer: "pride-sub", special: true,
    desc: "18-inch high-performance subwoofer for deep, powerful bass. Solid build that suits almost any setup."
  },
  {
    id: "audiobahn-as96v", name: "Audiobahn AS96V 6x9\" 3-way speakers", cat: "speakers", price: 650, unit: "set",
    img: "assets/img/products/spk-6x9.webp", flyer: "audiobahn-6x9", special: true,
    desc: "180 W RMS, 360 W max. Full-range 3-way sound with clear highs and deep bass. Sold as a pair."
  },
  {
    id: "nakamichi-9in", name: "Nakamichi 9\" Android multimedia player", cat: "radios", price: 3500, unit: "each",
    img: "assets/img/products/radio-9in.webp", flyer: "nakamichi", special: true,
    options: ["VW Golf 5", "VW Golf 6", "VW Polo (2010, selected models)"],
    desc: "Android OS, Bluetooth, WiFi, USB, radio, AUX and RCA. Fits the Golf 5 and 6 and some 2010 Polo models."
  },
  {
    id: "expo-amp-4ch", name: "Targa or Bass Station 4-channel amplifier", cat: "amps", price: 1500, unit: "each",
    img: "assets/img/products/amp-4ch.webp", flyer: "targa-bass-amps", special: true,
    options: ["Targa TO-H26500.4", "Bass Station 4.2000X"],
    desc: "Four-channel power amplifiers from Targa and Bass Station at a special expo price. Pick your model."
  },
  {
    id: "lc-mud-flaps", name: "Land Cruiser off-road mud flaps", cat: "offroad", price: 3500, unit: "set",
    img: "assets/img/products/mudflaps.webp", flyer: "mud-flaps", special: true,
    options: ["70 Series", "300 Series"],
    desc: "Heavy-duty ribbed rubber, reinforced metal end-plates with polished LAND CRUISER branding and a steel chain attachment."
  },
  {
    id: "ttx-lc70-kit", name: "TTX LC70 full body kit, fitted", cat: "offroad", price: 59999, unit: "incl. VAT",
    img: "assets/img/products/lc70-kit.webp", flyer: "lc70-kit", special: true,
    desc: "LC70 to LC79 conversion: front fenders, headlights, side indicators, grille, bonnet, mudflaps and fog lights. Includes installation and colour matching of fenders and bonnet. Special until the end of October 2026."
  },
  {
    id: "air-suspension", name: "Air suspension kit, supplied and fitted", cat: "offroad", price: null,
    img: "assets/img/products/airsus.webp", flyer: "air-suspension", special: true,
    desc: "Adjustable ride height, a smoother ride, better handling and more load capacity. Quoted per vehicle."
  },
  {
    id: "ttx-floor-mats", name: "TTX all-weather moulded floor mats", cat: "offroad", price: null,
    img: "assets/img/products/floormats.webp", flyer: "floor-mats", special: true,
    desc: "Precision-moulded 3D rubber with deep-dish edges that trap mud and water. Made for automatic bakkies only: tell us your model."
  },
  {
    id: "nudge-bar-spots", name: "Nudge bar with LED spotlights, fitted", cat: "offroad", price: null,
    img: "assets/img/products/nudgebar.webp", flyer: "ranger", special: true,
    desc: "Polished stainless nudge bar with two round LED spotlights, professionally installed on your Ranger or double cab."
  },

  /* ---- SAMPLE products and prices (replace with real stock) ---- */
  {
    id: "sub-12-ported", name: "12\" subwoofer in ported box", cat: "subs", price: 2499, unit: "each",
    img: "assets/img/products/sub-12-box.webp",
    desc: "Loaded, carpeted ported enclosure, ready to wire up. Big bass without giving up the whole boot."
  },
  {
    id: "component-65", name: "6.5\" 2-way component speakers", cat: "speakers", price: 899, unit: "set",
    img: "assets/img/products/spk-comp.webp",
    desc: "Separate woofers, tweeters and crossovers for clear vocals and a proper front stage."
  },
  {
    id: "mono-block", name: "Mono block amplifier", cat: "amps", price: 1899, unit: "each",
    img: "assets/img/products/amp-mono.webp",
    desc: "Class D mono block made to drive subwoofers. Small footprint, big output."
  },
  {
    id: "radio-1din", name: "Single-DIN Bluetooth radio", cat: "radios", price: 699, unit: "each",
    img: "assets/img/products/radio-1din.webp",
    desc: "Bluetooth calls and music, USB, AUX and FM in a standard single-DIN size."
  },
  {
    id: "amp-wiring-kit", name: "4-gauge amplifier wiring kit", cat: "install", price: 449, unit: "kit",
    img: "assets/img/products/wiring.webp",
    desc: "Power and ground cable, RCA lead, inline fuse holder and terminals for one amplifier."
  },
  {
    id: "capacitor", name: "Power capacitor with digital display", cat: "install", price: 899, unit: "each",
    img: "assets/img/products/capacitor.webp",
    desc: "Steadies your voltage on hard bass hits so the lights stop dimming."
  },
  {
    id: "gauges-52", name: "52 mm gauges with pod", cat: "install", price: 749, unit: "set",
    img: "assets/img/products/gauges.webp",
    options: ["Volt and boost", "Volt and oil pressure", "Boost and EGT"],
    desc: "Two red-lit 52 mm gauges and a triple pod. Pick your pair."
  },
  {
    id: "led-spots-7", name: "7\" round LED spotlights", cat: "lights", price: 1299, unit: "pair",
    img: "assets/img/products/spotlights.webp",
    desc: "Bright white driving lights in tough aluminium housings, with brackets."
  },
  {
    id: "led-light-bar", name: "Curved LED light bar", cat: "lights", price: 1499, unit: "each",
    img: "assets/img/products/lightbar.webp",
    desc: "Dual-row roof or bumper light bar with mounting brackets."
  },
  {
    id: "led-headlight-bulbs", name: "LED headlight bulbs", cat: "lights", price: 599, unit: "pair",
    img: "assets/img/products/led-bulbs.webp",
    options: ["H4", "H7", "H11", "Not sure, help me"],
    desc: "Whiter, brighter headlights with a fan-cooled LED conversion. Plug and play."
  },
  {
    id: "mags-17-black", name: "17\" gloss black mags", cat: "wheels", price: 8999, unit: "set of 4",
    img: "assets/img/products/mag-17.webp",
    options: ["4x100", "4x108", "5x112", "6x139.7 (bakkie)"],
    desc: "Multi-spoke gloss black wheels with a machined lip. Choose your stud pattern."
  },
  {
    id: "tyre-at", name: "All-terrain bakkie tyre", cat: "wheels", price: 2450, unit: "each",
    img: "assets/img/products/tyre-at.webp",
    options: ["245/70R16", "265/65R17", "265/60R18", "Other size"],
    desc: "Chunky all-terrain tread for gravel and town. Price per tyre."
  },
  {
    id: "sports-muffler", name: "Stainless sports muffler", cat: "exhaust", price: 1150, unit: "each",
    img: "assets/img/products/muffler.webp",
    desc: "Polished stainless silencer with a rolled tip. Ask us about fitment."
  }
];
