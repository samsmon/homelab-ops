#!/usr/bin/env python3
import os

BASE = '/mnt/hdd-backup/music/Lossless/Anime'
folders = sorted(os.listdir(BASE))

print(f"=== ALL {len(folders)} FOLDERS IN /mnt/hdd-backup/music/Lossless/Anime ===")
for i, f in enumerate(folders, 1):
    fp = os.path.join(BASE, f)
    # Check what is inside
    subdirs = [d for d in os.listdir(fp) if os.path.isdir(os.path.join(fp, d))]
    files = [fl for fl in os.listdir(fp) if os.path.isfile(os.path.join(fp, fl))]
    print(f"{i:02d}. {f} -> {len(subdirs)} subdirs, {len(files)} files")
    for s in subdirs[:3]:
        print(f"     * {s}")
    if len(subdirs) > 3:
        print(f"     ... ({len(subdirs) - 3} more)")
