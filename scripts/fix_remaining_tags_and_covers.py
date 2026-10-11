import os
import re
import subprocess
import struct

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=== FIXING REMAINING COVERS & TAGS ===")

# 1. Clean remaining duplicate cover.png
for root, dirs, files in os.walk(ROOT):
    fl = [f.lower() for f in files]
    has_jpg = any(i in ['cover.jpg', 'cover.jpeg'] for i in fl)
    has_png = any(i == 'cover.png' for i in fl)
    if has_jpg and has_png:
        png_name = [f for f in files if f.lower() == 'cover.png'][0]
        png_p = os.path.join(root, png_name)
        try:
            os.remove(png_p)
            print(f"Removed remaining cover.png: {os.path.relpath(png_p, ROOT)}")
        except Exception as e:
            print(f"Failed to remove {png_p}: {e}")

# 2. Extract title robustly
def extract_title(filename):
    name = os.path.splitext(filename)[0].strip()
    # Pattern 1: double track number like 00-04-Title or 01-01-Title
    m1 = re.match(r'^\d+[-_\.]+\d+[-_\.]+(.*)$', name)
    if m1:
        return m1.group(1).strip()
    # Pattern 2: prefix_07_Title
    m2 = re.search(r'_\d{2}_(.*)$', name)
    if m2:
        return m2.group(1).strip()
    # Pattern 3: standard track number like "01. Title" or "01 - Artist - Title"
    m3 = re.match(r'^\d+[\s\.-]+(?:[^-]+-\s+)?(.*)$', name)
    if m3:
        return m3.group(1).strip()
    # Pattern 4: single word joined by underscores
    if '_' in name and ' ' not in name:
        return name.replace('_', ' ').strip()
    # Fallback: whole filename without extension
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

tagged_count = 0
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith('.flac'):
            fp = os.path.join(root, f)
            tags = get_flac_tags(fp)
            if 'TITLE' not in tags or not tags['TITLE'].strip():
                title = extract_title(f)
                if title:
                    r = subprocess.run(["metaflac", f"--set-tag=TITLE={title}", fp], capture_output=True, text=True)
                    if r.returncode == 0:
                        tagged_count += 1
                        print(f"Set TITLE '{title}' on {os.path.relpath(fp, ROOT)}")

print(f"\nFinished: Successfully tagged {tagged_count} tracks.")
