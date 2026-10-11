#!/usr/bin/env python3
import os

p = "/mnt/hdd-backup/music/Lossless/Anime/Girls Band Cry (ガールズバンドクライ) ~"
if os.path.exists(p):
    for item in sorted(os.listdir(p)):
        print(f"  {item}")
else:
    print("Not found")
