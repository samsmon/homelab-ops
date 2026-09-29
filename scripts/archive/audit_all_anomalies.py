#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep anomaly audit script for all music folders.
"""
import os
from pathlib import Path

BASE_MUSIC = Path('/mnt/hdd-backup/music')
MUSIC_ROOT = BASE_MUSIC / 'Lossless'

print("="*60)
print("COMPREHENSIVE MUSIC ANOMALY AUDIT")
print("="*60)

# 1. Permanent delete target check
fujian = MUSIC_ROOT / 'Doujinshi' / 'Fujian Series ~'
print(f"Fujian Series exists: {fujian.exists()}")

# 2. Galaxy Triangle incomplete target check
gt = MUSIC_ROOT / 'Anime' / 'Galaxy Triangle ~'
print(f"Anime/Galaxy Triangle exists: {gt.exists()}")

# 3. Find all directories that contain 0 audio files (leaf level)
zero_audio_albums = []
for cat in ['Doujinshi', 'Vtuber', 'Anime', 'J-Pop', 'Vocaloid', 'Global']:
    cat_dir = MUSIC_ROOT / cat
    if not cat_dir.exists():
        continue
    for artist_dir in cat_dir.iterdir():
        if not artist_dir.is_dir():
            continue
        for album_dir in artist_dir.iterdir():
            if not album_dir.is_dir():
                continue
            # check if album_dir has any subfolders (like Disc 1, Scans)
            files = [f for f in album_dir.rglob('*') if f.is_file()]
            audio = [f for f in files if f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a', '.aiff', '.alac', '.tak', '.ape', '.ogg', '.opus', '.wma']]
            if not audio:
                zero_audio_albums.append((album_dir, len(files), [f.name for f in files[:5]]))

print(f"\n[1] Leaf Album Folders with ZERO Audio Files: {len(zero_audio_albums)}")
for p, fcount, sample in zero_audio_albums:
    print(f"  - {p.relative_to(MUSIC_ROOT)} ({fcount} non-audio files: {sample})")

# 4. Check Redundant Image FLACs (CDImage/LACM/etc alongside split tracks)
redundant_images = []
for p in MUSIC_ROOT.rglob('*.flac'):
    # if filename matches whole disc image patterns
    if p.name.startswith(('LACM-', 'LACA-')) or 'cdimage' in p.name.lower():
        parent = p.parent
        # check if parent or sibling has track flacs
        track_flacs = [f for f in parent.glob('*.flac') if f != p and not f.name.startswith(('LACM-', 'LACA-')) and 'cdimage' not in f.name.lower()]
        # also check subfolders like Disc 1
        if not track_flacs:
            track_flacs = [f for f in parent.rglob('*.flac') if f != p and not f.name.startswith(('LACM-', 'LACA-')) and 'cdimage' not in f.name.lower()]
        if track_flacs:
            redundant_images.append((p, len(track_flacs), p.stat().st_size / (1024*1024)))

print(f"\n[2] Redundant Whole-CD Image FLACs (where split tracks exist): {len(redundant_images)}")
for p, tcount, mb in redundant_images:
    print(f"  - {p.relative_to(MUSIC_ROOT)} ({mb:.1f} MB, alongside {tcount} split tracks)")

# 5. Check Uma Musume folder names
uma_dir = MUSIC_ROOT / 'Anime' / 'Uma Musume ~'
if uma_dir.exists():
    print(f"\n[3] Uma Musume Folder Inventory ({len(list(uma_dir.iterdir()))} items):")
    for d in sorted(uma_dir.iterdir()):
        if d.is_dir():
            print(f"  - {d.name}")
