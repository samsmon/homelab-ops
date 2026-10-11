import os
import subprocess

def get_tags(folder):
    tags = []
    if not os.path.exists(folder):
        return [f"Folder does not exist: {folder}"]
    for f in os.listdir(folder):
        if f.endswith('.flac'):
            fp = os.path.join(folder, f)
            try:
                out = subprocess.check_output(['metaflac', '--show-tag=ARTIST', '--show-tag=ALBUM', fp], universal_newlines=True).strip()
                tags.append(f"{f}: {out}")
            except Exception as e:
                tags.append(f"{f}: error {e}")
    return tags

print("=== Sa Na vs Sana ===")
for t in get_tags("/mnt/hdd-backup/music/Lossless/J-Pop/Sa Na (紗奈) ~/KISSIN' CLAW (AIRY STEPS)"):
    print("  ", t)
for t in get_tags("/mnt/hdd-backup/music/Lossless/J-Pop/Sana (鎖那) ~/CLOUD HAIRPIN"):
    print("  ", t)

print("\n=== Su Mi Ka vs sumika ===")
for t in get_tags("/mnt/hdd-backup/music/Lossless/J-Pop/Su Mi Ka (す み か) ~/花笑む"):
    print("  ", t)
for t in get_tags("/mnt/hdd-backup/music/Lossless/J-Pop/sumika ~/Honto"):
    print("  ", t)
