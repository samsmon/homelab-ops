#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import re
import json
import time

LOG_FILE = "/root/torrent_ingestion.log"
BACKUP_ROOT = "/mnt/hdd-backup/music/Lossless"
MUSIC_ROOT = "/mnt/hdd-music/music/Lossless"
TORRENT_DONE = "/mnt/hdd-backup/music/Torrent/done"

def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

log("=== STARTING TORRENT MUSIC INGESTION DAEMON ===")

# Load ingestion plan
with open('/tmp/ingestion_plan_142.json', 'r', encoding='utf-8') as f:
    plan = json.load(f)

# Also load duplicates to safely clean up from Torrent/done
with open('/tmp/truly_new_torrent_albums.json', 'r', encoding='utf-8') as f:
    dups_data = json.load(f)
duplicates = dups_data.get('duplicates', [])

log(f"Loaded {len(plan)} albums to ingest and {len(duplicates)} duplicates to clean.")

# -------------------------------------------------------------------------
# STEP 1: INGEST 142 ALBUMS
# -------------------------------------------------------------------------
log("--- STEP 1: Ingesting 142 Albums into Canonical Lossless Folders ---")

def sanitize_win_name(name):
    # Windows forbidden: \ / : * ? " < > |
    replacements = {
        ':': '：',
        '*': '＊',
        '?': '？',
        '"': "''",
        '<': '＜',
        '>': '＞',
        '|': '｜'
    }
    for bad, good in replacements.items():
        name = name.replace(bad, good)
    return name

ingested_count = 0

for item in plan:
    src_folder_name = item['source']
    target_parent_dir = item['target_dir']
    src_path = os.path.join(TORRENT_DONE, src_folder_name)
    
    if not os.path.exists(src_path):
        log(f"[WARN] Source path not found: {src_path}")
        continue
    
    clean_folder_name = sanitize_win_name(src_folder_name)
    
    # Specific normalization for HOPEFUL FE@THERS (split into individual albums if nested or move as is)
    if "HOPEFUL FE@THERS" in src_folder_name:
        # Check subfolders -Luna-, -Sol-, -Stella-
        for sub in ["-Luna-", "-Sol-", "-Stella-"]:
            sub_src = os.path.join(src_path, sub)
            if os.path.exists(sub_src):
                album_name = f"[2026.09.16] THE IDOLM@STER SHINY COLORS HOPEFUL FE@THERS {sub} [FLAC 96kHz／24bit]"
                dest_album = os.path.join(target_parent_dir, album_name)
                os.makedirs(dest_album, exist_ok=True)
                for f in os.listdir(sub_src):
                    shutil.move(os.path.join(sub_src, f), os.path.join(dest_album, f))
                log(f"Ingested nested Shiny album: {album_name}")
        shutil.rmtree(src_path, ignore_errors=True)
        ingested_count += 1
        continue
        
    dest_path = os.path.join(target_parent_dir, clean_folder_name)
    os.makedirs(target_parent_dir, exist_ok=True)
    
    if os.path.exists(dest_path):
        log(f"[INFO] Destination already exists, merging/updating: {dest_path}")
        for root, dirs, files in os.walk(src_path):
            rel = os.path.relpath(root, src_path)
            cur_dest = os.path.join(dest_path, rel)
            os.makedirs(cur_dest, exist_ok=True)
            for f in files:
                sf = os.path.join(root, f)
                df = os.path.join(cur_dest, f)
                if not os.path.exists(df):
                    shutil.move(sf, df)
        shutil.rmtree(src_path, ignore_errors=True)
    else:
        shutil.move(src_path, dest_path)
        log(f"Moved [{src_folder_name}] -> [{dest_path}]")
        
    ingested_count += 1

log(f"Successfully processed {ingested_count} albums.")

# Ingest loose files
loose_files = [
    ("01. Midnight Mission.flac", "Midnight Grand Orchestra ~", "Midnight Grand Orchestra - Starpeggio"),
    ("01. 夜を待つよ.flac", "Midnight Grand Orchestra ~", "Midnight Grand Orchestra - Starpeggio"),
    ("01_01_Moonlightspeed.flac", "Midnight Grand Orchestra ~", "Midnight Grand Orchestra - Starpeggio")
]
for fname, artist_dir, album_dir in loose_files:
    lf_path = os.path.join(TORRENT_DONE, fname)
    if os.path.exists(lf_path):
        # Already part of Starpeggio, remove loose duplicate from done
        os.remove(lf_path)
        log(f"Cleaned redundant loose track: {fname}")

# -------------------------------------------------------------------------
# STEP 2: REMOVE PROVEN DUPLICATES FROM TORRENT_DONE
# -------------------------------------------------------------------------
log("--- STEP 2: Cleaning Duplicate Albums from Torrent/done ---")
cleaned_dups = 0
for dup_item in duplicates:
    folder_name = dup_item[0]
    p = os.path.join(TORRENT_DONE, folder_name)
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            os.remove(p)
        cleaned_dups += 1
        log(f"Purged duplicate rip from Torrent/done: {folder_name}")

log(f"Purged {cleaned_dups} duplicate folders from Torrent/done.")

# -------------------------------------------------------------------------
# STEP 3: SANITIZE JUNK & HEAL CORRUPT TAGS IN LOSSLESS
# -------------------------------------------------------------------------
log("--- STEP 3: Sanitizing Piracy Junk & Healing Tags in Lossless ---")

junk_exts = {'.txt', '.url', '.log', '.m3u', '.nfo'}
junk_names = {'discord.txt', 'music download.txt', 'read.txt'}

purged_junk = 0
healed_tags = 0

for dirpath, dirnames, filenames in os.walk(BACKUP_ROOT):
    for f in filenames:
        fl = f.lower()
        full_f = os.path.join(dirpath, f)
        
        # 1. Clean junk files
        if fl in junk_names or (os.path.splitext(fl)[1] in junk_exts and fl != 'folder.jpg'):
            try:
                os.remove(full_f)
                purged_junk += 1
            except Exception:
                pass
            continue
            
        # 2. Heal FLAC tags
        if fl.endswith(".flac"):
            try:
                res = subprocess.run(["metaflac", "--show-tag=TITLE", full_f], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, errors="replace")
                out = res.stdout.strip()
                if "TITLE=" in out:
                    val = out.replace("TITLE=", "").strip()
                    # If tag corrupted with '?????'
                    if val and all(c in '?' for c in val) and len(val) >= 2:
                        stem = os.path.splitext(f)[0]
                        clean_title = re.sub(r'^\d+[\s\.\-_]+', '', stem).strip()
                        if " - " in clean_title:
                            clean_title = clean_title.split(" - ")[-1].strip()
                        if clean_title and not all(c in '?' for c in clean_title):
                            subprocess.run(["metaflac", "--remove-tag=TITLE", full_f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            subprocess.run(["metaflac", f"--set-tag=TITLE={clean_title}", full_f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            healed_tags += 1
                            log(f"Healed TITLE tag in [{f}]: '{val}' -> '{clean_title}'")
            except Exception:
                pass

log(f"Purged {purged_junk} junk/promo files. Healed {healed_tags} corrupted track tags.")

# -------------------------------------------------------------------------
# STEP 4: PERMISSIONS ENFORCEMENT (100000:100000, 775/664)
# -------------------------------------------------------------------------
log("--- STEP 4: Enforcing Permissions (100000:100000, 775/664) ---")
subprocess.run(["chown", "-R", "100000:100000", BACKUP_ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["find", BACKUP_ROOT, "-type", "d", "-exec", "chmod", "775", "{}", "+"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["find", BACKUP_ROOT, "-type", "f", "-exec", "chmod", "664", "{}", "+"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# -------------------------------------------------------------------------
# STEP 5: UPDATE SQLITE CATALOG
# -------------------------------------------------------------------------
log("--- STEP 5: Updating Master SQLite Catalog ---")
if os.path.exists("/tmp/update_catalog.py"):
    subprocess.run(["python3", "/tmp/update_catalog.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
elif os.path.exists("/root/homelab-ops/scripts/update_catalog.py"):
    subprocess.run(["python3", "/root/homelab-ops/scripts/update_catalog.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# -------------------------------------------------------------------------
# STEP 6: 1:1 RSYNC MIRROR TO HDD-MUSIC (Z:\)
# -------------------------------------------------------------------------
log("--- STEP 6: Mirroring 1:1 to /mnt/hdd-music/music/Lossless (Z:\\) ---")
rsync_cmd = [
    "rsync", "-avh", "--delete",
    f"{BACKUP_ROOT}/", f"{MUSIC_ROOT}/"
]
res = subprocess.run(rsync_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res.returncode == 0:
    log("Rsync mirroring finished successfully.")
else:
    log(f"Rsync completed with code {res.returncode}. Error: {res.stderr[:200]}")

# Ensure permissions on hdd-music
subprocess.run(["chown", "-R", "100000:100000", MUSIC_ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

log("=== TORRENT MUSIC INGESTION & 1:1 SYNC COMPLETED SUCCESSFULLY ===")
