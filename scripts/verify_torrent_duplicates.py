import os
import json
import re

LOSSLESS_ROOT = "/mnt/hdd-backup/music/Lossless"
TORRENT_DONE = "/mnt/hdd-backup/music/Torrent/done"

with open('/tmp/torrent_audit_report.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# Find all track filenames and sizes in Lossless
lossless_files = {} # filename -> list of (filesize, fullpath)
for root, dirs, files in os.walk(LOSSLESS_ROOT):
    for f in files:
        if f.lower().endswith(('.flac', '.wav', '.mp3')):
            full = os.path.join(root, f)
            sz = os.path.getsize(full)
            lossless_files.setdefault(f.lower(), []).append((sz, full))

print(f"Indexed {len(lossless_files)} unique audio filenames in Lossless")

truly_new = []
duplicates = []

for album in d['not_in_library']:
    album_path = os.path.join(TORRENT_DONE, album)
    if not os.path.isdir(album_path):
        continue
    
    # check tracks inside
    tracks = []
    for r, ds, fs in os.walk(album_path):
        for f in fs:
            if f.lower().endswith(('.flac', '.wav', '.mp3')):
                tracks.append((f, os.path.getsize(os.path.join(r, f))))
    
    if not tracks:
        continue
    
    # Check how many tracks exist identically in Lossless
    matched_tracks = 0
    match_dest = None
    for fname, sz in tracks:
        if fname.lower() in lossless_files:
            for lsz, lpath in lossless_files[fname.lower()]:
                if abs(lsz - sz) < 100: # identical or tag variation
                    matched_tracks += 1
                    match_dest = os.path.dirname(lpath)
                    break
    
    if matched_tracks == len(tracks) and len(tracks) > 0:
        duplicates.append((album, match_dest))
    else:
        truly_new.append(album)

print(f"Total evaluated from not_in_library: {len(d['not_in_library'])}")
print(f"Trully New: {len(truly_new)}")
print(f"Actually Duplicates (different folder name): {len(duplicates)}")

print("\n--- SAMPLE IDENTIFIED DUPLICATES ---")
for a, dest in duplicates[:15]:
    print(f" [DUP] {a}\n    --> ALREADY AT: {dest}")

with open('/tmp/truly_new_torrent_albums.json', 'w', encoding='utf-8') as f:
    json.dump({"truly_new": truly_new, "duplicates": duplicates}, f, ensure_ascii=False, indent=2)
