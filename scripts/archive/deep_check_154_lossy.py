import os
import re
import subprocess

ROOT_LOSSY = "/mnt/hdd-backup/music/Lossy"

print("=" * 60)
print(f"DEEP AUDIT ROUND 154: LOSSY LIBRARY AUDIT ({ROOT_LOSSY})")
print("=" * 60)

# 1. Categories in Lossy
cats = sorted([d for d in os.listdir(ROOT_LOSSY) if os.path.isdir(os.path.join(ROOT_LOSSY, d))])
print(f"Categories in Lossy: {cats}")

# 2. Artist folders missing tilde (~) in Lossy
missing_tilde_lossy = []
for cat in cats:
    cp = os.path.join(ROOT_LOSSY, cat)
    for artist in os.listdir(cp):
        ap = os.path.join(cp, artist)
        if os.path.isdir(ap) and not artist.endswith("~"):
            missing_tilde_lossy.append(f"{cat}/{artist}")

print(f"\n1. Artist folders missing tilde (~) in Lossy: {len(missing_tilde_lossy)}")
for m in missing_tilde_lossy[:15]:
    print(f"   - {m}")

# 3. Clutter files in Lossy (.cue, .log, .accurip, .m3u, .html, .url, .txt)
clutter_lossy = []
clutter_exts = {'.cue', '.log', '.accurip', '.html', '.htm', '.url', '.ini'}
for root, dirs, files in os.walk(ROOT_LOSSY):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        fp = os.path.join(root, f)
        if ext in clutter_exts:
            clutter_lossy.append((ext, fp))
        elif ext in ['.m3u', '.m3u8'] and fp != os.path.join(ROOT_LOSSY, 'Lossy.m3u8'):
            clutter_lossy.append((ext, fp))

print(f"\n2. Clutter files in Lossy (.cue, .log, .m3u, etc.): {len(clutter_lossy)}")
for ext, fp in clutter_lossy[:15]:
    print(f"   - [{ext}] {os.path.relpath(fp, ROOT_LOSSY)}")

# 4. Format noise in Lossy album folders ([MP3], [320K], (MP3), etc.)
noise_dirs_lossy = []
noise_pat = re.compile(r'\[(MP3|320K|320kbps|AAC|M4A|WEB-MP3|MP3-320k)\]|\((MP3|320k|320kbps)\)', re.IGNORECASE)
for root, dirs, files in os.walk(ROOT_LOSSY):
    for d in dirs:
        if noise_pat.search(d):
            noise_dirs_lossy.append(os.path.join(root, d))

print(f"\n3. Album folders with format noise in Lossy: {len(noise_dirs_lossy)}")
for d in noise_dirs_lossy[:15]:
    print(f"   - {os.path.relpath(d, ROOT_LOSSY)}")

# 5. Empty directories in Lossy
empty_dirs_lossy = []
for root, dirs, files in os.walk(ROOT_LOSSY, topdown=False):
    if not dirs and not files:
        empty_dirs_lossy.append(root)

print(f"\n4. Empty directories in Lossy: {len(empty_dirs_lossy)}")
for d in empty_dirs_lossy[:15]:
    print(f"   - {os.path.relpath(d, ROOT_LOSSY)}")

# 6. Case collisions in Lossy
case_collisions_lossy = 0
for root, dirs, files in os.walk(ROOT_LOSSY):
    seen = {}
    for d in dirs:
        dl = d.lower()
        if dl in seen:
            print(f"   Dir case collision in {root}: '{seen[dl]}' vs '{d}'")
            case_collisions_lossy += 1
        seen[dl] = d
    seen_f = {}
    for f in files:
        fl = f.lower()
        if fl in seen_f:
            print(f"   File case collision in {root}: '{seen_f[fl]}' vs '{f}'")
            case_collisions_lossy += 1
        seen_f[fl] = f

print(f"\n5. Case collisions in Lossy: {case_collisions_lossy}")

# 7. Total tracks breakdown in Lossy
lossy_audio = {}
for root, dirs, files in os.walk(ROOT_LOSSY):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wma', '.flac']:
            lossy_audio[ext] = lossy_audio.get(ext, 0) + 1

print(f"\n6. Audio formats in Lossy:")
for ext, count in sorted(lossy_audio.items()):
    print(f"   {ext}: {count}")
