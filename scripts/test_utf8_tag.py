import os
import subprocess

fp = "/mnt/hdd-backup/music/Lossless/Vtuber/La Prière ~/純情アンビバレンス/純情アンビバレンス.flac"

# First remove existing TITLE tags
subprocess.run(["metaflac", "--remove-tag=TITLE", fp])

# Now import UTF-8 tag
tag_file = "/tmp/tag_test.txt"
with open(tag_file, "w", encoding="utf-8") as f:
    f.write("TITLE=純情アンビバレンス\n")

env = os.environ.copy()
env["LC_ALL"] = "C.UTF-8"
env["LANG"] = "C.UTF-8"

subprocess.run(["metaflac", f"--import-tags-from={tag_file}", fp], env=env)

# Export and check
r = subprocess.run(["metaflac", "--export-tags-to=-", fp], env=env, capture_output=True, text=True)
print("Exported tags:")
print(r.stdout)
