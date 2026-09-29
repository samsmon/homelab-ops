#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

p1 = Path('/mnt/hdd-backup/music/Lossless/Anime/Im@s ~/学園アイドルマスター/Singles/花海咲季 1stシングル「Fighting My Way」[FLAC+BK]')
p2 = Path('/mnt/hdd-backup/music/Lossless/Anime/Im@s ~/学園アイドルマスター/Solo/花海咲季(CV.長月あおい) - Fighting My Way')

print("--- Singles ---")
if p1.exists():
    for f in p1.iterdir():
        print(f"  {f.name} ({f.stat().st_size} bytes)")

print("\n--- Solo ---")
if p2.exists():
    for f in p2.iterdir():
        print(f"  {f.name} ({f.stat().st_size} bytes)")

p3 = Path('/mnt/hdd-backup/music/Lossless/Anime/Im@s ~/学園アイドルマスター/Singles/月村手毬 1stシングル「Luna say maybe」[FLAC+BK]')
p4 = Path('/mnt/hdd-backup/music/Lossless/Anime/Im@s ~/学園アイドルマスター/Solo/月村手毬(CV.小鹿なお) - Luna say maybe')

print("\n--- Temari Singles ---")
if p3.exists():
    for f in p3.iterdir():
        print(f"  {f.name} ({f.stat().st_size} bytes)")

print("\n--- Temari Solo ---")
if p4.exists():
    for f in p4.iterdir():
        print(f"  {f.name} ({f.stat().st_size} bytes)")
