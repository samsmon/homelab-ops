import os
import re

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=" * 60)
print(f"DEEP AUDIT ROUND 152: {ROOT}")
print("=" * 60)

# 1. Missing tilde on artist/umbrella level (depth 1 from category)
missing_tilde = []
categories = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d))]

for cat in categories:
    cat_dir = os.path.join(ROOT, cat)
    for artist in os.listdir(cat_dir):
        ap = os.path.join(cat_dir, artist)
        if os.path.isdir(ap) and not artist.endswith("~"):
            missing_tilde.append(f"{cat}/{artist}")

print(f"\n1. Artist/Umbrella folders missing tilde (~): {len(missing_tilde)}")
for m in missing_tilde[:10]:
    print(f"   - {m}")

# 2. Junk files (.DS_Store, Thumbs.db, desktop.ini, .m3u inside albums)
junk_files = []
junk_names = {'.ds_store', 'thumbs.db', 'desktop.ini'}
m3u_files = []

for root, dirs, files in os.walk(ROOT):
    for f in files:
        fl = f.lower()
        fp = os.path.join(root, f)
        if fl in junk_names or fl.startswith('._'):
            junk_files.append(fp)
        elif fl.endswith(('.m3u', '.m3u8')) and fp != os.path.join(ROOT, 'Lossless.m3u8'):
            m3u_files.append(fp)

print(f"\n2. OS Junk files: {len(junk_files)}")
for j in junk_files[:10]:
    print(f"   - {j}")

print(f"\n3. In-album playlist clutter (.m3u/.m3u8): {len(m3u_files)}")
for m in m3u_files[:10]:
    print(f"   - {m}")

# 4. Folder format noise ([FLAC], [WEB-FLAC], [Hi-Res], etc.)
format_noise_dirs = []
pattern = re.compile(r'\[(FLAC|WEB-FLAC|CD-FLAC|Hi-Res|24bit|24bit[^\s]*|96kHz[^\s]*|48kHz[^\s]*|FLAC[^\s]*)\]|\((Hi-Res|FLAC|24bit|96kHz)\)|【FLAC】', re.IGNORECASE)

for root, dirs, files in os.walk(ROOT):
    for d in dirs:
        if pattern.search(d):
            format_noise_dirs.append(os.path.join(root, d))

print(f"\n4. Album directories with format noise tags in name: {len(format_noise_dirs)}")
for d in format_noise_dirs[:15]:
    rel = os.path.relpath(d, ROOT)
    print(f"   - {rel}")

# 5. Raw date prefix in album names (YYYY.MM.DD or YYYY-MM-DD at start)
date_prefix_dirs = []
date_pat = re.compile(r'^\d{4}[\.-]\d{2}[\.-]\d{2}\s+')
for root, dirs, files in os.walk(ROOT):
    for d in dirs:
        if date_pat.search(d):
            date_prefix_dirs.append(os.path.join(root, d))

print(f"\n5. Album directories with raw date prefix (YYYY.MM.DD): {len(date_prefix_dirs)}")
for d in date_prefix_dirs[:15]:
    rel = os.path.relpath(d, ROOT)
    print(f"   - {rel}")

# 6. Nested unnecessary folders (single subfolder named 'FLAC', 'CD', 'Disc 1' when only 1 disc)
nested_issues = []
for root, dirs, files in os.walk(ROOT):
    # Check if a folder has exactly one subdir named 'FLAC' or 'CD' or 'Disc 1' and no other dirs
    if len(dirs) == 1 and not files:
        sub = dirs[0]
        if sub.lower() in ['flac', 'cd', 'disc 1', 'disc 01', 'cd1', 'cd 1']:
            nested_issues.append((os.path.join(root, sub), root))

print(f"\n6. Unnecessarily nested single-container folders (e.g. /FLAC, /CD, /Disc 1): {len(nested_issues)}")
for sub, parent in nested_issues[:10]:
    rel = os.path.relpath(parent, ROOT)
    print(f"   - {rel} -> /{os.path.basename(sub)}")

# 7. Check for Touhou or other large split franchises
print("\n7. Checking key franchise consistency:")
for cat in categories:
    cat_path = os.path.join(ROOT, cat)
    dirs = [d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))]
    # Touhou check
    th = [d for d in dirs if 'touhou' in d.lower() or '東方' in d]
    if th:
        print(f"   Touhou dirs in {cat}: {th}")
    # Love Live check
    ll = [d for d in dirs if 'love live' in d.lower() or 'ラブライブ' in d]
    if ll:
        print(f"   Love Live dirs in {cat}: {ll}")
    # Idolmaster check
    im = [d for d in dirs if 'idolmaster' in d.lower() or 'アイドルマスター' in d]
    if im:
        print(f"   Idolmaster dirs in {cat}: {im}")

# 8. Non-FLAC audio check across whole library
non_flac = []
for root, dirs, files in os.walk(ROOT):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.wav', '.aiff', '.aif', '.wv', '.mp3', '.m4a', '.aac', '.ogg', '.cue', '.log', '.accurip']:
            non_flac.append(os.path.join(root, f))
print(f"\n8. Non-FLAC or Clutter audio files: {len(non_flac)}")
