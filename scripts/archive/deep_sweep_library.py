#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep scan of /mnt/hdd-backup/music/Lossless for:
1. Any directory ending in an audio extension (.flac, .mp3, etc.)
2. Any directory containing format/bitrate tags like [FLAC, [24bit, [WEB, etc.
3. Any loose albums in franchise folders that have subseries
4. Any redundant single-subfolder nesting (e.g. dir containing only 1 subfolder of same or similar name)
5. Any mojibake or suspicious characters (?, _, etc.)
"""

import os
import re
from pathlib import Path

LOSSLESS_ROOT = Path('/mnt/hdd-backup/music/Lossless')

AUDIO_EXTS = {'.flac', '.mp3', '.m4a', '.wav', '.ogg', '.opus', '.aac'}

FORMAT_TAG_PATTERN = re.compile(
    r'(\[|\()(?:flac|mp3|web|cd|eac|hi-res|lossless|24bit|16bit|44\.1khz|48khz|96khz|192khz|qobuz|mora|ototoy)[\s\w\.\-\_\/]*(\]|\))',
    re.IGNORECASE
)

DATE_PREFIX_PATTERN = re.compile(r'^\[\d{4}[.\-_]\d{2}[.\-_]\d{2}\]\s*')

print("=" * 80)
print(f"DEEP AUDIT STARTING ON: {LOSSLESS_ROOT}")
print("=" * 80)

anomalies = {
    'audio_ext_dirs': [],
    'format_tag_dirs': [],
    'loose_in_subseries_franchises': [],
    'redundant_single_subfolder': [],
    'mojibake_or_weird_names': [],
}

# 1. Recursive scan for audio ext in dir names, format tags, and redundant nesting
for root, dirs, files in os.walk(LOSSLESS_ROOT):
    root_p = Path(root)
    # Skip _corrupted_quarantine
    if '_corrupted_quarantine' in root_p.parts:
        continue

    for d in dirs:
        dir_p = root_p / d
        
        # Check audio extension in directory name
        if dir_p.suffix.lower() in AUDIO_EXTS:
            anomalies['audio_ext_dirs'].append(str(dir_p))

        # Check format tags
        if FORMAT_TAG_PATTERN.search(d):
            anomalies['format_tag_dirs'].append(str(dir_p))

        # Check weird chars (like raw ?)
        if '?' in d:
            anomalies['mojibake_or_weird_names'].append(str(dir_p))

# 2. Franchise specific loose items check
FRANCHISE_CHECKS = [
    LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~',
    LOSSLESS_ROOT / 'Anime' / 'Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~',
    LOSSLESS_ROOT / 'Anime' / 'Uma Musume (ウマ娘) ~',
    LOSSLESS_ROOT / 'Anime' / 'Love Live! (ラブライブ！) ~',
    LOSSLESS_ROOT / 'Anime' / 'D4DJ (ディーフォーディージェー) ~',
    LOSSLESS_ROOT / 'Anime' / 'BanG Dream! (バンドリ！) ~',
]

for franchise in FRANCHISE_CHECKS:
    if not franchise.exists():
        continue
    # Check top-level loose items in franchise
    for item in franchise.iterdir():
        if not item.is_dir():
            anomalies['loose_in_subseries_franchises'].append((str(franchise.name), str(item.name), "top-level-file"))
        else:
            # Does this franchise have subfranchises/subseries?
            # E.g. in Bocchi: all folders should be [2022-2022] DIGITAL SINGLES, etc.
            # In imas: Shiny Colors, Gakuen, Cinderella, Million, SideM, vα-liv, etc.
            # If an item is a direct album name not matching subfranchises
            pass

# Check Shiny Colors specifically
sc_dir = LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~' / 'Shiny Colors (シャイニーカラーズ) ~'
if sc_dir.exists():
    for item in sc_dir.iterdir():
        if not item.name.startswith(('01.', '02.', '03.', '04.', '05.', '06.', '07.')):
            anomalies['loose_in_subseries_franchises'].append(("Shiny Colors", item.name, "loose-item"))

# Check Gakuen Idolmaster specifically
gakumas_dir = LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~' / 'Gakuen Idolmaster (学園アイドルマスター) ~'
if gakumas_dir.exists():
    for item in gakumas_dir.iterdir():
        if not item.name.startswith(('01.', '02.', '03.', '04.')):
            anomalies['loose_in_subseries_franchises'].append(("Gakuen Idolmaster", item.name, "loose-item"))

# Check Bocchi specifically
bocchi_dir = LOSSLESS_ROOT / 'Anime' / 'Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~'
if bocchi_dir.exists():
    for item in bocchi_dir.iterdir():
        if not item.name.startswith('['):
            anomalies['loose_in_subseries_franchises'].append(("Bocchi the Rock!", item.name, "loose-item"))

# Check Uma Musume specifically
uma_dir = LOSSLESS_ROOT / 'Anime' / 'Uma Musume (ウマ娘) ~'
if uma_dir.exists():
    for item in uma_dir.iterdir():
        if not re.match(r'^\d{2}\.', item.name):
            anomalies['loose_in_subseries_franchises'].append(("Uma Musume", item.name, "loose-item"))

# Check Love Live specifically
ll_dir = LOSSLESS_ROOT / 'Anime' / 'Love Live! (ラブライブ！) ~'
if ll_dir.exists():
    for item in ll_dir.iterdir():
        if not item.name.endswith('~'):
            anomalies['loose_in_subseries_franchises'].append(("Love Live!", item.name, "loose-item"))

# Check D4DJ specifically
d4dj_dir = LOSSLESS_ROOT / 'Anime' / 'D4DJ (ディーフォーディージェー) ~'
if d4dj_dir.exists():
    for item in d4dj_dir.iterdir():
        if not item.name.endswith('~'):
            anomalies['loose_in_subseries_franchises'].append(("D4DJ", item.name, "loose-item"))

# 3. Check for suspicious artist folders (where album names were used as artist folders)
suspicious_artists = []
for cat in ["Anime", "J-Pop", "Vtuber", "Doujinshi", "Vocaloid"]:
    cat_dir = LOSSLESS_ROOT / cat
    if not cat_dir.exists():
        continue
    for artist in cat_dir.iterdir():
        if not artist.is_dir():
            continue
        name = artist.name
        if any(w in name for w in ["アルバム", "Single", "[FLAC]", "Original Soundtrack", "Theme Song", "「", "」", "OP", "ED"]):
            suspicious_artists.append((cat, name))
        # check if artist doesn't end with ~
        if not name.endswith('~'):
            anomalies.setdefault('artists_without_tilde', []).append((cat, name))

# 4. Check details of loose Love Live albums
ll_details = []
ll_dir = LOSSLESS_ROOT / 'Anime' / 'Love Live! (ラブライブ！) ~'
if ll_dir.exists():
    import subprocess
    for item in ll_dir.iterdir():
        if not item.name.endswith('~'):
            files = list(item.glob('**/*.flac'))
            tag_info = "no flac"
            if files:
                try:
                    res = subprocess.check_output(
                        ["ffprobe", "-show_entries", "format_tags=album,album_artist,artist,title", "-of", "default=noprint_wrappers=1", str(files[0])],
                        text=True, stderr=subprocess.DEVNULL
                    )
                    tag_info = " | ".join(line.strip() for line in res.splitlines() if line.strip())
                except Exception as e:
                    tag_info = str(e)
            ll_details.append((item.name, tag_info))

print("\n3. SUSPICIOUS ARTIST FOLDERS (Look like albums):")
for cat, name in suspicious_artists:
    print(f"  - [{cat}] {name}")

print(f"\n4. ARTIST FOLDERS WITHOUT '~' ({len(anomalies.get('artists_without_tilde', []))} found):")
for cat, name in anomalies.get('artists_without_tilde', []):
    print(f"  - [{cat}] {name}")

print("\n5. LOVE LIVE LOOSE ALBUMS METADATA:")
for name, tags in ll_details:
    print(f"  - {name}\n      Tags: {tags}")

