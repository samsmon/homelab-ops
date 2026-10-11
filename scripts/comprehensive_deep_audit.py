#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

LOSSLESS = Path('/mnt/hdd-backup/music/Lossless')

print("=" * 80)
print("COMPREHENSIVE DEEP AUDIT OF ALL CATEGORIES IN LOSSLESS")
print("=" * 80)

categories = ['Anime', 'Doujinshi', 'Global', 'J-Pop', 'Vocaloid', 'Vtuber']

# 1. Check deformed folder names
print("\n--- 1. DEFORMED / SUSPICIOUS FOLDER NAMES ---")
deformed = []
for cat in categories:
    cat_path = LOSSLESS / cat
    if not cat_path.exists():
        continue
    for p in cat_path.iterdir():
        if not p.is_dir():
            continue
        name = p.name
        # Check patterns
        is_deformed = False
        reasons = []
        if name.count('(') > 1:
            reasons.append("multiple_parens")
        if any(bad in name for bad in ['(hosi)', 'cv_', 'cv :', 'cv.', 'Akunaitsu', 'Porupurinsesu', 'Howaitoarubamu', 'sakai Junna']):
            reasons.append("kakasi_or_cv_artifact")
        if name.endswith(') ~') and not re.search(r'^[A-Za-z0-9\s\.\'\-&!?#@+*,_~]+ \(.*\)\s*~?$', name):
            # starts with non-ascii before paren?
            pass
        if name.startswith(' ') or name.endswith('  ~'):
            reasons.append("spacing_glitch")
        if not name.endswith('~'):
            reasons.append("missing_tilde")
        if reasons:
            deformed.append((cat, name, reasons))

print(f"Total deformed/suspicious folders: {len(deformed)}")
for cat, name, reasons in deformed:
    print(f"  [{cat}] {name}  -->  {reasons}")

# 2. Check for Cross-Category Duplicates (same artist name across categories)
print("\n--- 2. CROSS-CATEGORY DUPLICATE ARTISTS ---")
artist_map = {}
for cat in categories:
    cat_path = LOSSLESS / cat
    if not cat_path.exists():
        continue
    for p in cat_path.iterdir():
        if not p.is_dir():
            continue
        # normalize: strip ~ and lower
        clean_name = p.name.strip('~').strip().lower()
        # strip parens for fuzzy match
        base_name = re.sub(r'\(.*?\)', '', clean_name).strip()
        if not base_name:
            base_name = clean_name
        artist_map.setdefault(base_name, []).append((cat, p.name))

cross_dups = {k: v for k, v in artist_map.items() if len(v) > 1}
# filter out if all are in same category
cross_cat_dups = {}
for k, v in cross_dups.items():
    cats_present = set(c for c, n in v)
    if len(cats_present) > 1:
        cross_cat_dups[k] = v

print(f"Total cross-category split artists: {len(cross_cat_dups)}")
for k, v in sorted(cross_cat_dups.items()):
    print(f"  Artist '{k}':")
    for c, n in v:
        print(f"    - [{c}] {n}")

# 3. Audit all folders in Anime/ to classify: Real Anime/Franchise vs Game vs J-Pop Artist vs Vocaloid
print("\n--- 3. DETAILED AUDIT OF ANIME/ FOLDERS ---")
anime_path = LOSSLESS / 'Anime'
anime_folders = sorted([p for p in anime_path.iterdir() if p.is_dir()])
print(f"Total folders in Anime/: {len(anime_folders)}")

for p in anime_folders:
    subdirs = [s for s in p.iterdir() if s.is_dir()]
    files = [f for f in p.iterdir() if f.is_file()]
    # check if it's a known game
    name = p.name
    note = ""
    if any(g in name.lower() for g in ['blue protocol', 'arknights', 'azur lane', 'blue archive', 'heaven burns red', 'hoyoverse', 'wuthering waves', 'sega', 'ongeki', 'battle girl', 'towatsugai', 'mementomori', 'white album', 'project sekai']):
        note = "[GAME / MULTIMEDIA]"
    elif len(subdirs) <= 1:
        note = f"[POTENTIAL SINGLE/ARTIST - {len(subdirs)} subdirs]"
    print(f"  {name} (subdirs: {len(subdirs)}) {note}")

# 4. Check for Anime/Character Song infiltrations in J-Pop
print("\n--- 4. CHARACTER / ANIME SONGS IN J-POP ---")
jpop_path = LOSSLESS / 'J-Pop'
jpop_infiltrations = []
keywords = ['(cv', 'cv.', 'cv_', 'character', 'soundtrack', 'ost', 'anime', 'animation', 'idolmaster', 'denonbu', 'utanome', 'milgram', 'imarine', 'd4dj', 'bandori', 'love live']
for p in jpop_path.iterdir():
    if not p.is_dir():
        continue
    name_lower = p.name.lower()
    if any(k in name_lower for k in keywords):
        jpop_infiltrations.append(p.name)

print(f"Total suspected anime/character song folders in J-Pop: {len(jpop_infiltrations)}")
for n in jpop_infiltrations:
    print(f"  {n}")

# 5. Check for VTubers in J-Pop / Anime
print("\n--- 5. SUSPECTED VTUBERS IN J-POP OR ANIME ---")
vtuber_keywords = ['hololive', 'nijisanji', 'vspo', 'kamitsubaki', 'riot music', 'rk music', 'neoporte', '774inc', 'nanashi', 're:acT', 'brave group', 'aogiri']
for cat in ['J-Pop', 'Anime']:
    cat_p = LOSSLESS / cat
    for p in cat_p.iterdir():
        if not p.is_dir():
            continue
        n_lower = p.name.lower()
        if any(k in n_lower for k in vtuber_keywords):
            print(f"  [{cat}] {p.name}")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
