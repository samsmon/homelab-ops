#!/usr/bin/env python3
import os

p = "/mnt/hdd-backup/music/Lossless/J-Pop/tuki. ~/TrySail トライセイル (麻倉もも・雨宮天・夏川椎菜) (2015-2023)"
if os.path.exists(p):
    for root, dirs, files in os.walk(p):
        rel = os.path.relpath(root, p)
        audio = [f for f in files if f.endswith(('.flac', '.mp3'))]
        if audio:
            print(f"Dir: {rel} ({len(audio)} audio files)")
