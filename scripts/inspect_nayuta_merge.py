import os

uta_dir = "/mnt/hdd-backup/music/Lossless/J-Pop/7uta ~"
nayuta_dir = "/mnt/hdd-backup/music/Lossless/Doujinshi/nayuta ~"

uta_albums = set(os.listdir(uta_dir)) if os.path.exists(uta_dir) else set()
nayuta_albums = set(os.listdir(nayuta_dir)) if os.path.exists(nayuta_dir) else set()

print(f"7uta albums count: {len(uta_albums)}")
print(f"nayuta albums count: {len(nayuta_albums)}")

common = uta_albums.intersection(nayuta_albums)
print(f"Common albums: {common}")

for a in sorted(uta_albums):
    p = os.path.join(uta_dir, a)
    files = os.listdir(p) if os.path.isdir(p) else []
    print(f"  7uta album: {a} ({len(files)} items)")
