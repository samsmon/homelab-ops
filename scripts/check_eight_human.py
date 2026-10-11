import os
from mutagen.flac import FLAC

for path in [
    '/mnt/hdd-backup/music/Lossless/Vocaloid/Hachioji P (八王子P) ~/Eight -THE BEST OF 八王子P-/Disc 1/01 気まぐれメルシィ feat. 初音ミク.flac',
    '/mnt/hdd-backup/music/Lossless/Vocaloid/PinocchioP ~/HUMAN/Disc 1/01 ニッポンの夜明け.flac'
]:
    f = FLAC(path)
    print(path, 'embedded art count:', len(f.pictures))
    if f.pictures:
        pic = f.pictures[0]
        print(f"  mime={pic.mime}, type={pic.type}, bytes={len(pic.data)}")
