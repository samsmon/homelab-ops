#!/usr/bin/env python3
import os

p_download = "/mnt/hdd-backup/download"
p_lossless = "/mnt/hdd-backup/music/Lossless"

print("Auditing potential duplicates between /mnt/hdd-backup/download and /mnt/hdd-backup/music/Lossless...")

download_albums = set()
for root, dirs, files in os.walk(p_download):
    if any(f.endswith('.flac') for f in files):
        download_albums.add(os.path.basename(root))

lossless_albums = set()
for root, dirs, files in os.walk(p_lossless):
    if any(f.endswith('.flac') for f in files):
        lossless_albums.add(os.path.basename(root))

print(f"Albums in download: {len(download_albums)}")
print(f"Albums in Lossless: {len(lossless_albums)}")

overlap = download_albums & lossless_albums
print(f"Direct album name overlap: {len(overlap)}")
for o in list(overlap)[:10]:
    print(f"  * {o}")
