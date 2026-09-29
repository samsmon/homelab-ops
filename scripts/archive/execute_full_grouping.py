#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execute comprehensive grouping of all loose albums into Artist/Franchise ~ folders.
"""
import os
import sys
import shutil
import hashlib
import sqlite3
import subprocess
from pathlib import Path

MUSIC_ROOT = Path('/mnt/hdd-backup/music/Lossless')
BASE_MUSIC = Path('/mnt/hdd-backup/music')

def md5_file(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def safe_move(src_path, dst_path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    if dst_path.exists():
        # merge
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

print("="*60)
print("STARTING FULL MUSIC LIBRARY GROUPING PASS")
print("="*60)

# =========================================================================
# 1. SPECIAL CASE: SUKIDESUOST & LOOSE DOUJINSHI CONTAINERS
# =========================================================================
print("\n>>> Handling Special Doujinshi Containers & sukidesuost <<<")
sukidesu = MUSIC_ROOT / 'Doujinshi' / 'sukidesuost'
if sukidesu.exists():
    # 1. I SCREAM LIVE -> Vtuber/花譜 (KAF) ~
    kaf_dir = MUSIC_ROOT / 'Vtuber' / '花譜 (KAF) ~'
    if (sukidesu / 'I SCREAM LIVE').exists():
        print("  Moving sukidesuost/I SCREAM LIVE -> Vtuber/花譜 (KAF) ~")
        safe_move(sukidesu / 'I SCREAM LIVE', kaf_dir / '花譜 - I SCREAM LIVE')
        
    # 2. Awake -> Vtuber/理芽 (RIM) ~
    rim_dir = MUSIC_ROOT / 'Vtuber' / '理芽 (RIM) ~'
    if (sukidesu / 'Awake').exists():
        print("  Moving sukidesuost/Awake -> Vtuber/理芽 (RIM) ~")
        safe_move(sukidesu / 'Awake', rim_dir / '理芽 - Awake')
        
    # 3. Fukuzatsu Inshi & Senmei Aruiha Fusenmei -> J-Pop/UNIDOTS ~
    unidots_dir = MUSIC_ROOT / 'J-Pop' / 'UNIDOTS ~'
    if (sukidesu / 'Fukuzatsu Inshi').exists():
        print("  Moving sukidesuost/Fukuzatsu Inshi -> J-Pop/UNIDOTS ~")
        safe_move(sukidesu / 'Fukuzatsu Inshi', unidots_dir / 'UNIDOTS - 複雑因子 - complex factor -')
    if (sukidesu / 'Senmei Aruiha Fusenmei').exists():
        print("  Moving sukidesuost/Senmei Aruiha Fusenmei -> J-Pop/UNIDOTS ~")
        safe_move(sukidesu / 'Senmei Aruiha Fusenmei', unidots_dir / 'UNIDOTS - 鮮明 、あるいは 不鮮明 - clear_blur -')
        
    try:
        sukidesu.rmdir()
        print("  Removed empty sukidesuost directory!")
    except OSError:
        pass

# ABSOLUTE CASTAWAY
abcas = MUSIC_ROOT / 'Doujinshi' / 'ABSOLUTE CASTAWAY'
if abcas.exists():
    target = MUSIC_ROOT / 'Doujinshi' / '中恵光城 (ABSOLUTE CASTAWAY) ~'
    for item in list(abcas.iterdir()):
        print(f"  Moving {item.name} -> {target.name}")
        safe_move(item, target / item.name)
    try:
        abcas.rmdir()
    except OSError:
        pass

# Assortment
assort = MUSIC_ROOT / 'Doujinshi' / 'Assortment'
if assort.exists():
    target = MUSIC_ROOT / 'Doujinshi' / 'Room97 ~'
    for item in list(assort.iterdir()):
        print(f"  Moving {item.name} -> {target.name}")
        safe_move(item, target / item.name)
    try:
        assort.rmdir()
    except OSError:
        pass

# Luna
luna = MUSIC_ROOT / 'Doujinshi' / 'Luna'
if luna.exists():
    target = MUSIC_ROOT / 'Doujinshi' / '*Luna ~'
    for item in list(luna.iterdir()):
        print(f"  Moving {item.name} -> {target.name}")
        safe_move(item, target / item.name)
    try:
        luna.rmdir()
    except OSError:
        pass

# =========================================================================
# 2. RUN FULL GROUPING FROM PLAN SCRIPT
# =========================================================================
# We will dynamically run the logic of plan_full_grouping
import importlib.util
spec = importlib.util.spec_from_file_location("plan_module", "/tmp/plan_full_grouping.py")
plan_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plan_module)

plan = plan_module.build_plan()

total_moved = 0
for cat in ['Doujinshi', 'Vtuber', 'Anime', 'J-Pop', 'Vocaloid']:
    items = plan[cat]
    print(f"\n>>> Executing Grouping for [{cat.upper()}] ({len(items)} items) <<<")
    cat_dir = MUSIC_ROOT / cat
    for src_name, dst_folder in items:
        if dst_folder == 'SPECIAL_SUKIDESUOST':
            continue
        src_path = cat_dir / src_name
        if not src_path.exists():
            continue
        dst_path = cat_dir / dst_folder / src_name
        print(f"  [{cat}] '{src_name}'\n       -> '{dst_folder}/'")
        safe_move(src_path, dst_path)
        total_moved += 1

print(f"\nTotal albums grouped: {total_moved}")

# =========================================================================
# 3. REBUILD SQLITE CATALOG
# =========================================================================
print("\n>>> Rebuilding catalog.sqlite <<<")
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
print(f"Catalog successfully rebuilt with {count} tracks indexed at {db_path}!")

print("\n" + "="*60)
print("FULL GROUPING PASS COMPLETED SUCCESSFULLY!")
print("="*60)
