#!/usr/bin/env python3
import os
import mutagen

album_dir = '/mnt/hdd-backup/music/Lossless/Anime/Tetris (テトリス) ~/テトリス'

for fname in sorted(os.listdir(album_dir)):
    p = os.path.join(album_dir, fname)
    if os.path.isfile(p):
        f = mutagen.File(p)
        print(f"=== {fname} ===")
        if f:
            print("  artist:", f.get('artist'))
            print("  albumartist:", f.get('albumartist'))
            print("  album:", f.get('album'))
            print("  title:", f.get('title'))
