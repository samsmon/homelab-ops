import os
import re

ROOT = "/mnt/hdd-backup/music/Lossless"

print(f"=== CHECKING GAME & J-POP FOR FORMAT TAG NOISE ===")
for cat in ['Game', 'J-Pop', 'Doujinshi', 'Vocaloid', 'Global']:
    cat_path = os.path.join(ROOT, cat)
    if not os.path.isdir(cat_path):
        continue
    for r, d, f in os.walk(cat_path):
        for dir_name in d:
            dn_low = dir_name.lower()
            if any(t in dn_low for t in ['cd-flac', 'web-flac', 'hi-res', '32bit', '24bit', '96khz', '48khz']):
                rel = os.path.relpath(os.path.join(r, dir_name), ROOT)
                print(f"[{cat}] Format tag in dir: {rel}")
            elif dn_low.endswith(" flac") or " flac" in dn_low:
                rel = os.path.relpath(os.path.join(r, dir_name), ROOT)
                print(f"[{cat}] 'flac' in dir: {rel}")
