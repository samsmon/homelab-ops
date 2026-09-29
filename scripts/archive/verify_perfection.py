#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

LOSSLESS_ROOT = Path('/mnt/hdd-backup/music/Lossless')

print("=" * 80)
print("FINAL HEALTH VERIFICATION ACROSS LOSSLESS LIBRARY")
print("=" * 80)

# 1. Total counts by category
for cat in ['Anime', 'J-Pop', 'Vtuber', 'Doujinshi', 'Vocaloid', 'Global']:
    p = LOSSLESS_ROOT / cat
    if p.exists():
        dirs = [x for x in p.iterdir() if x.is_dir()]
        print(f"  Category [{cat}]: {len(dirs)} artist / franchise folders")

# 2. Key franchises audit
FRANCHISES = {
    'Bocchi the Rock!': LOSSLESS_ROOT / 'Anime' / 'Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~',
    'THE IDOLM@STER': LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~',
    'Love Live!': LOSSLESS_ROOT / 'Anime' / 'Love Live! (ラブライブ！) ~',
    'BanG Dream!': LOSSLESS_ROOT / 'Anime' / 'BanG Dream! (バンドリ！) ~',
    'Uma Musume': LOSSLESS_ROOT / 'Anime' / 'Uma Musume (ウマ娘) ~',
    'Hololive': LOSSLESS_ROOT / 'Vtuber' / 'Hololive (ホロライブ) ~',
    'Nijisanji': LOSSLESS_ROOT / 'Vtuber' / 'Nijisanji (にじさんじ) ~',
}

print("\nFranchise Health Check (Loose items count):")
for name, path in FRANCHISES.items():
    if not path.exists():
        print(f"  [{name}]: NOT FOUND")
        continue
    loose = [x.name for x in path.iterdir() if not x.name.endswith('~') and not x.name.startswith(('[2022', '[2023', '01.', '02.', '03.', '04.', '05.', '06.', '07.', '08.'))]
    subdirs = [x.name for x in path.iterdir() if x.is_dir()]
    print(f"  [{name}]: {len(subdirs)} subfolders | Loose items: {len(loose)}")
    if loose:
        print(f"     -> Loose: {loose}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
