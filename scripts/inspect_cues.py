#!/usr/bin/env python3
import os

p = "/mnt/hdd-backup/music/Lossless/Anime/Love Live! (ラブライブ！) ~/Liella! (ラブライブ！スーパースター!!) ~/Liella!/SPCD 02 ｢HAPPY TO DO WA!｣/BEPB-0035.cue"
if os.path.exists(p):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        print("=== BEPB-0035.cue ===")
        print(f.read())

p2 = "/mnt/hdd-backup/music/Lossless/Anime/Love Live! (ラブライブ！) ~/Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~/Original Song CD 04 ｢Look at me now｣/BCXA-1752.cue"
if os.path.exists(p2):
    with open(p2, 'r', encoding='utf-8', errors='ignore') as f:
        print("=== BCXA-1752.cue ===")
        print(f.read())
