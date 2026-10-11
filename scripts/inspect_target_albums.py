import os
import re
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

# Targets from deep_check_153 sample
target_dirs = set()
for root, dirs, files in os.walk(ROOT):
    flacs = [f for f in files if f.lower().endswith('.flac')]
    if flacs:
        # test first flac
        fp = os.path.join(root, flacs[0])
        r = subprocess.run(["metaflac", "--show-tag=TITLE", fp], capture_output=True, text=True)
        if not r.stdout.strip():
            # also check lowercase title
            r_all = subprocess.run(["metaflac", "--export-tags-to=-", fp], capture_output=True, text=True)
            tags = {line.split('=', 1)[0].upper(): line.split('=', 1)[1] for line in r_all.stdout.splitlines() if '=' in line}
            if 'TITLE' not in tags:
                target_dirs.add(root)

print(f"Target album directories with missing TITLE tag: {len(target_dirs)}")
for td in sorted(target_dirs):
    rel = os.path.relpath(td, ROOT)
    flacs = sorted([f for f in os.listdir(td) if f.lower().endswith('.flac')])
    print(f"\nAlbum: {rel} ({len(flacs)} tracks)")
    for fl in flacs[:3]:
        m = re.match(r'^\d+[\s\.-]+(?:[^-]+-\s+)?(.*)\.flac$', fl)
        guessed = m.group(1).strip() if m else os.path.splitext(fl)[0]
        print(f"   Track: {fl} -> Title: '{guessed}'")
