#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

bang_dir = Path("/mnt/hdd-backup/music/Lossless/Anime/BanG Dream! (バンドリ！) ~")
loose = []
for p in bang_dir.iterdir():
    if not p.is_dir():
        continue
    if p.name.endswith("~"):
        continue
    loose.append(p)

print(f"Total loose in BanG Dream: {len(loose)}")
for p in sorted(loose, key=lambda x: x.name):
    # probe first flac
    flacs = list(p.glob("**/*.flac"))
    artist = "Unknown"
    album = p.name
    if flacs:
        try:
            res = subprocess.check_output(
                ["ffprobe", "-show_entries", "format_tags=artist,album_artist,album", "-of", "default=noprint_wrappers=1", str(flacs[0])],
                text=True, stderr=subprocess.DEVNULL
            )
            for line in res.splitlines():
                u_line = line.upper()
                if "TAG:ARTIST=" in u_line or "TAG:ALBUM_ARTIST=" in u_line:
                    artist = line.split("=", 1)[1]
                elif "TAG:ALBUM=" in u_line:
                    album = line.split("=", 1)[1]
        except Exception:
            pass
    print(f"[{p.name}] -> Artist: {artist} | Album: {album}")
