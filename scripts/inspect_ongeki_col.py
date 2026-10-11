import os

col = "/mnt/hdd-backup/music/Lossless/Game/O.N.G.E.K.I. (オンゲキ) ~/ONGEKI Collection"

for item in sorted(os.listdir(col)):
    p = os.path.join(col, item)
    print(f"\nItem: {item}")
    for root, dirs, files in os.walk(p):
        rel = os.path.relpath(root, p)
        print(f"  [{rel}] dirs: {dirs}, files ({len(files)}): {files[:5]}")
