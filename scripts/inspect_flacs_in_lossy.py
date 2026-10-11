import os

ROOT_LOSSY = "/mnt/hdd-backup/music/Lossy"

flacs_in_lossy = []
for root, dirs, files in os.walk(ROOT_LOSSY):
    for f in files:
        if f.lower().endswith('.flac'):
            fp = os.path.join(root, f)
            flacs_in_lossy.append(fp)

print(f"Total FLAC files in Lossy: {len(flacs_in_lossy)}")
for f in flacs_in_lossy:
    rel = os.path.relpath(f, ROOT_LOSSY)
    print(f"  {rel} ({os.path.getsize(f) / (1024*1024):.1f} MB)")
