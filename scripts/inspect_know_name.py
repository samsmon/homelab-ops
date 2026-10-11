#!/usr/bin/env python3
import os

p = "/mnt/hdd-backup/music/Lossless/Anime/(K)NoW_NAME：NIKIIE ~"
if os.path.exists(p):
    for f in os.listdir(p):
        print(f"  {f}")
