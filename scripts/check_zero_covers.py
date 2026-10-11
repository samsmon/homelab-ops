import os

ROOT = "/mnt/hdd-backup/music/Lossless"

dup_covers = []
for root, dirs, files in os.walk(ROOT):
    fl = [f.lower() for f in files]
    has_jpg = any('cover.jpg' in i or 'cover.jpeg' in i for i in fl)
    has_png = any('cover.png' in i for i in fl)
    if has_jpg and has_png:
        dup_covers.append(root)

print(f"Remaining folders with both cover.jpg and cover.png: {len(dup_covers)}")
