import os

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=== ALL CUE FILES ===")
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith('.cue'):
            fp = os.path.join(root, f)
            parent = os.path.dirname(fp)
            flacs = [x for x in os.listdir(parent) if x.lower().endswith('.flac')]
            print(f"CUE: {fp}")
            print(f"  Flacs in dir ({len(flacs)}): {flacs[:5]}")

print("\n=== SHIRAKAMI FUBUKI DUPLICATE CHECK ===")
fubuki_dir = "/mnt/hdd-backup/music/Lossless/Vtuber/Hololive (ホロライブ) ~/Shirakami Fubuki (白上フブキ) ~"
if os.path.exists(fubuki_dir):
    for d in os.listdir(fubuki_dir):
        if "ヤマトファンタジア" in d:
            dp = os.path.join(fubuki_dir, d)
            print(f"Dir: {d}")
            print(f"  Contents: {os.listdir(dp)}")
