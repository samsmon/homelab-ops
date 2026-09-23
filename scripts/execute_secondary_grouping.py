#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secondary grouping pass for remaining loose albums in Anime, Vtuber, Vocaloid, and J-Pop.
"""
import os
import shutil
import hashlib
import sqlite3
from pathlib import Path

BASE_MUSIC = Path('/mnt/hdd-backup/music')
MUSIC_ROOT = BASE_MUSIC / 'Lossless'

def md5_file(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def safe_move(src_path, dst_path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    if dst_path.exists():
        for item in list(src_path.iterdir()):
            target_item = dst_path / item.name
            if target_item.exists():
                if item.is_file():
                    if item.stat().st_size == target_item.stat().st_size and md5_file(item) == md5_file(target_item):
                        item.unlink()
                    else:
                        stem = item.stem
                        suffix = item.suffix
                        new_target = dst_path / f"{stem}_alt{suffix}"
                        shutil.move(str(item), str(new_target))
                elif item.is_dir():
                    safe_move(item, target_item)
            else:
                shutil.move(str(item), str(target_item))
        try:
            src_path.rmdir()
        except OSError:
            pass
    else:
        shutil.move(str(src_path), str(dst_path))

moves = []

# =========================================================================
# 1. VOCALOID
# =========================================================================
vocaloid_dir = MUSIC_ROOT / 'Vocaloid'
for d in vocaloid_dir.iterdir():
    if not d.is_dir() or d.name.endswith('~'):
        continue
    name = d.name
    lower = name.lower()
    if 'ぬぬぬ' in name:
        moves.append(('Vocaloid', name, 'Vocaloid', 'ぬぬぬぬぬぬぬぬぬぬぬぬぬぬぬぬ ~'))
    elif 'on prism' in lower:
        moves.append(('Vocaloid', name, 'Vocaloid', 'On Prism Records ~'))
    elif 'マジカルミライ' in name:
        moves.append(('Vocaloid', name, 'Vocaloid', '初音ミク マジカルミライ ~'))
    elif 'honeyworks' in lower:
        moves.append(('Vocaloid', name, 'J-Pop', 'HoneyWorks ~'))

# =========================================================================
# 2. VTUBER
# =========================================================================
vtuber_dir = MUSIC_ROOT / 'Vtuber'
for d in vtuber_dir.iterdir():
    if not d.is_dir() or d.name.endswith('~'):
        continue
    name = d.name
    lower = name.lower()
    if '常闇トワ' in name:
        moves.append(('Vtuber', name, 'Vtuber', '常闇トワ (Towa Tokoyami) ~'))
    elif '大神ミオ' in name:
        moves.append(('Vtuber', name, 'Vtuber', '大神ミオ (Mio Ookami) ~'))
    elif '宝鐘マリン' in name:
        moves.append(('Vtuber', name, 'Vtuber', '宝鐘マリン (Marine Houshou) ~'))
    elif '赤井はあと' in name:
        moves.append(('Vtuber', name, 'Vtuber', '赤井はあと (Haato Akai) ~'))
    elif 'ホロウィッチ' in name:
        moves.append(('Vtuber', name, 'Vtuber', 'ホロウィッチ! (HoloWitches) ~'))
    elif 'ぶいすぽ' in name:
        moves.append(('Vtuber', name, 'Vtuber', 'ぶいすぽっ！ (VSPO!) ~'))
    elif 'himehina' in lower:
        moves.append(('Vtuber', name, 'Vtuber', 'HIMEHINA ~'))
    elif 'しぐれうい' in name:
        moves.append(('Vtuber', name, 'Vtuber', 'しぐれうい (Ui Shigure) ~'))
    elif '桃鈴ねね' in name:
        moves.append(('Vtuber', name, 'Vtuber', '桃鈴ねね (Nene Momosuzu) ~'))
    elif '儒烏風亭らでん' in name:
        moves.append(('Vtuber', name, 'Vtuber', 'Hololive Regloss ~'))
    elif '七海うらら' in name:
        moves.append(('Vtuber', name, 'J-Pop', '七海うらら (Nanami Urara) ~'))
    elif 'blue journey' in lower:
        moves.append(('Vtuber', name, 'Vtuber', 'Blue Journey (hololive) ~'))
    elif '星川サラ' in name:
        moves.append(('Vtuber', name, 'Vtuber', '星川サラ (Sara Hoshikawa) ~'))
    elif 'アンジュ・カトリーナ' in name:
        moves.append(('Vtuber', name, 'Vtuber', 'にじさんじ (Nijisanji) Group ~'))
    elif 'チームidd' in lower:
        moves.append(('Vtuber', name, 'Vtuber', 'にじさんじ (Nijisanji) Group ~'))
    elif 'hoshimatic' in lower or '至上主義アドトラック' in name:
        moves.append(('Vtuber', name, 'Vtuber', 'hololive Official ~'))
    elif '魔王2099' in name:
        moves.append(('Vtuber', name, 'Anime', '魔王2099 ~'))

# =========================================================================
# 3. ANIME
# =========================================================================
anime_dir = MUSIC_ROOT / 'Anime'
for d in anime_dir.iterdir():
    if not d.is_dir() or d.name.endswith('~'):
        continue
    name = d.name
    lower = name.lower()
    if 'イキヅライブ' in name or 'いきづらい部' in name or 'bluebird' in lower:
        moves.append(('Anime', name, 'Anime', 'Love Live ~'))
    elif 'ブルーアーカイブ' in name or 'blue archive' in lower:
        moves.append(('Anime', name, 'Anime', 'ブルーアーカイブ (Blue Archive) ~'))
    elif 'トワツガイ' in name:
        moves.append(('Anime', name, 'Anime', 'トワツガイ (Towatsugai) ~'))
    elif 'hitori bocchi' in lower:
        moves.append(('Anime', name, 'Anime', 'ひとりぼっちの○○生活 (Hitoribocchi) ~'))
    elif 'ユーフォニアム' in name:
        moves.append(('Anime', name, 'Anime', '響け！ユーフォニアム ~'))
    elif 'reona' in lower and '3rdアルバム' in name:
        moves.append(('Anime', name, 'J-Pop', 'レオナ (ReoNa) ~'))
    elif 'yoasobi' in lower:
        moves.append(('Anime', name, 'J-Pop', 'YOASOBI ~'))
    elif 'sizuk' in lower:
        moves.append(('Anime', name, 'Anime', 'Sizuk ~'))
    elif 'ヘブンバーンズレッド' in name:
        moves.append(('Anime', name, 'Anime', 'ヘブンバーンズレッド (Heaven Burns Red) ~'))
    elif 'macross' in lower or 'マクロス' in name:
        moves.append(('Anime', name, 'Anime', 'マクロスΔ (Macross Delta) ~'))
    elif 'neo' in lower and '初音ミク' in name:
        moves.append(('Anime', name, 'Anime', 'プロジェクトセカイ (Project SEKAI) ~'))
    elif 'synduality' in lower:
        moves.append(('Anime', name, 'Anime', 'SYNDUALITY ~'))
    elif '100人の彼女' in name:
        moves.append(('Anime', name, 'Anime', '君のことが大大大大大好きな100人の彼女 ~'))
    elif 'starlight' in lower or 'レヴュースタァライト' in name:
        moves.append(('Anime', name, 'Anime', '少女☆歌劇 レヴュースタァライト ~'))
    elif 'ウルトラマンアーク' in name:
        moves.append(('Anime', name, 'Anime', 'ウルトラマンアーク ~'))
    elif '灯火のまにまに' in name:
        moves.append(('Anime', name, 'Anime', 'かくりよの宿飯 ~'))

print(f"Total secondary moves planned: {len(moves)}")
for src_cat, name, dst_cat, target_folder in moves:
    src_p = MUSIC_ROOT / src_cat / name
    dst_p = MUSIC_ROOT / dst_cat / target_folder / name
    print(f"  [{src_cat} -> {dst_cat}] {name}\n       -> {target_folder}/")
    safe_move(src_p, dst_p)

# Rebuild catalog
print("\nRebuilding catalog.sqlite...")
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
for root_dir in [MUSIC_ROOT, BASE_MUSIC / 'Lossy']:
    if not root_dir.exists():
        continue
    is_lossless = 1 if root_dir == MUSIC_ROOT else 0
    for p in root_dir.rglob('*'):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext not in ['.flac', '.wav', '.mp3', '.m4a', '.aac', '.ogg', '.opus', '.ape', '.wv', '.tak']:
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
