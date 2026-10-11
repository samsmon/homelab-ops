#!/usr/bin/env python3
import os

p = "/mnt/hdd-backup/music/Lossless/Anime/Tv Anime (TVアニメ) ~"
if os.path.exists(p):
    for item in sorted(os.listdir(p)):
        print(f"  {item}")
