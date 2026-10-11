import os
import re
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

missing_title_tracks = []

for root, dirs, files in os.walk(ROOT):
    flacs = [f for f in files if f.lower().endswith('.flac')]
    for fl in flacs:
        fp = os.path.join(root, fl)
        # Check TITLE tag
        r = subprocess.run(["metaflac", "--export-tags-to=-", fp], capture_output=True, text=True)
        tags = {line.split('=', 1)[0].upper(): line.split('=', 1)[1] for line in r.stdout.splitlines() if '=' in line}
        if 'TITLE' not in tags or not tags['TITLE'].strip():
            # Guess title from filename: e.g. "01. Song Title.flac" -> "Song Title"
            m = re.match(r'^\d+[\s\.-]+(?:[^-]+-\s+)?(.*)\.flac$', fl)
            guessed = m.group(1).strip() if m else os.path.splitext(fl)[0]
            missing_title_tracks.append((fp, fl, guessed))

print(f"Total FLAC tracks missing TITLE tag: {len(missing_title_tracks)}")
for fp, fl, guessed in missing_title_tracks[:25]:
    rel = os.path.relpath(fp, ROOT)
    print(f"  {rel} -> Guessed: '{guessed}'")
