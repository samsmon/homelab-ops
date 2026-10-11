import os
import subprocess

ROOT_LOSSLESS = "/mnt/hdd-backup/music/Lossless"
ROOT_LOSSY = "/mnt/hdd-backup/music/Lossy"

print("=" * 60)
print("DEEP AUDIT ROUND 153: COMPREHENSIVE INTEGRITY CHECK")
print("=" * 60)

# 1. Disk usage
r = subprocess.run(["df", "-h", "/mnt/hdd-backup"], capture_output=True, text=True)
print("Disk Usage:")
print(r.stdout.strip())

# 2. Empty directories
empty_dirs = []
for base in [ROOT_LOSSLESS, ROOT_LOSSY]:
    for root, dirs, files in os.walk(base, topdown=False):
        if not dirs and not files:
            empty_dirs.append(root)

print(f"\n1. Empty Directories: {len(empty_dirs)}")
for d in empty_dirs[:10]:
    print(f"   - {d}")

# 3. Broken symlinks or non-regular files
non_regular = []
for base in [ROOT_LOSSLESS, ROOT_LOSSY]:
    for root, dirs, files in os.walk(base):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.islink(fp) and not os.path.exists(fp):
                non_regular.append(('broken_link', fp))
            elif not os.path.isfile(fp):
                non_regular.append(('non_regular', fp))

print(f"\n2. Broken symlinks / non-regular files: {len(non_regular)}")
for t, fp in non_regular[:10]:
    print(f"   - [{t}] {fp}")

# 4. Filename anomalies (double dots, leading spaces, double extension)
filename_anomalies = []
for base in [ROOT_LOSSLESS, ROOT_LOSSY]:
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.startswith(' ') or f.endswith(' '):
                filename_anomalies.append(('whitespace', os.path.join(root, f)))
            if f.count('.flac') > 1 or f.count('.mp3') > 1:
                filename_anomalies.append(('double_ext', os.path.join(root, f)))
            if '..' in f:
                filename_anomalies.append(('double_dot', os.path.join(root, f)))

print(f"\n3. Filename anomalies: {len(filename_anomalies)}")
for t, fp in filename_anomalies[:10]:
    print(f"   - [{t}] {fp}")

# 5. Duplicate Cover Art (e.g. cover.png AND cover.jpg in same folder)
duplicate_covers = []
for base in [ROOT_LOSSLESS]:
    for root, dirs, files in os.walk(base):
        images = [f.lower() for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        has_jpg = any('cover.jpg' in i for i in images)
        has_png = any('cover.png' in i for i in images)
        if has_jpg and has_png:
            duplicate_covers.append(root)

print(f"\n4. Folders with both cover.jpg and cover.png: {len(duplicate_covers)}")
for d in duplicate_covers[:10]:
    rel = os.path.relpath(d, ROOT_LOSSLESS)
    print(f"   - {rel}")

# 6. Sample tag audit on random FLACs across categories
print("\n5. Checking FLAC metadata tags integrity across categories:")
missing_tags = []
checked = 0
for root, dirs, files in os.walk(ROOT_LOSSLESS):
    flacs = [f for f in files if f.lower().endswith('.flac')]
    if flacs:
        # Check first track in each album
        sample_flac = os.path.join(root, flacs[0])
        checked += 1
        res = subprocess.run(["metaflac", "--show-tag=TITLE", sample_flac], capture_output=True, text=True)
        if not res.stdout.strip():
            missing_tags.append(sample_flac)

print(f"   Checked sample track across {checked} album folders.")
print(f"   Sample tracks missing TITLE tag: {len(missing_tags)}")
for m in missing_tags[:10]:
    print(f"     - {m}")

# 7. Check total tracks and file formats in Lossless
formats = {}
for root, dirs, files in os.walk(ROOT_LOSSLESS):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        formats[ext] = formats.get(ext, 0) + 1

print("\n6. File extensions breakdown in Lossless:")
for ext, count in sorted(formats.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"   {ext}: {count}")
