"""
fetch_places.py
---------------
Reads input/places.csv (exported from Google Takeout),
fetches details + CDN photo URLs from Google Places API v1,
and writes output to input/places_enriched.json.

Usage:
    cd foodie_sydney
    python scripts/fetch_places.py

Requirements:
    - API key with Places API (New) enabled
    - Key restriction temporarily set to "None" while running
    - Re-restrict to https://lihan72.github.io/* after done
"""

import csv
import json
import time
import urllib.request
import urllib.error
import urllib.parse

# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY = "YOUR_API_KEY_HERE"
INPUT_CSV = "input/places.csv"
OUTPUT_JSON = "input/places_enriched.json"

SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

PRICE_MAP = {
    "PRICE_LEVEL_FREE": 0,
    "PRICE_LEVEL_INEXPENSIVE": 1,
    "PRICE_LEVEL_MODERATE": 2,
    "PRICE_LEVEL_EXPENSIVE": 3,
    "PRICE_LEVEL_VERY_EXPENSIVE": 4,
}

# Map your Google Maps tags to site categories
TAG_TO_CAT = {
    "Japanese": "japanese",
    "Chinese": "chinese",
    "Korean": "korean",
    "Thai": "thai",
    "Vietnamese": "vietnamese",
    "Malaysian": "malaysian",
    "Indian": "indian",
    "Cafe": "cafe",
    "Bakery": "bakery",
    "Tea": "tea",
    "Western": "western",
}


# ── API HELPERS ──────────────────────────────────────────────────────────────

def search_place(name):
    """Return the Place ID for a given name."""
    body = json.dumps({"textQuery": name + " Sydney", "languageCode": "en"}).encode()
    req = urllib.request.Request(SEARCH_URL, data=body, headers={
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName",
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    return data.get("places", [{}])[0].get("id")


def get_details(place_id):
    """Fetch rating, address, price level, and photo references."""
    req = urllib.request.Request(
        f"https://places.googleapis.com/v1/places/{place_id}",
        headers={
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "displayName,rating,userRatingCount,formattedAddress,priceLevel,photos",
        }
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def resolve_photo_cdn(photo_name):
    """Follow the Places photo redirect to get a permanent CDN URL (no key needed at runtime)."""
    url = f"https://places.googleapis.com/v1/{photo_name}/media?maxWidthPx=600&key={API_KEY}"

    class StopRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)

    opener = urllib.request.build_opener(StopRedirect())
    try:
        opener.open(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}))
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307, 308):
            return e.headers.get("Location")
    return None


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    with open(INPUT_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    results = []
    for i, row in enumerate(rows):
        name = row.get("Title", "").strip()
        tag = row.get("Tags", "").strip()
        cat = TAG_TO_CAT.get(tag, "western")

        print(f"[{i+1}/{len(rows)}] {name}")

        try:
            place_id = search_place(name)
            if not place_id:
                print(f"  ✗ Not found")
                continue

            details = get_details(place_id)
            address = details.get("formattedAddress", "")
            rating = details.get("rating")
            rating_count = details.get("userRatingCount")
            price_raw = details.get("priceLevel")
            price = PRICE_MAP.get(price_raw)

            photo_url = None
            photos = details.get("photos", [])
            if photos:
                photo_url = resolve_photo_cdn(photos[0]["name"])

            maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

            results.append({
                "name": name,
                "cat": cat,
                "address": address,
                "rating": rating,
                "ratingCount": rating_count,
                "priceLevel": price,
                "photo": photo_url,
                "mapsUrl": maps_url,
            })
            print(f"  ✓ {address} | ★{rating} | photo: {'yes' if photo_url else 'no'}")

        except Exception as e:
            print(f"  ✗ Error: {e}")

        time.sleep(0.12)  # stay under rate limit

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nDone. {len(results)}/{len(rows)} places saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
