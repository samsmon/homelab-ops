#!/usr/bin/env python3
import os

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

targets = [
    # 1. Towatsugai
    os.path.join(BASE_DIR, "Game", "Towatsugai (トワツガイ) ~", "トワツガイ キャラクターソング「灰の棺／回転木馬とワルツ／花に願いを／偽りの救済／罪と罰／空の人魚」"),
    os.path.join(BASE_DIR, "Game", "Towatsugai (トワツガイ) ~", "トワツガイ キャラクターソング灰の棺／回転木馬とワルツ／花に願いを／偽りの救済／罪と罰／空の人魚」"),

    # 2. Rokudenashi
    os.path.join(BASE_DIR, "J-Pop", "Rokudenashi (ロクデナシ) ~", "ユリイカ [VTCL-35376]"),
    os.path.join(BASE_DIR, "J-Pop", "Rokudenashi (ロクデナシ) ~", "ユリイカ"),
    os.path.join(BASE_DIR, "J-Pop", "Rokudenashi (ロクデナシ) ~", "ユリイカ [初回限定盤]"),

    # 3. Hatsune Miku Magical Mirai 2024
    os.path.join(BASE_DIR, "Vocaloid", "Hatsune Miku Magical Mirai (初音ミク マジカルミライ) ~", "初音ミク「マジカルミライ 2024」OFFICIAL ALBUM"),
    os.path.join(BASE_DIR, "Vocaloid", "Hatsune Miku Magical Mirai (初音ミク マジカルミライ) ~", "初音ミク「マジカルミライ 2024」OFFICIAL ALBUM (Hatsune Miku 'Magical Mirai 2024' OFFICIAL ALBUM)"),

    # 4. 2.5 Jigen no Ririsa
    os.path.join(BASE_DIR, "Anime", "2.5 Jigen no Ririsa (2.5次元の誘惑) ~", "Watch Me (Digital Single)"),
    os.path.join(BASE_DIR, "Anime", "2.5 Jigen no Ririsa (2.5次元の誘惑) ~", "Watch Me"),
]

for t in targets:
    print(f"\nChecking: {t}")
    if os.path.exists(t):
        for f in os.listdir(t):
            size = os.path.getsize(os.path.join(t, f)) if os.path.isfile(os.path.join(t, f)) else "DIR"
            print(f"  {f} ({size})")
    else:
        print("  DOES NOT EXIST")
