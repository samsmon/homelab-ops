#!/usr/bin/env python3
import os

anime_dir = '/mnt/hdd-backup/music/Lossless/Anime'
folders = sorted([d for d in os.listdir(anime_dir) if os.path.isdir(os.path.join(anime_dir, d))])
print(f"Total folders in Anime: {len(folders)}")
for d in folders:
    full = os.path.join(anime_dir, d)
    subdirs = [s for s in os.listdir(full) if os.path.isdir(os.path.join(full, s))]
    files = [f for f in os.listdir(full) if os.path.isfile(os.path.join(full, f))]
    print(f"{d} | subfolders: {len(subdirs)}, files: {len(files)}")
    if len(subdirs) <= 2:
        for s in subdirs:
            print(f"    -> {s}")
