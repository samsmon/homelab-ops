import os
import shutil

LOSSLESS = "/mnt/hdd-backup/music/Lossless"
LOSSY = "/mnt/hdd-backup/music/Lossy"

print("=" * 60)
print("STARTING ROUND 154 EXECUTION")
print("=" * 60)

# Phase 1: Rescue FLAC album
src_flac_dir = os.path.join(LOSSY, "Doujinshi", "IOSYS (イオシス) - IOSYS TOHO MEGAMIX - GENSOKYO HOUSE EDITION", "IOSYS - スカーレット警察・総集編 春の特別警戒スペシャル")
dst_flac_dir = os.path.join(LOSSLESS, "Doujinshi", "IOSYS (イオシス) ~", "スカーレット警察・総集編 春の特別警戒スペシャル")

if os.path.exists(src_flac_dir):
    os.makedirs(dst_flac_dir, exist_ok=True)
    for item in os.listdir(src_flac_dir):
        shutil.move(os.path.join(src_flac_dir, item), os.path.join(dst_flac_dir, item))
    os.rmdir(src_flac_dir)
    print(f"Rescued 11 FLAC tracks to {dst_flac_dir}")
else:
    print(f"Source FLAC album not found: {src_flac_dir}")

# Phase 2: Purge redundant MP3 copy of GENSOKYO HOUSE EDITION
parent_lossy = os.path.join(LOSSY, "Doujinshi", "IOSYS (イオシス) - IOSYS TOHO MEGAMIX - GENSOKYO HOUSE EDITION")
if os.path.exists(parent_lossy):
    shutil.rmtree(parent_lossy)
    print("Purged redundant MP3 copy of GENSOKYO HOUSE EDITION from Lossy")

# Phase 3: Purge TrackList.htm
htm_file = os.path.join(LOSSY, "Doujinshi", "実谷ななゴールデンベスト -ボカロ曲を歌ってみた-", "TrackList.htm")
if os.path.exists(htm_file):
    os.remove(htm_file)
    print("Purged clutter TrackList.htm")

print("\nROUND 154 EXECUTION FINISHED!")
