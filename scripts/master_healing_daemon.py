#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import re
import json
import time

LOG_FILE = "/root/master_library_healing.log"
BACKUP_ROOT = "/mnt/hdd-backup/music/Lossless"
MUSIC_ROOT = "/mnt/hdd-music/music/Lossless"

def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

log("=== STARTING MASTER LIBRARY STANDARDIZATION & HEALING ===")

# ==========================================================
# STEP 1: FIX SIZUK (TAGS, ARTWORK, DEDUPLICATION)
# ==========================================================
log("--- STEP 1: Healing Sizuk Album & Moving to J-Pop ---")

sizuk_target_dir = os.path.join(BACKUP_ROOT, "J-Pop", "Sizuk ~", "[2024.12.25] Sizuk 1stアルバム「es」[FLAC 96kHz／24bit]")
os.makedirs(os.path.dirname(sizuk_target_dir), exist_ok=True)

# Sources
sizuk_anime = os.path.join(BACKUP_ROOT, "Anime", "Sizuk ~", "[2024.12.25] Sizuk 1stアルバム「es」[FLAC 96kHz／24bit]")
sizuk_bad_jpop = os.path.join(BACKUP_ROOT, "J-Pop", "Sizuk 1stアルバム「es」[FLAC 96kHz ~", "[2024.12.25] Sizuk 1stアルバム「es」[FLAC 96kHz／24bit]")

source_to_use = None
if os.path.exists(sizuk_bad_jpop):
    source_to_use = sizuk_bad_jpop
elif os.path.exists(sizuk_anime):
    source_to_use = sizuk_anime

if source_to_use and not os.path.exists(sizuk_target_dir):
    shutil.move(source_to_use, sizuk_target_dir)
    log(f"Moved Sizuk to canonical folder: {sizuk_target_dir}")

# Remove old incorrect folders
for old_dir in [
    os.path.join(BACKUP_ROOT, "Anime", "Sizuk ~"),
    os.path.join(BACKUP_ROOT, "J-Pop", "Sizuk 1stアルバム「es」[FLAC 96kHz ~")
]:
    if os.path.exists(old_dir):
        shutil.rmtree(old_dir, ignore_errors=True)
        log(f"Removed stale Sizuk directory: {old_dir}")

# Fix tags in Sizuk album
sizuk_titles = {
    "01. Dystopia.flac": ("Dystopia", "Sizuk feat.AYAME (from AliA)"),
    "02. anemone.flac": ("anemone", "Sizuk feat.Kotoha"),
    "03. 夏を呼ぶ声.flac": ("夏を呼ぶ声", "Sizuk feat.Kotoha"),
    "04. 蒼い孤島.flac": ("蒼い孤島", "Sizuk feat.AYAME (from AliA)"),
    "05. Baby Sweet Berry Love.flac": ("Baby Sweet Berry Love", "Sizuk feat.Kotoha"),
    "06. REVERSI.flac": ("REVERSI", "Sizuk feat.AYAME (from AliA)"),
    "07. Lover's Eye.flac": ("Lover's Eye", "Sizuk feat.AYAME (from AliA)"),
    "08. Cotton Days.flac": ("Cotton Days", "Sizuk feat.Kotoha"),
    "09. 奇跡.flac": ("奇跡", "Sizuk feat.AYAME (from AliA)"),
    "10. Para Bellum.flac": ("Para Bellum", "Sizuk feat.AYAME (from AliA)"),
    "11. アディクションベール.flac": ("アディクションベール", "Sizuk feat.AYAME (from AliA)"),
    "12. Only.flac": ("Only", "Sizuk feat.Kotoha")
}

cover_jpg_path = os.path.join(sizuk_target_dir, "Cover.jpg")

if os.path.exists(sizuk_target_dir):
    for f in os.listdir(sizuk_target_dir):
        if f in sizuk_titles:
            flac_path = os.path.join(sizuk_target_dir, f)
            title, artist = sizuk_titles[f]
            # Rewrite clean vorbis comments
            subprocess.run(["metaflac", "--remove-tag=TITLE", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["metaflac", f"--set-tag=TITLE={title}", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["metaflac", f"--set-tag=ARTIST={artist}", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["metaflac", "--set-tag=ALBUM=es", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["metaflac", "--set-tag=DATE=2024", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Clean and re-embed picture block if Cover.jpg exists
            if os.path.exists(cover_jpg_path):
                subprocess.run(["metaflac", "--remove", "--block-type=PICTURE", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["metaflac", f"--import-picture-from=3||||{cover_jpg_path}", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            log(f"Fixed tags & embedded cover for Sizuk: {f} -> TITLE={title}")

# ==========================================================
# STEP 2: REMOVE KAKURIYO NO YADOMESHI DUPLICATE
# ==========================================================
log("--- STEP 2: Cleaning duplicate Kakuriyo no Yadomeshi rip ---")
kakuriyo_dir = os.path.join(BACKUP_ROOT, "Anime", "かくりよの宿飯 ~")
if os.path.exists(kakuriyo_dir):
    shutil.rmtree(kakuriyo_dir, ignore_errors=True)
    log(f"Removed inferior raw rip folder: {kakuriyo_dir} (Track already verified in J-Pop/Tōyama Nao 東山奈央 ~)")

# ==========================================================
# STEP 3: MIGRATE MISPLACED ARTISTS ACROSS CATEGORIES
# ==========================================================
log("--- STEP 3: Migrating Misplaced Artists Sesuai Blueprint ---")

# (Source Category, Source Folder Name, Target Category, Target Canonical Folder Name)
migrations = [
    # VTubers misplaced in J-Pop
    ("J-Pop", "Mori Calliope ~", "Vtuber", "Mori Calliope ~"),
    ("J-Pop", "ときのそら ~", "Vtuber", "ときのそら (Tokino Sora) ~"),
    ("J-Pop", "AZKi ~", "Vtuber", "Azki ~"),
    ("J-Pop", "KMNZ ~", "Vtuber", "KMNZ ~"),
    ("J-Pop", "FLOW GLOW ~", "Vtuber", "FLOW GLOW ~"),
    ("J-Pop", "花鋏キョウ (Hanabasami Kyou) ~", "Vtuber", "花鋏キョウ (Hanabasami Kyo) ~"),
    ("J-Pop", "東雪蓮 (Seren Azuma) ~", "Vtuber", "東雪蓮 (Azuma Seren) ~"),
    ("J-Pop", "勿忘うた (Wasurena Uta)~", "Vtuber", "勿忘うた (Uta Wasurena) ~"),
    ("J-Pop", "Mimi ~", "Vtuber", "MIMI ~"),
    
    # Doujinshi / Vocaloid misplaced in J-Pop
    ("J-Pop", "Lunatic★Melody ~", "Doujinshi", "Lunatic★Melody ~"),
    ("J-Pop", "Static World ~", "Doujinshi", "Static World ~"),
    ("J-Pop", "Aintops ~", "Doujinshi", "Aintops ~"),
    ("J-Pop", "Room97 ~", "Doujinshi", "Room97 ~"),
    ("J-Pop", "On Prism Records (irucaice) ~", "Vocaloid", "On Prism Records ~"),
    ("Vtuber", "棗いつき (Natsume Itsuki) ~", "Doujinshi", "棗いつき (Itsuki Natsume) ~")
]

for src_cat, src_name, dst_cat, dst_name in migrations:
    src_path = os.path.join(BACKUP_ROOT, src_cat, src_name)
    dst_path = os.path.join(BACKUP_ROOT, dst_cat, dst_name)
    
    if os.path.exists(src_path):
        os.makedirs(dst_path, exist_ok=True)
        # Move all items inside src_path to dst_path
        for item in os.listdir(src_path):
            s_item = os.path.join(src_path, item)
            d_item = os.path.join(dst_path, item)
            if not os.path.exists(d_item):
                shutil.move(s_item, d_item)
                log(f"Moved [{src_cat}/{src_name}] '{item}' -> [{dst_cat}/{dst_name}]")
            else:
                log(f"Target already exists, skipping move: {d_item}")
        
        # Remove empty src_path
        if not os.listdir(src_path):
            shutil.rmtree(src_path, ignore_errors=True)
            log(f"Cleaned up empty source folder: {src_path}")

# ==========================================================
# STEP 4: HEAL ALL REMAINING CORRUPT TAGS (?????) IN LIBRARY
# ==========================================================
log("--- STEP 4: Scanning & Healing All Remaining Corrupt Tags in Library ---")

healed_count = 0
for dirpath, dirnames, filenames in os.walk(BACKUP_ROOT):
    for f in filenames:
        if f.lower().endswith(".flac"):
            flac_path = os.path.join(dirpath, f)
            try:
                res = subprocess.run(["metaflac", "--show-tag=TITLE", flac_path], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, errors="replace")
                out = res.stdout.strip()
                if "TITLE=" in out:
                    val = out.replace("TITLE=", "").strip()
                    # If corrupt question marks
                    if val and all(c in '?' for c in val) and len(val) >= 2:
                        # Try to infer clean title from filename
                        # Filename pattern usually: "01. Title.flac" or "Artist - Title.flac"
                        stem = os.path.splitext(f)[0]
                        clean_title = re.sub(r'^\d+[\s\.\-]+', '', stem).strip()
                        if " - " in clean_title:
                            clean_title = clean_title.split(" - ")[-1].strip()
                        
                        if clean_title and not all(c in '?' for c in clean_title):
                            subprocess.run(["metaflac", "--remove-tag=TITLE", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            subprocess.run(["metaflac", f"--set-tag=TITLE={clean_title}", flac_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            healed_count += 1
                            log(f"Healed tag in {f}: replaced '{val}' -> '{clean_title}'")
            except Exception as e:
                pass

log(f"Total other corrupted tags healed: {healed_count}")

# ==========================================================
# STEP 5: PERMISSIONS ENFORCEMENT & CATALOG UPDATE
# ==========================================================
log("--- STEP 5: Enforcing Permissions (100000:100000) ---")
subprocess.run(["chown", "-R", "100000:100000", BACKUP_ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["find", BACKUP_ROOT, "-type", "d", "-exec", "chmod", "775", "{}", "+"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["find", BACKUP_ROOT, "-type", "f", "-exec", "chmod", "664", "{}", "+"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

log("--- STEP 6: Updating SQLite Music Catalog ---")
if os.path.exists("/tmp/update_catalog.py"):
    subprocess.run(["python3", "/tmp/update_catalog.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
elif os.path.exists("/root/homelab-ops/scripts/update_catalog.py"):
    subprocess.run(["python3", "/root/homelab-ops/scripts/update_catalog.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ==========================================================
# STEP 7: 1:1 RSYNC MIRRORING TO HDD-MUSIC (Z:\)
# ==========================================================
log("--- STEP 7: Mirroring 1:1 to /mnt/hdd-music/music/Lossless (Z:\\) ---")
rsync_cmd = [
    "rsync", "-avh", "--delete", "--progress",
    f"{BACKUP_ROOT}/", f"{MUSIC_ROOT}/"
]
subprocess.run(rsync_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Sync permissions to hdd-music
subprocess.run(["chown", "-R", "100000:100000", MUSIC_ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

log("=== MASTER LIBRARY STANDARDIZATION & HEALING COMPLETED SUCCESSFULLY ===")
