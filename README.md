# 🍜 Lihan's Sydney Foodie Guide

A personal collection of 108 restaurants, cafes, and hidden gems across Sydney — with an interactive map, category filters, and suburb search.

**Live site:** https://lihan72.github.io/foodie_sydney

---

## Features

- **108 places** sourced from Google Maps saved list
- **Photo cards** with real ratings, review counts, and addresses (via Google Places API)
- **Category filters** — Japanese, Chinese, Korean, Thai, Vietnamese, Malaysian, Indian, Cafe, Bakery, Tea & Drinks, Western
- **Suburb dropdown** — filter by 27+ Sydney suburbs
- **Mini Sydney map** — Leaflet.js + OpenStreetMap, emoji markers per suburb, syncs with filters
- **Search** — live search by name or address
- **Warm design** — consistent cream/brown theme across landing and list page
- **Mobile responsive**

---

## Project Structure

```
foodie_sydney/
├── index.html       # Landing page (about Lihan + entry to list)
├── list.html        # Main foodie list with map and filters
├── lihan.png        # Illustration used on landing page
├── .nojekyll        # Tells GitHub Pages not to run Jekyll
└── README.md
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Hosting | GitHub Pages (free) |
| Map | Leaflet.js + OpenStreetMap (free, no API key) |
| Place data | Google Places API v1 (one-time fetch, pre-baked into HTML) |
| Photos | Google Places CDN URLs (no API key needed at runtime) |
| Frontend | Vanilla HTML/CSS/JS — no framework, no build step |

---

## How to Add or Update Places

1. Export your Google Maps saved list as CSV (Google Takeout)
2. Run the fetch script (see `skill.md`) to pull data from Google Places API
3. Update `list.html` with the new data
4. Commit and push

```bash
git add list.html
git commit -m "Update places list"
git push
```

---

## Google Places API Key

The API key is used **only during the data-fetch script** — it is **not embedded in any HTML file**.  
Photos are stored as permanent CDN URLs. The map uses OpenStreetMap (no key needed).

Keep the key restricted to your domain in [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

---

## Local Development

Just open the HTML files directly in a browser — no server or build step needed.

```bash
open index.html
open list.html
```

---

*Made with 🍜 and a lot of Google Maps pins*
