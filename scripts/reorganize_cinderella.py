import os
import sys
import glob
import shutil
from mutagen.flac import FLAC

candidates = glob.glob("/mnt/hdd-backup/music/Lossless/Anime/*IDOLM*/*Cinderella*")
if not candidates:
    print("ERROR: Cinderella Girls directory not found!")
    sys.exit(1)

TARGET = candidates[0]
print("=" * 80)
print(f"STEP 1: FLATTENING NESTED ALBUM DIRECTORIES IN: {TARGET}")
print("=" * 80)

# 1. Identify all album directories
albums = [d for d in sorted(os.listdir(TARGET)) if os.path.isdir(os.path.join(TARGET, d))]
flattened_count = 0
files_moved_total = 0

for alb in albums:
    alb_path = os.path.join(TARGET, alb)
    
    # Check if there are subdirectories inside this album
    subdirs = [d for d in os.listdir(alb_path) if os.path.isdir(os.path.join(alb_path, d))]
    if not subdirs:
        continue
    
    # Find all files recursively inside this album folder
    all_files = []
    for root, dirs, files in os.walk(alb_path):
        if root == alb_path:
            continue
        for f in files:
            all_files.append((os.path.join(root, f), f))
    
    if not all_files:
        continue

    # Move files up to alb_path
    moved_for_this_album = 0
    for src_file, fname in all_files:
        dest_file = os.path.join(alb_path, fname)
        
        # If dest_file already exists and differs, resolve collision
        if os.path.exists(dest_file) and os.path.abspath(src_file) != os.path.abspath(dest_file):
            base, ext = os.path.splitext(fname)
            # if both are covers, check sizes or keep larger
            if ext.lower() in [".jpg", ".png", ".jpeg"]:
                if os.path.getsize(src_file) > os.path.getsize(dest_file):
                    os.remove(dest_file)
                    shutil.move(src_file, dest_file)
                else:
                    os.remove(src_file)
            else:
                # rename with parent dir name
                parent_name = os.path.basename(os.path.dirname(src_file))
                dest_file = os.path.join(alb_path, f"{parent_name}_{fname}")
                shutil.move(src_file, dest_file)
        else:
            if os.path.abspath(src_file) != os.path.abspath(dest_file):
                shutil.move(src_file, dest_file)
        moved_for_this_album += 1
    
    # Remove empty subdirectories
    for d in subdirs:
        sub_p = os.path.join(alb_path, d)
        if os.path.exists(sub_p):
            shutil.rmtree(sub_p, ignore_errors=True)
            
    flattened_count += 1
    files_moved_total += moved_for_this_album

print(f"Flattening complete! Flattened {flattened_count} albums, moved {files_moved_total} files to album roots.")

# Standardize cover art name to cover.jpg if existing Cover.jpg / folder.jpg
print("\n" + "=" * 80)
print("STEP 2: STANDARDIZING COVER ARTWORK & REMOVING ORDER SCREENSHOTS")
print("=" * 80)
cover_fixed = 0
order_deleted = 0
for alb in os.listdir(TARGET):
    alb_path = os.path.join(TARGET, alb)
    if not os.path.isdir(alb_path):
        continue
    for f in os.listdir(alb_path):
        fp = os.path.join(alb_path, f)
        fl = f.lower()
        if "order" in fl and fl.endswith((".png", ".jpg", ".jpeg")):
            try:
                os.remove(fp)
                order_deleted += 1
            except:
                pass
        elif fl in ["cover.jpeg", "folder.jpg", "front.jpg", "cover.png"] and not os.path.exists(os.path.join(alb_path, "cover.jpg")):
            # If cover.jpg doesn't exist, standardize
            shutil.move(fp, os.path.join(alb_path, "cover.jpg"))
            cover_fixed += 1
        elif f == "Cover.jpg":
            shutil.move(fp, os.path.join(alb_path, "cover.jpg"))
            cover_fixed += 1

print(f"Removed {order_deleted} order screenshot clutter files.")
print(f"Standardized {cover_fixed} cover files.")

# Step 3: Organize into franchise sub-series
print("\n" + "=" * 80)
print("STEP 3: CATEGORIZING INTO SUB-SERIES DIRECTORIES")
print("=" * 80)

SUBSERIES_MAP = {
    "01. CINDERELLA MASTER Series ~": lambda u, n: ("CINDERELLA MASTER" in u or "3CHORD" in u or "JEWELRIES" in u or "01 NEVER" in u) and "STARLIGHT MASTER" not in u and "ANIMATION" not in u,
    "02. STARLIGHT MASTER Series ~": lambda u, n: "STARLIGHT MASTER" in u or "CGSM" in u or "SNOW WINGS" in u or "TULIP" in u,
    "03. ANIMATION PROJECT Series ~": lambda u, n: "ANIMATION PROJECT" in u or "ANIMATION" in u or "GOIN" in u or "ST@RTER" in u,
    "04. LITTLE STARS Series ~": lambda u, n: "LITTLE STARS" in u,
    "05. CINDERELLA PARTY & Radio Series ~": lambda u, n: "CINDERELLA PARTY" in u or "でれぱ" in n,
    "06. Singles & Others ~": lambda u, n: True # Fallback
}

# Create subseries folders
for cat in SUBSERIES_MAP.keys():
    os.makedirs(os.path.join(TARGET, cat), exist_ok=True)

classified_counts = {cat: 0 for cat in SUBSERIES_MAP.keys()}

for alb in sorted(os.listdir(TARGET)):
    alb_path = os.path.join(TARGET, alb)
    if not os.path.isdir(alb_path) or alb in SUBSERIES_MAP.keys():
        continue
    
    upper = alb.upper()
    dest_cat = "06. Singles & Others ~"
    for cat, cond in SUBSERIES_MAP.items():
        if cat == "06. Singles & Others ~":
            continue
        if cond(upper, alb):
            dest_cat = cat
            break
            
    dest_path = os.path.join(TARGET, dest_cat, alb)
    shutil.move(alb_path, dest_path)
    classified_counts[dest_cat] += 1

print("Categorization summary:")
for cat, cnt in classified_counts.items():
    print(f"  • {cat}: {cnt} albums moved")

print("\n" + "=" * 80)
print("ALL CLEANUP & REORGANIZATION STEPS SUCCESSFULLY COMPLETED!")
print("=" * 80)
