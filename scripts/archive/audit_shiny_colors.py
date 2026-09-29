#!/usr/bin/env python3
import os
from pathlib import Path

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~/シャイニーカラーズ')

AUDIO_EXTS = {'.flac', '.aiff', '.aif', '.alac', '.wav', '.m4a'}

total_albums = 0
total_audio = 0
anomalies = []

print("=== SHINY COLORS LIBRARY AUDIT (OPTION A) ===")

for cat in sorted(BASE.iterdir()):
    if not cat.is_dir():
        continue
    
    # Check if category has subcategories (like 01. WING & Main Game Series)
    subdirs = [d for d in sorted(cat.iterdir()) if d.is_dir()]
    has_subseries = any(d.name.startswith(('01.', '02.', '03.', '04.', '05.', '06.', '07.')) for d in subdirs)
    
    if has_subseries:
        print(f"\n📂 {cat.name}/")
        for sub in subdirs:
            albums = [d for d in sorted(sub.iterdir()) if d.is_dir()]
            print(f"  ├── 📁 {sub.name} ({len(albums)} albums)")
            for alb in albums:
                total_albums += 1
                audios = [f for f in alb.iterdir() if f.is_file() and f.suffix.lower() in AUDIO_EXTS]
                total_audio += len(audios)
                if not audios:
                    anomalies.append(f"No audio: {sub.name}/{alb.name}")
    else:
        albums = subdirs
        print(f"\n📂 {cat.name}/ ({len(albums)} albums)")
        for alb in albums:
            total_albums += 1
            audios = [f for f in alb.iterdir() if f.is_file() and f.suffix.lower() in AUDIO_EXTS]
            total_audio += len(audios)
            if not audios:
                # check if multi-disc
                discs = [d for d in alb.iterdir() if d.is_dir() and 'disc' in d.name.lower()]
                if discs:
                    for disc in discs:
                        daudios = [f for f in disc.iterdir() if f.is_file() and f.suffix.lower() in AUDIO_EXTS]
                        total_audio += len(daudios)
                else:
                    anomalies.append(f"No audio: {cat.name}/{alb.name}")

print("\n" + "="*50)
print(f"TOTAL ALBUMS: {total_albums}")
print(f"TOTAL AUDIO TRACKS: {total_audio}")
print(f"ANOMALIES FOUND: {len(anomalies)}")
for anom in anomalies:
    print("  ⚠️ ", anom)
