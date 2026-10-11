import os

ROOT = "/mnt/hdd-backup/music/Lossless/Vtuber"
agencies = sorted(os.listdir(ROOT))
print(f"Total Vtuber agencies/indies: {len(agencies)}")
no_tilde = [a for a in agencies if not a.endswith("~")]
print(f"Agencies without tilde: {no_tilde}")
for a in agencies:
    ap = os.path.join(ROOT, a)
    items = os.listdir(ap) if os.path.isdir(ap) else []
    print(f"  {a} ({len(items)} items)")
