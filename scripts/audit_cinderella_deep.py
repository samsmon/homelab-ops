import os
import sys
import glob
import subprocess
import json
from collections import defaultdict

# 1. Locate Target Folder
candidates = glob.glob("/mnt/hdd-backup/music/Lossless/Anime/*IDOLM*/*Cinderella*")
if not candidates:
    print("ERROR: Cinderella Girls directory not found!")
    sys.exit(1)

TARGET = candidates[0]
print("=" * 80)
print(f"AUDITING TARGET: {TARGET}")
print("=" * 80)

# 2. Check siblings in THE IDOLM@STER to understand standard naming conventions
parent_dir = os.path.dirname(TARGET)
siblings = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]
print("\n--- Siblings in THE IDOLM@STER ---")
for s in sorted(siblings):
    print(f"  • {s}")

# Check Gakuen or Million Live structure to see how subseries are organized
sample_subseries = []
for s in ["Gakuen Idolmaster (学園アイドルマスター) ~", "Million Live! (ミリオンライブ！) ~", "Shiny Colors (シャイニーカラーズ) ~"]:
    sp = os.path.join(parent_dir, s)
    if os.path.exists(sp):
        sub_dirs = [d for d in os.listdir(sp) if os.path.isdir(os.path.join(sp, d))]
        sample_subseries.append((s, sub_dirs[:5]))

print("\n--- Structural Convention Examples in Other Branches ---")
for name, examples in sample_subseries:
    print(f"[{name}] sample folders:")
    for ex in examples:
        print(f"   - {ex}")

# 3. Scan Cinderella Girls
top_entries = sorted(os.listdir(TARGET))
top_dirs = [d for d in top_entries if os.path.isdir(os.path.join(TARGET, d))]
top_files = [f for f in top_entries if not os.path.isdir(os.path.join(TARGET, f))]

print("\n" + "=" * 80)
print(f"TOP-LEVEL OVERVIEW: {len(top_dirs)} directories, {len(top_files)} loose files")
print("=" * 80)

if top_files:
    print("\n[!] Loose files in root:")
    for f in top_files:
        print(f"   {f}")

# Group top directories to identify patterns (e.g. CINDERELLA MASTER, STARLIGHT MASTER, etc.)
patterns = defaultdict(list)
for d in top_dirs:
    # Extract prefix / series if brackets or keywords exist
    parts = d.split(" - ")
    prefix = parts[0] if len(parts) > 1 else "NO_DASH_PREFIX"
    patterns[prefix].append(d)

print(f"\nTop Directory Patterns ({len(patterns)} pattern groups):")
for prefix, dirs in sorted(patterns.items(), key=lambda x: -len(x[1])):
    print(f"  • [{prefix}]: {len(dirs)} folders (e.g. '{dirs[0]}')")

# Check nested directories depth
deep_nested = []
empty_dirs = []
cue_issues = []
non_flac_audio = []
all_flac_files = []
corrupt_audio = []

print("\nScanning deep structure & audio files...")
for root, dirs, files in os.walk(TARGET):
    if not dirs and not files:
        empty_dirs.append(root)
    
    rel = os.path.relpath(root, TARGET)
    depth = len(rel.split(os.sep)) if rel != "." else 0
    if depth > 3:
        deep_nested.append(rel)
    
    for f in files:
        fp = os.path.join(root, f)
        ext = os.path.splitext(f)[1].lower()
        if ext == ".flac":
            all_flac_files.append(fp)
        elif ext in [".wav", ".m4a", ".mp3", ".aac", ".ogg", ".opus", ".ape", ".wv", ".tak"]:
            non_flac_audio.append((ext, os.path.relpath(fp, TARGET)))
        elif ext == ".cue":
            # check cue reference
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as cue_f:
                    cue_content = cue_f.read()
                    # check if referenced audio exists
                    for line in cue_content.splitlines():
                        if "FILE" in line:
                            cue_issues.append((os.path.relpath(fp, TARGET), line.strip()))
            except Exception as e:
                cue_issues.append((os.path.relpath(fp, TARGET), f"Read error: {e}"))

print(f"\nTotal FLAC files found: {len(all_flac_files)}")
print(f"Total Non-FLAC audio found: {len(non_flac_audio)}")
if non_flac_audio:
    print("Non-FLAC audio breakdown:")
    non_flac_types = defaultdict(int)
    for ext, path in non_flac_audio:
        non_flac_types[ext] += 1
    for ext, count in non_flac_types.items():
        print(f"  • {ext}: {count} files")
    print("Sample non-flac files:")
    for ext, path in non_flac_audio[:5]:
        print(f"  [{ext}] {path}")

if empty_dirs:
    print(f"\n[!] Empty directories: {len(empty_dirs)}")
    for ed in empty_dirs[:5]:
        print(f"   {os.path.relpath(ed, TARGET)}")

# 4. Audio Integrity Audit using flac -t (sample 100 or batch flac test)
print("\n" + "=" * 80)
print("AUDITING FLAC INTEGRITY (Checking all FLACs with `flac -t -s`)...")
print("=" * 80)

# We can test FLACs efficiently
corrupt_flacs = []
print(f"Testing {len(all_flac_files)} FLAC files for integrity...")

# Batch test in chunks of 50 to avoid max arg limit
chunk_size = 50
for i in range(0, len(all_flac_files), chunk_size):
    chunk = all_flac_files[i:i + chunk_size]
    # run flac -t
    proc = subprocess.run(["flac", "-t", "-s"] + chunk, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if proc.returncode != 0:
        # One or more in chunk failed, test individually
        for single in chunk:
            p_single = subprocess.run(["flac", "-t", "-s", single], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if p_single.returncode != 0:
                corrupt_flacs.append((os.path.relpath(single, TARGET), p_single.stderr.decode("utf-8", errors="ignore").strip()))

print(f"\n[INTEGRITY RESULT] Corrupt or unreadable FLACs: {len(corrupt_flacs)}")
if corrupt_flacs:
    for path, err in corrupt_flacs[:10]:
        print(f"  [CORRUPT] {path} -> {err}")
else:
    print("  ✓ All FLAC files passed integrity check (0 errors)!")

# 5. Metadata Tag Inspection (SAMPLE OF ALBUMS)
print("\n" + "=" * 80)
print("METADATA TAG & COVER AUDIT (Sample analysis)")
print("=" * 80)

missing_tags = []
missing_covers = []
flac_sample = all_flac_files[::max(1, len(all_flac_files) // 100)] # 100 sample files

try:
    from mutagen.flac import FLAC
    for fp in all_flac_files[:200]: # check first 200 tracks
        audio = FLAC(fp)
        rel = os.path.relpath(fp, TARGET)
        album = audio.get("album", [""])[0]
        artist = audio.get("artist", [""])[0]
        title = audio.get("title", [""])[0]
        track = audio.get("tracknumber", [""])[0]
        has_art = len(audio.pictures) > 0
        
        if not album or not title:
            missing_tags.append((rel, f"album={album}, title={title}"))
        if not has_art:
            # check if folder has cover.jpg or folder.jpg
            folder = os.path.dirname(fp)
            img_in_folder = [f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in [".jpg", ".jpeg", ".png"]]
            if not img_in_folder:
                missing_covers.append(rel)

    print(f"Checked 200 sample files:")
    print(f" - Missing essential tags (Title/Album): {len(missing_tags)}")
    print(f" - Tracks with neither embedded art nor folder image: {len(missing_covers)}")
    if missing_tags:
        for t in missing_tags[:5]:
            print(f"   [TAG] {t[0]}: {t[1]}")
    if missing_covers:
        for c in missing_covers[:5]:
            print(f"   [COVER] {c}")
except ImportError:
    print("Mutagen not installed, skipped tag inspection.")

print("\nAudit complete.")
