#!/usr/bin/env python3
import os

BASE = '/mnt/hdd-backup/music/Lossless/Vtuber'
folders = sorted(os.listdir(BASE))

print(f"=== ALL {len(folders)} FOLDERS IN /mnt/hdd-backup/music/Lossless/Vtuber ===")
for i, f in enumerate(folders, 1):
    fp = os.path.join(BASE, f)
    if os.path.isdir(fp):
        subdirs = [d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp, d))]
        print(f"{i:02d}. {f} ({len(subdirs)} subdirs)")
    else:
        print(f"{i:02d}. [FILE] {f}")
