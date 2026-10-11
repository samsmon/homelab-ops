#!/usr/bin/env python3
import os
import re

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=" * 80)
print("SEARCHING FOR DUPLICATE / NEAR-DUPLICATE ALBUMS WITHIN ARTISTS")
print("=" * 80)

def normalize_name(s):
    # remove brackets, years, catalog numbers, spaces, punctuation
    s = re.sub(r'[\(\[\{].*?[\)\]\}]', '', s)
    s = re.sub(r'[^\w\s]', '', s)
    return s.strip().lower()

duplicate_candidates = []

for cat in ["Anime", "Doujinshi", "Game", "Global", "J-Pop", "Vocaloid", "Vtuber"]:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for artist in sorted(os.listdir(cat_dir)):
        artist_dir = os.path.join(cat_dir, artist)
        if not os.path.isdir(artist_dir):
            continue
        albums = [d for d in os.listdir(artist_dir) if os.path.isdir(os.path.join(artist_dir, d))]
        seen = {}
        for alb in albums:
            norm = normalize_name(alb)
            if not norm:
                continue
            if norm in seen:
                duplicate_candidates.append((cat, artist, seen[norm], alb))
            else:
                seen[norm] = alb

print(f"Total potential duplicate albums found: {len(duplicate_candidates)}")
for cat, artist, alb1, alb2 in duplicate_candidates:
    print(f"  [{cat}] {artist}:")
    print(f"      1: {alb1}")
    print(f"      2: {alb2}")
