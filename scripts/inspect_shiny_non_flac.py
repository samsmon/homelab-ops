import os

ROOT = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~"

non_flacs = []
total_bytes = 0

for root, dirs, files in os.walk(ROOT):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.aiff', '.aif', '.wv', '.wav']:
            fp = os.path.join(root, f)
            sz = os.path.getsize(fp)
            total_bytes += sz
            non_flacs.append((ext, fp, sz))

print(f"Total non-FLAC files in Shiny Colors: {len(non_flacs)}")
print(f"Total size: {total_bytes / (1024*1024*1024):.2f} GB")

albums = {}
for ext, fp, sz in non_flacs:
    d = os.path.dirname(fp)
    albums[d] = albums.get(d, 0) + 1

print(f"\nAffected albums ({len(albums)}):")
for d, count in sorted(albums.items()):
    rel = os.path.relpath(d, ROOT)
    print(f"  {rel}: {count} tracks")
