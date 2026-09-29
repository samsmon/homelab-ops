import os

ROOT = "/mnt/hdd-backup/music/Lossless"

categories = sorted(os.listdir(ROOT))
print("Categories:", categories)

counts = {}
samples = {}

for root, dirs, files in os.walk(ROOT):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.wav', '.aiff', '.aif', '.wv', '.mp3', '.m4a', '.aac', '.ogg', '.cue', '.log', '.accurip']:
            counts[ext] = counts.get(ext, 0) + 1
            if ext not in samples:
                samples[ext] = []
            if len(samples[ext]) < 5:
                samples[ext].append(os.path.join(root, f))

print("\n--- Audio & Clutter File Counts ---")
for ext, c in sorted(counts.items()):
    print(f"{ext}: {c} files")
    for s in samples[ext]:
        print(f"  {s}")

# Check loose audio
print("\n--- Loose Audio in Category or Artist Root ---")
for cat in categories:
    cat_dir = os.path.join(ROOT, cat)
    if not os.path.isdir(cat_dir):
        continue
    # Files directly in category
    cat_files = [f for f in os.listdir(cat_dir) if os.path.isfile(os.path.join(cat_dir, f))]
    if cat_files:
        print(f"Loose files in category root {cat}: {cat_files}")
    
    # Check artist dirs
    for artist in os.listdir(cat_dir):
        art_dir = os.path.join(cat_dir, artist)
        if not os.path.isdir(art_dir):
            continue
        art_files = [f for f in os.listdir(art_dir) if os.path.isfile(os.path.join(art_dir, f))]
        # filter for audio
        audio_files = [f for f in art_files if os.path.splitext(f)[1].lower() in ['.flac', '.wav', '.aiff', '.mp3', '.wv', '.m4a']]
        if audio_files:
            print(f"Loose audio in artist {cat}/{artist}: {len(audio_files)} files (e.g. {audio_files[:3]})")
