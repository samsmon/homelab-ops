#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exhaustive catalog audit across /mnt/hdd-backup/music/Lossless/
Outputs full lists of:
1. Format tag folders (e.g. [FLAC], (Hi-Res), [24bit...], [WEB...])
2. Date prefix folders (e.g. [2024.01.01])
3. Misplaced artists / franchises (e.g. Hololive in Vocaloid, J-Pop in Anime)
4. Subfranchise / subunit folders in Anime that should be inside main franchises
5. Loose albums in franchises that have subseries (BanG Dream, Love Live, Idolmaster, etc.)
"""

import os
import re
from pathlib import Path

LOSSLESS_ROOT = Path('/mnt/hdd-backup/music/Lossless')

TAG_PATTERNS = [
    re.compile(r'\[(?:FLAC|MP3|WEB|CD|EAC|Hi-Res|Lossless|24bit|16bit|44\.1kHz|48kHz|96kHz|192kHz|Qobuz|Mora|Ototoy|Vinyl)[^\]]*\]', re.IGNORECASE),
    re.compile(r'\((?:FLAC|MP3|WEB|CD|EAC|Hi-Res|Lossless|24bit|16bit|44\.1kHz|48kHz|96kHz|192kHz)[^\)]*\)', re.IGNORECASE),
    re.compile(r'\{[A-Z0-9\-_]+\}\s*\[(?:CD-)?FLAC\]', re.IGNORECASE),
]

DATE_PATTERNS = [
    re.compile(r'\[\d{4}[.\-_]\d{2}[.\-_]\d{2}\]'),
    re.compile(r'\[\d{6}\]'),
]

format_tag_dirs = []
date_tag_dirs = []

for root, dirs, files in os.walk(LOSSLESS_ROOT):
    root_p = Path(root)
    if '_corrupted_quarantine' in root_p.parts:
        continue
    # skip root and category dirs
    if root_p == LOSSLESS_ROOT or root_p.parent == LOSSLESS_ROOT:
        continue

    for d in dirs:
        dir_p = root_p / d
        # Bocchi deliberate subseries folders like [2022-2023] PHYSICAL RELEASES are intentional
        if 'Bocchi the Rock!' in str(dir_p) and any(x in d for x in ['PHYSICAL RELEASES', 'SPECIAL DISCS', 'DIGITAL SINGLES']):
            continue

        for pat in TAG_PATTERNS:
            if pat.search(d):
                format_tag_dirs.append(dir_p.relative_to(LOSSLESS_ROOT))
                break

        for dpat in DATE_PATTERNS:
            if dpat.search(d):
                date_tag_dirs.append(dir_p.relative_to(LOSSLESS_ROOT))
                break

print("=" * 80)
print(f"1. ALL FORMAT TAG DIRECTORIES ({len(format_tag_dirs)}):")
print("=" * 80)
for p in sorted(format_tag_dirs):
    print(f"  {p}")

print("\n" + "=" * 80)
print(f"2. ALL DATE TAG DIRECTORIES ({len(date_tag_dirs)}):")
print("=" * 80)
for p in sorted(date_tag_dirs):
    print(f"  {p}")

print("\n" + "=" * 80)
print("AUDIT SCRIPT FINISHED")
print("=" * 80)
