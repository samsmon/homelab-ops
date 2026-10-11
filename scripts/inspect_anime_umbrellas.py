import os

ROOT = "/mnt/hdd-backup/music/Lossless/Anime"
items = sorted(os.listdir(ROOT))
print(f"Total Anime items: {len(items)}")
no_tilde = [i for i in items if not i.endswith("~")]
print(f"Items without tilde: {no_tilde}")
for i in items[:25]:
    ip = os.path.join(ROOT, i)
    sub = os.listdir(ip) if os.path.isdir(ip) else []
    print(f"  {i} ({len(sub)} items)")
if len(items) > 25:
    print(f"  ... and {len(items)-25} more.")
