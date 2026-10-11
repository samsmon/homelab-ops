#!/usr/bin/env python3
import os
import subprocess

BASE = "/mnt/hdd-backup/music/Lossless"

print("Auditing embedded Vorbis tags for missing TITLE/ARTIST...")
# Check a sample of 200 random tracks across different categories
# or check if mutagen is available
try:
    import mutagen
    from mutagen.flac import FLAC
    has_mutagen = True
except ImportError:
    has_mutagen = False

print(f"Mutagen available: {has_mutagen}")

missing_title = []
missing_artist = []
total_checked = 0

for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.lower().endswith('.flac'):
            total_checked += 1
            if has_mutagen:
                try:
                    audio = FLAC(os.path.join(root, f))
                    if not audio.get('title'):
                        missing_title.append(os.path.join(root, f))
                    if not audio.get('artist'):
                        missing_artist.append(os.path.join(root, f))
                except Exception as e:
                    pass
            if total_checked % 3000 == 0:
                print(f"Checked {total_checked} tracks...")

print(f"\nTotal checked: {total_checked}")
print(f"Missing TITLE tag: {len(missing_title)}")
for mt in missing_title[:5]:
    print(f"  {mt}")
print(f"Missing ARTIST tag: {len(missing_artist)}")
for ma in missing_artist[:5]:
    print(f"  {ma}")
