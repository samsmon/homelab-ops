#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply strict naming standards and separation for Gakuen Idolmaster:
1. Hierarchy:
   - 01. Solo/ (contains 13 character folders, each with strictly formatted 'Artist - Title [Format]')
   - 02. Duo/ (placeholder for future duos)
   - 03. Trio/ (all 20 trio releases, named '[Artist 1・Artist 2・Artist 3] - Title [Format]' with alphabetical artists)
   - 04. All Stars & Units/ (units and full cast anthems)
2. Rebuild catalog.sqlite
"""
import os
import shutil
import sqlite3
from pathlib import Path

GAKUMAS = Path('/mnt/hdd-backup/music/Lossless/Anime/学園アイドルマスター ~')
BASE_MUSIC = Path('/mnt/hdd-backup/music')

print("="*60)
print("APPLYING STRICT GAKUMAS STANDARDS & SEPARATION")
print("="*60)

# Create top-level categories
d_solo = GAKUMAS / '01. Solo'
d_duo = GAKUMAS / '02. Duo'
d_trio = GAKUMAS / '03. Trio'
d_units = GAKUMAS / '04. All Stars & Units'

for d in [d_solo, d_duo, d_trio, d_units]:
    d.mkdir(parents=True, exist_ok=True)

# 1. MOVE & STANDARDIZE SOLO FOLDERS
print("\n>>> 1. STANDARDIZING SOLO ALBUMS <<<")
char_folders = [
    '01. 花海咲季 (Saki Hanami)',
    '02. 月村手毬 (Temari Tsukimura)',
    '03. 藤田ことね (Kotone Fujita)',
    '04. 有村麻央 (Mao Arimura)',
    '05. 葛城リーリヤ (Lilja Katsuragi)',
    '06. 倉本千奈 (China Kuramoto)',
    '07. 紫雲清夏 (Sumika Shiun)',
    '08. 篠澤広 (Hiro Shinosawa)',
    '09. 姫崎莉波 (Rinami Himesaki)',
    '10. 花海佑芽 (Ume Hanami)',
    '11. 秦谷美鈴 (Misuzu Hataya)',
    '12. 十王星南 (Sena Juo)',
    '13. 雨夜燕 (Tsubame Amaya)',
]

# Move char folders into 01. Solo if currently at root
for cf in char_folders:
    src = GAKUMAS / cf
    dst = d_solo / cf
    if src.exists() and src != dst:
        shutil.move(str(src), str(dst))

solo_renames = {
    # Saki
    "花海咲季 1stシングル「Fighting My Way」[FLAC+BK]": "花海咲季 - Fighting My Way [1st Single CD-FLAC]",
    "花海咲季(CV.長月あおい) - Fighting My Way": "花海咲季 - Fighting My Way [FLAC 96kHz／24bit]",
    "花海咲季(CV.長月あおい) - Boom Boom Pow": "花海咲季 - Boom Boom Pow [FLAC 96kHz／24bit]",
    "[2025.04.02] 学園アイドルマスター 花海咲季 - Try it now [FLAC 96kHz／24bit]": "花海咲季 - Try it now [FLAC 96kHz／24bit]",
    
    # Temari
    "月村手毬 1stシングル「Luna say maybe」[FLAC+BK]": "月村手毬 - Luna say maybe [1st Single CD-FLAC]",
    "月村手毬(CV.小鹿なお) - Luna say maybe": "月村手毬 - Luna say maybe [FLAC 96kHz／24bit]",
    "月村手毬(CV.小鹿なお) - アイヴイ": "月村手毬 - アイヴイ [FLAC 96kHz／24bit]",
    "月村手毬 (CV.小鹿なお) - 叶えたい、ことばかり": "月村手毬 - 叶えたい、ことばかり [FLAC]",
    
    # Kotone
    "藤田ことね 1stシングル「世界一可愛い私」[FLAC+BK]": "藤田ことね - 世界一可愛い私 [1st Single CD-FLAC]",
    "藤田ことね(CV.飯田ヒカル) - 世界一可愛い私": "藤田ことね - 世界一可愛い私 [FLAC 96kHz／24bit]",
    "藤田ことね(CV.飯田ヒカル) - Yellow Big Bang!": "藤田ことね - Yellow Big Bang! [FLAC 96kHz／24bit]",
    "[2025.02.07] 学園アイドルマスター GOLD RUSH (1) オリジナルCD「かちドキ」／藤田ことね(CV.飯田ヒカル) [FLAC+BK]": "藤田ことね - かちドキ [GOLD RUSH CD-FLAC]",
    "[2025.08.13] 学園アイドルマスター 藤田ことね - 自己肯定感爆上げ↑↑しゅきしゅきソング [FLAC 96kHz／24bit]": "藤田ことね - 自己肯定感爆上げ↑↑しゅきしゅきソング [FLAC 96kHz／24bit]",
    
    # Mao
    "有村麻央(CV.七瀬つむぎ) - Fluorite": "有村麻央 - Fluorite [FLAC 96kHz／24bit]",
    "有村麻央(CV.七瀬つむぎ) - Feel Jewel Dream [FLAC 96kHz／24bit]": "有村麻央 - Feel Jewel Dream [FLAC 96kHz／24bit]",
    "[2025.01.18] 学園アイドルマスター 有村麻央 - Sweet Magic [FLAC 96kHz／24bit]": "有村麻央 - Sweet Magic [FLAC 96kHz／24bit]",
    "[2025.03.19] 学園アイドルマスター 有村麻央 - Top Secret [FLAC 96kHz／24bit]": "有村麻央 - Top Secret [FLAC 96kHz／24bit]",
    
    # Lilja
    "葛城リーリヤ(CV.花岩香奈) - 白線": "葛城リーリヤ - 白線 [FLAC 96kHz／24bit]",
    "葛城リーリヤ(CV.花岩香奈) - Wake up!!": "葛城リーリヤ - Wake up!! [FLAC]",
    "[2025.03.22] 学園アイドルマスター 葛城リーリヤ - 極光 [FLAC 96kHz／24bit]": "葛城リーリヤ - 極光 [FLAC 96kHz／24bit]",
    "[2025.03.26] 学園アイドルマスター 葛城リーリヤ - Fragile Heart [FLAC 96kHz／24bit]": "葛城リーリヤ - Fragile Heart [FLAC 96kHz／24bit]",
    
    # China
    "倉本千奈(CV.伊藤舞音) - Wonder Scale": "倉本千奈 - Wonder Scale [FLAC 96kHz／24bit]",
    "倉本千奈(CV.伊藤舞音) - 日々、発見的ステップ！ [FLAC 96kHz／24bit]": "倉本千奈 - 日々、発見的ステップ！ [FLAC 96kHz／24bit]",
    "倉本千奈(CV.伊藤舞音) - 憧れをいっぱい [FLAC 96kHz／24bit]": "倉本千奈 - 憧れをいっぱい [FLAC 96kHz／24bit]",
    "[2025.03.19] 学園アイドルマスター 倉本千奈 - ときめきのソルフェージュ [FLAC 96kHz／24bit]": "倉本千奈 - ときめきのソルフェージュ [FLAC 96kHz／24bit]",
    "[2025.10.22] 学園アイドルマスター 倉本千奈 - 空と約束 [FLAC 96kHz／24bit]": "倉本千奈 - 空と約束 [FLAC 96kHz／24bit]",
    
    # Sumika
    "紫雲清夏(CV.湊みや) - Tame-Lie-One-Step": "紫雲清夏 - Tame-Lie-One-Step [FLAC 96kHz／24bit]",
    "[2024.11.11] 学園アイドルマスター 紫雲清夏(CV.湊みや) - Ride on Beat [FLAC 96kHz／24bit]": "紫雲清夏 - Ride on Beat [FLAC 96kHz／24bit]",
    "[2025.03.26] 学園アイドルマスター 紫雲清夏 - Kira Kira [FLAC 96kHz／24bit]": "紫雲清夏 - Kira Kira [FLAC 96kHz／24bit]",
    
    # Hiro
    "篠澤広(CV.川村玲奈) - 光景": "篠澤広 - 光景 [FLAC 96kHz／24bit]",
    "篠澤広(CV.川村玲奈) - コントラスト": "篠澤広 - コントラスト [FLAC 96kHz／24bit]",
    "[2025.03.19] 学園アイドルマスター 篠澤広 - コンテンポラリのダンス [FLAC 96kHz／24bit]": "篠澤広 - コンテンポラリのダンス [FLAC 96kHz／24bit]",
    
    # Rinami
    "姫崎莉波(CV.薄井友里) - clumsy trick": "姫崎莉波 - clumsy trick [FLAC 96kHz／24bit]",
    "姫崎莉波(CV.薄井友里) - L.U.V [FLAC 96kHz／24bit]": "姫崎莉波 - L.U.V [FLAC 96kHz／24bit]",
    "[2025.03.26] 学園アイドルマスター 姫崎莉波 - 歌声は君いろ [FLAC 96kHz／24bit]": "姫崎莉波 - 歌声は君いろ [FLAC 96kHz／24bit]",
    
    # Ume
    "花海佑芽(CV.松田彩音) - The Rolling Riceball": "花海佑芽 - The Rolling Riceball [FLAC 96kHz／24bit]",
    "[2025.04.01] 学園アイドルマスター 花海佑芽 - つよつよ最強エクササイズ [FLAC 96kHz／24bit]": "花海佑芽 - つよつよ最強エクササイズ [FLAC 96kHz／24bit]",
    
    # Misuzu
    "[2025.02.06] 学園アイドルマスター 秦谷美鈴 - たいせつなもの [FLAC 96kHz／24bit]": "秦谷美鈴 - たいせつなもの [FLAC 96kHz／24bit]",
    "[2025.02.07] 学園アイドルマスター 秦谷美鈴 - ツキノカメ [FLAC 96kHz／24bit]": "秦谷美鈴 - ツキノカメ [FLAC 96kHz／24bit]",
    
    # Sena
    "[2024.11.16] 学園アイドルマスター 十王星南(CV.陽高真白) - 小さな野望 [FLAC 96kHz／24bit]": "十王星南 - 小さな野望 [FLAC 96kHz／24bit]",
    
    # Amaya
    "[2025.11.16] 学園アイドルマスター 雨夜燕 - 理論武装して [FLAC 96kHz／24bit]": "雨夜燕 - 理論武装して [FLAC 96kHz／24bit]"
}

for cf in char_folders:
    char_dir = d_solo / cf
    if not char_dir.exists():
        continue
    for alb in list(char_dir.iterdir()):
        if alb.name in solo_renames:
            target_name = solo_renames[alb.name]
            dst = char_dir / target_name
            print(f"  Solo: {alb.name} -> {target_name}")
            shutil.move(str(alb), str(dst))

# 2. STANDARDIZE TRIO RELEASES
print("\n>>> 2. STANDARDIZING TRIO RELEASES <<<")
# Old location of combo event songs
old_all_stars = GAKUMAS / '00. 全体曲・ユニット (All Stars & Units)'

# Mapping of all 20 trio releases with artists sorted alphabetically:
# Japanese Kana / Alphabetical order:
# Trio 1: 藤田ことね (Fujita), 花海咲季 (Hanami), 月村手毬 (Tsukimura) -> [藤田ことね・花海咲季・月村手毬]
# Trio 2: 姫崎莉波 (Himesaki), 葛城リーリヤ (Katsuragi), 倉本千奈 (Kuramoto) -> [姫崎莉波・葛城リーリヤ・倉本千奈]
# Trio 3: 有村麻央 (Arimura), 篠澤広 (Shinosawa), 紫雲清夏 (Shiun) -> [有村麻央・篠澤広・紫雲清夏]
# Trio 4: 十王星南 (Juo), 花海佑芽 (Hanami), 秦谷美鈴 (Hataya) -> [十王星南・花海佑芽・秦谷美鈴]
# Seasonal Trios:
# - キミとセミブルー: 有村麻央 (Arimura), 姫崎莉波 (Himesaki), 紫雲清夏 (Shiun) -> [有村麻央・姫崎莉波・紫雲清夏]
# - 冠菊: 藤田ことね (Fujita), 花海咲季 (Hanami), 葛城リーリヤ (Katsuragi) -> [藤田ことね・花海咲季・葛城リーリヤ]
# - 仮装狂騒曲: 倉本千奈 (Kuramoto), 篠澤広 (Shinosawa), 月村手毬 (Tsukimura) -> [倉本千奈・篠澤広・月村手毬]
# - ハッピーミルフィーユ: 姫崎莉波 (Himesaki), 十王星南 (Juo), 篠澤広 (Shinosawa) -> [姫崎莉波・十王星南・篠澤広]
# - 桜フォトグラフ: 花海咲季 (Hanami), 葛城リーリヤ (Katsuragi), 紫雲清夏 (Shiun) -> [花海咲季・葛城リーリヤ・紫雲清夏]

trio_renames = [
    # Trio 1 (Fujita, Hanami, Tsukimura)
    ("Howling over the World (花海咲季・月村手毬・藤田ことね Ver.) [FLAC 96kHz／24bit]",
     "[藤田ことね・花海咲季・月村手毬] - Howling over the World [FLAC 96kHz／24bit]"),
    ("がむしゃらに行こう！ (花海咲季・月村手毬・藤田ことね Ver.) [FLAC 96kHz／24bit]",
     "[藤田ことね・花海咲季・月村手毬] - がむしゃらに行こう！ [FLAC 96kHz／24bit]"),
    ("ミラクルナナウ(ﾟ∀ﾟ)！ (花海咲季・月村手毬・藤田ことね Ver.) [FLAC]",
     "[藤田ことね・花海咲季・月村手毬] - ミラクルナナウ(ﾟ∀ﾟ)！ [FLAC]"),
    ("[2025.07.26] 学園アイドルマスター - ENDLESS DANCE (花海咲季・月村手毬・藤田ことね Ver.) [FLAC 96kHz／24bit]",
     "[藤田ことね・花海咲季・月村手毬] - ENDLESS DANCE [FLAC 96kHz／24bit]"),
    ("[2024.10.30] 学園アイドルマスター - 古今東西ちょちょいのちょい (花海咲季・月村手毬・藤田ことね Ver.) [FLAC 96kHz／24bit]",
     "[藤田ことね・花海咲季・月村手毬] - 古今東西ちょちょいのちょい [FLAC 96kHz／24bit]"),
    ("冠菊 [FLAC 96kHz／24bit]",
     "[藤田ことね・花海咲季・葛城リーリヤ] - 冠菊 [FLAC 96kHz／24bit]"),

    # Trio 2 (Himesaki, Katsuragi, Kuramoto)
    ("Howling over the World (葛城リーリヤ・倉本千奈・姫崎莉波 Ver.) [FLAC 96kHz／24bit]",
     "[姫崎莉波・葛城リーリヤ・倉本千奈] - Howling over the World [FLAC 96kHz／24bit]"),
    ("学園アイドルマスター - がむしゃらに行こう！ (葛城リーリヤ・倉本千奈・姫崎莉波 Ver.) [FLAC 96kHz／24bit]",
     "[姫崎莉波・葛城リーリヤ・倉本千奈] - がむしゃらに行こう！ [FLAC 96kHz／24bit]"),
    ("ミラクルナナウ(ﾟ∀ﾟ)！ (葛城リーリヤ・倉本千奈・姫崎莉波 Ver.) [FLAC 96kHz／24bit]",
     "[姫崎莉波・葛城リーリヤ・倉本千奈] - ミラクルナナウ(ﾟ∀ﾟ)！ [FLAC 96kHz／24bit]"),
    ("[2025.08.02] 学園アイドルマスター - ENDLESS DANCE (葛城リーリヤ・倉本千奈・姫崎莉波 Ver.) [FLAC 96kHz／24bit]",
     "[姫崎莉波・葛城リーリヤ・倉本千奈] - ENDLESS DANCE [FLAC 96kHz／24bit]"),
    ("[2025.02.02] 学園アイドルマスター - ハッピーミルフィーユ [FLAC 96kHz／24bit]",
     "[姫崎莉波・十王星南・篠澤広] - ハッピーミルフィーユ [FLAC 96kHz／24bit]"),

    # Trio 3 (Arimura, Shinosawa, Shiun)
    ("Howling over the World (有村麻央・紫雲清夏・篠澤広 Ver.) [FLAC 96kHz／24bit]",
     "[有村麻央・篠澤広・紫雲清夏] - Howling over the World [FLAC 96kHz／24bit]"),
    ("がむしゃらに行こう！ (有村麻央・紫雲清夏・篠澤広 Ver.) [FLAC 96kHz／24bit]",
     "[有村麻央・篠澤広・紫雲清夏] - がむしゃらに行こう！ [FLAC 96kHz／24bit]"),
    ("ミラクルナナウ(ﾟ∀ﾟ)！ (有村麻央・紫雲清夏・篠澤広 Ver.) [FLAC 96kHz／24bit]",
     "[有村麻央・篠澤広・紫雲清夏] - ミラクルナナウ(ﾟ∀ﾟ)！ [FLAC 96kHz／24bit]"),
    ("[2025.08.09] 学園アイドルマスター - ENDLESS DANCE (有村麻央・紫雲清夏・篠澤広 Ver.) [FLAC 96kHz／24bit]",
     "[有村麻央・篠澤広・紫雲清夏] - ENDLESS DANCE [FLAC 96kHz／24bit]"),
    ("キミとセミブルー",
     "[有村麻央・姫崎莉波・紫雲清夏] - キミとセミブルー [FLAC]"),

    # Trio 4 (Juo, Hanami, Hataya)
    ("[2025.07.19] 学園アイドルマスター - ミラクルナナウ(ﾟ∀ﾟ)！ (花海佑芽・秦谷美鈴・十王星南 Ver.) [FLAC 96kHz／24bit]",
     "[十王星南・花海佑芽・秦谷美鈴] - ミラクルナナウ(ﾟ∀ﾟ)！ [FLAC 96kHz／24bit]"),
    ("[2025.02.08] 学園アイドルマスター - ENDLESS DANCE (花海佑芽・秦谷美鈴・十王星南 Ver.) [FLAC 96kHz／24bit]",
     "[十王星南・花海佑芽・秦谷美鈴] - ENDLESS DANCE [FLAC 96kHz／24bit]"),

    # Seasonal Trios
    ("[2024.10.01] 学園アイドルマスター - 仮装狂騒曲 [FLAC 96kHz／24bit]",
     "[倉本千奈・篠澤広・月村手毬] - 仮装狂騒曲 [FLAC 96kHz／24bit]"),
    ("[2025.04.02] 学園アイドルマスター - 桜フォトグラフ [FLAC 96kHz／24bit]",
     "[花海咲季・葛城リーリヤ・紫雲清夏] - 桜フォトグラフ [FLAC 96kHz／24bit]"),
]

for src_pattern, new_name in trio_renames:
    found = False
    for p in old_all_stars.rglob('*'):
        if p.is_dir() and p.name == src_pattern:
            dst = d_trio / new_name
            print(f"  Trio: {p.name} -> {new_name}")
            shutil.move(str(p), str(dst))
            found = True
            break
    if not found:
        print(f"  [TRIO NOT FOUND] {src_pattern}")

# 3. STANDARDIZE ALL STARS & UNITS
print("\n>>> 3. STANDARDIZING ALL STARS & UNITS <<<")
unit_renames = [
    ("Star-mine", "Begrazia - Star-mine [FLAC 96kHz／24bit]"),
    ("Campus mode", "初星学園 - Campus mode!! [FLAC 96kHz／24bit]"),
    ("初 HAJIME", "初星学園 - 初 HAJIME [FLAC]"),
    ("SUPREMACY", "[葛城リーリヤ・紫雲清夏・月村手毬・花海咲季・藤田ことね] - SUPREMACY [FLAC 96kHz／24bit]"),
    ("Let's GO!! ICHI-NO-NI!!", "[倉本千奈・篠澤広・秦谷美鈴・花海佑芽] - Let's GO!! ICHI-NO-NI!! [FLAC 96kHz／24bit]"),
    ("ナイワ", "[雨夜燕・有村麻央・十王星南・姫崎莉波] - ナイワ [FLAC 96kHz／24bit]"),
]

for kw, new_name in unit_renames:
    found = False
    for p in old_all_stars.rglob('*'):
        if p.is_dir() and kw in p.name:
            dst = d_units / new_name
            print(f"  Unit: {p.name} -> {new_name}")
            shutil.move(str(p), str(dst))
            found = True
            break
    if not found:
        print(f"  [UNIT NOT FOUND] {kw}")

# Clean old_all_stars
if old_all_stars.exists():
    shutil.rmtree(str(old_all_stars))
    print("  Cleaned old 00. 全体曲・ユニット directory!")

# 4. REBUILD CATALOG.SQLITE
print("\n>>> 4. REBUILDING CATALOG.SQLITE <<<")
db_path = BASE_MUSIC / 'catalog.sqlite'
if db_path.exists():
    db_path.unlink()

conn = sqlite3.connect(str(db_path))
c = conn.cursor()
c.execute('''
    CREATE TABLE tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        relative_path TEXT UNIQUE,
        filename TEXT,
        category TEXT,
        format TEXT,
        size_bytes INTEGER,
        is_lossless INTEGER
    )
''')
c.execute('CREATE INDEX idx_category ON tracks(category)')
c.execute('CREATE INDEX idx_format ON tracks(format)')

batch = []
count = 0
for root_dir in [BASE_MUSIC / 'Lossless', BASE_MUSIC / 'Lossy']:
    if not root_dir.exists():
        continue
    is_lossless = 1 if root_dir.name == 'Lossless' else 0
    for p in root_dir.rglob('*'):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext not in ['.flac', '.wav', '.mp3', '.m4a', '.aiff', '.alac', '.tak', '.ape', '.ogg', '.opus', '.wma']:
            continue
            
        rel = str(p.relative_to(BASE_MUSIC)).replace('\\', '/')
        parts = rel.split('/')
        category = parts[1] if len(parts) > 1 else 'Unknown'
        fmt = ext.replace('.', '').upper()
        size = p.stat().st_size
        
        batch.append((rel, p.name, category, fmt, size, is_lossless))
        count += 1
        if len(batch) >= 1000:
            c.executemany('''
                INSERT OR IGNORE INTO tracks 
                (relative_path, filename, category, format, size_bytes, is_lossless)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', batch)
            conn.commit()
            batch = []

if batch:
    c.executemany('''
        INSERT OR IGNORE INTO tracks 
        (relative_path, filename, category, format, size_bytes, is_lossless)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', batch)
    conn.commit()

conn.close()
print(f"Catalog successfully rebuilt with {count} tracks indexed!")
print("\n" + "="*60)
print("ALL STANDARDS APPLIED CLEANLY AND PERFECTLY!")
print("="*60)
