import os
import re

LOSSLESS = "/mnt/hdd-backup/music/Lossless"
LOSSY = "/mnt/hdd-backup/music/Lossy"

print(f"Checking overlap between Lossless and Lossy...")

# Build a map of normalized album titles in Lossless
lossless_albums = set()
for root, dirs, files in os.walk(LOSSLESS):
    # check if directory contains audio files
    flacs = [f for f in files if f.lower().endswith('.flac')]
    if flacs:
        # get album folder name
        dname = os.path.basename(root)
        if dname.lower() in ['disc 1', 'disc 2', 'disc 3', 'disc 4', 'cd 1', 'cd 2']:
            dname = os.path.basename(os.path.dirname(root))
        norm = re.sub(r'\[.*?\]|\(.*?\)|{.*?}', '', dname).strip().lower()
        norm = re.sub(r'[^\w\s]', '', norm)
        norm = re.sub(r'\s+', ' ', norm).strip()
        if norm:
            lossless_albums.add(norm)

print(f"Total distinct lossless albums: {len(lossless_albums)}")

# Check Lossy albums
lossy_overlap = []
for root, dirs, files in os.walk(LOSSY):
    audio = [f for f in files if os.path.splitext(f)[1].lower() in ['.mp3', '.m4a', '.aac', '.ogg', '.opus']]
    if audio:
        dname = os.path.basename(root)
        if dname.lower() in ['disc 1', 'disc 2', 'disc 3', 'disc 4', 'cd 1', 'cd 2']:
            dname = os.path.basename(os.path.dirname(root))
        norm = re.sub(r'\[.*?\]|\(.*?\)|{.*?}', '', dname).strip().lower()
        norm = re.sub(r'[^\w\s]', '', norm)
        norm = re.sub(r'\s+', ' ', norm).strip()
        if norm and norm in lossless_albums:
            lossy_overlap.append((root, dname, norm, len(audio)))

print(f"\nLossy albums that already exist in Lossless ({len(lossy_overlap)}):")
for r, d, n, count in lossy_overlap[:20]:
    rel = os.path.relpath(r, LOSSY)
    print(f"  {rel} ({count} tracks)")
