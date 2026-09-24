#!/usr/bin/env python3
import os
import re
import sys
import glob
import shutil
import zipfile
import subprocess
from pathlib import Path

DOWNLOAD_DIR = Path('/mnt/hdd-backup/download')
SHINY_ROOT = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~/シャイニーカラーズ')
TEMP_DIR = Path('/mnt/hdd-backup/download/~extract_shiny')

# Target Categories (Option A)
WING_ROOT = SHINY_ROOT / '01. WING & Main Game Series'
DIR_BRILLIANT = WING_ROOT / '01. BRILLI@NT WING (2018)'
DIR_FRAGMENT  = WING_ROOT / '02. FR@GMENT WING (2019)'
DIR_GRADATE   = WING_ROOT / '03. GR@DATE WING (2020)'
DIR_LAYERED   = WING_ROOT / '04. L@YERED WING (2021)'
DIR_PANORAMA  = WING_ROOT / '05. PANOR@MA WING (2022)'
DIR_CANVAS    = WING_ROOT / '06. "CANVAS" (2023)'
DIR_ECHOES    = WING_ROOT / '07. ECHOES (2024)'

DIR_PRISM     = SHINY_ROOT / '02. Song for Prism Series'
DIR_ANIME     = SHINY_ROOT / '03. Anime Series'
DIR_FEATHERS  = SHINY_ROOT / '04. COLORFUL FE@THERS Series'
DIR_SYNTHE    = SHINY_ROOT / '05. Synthe-Side & Collaborations'

ALL_DIRS = [
    DIR_BRILLIANT, DIR_FRAGMENT, DIR_GRADATE, DIR_LAYERED, DIR_PANORAMA,
    DIR_CANVAS, DIR_ECHOES, DIR_PRISM, DIR_ANIME, DIR_FEATHERS, DIR_SYNTHE
]

def sanitize_smb(s: str) -> str:
    s = s.replace(':', '：').replace('/', '／').replace('\\', '＼')
    s = s.replace('*', '＊').replace('?', '？').replace('"', '＂')
    s = s.replace('<', '＜').replace('>', '＞').replace('|', '｜')
    return s

def normalize_date(date_str: str) -> str:
    date_str = date_str.strip('[]')
    if len(date_str) == 6 and date_str.isdigit():
        yy = int(date_str[:2])
        century = '20' if yy <= 40 else '19'
        return f"[{century}{date_str[:2]}.{date_str[2:4]}.{date_str[4:6]}]"
    elif len(date_str) == 8 and date_str.isdigit():
        return f"[{date_str[:4]}.{date_str[4:6]}.{date_str[6:8]}]"
    return f"[{date_str}]"

def classify_archive(filename: str):
    clean_name = re.sub(r'\s*\(\d+\)', '', filename)
    clean_name = re.sub(r'\.zip$', '', clean_name, flags=re.IGNORECASE)

    # Format detection
    fmt = ""
    m_fmt = re.search(r'[\(\[]([A-Z]+)\s+([0-9]+k?Hz)?[_／]([0-9]+bit)[\)\]]', clean_name, re.IGNORECASE)
    if m_fmt:
        codec = m_fmt.group(1).upper()
        rate = m_fmt.group(2) or ""
        bit = m_fmt.group(3) or ""
        if rate and bit:
            fmt = f"[{codec} {rate}／{bit}]"
        elif bit:
            fmt = f"[{codec} {bit}]"
        else:
            fmt = f"[{codec}]"
    elif 'flac' in clean_name.lower():
        fmt = "[FLAC 96kHz／24bit]"
    elif 'aiff' in clean_name.lower():
        fmt = "[AIFF 96kHz／32bit]"
    elif 'alac' in clean_name.lower():
        fmt = "[ALAC 96kHz／32bit]"

    # Date extraction & cleanup
    date_prefix = ""
    m_date = re.match(r'^\[(\d{6}|\d{8})\]', clean_name)
    if m_date:
        date_prefix = normalize_date(m_date.group(1))
        clean_name = clean_name[len(m_date.group(0)):].strip()
    elif m_date2 := re.match(r'^\[(\d{6})\]\[(\d{6})\]', clean_name):
        date_prefix = normalize_date(m_date2.group(2))
        clean_name = clean_name[len(m_date2.group(0)):].strip()

    # Strip format tag from title
    clean_name = re.sub(r'[\(\[][A-Z0-9_\s／\+\-]*bit[\)\]]', '', clean_name, flags=re.IGNORECASE).strip()

    upper = clean_name.upper()
    if 'BRILLI@NT WING' in upper or 'BRILLIANT WING' in upper:
        target_dir = DIR_BRILLIANT
    elif 'FR@GMENT WING' in upper or 'FRAGMENT WING' in upper:
        target_dir = DIR_FRAGMENT
    elif 'GR@DATE WING' in upper or 'GRADATE WING' in upper or 'シャイノグラフィ' in clean_name:
        target_dir = DIR_GRADATE
    elif 'L@YERED WING' in upper or 'LAYERED WING' in upper:
        target_dir = DIR_LAYERED
    elif 'PANOR@MA WING' in upper or 'PANORAMA WING' in upper:
        target_dir = DIR_PANORAMA
    elif 'CANVAS' in upper:
        target_dir = DIR_CANVAS
    elif 'ECHOES' in upper:
        target_dir = DIR_ECHOES
    elif 'COLORFUL FE@THERS' in upper or 'COLORFUL FEATHERS' in upper:
        target_dir = DIR_FEATHERS
    elif 'SYNTHE-SIDE' in upper:
        target_dir = DIR_SYNTHE
    elif 'SONG FOR PRISM' in upper:
        target_dir = DIR_PRISM
    elif any(k in clean_name for k in ['アニメ', 'ツバサグラビティ', 'プリズムフレア', 'Happy Surprise Trick', 'Over the prism']):
        target_dir = DIR_ANIME
    else:
        target_dir = DIR_FEATHERS

    title = sanitize_smb(clean_name)
    if date_prefix:
        canonical_name = f"{date_prefix} {title} {fmt}".strip()
    else:
        canonical_name = f"{title} {fmt}".strip()
    canonical_name = re.sub(r'\s+', ' ', canonical_name)

    return target_dir, canonical_name

def step1_migrate_existing():
    """Migrate currently existing folders into Option A hierarchy."""
    print("=== STEP 1: Creating Option A directory skeleton ===")
    for d in ALL_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    old_echoes = SHINY_ROOT / '02. ECHOES Series'
    if old_echoes.exists() and old_echoes != DIR_ECHOES:
        print("Migrating existing ECHOES albums into 01. WING & Main Game Series/07. ECHOES (2024)...")
        for item in list(old_echoes.iterdir()):
            if item.is_dir():
                dest = DIR_ECHOES / item.name
                if not dest.exists():
                    shutil.move(str(item), str(dest))
                    print(f"  Moved: {item.name}")
        try:
            old_echoes.rmdir()
            print("  Removed old 02. ECHOES Series")
        except Exception as e:
            print(f"  Note: {e}")

    old_prism = SHINY_ROOT / '01. Song for Prism Series'
    if old_prism.exists() and old_prism != DIR_PRISM:
        print("Migrating existing Song for Prism albums into 02. Song for Prism Series...")
        for item in list(old_prism.iterdir()):
            if item.is_dir():
                dest = DIR_PRISM / item.name
                if not dest.exists():
                    shutil.move(str(item), str(dest))
                    print(f"  Moved: {item.name}")
        try:
            old_prism.rmdir()
            print("  Removed old 01. Song for Prism Series")
        except Exception as e:
            print(f"  Note: {e}")

    old_units = SHINY_ROOT / '04. Unit Singles & Compilations'
    if old_units.exists() and old_units != DIR_FEATHERS:
        print("Migrating existing Unit Singles into 04. COLORFUL FE@THERS Series...")
        for item in list(old_units.iterdir()):
            if item.is_dir():
                dest = DIR_FEATHERS / item.name
                if not dest.exists():
                    shutil.move(str(item), str(dest))
                    print(f"  Moved: {item.name}")
        try:
            old_units.rmdir()
            print("  Removed old 04. Unit Singles & Compilations")
        except Exception as e:
            print(f"  Note: {e}")

def flatten_extracted_album(dest_path: Path):
    """Ensure flat root: audio files directly in dest_path, artwork in root or BK/."""
    AUDIO_EXTS = ['.flac', '.aiff', '.alac', '.wav', '.m4a', '.mp3']
    all_files = list(dest_path.rglob('*'))
    audio_files = [f for f in all_files if f.is_file() and f.suffix.lower() in AUDIO_EXTS]

    if not audio_files:
        return

    # Check for inner zips (e.g. lacm*.zip booklet zip)
    inner_zips = [f for f in all_files if f.is_file() and f.suffix.lower() == '.zip']
    for iz in inner_zips:
        try:
            bk_dir = dest_path / 'BK'
            bk_dir.mkdir(exist_ok=True)
            subprocess.run(['unzip', '-q', '-o', str(iz), '-d', str(bk_dir)], check=False)
            iz.unlink()
        except Exception:
            pass

    # Move audio files directly to dest_path
    for af in audio_files:
        if af.parent != dest_path:
            target_file = dest_path / af.name
            if not target_file.exists():
                shutil.move(str(af), str(target_file))

    # Handle image files
    img_files = [f for f in dest_path.rglob('*') if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    has_cover = any(f.name.lower() in ['cover.jpg', 'cover.png', 'folder.jpg'] for f in dest_path.glob('*'))

    for img in img_files:
        if 'order_' in img.name: # e-onkyo receipts
            bk_dir = dest_path / 'BK'
            bk_dir.mkdir(exist_ok=True)
            shutil.move(str(img), str(bk_dir / img.name))
        elif img.parent != dest_path and not str(img.parent).endswith('/BK'):
            if not has_cover:
                shutil.move(str(img), str(dest_path / 'Cover.jpg'))
                has_cover = True
            else:
                bk_dir = dest_path / 'BK'
                bk_dir.mkdir(exist_ok=True)
                target_img = bk_dir / img.name
                if not target_img.exists():
                    shutil.move(str(img), str(target_img))

    # Remove empty subdirectories & junk files
    for f in list(dest_path.rglob('*')):
        if f.is_file() and f.suffix.lower() in ['.url', '.txt']:
            f.unlink()

    # Clean up empty folders from deepest to shallowest
    for root, dirs, files in os.walk(dest_path, topdown=False):
        for d in dirs:
            dp = Path(root) / d
            if dp.name != 'BK' and not any(dp.iterdir()):
                try:
                    dp.rmdir()
                except Exception:
                    pass

def step2_extract_and_ingest():
    keywords = ['shiny', 'prism', 'echoes', 'シャイニー', 'brilli@nt', 'fr@gment', 'gr@date', 'l@yered', 'panor@ma', 'synthe-side']
    archives = []
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for f in files:
            if not f.endswith('.zip'):
                continue
            fl = f.lower()
            if any(k in fl for k in keywords):
                if 'weather_planet' in fl or 'prism_2026' in fl:
                    continue
                archives.append(Path(root) / f)

    # Deduplicate: take 1 per release
    unique_map = {}
    for a in sorted(archives):
        key = re.sub(r'\s*\(\d+\)', '', a.name)
        if key not in unique_map:
            unique_map[key] = a
        else:
            if '(2)' in a.name and '(2)' not in unique_map[key].name:
                pass
            elif '(2)' not in a.name:
                unique_map[key] = a

    print(f"\n=== STEP 2: Processing {len(unique_map)} Unique Archives ===")
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    extracted_count = 0
    skipped_count = 0

    for key, arch in sorted(unique_map.items()):
        target_dir, canonical_name = classify_archive(arch.name)
        final_dest = target_dir / canonical_name

        # Check if already present in target or anywhere under SHINY_ROOT
        # (e.g. Song for Prism or Anime albums already placed)
        already_exists = False
        if final_dest.exists() and any(f.suffix.lower() in ['.flac', '.aiff', '.alac'] for f in final_dest.glob('*')):
            already_exists = True
        else:
            # Check for partial match (same title/date) in target_dir
            for existing_album in target_dir.iterdir():
                if existing_album.is_dir() and canonical_name[:30] in existing_album.name:
                    already_exists = True
                    break

        if already_exists:
            print(f"[EXISTS] Skipping: {canonical_name}")
            skipped_count += 1
            continue

        print(f"\n[EXTRACTING] {arch.name}")
        print(f"       -->  {target_dir.name} / {canonical_name}")

        temp_album_dir = TEMP_DIR / canonical_name
        if temp_album_dir.exists():
            shutil.rmtree(str(temp_album_dir))
        temp_album_dir.mkdir(parents=True, exist_ok=True)

        # Extract using 7z
        res = subprocess.run(['7z', 'x', '-y', f'-o{temp_album_dir}', str(arch)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print(f"  [ERROR] Failed to extract {arch.name}: {res.stderr.decode('utf-8', errors='ignore')}")
            shutil.rmtree(str(temp_album_dir), ignore_errors=True)
            continue

        # Flatten & organize album structure
        flatten_extracted_album(temp_album_dir)

        # Move to final destination
        if final_dest.exists():
            shutil.rmtree(str(final_dest))
        shutil.move(str(temp_album_dir), str(final_dest))
        extracted_count += 1

    # Cleanup temp
    shutil.rmtree(str(TEMP_DIR), ignore_errors=True)

    # Fix permissions
    print("\nFixing permissions across SHINY_ROOT (100000:100000, 775/664)...")
    subprocess.run(['chown', '-R', '100000:100000', str(SHINY_ROOT)], check=False)
    subprocess.run(['find', str(SHINY_ROOT), '-type', 'd', '-exec', 'chmod', '775', '{}', '+'], check=False)
    subprocess.run(['find', str(SHINY_ROOT), '-type', 'f', '-exec', 'chmod', '664', '{}', '+'], check=False)

    print(f"\nFinished: Extracted {extracted_count} new albums, Skipped {skipped_count} existing albums.")

if __name__ == '__main__':
    step1_migrate_existing()
    step2_extract_and_ingest()
