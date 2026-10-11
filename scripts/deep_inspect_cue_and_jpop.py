#!/usr/bin/env python3
import os
import re

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=" * 80)
print("INSPECTING CUE SHEETS, WAV FILES, J-POP AND LOSSY")
print("=" * 80)

# 1. Inspect CUE files
print("\n[INSPECTING ALL 24 CUE FILES]")
unsplit_cues = []
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.lower().endswith('.cue'):
            cue_path = os.path.join(root, f)
            # check sibling files in the same folder
            siblings = os.listdir(root)
            flacs = [s for s in siblings if s.lower().endswith('.flac')]
            wavs = [s for s in siblings if s.lower().endswith('.wav')]
            rel = os.path.relpath(cue_path, BASE_DIR)
            print(f"CUE: {rel} | FLACs={len(flacs)}, WAVs={len(wavs)}")
            if len(flacs) == 1 and len(wavs) == 0:
                unsplit_cues.append((cue_path, flacs[0]))

print(f"Total potential unsplit single-image CUEs: {len(unsplit_cues)}")
for c, img in unsplit_cues:
    print(f"  Unsplit image: {c} -> {img}")

# 2. Inspect WAV files
print("\n[INSPECTING ALL WAV FILES]")
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.lower().endswith('.wav'):
            wav_path = os.path.join(root, f)
            rel = os.path.relpath(wav_path, BASE_DIR)
            # check if a flac with similar name exists
            flac_counterpart = f[:-4] + ".flac"
            has_flac = flac_counterpart in files
            if has_flac:
                print(f"  Redundant WAV (FLAC exists): {rel}")
            else:
                pass # standalone WAV

# 3. Inspect J-Pop for any deformed / kakasi glitch / multiple parentheses
print("\n[INSPECTING J-POP ARTIST NAMES]")
jpop_dir = os.path.join(BASE_DIR, "J-Pop")
deformed_jpop = []
if os.path.exists(jpop_dir):
    for artist in sorted(os.listdir(jpop_dir)):
        # check for multiple parentheses: e.g. (A) (B) (C)
        parens = re.findall(r'\(.*?\)', artist)
        if len(parens) > 2:
            print(f"  Multiple parens (>2): {artist}")
            deformed_jpop.append(artist)
        # check for characters like '?' or '¿' or '__'
        if '?' in artist or '__' in artist or '??' in artist:
            print(f"  Suspicious characters: {artist}")
            deformed_jpop.append(artist)
        # check for trailing space before tilde: e.g. "Name  ~"
        if artist.endswith("  ~"):
            print(f"  Double space before tilde: {artist}")
        # check for lowercase start
        if artist[0].islower():
            # some names are naturally lowercase like eill, aimer, yama, Eve, etc.
            pass

print(f"Total suspicious J-Pop artist folders: {len(deformed_jpop)}")

# 4. Survey Lossy directory
lossy_dir = "/mnt/hdd-backup/music/Lossy"
print("\n[SURVEY OF LOSSY DIRECTORY]")
if os.path.exists(lossy_dir):
    for cat in sorted(os.listdir(lossy_dir)):
        cp = os.path.join(lossy_dir, cat)
        if os.path.isdir(cp):
            items = os.listdir(cp)
            print(f"  Lossy/{cat}: {len(items)} items")
            # check if any tilde
            with_tilde = [i for i in items if i.endswith('~')]
            print(f"      With '~': {len(with_tilde)}, Without '~': {len(items) - len(with_tilde)}")
