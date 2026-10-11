#!/usr/bin/env python3
import os

BASE = "/mnt/hdd-backup/download"
print("=== FOLDERS IN /mnt/hdd-backup/download ===")
for cat in os.listdir(BASE):
    cat_p = os.path.join(BASE, cat)
    if os.path.isdir(cat_p):
        subdirs = [d for d in os.listdir(cat_p) if os.path.isdir(os.path.join(cat_p, d))]
        print(f"[{cat}] {len(subdirs)} folders")
        for s in subdirs[:5]:
            print(f"   - {s}")
