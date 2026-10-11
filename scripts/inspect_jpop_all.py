#!/usr/bin/env python3
import os

BASE = '/mnt/hdd-backup/music/Lossless/J-Pop'
folders = sorted(os.listdir(BASE))

print(f"=== ALL {len(folders)} FOLDERS IN /mnt/hdd-backup/music/Lossless/J-Pop ===")
for i, f in enumerate(folders, 1):
    fp = os.path.join(BASE, f)
    if os.path.isdir(fp):
        subdirs = [d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp, d))]
        # print if it looks suspicious (e.g. Hololive, Nijisanji, Anime, Game, Vocaloid, Doujin)
        # or every 10th
        print(f"{i:03d}. {f} ({len(subdirs)} subdirs)")
    else:
        print(f"{i:03d}. [FILE] {f}")
