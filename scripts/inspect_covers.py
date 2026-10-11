import os

ROOT = "/mnt/hdd-backup/music/Lossless"

dup_covers = []
for root, dirs, files in os.walk(ROOT):
    fl = [f.lower() for f in files]
    if 'cover.jpg' in fl and 'cover.png' in fl:
        # Get actual filenames
        jpg_name = [f for f in files if f.lower() == 'cover.jpg'][0]
        png_name = [f for f in files if f.lower() == 'cover.png'][0]
        jpg_p = os.path.join(root, jpg_name)
        png_p = os.path.join(root, png_name)
        jpg_sz = os.path.getsize(jpg_p)
        png_sz = os.path.getsize(png_p)
        dup_covers.append((root, jpg_name, jpg_sz, png_name, png_sz))

print(f"Total folders with both cover.jpg and cover.png: {len(dup_covers)}")
for root, jn, jsz, pn, psz in dup_covers[:15]:
    rel = os.path.relpath(root, ROOT)
    print(f"  {rel}: {jn} ({jsz / 1024:.1f} KB) vs {pn} ({psz / 1024:.1f} KB)")
