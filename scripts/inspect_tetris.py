#!/usr/bin/env python3
import os
import subprocess

p = "/mnt/hdd-backup/music/Lossless/Anime/テトリス ~/テトリス/テトリス.flac"
if os.path.exists(p):
    res = subprocess.run(["metaflac", "--list", "--block-type=VORBIS_COMMENT", p], capture_output=True, text=True)
    print(res.stdout)
else:
    print("File not found")
