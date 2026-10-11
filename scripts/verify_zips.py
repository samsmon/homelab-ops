#!/usr/bin/env python3
import os
import subprocess

folder = "/mnt/hdd-backup/download/Anime/The Idolmaster (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~"

files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".zip")]
print(f"Total zip files to verify: {len(files)}")

corrupt = []
ok_count = 0

for idx, f in enumerate(files):
    # test archive
    res = subprocess.run(["7z", "t", f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print(f"[FAIL] {os.path.basename(f)}")
        corrupt.append(f)
    else:
        ok_count += 1

print(f"\nVerification finished: {ok_count} OK, {len(corrupt)} CORRUPT/FAILED.")
if corrupt:
    print("Files that failed:")
    for c in corrupt:
        print(f" - {c}")
