#!/usr/bin/env python3
import os
from pathlib import Path

imas = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~')
print(f"IMAS exists: {imas.exists()}")
if imas.exists():
    for p in sorted(imas.iterdir()):
        print(f"  sub: {p.name}")

# Find any gakumas folder
gakumas_dirs = []
for p in imas.rglob('*'):
    if '学園' in p.name or 'gakuen' in p.name.lower() or 'gakumas' in p.name.lower():
        if p.is_dir():
            gakumas_dirs.append(p)

print(f"\nGakumas dirs found: {len(gakumas_dirs)}")
for g in gakumas_dirs:
    print(f"  {g}")
