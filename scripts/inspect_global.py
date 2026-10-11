import os

ROOT = "/mnt/hdd-backup/music/Lossless/Global"
artists = sorted(os.listdir(ROOT))
print(f"Total Global artists: {len(artists)}")
no_tilde = [a for a in artists if not a.endswith("~")]
print(f"Artists without tilde: {no_tilde}")
for a in artists[:20]:
    ap = os.path.join(ROOT, a)
    albums = os.listdir(ap) if os.path.isdir(ap) else []
    print(f"  {a} ({len(albums)} albums)")
