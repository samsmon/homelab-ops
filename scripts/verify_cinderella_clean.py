import os
import sys
import glob
import subprocess
from collections import defaultdict

candidates = glob.glob("/mnt/hdd-backup/music/Lossless/Anime/*IDOLM*/*Cinderella*")
if not candidates:
    print("ERROR: Cinderella Girls directory not found!")
    sys.exit(1)

TARGET = candidates[0]
print("=" * 80)
print(f"RE-VERIFYING POST-REORGANIZATION STATUS: {TARGET}")
print("=" * 80)

# 1. Top level check
top_items = sorted(os.listdir(TARGET))
print(f"\n[1] Top-Level Folders ({len(top_items)} items):")
for item in top_items:
    p = os.path.join(TARGET, item)
    if os.path.isdir(p):
        child_count = len(os.listdir(p))
        print(f"  • {item} -> {child_count} albums")
    else:
        print(f"  • [LOOSE FILE] {item}")

# 2. Deep scan across all sub-series and albums
total_albums = 0
total_flacs = 0
non_flacs = []
empty_folders = []
albums_without_cover = []
nested_dirs = []
cue_files = []
corrupt_flacs = []

flac_paths = []

for cat in top_items:
    cat_path = os.path.join(TARGET, cat)
    if not os.path.isdir(cat_path):
        continue
    
    albums = sorted(os.listdir(cat_path))
    for alb in albums:
        alb_path = os.path.join(cat_path, alb)
        if not os.path.isdir(alb_path):
            continue
        total_albums += 1
        
        # Check files and subdirs in album
        items = os.listdir(alb_path)
        subdirs = [i for i in items if os.path.isdir(os.path.join(alb_path, i))]
        if subdirs:
            nested_dirs.append((os.path.join(cat, alb), subdirs))
        
        files = [i for i in items if not os.path.isdir(os.path.join(alb_path, i))]
        flacs = [f for f in files if f.lower().endswith(".flac")]
        covers = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
        cues = [f for f in files if f.lower().endswith(".cue")]
        
        if not flacs:
            empty_folders.append(os.path.join(cat, alb))
        
        if not covers:
            albums_without_cover.append(os.path.join(cat, alb))
            
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            fp = os.path.join(alb_path, f)
            if ext == ".flac":
                total_flacs += 1
                flac_paths.append(fp)
            elif ext in [".wav", ".m4a", ".mp3", ".aac", ".ogg", ".opus", ".ape", ".wv", ".zip", ".rar", ".7z"]:
                non_flacs.append((os.path.join(cat, alb, f), ext))
            elif ext == ".cue":
                cue_files.append(os.path.join(cat, alb, f))

print(f"\n[2] Structural Integrity:")
print(f"  • Total Albums: {total_albums}")
print(f"  • Total FLAC tracks: {total_flacs}")
print(f"  • Remaining nested subdirectories: {len(nested_dirs)}")
if nested_dirs:
    for nd in nested_dirs:
        print(f"     [!] {nd[0]} contains subdirs: {nd[1]}")

print(f"  • Albums with 0 audio files: {len(empty_folders)}")
if empty_folders:
    for ef in empty_folders:
        print(f"     [!] {ef}")

print(f"  • Albums missing cover art: {len(albums_without_cover)}")
if albums_without_cover:
    for mc in albums_without_cover:
        print(f"     [!] {mc}")

print(f"  • Non-FLAC audio or archive files: {len(non_flacs)}")
if non_flacs:
    for nf in non_flacs:
        print(f"     [!] {nf[0]} ({nf[1]})")

# 3. Flac integrity verification
print(f"\n[3] FLAC Stream Integrity Test (Testing all {len(flac_paths)} files via `flac -t -s`)...")
chunk_size = 50
for i in range(0, len(flac_paths), chunk_size):
    chunk = flac_paths[i:i + chunk_size]
    proc = subprocess.run(["flac", "-t", "-s"] + chunk, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if proc.returncode != 0:
        for single in chunk:
            p_single = subprocess.run(["flac", "-t", "-s", single], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if p_single.returncode != 0:
                corrupt_flacs.append((os.path.relpath(single, TARGET), p_single.stderr.decode("utf-8", errors="ignore").strip()))

print(f"  • Corrupt or unreadable FLAC files: {len(corrupt_flacs)}")
if corrupt_flacs:
    for cf in corrupt_flacs:
        print(f"     [CORRUPT] {cf[0]} -> {cf[1]}")
else:
    print("  ✓ All FLAC files 100% verified healthy.")

# 4. Check tags with mutagen
print(f"\n[4] Metadata Tag Quality Check (Sample 100 tracks across series)...")
try:
    from mutagen.flac import FLAC
    sample_flacs = flac_paths[::max(1, len(flac_paths) // 100)]
    missing_meta = []
    bitrates = defaultdict(int)
    for fp in sample_flacs:
        audio = FLAC(fp)
        title = audio.get("title", [""])[0]
        artist = audio.get("artist", [""])[0]
        album = audio.get("album", [""])[0]
        track = audio.get("tracknumber", [""])[0]
        sr = audio.info.sample_rate
        bps = audio.info.bits_per_sample
        bitrates[f"{bps}bit / {sr}Hz"] += 1
        if not title or not album or not artist:
            missing_meta.append((os.path.relpath(fp, TARGET), f"title={title}, artist={artist}, album={album}"))
            
    print(f"  • Sample tracks checked: {len(sample_flacs)}")
    print(f"  • Missing core tags (Title/Artist/Album): {len(missing_meta)}")
    print("  • Audio specs in library:")
    for spec, count in sorted(bitrates.items(), key=lambda x: -x[1]):
        print(f"     - {spec}: {count} sample tracks")
except ImportError:
    print("  • Mutagen not available.")

print("\n" + "=" * 80)
print("RE-VERIFICATION COMPLETED.")
print("=" * 80)
