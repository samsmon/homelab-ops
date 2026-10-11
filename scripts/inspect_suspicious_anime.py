#!/usr/bin/env python3
import os

BASE = '/mnt/hdd-backup/music/Lossless/Anime'
folders_to_check = [
    'テトリス ~',
    'バクプリチャンネル ~',
    'うたの☆プリンセスさまっ♪ ~',
    'GEMS COMPANY ~',
    'Princess Letter(s)! ~',
    '魔王2099 ~',
    '女神のカフェテラス ~',
    'ウルトラマンアーク ~',
    'スローループ (Slow Loop) ~',
    'ゆるキャン△ (Yuru Camp) ~',
    'ソードアート・オンライン (SAO) ~',
    'Fate (Series) ~'
]

for f in folders_to_check:
    fp = os.path.join(BASE, f)
    print(f"\n=== {f} ===")
    if not os.path.exists(fp):
        print("  DOES NOT EXIST")
        continue
    for root, dirs, files in os.walk(fp):
        rel = os.path.relpath(root, fp)
        audio = [x for x in files if x.endswith(('.flac', '.wav', '.mp3'))]
        if audio:
            print(f"  Folder: {rel}")
            for a in audio[:3]:
                print(f"    - {a}")
            if len(audio) > 3:
                print(f"    ... and {len(audio) - 3} more")
