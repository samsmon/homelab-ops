import os

ROOT = "/mnt/hdd-backup/music/Lossless"

for root, dirs, files in os.walk(ROOT):
    fl = [f.lower() for f in files]
    has_jpg = any('cover.jpg' in i or 'cover.jpeg' in i for i in fl)
    has_png = any('cover.png' in i for i in fl)
    if has_jpg and has_png:
        print(f"Folder: {os.path.relpath(root, ROOT)}")
        for f in files:
            if 'cover' in f.lower():
                fp = os.path.join(root, f)
                print(f"   {f} ({os.path.getsize(fp)} bytes)")
