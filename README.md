# National Machinery Stores — Website

Oil mill machinery, oil expellers, filter presses, conveyors and spare parts.
Kadi, Mahesana, Gujarat, India · Est. 1998.

Static site: plain HTML/CSS/JS, no framework, no runtime dependencies. Deploys as-is to Vercel or GitHub Pages.

---

## Structure

```
index.html                    Homepage (hand-written; marked regions are generated)
products/<slug>.html          11 product landing pages (generated — do not hand-edit)
catalogue.html                Printable A4 catalogue (hand-written)
assets/css/site.css           Design system
assets/js/site.js             Menu, product filter, gallery, inquiry form → WhatsApp
data/site.json                Business facts: phones, addresses, hours, stats, testimonials
data/products.json            Products, specs, line stages, FAQ (single source of truth)
images/products/              Real product photos (WebP)
images/editorial/             Atmosphere images (Higgsfield-generated, illustrative only)
images/og/                    WhatsApp / social share cards (generated)
images/brand/                 Logo PNGs (generated)
tools/build.py                Generator
sitemap.xml, llms.txt         Generated
robots.txt, vercel.json, site.webmanifest, favicon.svg
```

## Editing

| Change | Where |
|---|---|
| Phone, WhatsApp, address, hours, stats | `data/site.json`, then `index.html` hero/contact copy |
| Product name, specs, features, photos, SEO title | `data/products.json` |
| FAQ questions | `data/products.json` → `faq`, `homeFaq` |
| Homepage copy (hero, guide, services, about) | `index.html` (outside `@gen` regions) |
| Real client testimonials | `data/site.json` → `testimonials` (section appears automatically) |

After editing `data/*.json` or `tools/build.py`, regenerate:

```bash
python3 tools/build.py            # pages, homepage regions, sitemap, llms.txt
python3 tools/build.py --media    # also logo PNGs + share images (needs: pip install pillow)
```

Anything between `<!-- @gen:NAME -->` and `<!-- /@gen:NAME -->` in `index.html` is overwritten by the build.

Preview locally: `python3 -m http.server 8080` → http://localhost:8080

## Design system — "Nameplate & spec sheet"

| Token | Value | Use |
|---|---|---|
| `--ink` | `#111315` | Cast-iron black: hero, dark sections |
| `--paper` | `#F4F0E7` | Filter-cloth off-white: page background |
| `--oil` | `#E4A51E` | Pressed-oil gold: accent, primary CTA |
| `--oil-deep` | `#855900` | Gold text on light backgrounds (AA contrast) |
| `--wa` | `#0F7A43` | WhatsApp buttons (AA contrast with white) |

Type: **Archivo** (variable width — expanded for headlines) + **JetBrains Mono** (labels, specs).
Signature element: the riveted machine **nameplate** in the hero.

## SEO / AI-search (GEO)

- One indexable page per product with answer-first summary, spec table, FAQ.
- JSON-LD: `LocalBusiness` (+ factory department, geo, hours, contact points, offer catalog), `WebSite`, `WebPage`, `Product`/`Service` with spec `additionalProperty`, `BreadcrumbList`, `FAQPage`.
- Comparison tables (expeller sizing, casting vs PP filter) — the format AI answers cite most.
- `robots.txt` explicitly allows GPTBot, PerplexityBot, ClaudeBot, Google-Extended, Bingbot.
- `llms.txt` summarises the business and every product for LLM crawlers.
- Per-product 1200×630 share images for WhatsApp/LinkedIn link previews.
- `sitemap.xml` with `lastmod`. Update `data/site.json → updated` when content changes.

Canonical domain is set in `data/site.json → baseUrl` (`https://nationalmachinerystores.com`). Change it there and rebuild if the live domain differs.

## Deploy

**Vercel:** import the repo → Deploy. `vercel.json` adds long-cache headers for `/images` and `/assets`.
**GitHub Pages:** Settings → Pages → Deploy from branch `main`, folder `/`.

After first deploy: submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.

## Content rules

- Product photos must be real photos of machines we supply. AI images are used only for atmosphere and are captioned "Illustrative image" where they show work being done.
- Testimonials must be real client quotes used with permission. Do not publish invented reviews.
