#!/usr/bin/env python3
import json
import os

with open('/tmp/audit_lossless_report.json') as f:
    d = json.load(f)

print('=== 1. MISSING TILDE (4) ===')
for item in d['missing_tilde']:
    print(f"  [{item['category']}] {item['folder']}")

print('\n=== 2. ARTISTS WITH PURE ALBUM COLLISIONS (10) ===')
for artist, cols in d['collisions'].items():
    print(f"  Artist: {artist}")
    for pure_name, paths in cols.items():
        print(f"    Colliding Pure Name: '{pure_name}'")
        for p in paths:
            print(f"      - {p}")

print('\n=== 3. NON-FLAC AUDIO FILES BREAKDOWN (548) ===')
exts = {}
non_flac_by_cat = {}
for p in d['non_flac_audio']:
    ext = p.split('.')[-1].lower()
    exts[ext] = exts.get(ext, 0) + 1
    parts = p.split('/')
    # /mnt/hdd-backup/music/Lossless/<cat>/...
    cat = parts[5] if len(parts) > 5 else "unknown"
    non_flac_by_cat[cat] = non_flac_by_cat.get(cat, 0) + 1

print(f"  Extensions: {exts}")
print(f"  By Category: {non_flac_by_cat}")
print("  Sample non-flac paths (first 15):")
for p in d['non_flac_audio'][:15]:
    print(f"    {p}")

print('\n=== 4. CONTAINER FOLDERS (33) ===')
for c in d['container_folders']:
    print(f"  {c}")

print('\n=== 5. VIDEO FILES (8) ===')
for v in d['video_files']:
    print(f"  {v['size_mb']} MB : {v['path']}")

print('\n=== 6. JAPANESE FIRST (Sample of 113) ===')
for j in d['jp_first_folders'][:20]:
    print(f"  [{j['category']}] {j['folder']}")

print('\n=== 7. PURE JAPANESE (Sample of 119) ===')
for pj in d['pure_jp_folders'][:20]:
    print(f"  [{pj['category']}] {pj['folder']}")
