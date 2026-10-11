#!/usr/bin/env python3
import os

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=== ALL ITEMS IN Anime/ ===")
anime_dir = os.path.join(BASE_DIR, "Anime")
for item in sorted(os.listdir(anime_dir)):
    p = os.path.join(anime_dir, item)
    if os.path.isdir(p):
        sub = os.listdir(p)
        print(f"  {item} ({len(sub)} items)")

print("\n=== ALL ITEMS IN Game/ ===")
game_dir = os.path.join(BASE_DIR, "Game")
for item in sorted(os.listdir(game_dir)):
    p = os.path.join(game_dir, item)
    if os.path.isdir(p):
        sub = os.listdir(p)
        print(f"  {item} ({len(sub)} items)")
