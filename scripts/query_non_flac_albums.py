#!/usr/bin/env python3
import json
from collections import defaultdict

with open('/tmp/audit_lossless_report.json') as f:
    d = json.load(f)

# Group non-flac by album folder
album_non_flac = defaultdict(lambda: defaultdict(int))
for p in d['non_flac_audio']:
    ext = p.split('.')[-1].lower()
    # find album folder
    parts = p.split('/')
    # find where Disc or album is
    # e.g. /mnt/hdd-backup/music/Lossless/Cat/Artist/...
    rel = '/'.join(parts[5:-1])
    album_non_flac[rel][ext] += 1

print(f"Total Albums with non-FLAC audio: {len(album_non_flac)}")
for album, exts in sorted(album_non_flac.items()):
    print(f"  {album} -> {dict(exts)}")
