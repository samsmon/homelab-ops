#!/usr/bin/env python3
import os
import mutagen

album_dir = '/mnt/hdd-backup/music/Lossless/J-Pop/Koi Tarou Famiri (恋太郎ファミリー) ~/君のことが大大大大大好きな100人の彼女 3rd Season'

for fname in sorted(os.listdir(album_dir)):
    if fname.endswith('.flac'):
        p = os.path.join(album_dir, fname)
        f = mutagen.File(p)
        print(f"=== {fname} ===")
        print("  artist:", f.get('artist'))
        print("  albumartist:", f.get('albumartist'))
        print("  album:", f.get('album'))
        print("  title:", f.get('title'))
