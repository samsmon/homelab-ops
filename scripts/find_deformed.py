#!/usr/bin/env python3
import os
import re

anime_dir = '/mnt/hdd-backup/music/Lossless/Anime'
jpop_dir = '/mnt/hdd-backup/music/Lossless/J-Pop'

print("=== DEFORMED FOLDERS IN ANIME ===")
for d in sorted(os.listdir(anime_dir)):
    if '(' in d and ')' in d:
        # Check for multiple parens or strange kakasi
        if d.count('(') > 1 or 'Akunaitsu' in d or 'Porupurinsesu' in d or 'Howaitoarubamu' in d:
            print(f"Anime: {d}")

print("\n=== DEFORMED FOLDERS IN J-POP ===")
for d in sorted(os.listdir(jpop_dir)):
    if '(' in d and ')' in d:
        if d.count('(') > 1:
            print(f"J-Pop: {d}")
