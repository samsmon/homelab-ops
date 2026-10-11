#!/usr/bin/env python3
import os
from pathlib import Path

gakumas = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~')

print("=" * 80)
print("FULL TREE OF GAKUMAS")
print("=" * 80)

for root, dirs, files in os.walk(gakumas):
    rel = Path(root).relative_to(gakumas)
    depth = len(rel.parts)
    indent = "  " * depth
    flac_files = [f for f in files if f.endswith('.flac')]
    cue_files = [f for f in files if f.endswith('.cue')]
    other_files = [f for f in files if not f.endswith('.flac') and not f.endswith('.cue')]
    
    print(f"{indent}[DIR] {Path(root).name}  (flacs: {len(flac_files)}, cue: {len(cue_files)}, other: {len(other_files)})")
    if depth >= 2 and len(flac_files) > 0:
        for fl in sorted(flac_files)[:3]:
            print(f"{indent}   - {fl}")
        if len(flac_files) > 3:
            print(f"{indent}   - ... and {len(flac_files)-3} more flacs")
