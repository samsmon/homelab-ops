import os
import re
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=" * 60)
print("STARTING ROUND 153 EXECUTION")
print("=" * 60)

# ==============================================================================
# PHASE 1: Purge HTML spam / bookmarks
# ==============================================================================
print("\n--- PHASE 1: Purge HTML spam bookmarks ---")
html_purged = 0
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith(('.html', '.htm')):
            fp = os.path.join(root, f)
            try:
                os.remove(fp)
                html_purged += 1
                print(f"  Purged HTML ad: {os.path.relpath(fp, ROOT)}")
            except Exception as e:
                print(f"  Failed to delete {fp}: {e}")

print(f"  Total HTML files purged: {html_purged}")


# ==============================================================================
# PHASE 2: Deduplicate cover.png when cover.jpg exists
# ==============================================================================
print("\n--- PHASE 2: Deduplicate cover.png when cover.jpg exists ---")
covers_deduped = 0
for root, dirs, files in os.walk(ROOT):
    fl = [f.lower() for f in files]
    if ('cover.jpg' in fl or 'cover.jpeg' in fl) and 'cover.png' in fl:
        png_file = [f for f in files if f.lower() == 'cover.png'][0]
        png_p = os.path.join(root, png_file)
        try:
            os.remove(png_p)
            covers_deduped += 1
            print(f"  Purged redundant raw PNG cover: {os.path.relpath(png_p, ROOT)}")
        except Exception as e:
            print(f"  Failed to delete {png_p}: {e}")

print(f"  Total duplicate cover.png files purged: {covers_deduped}")


# ==============================================================================
# PHASE 3: Auto-populate missing TITLE tags on FLAC tracks
# ==============================================================================
print("\n--- PHASE 3: Auto-populate missing TITLE tags on FLAC tracks ---")
from concurrent.futures import ThreadPoolExecutor

def extract_title(filename):
    name = os.path.splitext(filename)[0]
    # Check pattern like "prefix_07_Title"
    m_sub = re.search(r'_\d{2}_(.*)$', name)
    if m_sub:
        return m_sub.group(1).strip()
    # Check standard track numbering "01. Title" or "01 - Artist - Title"
    m_num = re.match(r'^\d+[\s\.-]+(?:[^-]+-\s+)?(.*)$', name)
    if m_num:
        return m_num.group(1).strip()
    # Replace underscores if single word words joined by underscores
    if '_' in name and ' ' not in name:
        return name.replace('_', ' ').strip()
    return name.strip()

all_flacs = []
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith('.flac'):
            all_flacs.append(os.path.join(root, f))

print(f"  Scanning {len(all_flacs)} FLAC tracks across library with 8 workers...")

def process_track(fp):
    r = subprocess.run(["metaflac", "--export-tags-to=-", fp], capture_output=True, text=True)
    tags = {line.split('=', 1)[0].upper(): line.split('=', 1)[1] for line in r.stdout.splitlines() if '=' in line}
    if 'TITLE' not in tags or not tags['TITLE'].strip():
        fl = os.path.basename(fp)
        title = extract_title(fl)
        if title:
            cmd = ["metaflac", f"--set-tag=TITLE={title}", fp]
            r_set = subprocess.run(cmd, capture_output=True, text=True)
            if r_set.returncode == 0:
                print(f"  Set TITLE tag '{title}' on {os.path.relpath(fp, ROOT)}")
                return 1
    return 0

with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(process_track, all_flacs))

tagged_count = sum(results)
print(f"  Total FLAC tracks tagged with missing TITLE: {tagged_count}")

print("\nEXECUTION FINISHED!")
