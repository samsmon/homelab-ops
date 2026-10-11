#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess

root = Path("/mnt/hdd-backup/music/Lossless/J-Pop")
targets = [
    "イロアワセ キャラクターソングHIRAETH」 ~",
    "遙かなるエルドラド テーマソング「Gilded Dreams」 ~",
    "MEDA ~"
]

for target in targets:
    p = root / target
    if p.exists():
        print(f"=== {target} ===")
        for item in p.iterdir():
            print(f"  {item.name}")
            flacs = list(item.glob("**/*.flac")) if item.is_dir() else ([item] if item.suffix == ".flac" else [])
            if flacs:
                res = subprocess.check_output(
                    ["ffprobe", "-show_entries", "format_tags=artist,album,title", "-of", "default=noprint_wrappers=1", str(flacs[0])],
                    text=True, stderr=subprocess.DEVNULL
                )
                print("    Tags:", " | ".join(res.strip().splitlines()))
