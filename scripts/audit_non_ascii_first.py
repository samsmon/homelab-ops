#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

LOSSLESS = Path('/mnt/hdd-backup/music/Lossless')

print("=" * 80)
print("AUDIT: FOLDERS STARTING WITH NON-ASCII (JAPANESE FIRST)")
print("=" * 80)

non_ascii_folders = []
for cat in ['Anime', 'Doujinshi', 'Vtuber', 'Vocaloid', 'J-Pop']:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists():
        continue
    for p in cat_dir.iterdir():
        if not p.is_dir():
            continue
        first_char = p.name[0]
        # check if first char is non-ascii (Japanese CJK, kana, etc.)
        if ord(first_char) >= 128 and first_char not in ['（', '『', '「', '【']:
            non_ascii_folders.append((cat, p.name))

print(f"Total folders starting with non-ASCII: {len(non_ascii_folders)}")
for cat, name in non_ascii_folders[:50]:
    print(f"  [{cat}] {name}")
if len(non_ascii_folders) > 50:
    print(f"  ... and {len(non_ascii_folders) - 50} more")

print("=" * 80)
