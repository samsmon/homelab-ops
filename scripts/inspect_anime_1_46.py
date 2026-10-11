#!/usr/bin/env python3
import os

BASE = '/mnt/hdd-backup/music/Lossless/Anime'
folders = sorted(os.listdir(BASE))

print(f"=== ANIME FOLDERS 1 to 46 ===")
for i in range(min(46, len(folders))):
    f = folders[i]
    fp = os.path.join(BASE, f)
    subdirs = [d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp, d))]
    print(f"{i+1:02d}. {f} ({len(subdirs)} subdirs)")
    for s in subdirs[:2]:
        print(f"     * {s}")
