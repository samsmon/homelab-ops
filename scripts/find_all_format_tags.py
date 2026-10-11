import os
import re

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=== CHECKING FOR FORMAT TAG NOISE ACROSS ENTIRE LIBRARY ===")
patterns = [r'\[cd-flac\]', r'\[web-flac\]', r'\[flac\]', r'\[eac\]', r'\[hi-res\]', r'\[32bit\]', r'\[24bit\]', r'\[aiff.*?\]']

bad_folders = []
for r, d, f in os.walk(ROOT):
    for dir_name in d:
        dn_low = dir_name.lower()
        for p in patterns:
            if re.search(p, dn_low):
                bad_folders.append((os.path.join(r, dir_name), dir_name))
                break

print(f"Total folders with format tags: {len(bad_folders)}")
for fp, name in bad_folders:
    print(f"  {os.path.relpath(fp, ROOT)}")
