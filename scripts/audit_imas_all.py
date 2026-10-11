#!/usr/bin/env python3
import os
from pathlib import Path

imas = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~')

print("=" * 80)
print("AUDITING ALL IMAS SUBFRANCHISES")
print("=" * 80)

for sub in sorted(imas.iterdir()):
    if not sub.is_dir():
        continue
    loose_files = [f.name for f in sub.iterdir() if f.is_file()]
    subdirs = [d.name for d in sub.iterdir() if d.is_dir()]
    print(f"\nSubfranchise: {sub.name} (files: {len(loose_files)}, dirs: {len(subdirs)})")
    if loose_files:
        print(f"  LOOSE FILES: {loose_files}")
    for d in sorted(subdirs):
        p = sub / d
        sub_files = [f.name for f in p.iterdir() if f.is_file()]
        sub_dirs = [s.name for s in p.iterdir() if s.is_dir()]
        print(f"    - {d} (files: {len(sub_files)}, dirs: {len(sub_dirs)})")
