#!/usr/bin/env python3
import os
import subprocess

p = "/mnt/hdd-backup/music/Lossless/Anime/Tv Anime (TVアニメ) ~"
items = sorted(os.listdir(p))
print(f"Total items in Tv Anime: {len(items)}")

for item in items:
    ip = os.path.join(p, item)
    files = [f for f in os.listdir(ip) if f.endswith(('.flac', '.mp3'))]
    sample_file = files[0] if files else None
    tags = ""
    if sample_file:
        res = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format_tags=ARTIST,artist,ALBUM,album,TITLE,title', '-of', 'default=noprint_wrappers=1', os.path.join(ip, sample_file)], stdout=subprocess.PIPE, text=True)
        tags = res.stdout.replace('\n', ' | ')
    print(f"\nItem: {item} ({len(files)} tracks)")
    print(f"  Sample Tag: {tags[:120]}")
