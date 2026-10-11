#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import shutil

vspo = Path('/mnt/hdd-backup/music/Lossless/Vtuber/VSPO (ぶいすぽっ！) ~')
vtuber = Path('/mnt/hdd-backup/music/Lossless/Vtuber')

indie_list = [
    'Aitsuki Nakuru (藍月なくる) ~', 'Akami Karubi (赤見かるび) ~', 'Aogiri Koukou (あおぎり高校) ~',
    'Choten-chan (超てんちゃん) ~', 'DAZBEE (ダズビー) ~', 'Kagura Mea (神楽めあ) ~',
    'Kikirara Vivi (綺々羅々ヴィヴィ) ~', 'Kuon Tama (久遠たま) ~', 'Lunacchi Hoshi (るなっち☆ほし) ~',
    'Nanami Urara (七海うらら) ~', 'Natori Sana (名取さな) ~', 'Shigure Ui (しぐれうい) ~', 'VALIS ~'
]

for name in indie_list:
    src = vspo / name
    dst = vtuber / name
    if src.exists():
        if dst.exists():
            for child in list(src.iterdir()):
                shutil.move(str(child), str(dst / child.name))
            src.rmdir()
        else:
            shutil.move(str(src), str(dst))
        print(f"Moved {name} to Vtuber root.")

print("VSPO cleaned.")
