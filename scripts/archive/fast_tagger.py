import os
import struct
import subprocess
import re

ROOT = "/mnt/hdd-backup/music/Lossless"

def get_flac_tags(fp):
    """Parse Vorbis comment directly from FLAC header in pure Python in ~0.5ms"""
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

print("Scanning library using pure Python Vorbis parser...")
missing_tracks = []
total_flacs = 0

for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith('.flac'):
            total_flacs += 1
            fp = os.path.join(root, f)
            tags = get_flac_tags(fp)
            if 'TITLE' not in tags or not tags['TITLE'].strip():
                missing_tracks.append((fp, f))

print(f"Scanned {total_flacs} FLAC tracks.")
print(f"Found {len(missing_tracks)} tracks missing TITLE tag.")

tagged = 0
for fp, fl in missing_tracks:
    title = extract_title(fl)
    if title:
        r = subprocess.run(["metaflac", f"--set-tag=TITLE={title}", fp], capture_output=True, text=True)
        if r.returncode == 0:
            tagged += 1
            print(f"  Set TITLE tag: '{title}' on {os.path.relpath(fp, ROOT)}")

print(f"\nSuccessfully populated TITLE tags on {tagged} tracks!")
