import os
import re
import subprocess
import struct

ROOT = "/mnt/hdd-backup/music/Lossless"

env = os.environ.copy()
env["LC_ALL"] = "C.UTF-8"
env["LANG"] = "C.UTF-8"

print("=" * 60)
print("MASTER TAG & COVER PERFECTION")
print("=" * 60)

# 1. Clean remaining duplicate cover.png (case-insensitive)
covers_cleaned = 0
for root, dirs, files in os.walk(ROOT):
    fl = [f.lower() for f in files]
    if ('cover.jpg' in fl or 'cover.jpeg' in fl) and 'cover.png' in fl:
        png_names = [f for f in files if f.lower() == 'cover.png']
        for pn in png_names:
            fp = os.path.join(root, pn)
            try:
                os.remove(fp)
                covers_cleaned += 1
                print(f"Removed redundant PNG cover: {os.path.relpath(fp, ROOT)}")
            except Exception as e:
                print(f"Failed to remove {fp}: {e}")

print(f"Total duplicate cover.png removed: {covers_cleaned}")

# 2. Extract title robustly
def extract_title(filename):
    name = os.path.splitext(filename)[0].strip()
    m1 = re.match(r'^\d+[-_\.]+\d+[-_\.]+(.*)$', name)
    if m1:
        return m1.group(1).strip()
    m2 = re.search(r'_\d{2}_(.*)$', name)
    if m2:
        return m2.group(1).strip()
    m3 = re.match(r'^\d+[\s\.-]+(?:[^-]+-\s+)?(.*)$', name)
    if m3:
        return m3.group(1).strip()
    if '_' in name and ' ' not in name:
        return name.replace('_', ' ').strip()
    return name

# Fast Vorbis reader
def get_flac_tags(fp):
    try:
        with open(fp, 'rb') as f:
            if f.read(4) != b'fLaC':
                return {}
            while True:
                block_header = f.read(4)
                if len(block_header) < 4:
                    break
                is_last = (block_header[0] & 0x80) != 0
                block_type = block_header[0] & 0x7F
                block_len = (block_header[1] << 16) | (block_header[2] << 8) | block_header[3]
                if block_type == 4:
                    data = f.read(block_len)
                    vlen = struct.unpack('<I', data[0:4])[0]
                    pos = 4 + vlen
                    num = struct.unpack('<I', data[pos:pos+4])[0]
                    pos += 4
                    tags = {}
                    for _ in range(num):
                        if pos + 4 > len(data):
                            break
                        clen = struct.unpack('<I', data[pos:pos+4])[0]
                        pos += 4
                        cstr = data[pos:pos+clen].decode('utf-8', errors='ignore')
                        pos += clen
                        if '=' in cstr:
                            k, v = cstr.split('=', 1)
                            tags[k.upper()] = v
                    return tags
                else:
                    f.seek(block_len, 1)
                if is_last:
                    break
    except Exception:
        pass
    return {}

# 3. Find and fix all tracks missing TITLE or containing '???' in TITLE
print("\nScanning all FLAC tracks for missing or corrupted TITLE tags...")
fixed_count = 0
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith('.flac'):
            fp = os.path.join(root, f)
            tags = get_flac_tags(fp)
            cur_title = tags.get('TITLE', '').strip()
            # If missing or all question marks
            if not cur_title or re.match(r'^\?+$', cur_title):
                clean_title = extract_title(f)
                if clean_title:
                    subprocess.run(["metaflac", "--remove-tag=TITLE", fp], env=env)
                    # Write tag via temp file to guarantee UTF-8 encoding
                    tf = "/tmp/cur_tag.txt"
                    with open(tf, "w", encoding="utf-8") as tfile:
                        tfile.write(f"TITLE={clean_title}\n")
                    r = subprocess.run(["metaflac", f"--import-tags-from={tf}", fp], env=env)
                    if r.returncode == 0:
                        fixed_count += 1
                        if fixed_count <= 20 or fixed_count % 25 == 0:
                            print(f"  Fixed TITLE '{clean_title}' on {os.path.relpath(fp, ROOT)}")

if os.path.exists("/tmp/cur_tag.txt"):
    os.remove("/tmp/cur_tag.txt")

print(f"\nTotal tracks successfully tagged with pristine UTF-8 TITLE: {fixed_count}")
