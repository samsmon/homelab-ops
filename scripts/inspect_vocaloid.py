import os

ROOT = "/mnt/hdd-backup/music/Lossless/Vocaloid"
producers = sorted(os.listdir(ROOT))
print(f"Total Vocaloid producers: {len(producers)}")
no_tilde = [p for p in producers if not p.endswith("~")]
print(f"Producers without tilde: {no_tilde}")
for p in producers[:20]:
    pp = os.path.join(ROOT, p)
    albums = os.listdir(pp) if os.path.isdir(pp) else []
    print(f"  {p} ({len(albums)} albums)")
