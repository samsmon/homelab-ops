import os

ROOT = "/mnt/hdd-backup/music/Lossless/Game/O.N.G.E.K.I. (オンゲキ) ~"

p1 = os.path.join(ROOT, "ONGEKI 6th Anniversary CD「Individual on parade!」")
p2 = os.path.join(ROOT, "ONGEKI Collection", "2024.07.26 [ZMCZ-17641] ONGEKI 6th Anniversary CD 「Individual on parade!」")

print("=== P1 items ===")
for f in sorted(os.listdir(p1)):
    fp = os.path.join(p1, f)
    print(f"  {f} ({os.path.getsize(fp) if os.path.isfile(fp) else 'DIR'})")

print("\n=== P2 items ===")
for f in sorted(os.listdir(p2)):
    fp = os.path.join(p2, f)
    print(f"  {f} ({os.path.getsize(fp) if os.path.isfile(fp) else 'DIR'})")
