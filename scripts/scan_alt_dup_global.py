import os

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=== CHECKING FOR ANY _ALT OR _DUP FILES IN ENTIRE LIBRARY ===")
found = []
for r, d, f in os.walk(ROOT):
    for file in f:
        if "_alt" in file.lower() or "_dup" in file.lower() or "copy" in file.lower():
            found.append(os.path.join(r, file))

print(f"Total matching files: {len(found)}")
for fp in found:
    rel = os.path.relpath(fp, ROOT)
    print(f"  {rel}")
