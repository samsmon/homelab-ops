import os
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=== HTML FILES ===")
html_files = []
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith(('.html', '.htm')):
            html_files.append(os.path.join(root, f))
for h in html_files:
    print(f"  {os.path.relpath(h, ROOT)}")

print("\n=== BDMV FILES ===")
bdmv_files = []
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith('.bdmv'):
            bdmv_files.append(os.path.join(root, f))
for b in bdmv_files:
    print(f"  {os.path.relpath(b, ROOT)}")

print("\n=== TAG CASE CHECK ON SAMPLE ===")
sample = "/mnt/hdd-backup/music/Lossless/Anime/NEW GAME! (ニューゲーム!) ~/NEW GAME! CHARACTER SONG CD/NEW GAME! CHARACTER SONG CD Lv.1/01. Shunshoku Runway.flac"
if os.path.exists(sample):
    r = subprocess.run(["metaflac", "--export-tags-to=-", sample], capture_output=True, text=True)
    print("Tags for 01. Shunshoku Runway.flac:")
    print(r.stdout.strip())
