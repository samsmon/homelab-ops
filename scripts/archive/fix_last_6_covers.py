import os

ROOT = "/mnt/hdd-backup/music/Lossless"

# 1. ONGEKI Starry
starry_png = os.path.join(ROOT, "Game/ONGEKI (オンゲキ) ~/ONGEKI Memorial Soundtrack Nexture 01「Starry」/not_so_cover.png")
if os.path.exists(starry_png):
    os.remove(starry_png)
    print("Removed not_so_cover.png in ONGEKI Starry")

# 2. Uma Musume large_cover.png
uma_beyond_png = os.path.join(ROOT, "Anime/Uma Musume (ウマ娘) ~/06. Singles, OST & Other/Beyond/large_cover.png")
if os.path.exists(uma_beyond_png):
    os.remove(uma_beyond_png)
    print("Removed large_cover.png in Uma Musume Beyond")

for wl in ["WINNING LIVE 32", "WINNING LIVE 33", "WINNING LIVE 35"]:
    p = os.path.join(ROOT, "Anime/Uma Musume (ウマ娘) ~/01. WINNING LIVE Series", wl, "large_cover.png")
    if os.path.exists(p):
        os.remove(p)
        print(f"Removed large_cover.png in {wl}")

# WINNING LIVE 34: large_cover.jpg is the optimized JPG (1.3MB), cover.png is 13.4MB
wl34_dir = os.path.join(ROOT, "Anime/Uma Musume (ウマ娘) ~/01. WINNING LIVE Series/WINNING LIVE 34")
wl34_png = os.path.join(wl34_dir, "cover.png")
wl34_jpg = os.path.join(wl34_dir, "large_cover.jpg")
if os.path.exists(wl34_png) and os.path.exists(wl34_jpg):
    os.remove(wl34_png)
    os.rename(wl34_jpg, os.path.join(wl34_dir, "Cover.jpg"))
    print("Cleaned WINNING LIVE 34 cover art")

print("All 6 cover anomalies fixed!")
