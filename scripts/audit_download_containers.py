#!/usr/bin/env python3
import os

BASE = "/mnt/hdd-backup/download"

print("Auditing potential multi-album dumping grounds in /mnt/hdd-backup/download...")

for cat in os.listdir(BASE):
    cat_p = os.path.join(BASE, cat)
    if not os.path.isdir(cat_p):
        continue
    for artist_f in os.listdir(cat_p):
        artist_p = os.path.join(cat_p, artist_f)
        if not os.path.isdir(artist_p):
            continue
        
        # Check subdirs of artist
        subdirs = [d for d in os.listdir(artist_p) if os.path.isdir(os.path.join(artist_p, d))]
        for sub in subdirs:
            sub_p = os.path.join(artist_p, sub)
            sub_subdirs = [d for d in os.listdir(sub_p) if os.path.isdir(os.path.join(sub_p, d))]
            if len(sub_subdirs) > 5:
                print(f"SUSPICIOUS CONTAINER: [{cat}] {artist_f} / {sub} -> {len(sub_subdirs)} subdirectories!")
                for ssd in sub_subdirs[:5]:
                    print(f"    * {ssd}")
