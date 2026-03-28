# National Machinery Stores — Official Website

> **Live Business Website** for National Machinery Stores, Mahesana GIDC, Gujarat, India.  
> Oil Mill Machinery · Oil Expellers · Screw Conveyors · Conveyor Belts · Filters · Spare Parts

---

## 🌐 Live Site

**Deploy URL:** `https://nationalmachinerystores.vercel.app` *(update after deployment)*

---

## 🏭 About the Business

**National Machinery Stores**  
**Owner:** Mr. Iqbalhusen B Chishti  
**Address:** 12, Someshwar Complex, Opp. Pashupati Ginning, Nandasan Highway, Mahesana GIDC – 382715, Gujarat, India  
**Phone / WhatsApp:** +91 88666 88626  
**Est.:** 1998 | **Clients:** 500+ | **States Served:** 18+

Manufacturer · Exporter · Supplier · Service Provider of Oil Mill Machinery and Industrial Equipment across India.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Markup | HTML5 |
| Styling | Tailwind CSS (CDN) |
| Scripting | Vanilla JavaScript (ES6) |
| Fonts | Google Fonts — Barlow Condensed, Barlow, DM Sans |
| Deployment | Vercel / GitHub Pages |
| Backend | None — zero-dependency static site |

**Single file architecture** — the entire website lives in `index.html`. No build step, no npm, no dependencies to install.

---

## 📁 Repository Structure

```
nationalmachinerystores/
│
├── index.html          ← Complete website (single file)
└── README.md           ← This file
```

---

## 🚀 Deployment

### Option 1 — Vercel (Recommended)

1. Push this repository to GitHub
2. Go to [vercel.com](https://vercel.com) → **Add New Project**
3. Import your GitHub repository
4. Vercel auto-detects static HTML — click **Deploy**
5. Done. Live in under 60 seconds.

No `vercel.json` config needed. Vercel serves `index.html` automatically.

### Option 2 — GitHub Pages

1. Go to your repository → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` | Folder: `/ (root)`
4. Click **Save**
5. Your site will be live at `https://yourusername.github.io/repo-name/`

---

## 🛠️ Local Development

No build tools required. Just open the file:

```bash
# Clone the repository
git clone https://github.com/yourusername/nationalmachinerystores.git

# Open directly in browser
open index.html

# OR serve locally with Python (optional, for testing)
cd nationalmachinerystores
python3 -m http.server 8080
# Visit: http://localhost:8080
```

---

## ✏️ How to Update Content

Since the entire site is a single HTML file, all edits are straightforward.

### Update Phone Number
Search for `+918866688626` and `88666 88626` — replace all instances with the new number.

### Update Address
Search for `Someshwar Complex` — update the address block wherever it appears.

### Update Owner Name
Search for `Iqbalhusen B Chishti` — replace all instances.

### Update WhatsApp Number
Search for `wa.me/918866688626` — replace the number in all `href` attributes.

### Add / Edit a Product Card
Each product card is a `<div class="pc rv">` block inside the products grid section. Copy an existing card and update the:
- `onclick="openModal('key')"` — product key
- `<img src="...">` — product image URL
- `<h3>` — product name
- `<p>` — short description

### Add / Edit Product Modal Data
In the `<script>` block at the bottom, find the `const PRODUCTS = { ... }` object. Each key (e.g. `moe`, `hce`, `sc`) maps to a product. Update or add entries following the same structure:

```javascript
your_key: {
  title: 'Product Name',
  badge: 'Badge Text',        // or '' for no badge
  badgeClass: 'pb-am',        // pb-am (amber) | pb-gn (green) | pb-bl (blue)
  img: 'https://image-url',
  imgAlt: 'Image alt text',
  desc: 'Product description paragraph.',
  features: [
    'Feature one',
    'Feature two',
    // ...
  ],
  specs: [
    ['Spec Label', 'Spec Value'],
    // ...
  ],
  apps: 'Applications text.'
}
```

### Change Contact Number / WhatsApp Pre-fill Message
Search for `wa.me/918866688626?text=` to find all WhatsApp links and update the pre-filled message text after `text=`.

---

## 🎨 Design System

| Token | Value | Usage |
|---|---|---|
| `--navy` | `#0d1f3c` | Primary background, headings |
| `--steel` | `#1e3a5f` | Secondary navy, gradients |
| `--amber` | `#f59e0b` | Accent colour, CTAs, highlights |
| `--amber-hot` | `#d97706` | CTA hover state |
| `--smoke` | `#f0f4f8` | Light section backgrounds |
| `--muted` | `#5a6a80` | Body text, descriptions |

**Fonts:**
- `Barlow Condensed` — headings, section titles, buttons
- `Barlow` — nav links, labels, UI text
- `DM Sans` — body text, paragraphs, form inputs

---

## 📋 Features Checklist

- [x] Fully responsive — mobile, tablet, desktop
- [x] Sticky WhatsApp floating button (pulsing animation)
- [x] Sticky Call floating button
- [x] Urgency top bar with phone number
- [x] Scroll-aware navbar (transparent → solid on scroll)
- [x] Mobile hamburger menu
- [x] Hero section with 3 CTAs
- [x] Stats bar (25+ years, 500+ clients, 11 products, 18+ states)
- [x] Complete 11-product catalogue with real images
- [x] Product detail modals (specs, features, applications)
- [x] Mid-page quick inquiry form
- [x] Full contact section with detailed inquiry form
- [x] Form → WhatsApp redirect (zero-backend lead capture)
- [x] Why Choose Us section
- [x] About Us with timeline
- [x] Industries We Serve section
- [x] Client testimonials
- [x] 8-question FAQ accordion
- [x] Google Maps embed
- [x] Footer with product and quick links
- [x] SEO meta tags (title, description, keywords, canonical)
- [x] Open Graph tags
- [x] Schema.org LocalBusiness JSON-LD
- [x] H1/H2/H3 heading structure with target keywords
- [x] Real product images from ExportersIndia catalogue
- [x] Real business details (owner, address, phone)

---

## 🔍 SEO Keywords Targeted

- Oil Expeller Manufacturer Gujarat
- Mini Oil Expeller Mahesana
- High Capacity Oil Expeller Gujarat
- Oil Mill Machinery Supplier India
- Screw Conveyor Manufacturer Kadi
- Conveyor Belt Supplier Mehasana
- Casting Oil Filter Gujarat
- Plastic Oil Filter Hydraulic
- Vassal Oil Neutralizer Supplier
- Radler Chain Oil Mill India
- Oil Expeller Spare Parts India
- Oil Mill Erector Service Gujarat

---

## 📞 Support / Contact

For website updates or technical queries, contact the site administrator.

For business inquiries, contact **Mr. Iqbalhusen B Chishti** directly:

- 📞 **Call:** [+91 88666 88626](tel:+918866688626)
- 💬 **WhatsApp:** [wa.me/918866688626](https://wa.me/918866688626)
- 📍 **Address:** 12, Someshwar Complex, Opp. Pashupati Ginning, Nandasan Highway, Mahesana GIDC – 382715, Gujarat, India

---

*Built for National Machinery Stores · Mahesana GIDC, Gujarat, India*
