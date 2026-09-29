#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path('/mnt/hdd-backup/music/Lossless')

def clean_anomalies():
    print("=== STEP 1: Flattening 11 Nested Audio Directories (FLAC/ / WAV/) ===")
    AUDIO_EXTS = {'.flac', '.wav', '.m4a', '.mp3', '.aif', '.aiff'}
    
    for root, dirs, files in os.walk(ROOT):
        rpath = Path(root)
        if rpath.name.lower() in ['flac', 'wav'] and rpath != ROOT:
            parent = rpath.parent
            print(f"Flattening nested folder: {rpath.relative_to(ROOT)}")
            for f in rpath.iterdir():
                if f.is_file():
                    dest = parent / f.name
                    if not dest.exists():
                        shutil.move(str(f), str(dest))
                    else:
                        f.unlink()
            try:
                rpath.rmdir()
                print(f"  Removed empty folder: {rpath.name}")
            except Exception as e:
                print(f"  Could not remove {rpath.name}: {e}")

    print("\n=== STEP 2: Removing 245 Junk Files (.url, Discord.txt, Read.txt, etc.) ===")
    junk_names = {'discord.txt', 'read.txt', 'readme.txt', 'desktop.ini', 'thumbs.db'}
    junk_count = 0
    for root, dirs, files in os.walk(ROOT):
        for f in files:
            lower = f.lower()
            if lower.endswith(('.url', '.lnk')) or lower in junk_names:
                fpath = Path(root) / f
                try:
                    fpath.unlink()
                    junk_count += 1
                except Exception:
                    pass
    print(f"Removed {junk_count} junk advertisement files.")

    print("\n=== STEP 3: Removing Redundant .cue Sheets (Where Split Tracks Already Exist) ===")
    cue_count = 0
    for root, dirs, files in os.walk(ROOT):
        rpath = Path(root)
        cues = [f for f in files if f.lower().endswith('.cue')]
        flacs = [f for f in files if f.lower().endswith('.flac')]
        # If split tracks are present (>1 flac), the CUE causes duplicate track parsing in MusicBee
        if cues and len(flacs) > 1:
            for c in cues:
                cpath = rpath / c
                try:
                    cpath.unlink()
                    cue_count += 1
                except Exception:
                    pass
    print(f"Removed {cue_count} redundant CUE sheets.")

    print("\n=== STEP 4: Enforcing Ownership (100000:100000) and Permissions (775/664) ===")
    subprocess.run(['chown', '-R', '100000:100000', str(ROOT)], check=False)
    subprocess.run(['find', str(ROOT), '-type', 'd', '-exec', 'chmod', '775', '{}', '+'], check=False)
    subprocess.run(['find', str(ROOT), '-type', 'f', '-exec', 'chmod', '664', '{}', '+'], check=False)
    print("Permissions updated.")

if __name__ == '__main__':
    clean_anomalies()
