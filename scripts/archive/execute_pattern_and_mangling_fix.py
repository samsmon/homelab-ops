#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execution Script:
1. Fix SMB name mangling:
   - Rename Doujinshi/[ahi:] ~ -> Doujinshi/[ahi] ~
   - Consolidate *Luna into J-Pop/＊Luna ~ and remove Doujinshi/*Luna ~ and Vocaloid/＊luna ~
2. Reorganize Anime/Uma Musume ~ into 5 subseries pattern folders:
   - 01. WINNING LIVE Series
   - 02. ANIMATION DERBY Series
   - 03. STARTING GATE Series
   - 04. Theatrical & Specials
   - 05. Compilations
3. Rebuild catalog.sqlite
"""
import os
import shutil
import sqlite3
import subprocess
from pathlib import Path

BASE_MUSIC = Path('/mnt/hdd-backup/music')
MUSIC_ROOT = BASE_MUSIC / 'Lossless'

print("="*60)
print("STARTING EXECUTION: SMB MANGLING FIX & UMA MUSUME PATTERN GROUPING")
print("="*60)

# =========================================================================
# 1. FIX SMB MANGLING FOR [ahi:] ~
# =========================================================================
print("\n>>> 1. FIXING SMB MANGLING FOR [ahi:] ~ <<<")
ahi_old = MUSIC_ROOT / 'Doujinshi' / '[ahi:] ~'
ahi_new = MUSIC_ROOT / 'Doujinshi' / '[ahi] ~'

if ahi_old.exists():
    if not ahi_new.exists():
        print(f"  Renaming {ahi_old.name} -> {ahi_new.name}")
        shutil.move(str(ahi_old), str(ahi_new))
    else:
        # Merge if new already exists
        for item in ahi_old.iterdir():
            shutil.move(str(item), str(ahi_new / item.name))
        ahi_old.rmdir()
    print("  [ahi] ~ is now 100% legal in Windows SMB!")
else:
    print(f"  [ahi:] ~ already resolved or not found.")

# =========================================================================
# 2. CONSOLIDATE *LUNA INTO J-POP/＊Luna ~
# =========================================================================
print("\n>>> 2. CONSOLIDATING *LUNA INTO J-POP <<<")
# J-Pop target uses full-width asterisk (U+FF0A)
jpop_luna = MUSIC_ROOT / 'J-Pop' / '＊Luna ~'
jpop_luna.mkdir(parents=True, exist_ok=True)

# A. From Doujinshi/*Luna ~ (ASCII *)
doujin_luna = MUSIC_ROOT / 'Doujinshi' / '*Luna ~'
if doujin_luna.exists():
    for item in list(doujin_luna.iterdir()):
        dst_name = item.name
        if not dst_name.startswith('＊Luna') and not dst_name.startswith('*Luna'):
            dst_name = f"＊Luna - {dst_name}"
        dst = jpop_luna / dst_name
        print(f"  Moving from Doujinshi: {item.name} -> {dst.relative_to(MUSIC_ROOT)}")
        shutil.move(str(item), str(dst))
    try:
        doujin_luna.rmdir()
        print("  Doujinshi/*Luna ~ removed cleanly (mangled _FCR9Q~X eliminated)!")
    except Exception as e:
        print(f"  Warning removing {doujin_luna}: {e}")

# B. From Vocaloid/＊luna ~
vocaloid_luna = MUSIC_ROOT / 'Vocaloid' / '＊luna ~'
if vocaloid_luna.exists():
    for item in list(vocaloid_luna.iterdir()):
        dst = jpop_luna / item.name
        print(f"  Moving from Vocaloid: {item.name} -> {dst.relative_to(MUSIC_ROOT)}")
        if not dst.exists():
            shutil.move(str(item), str(dst))
        else:
            print(f"  Destination already exists: {dst.name}")
    try:
        vocaloid_luna.rmdir()
        print("  Vocaloid/＊luna ~ consolidated into J-Pop!")
    except Exception as e:
        print(f"  Warning removing {vocaloid_luna}: {e}")

print("  *Luna discography in J-Pop now contains:")
for alb in sorted(jpop_luna.iterdir()):
    print(f"    - {alb.name}")

# =========================================================================
# 3. REORGANIZE UMA MUSUME ~ INTO 5 SUBSERIES PATTERN FOLDERS
# =========================================================================
print("\n>>> 3. REORGANIZING UMA MUSUME INTO 5 PATTERN FOLDERS <<<")
uma_root = MUSIC_ROOT / 'Anime' / 'Uma Musume ~'
if uma_root.exists():
    series_dirs = {
        '01. WINNING LIVE Series': uma_root / '01. WINNING LIVE Series',
        '02. ANIMATION DERBY Series': uma_root / '02. ANIMATION DERBY Series',
        '03. STARTING GATE Series': uma_root / '03. STARTING GATE Series',
        '04. Theatrical & Specials': uma_root / '04. Theatrical & Specials',
        '05. Compilations': uma_root / '05. Compilations',
    }

    for d in series_dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    albums = [d for d in uma_root.iterdir() if d.is_dir() and d.name not in series_dirs]
    print(f"  Found {len(albums)} albums to classify in Uma Musume ~")

    moved_counts = {k: 0 for k in series_dirs}

    for a in albums:
        name = a.name
        target_category = None
        
        if 'WINNING LIVE' in name:
            target_category = '01. WINNING LIVE Series'
        elif 'ANIMATION DERBY' in name or 'うまよん' in name:
            target_category = '02. ANIMATION DERBY Series'
        elif 'STARTING GATE' in name:
            target_category = '03. STARTING GATE Series'
        elif '新時代の扉' in name or 'ROAD TO THE TOP' in name:
            target_category = '04. Theatrical & Specials'
        elif 'Astell&Kern' in name:
            target_category = '05. Compilations'
        else:
            print(f"  [WARNING] Uncategorized album: {name}")
            continue

        target_dir = series_dirs[target_category]
        dst = target_dir / name
        # print(f"  Moving {name} -> {target_category}/")
        shutil.move(str(a), str(dst))
        moved_counts[target_category] += 1

    print("\n  Uma Musume reorganization summary:")
    for cat, cnt in moved_counts.items():
        print(f"    - {cat}: {cnt} albums moved")

# =========================================================================
# 4. REBUILD CATALOG.SQLITE
# =========================================================================
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
for root_dir in [MUSIC_ROOT, BASE_MUSIC / 'Lossy']:
    if not root_dir.exists():
        continue
    is_lossless = 1 if root_dir == MUSIC_ROOT else 0
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
print(f"  Catalog successfully rebuilt with {count} tracks indexed!")
print("\n" + "="*60)
print("EXECUTION COMPLETED SUCCESSFULLY!")
print("="*60)
