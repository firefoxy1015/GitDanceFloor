# Shenli Mining Machinery — Interactive Catalog

An interactive English-language web version of the **Hebei Shenli Pneumatic
Machinery Co., Ltd. 2025** product brochure.

## Run

The catalog is a static site — no build step. Open `index.html` directly, or
serve the folder with any static server:

```bash
cd interactive-catalog
python3 -m http.server 8080
# then visit http://localhost:8080
```

## Structure

```
interactive-catalog/
  index.html       # Page shell, hero, about, footer, modals
  styles.css       # Dark industrial theme, responsive layout
  app.js           # Renders the gallery and handles drawer / modal state
  data.js          # All product data (categories, specs, descriptions)
  images/          # Hero, category and per-product images extracted from the PDF
```

## How it works

* The home page shows a hero, "About us" intro, and a six-card category gallery.
* Clicking a category opens a right-hand drawer listing the products in that range.
* Clicking a product opens a modal with photo, description, highlights, and a
  full specification table.
* The URL hash (e.g. `#rockdrill`) deep-links to a category drawer.
* Press `Esc` or click the backdrop to close.

## Product families

1. **S250 Pneumatic Rock Drill** — flagship Secoroc 250 air-leg drill
2. **Pneumatic Rock Drills** — Y018, Y19A, Y24, Y26, TY24C, YT29A, YT28, YT27, S82, YT24, S83, YN27C
3. **Pneumatic Breakers & Air Picks** — SK10, G10, TCA-7, TCD-20, B37, B47, B67C, BB7C, TPB-40/60/90, RB777
4. **Drill Bits & Drill Rods** — 4/5/6/7-button bits, cross / horse-type bits, H22/B22 tapered rods
5. **Air Compressors** — LGCY, LGY, KSCY, KSDY, BK / Piston
6. **Mining Electric Tricycles** — 1 T, 2 T, 3 T, 4 T zero-emission ore handlers
