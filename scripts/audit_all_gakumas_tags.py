#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inspect all 67 releases in Anime/学園アイドルマスター ~:
Extract artist tag, title tag, date tag, and examine whether it's Solo, Duo, Trio, or All Unit.
"""
import os
import subprocess
from pathlib import Path

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime/学園アイドルマスター ~')

def get_flac_tags(flac_path):
    res = subprocess.run(['metaflac', '--export-tags-to=-', str(flac_path)], capture_output=True, text=True)
    tags = {}
    for line in res.stdout.splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            tags[k.upper()] = v
    return tags

all_releases = []
for p in BASE.rglob('*'):
    if p.is_dir() and any(f.suffix.lower() == '.flac' for f in p.iterdir() if f.is_file()):
        flacs = list(p.glob('*.flac'))
        sample_tag = get_flac_tags(flacs[0]) if flacs else {}
        all_releases.append((p, sample_tag, len(flacs)))

print(f"Total releases found: {len(all_releases)}\n")

for p, tags, n_flac in sorted(all_releases, key=lambda x: str(x[0])):
    rel = p.relative_to(BASE)
    artist = tags.get('ARTIST', 'N/A')
    album = tags.get('ALBUM', 'N/A')
    date = tags.get('DATE', tags.get('YEAR', 'N/A'))
    print(f"PATH:   {rel}")
    print(f"  ARTIST: {artist}")
    print(f"  ALBUM:  {album}")
    print(f"  DATE:   {date} | TRACKS: {n_flac}")
    print()
