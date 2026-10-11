import os

ROOT = "/mnt/hdd-backup/music/Lossless/Doujinshi"
circles = sorted(os.listdir(ROOT))
print(f"Total Doujinshi circles: {len(circles)}")
no_tilde = [c for c in circles if not c.endswith("~")]
print(f"Circles without tilde: {no_tilde}")
for c in circles[:20]:
    cp = os.path.join(ROOT, c)
    albums = os.listdir(cp) if os.path.isdir(cp) else []
    print(f"  {c} ({len(albums)} albums)")
