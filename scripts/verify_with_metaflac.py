import subprocess
import os

sample_files = [
    "/mnt/hdd-backup/music/Lossless/Vtuber/La Prière ~/純情アンビバレンス/純情アンビバレンス.flac",
    "/mnt/hdd-backup/music/Lossless/Vtuber/La Prière ~/純情アンビバレンス/純情アンビバレンス（Instrumental）.flac",
    "/mnt/hdd-backup/music/Lossless/Vtuber/Natsume Itsuki (棗いつき) ~/Elis Dogma/00-04-Knightmare.flac",
    "/mnt/hdd-backup/music/Lossless/Vtuber/Natsume Itsuki (棗いつき) ~/Elis Dogma/00-06-Checkmate.flac",
    "/mnt/hdd-backup/music/Lossless/Vtuber/Aitsuki Nakuru (藍月なくる) ~/トコロクラニスト/02. 今.flac",
    "/mnt/hdd-backup/music/Lossless/Vtuber/Aitsuki Nakuru (藍月なくる) ~/トコロクラニスト/05. シーサイド.flac"
]

env = os.environ.copy()
env["LC_ALL"] = "C.UTF-8"
env["LANG"] = "C.UTF-8"

print("Checking tags via metaflac with UTF-8 locale:")
for f in sample_files:
    r = subprocess.run(["metaflac", "--show-tag=TITLE", f], env=env, capture_output=True, text=True)
    print(f"  {os.path.basename(f)}: '{r.stdout.strip()}'")
