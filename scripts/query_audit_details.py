#!/usr/bin/env python3
import json

with open('/tmp/audit_lossless_report.json') as f:
    d = json.load(f)

print('=== 1. MISSING TILDE (4) ===')
for item in d['missing_tilde']:
    print(f"  [{item['category']}] '{item['folder']}'")

print('\n=== 2. ALL 10 COLLISION CASES & CAUSES ===')
for artist, cols in d['collisions'].items():
    print(f"\nArtist: {artist}")
    for pure_name, paths in cols.items():
        print(f"  Colliding Name: '{pure_name}'")
        for p in paths:
            print(f"    Path: {p}")

print('\n=== 3. WHAT ARE THE 548 NON-FLAC AUDIO FILES? ===')
# Let's inspect each folder that has non-flac
for p in d['non_flac_audio'][:30]:
    print(f"  {p}")
if len(d['non_flac_audio']) > 30:
    print(f"  ... and {len(d['non_flac_audio']) - 30} more")
