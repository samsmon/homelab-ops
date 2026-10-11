#!/usr/bin/env python3
import os
import re
import json

TORRENT_DONE = "/mnt/hdd-backup/music/Torrent/done"
LOSSLESS_ROOT = "/mnt/hdd-backup/music/Lossless"

print("--- AUDITING TORRENT/DONE AGAINST LOSSLESS LIBRARY ---")

items = os.listdir(TORRENT_DONE)
print(f"Total items in Torrent/done: {len(items)}")

loose_files = []
album_dirs = []

for item in items:
    full = os.path.join(TORRENT_DONE, item)
    if os.path.isfile(full):
        loose_files.append(item)
    elif os.path.isdir(full):
        album_dirs.append(item)

print(f"Loose files in root: {len(loose_files)}")
print(f"Album directories: {len(album_dirs)}")

# Build an index of existing albums in Lossless
lossless_albums = set()
for root, dirs, files in os.walk(LOSSLESS_ROOT):
    for d in dirs:
        lossless_albums.add(d.lower())

already_in_library = []
not_in_library = []

for album in album_dirs:
    album_clean = album.lower().strip()
    # Check exact match
    if album_clean in lossless_albums:
        already_in_library.append(album)
    else:
        # Check fuzzy match by keywords or date
        date_m = re.match(r'\[(\d{4}\.\d{2}\.\d{2})\]', album)
        matched = False
        if date_m:
            dt = date_m.group(1)
            # Find if any album in lossless has this date and some words
            words = set(re.findall(r'[\w]+', album_clean))
            words.discard(dt.replace('.', ''))
            for la in lossless_albums:
                if dt in la:
                    la_words = set(re.findall(r'[\w]+', la))
                    common = words.intersection(la_words)
                    if len(common) >= 2:
                        matched = True
                        break
        if matched:
            already_in_library.append(album)
        else:
            not_in_library.append(album)

print(f"\nAlready in Lossless Library: {len(already_in_library)}")
print(f"NOT in Lossless Library (Genuinely New): {len(not_in_library)}")

report = {
    "total_items": len(items),
    "loose_files": loose_files,
    "already_in_library": sorted(already_in_library),
    "not_in_library": sorted(not_in_library)
}

with open("/tmp/torrent_audit_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("\n--- SAMPLE NEW ALBUMS (NOT IN LIBRARY YET) ---")
for a in not_in_library[:25]:
    print(" -", a)

print("\n--- SAMPLE ALREADY IN LIBRARY (CAN BE RECLAIMED / SEEDED) ---")
for a in already_in_library[:15]:
    print(" -", a)
