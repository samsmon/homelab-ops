import os
import glob
from mutagen.flac import FLAC

paths = [
    '/mnt/hdd-backup/music/Lossless/Vocaloid/Hachioji P (八王子P) ~/Eight -THE BEST OF 八王子P-',
    '/mnt/hdd-backup/music/Lossless/Vocaloid/PinocchioP ~/HUMAN',
    "/mnt/hdd-backup/music/Lossless/Vocaloid/Osanzi ~/4 O'Clock!",
    "/mnt/hdd-backup/music/Lossless/Vocaloid/Osanzi ~/3.5 O'Clock!"
]

for p in paths:
    print(f"\nDirectory: {p}")
    if os.path.exists(p):
        items = os.listdir(p)
        print("  Items:", items)
        for item in items:
            sub = os.path.join(p, item)
            if os.path.isdir(sub):
                print(f"    Subdir {item}: {os.listdir(sub)[:5]}")
            elif item.lower().endswith(('.jpg', '.png', '.jpeg')):
                print(f"    Image {item}: size {os.path.getsize(sub)} bytes")
    else:
        print("  DOES NOT EXIST")

# Also check Osanzi entire folder
osanzi_root = "/mnt/hdd-backup/music/Lossless/Vocaloid/Osanzi ~"
print(f"\nAll Osanzi albums:")
for alb in sorted(os.listdir(osanzi_root)):
    alb_p = os.path.join(osanzi_root, alb)
    if os.path.isdir(alb_p):
        files = os.listdir(alb_p)
        imgs = [f for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        flacs = [f for f in files if f.endswith('.flac')]
        embedded = 0
        for fl in flacs:
            af = FLAC(os.path.join(alb_p, fl))
            if af.pictures:
                embedded += 1
        print(f"  {alb}: {len(flacs)} FLACs, {embedded} embedded art, images: {imgs}")
