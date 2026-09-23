#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reorganize Gakuen Idolmaster into a clean Per-Character Artist Hierarchy:
1. Consolidate Anime/Im@s ~/学園アイドルマスター and Anime/学園アイドルマスター ~
   into a single master hub: Anime/学園アイドルマスター ~
2. Create per-character folders:
   - 00. 全体曲・ユニット (All Stars & Units)
   - 01. 花海咲季 (Saki Hanami)
   - 02. 月村手毬 (Temari Tsukimura)
   - 03. 藤田ことね (Kotone Fujita)
   - 04. 有村麻央 (Mao Arimura)
   - 05. 葛城リーリヤ (Lilja Katsuragi)
   - 06. 倉本千奈 (China Kuramoto)
   - 07. 紫雲清夏 (Sumika Shiun)
   - 08. 篠澤広 (Hiro Shinosawa)
   - 09. 姫崎莉波 (Rinami Himesaki)
   - 10. 花海佑芽 (Ume Hanami)
   - 11. 秦谷美鈴 (Misuzu Hataya)
   - 12. 十王星南 (Sena Juo)
   - 13. 雨夜燕 (Tsubame Amaya)
3. Organize Combination/Trio event songs into clean subfolders under 00. 全体曲・ユニット
4. Remove empty Im@s ~ directory
5. Rebuild catalog.sqlite
"""
import os
import shutil
import sqlite3
from pathlib import Path

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime')
imas_root = BASE / 'Im@s ~'
imas_gakumas = imas_root / '学園アイドルマスター'
target_gakumas = BASE / '学園アイドルマスター ~'

print("="*60)
print("REORGANIZING GAKUEN IDOLMASTER PER CHARACTER HIERARCHY")
print("="*60)

# Character definitions
char_folders = {
    '花海咲季': '01. 花海咲季 (Saki Hanami)',
    '月村手毬': '02. 月村手毬 (Temari Tsukimura)',
    '藤田ことね': '03. 藤田ことね (Kotone Fujita)',
    '有村麻央': '04. 有村麻央 (Mao Arimura)',
    '葛城リーリヤ': '05. 葛城リーリヤ (Lilja Katsuragi)',
    '倉本千奈': '06. 倉本千奈 (China Kuramoto)',
    '紫雲清夏': '07. 紫雲清夏 (Sumika Shiun)',
    '篠澤広': '08. 篠澤広 (Hiro Shinosawa)',
    '姫崎莉波': '09. 姫崎莉波 (Rinami Himesaki)',
    '花海佑芽': '10. 花海佑芽 (Ume Hanami)',
    '秦谷美鈴': '11. 秦谷美鈴 (Misuzu Hataya)',
    '十王星南': '12. 十王星南 (Sena Juo)',
    '雨夜燕': '13. 雨夜燕 (Tsubame Amaya)',
}

# Create all character directories
for folder_name in char_folders.values():
    (target_gakumas / folder_name).mkdir(parents=True, exist_ok=True)

all_stars_dir = target_gakumas / '00. 全体曲・ユニット (All Stars & Units)'
all_stars_dir.mkdir(parents=True, exist_ok=True)

combos_dir = all_stars_dir / 'Event Songs (Trio Ver)'
combos_dir.mkdir(parents=True, exist_ok=True)

# 1. PROCESS IMAS_GAKUMAS RELEASES (35 releases)
print("\n>>> 1. PROCESSING RELEASES FROM Im@s ~/学園アイドルマスター <<<")
if imas_gakumas.exists():
    for sub in list(imas_gakumas.iterdir()):
        if not sub.is_dir():
            continue
        for alb in list(sub.iterdir()):
            if not alb.is_dir():
                continue
            name = alb.name
            
            # Check if it's a combination / trio event song
            if any(k in name for k in ['Howling over the World', 'がむしゃらに行こう！', 'ミラクルナナウ', 'ENDLESS DANCE']):
                # Find event song name
                event_name = 'Other'
                if 'Howling over the World' in name:
                    event_name = 'Howling over the World'
                elif 'がむしゃらに行こう！' in name:
                    event_name = 'がむしゃらに行こう！'
                elif 'ミラクルナナウ' in name:
                    event_name = 'ミラクルナナウ(ﾟ∀ﾟ)！'
                elif 'ENDLESS DANCE' in name:
                    event_name = 'ENDLESS DANCE'
                    
                dest_sub = combos_dir / event_name
                dest_sub.mkdir(parents=True, exist_ok=True)
                dest = dest_sub / name
                print(f"  Combo: {name} -> Event Songs/{event_name}/")
                shutil.move(str(alb), str(dest))
            elif any(k in name for k in ['Campus mode', '初 HAJIME', 'キミとセミブルー', '冠菊']):
                dest = all_stars_dir / name
                print(f"  All-Stars: {name} -> 00. 全体曲・ユニット/")
                shutil.move(str(alb), str(dest))
            else:
                # Character solo / birthday / single
                matched = False
                for jp, folder_name in char_folders.items():
                    if jp in name:
                        dest_dir = target_gakumas / folder_name
                        dest = dest_dir / name
                        print(f"  Solo ({jp}): {name} -> {folder_name}/")
                        shutil.move(str(alb), str(dest))
                        matched = True
                        break
                if not matched:
                    print(f"  [UNMATCHED IMAS] {name} -> All Stars")
                    shutil.move(str(alb), str(all_stars_dir / name))

    # Clean empty imas_gakumas
    shutil.rmtree(str(imas_root))
    print("  Removed empty Im@s ~ directory successfully!")

# 2. PROCESS FLAT GAKUMAS RELEASES (32 releases)
print("\n>>> 2. PROCESSING FLAT RELEASES IN 学園アイドルマスター ~ <<<")
existing_dirs = set(char_folders.values()) | {'00. 全体曲・ユニット (All Stars & Units)'}

for alb in list(target_gakumas.iterdir()):
    if not alb.is_dir() or alb.name in existing_dirs:
        continue
    name = alb.name
    
    # Check if Begrazia
    if 'Begrazia' in name:
        dest_dir = all_stars_dir / 'Begrazia'
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / name
        print(f"  Begrazia: {name} -> Begrazia/")
        shutil.move(str(alb), str(dest))
    # Check combination songs
    elif any(k in name for k in ['ENDLESS DANCE', 'ミラクルナナウ', 'がむしゃらに行こう！', '古今東西ちょちょいのちょい']):
        event_name = 'Other'
        if 'ENDLESS DANCE' in name:
            event_name = 'ENDLESS DANCE'
        elif 'ミラクルナナウ' in name:
            event_name = 'ミラクルナナウ(ﾟ∀ﾟ)！'
        elif 'がむしゃらに行こう！' in name:
            event_name = 'がむしゃらに行こう！'
        elif '古今東西ちょちょいのちょい' in name:
            event_name = '古今東西ちょちょいのちょい'
            
        dest_sub = combos_dir / event_name
        dest_sub.mkdir(parents=True, exist_ok=True)
        dest = dest_sub / name
        print(f"  Combo: {name} -> Event Songs/{event_name}/")
        shutil.move(str(alb), str(dest))
    elif any(k in name for k in ['桜フォトグラフ', 'ハッピーミルフィーユ', 'SUPREMACY', "Let's GO!! ICHI-NO-NI!!", 'ナイワ', '仮装狂騒曲']):
        dest = all_stars_dir / name
        print(f"  All-Stars: {name} -> 00. 全体曲・ユニット/")
        shutil.move(str(alb), str(dest))
    else:
        # Match character
        matched = False
        for jp, folder_name in char_folders.items():
            if jp in name:
                dest_dir = target_gakumas / folder_name
                dest = dest_dir / name
                print(f"  Solo ({jp}): {name} -> {folder_name}/")
                shutil.move(str(alb), str(dest))
                matched = True
                break
        if not matched:
            print(f"  [UNMATCHED FLAT] {name} -> All Stars")
            shutil.move(str(alb), str(all_stars_dir / name))

# 3. REBUILD CATALOG.SQLITE
print("\n>>> 3. REBUILDING CATALOG.SQLITE <<<")
base_music = Path('/mnt/hdd-backup/music')
db_path = base_music / 'catalog.sqlite'
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
for root_dir in [base_music / 'Lossless', base_music / 'Lossy']:
    if not root_dir.exists():
        continue
    is_lossless = 1 if root_dir.name == 'Lossless' else 0
    for p in root_dir.rglob('*'):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext not in ['.flac', '.wav', '.mp3', '.m4a', '.aiff', '.alac', '.tak', '.ape', '.ogg', '.opus', '.wma']:
            continue
            
        rel = str(p.relative_to(base_music)).replace('\\', '/')
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
print(f"Catalog rebuilt successfully with {count} tracks indexed!")
print("\n" + "="*60)
print("GAKUEN IDOLMASTER REORGANIZATION COMPLETED!")
print("="*60)
