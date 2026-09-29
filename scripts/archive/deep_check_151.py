import os
import re
import sys
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=" * 60)
print(f"DEEP LIBRARY AUDIT: {ROOT}")
print("=" * 60)

# Check df
res = subprocess.run(["df", "-h", "/mnt/hdd-backup"], capture_output=True, text=True)
print("DISK USAGE:")
print(res.stdout)

# 1. Non-FLAC audio
non_flac = []
all_audio = 0
audio_exts = {'.flac', '.wav', '.ape', '.wv', '.m4a', '.mp3', '.ogg', '.dsf', '.dff', '.aiff', '.aif', '.wma', '.aac'}
clutter_exts = {'.cue', '.log', '.accurip', '.url', '.ini'}
clutter_files = []
alt_dup_files = []
loose_audio = []
empty_dirs = []

for root, dirs, files in os.walk(ROOT):
    rel = os.path.relpath(root, ROOT)
    parts = rel.split(os.sep) if rel != '.' else []

    if not dirs and not files:
        empty_dirs.append(root)

    # Check loose audio
    if len(parts) == 1:
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in audio_exts:
                loose_audio.append(os.path.join(root, f))
    elif len(parts) == 2:
        # Check if this depth has audio files while having subdirectories
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in audio_exts:
                loose_audio.append(os.path.join(root, f))

    for f in files:
        ext = os.path.splitext(f)[1].lower()
        fp = os.path.join(root, f)
        if ext in audio_exts:
            all_audio += 1
            if ext != '.flac':
                non_flac.append((ext, fp))
        if ext in clutter_exts:
            clutter_files.append((ext, fp))
        if '_alt' in f.lower() or '_dup' in f.lower() or 'cover_dup' in f.lower():
            alt_dup_files.append(fp)

print(f"Total audio tracks: {all_audio}")
print(f"Non-FLAC audio files found: {len(non_flac)}")
by_ext = {}
for ext, fp in non_flac:
    by_ext[ext] = by_ext.get(ext, 0) + 1
for ext, count in sorted(by_ext.items()):
    print(f"  {ext}: {count}")
    sample = [fp for e, fp in non_flac if e == ext][:5]
    for s in sample:
        print(f"    Sample: {s}")

print(f"\nClutter files (.cue, .log, .accurip, etc.): {len(clutter_files)}")
by_clutter = {}
for ext, fp in clutter_files:
    by_clutter[ext] = by_clutter.get(ext, 0) + 1
for ext, count in sorted(by_clutter.items()):
    print(f"  {ext}: {count}")
    sample = [fp for e, fp in clutter_files if e == ext][:5]
    for s in sample:
        print(f"    Sample: {s}")

print(f"\nAlt/Dup files: {len(alt_dup_files)}")
for f in alt_dup_files:
    print(f"  {f}")

print(f"\nLoose audio files: {len(loose_audio)}")
for f in loose_audio[:10]:
    print(f"  {f}")

print(f"\nEmpty directories: {len(empty_dirs)}")
for d in empty_dirs[:10]:
    print(f"  {d}")

# 2. Inspect ONGEKI structure
print("\n" + "=" * 40)
print("ONGEKI & SEGA INSPECTION:")
ongeki_dirs = []
for root, dirs, files in os.walk(os.path.join(ROOT, "Game")):
    for d in dirs:
        if "ongeki" in d.lower() or "オンゲキ" in d:
            ongeki_dirs.append(os.path.join(root, d))
for d in ongeki_dirs:
    print(f"  ONGEKI dir: {d}")
    try:
        sub = os.listdir(d)
        print(f"    Sub-items ({len(sub)}): {sub[:10]}")
    except Exception as e:
        print(f"    Error: {e}")

sega_dir = os.path.join(ROOT, "Game", "SEGA & Arcade Games ~")
if os.path.exists(sega_dir):
    print(f"  SEGA & Arcade Games ~ contents: {os.listdir(sega_dir)}")

# 3. Inspect nayuta & 7uta
print("\n" + "=" * 40)
print("7UTA / NAYUTA INSPECTION:")
uta_dir = os.path.join(ROOT, "J-Pop", "7uta ~")
if os.path.exists(uta_dir):
    print(f"  J-Pop/7uta ~ exists with {len(os.listdir(uta_dir))} albums:")
    for a in sorted(os.listdir(uta_dir)):
        print(f"    - {a}")
else:
    print("  J-Pop/7uta ~ does not exist.")

nayuta_dir = os.path.join(ROOT, "Doujinshi", "nayuta ~")
if os.path.exists(nayuta_dir):
    print(f"  Doujinshi/nayuta ~ exists with {len(os.listdir(nayuta_dir))} albums:")
    for a in sorted(os.listdir(nayuta_dir))[:15]:
        print(f"    - {a}")
    if len(os.listdir(nayuta_dir)) > 15:
        print(f"    ... and {len(os.listdir(nayuta_dir)) - 15} more.")

# 4. Check case collisions
print("\n" + "=" * 40)
print("CASE COLLISION AUDIT:")
case_collisions = 0
for root, dirs, files in os.walk(ROOT):
    seen = {}
    for d in dirs:
        dl = d.lower()
        if dl in seen:
            print(f"  Dir case collision in {root}: '{seen[dl]}' vs '{d}'")
            case_collisions += 1
        else:
            seen[dl] = d
    seen_f = {}
    for f in files:
        fl = f.lower()
        if fl in seen_f:
            print(f"  File case collision in {root}: '{seen_f[fl]}' vs '{f}'")
            case_collisions += 1
        else:
            seen_f[fl] = f

if case_collisions == 0:
    print("  Zero case collisions found.")
