#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inspect the cover images, metadata, and distinguishing characteristics of:
1. Birthday releases
2. Solo releases
3. Solo Special releases
4. Physical CD Singles
5. Event Trio Combinations
6. All Stars / Group Anthems
7. Special Units & Media tie-ins
"""
import os
from pathlib import Path
from PIL import Image

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime/学園アイドルマスター ~')

def get_img_info(d):
    imgs = list(d.glob('*.jpg')) + list(d.glob('*.png')) + list(d.glob('*.webp'))
    if not imgs:
        # check parent or child
        for sub in d.iterdir():
            if sub.is_dir():
                imgs.extend(list(sub.glob('*.jpg')) + list(sub.glob('*.png')))
    res = []
    for img in imgs[:3]:
        try:
            with Image.open(img) as im:
                res.append(f"{img.name} ({im.size[0]}x{im.size[1]}, {img.stat().st_size/1024:.0f}KB)")
        except Exception:
            res.append(img.name)
    return res

samples = [
    # 1. Birthday
    ("Birthday (Temari)", BASE / "02. 月村手毬 (Temari Tsukimura)" / "月村手毬 (CV.小鹿なお) - 叶えたい、ことばかり"),
    ("Birthday (China)", BASE / "06. 倉本千奈 (China Kuramoto)" / "倉本千奈(CV.伊藤舞音) - 憧れをいっぱい [FLAC 96kHz／24bit]"),
    ("Birthday (Lilja)", BASE / "05. 葛城リーリヤ (Lilja Katsuragi)" / "葛城リーリヤ(CV.花岩香奈) - Wake up!!"),
    
    # 2. Solo (Hi-Res Digital Launch)
    ("Solo Launch (Saki)", BASE / "01. 花海咲季 (Saki Hanami)" / "花海咲季(CV.長月あおい) - Fighting My Way"),
    ("Solo Launch (Hiro)", BASE / "08. 篠澤広 (Hiro Shinosawa)" / "篠澤広(CV.川村玲奈) - 光景"),
    ("Solo Later (Saki 2025)", BASE / "01. 花海咲季 (Saki Hanami)" / "[2025.04.02] 学園アイドルマスター 花海咲季 - Try it now [FLAC 96kHz／24bit]"),
    
    # 3. Solo Special (Second solo song / Game True End songs)
    ("Solo Special (Kotone)", BASE / "03. 藤田ことね (Kotone Fujita)" / "藤田ことね(CV.飯田ヒカル) - Yellow Big Bang!"),
    ("Solo Special (Mao)", BASE / "04. 有村麻央 (Mao Arimura)" / "有村麻央(CV.七瀬つむぎ) - Feel Jewel Dream [FLAC 96kHz／24bit]"),
    
    # 4. CD Singles (Physical Launch)
    ("CD Single (Saki)", BASE / "01. 花海咲季 (Saki Hanami)" / "花海咲季 1stシングル「Fighting My Way」[FLAC+BK]"),
    ("CD Single (Kotone)", BASE / "03. 藤田ことね (Kotone Fujita)" / "藤田ことね 1stシングル「世界一可愛い私」[FLAC+BK]"),
    
    # 5. Event Songs (Trio)
    ("Trio Combo (ENDLESS DANCE)", BASE / "00. 全体曲・ユニット (All Stars & Units)" / "Event Songs (Trio Ver)" / "ENDLESS DANCE" / "[2025.07.26] 学園アイドルマスター - ENDLESS DANCE (花海咲季・月村手毬・藤田ことね Ver.) [FLAC 96kHz／24bit]"),
    ("Trio Combo (Howling)", BASE / "00. 全体曲・ユニット (All Stars & Units)" / "Event Songs (Trio Ver)" / "Howling over the World" / "Howling over the World (花海咲季・月村手毬・藤田ことね Ver.) [FLAC 96kHz／24bit]"),
    
    # 6. All Stars / Seasons
    ("All Stars (Campus mode)", BASE / "00. 全体曲・ユニット (All Stars & Units)" / "全體曲 Campus mode!! [96kHz／24bit][FLAC]"),
    ("Season (Semi-blue)", BASE / "00. 全体曲・ユニット (All Stars & Units)" / "キミとセミブルー"),
    ("Season (Hatsumairi)", BASE / "00. 全体曲・ユニット (All Stars & Units)" / "[2025.02.02] 学園アイドルマスター - ハッピーミルフィーユ [FLAC 96kHz／24bit]"),
    
    # 7. Media Tie-in & Unit
    ("Manga CD (GOLD RUSH)", BASE / "03. 藤田ことね (Kotone Fujita)" / "[2025.02.07] 学園アイドルマスター GOLD RUSH (1) オリジナルCD「かちドキ」／藤田ことね [FLAC+BK]"),
    ("Unit (Begrazia)", BASE / "00. 全体曲・ユニット (All Stars & Units)" / "Begrazia" / "[2025.08.01] 学園アイドルマスター Begrazia - Star-mine [FLAC 96kHz／24bit]"),
]

for label, p in samples:
    print(f"\n=== {label} ===")
    if p.exists():
        imgs = get_img_info(p)
        flacs = [f.name for f in p.glob('*.flac')]
        print(f"  Path: {p.name}")
        print(f"  Images: {', '.join(imgs)}")
        print(f"  Tracks ({len(flacs)}): {flacs[:4]}")
    else:
        print(f"  NOT FOUND: {p}")
