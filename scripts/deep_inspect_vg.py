import os
import glob
from mutagen.flac import FLAC
from PIL import Image

print("=== 1. CHECKING GALACTIC FANTASIA ===")
p = '/mnt/hdd-backup/music/Lossless/Vocaloid/Harumaki Gohan (はるまきごはん) ~/Galactic Fantasia'
if os.path.exists(p):
    for f in sorted(os.listdir(p)):
        if f.endswith('.flac'):
            audio = FLAC(os.path.join(p, f))
            print(f"  {f} | Artist: {audio.get('artist')} | AlbumArtist: {audio.get('albumartist')}")

print("\n=== 2. GLOBAL AUDIT (/mnt/hdd-backup/music/Lossless/Global) ===")
g_root = '/mnt/hdd-backup/music/Lossless/Global'
for root, dirs, files in os.walk(g_root):
    flacs = [f for f in files if f.endswith('.flac')]
    if flacs:
        print(f"\nAlbum: {root}")
        print(f"  Flacs ({len(flacs)}): {flacs[:3]}")
        cov = os.path.join(root, 'Cover.jpg')
        low_cov = os.path.join(root, 'cover.jpg')
        png_cov = os.path.join(root, 'cover.png')
        print(f"  Cover.jpg: {os.path.exists(cov)}, cover.jpg: {os.path.exists(low_cov)}, cover.png: {os.path.exists(png_cov)}")
        for fl in flacs:
            af = FLAC(os.path.join(root, fl))
            has_pic = len(af.pictures) > 0
            rg = 'replaygain_track_gain' in af
            print(f"    {fl} -> Title: {af.get('title')}, Artist: {af.get('artist')}, AA: {af.get('albumartist')}, Pic: {has_pic}, RG: {rg}")

print("\n=== 3. COVER ART RECONNAISSANCE ACROSS VOCALOID ===")
# For each album folder in Vocaloid, check what artwork exists
v_root = '/mnt/hdd-backup/music/Lossless/Vocaloid'
albums_summary = []
for root, dirs, files in os.walk(v_root):
    flacs = [f for f in files if f.endswith('.flac')]
    if flacs:
        images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        has_Cover_jpg = 'Cover.jpg' in files
        has_cover_jpg = 'cover.jpg' in files
        embedded = 0
        missing_embedded = 0
        for fl in flacs:
            af = FLAC(os.path.join(root, fl))
            if af.pictures and af.pictures[0].type == 3 and af.pictures[0].mime == 'image/jpeg':
                embedded += 1
            else:
                missing_embedded += 1
        albums_summary.append({
            'path': root,
            'flac_count': len(flacs),
            'has_Cover_jpg': has_Cover_jpg,
            'has_cover_jpg': has_cover_jpg,
            'images': images,
            'embedded': embedded,
            'missing_embedded': missing_embedded
        })

print(f"Total Vocaloid album folders: {len(albums_summary)}")
no_art_at_all = [a for a in albums_summary if not a['images'] and a['missing_embedded'] == a['flac_count']]
print(f"Folders with NO image file AND NO embedded cover: {len(no_art_at_all)}")
for a in no_art_at_all:
    print(f"  CRITICAL NO ART: {a['path']}")

only_lower = [a for a in albums_summary if not a['has_Cover_jpg'] and a['has_cover_jpg']]
print(f"Folders with lower 'cover.jpg' but no 'Cover.jpg': {len(only_lower)}")

only_other = [a for a in albums_summary if not a['has_Cover_jpg'] and not a['has_cover_jpg'] and a['images']]
print(f"Folders with other image names (e.g. png, folder.jpg, etc.): {len(only_other)}")
for a in only_other:
    print(f"  OTHER ART: {a['path']} -> {a['images']}")

only_embedded = [a for a in albums_summary if not a['images'] and a['embedded'] > 0]
print(f"Folders with NO image file but HAS embedded cover: {len(only_embedded)}")
for a in only_embedded:
    print(f"  RESCUEABLE FROM FLAC: {a['path']}")
