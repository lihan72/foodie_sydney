"""
inject_places.py
----------------
Reads input/places_enriched.json and writes it to data/places.json
(the file served by GitHub Pages and loaded by list.html via fetch).

Run this after fetch_places.py to update the live site data.

Usage:
    cd foodie_sydney
    python scripts/inject_places.py
"""

import json
import os

INPUT_JSON = "input/places_enriched.json"
OUTPUT_JSON = "data/places.json"


def main():
    with open(INPUT_JSON, encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Written {len(data)} places to {OUTPUT_JSON}")
    print("Now commit and push data/places.json to deploy.")


if __name__ == "__main__":
    main()
