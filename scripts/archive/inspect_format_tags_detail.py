import os

ROOT = "/mnt/hdd-backup/music/Lossless"

folders_to_check = [
    "J-Pop/Kokuhaku Jikkouiinkai -flying Songs- Koishi Teru [48khz (告白実行委員会 -FLYING SONGS- 恋してる[48kHz) ~",
    "Doujinshi/Vivid Lila ~/WEB FLAC",
    "Game/O.N.G.E.K.I. (オンゲキ) ~/2022.11.30 [ZMCZ-15812] ONGEKI Vocal Memory [USB+CD-FLAC]",
    "Game/Kancolle (艦隊これくしょん -艦これ-) ~/艦隊これくしょん -艦これ-」キャラクターソング 艦娘乃歌 Vol.1 [WAV 48.0kHz-24bit]"
]

for rel in folders_to_check:
    fp = os.path.join(ROOT, rel)
    print(f"=== {rel} ===")
    if os.path.exists(fp):
        for r, d, f in os.walk(fp):
            print(f"  DIR: {r}")
            print(f"    dirs: {d}")
            print(f"    files: {f[:5]}")
    else:
        print("  DOES NOT EXIST")
