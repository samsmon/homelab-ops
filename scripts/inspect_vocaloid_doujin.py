#!/usr/bin/env python3
import os
import subprocess

BASE = '/mnt/hdd-backup/music/Lossless'

for cat in ['Vocaloid', 'Doujinshi', 'Global']:
    cat_dir = os.path.join(BASE, cat)
    if not os.path.isdir(cat_dir):
        continue
    print(f"\n=======================================================")
    print(f"=== ALL FOLDERS IN {cat} ({len(os.listdir(cat_dir))}) ===")
    print(f"=======================================================")
    for f in sorted(os.listdir(cat_dir)):
        fp = os.path.join(cat_dir, f)
        if not os.path.isdir(fp):
            print(f"  [FILE] {f}")
            continue
        subdirs = [d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp, d))]
        files = [fl for fl in os.listdir(fp) if os.path.isfile(os.path.join(fp, fl))]
        print(f"  * {f} ({len(subdirs)} subdirs, {len(files)} files)")
        for s in subdirs[:3]:
            print(f"      - {s}")
        if len(subdirs) > 3:
            print(f"      ... and {len(subdirs) - 3} more")
