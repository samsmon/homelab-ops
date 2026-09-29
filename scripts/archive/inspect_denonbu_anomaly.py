#!/usr/bin/env python3
"""
Inspect the 0_00 anomaly folder and map all files/subalbums to their canonical locations.
"""
import os
import glob
from pathlib import Path

BASE_DIR = Path("/mnt/hdd-backup/music/Lossless/Anime/Denonbu (電音部) ~/0_00 (Prod. Funk Uchino)")
VTUBER_ROOT = Path("/mnt/hdd-backup/music/Lossless/Vtuber")
DENONBU_ROOT = Path("/mnt/hdd-backup/music/Lossless/Anime/Denonbu (電音部) ~")

print("=== VTUBER DESTINATION CHECK ===")
# Check for Omaru Polka
polka_dirs = list(VTUBER_ROOT.rglob("*Polka*")) + list(VTUBER_ROOT.rglob("*尾丸*"))
print(f"Polka dirs: {set(d for d in polka_dirs if d.is_dir())}")

# Check for Subaru
subaru_dirs = list(VTUBER_ROOT.rglob("*Subaru*")) + list(VTUBER_ROOT.rglob("*スバル*"))
print(f"Subaru dirs: {set(d for d in subaru_dirs if d.is_dir())}")

# Check for Luna
luna_dirs = list(VTUBER_ROOT.rglob("*Luna*")) + list(VTUBER_ROOT.rglob("*ルーナ*"))
print(f"Luna dirs: {set(d for d in luna_dirs if d.is_dir())}")

# Check for Asu / 明透
asu_dirs = list(VTUBER_ROOT.rglob("*Asu*")) + list(VTUBER_ROOT.rglob("*明透*"))
print(f"Asu dirs: {set(d for d in asu_dirs if d.is_dir())}")

print("\n=== DENONBU 0_00 FILES ===")
for f in BASE_DIR.iterdir():
    if f.is_file():
        print(f"  {f.name} ({f.stat().st_size} bytes)")
