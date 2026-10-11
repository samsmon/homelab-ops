#!/usr/bin/env python3
import os
import re
from pathlib import Path

LOSSLESS = Path('/mnt/hdd-backup/music/Lossless')
categories = ['Anime', 'Doujinshi', 'Global', 'J-Pop', 'Vocaloid', 'Vtuber']

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
        reasons = []
        if name.count('(') > 1:
            reasons.append("multiple_parens")
        if any(bad in name for bad in ['(hosi)', 'cv_', 'cv :', 'cv.', 'Akunaitsu', 'Porupurinsesu', 'Howaitoarubamu', 'sakai Junna']):
            reasons.append("kakasi_or_cv_artifact")
        if name.startswith(' ') or name.endswith('  ~'):
            reasons.append("spacing_glitch")
        if not name.endswith('~'):
            reasons.append("missing_tilde")
        if reasons:
            deformed.append((cat, name, reasons))

print(f"Total deformed/suspicious folders: {len(deformed)}")
for cat, name, reasons in deformed:
    print(f"  [{cat}] {name}  -->  {reasons}")

print("\n--- 2. CROSS-CATEGORY DUPLICATE ARTISTS ---")
artist_map = {}
for cat in categories:
    cat_path = LOSSLESS / cat
    if not cat_path.exists():
        continue
    for p in cat_path.iterdir():
        if not p.is_dir():
            continue
        clean_name = p.name.strip('~').strip().lower()
        base_name = re.sub(r'\(.*?\)', '', clean_name).strip()
        if not base_name:
            base_name = clean_name
        artist_map.setdefault(base_name, []).append((cat, p.name))

cross_dups = {k: v for k, v in artist_map.items() if len(v) > 1}
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
