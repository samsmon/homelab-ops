#!/usr/bin/env python3
import os
import json
import subprocess

p = "/mnt/hdd-backup/music/Lossless/Anime/Tv Anime (TVアニメ) ~"
items = sorted(os.listdir(p))

data = []
for idx, item in enumerate(items):
    ip = os.path.join(p, item)
    files = [f for f in os.listdir(ip) if f.endswith(('.flac', '.mp3'))]
    sample_tag = {}
    if files:
        sample_file = os.path.join(ip, files[0])
        res = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format_tags=ARTIST,artist,ALBUM,album,TITLE,title', '-of', 'json', sample_file], stdout=subprocess.PIPE, text=True)
        try:
            sample_tag = json.loads(res.stdout).get('format', {}).get('tags', {})
        except Exception:
            pass
    data.append({
        'index': idx,
        'item': item,
        'track_count': len(files),
        'sample_tags': sample_tag
    })

with open('/tmp/tv_anime_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Written {len(data)} items to /tmp/tv_anime_analysis.json")
