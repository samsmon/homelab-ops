import os
import re
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

def extract_title(filename):
    name = os.path.splitext(filename)[0]
    m_sub = re.search(r'_\d{2}_(.*)$', name)
    if m_sub:
        return m_sub.group(1).strip()
    m_num = re.match(r'^\d+[\s\.-]+(?:[^-]+-\s+)?(.*)$', name)
    if m_num:
        return m_num.group(1).strip()
    if '_' in name and ' ' not in name:
        return name.replace('_', ' ').strip()
    return name.strip()

print("Finding tracks with missing TITLE tags...")
missing_tracks = []

for root, dirs, files in os.walk(ROOT):
    flacs = [f for f in files if f.lower().endswith('.flac')]
    for fl in flacs:
        fp = os.path.join(root, fl)
        # Check TITLE tag with show-tag
        r = subprocess.run(["metaflac", "--show-tag=TITLE", fp], capture_output=True, text=True, close_fds=True)
        if not r.stdout.strip():
            # Double check with export-tags
            r2 = subprocess.run(["metaflac", "--export-tags-to=-", fp], capture_output=True, text=True, close_fds=True)
            tags = {line.split('=', 1)[0].upper(): line.split('=', 1)[1] for line in r2.stdout.splitlines() if '=' in line}
            if 'TITLE' not in tags or not tags['TITLE'].strip():
                missing_tracks.append((fp, fl))

print(f"Total remaining tracks missing TITLE: {len(missing_tracks)}")

tagged = 0
for fp, fl in missing_tracks:
    title = extract_title(fl)
    if title:
        r_set = subprocess.run(["metaflac", f"--set-tag=TITLE={title}", fp], capture_output=True, text=True, close_fds=True)
        if r_set.returncode == 0:
            tagged += 1
            print(f"  Tagged: '{title}' on {os.path.relpath(fp, ROOT)}")

print(f"Successfully tagged {tagged} tracks.")
