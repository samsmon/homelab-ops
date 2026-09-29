import os
import struct
import subprocess

ROOT_LOSSLESS = "/mnt/hdd-backup/music/Lossless"
ROOT_LOSSY = "/mnt/hdd-backup/music/Lossy"

print("=" * 60)
print("VERIFICATION AUDIT ROUND 153")
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

# 3. HTML spam files
html_files = []
for root, dirs, files in os.walk(ROOT_LOSSLESS):
    for f in files:
        if f.lower().endswith(('.html', '.htm')):
            html_files.append(os.path.join(root, f))
print(f"2. HTML spam files: {len(html_files)}")

# 4. Duplicate Cover Art (cover.png AND cover.jpg)
duplicate_covers = []
for root, dirs, files in os.walk(ROOT_LOSSLESS):
    images = [f.lower() for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    has_jpg = any('cover.jpg' in i or 'cover.jpeg' in i for i in images)
    has_png = any('cover.png' in i for i in images)
    if has_jpg and has_png:
        duplicate_covers.append(root)
print(f"3. Folders with both cover.jpg and cover.png: {len(duplicate_covers)}")

# 5. Fast Vorbis comment parser for TITLE tags
def get_flac_tags(fp):
    try:
        with open(fp, 'rb') as f:
            header = f.read(4)
            if header != b'fLaC':
                return {}
            while True:
                block_header = f.read(4)
                if len(block_header) < 4:
                    break
                is_last = (block_header[0] & 0x80) != 0
                block_type = block_header[0] & 0x7F
                block_len = (block_header[1] << 16) | (block_header[2] << 8) | block_header[3]
                if block_type == 4: # VORBIS_COMMENT
                    data = f.read(block_len)
                    vendor_len = struct.unpack('<I', data[0:4])[0]
                    pos = 4 + vendor_len
                    num_comments = struct.unpack('<I', data[pos:pos+4])[0]
                    pos += 4
                    tags = {}
                    for _ in range(num_comments):
                        if pos + 4 > len(data):
                            break
                        clen = struct.unpack('<I', data[pos:pos+4])[0]
                        pos += 4
                        comment_str = data[pos:pos+clen].decode('utf-8', errors='ignore')
                        pos += clen
                        if '=' in comment_str:
                            k, v = comment_str.split('=', 1)
                            tags[k.upper()] = v
                    return tags
                else:
                    f.seek(block_len, 1)
                if is_last:
                    break
    except Exception:
        pass
    return {}

missing_titles = []
total_flacs = 0
for root, dirs, files in os.walk(ROOT_LOSSLESS):
    for f in files:
        if f.lower().endswith('.flac'):
            total_flacs += 1
            fp = os.path.join(root, f)
            tags = get_flac_tags(fp)
            if 'TITLE' not in tags or not tags['TITLE'].strip():
                missing_titles.append(fp)

print(f"4. Total FLAC tracks in Lossless: {total_flacs}")
print(f"5. Total tracks missing TITLE tag: {len(missing_titles)}")
for m in missing_titles[:10]:
    print(f"   - {m}")

print("\nALL VERIFICATIONS COMPLETE!")
