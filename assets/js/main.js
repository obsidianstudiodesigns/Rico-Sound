(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var WHATSAPP = "27826380403";
  var PHONE_LABEL = "082 638 0403";
  var STORE_KEY = "ricos-sound-cart-v1";
  // Flyer image widths at 1000 px high (made by tools/make-assets.py)
  var FLYER_W = {
    "pride-sub": 667, "audiobahn-6x9": 667, "nakamichi": 1000, "targa-bass-amps": 504, "mud-flaps": 590,
    "lc70-kit": 829, "floor-mats": 652, "air-suspension": 1000, "ranger": 667, "feel-every-beat": 738
  };

  var CATS = window.CATEGORIES;
  var PRODUCTS = window.PRODUCTS;
  var byId = {};
  var catOrder = Object.keys(CATS);
  PRODUCTS.forEach(function (p, i) { p.order = i; byId[p.id] = p; });

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function rand(n) { return "R" + n.toLocaleString("en-ZA").replace(/,/g, " "); }
  function priceHTML(p) {
    if (p.price == null) return '<p class="price quote">Quote</p>';
    return '<p class="price">' + rand(p.price) + (p.unit ? '<small>' + esc(p.unit) + '</small>' : '') + '</p>';
  }
  function waLink(text) { return "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(text); }

  /* ---------- Cart state: { "id" or "id|option": qty } ---------- */
  function split(key) { var i = key.indexOf("|"); return i < 0 ? { id: key, opt: "" } : { id: key.slice(0, i), opt: key.slice(i + 1) }; }
  var cart = {};
  try {
    var saved = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
    Object.keys(saved).forEach(function (key) {
      var q = parseInt(saved[key], 10);
      if (byId[split(key).id] && q > 0) cart[key] = Math.min(q, 99);
    });
  } catch (e) { cart = {}; }

  function persist() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(cart)); } catch (e) { /* private mode: cart lasts for this visit */ }
  }
  function count() { return Object.keys(cart).reduce(function (n, k) { return n + cart[k]; }, 0); }
  function subtotal() {
    return Object.keys(cart).reduce(function (n, k) { var p = byId[split(k).id]; return n + (p.price || 0) * cart[k]; }, 0);
  }
  function hasQuote() { return Object.keys(cart).some(function (k) { return byId[split(k).id].price == null; }); }
  function qtyOf(id) { // all lines of a product
    return Object.keys(cart).reduce(function (n, k) { return split(k).id === id ? n + cart[k] : n; }, 0);
  }
  function firstKey(id) { return Object.keys(cart).filter(function (k) { return split(k).id === id; })[0]; }

  function setQty(key, qty, opts) {
    var id = split(key).id;
    var before = cart[key] || 0;
    qty = Math.max(0, Math.min(99, qty));
    if (qty === 0) delete cart[key]; else cart[key] = qty;
    persist();
    refreshControls(id);
    refreshCart();
    if (qty > before && !(opts && opts.quiet) && !sheet.open) {
      toast(byId[id].name);
      var badge = $("[data-cart-count]");
      badge.classList.remove("bump"); void badge.offsetWidth; badge.classList.add("bump");
    }
  }

  /* ---------- Add / stepper controls ----------
     Products with options open the quick view so the buyer picks one.
     Products with several cart lines (different options) show "Add" plus the count. */
  function controlsHTML(p) {
    var q = qtyOf(p.id);
    var lines = Object.keys(cart).filter(function (k) { return split(k).id === p.id; }).length;
    if (!q || p.options) {
      return '<button class="add-btn" type="button" ' + (p.options ? 'data-quick-open="' : 'data-add="') + p.id + '">' +
        '<span><i class="ph ph-plus" aria-hidden="true"></i> ' + (q ? "Add (" + q + ")" : "Add") + '<span class="sr-only"> ' + esc(p.name) + ' to cart</span></span></button>';
    }
    var key = lines === 1 ? firstKey(p.id) : p.id;
    return '<div class="stepper" role="group" aria-label="Quantity of ' + esc(p.name) + '">' +
      '<button type="button" data-dec="' + esc(key) + '" aria-label="One less"><i class="ph ph-' + (q === 1 ? "trash" : "minus") + '" aria-hidden="true"></i></button>' +
      '<span aria-live="polite">' + q + '</span>' +
      '<button type="button" data-inc="' + esc(key) + '" aria-label="One more"><i class="ph ph-plus" aria-hidden="true"></i></button></div>';
  }
  function lineControlsHTML(key) {
    var q = cart[key];
    return '<div class="stepper" role="group" aria-label="Quantity">' +
      '<button type="button" data-dec="' + esc(key) + '" aria-label="One less"><i class="ph ph-' + (q === 1 ? "trash" : "minus") + '" aria-hidden="true"></i></button>' +
      '<span aria-live="polite">' + q + '</span>' +
      '<button type="button" data-inc="' + esc(key) + '" aria-label="One more"><i class="ph ph-plus" aria-hidden="true"></i></button></div>';
  }

  function refreshControls(id) {
    var p = byId[id];
    $$('[data-controls="' + id + '"]').forEach(function (el) {
      var hadFocus = el.contains(document.activeElement);
      var focusInc = hadFocus && document.activeElement.hasAttribute("data-inc");
      el.innerHTML = controlsHTML(p);
      if (hadFocus) {
        var next = el.querySelector(focusInc ? "[data-inc]" : "[data-add], [data-dec], [data-quick-open]") || el.querySelector("button");
        if (next) next.focus();
      }
    });
  }

  /* ---------- Specials rail (Rico's own flyers) ---------- */
  var rail = $("[data-flyer-rail]");
  rail.innerHTML = PRODUCTS.filter(function (p) { return p.special && p.flyer; }).map(function (p) {
    var w = FLYER_W[p.flyer] || 700;
    return '<li class="flyer">' +
      '<button class="flyer-media" type="button" data-flyer="' + p.flyer + '" aria-label="View the flyer: ' + esc(p.name) + '">' +
      '<img src="assets/img/flyers/' + p.flyer + '.webp" width="' + w + '" height="1000" loading="lazy" alt="Rico\'s Sound flyer: ' + esc(p.name) + '"></button>' +
      '<div class="flyer-body"><div><h3>' + esc(p.name) + '</h3>' + priceHTML(p) + '</div>' +
      '<div data-controls="' + p.id + '">' + controlsHTML(p) + '</div></div></li>';
  }).join("");

  function railStep(dir) {
    var item = rail.querySelector(".flyer");
    var step = item ? item.getBoundingClientRect().width + 20 : 320;
    rail.scrollBy({ left: dir * step * 2, behavior: reduceMotion ? "auto" : "smooth" });
  }
  $$("[data-rail]").forEach(function (b) { b.addEventListener("click", function () { railStep(+b.dataset.rail); }); });
  function railButtons() {
    var max = rail.scrollWidth - rail.clientWidth - 4;
    $('[data-rail="-1"]').disabled = rail.scrollLeft <= 4;
    $('[data-rail="1"]').disabled = rail.scrollLeft >= max;
  }
  rail.addEventListener("scroll", function () { window.requestAnimationFrame(railButtons); }, { passive: true });
  window.addEventListener("load", railButtons);

  /* ---------- Shop: chips, search, sort, grid ---------- */
  var chipKeys = ["all"].concat(catOrder.filter(function (k) { return PRODUCTS.some(function (p) { return p.cat === k; }); }));
  $("[data-chips]").innerHTML = chipKeys.map(function (key) {
    if (key === "all") return '<button class="chip" type="button" data-cat="all" aria-pressed="true">All</button>';
    var c = CATS[key];
    return '<button class="chip" type="button" data-cat="' + key + '" aria-pressed="false"><i class="ph ph-' + c.icon + '" aria-hidden="true"></i>' + esc(c.label) + '</button>';
  }).join("");

  var state = { cat: "all", q: "", sort: "featured" };
  var grid = $("[data-grid]");

  function visible() {
    var q = state.q.trim().toLowerCase();
    var list = PRODUCTS.filter(function (p) {
      if (state.cat !== "all" && p.cat !== state.cat) return false;
      if (!q) return true;
      return (p.name + " " + p.desc + " " + CATS[p.cat].label + " " + (p.options || []).join(" ")).toLowerCase().indexOf(q) !== -1;
    });
    var big = 1e9; // quoted items sort last on price
    var sorters = {
      featured: function (a, b) { return (b.special ? 1 : 0) - (a.special ? 1 : 0) || catOrder.indexOf(a.cat) - catOrder.indexOf(b.cat) || a.order - b.order; },
      low: function (a, b) { return (a.price == null ? big : a.price) - (b.price == null ? big : b.price) || a.order - b.order; },
      high: function (a, b) { return (b.price == null ? -1 : b.price) - (a.price == null ? -1 : a.price) || a.order - b.order; },
      az: function (a, b) { return a.name.localeCompare(b.name); }
    };
    return list.sort(sorters[state.sort]);
  }

  function renderGrid(animate) {
    var list = visible();
    grid.innerHTML = list.map(function (p, i) {
      var c = CATS[p.cat];
      return '<li class="card' + (animate ? " enter" : "") + '" style="--i:' + Math.min(i, 12) + '">' +
        '<button class="card-media" type="button" data-quick-open="' + p.id + '" aria-label="View details: ' + esc(p.name) + '">' +
        '<img src="' + p.img + '" width="720" height="720" loading="lazy" alt="' + esc(p.name) + '"></button>' +
        '<div class="card-body"><span class="card-cat">' + esc(c.label) + (p.special ? ' <span class="hot">On special</span>' : '') + '</span>' +
        '<h3 class="card-name">' + esc(p.name) + '</h3>' +
        '<div class="card-foot">' + priceHTML(p) +
        '<div data-controls="' + p.id + '">' + controlsHTML(p) + '</div></div></div></li>';
    }).join("");
    var label = state.cat === "all" ? (list.length === 1 ? "product" : "products") : CATS[state.cat].label.toLowerCase();
    $("[data-result-count]").textContent = list.length
      ? "Showing " + list.length + " " + label + (state.q.trim() ? ' for "' + state.q.trim() + '"' : "")
      : "";
    $("[data-empty]").hidden = list.length > 0;
    $("[data-ask-link]").href = waLink("Hi Rico's Sound! Do you have " + (state.q.trim() || "this") + " in stock?");
  }
  renderGrid(false);

  function setCat(key) {
    state.cat = key;
    $$(".chip").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.cat === key)); });
    var active = $('.chip[data-cat="' + key + '"]');
    if (active && active.scrollIntoView && window.innerWidth < 1100) active.scrollIntoView({ block: "nearest", inline: "center", behavior: reduceMotion ? "auto" : "smooth" });
    renderGrid(true);
  }
  $("[data-chips]").addEventListener("click", function (e) {
    var b = e.target.closest(".chip");
    if (b) setCat(b.dataset.cat);
  });
  var searchTimer;
  $("[data-search]").addEventListener("input", function (e) {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function () { state.q = e.target.value; renderGrid(true); }, 140);
  });
  $("[data-sort]").addEventListener("change", function (e) { state.sort = e.target.value; renderGrid(true); });
  $("[data-reset]").addEventListener("click", function () { state.q = ""; $("[data-search]").value = ""; setCat("all"); });

  /* ---------- Global clicks ---------- */
  document.addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("[data-add]"))) { setQty(t.dataset.add, (cart[t.dataset.add] || 0) + 1); return; }
    if ((t = e.target.closest("[data-inc]"))) { setQty(t.dataset.inc, (cart[t.dataset.inc] || 0) + 1); return; }
    if ((t = e.target.closest("[data-dec]"))) { setQty(t.dataset.dec, (cart[t.dataset.dec] || 0) - 1); return; }
    if ((t = e.target.closest("[data-remove]"))) { setQty(t.dataset.remove, 0); return; }
    if ((t = e.target.closest("[data-quick-open]"))) { openQuick(t.dataset.quickOpen); return; }
    if ((t = e.target.closest("[data-flyer]"))) { openFlyer(t.dataset.flyer, t.querySelector("img") ? t.querySelector("img").alt : "Flyer"); return; }
    if ((t = e.target.closest("[data-open-cart]"))) { openCart(); return; }
  });

  /* ---------- Toast ---------- */
  var toastEl = $("[data-toast]");
  var toastTimer;
  function toast(name) {
    toastEl.innerHTML = '<i class="ph-fill ph-check-circle" aria-hidden="true"></i><span>Added: ' + esc(name.length > 34 ? name.slice(0, 32) + "..." : name) + '</span>';
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 2200);
  }

  /* ---------- Dialog helpers ---------- */
  function wireDialog(dlg) {
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg || e.target.closest("[data-close]")) dlg.close();
    });
    dlg.addEventListener("close", function () {
      if (!$$("dialog[open]").length) document.documentElement.style.overflow = "";
      refreshCartBar();
    });
  }
  function showDialog(dlg) {
    if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
    document.documentElement.style.overflow = "hidden";
  }

  /* ---------- Flyer viewer ---------- */
  var flyerView = $("[data-flyer-view]");
  wireDialog(flyerView);
  function openFlyer(name, alt) {
    var img = $("[data-flyer-img]");
    img.src = "assets/img/flyers/" + name + ".webp";
    img.alt = alt;
    img.width = FLYER_W[name] || 700; img.height = 1000;
    showDialog(flyerView);
  }

  /* ---------- Quick view ---------- */
  var quick = $("[data-quick]");
  var quickId = null, quickQty = 1;
  wireDialog(quick);
  var optSel = $("[data-quick-opt]");
  function openQuick(id) {
    var p = byId[id], c = CATS[p.cat];
    quickId = id; quickQty = 1;
    $("[data-quick-media]").innerHTML = '<img src="' + p.img + '" width="720" height="720" alt="' + esc(p.name) + '">';
    $("[data-quick-cat]").textContent = c.label + (p.special ? ". On special" : "");
    $("[data-quick-name]").textContent = p.name;
    $("[data-quick-price]").outerHTML = priceHTML(p).replace('<p class="price', '<p data-quick-price class="quick-price price');
    $("[data-quick-desc]").textContent = p.desc;
    $("[data-q-qty]").textContent = "1";
    $("[data-quick-opt-wrap]").hidden = !p.options;
    optSel.innerHTML = (p.options || []).map(function (o) { return '<option>' + esc(o) + '</option>'; }).join("");
    $("[data-quick-add] span").textContent = p.price == null ? "Add for a quote" : (qtyOf(id) ? "Add more to cart" : "Add to cart");
    var flyerBtn = $("[data-quick-flyer]");
    flyerBtn.hidden = !p.flyer;
    flyerBtn.dataset.name = p.flyer || "";
    $("[data-quick-ask]").href = waLink("Hi Rico's Sound! I'm interested in the " + p.name + (p.price != null ? " (" + rand(p.price) + ")" : "") + ". Is it in stock?");
    showDialog(quick);
  }
  $("[data-q-minus]").addEventListener("click", function () { quickQty = Math.max(1, quickQty - 1); $("[data-q-qty]").textContent = quickQty; });
  $("[data-q-plus]").addEventListener("click", function () { quickQty = Math.min(99, quickQty + 1); $("[data-q-qty]").textContent = quickQty; });
  $("[data-quick-add]").addEventListener("click", function () {
    var p = byId[quickId];
    var key = p.options ? quickId + "|" + optSel.value : quickId;
    quick.close();
    setQty(key, (cart[key] || 0) + quickQty);
  });
  $("[data-quick-flyer]").addEventListener("click", function () {
    var p = byId[quickId];
    quick.close();
    openFlyer(this.dataset.name, "Rico's Sound flyer: " + p.name);
  });

  /* ---------- Cart sheet ---------- */
  var sheet = $("[data-cart]");
  wireDialog(sheet);

  function openCart() {
    $("[data-cart-sent]").hidden = true;
    refreshCart();
    showDialog(sheet);
  }

  function refreshCart() {
    var n = count();
    $("[data-cart-count]").textContent = n;
    $(".cart-btn").setAttribute("aria-label", "Open cart, " + n + (n === 1 ? " item" : " items"));
    var keys = Object.keys(cart);
    var sent = !$("[data-cart-sent]").hidden;
    $("[data-cart-empty]").hidden = keys.length > 0 || sent;
    $("[data-cart-body]").hidden = keys.length === 0 || sent;
    $("[data-cart-lines]").innerHTML = keys.map(function (key) {
      var s = split(key), p = byId[s.id];
      var per = !p.unit || p.unit === "each" ? " each" : /^incl/.test(p.unit) ? " " + p.unit : " per " + p.unit;
      var each = p.price == null ? "Quoted for your vehicle" : rand(p.price) + per;
      return '<li><img src="' + p.img + '" width="64" height="64" alt="">' +
        '<div><p class="line-name">' + esc(p.name) + '</p>' + (s.opt ? '<p class="line-opt">' + esc(s.opt) + '</p>' : '') +
        '<p class="line-price">' + esc(each) + '</p>' + lineControlsHTML(key) + '</div>' +
        '<div class="line-side"><span class="line-total">' + (p.price == null ? "Quote" : rand(p.price * cart[key])) + '</span>' +
        '<button class="line-remove" type="button" data-remove="' + esc(key) + '">Remove</button></div></li>';
    }).join("");
    $("[data-cart-subtotal]").textContent = rand(subtotal()) + (hasQuote() ? " + quote" : "");
    $("[data-quote-note]").hidden = !hasQuote();
    refreshCartBar();
  }

  function refreshCartBar() {
    var n = count();
    var bar = $("[data-cart-bar]");
    bar.hidden = n === 0 || sheet.open;
    document.body.classList.toggle("has-cart-bar", n > 0);
    $("[data-cart-bar-text]").textContent = "View cart, " + n + (n === 1 ? " item" : " items");
    $("[data-cart-bar-total]").textContent = subtotal() ? rand(subtotal()) : "Quote";
  }

  $("[data-go-shop]").addEventListener("click", function () { sheet.close(); $("#shop").scrollIntoView(); });

  var form = $("[data-checkout]");
  form.addEventListener("change", function (e) {
    if (e.target.name === "method") $("[data-address-field]").hidden = e.target.value !== "courier";
  });

  function orderText() {
    var data = new FormData(form);
    var lines = Object.keys(cart).map(function (key, i) {
      var s = split(key), p = byId[s.id];
      return (i + 1) + ". " + p.name + (s.opt ? " (" + s.opt + ")" : "") + " x " + cart[key] +
        (p.price == null ? " = please quote" : " = " + rand(p.price * cart[key]));
    });
    var method = {
      collect: "I'll collect at the shop in Witbank.",
      fit: "Please fit it for me. When can I book the car in?",
      courier: "Please courier to: " + (String(data.get("address") || "").trim() || "(town to confirm)") + ". Quote me for delivery."
    }[data.get("method")];
    var vehicle = String(data.get("vehicle") || "").trim();
    var note = String(data.get("note") || "").trim();
    return [
      "Hi Rico's Sound! I'd like to order from your website:",
      "",
      lines.join("\n"),
      "",
      "Subtotal: " + rand(subtotal()) + (hasQuote() ? " plus quoted items" : "") + " (" + count() + (count() === 1 ? " item" : " items") + ")",
      "Name: " + String(data.get("name") || "").trim()
    ].concat(vehicle ? ["Vehicle: " + vehicle] : [])
      .concat([method])
      .concat(note ? ["Note: " + note] : [])
      .concat(["", "Please confirm stock, fitment and my total. Thanks!"]).join("\n");
  }

  function validName() {
    var input = $("#co-name");
    var ok = input.value.trim().length > 1;
    input.setAttribute("aria-invalid", String(!ok));
    if (ok) input.removeAttribute("aria-describedby"); else input.setAttribute("aria-describedby", "co-name-error");
    $("#co-name-error").hidden = ok;
    if (!ok) input.focus();
    return ok;
  }
  $("#co-name").addEventListener("input", function () {
    if (this.getAttribute("aria-invalid") === "true" && this.value.trim().length > 1) {
      this.setAttribute("aria-invalid", "false"); this.removeAttribute("aria-describedby"); $("#co-name-error").hidden = true;
    }
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!count() || !validName()) return;
    var link = waLink(orderText());
    window.open(link, "_blank", "noopener");
    $("[data-resend]").href = link;
    $("[data-cart-sent]").hidden = false;
    refreshCart();
    $(".sheet-inner").scrollTop = 0;
  });

  $("[data-new-order]").addEventListener("click", function () {
    cart = {}; persist();
    form.reset(); $("[data-address-field]").hidden = true;
    $("[data-cart-sent]").hidden = true;
    PRODUCTS.forEach(function (p) { refreshControls(p.id); });
    refreshCart();
  });

  refreshCart();

  /* ---------- Header state and scroll reveals (IntersectionObserver, no scroll listeners) ---------- */
  var header = $("[data-header]");
  var sentinel = document.createElement("div");
  sentinel.style.cssText = "position:absolute;top:0;left:0;height:40px;width:1px;pointer-events:none";
  document.body.prepend(sentinel);
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      header.classList.toggle("is-scrolled", !entries[0].isIntersecting);
    }).observe(sentinel);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    $$(".reveal").forEach(function (el, i) { el.style.setProperty("--i", i % 4); io.observe(el); });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
