"""
find_instagram.py
-----------------
Searches Google for Instagram handles for places that have no website.
Prints results for you to review — does NOT auto-save.
Once you've confirmed the handles, run with --save to update data/places.json.

Usage:
    cd foodie_sydney
    python scripts/find_instagram.py          # dry run — prints results
    python scripts/find_instagram.py --save   # saves confirmed handles
"""

import json
import re
import sys
import time
import urllib.request
import urllib.parse

DATA_FILE = "data/places.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def search_instagram(name):
    """Search Google for an Instagram handle for this place."""
    query = urllib.parse.quote(f'"{name}" sydney instagram')
    url = f"https://www.google.com/search?q={query}&num=5"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None, str(e)

    # Extract all instagram.com/handle patterns (exclude reels, p/, explore/, etc.)
    handles = re.findall(r'instagram\.com/([A-Za-z0-9_.]{3,30})(?:[/"?]|\\u)', html)
    # Filter out generic Instagram pages
    ignore = {"p", "reel", "reels", "explore", "stories", "accounts", "about",
              "legal", "privacy", "help", "directory", "hashtag", "shoppingtag"}
    handles = [h for h in handles if h.lower() not in ignore]

    # Return most common handle
    if not handles:
        return None, "not found"
    from collections import Counter
    best = Counter(handles).most_common(1)[0][0]
    return best, None


def main():
    save_mode = "--save" in sys.argv

    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    targets = [p for p in data if not p.get("website") and not p.get("instagram")]
    print(f"Searching Instagram for {len(targets)} places without a website...\n")

    found = {}
    for i, p in enumerate(targets):
        handle, err = search_instagram(p["name"])
        if handle:
            print(f"[{i+1}] {p['name']}\n     → instagram.com/{handle}")
            found[p["name"]] = handle
        else:
            print(f"[{i+1}] {p['name']}\n     → {err}")
        time.sleep(1.5)  # be polite to Google

    print(f"\n--- Found {len(found)}/{len(targets)} handles ---")

    if save_mode and found:
        for p in data:
            if p["name"] in found:
                p["instagram"] = found[p["name"]]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved to {DATA_FILE}")
        print("Review data/places.json, fix any wrong handles, then commit and push.")
    elif found:
        print("\nRun with --save to write these to data/places.json")
        print("Or manually add \"instagram\": \"handle\" to entries in data/places.json")


if __name__ == "__main__":
    main()
