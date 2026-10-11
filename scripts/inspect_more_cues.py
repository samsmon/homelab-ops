#!/usr/bin/env python3
import os

for p in [
    "/mnt/hdd-backup/music/Lossless/Vtuber/Azuma Seren (東雪蓮) ~/KEEP OUT {AZSE-0009}/KEEP OUT.cue",
    "/mnt/hdd-backup/music/Lossless/J-Pop/TUYU (ツユ) ~/「アンダーキッズ」ピアノアレンジCD/DSP-02365.cue",
    "/mnt/hdd-backup/music/Lossless/Doujinshi/Shinra-bansho (森羅万象) ~/toge/toge.cue",
    "/mnt/hdd-backup/music/Lossless/Doujinshi/Mamyukka ~/サハラムシカ/サハラムシカ.cue"
]:
    if os.path.exists(p):
        print(f"\n=== {os.path.basename(p)} ===")
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            print(f.read()[:500])
