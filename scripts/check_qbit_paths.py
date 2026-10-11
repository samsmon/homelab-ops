import glob
import re

files = glob.glob('/var/lib/docker/volumes/qbittorrent_config/_data/qBittorrent/BT_backup/*.fastresume')
print(f"Total fastresume files: {len(files)}")

paths = set()
names = []

for f in files:
    try:
        with open(f, 'rb') as fp:
            data = fp.read().decode('latin1', errors='ignore')
            m = re.search(r'save_path\d+:([^:]+?)(?:seed_mode|total_downloaded|qBt-|\d+:)', data)
            if m:
                paths.add(m.group(1))
            m_name = re.search(r'4:name\d+:([^\d]+)', data)
            if m_name:
                names.append((m_name.group(1)[:40], m.group(1) if m else 'unknown'))
    except Exception as e:
        pass

print("Distinct save_paths in qBittorrent:")
for p in sorted(paths):
    print(" -", p)

print(f"\nSample 10 torrents and their targets:")
for n, p in names[:10]:
    print(f" - {n} -> {p}")
