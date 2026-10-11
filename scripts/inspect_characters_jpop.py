#!/usr/bin/env python3
import mutagen
from pathlib import Path

jpop = Path('/mnt/hdd-backup/music/Lossless/J-Pop')

for target in ['Nishiura Sora (cv. Aikawa Nao ) (西浦そら(CV.相川奈央)) ~', 'Yura (cv. Oonishi Saori ) (ユラ(CV.大西沙織)) ~']:
    p = jpop / target
    if p.exists():
        flacs = list(p.rglob('*.flac'))
        if flacs:
            f = mutagen.File(flacs[0])
            print(f"=== {target} ===")
            print("  artist:", f.get('artist'))
            print("  album:", f.get('album'))
            print("  title:", f.get('title'))
