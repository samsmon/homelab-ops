#!/usr/bin/env python3
import os
import re

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=" * 80)
print("INSPECTING ALL 43 NESTED DUPLICATES")
print("=" * 80)

for root, dirs, files in os.walk(BASE_DIR):
    parent = os.path.basename(root)
    for d in dirs:
        clean_d = re.sub(r'[\s\~\(\)\[\]]+', '', d).lower()
        clean_p = re.sub(r'[\s\~\(\)\[\]]+', '', parent).lower()
        if clean_d and clean_d == clean_p:
            full_p = os.path.join(root, d)
            sub_files = os.listdir(full_p)
            rel = os.path.relpath(full_p, BASE_DIR)
            print(f"\nNested: {rel} ({len(sub_files)} items)")
            for sf in sub_files[:6]:
                print(f"   -> {sf}")
            if len(sub_files) > 6:
                print(f"   -> ... and {len(sub_files) - 6} more")
