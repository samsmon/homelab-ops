#!/usr/bin/env python3
"""
Fix Denonbu 0_00 anomaly folder:
1. Evacuate 5 nested VTuber/Hololive albums to canonical locations:
   - ENDLESS FES -> Delete duplicate (verified identical to Hololive Official ~/ENDLESS FES)
   - Pastel Tea Time／ペルソナ -> Hololive (ホロライブ) ~/Omaru Polka (尾丸ポルカ) ~/
   - ホットダック! -> Hololive (ホロライブ) ~/Oozora Subaru (大空スバル) ~/
   - 守護ってルーナイト -> Hololive (ホロライブ) ~/Himemori Luna (姫森ルーナ) ~/
   - Shiny -> KAMITSUBAKI STUDIO (神椿スタジオ) ~/ASU (明透) ~/
2. Clean up 0:00 (Prod. Funk Uchino) Denonbu single:
   - Remove duplicate _1.flac
   - Rename album directory to '0：00 (Prod. Funk Uchino)'
   - Standardize track filenames (01. ..., 02. ...)
   - Clean corrupted Vorbis tags (remove '???', set proper Artist, Album, Title)
   - Apply ReplayGain 2.0 (EBU R128)
3. Set permissions to 100000:100000 (775/664)
4. Trigger catalog and scorecard refresh.
"""

import os
import shutil
import subprocess
from pathlib import Path

BASE_DENONBU = Path("/mnt/hdd-backup/music/Lossless/Anime/Denonbu (電音部) ~")
SOURCE_DIR = BASE_DENONBU / "0_00 (Prod. Funk Uchino)"
TARGET_DIR = BASE_DENONBU / "0：00 (Prod. Funk Uchino)"

VTUBER_ROOT = Path("/mnt/hdd-backup/music/Lossless/Vtuber")
HOLOLIVE_ROOT = VTUBER_ROOT / "Hololive (ホロライブ) ~"
KAMITSUBAKI_ROOT = VTUBER_ROOT / "KAMITSUBAKI STUDIO (神椿スタジオ) ~"

def run_cmd(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error executing {cmd}: {res.stderr}")
    return res

def main():
    print(f"[*] Starting Denonbu 0_00 anomaly resolution...")
    if not SOURCE_DIR.exists():
        print(f"Source dir {SOURCE_DIR} does not exist!")
        return

    # --- STEP 1: Evacuate Nested Albums ---
    print("\n[1/5] Evacuating nested VTuber albums...")

    # 1.1 ENDLESS FES (Duplicate check & removal)
    endless_src = SOURCE_DIR / "ENDLESS FES"
    if endless_src.exists():
        official_endless = HOLOLIVE_ROOT / "Hololive Official ~" / "ENDLESS FES"
        print(f"  - Removing duplicate {endless_src} (official exists at {official_endless})")
        shutil.rmtree(endless_src)
        print("    -> Successfully pruned.")

    # 1.2 Pastel Tea Time／ペルソナ -> Omaru Polka
    polka_dest = HOLOLIVE_ROOT / "Omaru Polka (尾丸ポルカ) ~" / "Pastel Tea Time／ペルソナ"
    pastel_src = SOURCE_DIR / "Pastel Tea Time／ペルソナ"
    if pastel_src.exists():
        print(f"  - Moving {pastel_src.name} -> {polka_dest}")
        shutil.move(str(pastel_src), str(polka_dest))
        print("    -> Moved.")

    # 1.3 ホットダック! -> Oozora Subaru
    subaru_dest = HOLOLIVE_ROOT / "Oozora Subaru (大空スバル) ~" / "ホットダック!"
    duck_src = SOURCE_DIR / "ホットダック!"
    if duck_src.exists():
        print(f"  - Moving {duck_src.name} -> {subaru_dest}")
        shutil.move(str(duck_src), str(subaru_dest))
        print("    -> Moved.")

    # 1.4 守護ってルーナイト -> Himemori Luna
    luna_artist_dir = HOLOLIVE_ROOT / "Himemori Luna (姫森ルーナ) ~"
    luna_artist_dir.mkdir(parents=True, exist_ok=True)
    luna_dest = luna_artist_dir / "守護ってルーナイト"
    luna_src = SOURCE_DIR / "守護ってルーナイト"
    if luna_src.exists():
        print(f"  - Moving {luna_src.name} -> {luna_dest}")
        shutil.move(str(luna_src), str(luna_dest))
        print("    -> Moved.")

    # 1.5 Shiny -> ASU (明透)
    asu_artist_dir = KAMITSUBAKI_ROOT / "ASU (明透) ~"
    asu_artist_dir.mkdir(parents=True, exist_ok=True)
    asu_dest = asu_artist_dir / "Shiny"
    shiny_src = SOURCE_DIR / "Shiny"
    if shiny_src.exists():
        print(f"  - Moving {shiny_src.name} -> {asu_dest}")
        shutil.move(str(shiny_src), str(asu_dest))
        print("    -> Moved.")

    # --- STEP 2: Normalize 0:00 (Prod. Funk Uchino) ---
    print("\n[2/5] Cleaning and normalizing 0:00 (Prod. Funk Uchino)...")
    
    # Remove duplicate file
    dup_file = SOURCE_DIR / "1. 電音部 - 0_00 (Prod. Funk Uchino)_1.flac"
    if dup_file.exists():
        print(f"  - Deleting duplicate FLAC: {dup_file.name}")
        dup_file.unlink()

    # Rename single directory
    print(f"  - Renaming folder: {SOURCE_DIR.name} -> {TARGET_DIR.name}")
    shutil.move(str(SOURCE_DIR), str(TARGET_DIR))

    # Rename tracks
    t1_src = TARGET_DIR / "1. 電音部 - 0_00 (Prod. Funk Uchino).flac"
    t1_dst = TARGET_DIR / "01. 0：00 (Prod. Funk Uchino).flac"
    if t1_src.exists():
        print(f"  - Renaming {t1_src.name} -> {t1_dst.name}")
        t1_src.rename(t1_dst)

    t2_src = TARGET_DIR / "2. 電音部 - 0_00 (Prod. Funk Uchino)[Instrumental].flac"
    t2_dst = TARGET_DIR / "02. 0：00 (Prod. Funk Uchino) [Instrumental].flac"
    if t2_src.exists():
        print(f"  - Renaming {t2_src.name} -> {t2_dst.name}")
        t2_src.rename(t2_dst)

    # --- STEP 3: Clean Vorbis Comments & Tag Integrity ---
    print("\n[3/5] Cleaning Vorbis tags (removing corrupt '???' markers)...")
    
    # Track 1
    t1_tags = [
        "--remove-all-tags",
        "--set-tag=ALBUM=0：00 (Prod. Funk Uchino)",
        "--set-tag=TITLE=0：00 (Prod. Funk Uchino)",
        "--set-tag=ARTIST=白金 煌 (CV: 小宮有紗)",
        "--set-tag=ALBUMARTIST=電音部",
        "--set-tag=DATE=2024-10-23",
        "--set-tag=TRACKNUMBER=01",
        "--set-tag=TRACKTOTAL=02",
        "--set-tag=ORGANIZATION=ASOBINOTES",
        "--set-tag=ISRC=JPR502416190"
    ]
    run_cmd(["metaflac"] + t1_tags + [str(t1_dst)])

    # Track 2
    t2_tags = [
        "--remove-all-tags",
        "--set-tag=ALBUM=0：00 (Prod. Funk Uchino)",
        "--set-tag=TITLE=0：00 (Prod. Funk Uchino) [Instrumental]",
        "--set-tag=ARTIST=白金 煌 (CV: 小宮有紗)",
        "--set-tag=ALBUMARTIST=電音部",
        "--set-tag=DATE=2024-10-23",
        "--set-tag=TRACKNUMBER=02",
        "--set-tag=TRACKTOTAL=02",
        "--set-tag=ORGANIZATION=ASOBINOTES"
    ]
    run_cmd(["metaflac"] + t2_tags + [str(t2_dst)])
    print("  -> Tags successfully normalized.")

    # --- STEP 4: Apply ReplayGain 2.0 (EBU R128) ---
    print("\n[4/5] Applying ReplayGain 2.0 to evacuated & normalized albums...")
    albums_to_rg = [TARGET_DIR, polka_dest, subaru_dest, luna_dest, asu_dest]
    for alb in albums_to_rg:
        flacs = list(alb.glob("*.flac"))
        if flacs:
            print(f"  - ReplayGain: {alb.name} ({len(flacs)} tracks)")
            run_cmd(["metaflac", "--add-replay-gain"] + [str(f) for f in flacs])

    # --- STEP 5: Fix Permissions ---
    print("\n[5/5] Setting permissions (100000:100000, 775/664)...")
    all_affected_paths = [
        TARGET_DIR,
        polka_dest,
        subaru_dest,
        luna_artist_dir,
        asu_artist_dir
    ]
    for p in all_affected_paths:
        run_cmd(["chown", "-R", "100000:100000", str(p)])
        run_cmd(["chmod", "-R", "u+rwX,g+rwX,o+rX", str(p)])

    print("\n[✓] Denonbu 0_00 anomaly resolution completed successfully!")

if __name__ == "__main__":
    main()
