#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import shutil

LOSSLESS = Path('/mnt/hdd-backup/music/Lossless')

def safe_move(src, dst):
    if not src.exists() or src == dst:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if src.is_dir() and dst.is_dir():
            for child in list(src.iterdir()):
                safe_move(child, dst / child.name)
            try: src.rmdir()
            except Exception: pass
            return
    shutil.move(str(src), str(dst))

# Fix Vocaloid remaining non-ascii
voc = LOSSLESS / 'Vocaloid'
voc_fixes = [
    ('初音ミク マジカルミライ ~', voc / 'Hatsune Miku Magical Mirai (初音ミク マジカルミライ) ~'),
    ('ぬぬぬぬぬぬぬぬぬぬぬぬぬぬぬぬ ~', voc / 'Nununununununununununununununu (ぬぬぬぬぬぬぬぬぬぬぬぬぬぬぬぬ) ~'),
    ('八王子P ~', voc / 'Hachioji P (八王子P) ~'),
    ('椎乃味醂 ~', voc / 'Sheeno Mirin (椎乃味醂) ~'),
    ('＊Luna feat. ねんね ~', LOSSLESS / 'J-Pop' / '*Luna ~' / 'ねんね'),
]
for old_name, dst in voc_fixes:
    p = voc / old_name
    if p.exists():
        safe_move(p, dst)

# Fix J-Pop remaining
jpop = LOSSLESS / 'J-Pop'
jpop_fixes = [
    ('≠ME ~', jpop / 'Not Equal Me (≠ME) ~'),
    ('≒JOY ~', jpop / 'Nearly Equal Joy (≒JOY) ~'),
    ('Карамазовы ~', jpop / 'Karamazovy (Карамазовы) ~'),
    ('¿？shimon ~', jpop / 'Shimon (¿？shimon) ~'),
]
for old_name, dst in jpop_fixes:
    p = jpop / old_name
    if p.exists():
        safe_move(p, dst)

# Merge all *Luna / ∗Luna / ＊Luna in J-Pop into '*Luna ~'
luna_target = jpop / '*Luna ~'
luna_target.mkdir(parents=True, exist_ok=True)
for p in list(jpop.iterdir()):
    if 'Luna' in p.name and p != luna_target:
        for item in list(p.iterdir()):
            safe_move(item, luna_target / item.name)
        try: p.rmdir()
        except Exception: pass

print("Remaining 11 fixed.")
