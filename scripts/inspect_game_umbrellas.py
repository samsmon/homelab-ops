import os

ROOT = "/mnt/hdd-backup/music/Lossless/Game"
items = sorted(os.listdir(ROOT))
print(f"Total Game items: {len(items)}")
no_tilde = [i for i in items if not i.endswith("~")]
print(f"Items without tilde: {no_tilde}")
for i in items:
    ip = os.path.join(ROOT, i)
    sub = os.listdir(ip) if os.path.isdir(ip) else []
    print(f"  {i} ({len(sub)} items)")
