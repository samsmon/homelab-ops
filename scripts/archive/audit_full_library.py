#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path('/mnt/hdd-backup/music/Lossless')
FORBIDDEN_CHARS = set(r'\/:*?"<>|')

def run_deep_audit():
    print(f"=== FULL MASTER LIBRARY AUDIT ({ROOT}) ===")
    
    anomalies = {
        'forbidden_char_dirs': [],
        'forbidden_char_files': [],
        'zero_byte_files': [],
        'nested_audio_dirs': [],
        'loose_albums': [],
        'redundant_cues': [],
        'unsplit_cue_images': [],
        'lossy_in_lossless': [],
        'junk_files': [],
        'corrupt_flacs': []
    }

    # 1. Check for loose albums in category roots
    for cat in ROOT.iterdir():
        if not cat.is_dir():
            continue
        for child in cat.iterdir():
            if child.is_dir() and not child.name.endswith('~'):
                anomalies['loose_albums'].append(str(child))

    # 2. Walk entire tree
    total_files = 0
    total_flacs = 0
    
    for root, dirs, files in os.walk(ROOT):
        rpath = Path(root)
        
        # Check folder name
        for char in FORBIDDEN_CHARS:
            if char in rpath.name:
                anomalies['forbidden_char_dirs'].append(str(rpath))
                break

        # Check nested audio folders
        if rpath.name.lower() in ['flac', 'wav', 'mp3'] and rpath != ROOT:
            anomalies['nested_audio_dirs'].append(str(rpath))

        cues = [f for f in files if f.lower().endswith('.cue')]
        flacs = [f for f in files if f.lower().endswith('.flac')]
        total_flacs += len(flacs)
        total_files += len(files)

        if cues and len(flacs) > 1:
            anomalies['redundant_cues'].append((str(rpath), cues))
        elif cues and len(flacs) == 1:
            # Single FLAC image with CUE
            anomalies['unsplit_cue_images'].append((str(rpath), cues, flacs))

        for f in files:
            fpath = rpath / f
            lower = f.lower()
            
            # Check 0-byte
            try:
                if fpath.stat().st_size == 0:
                    anomalies['zero_byte_files'].append(str(fpath))
            except Exception:
                pass

            # Check forbidden chars in filename
            for char in FORBIDDEN_CHARS:
                if char in f:
                    anomalies['forbidden_char_files'].append(str(fpath))
                    break

            # Check lossy audio in Lossless
            if lower.endswith(('.mp3', '.m4a', '.aac', '.ogg', '.wma')):
                # Check if it is a real lossy or ALAC m4a
                anomalies['lossy_in_lossless'].append(str(fpath))

            # Check junk files
            if lower.endswith(('.url', '.lnk')) or lower in ['read.txt', 'discord.txt', 'readme.txt', 'desktop.ini', 'thumbs.db']:
                anomalies['junk_files'].append(str(fpath))

    print("\n" + "="*70)
    print("AUDIT SUMMARY REPORT")
    print("="*70)
    print(f"Total Audio Files Scanned: {total_files} ({total_flacs} FLACs)")
    for key, items in anomalies.items():
        print(f"- {key}: {len(items)}")

    print("\n" + "="*70)
    print("DETAILED ANOMALIES")
    print("="*70)
    for key, items in anomalies.items():
        if items:
            print(f"\n[{key.upper()}] ({len(items)} items):")
            for it in items[:15]:
                print(f"  {it}")
            if len(items) > 15:
                print(f"  ... and {len(items)-15} more.")

if __name__ == '__main__':
    run_deep_audit()
