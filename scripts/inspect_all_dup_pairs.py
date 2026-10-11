import os
import re

ROOT = "/mnt/hdd-backup/music/Lossless"

potential_dups = []

for root, dirs, files in os.walk(ROOT):
    if dirs:
        norm_map = {}
        for d in dirs:
            n = d.lower()
            n = re.sub(r'\[.*?\]|\(.*?\)', '', n).strip()
            n = re.sub(r'[^\w\s]', '', n)
            n = re.sub(r'\s+', ' ', n).strip()
            if n:
                if n in norm_map:
                    p1 = os.path.join(root, norm_map[n])
                    p2 = os.path.join(root, d)
                    potential_dups.append((norm_map[n], d, root))
                else:
                    norm_map[n] = d

print(f"Total potential duplicate pairs: {len(potential_dups)}")
for d1, d2, parent in potential_dups:
    p1 = os.path.join(parent, d1)
    p2 = os.path.join(parent, d2)
    files1 = set(os.listdir(p1)) if os.path.isdir(p1) else set()
    files2 = set(os.listdir(p2)) if os.path.isdir(p2) else set()
    audio1 = {f for f in files1 if f.endswith(('.flac', '.wav', '.m4a', '.mp3'))}
    audio2 = {f for f in files2 if f.endswith(('.flac', '.wav', '.m4a', '.mp3'))}
    
    # Check if they share audio file names or if one is exact duplicate
    overlap = audio1.intersection(audio2)
    rel_parent = os.path.relpath(parent, ROOT)
    print(f"[{rel_parent}]")
    print(f"  1: {d1} ({len(audio1)} audio)")
    print(f"  2: {d2} ({len(audio2)} audio)")
    print(f"  Audio overlap: {len(overlap)} / {max(len(audio1), len(audio2), 1)}")
    if overlap or d1 == d2:
        print(f"  >>> LIKELY DUPLICATE! <<<")
