#!/usr/bin/env python3
import os

BASE = '/mnt/hdd-backup/music/Lossless/J-Pop'
folders = sorted(os.listdir(BASE))

print(f"=== J-POP FOLDERS 1 to 41 ===")
for i in range(min(41, len(folders))):
    f = folders[i]
    fp = os.path.join(BASE, f)
    subdirs = [d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp, d))]
    print(f"{i+1:03d}. {f} ({len(subdirs)} subdirs)")
