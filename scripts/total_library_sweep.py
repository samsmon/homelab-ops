#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOTAL EXHAUSTIVE LIBRARY SWEEP
Audits every corner of /mnt/hdd-backup/music/Lossless across 10 critical dimensions:
1. Empty directories
2. Loose audio files at root, category, or umbrella levels
3. Nested / double container folders
4. Deformed / abnormal folder names (parens, spacing, missing tilde)
5. Non-ASCII starting artist/umbrella folders
6. Cross-category duplicate artists
7. Anime / Game character songs or franchises still lurking in J-Pop
8. Seiyuu / J-Pop artists still lurking in Anime
9. Windows SMB forbidden characters (: * ? " < > |)
10. Residual CUE / monolithic WAV/FLAC disc images
"""

import os
import re
from pathlib import Path

LOSSLESS = Path('/mnt/hdd-backup/music/Lossless')
categories = ['Anime', 'Doujinshi', 'Game', 'Global', 'J-Pop', 'Vocaloid', 'Vtuber']

print("=" * 80)
print("TOTAL EXHAUSTIVE SWEEP OF /mnt/hdd-backup/music/Lossless")
print("=" * 80)

# ------------------------------------------------------------------------------
# 1. EMPTY DIRECTORIES
# ------------------------------------------------------------------------------
print("\n[CHECK 1] EMPTY DIRECTORIES")
empty_dirs = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists():
        continue
    for root, dirs, files in os.walk(cat_dir, topdown=False):
        p = Path(root)
        if not list(p.iterdir()):
            empty_dirs.append(p.relative_to(LOSSLESS))

print(f"Total empty directories: {len(empty_dirs)}")
for d in empty_dirs[:20]:
    print(f"  Empty: {d}")
if len(empty_dirs) > 20:
    print(f"  ... and {len(empty_dirs) - 20} more")

# ------------------------------------------------------------------------------
# 2. LOOSE AUDIO FILES AT ROOT OR ARTIST LEVEL
# ------------------------------------------------------------------------------
print("\n[CHECK 2] LOOSE AUDIO FILES (Files not in an Album folder)")
audio_exts = {'.flac', '.wav', '.mp3', '.m4a', '.aac', '.ogg', '.opus', '.ape', '.wv', '.tak', '.aiff', '.alac'}
loose_audio = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists():
        continue
    # Files directly in category root: Lossless/Anime/*.flac
    for f in cat_dir.glob('*'):
        if f.is_file() and f.suffix.lower() in audio_exts:
            loose_audio.append(f.relative_to(LOSSLESS))
    # Files directly in artist root: Lossless/Anime/Artist ~/*.flac
    for artist in cat_dir.iterdir():
        if artist.is_dir():
            for f in artist.glob('*'):
                if f.is_file() and f.suffix.lower() in audio_exts:
                    loose_audio.append(f.relative_to(LOSSLESS))

print(f"Total loose audio files at category/artist level: {len(loose_audio)}")
for l in loose_audio[:20]:
    print(f"  Loose audio: {l}")

# ------------------------------------------------------------------------------
# 3. NESTED CONTAINERS (Depth > 3 or nested torrent pack patterns)
# ------------------------------------------------------------------------------
print("\n[CHECK 3] SUSPICIOUS NESTED CONTAINERS")
suspicious_nested = []
container_patterns = ['[20', '[19', 'ERA ', 'DISC ', 'CD ', 'Singles', 'Albums', 'FLAC', 'WEB-FLAC', 'Collection']
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists():
        continue
    for root, dirs, files in os.walk(cat_dir):
        p = Path(root)
        rel = p.relative_to(cat_dir)
        # Check if dir contains child dirs that have similar container patterns
        if any(pat in p.name for pat in ['ERA ', 'Singles & Albums', '[2022-2023]']):
            suspicious_nested.append(rel)

print(f"Total suspicious container folders: {len(suspicious_nested)}")
for s in suspicious_nested[:20]:
    print(f"  Nested: {s}")

# ------------------------------------------------------------------------------
# 4. DEFORMED / ABNORMAL FOLDER NAMES
# ------------------------------------------------------------------------------
print("\n[CHECK 4] DEFORMED / ABNORMAL FOLDER NAMES AT ARTIST LEVEL")
deformed_names = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists():
        continue
    for artist in cat_dir.iterdir():
        if not artist.is_dir():
            continue
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

# ------------------------------------------------------------------------------
# 5. NON-ASCII STARTING FOLDERS (Japanese before Romaji)
# ------------------------------------------------------------------------------
print("\n[CHECK 5] NON-ASCII STARTING ARTIST FOLDERS")
non_ascii = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists():
        continue
    for artist in cat_dir.iterdir():
        if not artist.is_dir():
            continue
        first_char = artist.name[0]
        if ord(first_char) >= 128:
            non_ascii.append((cat, artist.name))

print(f"Total non-ASCII starting folders: {len(non_ascii)}")
for cat, name in non_ascii:
    print(f"  [{cat}] {name}")

# ------------------------------------------------------------------------------
# 6. CROSS-CATEGORY DUPLICATE ARTISTS
# ------------------------------------------------------------------------------
print("\n[CHECK 6] CROSS-CATEGORY SPLIT ARTISTS")
artist_lookup = {}
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists():
        continue
    for artist in cat_dir.iterdir():
        if not artist.is_dir():
            continue
        clean = artist.name.strip('~').strip().lower()
        base = re.sub(r'\(.*?\)', '', clean).strip()
        if not base:
            base = clean
        artist_lookup.setdefault(base, []).append((cat, artist.name))

cross_cat = {}
for k, v in artist_lookup.items():
    cats = set(c for c, n in v)
    if len(cats) > 1:
        cross_cat[k] = v

print(f"Total cross-category split artists: {len(cross_cat)}")
for k, v in sorted(cross_cat.items()):
    print(f"  Artist '{k}':")
    for c, n in v:
        print(f"    - [{c}] {n}")

# ------------------------------------------------------------------------------
# 7. CHARACTER / ANIME SONGS STILL LURKING IN J-POP
# ------------------------------------------------------------------------------
print("\n[CHECK 7] CHARACTER SONGS / ANIME / VTUBERS IN J-POP")
jpop_dir = LOSSLESS / 'J-Pop'
suspects = []
kw = ['(cv', 'cv.', 'cv_', 'character', 'soundtrack', 'hololive', 'nijisanji', 'vspo', 'kamitsubaki', 'riot music', 'rk music']
for artist in jpop_dir.iterdir():
    if not artist.is_dir():
        continue
    nl = artist.name.lower()
    if any(k in nl for k in kw):
        suspects.append(artist.name)

print(f"Total suspected anime/vtuber/character folders in J-Pop: {len(suspects)}")
for s in suspects:
    print(f"  {s}")

# ------------------------------------------------------------------------------
# 8. SEIYUU / J-POP ARTISTS STILL LURKING IN ANIME
# ------------------------------------------------------------------------------
print("\n[CHECK 8] ARTISTS STILL LURKING IN ANIME")
anime_dir = LOSSLESS / 'Anime'
anime_suspects = []
for artist in anime_dir.iterdir():
    if not artist.is_dir():
        continue
    subdirs = [s for s in artist.iterdir() if s.is_dir()]
    # Check if folder looks like a person name e.g. "Surname Forename (Kanji)" with 1 album
    if len(subdirs) == 1 and re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+ \(.*?\)\s*~?$', artist.name):
        anime_suspects.append((artist.name, [s.name for s in subdirs]))

print(f"Total 1-album person-like folders in Anime: {len(anime_suspects)}")
for name, albs in anime_suspects:
    print(f"  {name} -> {albs}")

# ------------------------------------------------------------------------------
# 9. WINDOWS FORBIDDEN CHARACTERS IN ALL PATHS
# ------------------------------------------------------------------------------
print("\n[CHECK 9] WINDOWS FORBIDDEN CHARACTERS (: * ? \" < > |)")
forbidden_chars = [':', '*', '?', '"', '<', '>', '|']
windows_bad = []
for cat in categories:
    cat_dir = LOSSLESS / cat
    if not cat_dir.exists():
        continue
    for root, dirs, files in os.walk(cat_dir):
        for d in dirs:
            if any(ch in d for ch in forbidden_chars):
                windows_bad.append(('DIR', os.path.join(root, d)))
        for f in files:
            if any(ch in f for ch in forbidden_chars):
                windows_bad.append(('FILE', os.path.join(root, f)))

print(f"Total paths with Windows forbidden characters: {len(windows_bad)}")
for t, p in windows_bad[:20]:
    rel = Path(p).relative_to(LOSSLESS)
    print(f"  [{t}] {rel}")

# ------------------------------------------------------------------------------
# 10. RESIDUAL CUE SHEETS AND MONOLITHIC WAV/FLAC DISC IMAGES
# ------------------------------------------------------------------------------
print("\n[CHECK 10] RESIDUAL CUE SHEETS / UNSPLIT DISC IMAGES")
cue_files = list(LOSSLESS.rglob('*.cue'))
wav_files = list(LOSSLESS.rglob('*.wav'))
print(f"Total .cue files found: {len(cue_files)}")
for c in cue_files[:10]:
    print(f"  CUE: {c.relative_to(LOSSLESS)}")
print(f"Total .wav files found: {len(wav_files)}")
for w in wav_files[:10]:
    print(f"  WAV: {w.relative_to(LOSSLESS)}")

print("\n" + "=" * 80)
print("TOTAL SWEEP FINISHED")
print("=" * 80)
