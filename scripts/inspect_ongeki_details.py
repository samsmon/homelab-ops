import os

ROOT = "/mnt/hdd-backup/music/Lossless"

dir1 = os.path.join(ROOT, "Game", "O.N.G.E.K.I. (オンゲキ) ~")
dir2 = os.path.join(ROOT, "Game", "SEGA & Arcade Games ~", "ONGEKI (オンゲキ) ~")
sega_dir = os.path.join(ROOT, "Game", "SEGA & Arcade Games ~")

print("=== DIR 1: Game/O.N.G.E.K.I. (オンゲキ) ~ ===")
if os.path.exists(dir1):
    for item in sorted(os.listdir(dir1)):
        p = os.path.join(dir1, item)
        if os.path.isdir(p):
            sub = os.listdir(p)
            print(f"  [D] {item} ({len(sub)} items)")
            if item == "ONGEKI Collection":
                for c in sorted(sub):
                    cp = os.path.join(p, c)
                    print(f"      - {c} ({len(os.listdir(cp)) if os.path.isdir(cp) else 'file'})")
        else:
            print(f"  [F] {item}")

print("\n=== DIR 2: Game/SEGA & Arcade Games ~/ONGEKI (オンゲキ) ~ ===")
if os.path.exists(dir2):
    for item in sorted(os.listdir(dir2)):
        p = os.path.join(dir2, item)
        if os.path.isdir(p):
            print(f"  [D] {item} ({len(os.listdir(p))} items)")
        else:
            print(f"  [F] {item}")

print("\n=== SEGA & Arcade Games ~ OTHER ITEMS ===")
if os.path.exists(sega_dir):
    for item in sorted(os.listdir(sega_dir)):
        if item != "ONGEKI (オンゲキ) ~":
            p = os.path.join(sega_dir, item)
            print(f"  [D] {item}: {os.listdir(p) if os.path.isdir(p) else 'file'}")
