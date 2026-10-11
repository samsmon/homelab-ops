import os
import re
import subprocess
import json
from PIL import Image
import mutagen
from mutagen.flac import FLAC

targets = [
    '/mnt/hdd-backup/music/Lossless/Global',
    '/mnt/hdd-backup/music/Lossless/Vocaloid'
]

print("=== STARTING FORENSIC AUDIT ON GLOBAL & VOCALOID ===")

all_albums = []
all_flacs = []
defects = {
    'flac_integrity': [],
    'missing_cover_file': [],
    'corrupt_or_small_cover': [],
    'missing_embedded_cover': [],
    'missing_tags': [],
    'forum_spam_tags': [],
    'non_standard_filename': [],
    'illegal_smb_char': [],
    'missing_replaygain': [],
    'multi_disc_structure_issue': [],
    'duplicate_or_clone_track': [],
    'extra_clutter_files': [],
}

MANDATORY_TAGS = ['title', 'artist', 'album', 'albumartist', 'tracknumber', 'tracktotal', 'discnumber', 'disctotal', 'date']

for t in targets:
    for root, dirs, files in os.walk(t):
        # Check clutter files
        for f in files:
            full_p = os.path.join(root, f)
            low_f = f.lower()
            if low_f.endswith(('.cue', '.log', '.accurip', '.txt', '.url', '.ini', '.m3u', '.m3u8')) and not full_p.endswith('Lossless.m3u8'):
                defects['extra_clutter_files'].append(full_p)
            elif low_f.endswith(('.png', '.jpeg', '.webp', '.bmp', '.gif')) and f != 'Cover.jpg':
                defects['extra_clutter_files'].append(full_p)
            elif low_f.endswith('.jpg') and f != 'Cover.jpg':
                defects['extra_clutter_files'].append(full_p)
            
            # Illegal SMB chars
            if any(c in f for c in ':*?"<>|\\') or f.endswith('.'):
                defects['illegal_smb_char'].append(full_p)

            if low_f.endswith('.flac'):
                all_flacs.append(full_p)
        
        # Check album folder (folder containing FLACs)
        flacs_in_dir = [f for f in files if f.lower().endswith('.flac')]
        if flacs_in_dir:
            all_albums.append(root)
            # Check Cover.jpg
            cov_p = os.path.join(root, 'Cover.jpg')
            if not os.path.exists(cov_p):
                defects['missing_cover_file'].append(root)
            else:
                try:
                    with Image.open(cov_p) as img:
                        w, h = img.size
                        fmt = img.format
                        mode = img.mode
                        if fmt != 'JPEG' or mode != 'RGB' or w < 500 or h < 500:
                            defects['corrupt_or_small_cover'].append((cov_p, f'{fmt} {mode} {w}x{h}'))
                except Exception as e:
                    defects['corrupt_or_small_cover'].append((cov_p, f'Corrupt: {e}'))

print(f"Total Album/Disc directories identified: {len(all_albums)}")
print(f"Total FLAC files identified: {len(all_flacs)}")

# Audit FLAC files
print("Scanning FLAC files metadata & integrity...")
for idx, flac_p in enumerate(all_flacs):
    fname = os.path.basename(flac_p)
    # Filename pattern: e.g. "01. Title.flac"
    if not re.match(r'^\d{2,3}\.\s+.+\.flac$', fname):
        defects['non_standard_filename'].append(flac_p)
    
    # Mutagen tag inspection
    try:
        audio = FLAC(flac_p)
        # Embedded cover check
        if not audio.pictures:
            defects['missing_embedded_cover'].append(flac_p)
        else:
            pic = audio.pictures[0]
            if pic.type != 3 or pic.mime != 'image/jpeg':
                defects['missing_embedded_cover'].append((flac_p, f"Type={pic.type}, Mime={pic.mime}"))

        # Tags check
        missing = []
        for tag in MANDATORY_TAGS:
            val = audio.get(tag)
            if not val or not str(val[0]).strip():
                # check aliases
                if tag == 'tracktotal' and (audio.get('totaltracks') or audio.get('trackc')):
                    continue
                if tag == 'disctotal' and (audio.get('totaldiscs') or audio.get('discc')):
                    continue
                if tag == 'date' and audio.get('year'):
                    continue
                missing.append(tag)
        if missing:
            defects['missing_tags'].append((flac_p, missing))

        # Forum ads / promo spam
        for k, v in audio.items():
            for val in v:
                val_str = str(val).lower()
                if any(s in val_str for s in ['tsdm', 'iacg', 'bbs.', '.com', '.net', '.org', 'share', 'torrent', 'weibo', 'http://', 'https://']) and k not in ['comment']:
                    # check if it is spam or legitimate url
                    if any(spam in val_str for spam in ['tsdm39', 'tsdm', 'iacg', 'cdbao', 'astost', '绯月', '天使动漫']):
                        defects['forum_spam_tags'].append((flac_p, k, val))
                if k == 'comment' and any(spam in val_str for spam in ['tsdm39', 'tsdm', 'iacg', 'cdbao', 'astost', 'www.', 'http', 'bbs']):
                    defects['forum_spam_tags'].append((flac_p, k, val))

        # Replaygain
        if 'replaygain_track_gain' not in audio:
            defects['missing_replaygain'].append(flac_p)

    except Exception as e:
        defects['flac_integrity'].append((flac_p, str(e)))

print("--- FORENSIC AUDIT RESULTS ---")
total_defect_count = sum(len(v) for v in defects.values())
print(f"TOTAL DEFECTS COUNT: {total_defect_count}")
for k, v in defects.items():
    print(f"  {k}: {len(v)} issues")

# Output detailed defect summary
with open('/tmp/audit_defects_vocaloid_global.json', 'w', encoding='utf-8') as f:
    json.dump(defects, f, indent=2, ensure_ascii=False)
print("Defect details written to /tmp/audit_defects_vocaloid_global.json")
