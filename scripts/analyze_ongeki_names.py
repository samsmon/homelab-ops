import os
import re

d1 = "/mnt/hdd-backup/music/Lossless/Game/O.N.G.E.K.I. (オンゲキ) ~"

for item in sorted(os.listdir(d1)):
    # check if YYYY.MM.DD prefix
    clean = item
    m = re.match(r'^\d{4}\.\d{2}\.\d{2}\s+(?:\[(.*?)\]\s+)?(.*)$', item)
    if m:
        cat = m.group(1)
        title = m.group(2)
        if cat:
            clean = f"{title} {{{cat}}}"
        else:
            clean = title
    print(f"'{item}' -> '{clean}'")
