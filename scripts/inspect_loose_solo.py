#!/usr/bin/env python3
import os
import mutagen
from pathlib import Path

solo_dir = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~/01. Solo')

print("=" * 80)
print("INSPECTING LOOSE ALBUMS IN 01. Solo")
print("=" * 80)

for p in sorted(solo_dir.iterdir()):
    if not p.is_dir():
        continue
    # If it's a character folder starting with a number, skip
    if p.name[0].isdigit() and p.name[1].isdigit() and '.' in p.name:
        continue
    
    # Check if it has flacs
    flacs = list(p.rglob('*.flac'))
    if flacs:
        f = mutagen.File(flacs[0])
        artist = f.get('artist', ['Unknown'])[0] if f else 'Unknown'
        title = f.get('title', ['Unknown'])[0] if f else 'Unknown'
        album = f.get('album', ['Unknown'])[0] if f else 'Unknown'
        print(f"Item: {p.name}")
        print(f"  Artist: {artist}")
        print(f"  Album:  {album}")
        print(f"  Flacs:  {len(flacs)}")
