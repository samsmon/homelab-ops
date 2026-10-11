import os
import re
from pathlib import Path

LOSSLESS_ROOT = Path('/mnt/hdd-backup/music/Lossless')

print("=== 1. THE IDOLM@STER CONTENTS ===")
imas = LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~'
for p in imas.iterdir():
    print(f"DIR: {repr(p.name)}")
    if p.is_dir():
        items = list(p.iterdir())
        print(f"  Count: {len(items)}")
        for sub in items[:5]:
            print(f"    - {repr(sub.name)}")

print("\n=== 2. BOCCHI THE ROCK CONTENTS ===")
bocchi = LOSSLESS_ROOT / 'Anime' / 'Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~'
for p in bocchi.iterdir():
    print(f"DIR: {repr(p.name)}")
    if p.is_dir():
        items = list(p.iterdir())
        print(f"  Count: {len(items)}")
        for sub in items[:5]:
            print(f"    - {repr(sub.name)}")

print("\n=== 3. ALL UMBRELLAS WITH MIXED / INCONSISTENT STRUCTURE ===")
for cat in LOSSLESS_ROOT.iterdir():
    if not cat.is_dir():
        continue
    for artist in cat.iterdir():
        if not artist.is_dir():
            continue
        subdirs = [d for d in artist.iterdir() if d.is_dir()]
        has_subseries = any(re.match(r'^(?:\[\d{4}|\d{2}\.|Solo|Unit|Group|Series|Season)', d.name, re.IGNORECASE) for d in subdirs)
        if has_subseries:
            loose = [d for d in subdirs if not re.match(r'^(?:\[\d{4}|\d{2}\.|Solo|Unit|Group|Series|Season)', d.name, re.IGNORECASE)]
            if loose:
                print(f"[{cat.name}] {artist.name}")
                print(f"   Subseries: {[d.name for d in subdirs if not d in loose]}")
                print(f"   Loose ({len(loose)}): {[d.name for d in loose[:5]]}")

print("\n=== 4. ALBUMS WITH REMAINING BRACKETS / BITRATES / FORMATS ===")
bad_albums = []
for p in LOSSLESS_ROOT.rglob('*'):
    if not p.is_dir():
        continue
    if p.name in ['BK', 'Scans', 'Disc 1', 'Disc 2', 'Disc 3', 'Disc 4', 'Disc 5']:
        continue
    # Check if ends with bracketed tags
    if re.search(r'[\[\(](?:FLAC|WEB-FLAC|Hi-Res|MP3|AAC|24bit|16bit|48kHz|96kHz|192kHz|CD|BK|BD|DVD|WEB|Lossless|Vinyl|WVP)[^\]\)]*[\]\)]\s*$', p.name, re.IGNORECASE):
        bad_albums.append(p)
print(f"Total albums with format tags: {len(bad_albums)}")
for b in bad_albums[:30]:
    print(f"  {b.relative_to(LOSSLESS_ROOT)}")
