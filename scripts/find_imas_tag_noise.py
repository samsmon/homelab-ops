import os
import re

imas_root = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~"

print("=== CHECKING FOR FORMAT TAG NOISE IN IMAS ===")
for r, d, f in os.walk(imas_root):
    for dir_name in d:
        if any(tag in dir_name.lower() for tag in ['cd-flac', 'flac', 'web-flac', 'eac', 'hi-res', '32bit', '24bit', '96khz', '48khz']):
            rel = os.path.relpath(os.path.join(r, dir_name), imas_root)
            print(f"Format tag in dir: {rel}")
