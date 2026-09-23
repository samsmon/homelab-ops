#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classify all 67 releases into Solo, Duo, Trio, and Unit/All Stars.
"""
import re
from pathlib import Path

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime/学園アイドルマスター ~')

# Map of all 67 releases
data = [
    # Solo releases
    ("01. 花海咲季", "花海咲季 1stシングル「Fighting My Way」[FLAC+BK]", ["花海咲季"], "Fighting My Way [1st Single CD-FLAC]"),
    ("01. 花海咲季", "花海咲季(CV.長月あおい) - Fighting My Way", ["花海咲季"], "Fighting My Way [FLAC 96kHz／24bit]"),
    ("01. 花海咲季", "花海咲季(CV.長月あおい) - Boom Boom Pow", ["花海咲季"], "Boom Boom Pow [FLAC 96kHz／24bit]"),
    ("01. 花海咲季", "[2025.04.02] 学園アイドルマスター 花海咲季 - Try it now [FLAC 96kHz／24bit]", ["花海咲季"], "Try it now [FLAC 96kHz／24bit]"),
    
    ("02. 月村手毬", "月村手毬 1stシングル「Luna say maybe」[FLAC+BK]", ["月村手毬"], "Luna say maybe [1st Single CD-FLAC]"),
    ("02. 月村手毬", "月村手毬(CV.小鹿なお) - Luna say maybe", ["月村手毬"], "Luna say maybe [FLAC 96kHz／24bit]"),
    ("02. 月村手毬", "月村手毬(CV.小鹿なお) - アイヴイ", ["月村手毬"], "アイヴイ [FLAC 96kHz／24bit]"),
    ("02. 月村手毬", "月村手毬 (CV.小鹿なお) - 叶えたい、ことばかり", ["月村手毬"], "叶えたい、ことばかり [FLAC]"),
    
    ("03. 藤田ことね", "藤田ことね 1stシングル「世界一可愛い私」[FLAC+BK]", ["藤田ことね"], "世界一可愛い私 [1st Single CD-FLAC]"),
    ("03. 藤田ことね", "藤田ことね(CV.飯田ヒカル) - 世界一可愛い私", ["藤田ことね"], "世界一可愛い私 [FLAC 96kHz／24bit]"),
    ("03. 藤田ことね", "藤田ことね(CV.飯田ヒカル) - Yellow Big Bang!", ["藤田ことね"], "Yellow Big Bang! [FLAC 96kHz／24bit]"),
    ("03. 藤田ことね", "[2025.02.07] 学園アイドルマスター GOLD RUSH (1) オリジナルCD「かちドキ」／藤田ことね(CV.飯田ヒカル) [FLAC+BK]", ["藤田ことね"], "かちドキ [GOLD RUSH CD-FLAC]"),
    ("03. 藤田ことね", "[2025.08.13] 学園アイドルマスター 藤田ことね - 自己肯定感爆上げ↑↑しゅきしゅきソング [FLAC 96kHz／24bit]", ["藤田ことね"], "自己肯定感爆上げ↑↑しゅきしゅきソング [FLAC 96kHz／24bit]"),
    
    ("04. 有村麻央", "有村麻央(CV.七瀬つむぎ) - Fluorite", ["有村麻央"], "Fluorite [FLAC 96kHz／24bit]"),
    ("04. 有村麻央", "有村麻央(CV.七瀬つむぎ) - Feel Jewel Dream [FLAC 96kHz／24bit]", ["有村麻央"], "Feel Jewel Dream [FLAC 96kHz／24bit]"),
    ("04. 有村麻央", "[2025.01.18] 学園アイドルマスター 有村麻央 - Sweet Magic [FLAC 96kHz／24bit]", ["有村麻央"], "Sweet Magic [FLAC 96kHz／24bit]"),
    ("04. 有村麻央", "[2025.03.19] 学園アイドルマスター 有村麻央 - Top Secret [FLAC 96kHz／24bit]", ["有村麻央"], "Top Secret [FLAC 96kHz／24bit]"),
    
    ("05. 葛城リーリヤ", "葛城リーリヤ(CV.花岩香奈) - 白線", ["葛城リーリヤ"], "白線 [FLAC 96kHz／24bit]"),
    ("05. 葛城リーリヤ", "葛城リーリヤ(CV.花岩香奈) - Wake up!!", ["葛城リーリヤ"], "Wake up!! [FLAC]"),
    ("05. 葛城リーリヤ", "[2025.03.22] 学園アイドルマスター 葛城リーリヤ - 極光 [FLAC 96kHz／24bit]", ["葛城リーリヤ"], "極光 [FLAC 96kHz／24bit]"),
    ("05. 葛城リーリヤ", "[2025.03.26] 学園アイドルマスター 葛城リーリヤ - Fragile Heart [FLAC 96kHz／24bit]", ["葛城リーリヤ"], "Fragile Heart [FLAC 96kHz／24bit]"),
    
    ("06. 倉本千奈", "倉本千奈(CV.伊藤舞音) - Wonder Scale", ["倉本千奈"], "Wonder Scale [FLAC 96kHz／24bit]"),
    ("06. 倉本千奈", "倉本千奈(CV.伊藤舞音) - 日々、発見的ステップ！ [FLAC 96kHz／24bit]", ["倉本千奈"], "日々、発見的ステップ！ [FLAC 96kHz／24bit]"),
    ("06. 倉本千奈", "倉本千奈(CV.伊藤舞音) - 憧れをいっぱい [FLAC 96kHz／24bit]", ["倉本千奈"], "憧れをいっぱい [FLAC 96kHz／24bit]"),
    ("06. 倉本千奈", "[2025.03.19] 学園アイドルマスター 倉本千奈 - ときめきのソルフェージュ [FLAC 96kHz／24bit]", ["倉本千奈"], "ときめきのソルフェージュ [FLAC 96kHz／24bit]"),
    ("06. 倉本千奈", "[2025.10.22] 学園アイドルマスター 倉本千奈 - 空と約束 [FLAC 96kHz／24bit]", ["倉本千奈"], "空と約束 [FLAC 96kHz／24bit]"),
    
    ("07. 紫雲清夏", "紫雲清夏(CV.湊みや) - Tame-Lie-One-Step", ["紫雲清夏"], "Tame-Lie-One-Step [FLAC 96kHz／24bit]"),
    ("07. 紫雲清夏", "[2024.11.11] 学園アイドルマスター 紫雲清夏(CV.湊みや) - Ride on Beat [FLAC 96kHz／24bit]", ["紫雲清夏"], "Ride on Beat [FLAC 96kHz／24bit]"),
    ("07. 紫雲清夏", "[2025.03.26] 学園アイドルマスター 紫雲清夏 - Kira Kira [FLAC 96kHz／24bit]", ["紫雲清夏"], "Kira Kira [FLAC 96kHz／24bit]"),
    
    ("08. 篠澤広", "篠澤広(CV.川村玲奈) - 光景", ["篠澤広"], "光景 [FLAC 96kHz／24bit]"),
    ("08. 篠澤広", "篠澤広(CV.川村玲奈) - コントラスト", ["篠澤広"], "コントラスト [FLAC 96kHz／24bit]"),
    ("08. 篠澤広", "[2025.03.19] 学園アイドルマスター 篠澤広 - コンテンポラリのダンス [FLAC 96kHz／24bit]", ["篠澤広"], "コンテンポラリのダンス [FLAC 96kHz／24bit]"),
    
    ("09. 姫崎莉波", "姫崎莉波(CV.薄井友里) - clumsy trick", ["姫崎莉波"], "clumsy trick [FLAC 96kHz／24bit]"),
    ("09. 姫崎莉波", "姫崎莉波(CV.薄井友里) - L.U.V [FLAC 96kHz／24bit]", ["姫崎莉波"], "L.U.V [FLAC 96kHz／24bit]"),
    ("09. 姫崎莉波", "[2025.03.26] 学園アイドルマスター 姫崎莉波 - 歌声は君いろ [FLAC 96kHz／24bit]", ["姫崎莉波"], "歌声は君いろ [FLAC 96kHz／24bit]"),
    
    ("10. 花海佑芽", "花海佑芽(CV.松田彩音) - The Rolling Riceball", ["花海佑芽"], "The Rolling Riceball [FLAC 96kHz／24bit]"),
    ("10. 花海佑芽", "[2025.04.01] 学園アイドルマスター 花海佑芽 - つよつよ最強エクササイズ [FLAC 96kHz／24bit]", ["花海佑芽"], "つよつよ最強エクササイズ [FLAC 96kHz／24bit]"),
    
    ("11. 秦谷美鈴", "[2025.02.06] 学園アイドルマスター 秦谷美鈴 - たいせつなもの [FLAC 96kHz／24bit]", ["秦谷美鈴"], "たいせつなもの [FLAC 96kHz／24bit]"),
    ("11. 秦谷美鈴", "[2025.02.07] 学園アイドルマスター 秦谷美鈴 - ツキノカメ [FLAC 96kHz／24bit]", ["秦谷美鈴"], "ツキノカメ [FLAC 96kHz／24bit]"),
    
    ("12. 十王星南", "[2024.11.16] 学園アイドルマスター 十王星南(CV.陽高真白) - 小さな野望 [FLAC 96kHz／24bit]", ["十王星南"], "小さな野望 [FLAC 96kHz／24bit]"),
    
    ("13. 雨夜燕", "[2025.11.16] 学園アイドルマスター 雨夜燕 - 理論武装して [FLAC 96kHz／24bit]", ["雨夜燕"], "理論武装して [FLAC 96kHz／24bit]"),
]

# Print Solo count
print(f"Total Solo Releases: {len(data)}")
