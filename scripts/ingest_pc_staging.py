#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INGEST PC STAGING SCRIPT
Unpacks, categorizes, normalizes, and absorbs all 122 GB from /mnt/hdd-backup/download_pc_staging/
into the master archive /mnt/hdd-backup/music/Lossless/.
"""

import os
import re
import sys
import time
import shutil
import subprocess
from pathlib import Path

# Add script dir to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from master_music_centralization import (
    LOSSLESS_ROOT, LOSSY_ROOT, MUSIC_ROOT,
    clean_album_title, sanitize_filename, safe_move,
    resolve_umbrella, phase_3_split_cue_and_unpack,
    phase_4_ingest_and_normalize, phase_5_purify_master_library,
    phase_6_permissions_and_catalog, ALL_MUSIC_EXTENSIONS, log
)

PC_STAGING_ROOT = Path('/mnt/hdd-backup/download_pc_staging')

def extract_general_anime_singles():
    log("=== EXTRACTING & PARSING GENERAL ANIME SINGLES ===")
    gen_dir = PC_STAGING_ROOT / 'Anime' / 'General Anime Singles & OST'
    if not gen_dir.exists():
        log("No General Anime Singles folder found in staging.")
        return

    archives = list(gen_dir.glob('*.zip')) + list(gen_dir.glob('*.rar')) + list(gen_dir.glob('*.7z'))
    log(f"Found {len(archives)} archives in General Anime Singles...")
    
    for idx, arch in enumerate(archives, 1):
        filename = arch.name
        # 1. Parse artist from filename: ／([^／\[\]]+)\s*\[ or - ([^-\[\]]+)\s*\[
        artist = None
        m_artist = re.search(r'／([^／\[\]]+)\s*\[', filename)
        if m_artist:
            artist = m_artist.group(1).strip()
        else:
            m_dash = re.search(r'\s*-\s*([^-\[\]]+)\s*\[', filename)
            if m_dash:
                artist = m_dash.group(1).strip()
                
        # 2. Parse album title from filename: 「([^」]+)」
        title = None
        m_title = re.search(r'「([^」]+)」', filename)
        if m_title:
            title = m_title.group(1).strip()
        else:
            title = clean_album_title(arch.stem)

        # Temporary extraction folder
        temp_dir = PC_STAGING_ROOT / '_temp_extract' / f"single_{idx}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        res = subprocess.run(['7z', 'x', '-y', f'-o{temp_dir}', str(arch)], capture_output=True)
        if res.returncode != 0:
            log(f"Failed to extract {filename}: {res.stderr.decode('utf-8', 'ignore')}", "WARN")
            shutil.rmtree(temp_dir, ignore_errors=True)
            continue

        # If artist still unknown, try reading Vorbis tag from extracted flac
        if not artist or len(artist) > 40:
            for audio in temp_dir.rglob('*.flac'):
                try:
                    import mutagen
                    f = mutagen.File(str(audio))
                    if f and 'artist' in f:
                        artist = f['artist'][0].strip()
                        break
                except Exception:
                    pass

        if not artist:
            artist = "Various Artists"

        # Clean artist name & resolve umbrella
        artist_clean = re.sub(r'[\(\[].*?[\)\]]', '', artist).strip()
        if not artist_clean:
            artist_clean = artist.strip()
        
        target_cat, umbrella_1, umbrella_2 = resolve_umbrella('J-Pop', artist_clean)
        
        if umbrella_2:
            target_artist_dir = LOSSLESS_ROOT / target_cat / umbrella_1 / umbrella_2
        else:
            target_artist_dir = LOSSLESS_ROOT / target_cat / umbrella_1
            
        target_album_dir = target_artist_dir / clean_album_title(title)
        target_album_dir.mkdir(parents=True, exist_ok=True)

        # Flatten audio files directly into target_album_dir
        for audio in list(temp_dir.rglob('*')):
            if audio.is_file():
                ext = audio.suffix.lower()
                if ext in ALL_MUSIC_EXTENSIONS or ext in ['.jpg', '.png']:
                    clean_name = sanitize_filename(audio.name)
                    safe_move(audio, target_album_dir / clean_name)

        shutil.rmtree(temp_dir, ignore_errors=True)
        arch.unlink()
        
        if idx % 50 == 0 or idx == len(archives):
            log(f"  Processed {idx}/{len(archives)} general anime singles...")

    try:
        gen_dir.rmdir()
    except OSError:
        pass
    log("General Anime Singles extracted successfully.")

def unpack_all_staging_archives():
    log("=== UNPACKING ALL ARCHIVES IN PC STAGING ===")
    archives = []
    for ext in ['*.zip', '*.rar', '*.7z']:
        for p in PC_STAGING_ROOT.rglob(ext):
            if 'General Anime Singles' not in str(p):
                archives.append(p)
                
    log(f"Found {len(archives)} albums in archive format to unpack...")
    
    for idx, arch in enumerate(archives, 1):
        album_name = clean_album_title(arch.stem)
        target_album_dir = arch.parent / album_name
        target_album_dir.mkdir(parents=True, exist_ok=True)
        
        res = subprocess.run(['7z', 'x', '-y', f'-o{target_album_dir}', str(arch)], capture_output=True)
        if res.returncode == 0:
            arch.unlink()
            # If target_album_dir contains only 1 folder, flatten it
            subdirs = [d for d in target_album_dir.iterdir() if d.is_dir() and d.name not in ['BK', 'Scans', 'Disc 1', 'Disc 2']]
            files = [f for f in target_album_dir.iterdir() if f.is_file()]
            if len(subdirs) == 1 and len(files) == 0:
                inner = subdirs[0]
                for item in list(inner.iterdir()):
                    safe_move(item, target_album_dir / item.name)
                try:
                    inner.rmdir()
                except OSError:
                    pass
        else:
            log(f"Warning extracting {arch.name}: {res.stderr.decode('utf-8', 'ignore')}", "WARN")

        if idx % 50 == 0 or idx == len(archives):
            log(f"  Unpacked {idx}/{len(archives)} archives...")

    log("All archives unpacked.")

def main():
    start_time = time.time()
    log("STARTING INGESTION OF PC STAGING DATA")
    
    # 1. Extract General Anime Singles into commercial J-Pop
    extract_general_anime_singles()
    
    # 2. Unpack all remaining archives in staging
    unpack_all_staging_archives()
    
    # 3. Split any CUE disc images in staging
    phase_3_split_cue_and_unpack([PC_STAGING_ROOT])
    
    # 4. Ingest and normalize staging into Lossless master
    phase_4_ingest_and_normalize(PC_STAGING_ROOT)
    
    # 5. Master purification across the entire library
    phase_5_purify_master_library()
    
    # 6. Rebuild permissions and catalog
    phase_6_permissions_and_catalog()
    
    # Remove flag and empty staging
    flag = PC_STAGING_ROOT / 'upload_complete.flag'
    if flag.exists():
        flag.unlink()
        
    elapsed = time.time() - start_time
    log(f"PC STAGING INGESTION FINISHED IN {elapsed:.2f} SECONDS!")

if __name__ == '__main__':
    main()
