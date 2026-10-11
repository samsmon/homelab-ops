import os

ROOT = "/mnt/hdd-backup/music/Lossless"

mp3s = []
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith('.mp3'):
            mp3s.append(os.path.join(root, f))

print(f"Total MP3s: {len(mp3s)}")
for m in sorted(mp3s):
    sz = os.path.getsize(m)
    # Check sibling files
    d = os.path.dirname(m)
    sibs = os.listdir(d)
    flacs = [f for f in sibs if f.lower().endswith('.flac')]
    print(f"\nMP3: {m} ({sz / (1024*1024):.2f} MB)")
    print(f"  Directory: {d}")
    print(f"  FLACs in dir: {flacs}")
