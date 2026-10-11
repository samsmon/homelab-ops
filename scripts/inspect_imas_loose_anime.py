#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

root = Path("/mnt/hdd-backup/music/Lossless/Anime")
names = [
    "シャイニーカラーズ ~", "アルストロメリア ~", "アンティーカ ~", "アンティーカ×シーズ ~",
    "イルミネーションスターズ ~", "イルミネーションスターズ×ノクチル ~", "コメティック ~",
    "シーズ ~", "ストレイライト ~", "ノクチル ~", "放課後クライマックスガールズ ~",
    "放課後クライマックスガールズ×ストレイライト ~", "大崎甘奈 (CV.黒木ほの香) ~",
    "小宮果穂 (CV.河野ひより) ~", "L'Antica ~", "Hatsuboshi Gakuen (初星学園) ~"
]

for name in names:
    p = root / name
    if p.exists():
        subdirs = [x.name for x in p.iterdir() if x.is_dir()]
        files = [x.name for x in p.iterdir() if x.is_file()]
        print(f"[{name}] dirs: {len(subdirs)}, files: {len(files)}")
        for sd in subdirs[:10]:
            print(f"   dir: {sd}")
        for f in files[:5]:
            print(f"   file: {f}")
