#!/usr/bin/env python3
import os

gakumas_dir = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~"

print(f"=== CHECKING GAKUMAS: {gakumas_dir} ===")
if not os.path.exists(gakumas_dir):
    print("GAKUMAS NOT FOUND!")
    exit(1)

for root, dirs, files in os.walk(gakumas_dir):
    rel = os.path.relpath(root, gakumas_dir)
    print(f"\nDIR: {rel}")
    dirs.sort()
    files.sort()
    if dirs:
        print(f"  [SUBDIRS]: {dirs}")
    audio = [f for f in files if f.endswith(('.flac', '.mp3', '.wav', '.m4a'))]
    non_audio = [f for f in files if not f.endswith(('.flac', '.mp3', '.wav', '.m4a'))]
    if audio:
        print(f"  [AUDIO] ({len(audio)} tracks): {audio[:3]}...{audio[-1:] if len(audio) > 3 else ''}")
    if non_audio:
        print(f"  [NON-AUDIO] ({len(non_audio)} files): {non_audio[:5]}")
