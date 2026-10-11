#!/usr/bin/env python3
import os
import re
from pathlib import Path

LOSSLESS = Path('/mnt/hdd-backup/music/Lossless')
categories = ['Anime', 'Doujinshi', 'Game', 'Global', 'J-Pop', 'Vocaloid', 'Vtuber']

print("=== CHECK 1: EMPTY DIRS ===")
empty_dirs = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists(): continue
    for root, dirs, files in os.walk(cat_dir, topdown=False):
        p = Path(root)
        if not list(p.iterdir()):
            empty_dirs.append(str(p.relative_to(LOSSLESS)))
print(f"Total empty: {len(empty_dirs)}")
for d in empty_dirs:
    print(f"  {d}")

print("\n=== CHECK 2: LOOSE AUDIO ===")
audio_exts = {'.flac', '.wav', '.mp3', '.m4a', '.aac', '.ogg', '.opus', '.ape', '.wv', '.tak', '.aiff', '.alac'}
loose_audio = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists(): continue
    for f in cat_dir.glob('*'):
        if f.is_file() and f.suffix.lower() in audio_exts:
            loose_audio.append(str(f.relative_to(LOSSLESS)))
    for artist in cat_dir.iterdir():
        if artist.is_dir():
            for f in artist.glob('*'):
                if f.is_file() and f.suffix.lower() in audio_exts:
                    loose_audio.append(str(f.relative_to(LOSSLESS)))
print(f"Total loose audio: {len(loose_audio)}")
for l in loose_audio:
    print(f"  {l}")

print("\n=== CHECK 4: DEFORMED NAMES ===")
deformed_names = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists(): continue
    for artist in cat_dir.iterdir():
        if not artist.is_dir(): continue
        name = artist.name
        issues = []
        if name.count('(') > 1:
            issues.append("multiple_parens")
        if not name.endswith('~'):
            issues.append("missing_trailing_tilde")
        if name.startswith(' ') or '  ' in name:
            issues.append("irregular_spacing")
        if any(bad in name for bad in ['(hosi)', 'cv_', 'cv :', 'cv.', 'Akunaitsu', 'Porupurinsesu', 'Howaitoarubamu', '_alt', '??']):
            issues.append("kakasi_or_glitch")
        if issues:
            deformed_names.append((cat, name, issues))
print(f"Total deformed artist folders: {len(deformed_names)}")
for cat, name, issues in deformed_names:
    print(f"  [{cat}] {name} -> {issues}")

print("\n=== CHECK 5: NON-ASCII STARTING FOLDERS ===")
non_ascii = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists(): continue
    for artist in cat_dir.iterdir():
        if not artist.is_dir(): continue
        first_char = artist.name[0]
        if ord(first_char) >= 128:
            non_ascii.append((cat, artist.name))
print(f"Total non-ASCII starting: {len(non_ascii)}")
for cat, name in non_ascii:
    print(f"  [{cat}] {name}")
