# Skill: Lihan's Sydney Foodie Guide — Maintain & Extend

> Personal reference for Lihan.  
> Repo: https://github.com/lihan72/foodie_sydney  
> Live: https://lihan72.github.io/foodie_sydney

---

## Project Structure

```
foodie_sydney/
├── index.html            # Landing page (about Lihan)
├── list.html             # Main list: cards + map + filters (loads data via fetch)
├── lihan.png             # Illustration on landing page
├── .nojekyll             # Prevents GitHub Pages running Jekyll
├── .gitignore            # Excludes input/*.csv and input/*.json
├── README.md
├── data/
│   └── places.json       # ✅ Committed — public place data loaded by list.html
├── input/                # Local only — NOT committed to git
│   ├── places.csv        # Google Takeout export (your source)
│   └── places_enriched.json  # Output from fetch_places.py
└── scripts/
    ├── fetch_places.py   # Fetch details + CDN photos from Google Places API
    ├── inject_places.py  # Copy places_enriched.json → data/places.json
    └── remove_place.py   # Remove a place from data/places.json by name
```

> **Local testing:** `list.html` uses `fetch()` so it won't work from `file://`.  
> Run a local server instead:
> ```bash
> cd foodie_sydney && python3 -m http.server 8000
> # open http://localhost:8000/list.html
> ```

---

## Quick Reference: Common Tasks

### Add new places
```bash
# 1. Export latest CSV from Google Takeout → save to input/places.csv
# 2. Temporarily remove API key restriction in Google Cloud Console
# 3. Fetch place details + CDN photos
python scripts/fetch_places.py        # → writes input/places_enriched.json
# 4. Copy to public data file
python scripts/inject_places.py       # → writes data/places.json
# 5. Re-restrict API key to https://lihan72.github.io/*
# 6. If new suburb, add coords to SUBURB_COORDS in list.html
# 7. Deploy
git add data/places.json list.html
git commit -m "Add new places"
git push
```

### Remove a place
```bash
python scripts/remove_place.py "Place Name"
```

### Deploy changes
```bash
# Quick (solo use) — temporarily disable branch protection first:
# Repo → Settings → Branches → Edit → uncheck "Require PR" → Save
git add list.html index.html
git commit -m "Update: describe what changed"
git push
# Re-enable branch protection after. GitHub Pages auto-deploys in ~1 min.
```

---

## Pending Tasks

- [ ] Merge `add-readme` PR — branch `add-readme` is open on GitHub
  - Steps: Settings → Branches → Edit → uncheck "Require PR" → merge PR → re-enable

---

## API Key Management

- Key lives **only in `scripts/fetch_places.py`** — never in any HTML file
- After fetching: restrict key to `https://lihan72.github.io/*` in Google Cloud Console
- Before fetching: temporarily set restriction to "None"
- Monthly cost: well under $1 for ~100 place fetches

---

## Categories & Emojis

```javascript
japanese: "🍜",  chinese: "🥢",   korean: "🥩",
thai: "🌶️",     vietnamese: "🥖", malaysian: "🍛",
indian: "🫓",   cafe: "☕",       bakery: "🥐",
tea: "🧋",      western: "🍽️"
```

---

## Suburb Coordinates (add new ones to SUBURB_COORDS in list.html)

```javascript
"Alexandria": [-33.909, 151.197], "Artarmon": [-33.819, 151.189],
"Barangaroo": [-33.862, 151.200], "Botany": [-33.944, 151.202],
"Burwood": [-33.877, 151.104],    "Cabramatta": [-33.894, 150.939],
"Chatswood": [-33.797, 151.182],  "Chippendale": [-33.889, 151.198],
"Crows Nest": [-33.827, 151.200], "Darling Harbour": [-33.873, 151.199],
"Darlinghurst": [-33.876, 151.219],"Eastwood": [-33.790, 151.081],
"Erskineville": [-33.900, 151.185],"Glebe": [-33.880, 151.186],
"Haymarket": [-33.880, 151.204],  "Mascot": [-33.927, 151.191],
"Neutral Bay": [-33.834, 151.221],"Newtown": [-33.897, 151.177],
"North Sydney": [-33.840, 151.207],"Potts Point": [-33.870, 151.226],
"Redfern": [-33.893, 151.201],    "St Leonards": [-33.822, 151.195],
"Surry Hills": [-33.885, 151.212],"Sydney": [-33.869, 151.207],
"The Rocks": [-33.860, 151.208],  "Ultimo": [-33.881, 151.197],
"Waterloo": [-33.897, 151.202],   "Zetland": [-33.911, 151.207],
```

---

## Common Issues & Fixes

| Problem | Cause | Fix |
|---|---|---|
| Photos not loading | API key restricted | CDN URLs don't need key — remove restriction only for script runs |
| Places API 403 | Referrer restriction active during script run | Set restriction to "None" while running fetch script |
| All places disappear | JS temporal dead zone (`let` declared after `render()`) | Move `let leafletMap` and `let mapMarkers` above init calls |
| Wrong place returned | Search query too generic | Add suburb name to query in `fetch_places.py` |
| Map tiles not loading | No internet | Leaflet needs internet for OpenStreetMap tiles |
| GitHub Pages 404 | Jekyll processing | Ensure `.nojekyll` file exists in repo root |
| Can't push directly | Branch protection ON | Disable "Require PR" in Settings → Branches, push, re-enable |
| Can't approve own PR | GitHub policy | Owner can't self-approve — disable protection and merge directly |

---

## Key Technical Notes

**Photo CDN trick:** Resolve `lh3.googleusercontent.com` URLs at fetch time by following the Places API photo redirect. These permanent URLs need no API key — safe to embed in public HTML.

**Suburb extraction regex:**
```javascript
addr.match(/,\s*([^,]+?)\s+NSW\s+\d/)  // matches suburb before "NSW postcode"
```

**JS init order (critical):**
```javascript
// These MUST be declared before render() is called
let leafletMap = null;
let mapMarkers = {};
buildFilters(); buildSuburbSelect(); render();
```

**Place data shape in `const ALL`:**
```javascript
{ name, cat, address, rating, ratingCount, priceLevel, photo, mapsUrl }
```

---

## Future Ideas

- [ ] Add a "visited / want to go" toggle per place
- [ ] Star/favourite individual places
- [ ] Add more cities (Melbourne, Brisbane)
- [ ] Dark mode
- [ ] Share button per place
