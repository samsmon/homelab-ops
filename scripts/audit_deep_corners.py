import os

ROOT = "/mnt/hdd-backup/music/Lossless"

print("======================================================")
print("=== DEEP SCAN OF ALL CORNERS & POTENTIAL ISSUES ===")
print("======================================================")

# 1. Inspect _corrupted_quarantine
quarantine = os.path.join(ROOT, "_corrupted_quarantine")
print(f"\n1. _corrupted_quarantine: exists = {os.path.exists(quarantine)}")
if os.path.exists(quarantine):
    for r, d, f in os.walk(quarantine):
        print(f"  {r}: {len(f)} files, {len(d)} dirs")
        for file in f[:5]:
            print(f"    - {file}")

# 2. Check Gakumas (Gakuen Idolmaster)
print(f"\n2. Gakuen Idolmaster Inspection:")
gakumas_dirs = []
for r, d, f in os.walk(ROOT):
    if "学園アイドルマスター" in r or "Gakuen" in r or "gakumas" in r.lower():
        gakumas_dirs.append(r)

for gd in gakumas_dirs:
    # only check if it is directly the umbrella or category
    print(f"  Found Gakumas path: {gd}")
    items = os.listdir(gd)
    dirs_only = [i for i in items if os.path.isdir(os.path.join(gd, i))]
    files_only = [i for i in items if os.path.isfile(os.path.join(gd, i))]
    print(f"    {len(dirs_only)} dirs, {len(files_only)} files")
    for f in files_only:
        print(f"    [STRAY FILE] {f}")
    for d in sorted(dirs_only):
        dp = os.path.join(gd, d)
        sub_files = os.listdir(dp)
        audio = [x for x in sub_files if x.endswith(('.flac', '.wav', '.wv', '.m4a', '.aif', '.aiff', '.mp3'))]
        sub_dirs = [x for x in sub_files if os.path.isdir(os.path.join(dp, x))]
        if len(audio) == 0:
            print(f"    [EMPTY/NO AUDIO ALBUM] {d} (subdirs: {sub_dirs})")
        if any(c in d for c in ':*?"<>|'):
            print(f"    [FORBIDDEN CHAR IN ALBUM] {d}")

# 3. Check for any empty directories across the ENTIRE Lossless root
print("\n3. Scanning for ANY empty directories across the ENTIRE Lossless root:")
empty_dirs = []
for r, d, f in os.walk(ROOT):
    if not d and not f:
        empty_dirs.append(r)
print(f"  Total completely empty leaf directories: {len(empty_dirs)}")
for ed in empty_dirs[:20]:
    print(f"    {os.path.relpath(ed, ROOT)}")

# 4. Check for any junk files (.DS_Store, Thumbs.db, desktop.ini, ._* etc.)
print("\n4. Scanning for system junk files (.DS_Store, Thumbs.db, desktop.ini, ._*):")
junk_files = []
for r, d, f in os.walk(ROOT):
    for file in f:
        if file.lower() in ('.ds_store', 'thumbs.db', 'desktop.ini') or file.startswith('._'):
            junk_files.append(os.path.join(r, file))
print(f"  Total junk files found: {len(junk_files)}")
for jf in junk_files[:20]:
    print(f"    {os.path.relpath(jf, ROOT)}")

# 5. Check artist / umbrella folders without trailing tilde ' ~'
print("\n5. Checking Category subdirectories for missing trailing tilde ' ~':")
missing_tilde = []
for cat in os.listdir(ROOT):
    cat_path = os.path.join(ROOT, cat)
    if not os.path.isdir(cat_path) or cat.startswith('.'):
        continue
    for entry in os.listdir(cat_path):
        ep = os.path.join(cat_path, entry)
        if os.path.isdir(ep) and not entry.endswith(' ~') and not entry.startswith('_'):
            missing_tilde.append((cat, entry))
print(f"  Total folders missing ' ~': {len(missing_tilde)}")
for cat, entry in missing_tilde:
    print(f"    [{cat}] {entry}")
