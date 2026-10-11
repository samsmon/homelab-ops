#!/usr/bin/env python3
import os

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

for target in [
    os.path.join(BASE_DIR, "J-Pop", "TrySail (トライセイル) ~"),
    os.path.join(BASE_DIR, "J-Pop", "Akari Kito (鬼頭明里) ~"),
    os.path.join(BASE_DIR, "J-Pop", "Riria . (りりあ。) ~"),
    os.path.join(BASE_DIR, "Anime", "D4DJ (ディーフォーディージェー) ~"),
]:
    print(f"\nTarget: {target}")
    if os.path.exists(target):
        for item in sorted(os.listdir(target)):
            print(f"  {item}")
    else:
        print("  DOES NOT EXIST")
