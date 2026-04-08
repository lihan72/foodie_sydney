"""
fetch_websites.py
-----------------
Enriches data/places.json with website URLs from Google Places API.
Extracts place IDs from existing mapsUrl field — no re-searching needed.

Run once, then commit data/places.json.

Usage:
    cd foodie_sydney
    python scripts/fetch_websites.py

Requirements:
    - API key restriction temporarily set to "None"
    - Re-restrict to https://lihan72.github.io/* after done
"""

import json
import time
import urllib.request
import urllib.error
import re

API_KEY = "AIzaSyCOktI5Dwmq0PYQ2wPzHs1rfHGMRxCPN4I"
DATA_FILE = "data/places.json"


def get_place_id(maps_url):
    m = re.search(r'place_id:([A-Za-z0-9_-]+)', maps_url)
    return m.group(1) if m else None


def fetch_website(place_id):
    req = urllib.request.Request(
        f"https://places.googleapis.com/v1/places/{place_id}",
        headers={
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "websiteUri",
        }
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    return data.get("websiteUri")


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        places = json.load(f)

    updated = 0
    for i, p in enumerate(places):
        place_id = get_place_id(p.get("mapsUrl", ""))
        if not place_id:
            print(f"[{i+1}] {p['name']} — no place ID, skipping")
            continue

        # Skip if already has a website
        if p.get("website"):
            print(f"[{i+1}] {p['name']} — already has website, skipping")
            continue

        try:
            website = fetch_website(place_id)
            p["website"] = website
            status = website if website else "no website"
            print(f"[{i+1}] {p['name']} → {status}")
            if website:
                updated += 1
        except Exception as e:
            print(f"[{i+1}] {p['name']} — error: {e}")
            p["website"] = None

        time.sleep(0.12)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(places, f, ensure_ascii=False, indent=2)

    print(f"\nDone. {updated} websites found. Updated {DATA_FILE}")
    print("Now commit and push data/places.json to deploy.")


if __name__ == "__main__":
    main()
