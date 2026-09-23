#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tertiary grouping pass: Clean up 100% of remaining loose albums in Anime, Vocaloid, Vtuber, and J-Pop.
"""
import os
import shutil
import hashlib
import sqlite3
import subprocess
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

# =========================================================================
# 1. ANIME (12 remaining)
# =========================================================================
anime_dir = MUSIC_ROOT / 'Anime'
for d in list(anime_dir.iterdir()):
    if not d.is_dir() or d.name.endswith('~'):
        continue
    name = d.name
    lower = name.lower()
    if 'fate' in lower:
        dst = anime_dir / 'Fate (Series) ~' / name
    elif 'just because' in lower:
        dst = anime_dir / 'Just Because! ~' / name
    elif 'marine summer' in lower:
        dst = MUSIC_ROOT / 'Vtuber' / '宝鐘マリン (Marine Houshou) ~' / name
    elif 'yuru camp' in lower or 'ゆるキャン' in name:
        dst = anime_dir / 'ゆるキャン△ (Yuru Camp) ~' / name
    elif 'slow loop' in lower or 'yajirushi' in lower:
        dst = anime_dir / 'スローループ (Slow Loop) ~' / name
    elif 'blue protocol' in lower:
        dst = anime_dir / 'BLUE PROTOCOL ~' / name
    elif 'ばっどがーる' in name:
        dst = anime_dir / 'ばっどがーる ~' / name
    elif name == 'True':
        dst = MUSIC_ROOT / 'J-Pop' / 'TRUE ~' / name
    elif 'シリウスの輝き' in name or '夢のステラリウム' in name:
        dst = anime_dir / 'ワールドダイスター~' / name
    elif name == 'Galaxy Triangle':
        dst = anime_dir / 'Galaxy Triangle ~' / name
    elif name == 'テトリス':
        dst = anime_dir / 'テトリス ~' / name
    else:
        dst = anime_dir / f"{name} ~" / name
    print(f"Anime: {name} -> {dst.relative_to(MUSIC_ROOT)}")
    safe_move(d, dst)

# =========================================================================
# 2. VOCALOID (6 remaining)
# =========================================================================
vocaloid_dir = MUSIC_ROOT / 'Vocaloid'
for d in list(vocaloid_dir.iterdir()):
    if not d.is_dir() or d.name.endswith('~'):
        continue
    name = d.name
    lower = name.lower()
    if '八王子p' in lower:
        dst = vocaloid_dir / '八王子P ~' / name
    elif 'cosmo' in lower or '暴走p' in lower:
        dst = vocaloid_dir / 'cosMo@暴走P ~' / name
    elif 'livetune' in lower:
        dst = vocaloid_dir / 'livetune ~' / name
    elif 'alextrip' in lower:
        dst = vocaloid_dir / 'AlexTrip Sands ~' / name
    elif 'synthion' in lower:
        dst = vocaloid_dir / 'Synthion ~' / name
    elif 'exit tunes' in lower:
        dst = vocaloid_dir / 'EXIT TUNES PRESENTS ~' / name
    else:
        dst = vocaloid_dir / f"{name} ~" / name
    print(f"Vocaloid: {name} -> {dst.relative_to(MUSIC_ROOT)}")
    safe_move(d, dst)

# =========================================================================
# 3. VTUBER (38 remaining)
# =========================================================================
vtuber_dir = MUSIC_ROOT / 'Vtuber'
for d in list(vtuber_dir.iterdir()):
    if not d.is_dir() or d.name.endswith('~'):
        continue
    name = d.name
    lower = name.lower()
    if 'mori calliope' in lower:
        dst = vtuber_dir / 'Mori Calliope ~' / name
    elif 'kmnz' in lower:
        dst = vtuber_dir / 'KMNZ ~' / name
    elif 'v.w.p' in lower:
        dst = vtuber_dir / 'V.W.P ~' / name
    elif 'kizuna ai' in lower:
        dst = vtuber_dir / 'Kizuna AI ~' / name
    elif 'murasaki shion' in lower:
        dst = vtuber_dir / '紫咲シオン (Murasaki Shion) ~' / name
    elif 'fuwamoco' in lower:
        dst = vtuber_dir / 'FUWAMOCO ~' / name
    elif 'shigure ui' in lower:
        dst = vtuber_dir / 'しぐれうい (Ui Shigure) ~' / name
    elif 'ほろはにヶ丘高校' in name:
        dst = vtuber_dir / 'hololive Official ~' / name
    elif 'kamitsubaki city' in lower:
        dst = vtuber_dir / 'KAMITSUBAKI Studio ~' / name
    elif '廻花' in name:
        dst = vtuber_dir / '花譜 (KAF) ~' / name
    elif 'コハク' in name and '夢限大' in name:
        dst = MUSIC_ROOT / 'Anime' / 'BanG Dream! ~' / name
    elif 'ongeki' in lower:
        dst = MUSIC_ROOT / 'Anime' / 'ONGEKI (オンゲキ) ~' / name
    elif 'sekai' in lower:
        dst = vtuber_dir / 'Sekai ~' / name
    elif 'shirayuki hina' in lower:
        dst = vtuber_dir / '白雪ひな (Shirayuki Hina) ~' / name
    elif any(k in lower for k in ['riot music', '芦澤サキ', '松永依織']):
        dst = vtuber_dir / 'RIOT MUSIC ~' / name
    elif 'vesperbell' in lower:
        dst = vtuber_dir / 'VESPERBELL ~' / name
    elif '龍ヶ崎リン' in name:
        dst = vtuber_dir / '龍ヶ崎リン ~' / name
    elif 'ciel' in lower:
        dst = vtuber_dir / 'CIEL ~' / name
    elif 'guiano' in lower:
        dst = vtuber_dir / 'Guiano ~' / name
    elif 'mimi' in lower:
        dst = vtuber_dir / 'MIMI ~' / name
    elif 'meda' in lower:
        dst = vtuber_dir / 'MEDA ~' / name
    elif 'neun' in lower:
        dst = vtuber_dir / 'NEUN ~' / name
    elif 'riot of emotions' in lower:
        dst = vtuber_dir / 'Riot Of Emotions ~' / name
    elif 'ruki otokado' in lower:
        dst = vtuber_dir / '音門るき (Ruki Otokado) ~' / name
    elif 'uta wasurena' in lower or '勿忘うた' in name:
        dst = vtuber_dir / '勿忘うた (Uta Wasurena) ~' / name
    elif 'vα-liv' in lower:
        dst = MUSIC_ROOT / 'Anime' / 'THE IDOLM@STER ~' / name
    elif name == 'のあ - When you wish upon a star [FLAC]':
        dst = vtuber_dir / 'のあ ~' / name
    elif 'imagination' in lower:
        dst = vtuber_dir / 'IMAGINATION ~' / name
    elif '瀬戸乃とと' in name:
        dst = vtuber_dir / '瀬戸乃とと ~' / name
    elif '燦鳥ノム' in name:
        dst = vtuber_dir / '燦鳥ノム ~' / name
    elif '織姫はるか' in name:
        dst = vtuber_dir / '織姫はるか ~' / name
    elif '陽月るるふ' in name:
        dst = vtuber_dir / '陽月るるふ ~' / name
    else:
        # Default single-artist cluster
        cand = name.split(' - ')[0].strip()
        dst = vtuber_dir / f"{cand} ~" / name
    print(f"Vtuber: {name} -> {dst.relative_to(MUSIC_ROOT)}")
    safe_move(d, dst)

# =========================================================================
# 4. J-POP (Remaining loose albums)
# =========================================================================
jpop_dir = MUSIC_ROOT / 'J-Pop'
for d in list(jpop_dir.iterdir()):
    if not d.is_dir() or d.name.endswith('~'):
        continue
    name = d.name
    # Extract candidate artist
    artist = None
    # 1. Look for existing J-Pop artist folders that match
    for existing in [x.name for x in jpop_dir.iterdir() if x.is_dir() and x.name.endswith('~')]:
        clean = existing.rstrip('~').strip()
        parts = [clean]
        if '(' in clean and ')' in clean:
            parts.extend([clean[:clean.find('(')].strip(), clean[clean.find('(')+1:clean.find(')')].strip()])
        for p in parts:
            if len(p) >= 3 and p.lower() in name.lower():
                artist = existing
                break
        if artist:
            break
            
    if not artist:
        # Extract artist from name pattern
        clean_name = name
        if clean_name.startswith('[') and ']' in clean_name:
            clean_name = clean_name[clean_name.find(']')+1:].strip()
            
        for delim in [' - ', '／', ' / ', ' 1st', ' 2nd', ' 3rd', ' 4th', ' 5th', ' (', ' [', '【']:
            if delim in clean_name:
                cand = clean_name.split(delim)[0].strip()
                if len(cand) >= 2:
                    artist = f"{cand} ~"
                    break
        if not artist:
            artist = f"{clean_name} ~"
            
    dst = jpop_dir / artist / name
    print(f"J-Pop: {name} -> {artist}/")
    safe_move(d, dst)

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
