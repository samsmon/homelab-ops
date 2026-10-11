#!/usr/bin/env python3
import os
import subprocess

p = "/mnt/hdd-backup/music/Lossless/J-Pop/Hibana (ヒバナ) ~"
loose = [f for f in os.listdir(p) if f.endswith('.flac')]
for f in loose[:5]:
    audio_path = os.path.join(p, f)
    res = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format_tags=ARTIST,artist,ALBUM,album,TITLE,title', '-of', 'default=noprint_wrappers=1', audio_path], stdout=subprocess.PIPE, text=True)
    print(f"{f}: {res.stdout.replace(chr(10), ' | ')}")
