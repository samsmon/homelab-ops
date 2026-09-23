#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all anomalies across the music library:
1. Permanent deletion of Fujian Series ~
2. Delete incomplete Anime/Galaxy Triangle ~
3. Clean orphan empty/metadata-only folders
4. Extract unextracted zips in TRUE and Priere
5. Standardize Uma Musume ~ and remove duplicate CD images
6. Rebuild catalog.sqlite
"""
import os
import shutil
import sqlite3
import subprocess
from pathlib import Path

BASE_MUSIC = Path('/mnt/hdd-backup/music')
MUSIC_ROOT = BASE_MUSIC / 'Lossless'

def test_flac(filepath):
    try:
        res = subprocess.run(['flac', '-t', '-s', str(filepath)], capture_output=True, timeout=30)
        return res.returncode == 0
    except Exception:
        return False

print("="*60)
print("EXECUTING COMPREHENSIVE ANOMALY RESOLUTION")
print("="*60)

# =========================================================================
# 1. PERMANENT DELETE FUJIAN SERIES
# =========================================================================
print("\n>>> 1. PERMANENT DELETE FUJIAN SERIES <<<")
fujian = MUSIC_ROOT / 'Doujinshi' / 'Fujian Series ~'
if fujian.exists():
    print(f"  Deleting: {fujian}")
    shutil.rmtree(str(fujian))
    print("  Fujian Series ~ successfully deleted permanently!")

# =========================================================================
# 2. DELETE INCOMPLETE GALAXY TRIANGLE
# =========================================================================
print("\n>>> 2. DELETE INCOMPLETE GALAXY TRIANGLE <<<")
gt = MUSIC_ROOT / 'Anime' / 'Galaxy Triangle ~'
if gt.exists():
    print(f"  Deleting incomplete: {gt}")
    shutil.rmtree(str(gt))
    print("  Anime/Galaxy Triangle ~ successfully deleted (master is in Vtuber/La Prière ~)!")

# =========================================================================
# 3. CLEAN ORPHAN STUBS (EMPTY OR CORRUPT METADATA LEFTOVERS)
# =========================================================================
print("\n>>> 3. CLEANING ORPHAN STUBS & EMPTY FOLDERS <<<")
orphan_targets = [
    MUSIC_ROOT / 'Anime' / '学園アイドルマスター ~' / '[2025.11.01] 学園アイドルマスター 有村麻央 - 見て [FLAC 96kHz／24bit]',
    MUSIC_ROOT / 'Anime' / 'ひとりぼっちの○○生活 (Hitoribocchi) ~' / 'Hitori Bocchi no Marumaru Seikatsu - Opening [FLAC 24-96]',
    MUSIC_ROOT / 'Vtuber' / 'La Prière ~' / 'La Prière - Infinity Rage',
    MUSIC_ROOT / 'Vtuber' / 'FLOW GLOW ~' / '[2024.11.09] FLOW GLOW - FG ROADSTER [FLAC 48kHz／24bit]',
    MUSIC_ROOT / 'Vtuber' / '天音かなた (Kanata Amane) ~' / '[2024.03.13] 天音かなた 1stアルバム「Unknown DIVA」[FLAC 48kHz／24bit]',
    MUSIC_ROOT / 'J-Pop' / '青山なぎさ (Nagisa Aoyama) ~' / '[2024.10.16] 青山なぎさ 1stアルバム「解放」[FLAC 96kHz／24bit]',
    MUSIC_ROOT / 'J-Pop' / '柚木梨沙 (Risa Yuzuki) ~' / 'BlackY, Risa Yuzuki - Ego Eimi',
    MUSIC_ROOT / 'J-Pop' / '柚木梨沙 (Risa Yuzuki) ~' / 'Risa Yuzuki - Innocent Proof [CD-FLAC]',
    MUSIC_ROOT / 'J-Pop' / 'WaMi ~' / 'WaMi - 2600 [2023.09.27][Hi-Res FLAC]',
    MUSIC_ROOT / 'J-Pop' / '7uta ~' / 'nayuta - Decillion Encounter',
    MUSIC_ROOT / 'J-Pop' / 'フーリンキャットマーク (Fuling Cat Mark) ~' / 'フーリンキャットマーク - キャプリーヌにこいして [C96]',
    MUSIC_ROOT / 'J-Pop' / 'Feryquitous ~' / 'Feryquitous x 藍月なくる - IdenTism (FLAC)'
]

for p in orphan_targets:
    if p.exists():
        print(f"  Removing orphan stub: {p.relative_to(MUSIC_ROOT)}")
        shutil.rmtree(str(p))

# Clean empty artist containers if any
for cat in MUSIC_ROOT.iterdir():
    if not cat.is_dir():
        continue
    for artist_d in list(cat.iterdir()):
        if artist_d.is_dir() and not list(artist_d.iterdir()):
            print(f"  Removing empty artist container: {artist_d.relative_to(MUSIC_ROOT)}")
            artist_d.rmdir()

# =========================================================================
# 4. EXTRACT ZIPS IN PRIERE & TRUE
# =========================================================================
print("\n>>> 4. EXTRACTING ARCHIVES IN PRIERE & TRUE <<<")
# A. Priere
priere_dir = MUSIC_ROOT / 'J-Pop' / '如月梢 (Priere＊) ~'
if priere_dir.exists():
    for z in priere_dir.rglob('*.zip'):
        target_sub = z.parent
        print(f"  Extracting {z.name} -> {target_sub.name} ...")
        res = subprocess.run(['7z', 'x', f'-o{target_sub}', '-y', str(z)], capture_output=True)
        if res.returncode == 0:
            print(f"    Success! Verifying FLACs in {target_sub.name}...")
            flacs = list(target_sub.glob('*.flac'))
            if flacs and all(test_flac(f) for f in flacs):
                print(f"    All {len(flacs)} FLACs valid! Removing zip.")
                z.unlink()

# B. TRUE
true_container = MUSIC_ROOT / 'J-Pop' / 'TRUE ~'
if true_container.exists():
    true_singles = true_container / 'True' / 'True' / 'TRUE' / 'Singles'
    if true_singles.exists():
        zips = list(true_singles.glob('*.zip'))
        for z in zips:
            stem = z.stem
            dest_dir = true_container / f"{stem} [FLAC]"
            dest_dir.mkdir(parents=True, exist_ok=True)
            print(f"  Extracting TRUE single {z.name} -> {dest_dir.name} ...")
            res = subprocess.run(['7z', 'x', f'-o{dest_dir}', '-y', str(z)], capture_output=True)
            if res.returncode == 0:
                flacs = list(dest_dir.rglob('*.flac'))
                if flacs and all(test_flac(f) for f in flacs):
                    print(f"    All {len(flacs)} FLACs valid! Removing zip.")
                    z.unlink()
        # Remove nested True folder
        nested_true = true_container / 'True'
        if nested_true.exists():
            shutil.rmtree(str(nested_true))
            print("  Cleaned nested True folder structure!")

# =========================================================================
# 5. STANDARDIZE UMA MUSUME ~ & REMOVE DUPLICATE CD IMAGES
# =========================================================================
print("\n>>> 5. STANDARDIZING UMA MUSUME & REMOVING REDUNDANT CD IMAGES <<<")
uma_dir = MUSIC_ROOT / 'Anime' / 'Uma Musume ~'
if uma_dir.exists():
    # A. Remove duplicate CD image flacs in DERBY 01-05
    for p in uma_dir.rglob('*.flac'):
        if p.name.startswith(('LACM-', 'LACA-')):
            # verify that sibling or child flacs exist
            parent = p.parent
            siblings = [f for f in parent.rglob('*.flac') if f != p and not f.name.startswith(('LACM-', 'LACA-'))]
            if siblings:
                print(f"  Removing redundant CD image: {p.relative_to(uma_dir)} ({p.stat().st_size / (1024*1024):.1f} MB alongside {len(siblings)} split tracks)")
                p.unlink()
                # remove associated cue
                cue = p.with_suffix('.cue')
                if cue.exists():
                    cue.unlink()

    # B. Also remove cues with "[ウマ娘 プリティーダービー]" in DERBY 01-05 root that cause MusicBee errors
    for cue in uma_dir.glob('*DERBY*/*.cue'):
        print(f"  Removing redundant root cue: {cue.name}")
        cue.unlink()

    # C. Standardize folder names
    rename_map = {
        '[180214] ウマ娘 プリティーダービー STARTING GATE 08 [FLAC+CUE]': '[2018.02.14] ウマ娘 プリティーダービー STARTING GATE 08 [FLAC]',
        '[180425] ANIMATION DERBY 01 ｢Make Debut!｣ (flac+webp)': '[2018.04.25] TVアニメ『ウマ娘 プリティーダービー』ANIMATION DERBY 01「Make debut!」[FLAC]',
        '[180509] ANIMATION DERBY 02 ｢グロウアップ・シャイン!｣ (flac+webp)': '[2018.05.09] TVアニメ『ウマ娘 プリティーダービー』ANIMATION DERBY 02「グロウアップ・シャイン！」[FLAC]',
        '[180725] ANIMATION DERBY 03 ｢Find My Only Way｣ (flac+webp)': '[2018.07.25] TVアニメ『ウマ娘 プリティーダービー』ANIMATION DERBY 03「Find My Only Way」[FLAC]',
        '[180801] ANIMATION DERBY 04 Original Soundtrack (flac)': '[2018.08.01] TVアニメ『ウマ娘 プリティーダービー』ANIMATION DERBY 04 Original Soundtrack [FLAC]',
        '[180912] ANIMATION DERBY 05 (flac+webp)': '[2018.09.12] TVアニメ『ウマ娘 プリティーダービー』ANIMATION DERBY 05 [FLAC]',
        '[181214] Astell&Kern SPCD [24bit_96kHz] (flac)': '[2018.12.14] ウマ娘 プリティーダービー Astell&Kern Special Compilation CD [FLAC 96kHz／24bit]',
        '[210224] ANIMATION DERBY Season 2 vol.1「ユメヲカケル！」(AIFF 96kHz_32bit)': '[2021.02.24] TVアニメ『ウマ娘 プリティーダービー Season 2』ANIMATION DERBY Season 2 vol.1「ユメヲカケル！」[AIFF 96kHz／32bit]',
        '[210310] ANIMATION DERBY Season 2 vol.2「木漏れ日のエール」(AIFF 96kHz_32bit)': '[2021.03.10] TVアニメ『ウマ娘 プリティーダービー Season 2』ANIMATION DERBY Season 2 vol.2「木漏れ日のエール」[AIFF 96kHz／32bit]',
        '[210317] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 01 (AIFF 96kHz_32bit)': '[2021.03.17] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 01 [AIFF 96kHz／32bit]',
        '[210616] アニメ『うまよん』ミニアルバム (AIFF 96kHz_32bit)': '[2021.06.16] アニメ『うまよん』ミニアルバム [AIFF 96kHz／32bit]',
        '[210922] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 02 (ALAC 96kHz_32bit)': '[2021.09.22] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 02 [ALAC 96kHz／32bit]',
        '[220209] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 03 (ALAC 96kHz_32bit)': '[2022.02.09] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 03 [ALAC 96kHz／32bit]',
        '[220316] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 04 (ALAC 96kHz_32bit)': '[2022.03.16] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 04 [ALAC 96kHz／32bit]',
        '[220427] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 05 (ALAC 96kHz_32bit)': '[2022.04.27] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 05 [ALAC 96kHz／32bit]',
        '[220427] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 06 (ALAC 96kHz_32bit)': '[2022.04.27] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 06 [ALAC 96kHz／32bit]',
        '[220817] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 07': '[2022.08.17] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 07 [FLAC]',
        '[220928] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 08': '[2022.09.28] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 08 [FLAC]',
        '[221228] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 09': '[2022.12.28] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 09 [FLAC]',
        '[230208] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 10': '[2023.02.08] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 10 [FLAC]',
        '[230329] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 11 (FLAC 96kHz_24bit)': '[2023.03.29] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 11 [FLAC 96kHz／24bit]',
        '[230427] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 12 (WebFLAC)': '[2023.04.27] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 12 [WebFLAC]',
        '[230906] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 13 (WebFLAC)': '[2023.09.06] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 13 [WebFLAC]',
        '[230913] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 14 (WebFLAC)': '[2023.09.13] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 14 [WebFLAC]',
        '[240124] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 15 (FLAC 96kHz_24bit)': '[2024.01.24] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 15 [FLAC 96kHz／24bit]',
        '[240306] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 16 (FLAC 96kHz_24bit)': '[2024.03.06] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 16 [FLAC 96kHz／24bit]',
        '[240306] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 17 (FLAC 96kHz_24bit)': '[2024.03.06] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 17 [FLAC 96kHz／24bit]',
        '[240417] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 18 (FLAC 96kHz_24bit)': '[2024.04.17] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 18 [FLAC 96kHz／24bit]',
        '[240524] 劇場版『ウマ娘 プリティーダービー 新時代の扉』オリジナル・サウンドトラック (FLAC 96kHz_24bit)': '[2024.05.24] 劇場版『ウマ娘 プリティーダービー 新時代の扉』オリジナル・サウンドトラック [FLAC 96kHz／24bit]',
        '[240626] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 19 (FLAC 96kHz_24bit)': '[2024.06.26] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 19 [FLAC 96kHz／24bit]',
        'ウマ娘 プリティーダービー - O - ロライズ [FLAC 96kHz／24bit]': '[2024.05.10] 劇場版『ウマ娘 プリティーダービー 新時代の扉』主題歌「Ready!! Steady!! Derby!!」／O - ロライズ [FLAC 96kHz／24bit]',
        'ウマ娘 プリティーダービー WINNING LIVE 20 [FLAC 96kHz／24bit]': '[2024.07.31] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 20 [FLAC 96kHz／24bit]',
        'ウマ娘 プリティーダービー WINNING LIVE 21 [FLAC 96kHz／24bit]': '[2024.10.16] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 21 [FLAC 96kHz／24bit]',
        'ウマ娘 プリティーダービー WINNING LIVE 22 [FLAC 96kHz／24bit]': '[2024.12.11] スマホゲーム『ウマ娘 プリティーダービー』WINNING LIVE 22 [FLAC 96kHz／24bit]'
    }
    
    for old_name, new_name in rename_map.items():
        src = uma_dir / old_name
        dst = uma_dir / new_name
        if src.exists():
            print(f"  Renaming: {old_name}\n        -> {new_name}")
            shutil.move(str(src), str(dst))

# =========================================================================
# 6. REBUILD CATALOG.SQLITE
# =========================================================================
print("\n>>> 6. REBUILDING CATALOG.SQLITE <<<")
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
print(f"Catalog successfully rebuilt with {count} tracks indexed!")
print("\n" + "="*60)
print("ALL ANOMALIES RESOLVED SUCCESSFULLY!")
print("="*60)
