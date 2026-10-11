#!/usr/bin/env python3
import os
import mutagen

album_dir = '/mnt/hdd-backup/music/Lossless/Anime/100 Kanojo (君のことが大大大大大好きな100人の彼女) ~/TVアニメ「君のことが大大大大大好きな100人の彼女 2nd Season」OP&EDテーマ「ありがと、大好きになってくれて／Unmei？」'

for fname in sorted(os.listdir(album_dir)):
    if fname.endswith('.flac'):
        p = os.path.join(album_dir, fname)
        f = mutagen.File(p)
        print(f"=== {fname} ===")
        print("  artist:", f.get('artist'))
        print("  albumartist:", f.get('albumartist'))
        print("  album:", f.get('album'))
        print("  title:", f.get('title'))
