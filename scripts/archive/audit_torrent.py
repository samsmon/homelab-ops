import os
import sys
import hashlib
import sqlite3
import subprocess
from pathlib import Path

music_root = Path('/mnt/hdd-backup/music')
torrent_root = music_root / 'Torrent'
torrent_done = torrent_root / 'done'
torrent_leeching = torrent_root / '!leeching'
lossless_root = music_root / 'Lossless'

def get_md5(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

print("="*60)
print("AUDIT OF TORRENT DIRECTORIES")
print("="*60)

# 1. Audit !leeching
print("\n>>> 1. AUDITING Torrent/!leeching <<<")
if torrent_leeching.exists():
    for item in sorted(torrent_leeching.iterdir()):
        if not item.is_dir():
            continue
        files = [f for f in item.rglob('*') if f.is_file()]
        audio = [f for f in files if f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a']]
        size_mb = sum(f.stat().st_size for f in files) / (1024*1024)
        print(f"[{item.name}]")
        print(f"   Files: {len(files)}, Audio: {len(audio)}, Size: {size_mb:.2f} MB")
        if len(files) == 0:
            print("   -> STATUS: Completely empty directory (can be safely deleted)")
        elif len(audio) == 0:
            print(f"   -> STATUS: No audio files (non-audio: {[f.name for f in files]})")
        else:
            print(f"   -> STATUS: Has {len(audio)} audio files.")

# 2. Audit done
print("\n>>> 2. AUDITING Torrent/done <<<")
done_folders = sorted([d for d in torrent_done.iterdir() if d.is_dir()])
print(f"Total folders in done: {len(done_folders)}")

empty_folders = []
cover_only_folders = []
folders_with_audio = []

for d in done_folders:
    files = [f for f in d.rglob('*') if f.is_file()]
    audio = [f for f in files if f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a', '.aac', '.ogg', '.opus']]
    if len(files) == 0:
        empty_folders.append(d)
    elif len(audio) == 0:
        cover_only_folders.append((d, files))
    else:
        folders_with_audio.append((d, audio, files))

print(f"\n[Empty Folders] Count: {len(empty_folders)}")
for d in empty_folders:
    print(f"  - {d.name}")

print(f"\n[Cover/Metadata Only Folders (No Audio)] Count: {len(cover_only_folders)}")
for d, files in cover_only_folders:
    print(f"  - {d.name} -> {[f.name for f in files]}")

print(f"\n[Folders with Audio Tracks] Count: {len(folders_with_audio)}")

# Check duplicate status against Lossless
exact_duplicate_albums = []
partial_or_new_albums = []

for d, audio, all_files in folders_with_audio:
    # Check if all audio files in d exist with identical size/content in Lossless
    all_matched = True
    match_paths = []
    for a in audio:
        # search by filename in Lossless
        candidates = [c for c in lossless_root.rglob(a.name) if c.is_file()]
        found = False
        for c in candidates:
            if c.stat().st_size == a.stat().st_size:
                # size matches, verify md5
                if get_md5(c) == get_md5(a):
                    found = True
                    match_paths.append(c)
                    break
        if not found:
            all_matched = False
            break
            
    if all_matched and len(match_paths) == len(audio):
        exact_duplicate_albums.append((d, match_paths[0].parent))
    else:
        partial_or_new_albums.append((d, len(audio)))

print(f"\n[Exact Full Duplicates of Lossless] Count: {len(exact_duplicate_albums)}")
for src, dst in exact_duplicate_albums[:10]:
    print(f"  DUP: {src.name} == {dst.relative_to(music_root)}")
if len(exact_duplicate_albums) > 10:
    print(f"  ... and {len(exact_duplicate_albums) - 10} more duplicate albums")

print(f"\n[Unique or Not Fully in Lossless] Count: {len(partial_or_new_albums)}")
for src, cnt in partial_or_new_albums[:15]:
    print(f"  NEW: {src.name} ({cnt} tracks)")
if len(partial_or_new_albums) > 15:
    print(f"  ... and {len(partial_or_new_albums) - 15} more new albums")
