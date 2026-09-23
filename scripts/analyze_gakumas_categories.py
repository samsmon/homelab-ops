#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep analysis of Gakumas release categories:
1. Birthday releases
2. Solo (Initial Debut) releases
3. Solo Special (Second solo / True End) releases
4. Physical CD Singles
5. Trio / Combination Event Songs
6. All Stars / Seasonal Group Anthems
7. Media Tie-in & Units
"""
import os
import subprocess
from pathlib import Path

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime/学園アイドルマスター ~')

def get_tags(flac_path):
    res = subprocess.run(['metaflac', '--export-tags-to=-', str(flac_path)], capture_output=True, text=True)
    tags = {}
    for line in res.stdout.splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            tags[k.upper()] = v
    return tags

categories = {
    'Birthday': [
        BASE / '02. 月村手毬 (Temari Tsukimura)' / '月村手毬 (CV.小鹿なお) - 叶えたい、ことばかり',
        BASE / '05. 葛城リーリヤ (Lilja Katsuragi)' / '葛城リーリヤ(CV.花岩香奈) - Wake up!!',
        BASE / '06. 倉本千奈 (China Kuramoto)' / '倉本千奈(CV.伊藤舞音) - 憧れをいっぱい [FLAC 96kHz／24bit]',
    ],
    'Solo (Debut / 1st Solo)': [
        BASE / '01. 花海咲季 (Saki Hanami)' / '花海咲季(CV.長月あおい) - Fighting My Way',
        BASE / '02. 月村手毬 (Temari Tsukimura)' / '月村手毬(CV.小鹿なお) - Luna say maybe',
        BASE / '03. 藤田ことね (Kotone Fujita)' / '藤田ことね(CV.飯田ヒカル) - 世界一可愛い私',
        BASE / '04. 有村麻央 (Mao Arimura)' / '有村麻央(CV.七瀬つむぎ) - Fluorite',
        BASE / '08. 篠澤広 (Hiro Shinosawa)' / '篠澤広(CV.川村玲奈) - 光景',
    ],
    'Solo Special (True End / 2nd Solo)': [
        BASE / '01. 花海咲季 (Saki Hanami)' / '花海咲季(CV.長月あおい) - Boom Boom Pow',
        BASE / '02. 月村手毬 (Temari Tsukimura)' / '月村手毬(CV.小鹿なお) - アイヴイ',
        BASE / '03. 藤田ことね (Kotone Fujita)' / '藤田ことね(CV.飯田ヒカル) - Yellow Big Bang!',
        BASE / '04. 有村麻央 (Mao Arimura)' / '有村麻央(CV.七瀬つむぎ) - Feel Jewel Dream [FLAC 96kHz／24bit]',
        BASE / '08. 篠澤広 (Hiro Shinosawa)' / '篠澤広(CV.川村玲奈) - コントラスト',
    ],
    'Solo Later (2025 Updates)': [
        BASE / '01. 花海咲季 (Saki Hanami)' / '[2025.04.02] 学園アイドルマスター 花海咲季 - Try it now [FLAC 96kHz／24bit]',
        BASE / '04. 有村麻央 (Mao Arimura)' / '[2025.01.18] 学園アイドルマスター 有村麻央 - Sweet Magic [FLAC 96kHz／24bit]',
        BASE / '04. 有村麻央 (Mao Arimura)' / '[2025.03.19] 学園アイドルマスター 有村麻央 - Top Secret [FLAC 96kHz／24bit]',
        BASE / '06. 倉本千奈 (China Kuramoto)' / '[2025.03.19] 学園アイドルマスター 倉本千奈 - ときめきのソルフェージュ [FLAC 96kHz／24bit]',
        BASE / '07. 紫雲清夏 (Sumika Shiun)' / '[2024.11.11] 学園アイドルマスター 紫雲清夏(CV.湊みや) - Ride on Beat [FLAC 96kHz／24bit]',
    ],
    'Physical CD Singles': [
        BASE / '01. 花海咲季 (Saki Hanami)' / '花海咲季 1stシングル「Fighting My Way」[FLAC+BK]',
        BASE / '02. 月村手毬 (Temari Tsukimura)' / '月村手毬 1stシングル「Luna say maybe」[FLAC+BK]',
        BASE / '03. 藤田ことね (Kotone Fujita)' / '藤田ことね 1stシングル「世界一可愛い私」[FLAC+BK]',
    ],
    'Event Songs (Trio Combinations)': [
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / 'Event Songs (Trio Ver)' / 'Howling over the World' / 'Howling over the World (花海咲季・月村手毬・藤田ことね Ver.) [FLAC 96kHz／24bit]',
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / 'Event Songs (Trio Ver)' / 'がむしゃらに行こう！' / 'がむしゃらに行こう！ (有村麻央・紫雲清夏・篠澤広 Ver.) [FLAC 96kHz／24bit]',
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / 'Event Songs (Trio Ver)' / 'ミラクルナナウ(ﾟ∀ﾟ)！' / 'ミラクルナナウ(ﾟ∀ﾟ)！ (葛城リーリヤ・倉本千奈・姫崎莉波 Ver.) [FLAC 96kHz／24bit]',
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / 'Event Songs (Trio Ver)' / 'ENDLESS DANCE' / '[2025.07.26] 学園アイドルマスター - ENDLESS DANCE (花海咲季・月村手毬・藤田ことね Ver.) [FLAC 96kHz／24bit]',
    ],
    'All Stars & Seasons': [
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / '初 HAJIME',
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / '全體曲 Campus mode!! [96kHz／24bit][FLAC]',
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / 'キミとセミブルー',
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / '冠菊 [FLAC 96kHz／24bit]',
        BASE / '00. 全体曲・ユニット (All Stars & Units)' / '[2024.10.01] 学園アイドルマスター - 仮装狂騒曲 [FLAC 96kHz／24bit]',
    ]
}

for cat_name, folder_list in categories.items():
    print("="*60)
    print(f"CATEGORY: {cat_name}")
    print("="*60)
    for p in folder_list:
        if not p.exists():
            print(f"  Missing: {p.name}")
            continue
        flacs = list(p.glob('*.flac'))
        imgs = list(p.glob('*.jpg')) + list(p.glob('*.png'))
        sample_tag = get_tags(flacs[0]) if flacs else {}
        print(f"\nFolder: {p.name}")
        print(f"  Files: {len(flacs)} FLACs, {len(imgs)} Images ({', '.join(f.name for f in imgs)})")
        print(f"  Album Tag: {sample_tag.get('ALBUM', 'N/A')}")
        print(f"  Artist Tag: {sample_tag.get('ARTIST', 'N/A')}")
        print(f"  Track 1 Title: {sample_tag.get('TITLE', 'N/A')}")
        print(f"  Date Tag: {sample_tag.get('DATE', sample_tag.get('YEAR', 'N/A'))}")
