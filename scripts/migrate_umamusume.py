#!/usr/bin/env python3
import os
import re
import sys
import shutil
import subprocess
from pathlib import Path

TORRENT_ROOT = Path('/mnt/hdd-media/qbittorrent/watch-torrents/UmaMusu discography')
UMA_ROOT = Path('/mnt/hdd-backup/music/Lossless/Anime/Uma Musume ~')
SAFE_TEMP = Path('/tmp/astell_kern_backup')

DIR_WINNING   = UMA_ROOT / '01. WINNING LIVE Series'
DIR_DERBY     = UMA_ROOT / '02. ANIMATION DERBY Series'
DIR_GATE      = UMA_ROOT / '03. STARTING GATE Series'
DIR_SOLO      = UMA_ROOT / '04. SOLO VOCAL TRACKS'
DIR_SPINOFF   = UMA_ROOT / '05. UMAYURU & UMAYON'
DIR_OTHER     = UMA_ROOT / '06. Singles, OST & Other'
DIR_COMPIL    = UMA_ROOT / '07. Compilations'

ALL_DIRS = [DIR_WINNING, DIR_DERBY, DIR_GATE, DIR_SOLO, DIR_SPINOFF, DIR_OTHER, DIR_COMPIL]

def sanitize_smb(s: str) -> str:
    s = s.replace(':', '：').replace('/', '／').replace('\\', '＼')
    s = s.replace('*', '＊').replace('?', '？').replace('"', '＂')
    s = s.replace('<', '＜').replace('>', '＞').replace('|', '｜')
    return s

def get_audio_quality_tag(album_path: Path) -> str:
    flacs = list(album_path.rglob('*.flac'))
    if not flacs:
        return "[FLAC]"
    first_flac = flacs[0]
    sr = subprocess.run(['metaflac', '--show-sample-rate', str(first_flac)], capture_output=True, text=True).stdout.strip()
    bps = subprocess.run(['metaflac', '--show-bps', str(first_flac)], capture_output=True, text=True).stdout.strip()
    if sr and bps:
        if bps == '24':
            khz = int(sr) // 1000
            return f"[FLAC {khz}kHz／24bit]"
        elif bps == '16':
            return "[FLAC]"
    return "[FLAC]"

def flatten_album(alb: Path):
    AUDIO_EXTS = {'.flac', '.aiff', '.aif', '.alac', '.wav', '.m4a', '.mp3'}
    # Keep multi-disc intact if present
    subdirs = [d for d in alb.iterdir() if d.is_dir()]
    if any(d.name.lower().startswith('disc') for d in subdirs):
        return

    # Extract any inner zips
    for z in list(alb.rglob('*.zip')):
        bk_dir = alb / 'BK'
        bk_dir.mkdir(exist_ok=True)
        subprocess.run(['unzip', '-q', '-o', str(z), '-d', str(bk_dir)], check=False)
        z.unlink()

    # Move audio to root
    for f in list(alb.rglob('*')):
        if f.is_file() and f.suffix.lower() in AUDIO_EXTS:
            if f.parent != alb:
                dest = alb / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))

    # Clean empty directories
    for root, dirs, files in os.walk(alb, topdown=False):
        for d in dirs:
            dp = Path(root) / d
            if dp.name != 'BK' and not any(dp.iterdir()):
                try:
                    dp.rmdir()
                except Exception:
                    pass

def run_migration():
    print("=== STEP 1: Preserving Astell&Kern Special Compilation ===")
    old_astell = UMA_ROOT / '05. Compilations' / '[2018.12.14] ウマ娘 プリティーダービー Astell&Kern Special Compilation CD [FLAC 96kHz／24bit]'
    if SAFE_TEMP.exists():
        shutil.rmtree(str(SAFE_TEMP))
    if old_astell.exists():
        shutil.copytree(str(old_astell), str(SAFE_TEMP))
        print("  Astell&Kern saved to safe temp.")
    else:
        print("  Warning: old_astell not found!")

    print("\n=== STEP 2: Clearing obsolete existing library ===")
    for item in list(UMA_ROOT.iterdir()):
        if item.is_dir():
            shutil.rmtree(str(item))
            print(f"  Removed old category: {item.name}")

    print("\n=== STEP 3: Re-creating canonical directory skeleton ===")
    for d in ALL_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    print("\n=== STEP 4: Restoring Astell&Kern Special Compilation ===")
    if SAFE_TEMP.exists():
        dest = DIR_COMPIL / '[2018.12.14] ウマ娘 プリティーダービー Astell&Kern Special Compilation CD [FLAC 96kHz／24bit]'
        shutil.copytree(str(SAFE_TEMP), str(dest))
        shutil.rmtree(str(SAFE_TEMP))
        print("  Astell&Kern restored to 07. Compilations.")

    print("\n=== STEP 5: Copying and organizing 151 albums from Torrent ===")
    category_mapping = [
        ('[2021-2026] WINNING LIVE', DIR_WINNING),
        ('[2017-2024] ANIMATION DERBY', DIR_DERBY),
        ('[2016-2021] STARTING GATE', DIR_GATE),
        ('[2021-2025] SOLO VOCAL TRACKS', DIR_SOLO),
        ('[2020-2021] UMAYON', DIR_SPINOFF),
        ('[2022-2025] UMAYURU', DIR_SPINOFF),
        ('[2018-2026] OTHER', DIR_OTHER)
    ]

    copied_count = 0
    for src_folder_name, target_dir in category_mapping:
        src_path = TORRENT_ROOT / src_folder_name
        if not src_path.exists():
            print(f"  Warning: {src_folder_name} not found!")
            continue

        print(f"\nProcessing {src_folder_name} -> {target_dir.name}...")
        for alb in sorted(src_path.iterdir()):
            if not alb.is_dir():
                continue

            # Determine audio format tag
            tag = get_audio_quality_tag(alb)

            # Build canonical folder name
            clean_name = alb.name
            # If date prefix is e.g. [2021.03.17]
            clean_name = sanitize_smb(clean_name)
            if not clean_name.endswith(']'):
                canonical_name = f"{clean_name} {tag}"
            else:
                canonical_name = clean_name

            dest_album = target_dir / canonical_name
            print(f"  Copying: {alb.name} -> {canonical_name}")
            shutil.copytree(str(alb), str(dest_album))
            flatten_album(dest_album)
            copied_count += 1

    print(f"\nSuccessfully copied and organized {copied_count} albums!")

    print("\n=== STEP 6: Setting Permissions (100000:100000, 775/664) ===")
    subprocess.run(['chown', '-R', '100000:100000', str(UMA_ROOT)], check=False)
    subprocess.run(['find', str(UMA_ROOT), '-type', 'd', '-exec', 'chmod', '775', '{}', '+'], check=False)
    subprocess.run(['find', str(UMA_ROOT), '-type', 'f', '-exec', 'chmod', '664', '{}', '+'], check=False)
    print("Permissions updated.")

if __name__ == '__main__':
    run_migration()
