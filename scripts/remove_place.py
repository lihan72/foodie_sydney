"""
remove_place.py
---------------
Remove a place from data/places.json by name.
After running, commit and push data/places.json to deploy.

Usage:
    cd foodie_sydney
    python scripts/remove_place.py "Place Name"
"""

import json
import sys

DATA_FILE = "data/places.json"


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/remove_place.py \"Place Name\"")
        sys.exit(1)

    target = sys.argv[1].strip().lower()

    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    before = len(data)
    data = [p for p in data if target not in p["name"].lower()]
    after = len(data)

    if before == after:
        print(f"No place matching '{sys.argv[1]}' found.")
        sys.exit(1)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Removed {before - after} place(s). {after} places remain in {DATA_FILE}")
    print("Now commit and push data/places.json to deploy.")


if __name__ == "__main__":
    main()
