#!/usr/bin/env python3
import os

targets = [
    "/mnt/hdd-backup/music/Lossless/J-Pop/YENA ~",
    "/mnt/hdd-backup/music/Lossless/J-Pop/Various Artists ~/Various Artists ~",
    "/mnt/hdd-backup/music/Lossless/Vtuber/KAMITSUBAKI STUDIO (神椿スタジオ) ~/Isekaijoucho (ヰ世界情緒) ~/眠りゆく芽吹き",
    "/mnt/hdd-backup/music/Lossless/Vtuber/Hololive (ホロライブ) ~/Hololive Official ~/Juara Khatulistiwa",
    "/mnt/hdd-backup/music/Lossless/Vtuber/Hololive (ホロライブ) ~/Amane Kanata (天音かなた) ~/中空の庭",
]

for t in targets:
    print(f"\nChecking: {t}")
    if os.path.exists(t):
        for item in sorted(os.listdir(t)):
            print(f"  {item}")
