#!/usr/bin/env python3
import os

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

queries = ['d4dj', 'rondo', '燐舞曲', 'kito', '鬼頭', 'trysail', 'riria', 'りりあ', 'hibana', 'ヒバナ', 'tokyo 7th']

print("=== SEARCHING FOLDERS ===")
for cat in os.listdir(BASE_DIR):
    cat_path = os.path.join(BASE_DIR, cat)
    if not os.path.isdir(cat_path):
        continue
    for item in os.listdir(cat_path):
        for q in queries:
            if q in item.lower():
                print(f"[{cat}] {item}")
                break

print("\n=== SEARCHING FORBIDDEN CHARACTERS IN ALL PATHS ===")
forbidden = [':', '*', '?', '"', '<', '>', '|']
for root, dirs, files in os.walk(BASE_DIR):
    for d in dirs:
        if any(c in d for c in forbidden):
            print(f"DIR:  {os.path.relpath(os.path.join(root, d), BASE_DIR)}")
    for f in files:
        if any(c in f for c in forbidden):
            print(f"FILE: {os.path.relpath(os.path.join(root, f), BASE_DIR)}")
