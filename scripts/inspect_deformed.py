#!/usr/bin/env python3
import os

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

folders = [
    os.path.join(BASE_DIR, "J-Pop", "Sakurariumu ( Yuu Nagi Michiru ) (yunagi Michiru) (サクラリウム (夕凪みちる) (Yunagi Michiru)) ~"),
    os.path.join(BASE_DIR, "J-Pop", "Kisaragi Kozue (priere * ) (如月梢 (Priere＊)) ~"),
    os.path.join(BASE_DIR, "J-Pop", "Kokoro Hana Gaku ( No Hana Koyori ) (心花学 (乃花こより)) ~"),
    os.path.join(BASE_DIR, "Anime", "Maebashi Witches (前橋ウィッチーズ) ~"),
    os.path.join(BASE_DIR, "Game", "Towatsugai (トワツガイ) ~"),
]

for f in folders:
    print(f"\nChecking: {f}")
    if os.path.exists(f):
        for item in sorted(os.listdir(f)):
            print(f"  {item}")
    else:
        print("  DOES NOT EXIST")
