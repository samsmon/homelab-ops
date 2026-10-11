import os

base = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~"

print(f"=== SCANNING FOR ZERO-AUDIO LEAF FOLDERS IN SHINY COLORS ===")
for root, dirs, files in os.walk(base):
    # Only check if this is an album folder (contains no subdirectories or only 'BK' / 'Scans')
    subdirs = [d for d in dirs if d.lower() not in ('bk', 'scans', 'scan', 'booklet')]
    if not subdirs:
        audio = [f for f in files if f.endswith(('.flac', '.wav', '.wv', '.m4a', '.aif', '.aiff', '.ape', '.mp3'))]
        if len(audio) == 0:
            rel = os.path.relpath(root, base)
            print(f"Leaf with 0 audio: {rel}")
            print(f"  Files: {files}")
