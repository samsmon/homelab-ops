import os
import sys
import json
from pathlib import Path

music_root = Path('/mnt/hdd-backup/music')

print("=== DEEP AUDIT OF MUSIC GUDANG PUSAT ===")

# 1. Audit ~Extract
extract_dir = music_root / '~Extract'
print("\n--- 1. AUDIT OF ~Extract ---")
if extract_dir.exists():
    archives = [f for f in extract_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.zip', '.rar', '.7z', '.tar', '.gz']]
    print(f"Unextracted archives in ~Extract: {len(archives)}")
    for a in archives:
        print(f"  [ARCHIVE] {a.name} ({a.stat().st_size / (1024*1024):.1f} MB)")
        
    flac_dir = extract_dir / 'flac'
    if flac_dir.exists():
        flac_items = [d for d in flac_dir.iterdir() if d.is_dir()]
        print(f"\nFolders in ~Extract/flac: {len(flac_items)}")
        for d in flac_items:
            files = [f for f in d.rglob('*') if f.is_file()]
            audio = [f for f in files if f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a', '.aac', '.ogg', '.opus']]
            print(f"  [FOLDER] {d.name} -> {len(files)} files ({len(audio)} audio, {[f.name for f in files if f.suffix.lower() not in ['.flac', '.wav', '.mp3', '.m4a']][:3]})")

# 2. Audit Torrent/done
done_dir = music_root / 'Torrent' / 'done'
print("\n--- 2. AUDIT OF Torrent/done ---")
if done_dir.exists():
    items = sorted([d for d in done_dir.iterdir() if d.is_dir()])
    print(f"Total folders in Torrent/done: {len(items)}")
    empty_or_cover_only = []
    has_audio = []
    for d in items:
        files = [f for f in d.rglob('*') if f.is_file()]
        audio = [f for f in files if f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a']]
        if not audio:
            empty_or_cover_only.append((d.name, [f.name for f in files]))
        else:
            has_audio.append((d.name, len(audio), sum(f.stat().st_size for f in audio)/(1024*1024)))
            
    print(f"\nEmpty or Cover/Metadata-Only Folders: {len(empty_or_cover_only)}")
    for name, fnames in empty_or_cover_only:
        print(f"  [EMPTY/COVER] {name} -> {fnames}")
        
    print(f"\nFolders with Audio: {len(has_audio)}")
    for name, count, mb in has_audio:
        print(f"  [AUDIO] {name} ({count} tracks, {mb:.1f} MB)")

# 3. Audit Torrent/!leeching
leech_dir = music_root / 'Torrent' / '!leeching'
print("\n--- 3. AUDIT OF Torrent/!leeching ---")
if leech_dir.exists():
    for d in sorted([x for x in leech_dir.iterdir() if x.is_dir()]):
        files = [f for f in d.rglob('*') if f.is_file()]
        audio = [f for f in files if f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a']]
        mb = sum(f.stat().st_size for f in files) / (1024*1024)
        print(f"  {d.name} -> {len(files)} files ({len(audio)} audio, {mb:.1f} MB)")

# 4. Audit Islet / Tayori
print("\n--- 4. AUDIT OF ISLET / TAYORI ---")
for p in music_root.rglob('*islet*'):
    if p.is_dir():
        print(f"  DIR:  {p.relative_to(music_root)}")
for p in music_root.rglob('*Tayori*'):
    if p.is_dir():
        print(f"  DIR:  {p.relative_to(music_root)}")

# 5. Audit Loose Folders in Lossless and Lossy Root
print("\n--- 5. AUDIT OF LOOSE FOLDERS IN LOSSLESS & LOSSY ROOT ---")
lossless_root = music_root / 'Lossless'
for d in lossless_root.iterdir():
    if d.is_dir() and d.name not in ['Anime', 'Doujinshi', 'Global', 'J-Pop', 'Vocaloid', 'Vtuber']:
        print(f"  [LOSSLESS LOOSE] {d.name}")

lossy_root = music_root / 'Lossy'
for d in lossy_root.iterdir():
    if d.is_dir() and d.name not in ['Anime', 'Doujinshi', 'Global', 'J-Pop', 'Vocaloid', 'Vtuber']:
        print(f"  [LOSSY LOOSE] {d.name}")
