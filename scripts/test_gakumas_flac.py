#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime')
imas_gakumas = BASE / 'Im@s ~' / '学園アイドルマスター'
flat_gakumas = BASE / '学園アイドルマスター ~'

print("Testing all audio files in Gakumas...")
corrupt = []
tested = 0

for p in [imas_gakumas, flat_gakumas]:
    if not p.exists():
        continue
    for f in p.rglob('*.flac'):
        tested += 1
        res = subprocess.run(['flac', '-t', '-s', str(f)], capture_output=True)
        if res.returncode != 0:
            corrupt.append(f)

print(f"Tested {tested} FLAC files. Corrupted: {len(corrupt)}")
for c in corrupt:
    print(f"  CORRUPT: {c}")
