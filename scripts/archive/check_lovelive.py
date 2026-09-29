import os

base = "/mnt/hdd-backup/music/Lossless/Anime/Love Live! (ラブライブ！) ~"

print(f"=== CHECKING LOVE LIVE FRANCHISE ===")
for r, d, f in os.walk(base):
    rel = os.path.relpath(r, base)
    audio = [x for x in f if x.endswith(('.flac', '.wav', '.wv', '.m4a'))]
    if not d and not audio:
        print(f"  [EMPTY LEAF] {rel} (files: {f})")
    for x in f:
        if "_alt" in x.lower() or "_dup" in x.lower():
            print(f"  [ALT/DUP] {os.path.join(rel, x)}")
    for x in d:
        if any(t in x.lower() for t in ['cd-flac', 'web-flac', 'hi-res', '32bit', '24bit']):
            print(f"  [FORMAT TAG] {os.path.join(rel, x)}")
