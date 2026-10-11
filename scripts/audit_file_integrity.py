#!/usr/bin/env python3
import os
import re

BASE = "/mnt/hdd-backup/music/Lossless"

print("=== DEEP FILE-LEVEL INTEGRITY & JUNK AUDIT ===")

zero_byte_files = []
double_ext_files = []
apple_double_files = []
os_junk_files = []
bad_char_files = []
non_standard_image_files = []
cover_files = []
cue_sheets = []
log_files = []
m3u_files = []

for root, dirs, files in os.walk(BASE):
    for f in files:
        fp = os.path.join(root, f)
        sz = 0
        try:
            sz = os.path.getsize(fp)
        except Exception:
            pass

        # 0-byte files
        if sz == 0:
            zero_byte_files.append(fp)

        # AppleDouble (._*)
        if f.startswith('._'):
            apple_double_files.append(fp)

        # OS junk
        if f.lower() in ('thumbs.db', '.ds_store', 'desktop.ini', 'folder.ico'):
            os_junk_files.append(fp)

        # Double extensions
        if re.search(r'\.(flac|mp3|wav)\.(flac|mp3|wav)$', f, re.IGNORECASE):
            double_ext_files.append(fp)

        # Hidden control characters or zero-width spaces
        if re.search(r'[\x00-\x1f\x7f\u200b\u200c\u200d\ufeff]', f):
            bad_char_files.append(fp)

        ext = os.path.splitext(f)[1].lower()
        if ext in ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'):
            if f.lower() in ('cover.jpg', 'cover.png', 'folder.jpg', 'front.jpg'):
                cover_files.append(fp)
            elif sz > 20 * 1024 * 1024: # > 20 MB image
                non_standard_image_files.append((fp, sz / (1024 * 1024)))
        elif ext == '.cue':
            cue_sheets.append(fp)
        elif ext == '.log':
            log_files.append(fp)
        elif ext in ('.m3u', '.m3u8'):
            if fp != os.path.join(BASE, 'Lossless.m3u8'):
                m3u_files.append(fp)

print(f"Zero-byte files: {len(zero_byte_files)}")
for z in zero_byte_files:
    print(f"  {z}")

print(f"AppleDouble (._*) junk: {len(apple_double_files)}")
for a in apple_double_files[:10]:
    print(f"  {a}")

print(f"OS junk (Thumbs.db, .DS_Store, desktop.ini): {len(os_junk_files)}")
for o in os_junk_files:
    print(f"  {o}")

print(f"Double extension files: {len(double_ext_files)}")
for d in double_ext_files:
    print(f"  {d}")

print(f"Files with control chars/zero-width space: {len(bad_char_files)}")
for b in bad_char_files[:10]:
    print(f"  {b}")

print(f"Massive images (>20MB): {len(non_standard_image_files)}")
for n, sz in non_standard_image_files[:10]:
    print(f"  {sz:.1f} MB: {n}")

print(f"CUE sheets found: {len(cue_sheets)}")
print(f"EAC/XLD Log files found: {len(log_files)}")
print(f"Local m3u/m3u8 files found: {len(m3u_files)}")
for m in m3u_files[:10]:
    print(f"  {m}")
