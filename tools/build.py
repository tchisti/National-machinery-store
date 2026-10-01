#!/usr/bin/env python3
"""
National Machinery Stores — static site generator.

Single source of truth: data/site.json + data/products.json.

    python3 tools/build.py          # regenerate pages, homepage regions, sitemap, llms.txt
    python3 tools/build.py --media  # also re-render logo PNGs and social share (OG) images (needs Pillow)

Outputs
  products/<slug>.html                   one SEO landing page per product
  index.html  regions between <!-- @gen:NAME --> ... <!-- /@gen:NAME -->
  sitemap.xml, llms.txt
Everything else in index.html is hand-written and safe to edit directly.
"""
import hashlib
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
DATA = json.loads((ROOT / "data/products.json").read_text(encoding="utf-8"))
PRODUCTS = DATA["products"]
STAGES = {s["id"]: s for s in DATA["stages"]}
FAQ = DATA["faq"]
BASE = SITE["baseUrl"].rstrip("/")
CSS_VER = hashlib.md5((ROOT / "assets/css/site.css").read_bytes()).hexdigest()[:8]
JS_VER = hashlib.md5((ROOT / "assets/js/site.js").read_bytes()).hexdigest()[:8]

try:
    from PIL import Image  # optional: exact width/height attributes + media rendering
except ImportError:  # pragma: no cover
    Image = None


def e(s):
    return html.escape(str(s), quote=True)


def wa_link(text):
    return f"https://wa.me/{SITE['whatsapp']}?text={quote(text)}"


def img_size(rel):
    p = ROOT / rel
    if Image and p.exists():
        with Image.open(p) as im:
            return im.size
    return (1200, 900)


def product_url(p, absolute=False):
    path = f"products/{p['slug']}.html"
    return f"{BASE}/{path}" if absolute else path


def stage_label(p):
    st = STAGES[p["stage"]]
    return f"{st['num']} · {st['name']}"


# --------------------------------------------------------------------------
# Icons
# --------------------------------------------------------------------------
SPRITE = """<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">
<symbol id="i-phone" viewBox="0 0 24 24"><path fill="currentColor" d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1-9.4 0-17-7.6-17-17 0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path fill="currentColor" d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35z"/><path fill="currentColor" d="M12 0C5.37 0 0 5.37 0 12c0 2.1.55 4.09 1.5 5.81L.06 23.18a.75.75 0 00.93.91l5.5-1.44A11.95 11.95 0 0012 24c6.63 0 12-5.37 12-12S18.63 0 12 0zm0 21.75c-1.8 0-3.5-.49-4.95-1.35l-.36-.21-3.67.96.97-3.58-.23-.37A9.72 9.72 0 012.25 12C2.25 6.59 6.59 2.25 12 2.25S21.75 6.59 21.75 12 17.41 21.75 12 21.75z"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M4 12h15M13 6l6 6-6 6"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.5l4.5 4.5L19.5 6.5"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></g></symbol>
<symbol id="i-truck" viewBox="0 0 24 24"><path fill="currentColor" d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4zM6 18.5a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm13.5-9l1.96 2.5H17V9.5h2.5zM18 18.5a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></g></symbol>
<symbol id="i-receipt" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3z"/><path d="M9 8h6M9 12h6" stroke-linecap="round"/></g></symbol>
<symbol id="i-wrench" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M14.7 6.3a4 4 0 00-5.4 5.1L3.5 17.2a1.8 1.8 0 002.5 2.5l5.8-5.8a4 4 0 005.1-5.4l-2.5 2.5-2.2-.4-.4-2.2 2.9-2.1z"/></symbol>
<symbol id="i-gear" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3.2"/><path stroke-linecap="round" d="M12 2.8v2.6M12 18.6v2.6M21.2 12h-2.6M5.4 12H2.8M18.5 5.5l-1.8 1.8M7.3 16.7l-1.8 1.8M18.5 18.5l-1.8-1.8M7.3 7.3L5.5 5.5"/><circle cx="12" cy="12" r="6.6"/></g></symbol>
<symbol id="i-swap" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M4 8h14l-4-4M20 16H6l4 4"/></symbol>
<symbol id="i-hammer" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M13 7l4 4M9.5 3.5l6 6-2.5 2.5-6-6zM11.5 10.5L4 18a1.4 1.4 0 002 2l7.5-7.5"/></symbol>
<symbol id="i-bolt" viewBox="0 0 24 24"><path fill="currentColor" d="M13 2L4 14h6l-1 8 9-12h-6l1-8z"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M4 7h16M4 12h16M4 17h10"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></symbol>
</svg>"""


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


LOGO = """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="National Machinery Stores logo"><rect width="100" height="100" rx="16" fill="#E4A51E"/><path d="M50 9C50 9 14 43 14 66a36 36 0 0072 0C86 43 50 9 50 9z" fill="#111315"/><polygon points="20,52 26,52 36,66 36,52 42,52 42,74 36,74 26,60 26,74 20,74" fill="#E4A51E"/><polygon points="47,52 53,52 60,63 67,52 73,52 73,74 67,74 67,62 60,72 53,62 53,74 47,74" fill="#E4A51E"/></svg>"""


# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------
NAV = [
    ("Products", "#products"),
    ("Your line", "#line"),
    ("Buyer's guide", "#guide"),
    ("Services", "#services"),
    ("About", "#about"),
    ("FAQ", "#faq"),
    ("Contact", "#contact"),
]


def chrome_top(root):
    home = root or "./"
    links = "".join(f'<a href="{home}{h}">{e(t)}</a>' for t, h in NAV)
    dlinks = "".join(f'<a href="{home}{h}">{e(t)}</a>' for t, h in NAV)
    langs = " · ".join(SITE["languages"])
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="util">
  <div class="wrap">
    <span>{e(SITE['hours'])}<span class="util-langs"> · {e(langs)}</span></span>
    <a href="tel:{SITE['phone']}">Sales {e(SITE['phoneDisplay'])}</a>
  </div>
</div>
<header class="header">
  <div class="wrap">
    <a class="brand" href="{home}" aria-label="National Machinery Stores — home">
      {LOGO}
      <span><span class="brand-name">National Machinery Stores</span><span class="brand-sub">Kadi · Gujarat · Est. {SITE['founded']}</span></span>
    </a>
    <nav class="nav" aria-label="Primary">{links}</nav>
    <a class="btn btn--sm header-cta" href="{wa_link('Hello National Machinery Stores, I need a quote.')}" target="_blank" rel="noopener">{ic('wa')}Get a quote</a>
    <button class="menu-btn" type="button" data-open-drawer aria-controls="drawer" aria-expanded="false" aria-label="Open menu">{ic('menu')}</button>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true" role="dialog" aria-label="Menu">
  <div class="drawer-top">
    <span class="brand-sub">Menu</span>
    <button class="menu-btn" type="button" data-close-drawer aria-label="Close menu">{ic('close')}</button>
  </div>
  <nav aria-label="Mobile">{dlinks}</nav>
  <div class="btn-row">
    <a class="btn" href="tel:{SITE['phone']}">{ic('phone')}Call</a>
    <a class="btn btn--wa" href="{wa_link('Hello National Machinery Stores, I need a quote.')}" target="_blank" rel="noopener">{ic('wa')}WhatsApp</a>
  </div>
</div>"""


def footer(root):
    home = root or "./"
    prod = "".join(f'<li><a href="{root}{product_url(p)}">{e(p["name"])}</a></li>' for p in PRODUCTS)
    o, f = SITE["office"], SITE["factory"]
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{home}">{LOGO}<span><span class="brand-name" style="color:#F4F0E7">National Machinery Stores</span><span class="brand-sub">Kadi · Gujarat · Est. {SITE['founded']}</span></span></a>
        <p class="footer-gu" lang="gu">નેશનલ મશીનરી સ્ટોર્સ · કડી, મહેસાણા</p>
        <p class="about-txt">Manufacturer, exporter, supplier and service provider of oil expellers, filter presses, conveyors, refining equipment and spare parts for edible-oil mills — in India and abroad.</p>
        <ul>
          <li><a href="tel:{SITE['phone']}">Call {e(SITE['phoneDisplay'])}</a></li>
          <li><a href="https://wa.me/{SITE['whatsapp']}" target="_blank" rel="noopener">WhatsApp {e(SITE['whatsappDisplay'])}</a></li>
          <li>{e(o['label'])}: {e(', '.join(o['lines'][:3]))}</li>
          <li>{e(f['label'])}: {e(', '.join(f['lines'][:3]))}</li>
        </ul>
      </div>
      <div>
        <h2>Products</h2>
        <ul>{prod}</ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="{home}#line">Build your line</a></li>
          <li><a href="{home}#guide">Buyer's guide</a></li>
          <li><a href="{home}#services">Erection &amp; AMC</a></li>
          <li><a href="{home}#about">About us</a></li>
          <li><a href="{home}#faq">FAQ</a></li>
          <li><a href="{home}#contact">Contact &amp; quote</a></li>
          <li><a href="{root}catalogue.html">Printable catalogue</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-base">
      <span>© <span data-year>{SITE['updated'][:4]}</span> National Machinery Stores, Kadi, Mahesana, Gujarat, India</span>
      <span>GST billing · PAN India delivery · Export · Updated {e(SITE['updatedLabel'])}</span>
    </div>
  </div>
</footer>"""


def action_bar(msg="Hello National Machinery Stores, I need a quote."):
    return f"""<a class="fab-wa" href="{wa_link(msg)}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ic('wa')}</a>
<div class="actionbar" role="navigation" aria-label="Quick contact">
  <a class="btn btn--sm" href="tel:{SITE['phone']}">{ic('phone')}Call now</a>
  <a class="btn btn--sm btn--wa" href="{wa_link(msg)}" target="_blank" rel="noopener">{ic('wa')}WhatsApp</a>
</div>"""


def product_options(selected=None):
    opts = ['<option value="">Select product or service</option>']
    for p in PRODUCTS:
        s = " selected" if p["name"] == selected else ""
        opts.append(f'<option{s}>{e(p["name"])}</option>')
    for extra in ["Complete oil mill plant (turnkey)", "Used / refurbished machinery", "Sell my machinery (commission agent)", "AMC — Annual Maintenance Contract"]:
        opts.append(f"<option>{e(extra)}</option>")
    opts.append('<option value="Other">Other — please specify</option>')
    return "\n".join(opts)


def inquiry_form(selected=None, compact=False):
    extra = "" if compact else """
          <div class="field"><label for="f-company">Company / mill</label><input class="input" id="f-company" name="company" autocomplete="organization" placeholder="Your business name"></div>"""
    return f"""<form class="form-card" data-wa-form novalidate>
        <div class="form-grid">
          <div class="field"><label for="f-name">Full name <span class="req">*</span></label><input class="input" id="f-name" name="name" autocomplete="name" required placeholder="Your name"></div>
          <div class="field"><label for="f-phone">Phone <span class="req">*</span></label><input class="input" id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required placeholder="+91 98xxx xxxxx"></div>
          <div class="field{' full' if compact else ''}"><label for="f-city">City &amp; state <span class="req">*</span></label><input class="input" id="f-city" name="city" autocomplete="address-level2" required placeholder="e.g. Rajkot, Gujarat"></div>{extra}
          <div class="field full"><label for="f-product">Product or service <span class="req">*</span></label><select class="input" id="f-product" name="product" required>{product_options(selected)}</select></div>
          <div class="field full" data-other hidden><label for="f-other">What are you looking for?</label><input class="input" id="f-other" name="other" placeholder="Describe the machine or part"></div>
          <div class="field full"><label for="f-capacity">Seed type &amp; capacity</label><input class="input" id="f-capacity" name="capacity" placeholder="e.g. Groundnut, 10 tonnes/day"></div>
          <div class="field full"><label for="f-message">Requirement details</label><textarea class="input" id="f-message" name="message" rows="3" placeholder="Quantity, budget, timeline, new or refurbished…"></textarea></div>
        </div>
        <button class="btn btn--wa btn--block" type="submit" style="margin-top:18px">{ic('wa')}Send inquiry on WhatsApp</button>
        <p class="form-note">Opens WhatsApp with your details filled in. We call back within {e(SITE['callback'])} · {e(' / '.join(SITE['languages']))}.</p>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>"""


# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------
def card(p, root="", idx=None, wide=False):
    img = p["images"][0]
    rel = f"images/products/{img['src']}"
    w, h = img_size(rel)
    badge = f'<span class="card-badge">{e(p["badge"])}</span>' if p.get("badge") else ""
    pills = "".join(f'<span class="spec-pill">{e(s)}</span>' for s in p["keySpecs"])
    msg = f"Hello National Machinery Stores, I need price and availability for: {p['name']}."
    num = f"No. {idx:02d} · " if idx else ""
    return f"""<article class="card{' card--wide' if wide else ''} rv" data-stage="{p['stage']}">
  <div class="card-media fit-{img['fit']}">
    <span class="card-tag">{num}{e(STAGES[p['stage']]['name'])}</span>{badge}
    <img src="{root}{rel}" alt="{e(img['alt'])}" width="{w}" height="{h}" loading="lazy" decoding="async">
  </div>
  <div class="card-body">
    <h3><a href="{root}{product_url(p)}">{e(p['name'])}</a></h3>
    <p>{e(p['short'])}</p>
    <div class="specs-inline">{pills}</div>
    <div class="card-foot"><span class="card-cta">Specs &amp; price {ic('arrow')}</span><a class="wa-mini" href="{wa_link(msg)}" target="_blank" rel="noopener">{ic('wa')}Quote</a></div>
  </div>
</article>"""


def gen_cards():
    out = []
    for i, p in enumerate(PRODUCTS, 1):
        out.append(card(p, "", i, wide=(p["slug"] == "oil-mill-erection-service")))
    return "\n".join(out)


def gen_filters():
    chips = [f'<button class="chip" type="button" data-filter="all" aria-pressed="true">All <span class="n">{len(PRODUCTS)}</span></button>']
    for st in DATA["stages"]:
        n = sum(1 for p in PRODUCTS if p["stage"] == st["id"])
        chips.append(f'<button class="chip" type="button" data-filter="{st["id"]}" aria-pressed="false">{st["num"]} {e(st["name"])} <span class="n">{n}</span></button>')
    return "\n".join(chips)


def gen_line():
    out = []
    for st in DATA["stages"]:
        items = "".join(
            f'<li><a href="{product_url(p)}">{e(p["name"])}{ic("arrow")}</a></li>'
            for p in PRODUCTS if p["stage"] == st["id"]
        )
        out.append(f"""<div class="stage rv">
  <span class="stage-num">{st['num']}</span>
  <h3>{e(st['name'])}</h3>
  <p class="verb">{e(st['verb'])}</p>
  <p>{e(st['text'])}</p>
  <ul>{items}</ul>
</div>""")
    return "\n".join(out)


def faq_html(keys, open_first=True):
    out = []
    for i, k in enumerate(keys):
        q = FAQ[k]
        o = " open" if (open_first and i == 0) else ""
        out.append(f'<details{o}><summary>{e(q["q"])}</summary><div><p>{e(q["a"])}</p></div></details>')
    return "\n".join(out)


def testimonials_html():
    items = SITE.get("testimonials") or []
    if not items:
        return ""
    quotes = "".join(
        f"""<figure class="quote"><blockquote>“{e(t['quote'])}”</blockquote><figcaption><b>{e(t['name'])}</b>{e(t.get('role', ''))}{(' · ' + e(t['place'])) if t.get('place') else ''}{(' · ' + e(t['since'])) if t.get('since') else ''}</figcaption></figure>"""
        for t in items
    )
    return f"""<section class="section" aria-labelledby="t-h">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow"><span class="idx">★</span> In their words</span><h2 class="h-section" id="t-h">What mill owners say</h2></div>
    <div class="quote-grid">{quotes}</div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------
def business_node():
    o, f = SITE["office"], SITE["factory"]
    return {
        "@type": "LocalBusiness",
        "@id": f"{BASE}/#business",
        "name": SITE["name"],
        "alternateName": ["NMS Kadi", "નેશનલ મશીનરી સ્ટોર્સ"],
        "url": f"{BASE}/",
        "logo": f"{BASE}/images/brand/logo-512.png",
        "image": [f"{BASE}/images/og/og-home.jpg", f"{BASE}/images/products/oil-mill-machinery.webp"],
        "description": "Oil mill machinery manufacturer, exporter, supplier and service provider in Kadi, Mahesana, Gujarat. Oil expellers, filter presses, screw conveyors, Radler chains, conveyor belts, vassal oil neutralizers, spare parts, and oil mill erection and AMC.",
        "foundingDate": SITE["founded"],
        "founder": {"@type": "Person", "name": SITE["founder"]},
        "telephone": SITE["phone"],
        "priceRange": "₹₹",
        "currenciesAccepted": "INR",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": o["street"],
            "addressLocality": o["locality"],
            "addressRegion": o["region"],
            "postalCode": o["postalCode"],
            "addressCountry": "IN",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": o["lat"], "longitude": o["lng"]},
        "hasMap": o["map"],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "09:00", "closes": "19:00",
        }],
        "areaServed": [{"@type": "Country", "name": "India"}, {"@type": "Continent", "name": "Africa"}],
        "knowsLanguage": ["hi", "gu", "en"],
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": SITE["phone"], "contactType": "sales", "areaServed": ["IN", "Africa"], "availableLanguage": ["Hindi", "Gujarati", "English"]},
            {"@type": "ContactPoint", "telephone": "+" + SITE["whatsapp"], "contactType": "customer support", "description": "WhatsApp", "availableLanguage": ["Hindi", "Gujarati", "English"]},
        ],
        "department": {
            "@type": "LocalBusiness",
            "name": "National Machinery Stores — Factory & Warehouse",
            "address": {"@type": "PostalAddress", "streetAddress": f["street"], "addressLocality": f["locality"], "addressRegion": f["region"], "postalCode": f["postalCode"], "addressCountry": "IN"},
            "hasMap": f["map"],
        },
        "sameAs": [o["map"]],
        "knowsAbout": ["Oil expeller", "Oil mill machinery", "Filter press", "Edible oil refining", "Screw conveyor", "En-masse conveyor", "Oil mill erection"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Oil mill machinery & services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service" if p["slug"] == "oil-mill-erection-service" else "Product", "name": p["name"], "url": product_url(p, True)}}
                for p in PRODUCTS
            ],
        },
    }


def website_node():
    return {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": SITE["name"], "inLanguage": "en-IN", "publisher": {"@id": f"{BASE}/#business"}}


def faq_node(keys, page_url):
    return {
        "@type": "FAQPage",
        "@id": f"{page_url}#faq",
        "mainEntity": [{"@type": "Question", "name": FAQ[k]["q"], "acceptedAnswer": {"@type": "Answer", "text": FAQ[k]["a"]}} for k in keys],
    }


def jsonld(graph):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")) + "</script>"


def home_jsonld():
    page = {"@type": "WebPage", "@id": f"{BASE}/#webpage", "url": f"{BASE}/", "name": "Oil Mill Machinery & Oil Expellers | National Machinery Stores, Kadi", "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": f"{BASE}/#business"}, "dateModified": SITE["updated"], "inLanguage": "en-IN", "primaryImageOfPage": f"{BASE}/images/editorial/hero-oil-expeller-1400.webp"}
    return jsonld([business_node(), website_node(), page, faq_node(DATA["homeFaq"], f"{BASE}/")])


def product_jsonld(p):
    url = product_url(p, True)
    imgs = [f"{BASE}/images/products/{i['src']}" for i in p["images"]]
    is_service = p["slug"] == "oil-mill-erection-service"
    item = {
        "@type": "Service" if is_service else "Product",
        "@id": f"{url}#item",
        "name": p["name"],
        "description": p["summary"],
        "image": imgs,
        "url": url,
        "category": "Oil mill machinery" if not is_service else "Oil mill erection and maintenance",
    }
    if is_service:
        item.update({"serviceType": "Oil mill erection, demolition and annual maintenance contract", "provider": {"@id": f"{BASE}/#business"}, "areaServed": {"@type": "Country", "name": "India"}})
    else:
        item.update({"additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in p["specs"]]})
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Products", "item": f"{BASE}/#products"},
        {"@type": "ListItem", "position": 3, "name": p["name"], "item": url},
    ]}
    page = {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": p["seoTitle"], "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": f"{url}#item"}, "dateModified": SITE["updated"], "inLanguage": "en-IN", "breadcrumb": crumbs}
    graph = [item, page, crumbs, {"@type": "LocalBusiness", "@id": f"{BASE}/#business", "name": SITE["name"], "url": f"{BASE}/", "telephone": SITE["phone"]}]
    if p.get("faq"):
        graph.append(faq_node(p["faq"], url))
    return jsonld(graph)


# --------------------------------------------------------------------------
# Product page
# --------------------------------------------------------------------------
def head(title, desc, url, og_image, root, extra=""):
    return f"""<!doctype html>
<html lang="en-IN" data-wa="{SITE['whatsapp']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#111315">
<meta property="og:site_name" content="National Machinery Stores">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{root}images/brand/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="{root}images/brand/apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&amp;family=JetBrains+Mono:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="{root}assets/css/site.css?v={CSS_VER}">
{extra}
</head>"""


def product_page(p):
    root = "../"
    url = product_url(p, True)
    st = STAGES[p["stage"]]
    imgs = p["images"]
    first = imgs[0]
    rel0 = f"images/products/{first['src']}"
    w0, h0 = img_size(rel0)
    thumbs = ""
    if len(imgs) > 1:
        tb = []
        for i, im in enumerate(imgs):
            r = f"images/products/{im['src']}"
            tb.append(f'<button type="button" data-gallery-thumb data-src="{root}{r}" data-alt="{e(im["alt"])}" aria-current="{"true" if i == 0 else "false"}" aria-label="Photo {i + 1} of {len(imgs)}"><img src="{root}{r}" alt="" loading="lazy" decoding="async" width="76" height="76"></button>')
        thumbs = f'<div class="thumbs">{"".join(tb)}</div>'
    key = "".join(f"<div><dt>{e(lbl)}</dt><dd>{e(val)}</dd></div>" for lbl, val in zip(p.get("keyLabels", ["Spec", "Spec"]), p["keySpecs"]))
    spec_rows = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in p["specs"])
    feats = "".join(f"<li><span>{i:02d}</span>{e(f)}</li>" for i, f in enumerate(p["features"], 1))
    line = "".join(f'<li class="{"is-here" if s["id"] == p["stage"] else ""}">{s["num"]} {e(s["name"])}</li>' for s in DATA["stages"])
    rel_items = [x for x in PRODUCTS if x["stage"] == p["stage"] and x["slug"] != p["slug"]]
    for slug in ["oil-expeller-spare-parts", "oil-mill-erection-service", "oil-mill-machinery", "plastic-oil-filter-hydraulic", "mini-oil-expeller"]:
        if len(rel_items) >= 3:
            break
        cand = next(x for x in PRODUCTS if x["slug"] == slug)
        if cand["slug"] != p["slug"] and cand not in rel_items:
            rel_items.append(cand)
    related = "".join(card(x, root) for x in rel_items[:3])
    msg = f"Hello National Machinery Stores, I need price and availability for: {p['name']}."
    faq = ""
    if p.get("faq"):
        faq = f"""<section class="section on-paper-2" aria-labelledby="pf-h">
  <div class="wrap faq">
    <div class="section-head"><span class="eyebrow"><span class="idx">?</span> Questions</span><h2 class="h-sub" id="pf-h">{e(p['name'])}: common questions</h2></div>
    <div class="faq-list">{faq_html(p['faq'])}</div>
  </div>
</section>"""
    preload = f'<link rel="preload" as="image" href="{root}{rel0}" fetchpriority="high">\n{product_jsonld(p)}'
    return f"""{head(p['seoTitle'], p['metaDesc'], url, f"{BASE}/images/og/{p['slug']}.jpg", root, preload)}
<body>
{SPRITE}
{chrome_top(root)}
<main id="main">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="../">Home</a></li><li><a href="../#products">Products</a></li><li aria-current="page">{e(p['name'])}</li></ol></nav>
    <div class="p-hero">
      <div class="gallery">
        <div class="gallery-main fit-{first['fit']}"><img data-gallery-main src="{root}{rel0}" alt="{e(first['alt'])}" width="{w0}" height="{h0}" fetchpriority="high" decoding="async"></div>
        {thumbs}
      </div>
      <div class="p-info">
        <span class="eyebrow"><span class="idx">{st['num']}</span> {e(st['name'])} stage{(' · ' + e(p['badge'])) if p.get('badge') else ''}</span>
        <h1>{e(p['name'])}</h1>
        <p class="sub">Supplied, erected &amp; serviced from Kadi, Mahesana, Gujarat</p>
        <p class="answer">{e(p['summary'])}</p>
        <dl class="keyspecs">{key}</dl>
        <div class="btn-row">
          <a class="btn btn--wa" href="{wa_link(msg)}" target="_blank" rel="noopener">{ic('wa')}Get price on WhatsApp</a>
          <a class="btn btn--line" href="tel:{SITE['phone']}">{ic('phone')}{e(SITE['phoneDisplay'])}</a>
        </div>
        <ul class="assure">
          <li>{ic('receipt')}GST billing</li>
          <li>{ic('truck')}PAN India delivery</li>
          <li>{ic('swap')}New &amp; refurbished</li>
          <li>{ic('globe')}Export to Africa &amp; beyond</li>
        </ul>
      </div>
    </div>
  </div>

  <section class="section on-paper-2" aria-labelledby="spec-h">
    <div class="wrap p-body">
      <div>
        <span class="eyebrow"><span class="idx">A</span> Specification sheet</span>
        <h2 class="h-sub" id="spec-h" style="margin:14px 0 22px">{e(p['name'])} specifications</h2>
        <div class="table-wrap"><table class="spec spec--kv"><caption>{e(p['name'])} — typical range, confirm per model</caption><tbody>{spec_rows}</tbody></table></div>
      </div>
      <div>
        <span class="eyebrow"><span class="idx">B</span> Build &amp; features</span>
        <h2 class="h-sub" style="margin:14px 0 22px">What you get</h2>
        <ul class="features">{feats}</ul>
        <p class="muted" style="margin-top:22px">{e(p['desc'])}</p>
      </div>
    </div>
  </section>

  <section class="section on-ink" aria-labelledby="app-h">
    <div class="wrap">
      <div class="cta-band">
        <div>
          <span class="eyebrow"><span class="idx">C</span> Where it fits</span>
          <h2 class="h-sub" id="app-h" style="margin:14px 0 14px">Applications</h2>
          <p class="lede">{e(p['apps'])}</p>
          <ul class="mini-line" style="margin-top:22px" aria-label="Oil mill line stages">{line}</ul>
        </div>
        <div class="btn-row">
          <a class="btn" href="{wa_link(msg)}" target="_blank" rel="noopener">{ic('wa')}Ask for this machine</a>
          <a class="btn btn--ghost" href="../#line">See the full line {ic('arrow')}</a>
        </div>
      </div>
    </div>
  </section>

  {faq}

  <section class="section" aria-labelledby="rel-h">
    <div class="wrap">
      <div class="section-head"><span class="eyebrow"><span class="idx">→</span> Same line</span><h2 class="h-section" id="rel-h">Often bought with it</h2></div>
      <div class="grid-cards">{related}</div>
    </div>
  </section>

  <section class="section on-ink" id="contact" aria-labelledby="pc-h">
    <div class="wrap contact">
      {inquiry_form(selected=p['name'], compact=True)}
      <div>
        <span class="eyebrow"><span class="idx">✆</span> Price &amp; availability</span>
        <h2 class="h-section" id="pc-h" style="margin:16px 0 18px">Get today's price for the {e(p['name'])}</h2>
        <p class="lede">Tell us your seed, capacity and city. Our sales team replies on WhatsApp and calls back within {e(SITE['callback'])}, in Hindi, Gujarati or English.</p>
        <div class="channels" style="margin-top:28px">
          <div class="channel"><span class="ic">{ic('phone')}</span><div><div class="k">Call sales</div><a class="v" href="tel:{SITE['phone']}">{e(SITE['phoneDisplay'])}</a><div class="sm">{e(SITE['hours'])}</div></div></div>
          <div class="channel"><span class="ic wa">{ic('wa')}</span><div><div class="k">WhatsApp</div><a class="v" href="https://wa.me/{SITE['whatsapp']}" target="_blank" rel="noopener">{e(SITE['whatsappDisplay'])}</a></div></div>
        </div>
      </div>
    </div>
  </section>
</main>
{footer(root)}
{action_bar(msg)}
<script src="{root}assets/js/site.js?v={JS_VER}" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Homepage regions
# --------------------------------------------------------------------------
def replace_region(src, name, content):
    pat = re.compile(r"(<!-- @gen:%s -->)(.*?)(<!-- /@gen:%s -->)" % (re.escape(name), re.escape(name)), re.S)
    if not pat.search(src):
        raise SystemExit(f"index.html is missing region @gen:{name}")
    return pat.sub(lambda m: m.group(1) + "\n" + content + "\n" + m.group(3), src)


def build_index():
    path = ROOT / "index.html"
    src = path.read_text(encoding="utf-8")
    regions = {
        "jsonld": home_jsonld(),
        "assets-css": f'<link rel="stylesheet" href="assets/css/site.css?v={CSS_VER}">',
        "assets-js": f'<script src="assets/js/site.js?v={JS_VER}" defer></script>',
        "sprite": SPRITE,
        "chrome-top": chrome_top(""),
        "line": gen_line(),
        "filters": gen_filters(),
        "cards": gen_cards(),
        "faq": faq_html(DATA["homeFaq"]),
        "form": inquiry_form(),
        "testimonials": testimonials_html(),
        "footer": footer(""),
        "actionbar": action_bar(),
    }
    for k, v in regions.items():
        src = replace_region(src, k, v)
    path.write_text(src, encoding="utf-8")


def build_sitemap():
    urls = [(f"{BASE}/", "1.0")] + [(product_url(p, True), "0.8") for p in PRODUCTS] + [(f"{BASE}/catalogue.html", "0.4")]
    body = "\n".join(f"  <url><loc>{u}</loc><lastmod>{SITE['updated']}</lastmod><priority>{pr}</priority></url>" for u, pr in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n', encoding="utf-8")


def build_llms():
    o, f = SITE["office"], SITE["factory"]
    lines = [
        "# National Machinery Stores",
        "",
        f"> Oil mill machinery manufacturer, exporter, supplier and service provider in Kadi, Mahesana district, Gujarat, India. Founded in {SITE['founded']} by {SITE['founder']}. Supplies oil expellers, filter presses, conveyors, refining equipment and spare parts, and erects and maintains complete edible-oil plants across {SITE['stats']['states']} Indian states and for export clients in Africa.",
        "",
        "## Key facts",
        f"- Founded: {SITE['founded']} (Kadi, Mahesana, Gujarat)",
        f"- Office: {', '.join(o['lines'])}",
        f"- Factory & warehouse: {', '.join(f['lines'])}",
        f"- Sales phone: {SITE['phoneDisplay']}; WhatsApp: {SITE['whatsappDisplay']}",
        f"- Hours: {SITE['hours']}",
        f"- Languages: {', '.join(SITE['languages'])}",
        f"- Clients served: {SITE['stats']['clients']}; states served: {SITE['stats']['states']}",
        f"- Spare parts dispatch: {SITE['stats']['spares']} for stocked items",
        "- New and refurbished machinery; commission agent for used machinery; GST billing; PAN India delivery; licensed exporter",
        "",
        "## Products and services",
    ]
    for p in PRODUCTS:
        lines.append(f"- [{p['name']}]({product_url(p, True)}): {p['summary']}")
    lines += ["", "## Frequently asked questions"]
    for k in DATA["homeFaq"]:
        lines.append(f"- Q: {FAQ[k]['q']}\n  A: {FAQ[k]['a']}")
    lines += ["", f"Last updated: {SITE['updated']}", ""]
    (ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------
# Media (logo PNGs + Open Graph share images). Requires Pillow.
# --------------------------------------------------------------------------
def build_media():
    if not Image:
        raise SystemExit("Pillow is required for --media (pip install pillow)")
    from PIL import ImageDraw, ImageFont, ImageFilter

    fonts = ROOT / "tools/fonts"
    F_DISP = str(fonts / "Archivo-Expanded-ExtraBold.ttf")
    F_SEMI = str(fonts / "Archivo-SemiBold.ttf")
    F_MONO = str(fonts / "JetBrainsMono-Medium.ttf")
    INK, PAPER, OIL, MUTED = (17, 19, 21), (244, 240, 231), (228, 165, 30), (169, 164, 154)

    def logo(size):
        s = size / 100
        im = Image.new("RGBA", (size * 4, size * 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        k = 4 * s
        d.rounded_rectangle([0, 0, 100 * k - 1, 100 * k - 1], radius=16 * k, fill=OIL)
        # drop: circle + triangle
        d.ellipse([14 * k, 30 * k, 86 * k, 102 * k], fill=INK)
        d.polygon([(50 * k, 9 * k), (17 * k, 54 * k), (83 * k, 54 * k)], fill=INK)
        n = [(20, 52), (26, 52), (36, 66), (36, 52), (42, 52), (42, 74), (36, 74), (26, 60), (26, 74), (20, 74)]
        m = [(47, 52), (53, 52), (60, 63), (67, 52), (73, 52), (73, 74), (67, 74), (67, 62), (60, 72), (53, 62), (53, 74), (47, 74)]
        d.polygon([(x * k, y * k) for x, y in n], fill=OIL)
        d.polygon([(x * k, y * k) for x, y in m], fill=OIL)
        return im.resize((size, size), Image.LANCZOS)

    brand = ROOT / "images/brand"
    brand.mkdir(parents=True, exist_ok=True)
    logo(512).save(brand / "logo-512.png")
    logo(192).save(brand / "icon-192.png")
    logo(180).save(brand / "apple-touch-icon.png")
    logo(48).save(brand / "favicon-48.png")

    og = ROOT / "images/og"
    og.mkdir(parents=True, exist_ok=True)

    def fit_text(draw, text, font_path, max_w, start):
        size = start
        while size > 20:
            ft = ImageFont.truetype(font_path, size)
            if draw.textlength(text, font=ft) <= max_w:
                return ft
            size -= 2
        return ImageFont.truetype(font_path, size)

    def wrap(draw, text, ft, max_w):
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=ft) <= max_w:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        return lines

    def chrome(im, d, compact=False):
        lg = logo(64)
        im.paste(lg, (64, 52), lg)
        d.text((146, 58), "NATIONAL MACHINERY STORES", font=ImageFont.truetype(F_DISP, 20 if compact else 26), fill=PAPER)
        d.text((146, 90), f"KADI · GUJARAT · EST. {SITE['founded']}", font=ImageFont.truetype(F_MONO, 16 if compact else 17), fill=OIL)
        foot = f"WhatsApp {SITE['whatsappDisplay']}" if compact else f"WhatsApp {SITE['whatsappDisplay']}   ·   Call {SITE['phoneDisplay']}"
        d.text((64, 566), foot, font=ImageFont.truetype(F_MONO, 20), fill=MUTED)

    # Home: photo pushed right so the oil stream clears the headline
    hero = Image.open(ROOT / "images/editorial/hero-oil-expeller-1400.webp").convert("RGB")
    hero = hero.resize((1200, int(1200 * hero.height / hero.width)), Image.LANCZOS)
    top = max(0, (hero.height - 630) // 2)
    hero = hero.crop((0, top, 1200, top + 630))
    im = Image.new("RGB", (1200, 630), INK)
    off = 330
    mask = Image.new("L", (1200, 1), 0)
    for x in range(1200):
        mask.putpixel((x, 0), int(max(0, min(255, 255 * (x - 40) / 420))))
    mask = mask.resize((1200, 630))
    layer = Image.new("RGB", (1200, 630), INK)
    layer.paste(hero.crop((0, 0, 1200 - off, 630)), (off, 0))
    im = Image.composite(layer, im, Image.composite(mask, Image.new("L", (1200, 630), 0), Image.new("L", (1200, 630), 255)))
    # fade the photo's left edge into ink
    edge = Image.new("L", (1200, 1), 0)
    for x in range(1200):
        edge.putpixel((x, 0), 255 if x < off else int(max(0, 255 * (1 - (x - off) / 380))))
    im = Image.composite(Image.new("RGB", (1200, 630), INK), im, edge.resize((1200, 630)))
    d = ImageDraw.Draw(im)
    chrome(im, d)
    ft = ImageFont.truetype(F_DISP, 60)
    y = 196
    for ln in ["OIL MILL", "MACHINERY THAT", "KEEPS MILLS"]:
        d.text((64, y), ln, font=ft, fill=PAPER)
        y += 68
    d.text((64, y), "RUNNING.", font=ft, fill=OIL)
    im.save(og / "og-home.jpg", quality=86, optimize=True, progressive=True)

    # Products
    for p in PRODUCTS:
        im = Image.new("RGB", (1200, 630), INK)
        d = ImageDraw.Draw(im)
        panel_x = 700
        ph = Image.open(ROOT / "images/products" / p["images"][0]["src"]).convert("RGB")
        pw, phh = 1200 - panel_x, 630
        if p["images"][0]["fit"] == "contain":
            bg = Image.new("RGB", (pw, phh), (234, 228, 215))
            ph.thumbnail((pw - 60, phh - 60), Image.LANCZOS)
            bg.paste(ph, ((pw - ph.width) // 2, (phh - ph.height) // 2))
            ph = bg
        else:
            r = max(pw / ph.width, phh / ph.height)
            ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
            lx, ty = (ph.width - pw) // 2, (ph.height - phh) // 2
            ph = ph.crop((lx, ty, lx + pw, ty + phh))
        im.paste(ph, (panel_x, 0))
        d.rectangle([panel_x - 4, 0, panel_x, 630], fill=OIL)
        chrome(im, d, compact=True)
        st = STAGES[p["stage"]]
        d.text((64, 176), f"{st['num']} · {st['name'].upper()} STAGE", font=ImageFont.truetype(F_MONO, 20), fill=OIL)
        ft = ImageFont.truetype(F_DISP, 52)
        lines = wrap(d, p["name"].upper(), ft, panel_x - 110)
        if len(lines) > 3:
            ft = ImageFont.truetype(F_DISP, 40)
            lines = wrap(d, p["name"].upper(), ft, panel_x - 110)
        y = 214
        for ln in lines:
            d.text((64, y), ln, font=ft, fill=PAPER)
            y += int(ft.size * 1.08)
        y += 18
        fs = ImageFont.truetype(F_SEMI, 26)
        x = 64
        for s in p["keySpecs"]:
            tw = d.textlength(s, font=fs)
            d.rounded_rectangle([x, y, x + tw + 28, y + 46], radius=4, outline=(80, 84, 90), width=2)
            d.text((x + 14, y + 8), s, font=fs, fill=PAPER)
            x += tw + 44
        im.save(og / f"{p['slug']}.jpg", quality=84, optimize=True, progressive=True)
    print("media: logo PNGs + OG images written")


def main():
    if "--media" in sys.argv:
        build_media()
    (ROOT / "products").mkdir(exist_ok=True)
    for p in PRODUCTS:
        (ROOT / "products" / f"{p['slug']}.html").write_text(product_page(p), encoding="utf-8")
    build_index()
    build_sitemap()
    build_llms()
    print(f"built: {len(PRODUCTS)} product pages, index regions, sitemap.xml, llms.txt (css v{CSS_VER}, js v{JS_VER})")


if __name__ == "__main__":
    main()
