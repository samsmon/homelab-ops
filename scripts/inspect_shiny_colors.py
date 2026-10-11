#!/usr/bin/env python3
import os
from pathlib import Path
from collections import defaultdict

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~/シャイニーカラーズ')

categories = defaultdict(list)

for p in sorted(BASE.rglob('*')):
    if p.is_dir():
        audio = [f for f in p.iterdir() if f.is_file() and f.suffix.lower() in ['.flac', '.aiff', '.m4a', '.wav']]
        if audio and p.name != 'BK':
            # find category tier
            rel = p.relative_to(BASE)
            cat = rel.parts[0]
            categories[cat].append((p.name, len(audio)))

print("=== THE IDOLM@STER SHINY COLORS ALBUM BREAKDOWN ===")
total_albums = 0
total_tracks = 0
for cat in sorted(categories.keys()):
    items = categories[cat]
    cat_tracks = sum(t for _, t in items)
    total_albums += len(items)
    total_tracks += cat_tracks
    print(f"\n📂 {cat}: {len(items)} albums ({cat_tracks} tracks)")
    for name, cnt in items:
        print(f"   • {name} [{cnt} tracks]")

print("\n" + "="*60)
print(f"TOTAL ALBUM FOLDERS: {total_albums}")
print(f"TOTAL AUDIO TRACKS : {total_tracks}")
print("="*60)
