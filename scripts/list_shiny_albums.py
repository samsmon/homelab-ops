import os
import sys

root = r"/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~/シャイニーカラーズ"
albums = []
for r, dirs, files in os.walk(root):
    for d in dirs:
        if d.startswith('[') and any(d[1:3] == yr for yr in ['18', '19', '20', '21', '22', '23', '24', '25', '26']):
            albums.append(d)

print(f"COUNT={len(albums)}")
for a in sorted(albums):
    print(a)
