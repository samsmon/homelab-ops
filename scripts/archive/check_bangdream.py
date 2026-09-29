import os

base = "/mnt/hdd-backup/music/Lossless/Anime/BanG Dream! (バンドリ！) ~"

print(f"=== CHECKING BANG DREAM FRANCHISE ===")
for r, d, f in os.walk(base):
    rel = os.path.relpath(r, base)
    audio = [x for x in f if x.endswith(('.flac', '.wav', '.wv', '.m4a'))]
    if not d and not audio and not any(k in rel.lower() for k in ['scans', 'bk', 'booklet']):
        print(f"  [EMPTY NON-SCAN LEAF] {rel} (files: {f})")
    for x in f:
        if "_alt" in x.lower() or "_dup" in x.lower():
            print(f"  [ALT/DUP] {os.path.join(rel, x)}")
    for x in d:
        if any(t in x.lower() for t in ['cd-flac', 'web-flac', 'hi-res', '32bit', '24bit']):
            print(f"  [FORMAT TAG] {os.path.join(rel, x)}")
