import os

ROOT = "/mnt/hdd-backup/music/Lossless"

files_to_purge = [
    "Vtuber/Nanami Urara (七海うらら) ~/Kiss and Cry/10. Love and Hate_alt.flac",
    "Vtuber/Nanami Urara (七海うらら) ~/Kiss and Cry/03. パラレル☆ショータイム_alt.flac",
    "Vtuber/Nanami Urara (七海うらら) ~/Kiss and Cry/01. Kiss and Cry_alt.flac",
    "Vtuber/Nanami Urara (七海うらら) ~/Kiss and Cry/13. ダイヤノカガヤキ_alt.flac",
    "Vtuber/Nanami Urara (七海うらら) ~/Kiss and Cry/06. キワメテカワイイ_alt.flac",
    "Vtuber/Hololive (ホロライブ) ~/Ookami Mio (大神ミオ) ~/小心旅行/01. 小心旅行_alt.flac",
    "Vtuber/Hololive (ホロライブ) ~/Ookami Mio (大神ミオ) ~/小心旅行/02. 小心旅行 (Instrumental)_alt.flac",
    "Vtuber/Hololive (ホロライブ) ~/Sakura Miko (さくらみこ) ~/サキミダレアッパレード♪/02. サキミダレアッパレード♪ (Instrumental)_alt.flac",
    "Vtuber/Hololive (ホロライブ) ~/Sakura Miko (さくらみこ) ~/サキミダレアッパレード♪/01. サキミダレアッパレード♪_alt.flac",
    "Vtuber/Hololive (ホロライブ) ~/Takane Lui (鷹嶺ルイ) ~/DARE!？/02. DARE!？ (Instrumental)_alt.flac",
    "Vtuber/Hololive (ホロライブ) ~/Takane Lui (鷹嶺ルイ) ~/DARE!？/01. DARE!？_alt.flac",
    "Vtuber/Hololive (ホロライブ) ~/Shirakami Fubuki (白上フブキ) ~/白上フブキ 1stアルバム「FBKINGDOM “Blessing”」/01. SUPERNOVA_alt.flac",
    "Game/Idoly Pride (アイドリープライド) ~/Shining Days/Cover_alt.jpg",
    "Game/Idoly Pride (アイドリープライド) ~/Shining Days/01. Shining Days_alt.flac",
    "Game/Idoly Pride (アイドリープライド) ~/Daytime Moon/01. Daytime Moon_alt.flac",
    "Game/Idoly Pride (アイドリープライド) ~/Daytime Moon/Cover_alt.jpg",
    "Anime/Makeine (負けヒロインが多すぎる！) ~/つよがるガール/Cover_dup.jpg",
    "Anime/Makeine (負けヒロインが多すぎる！) ~/つよがるガール/01. つよがるガール_dup.flac",
    "Anime/Spice and Wolf ~/In the Middle of a Journey/01. In the Middle of a Journey_alt.flac",
    "Anime/Spice and Wolf ~/Sign/01. Sign_dup.flac",
    "Anime/Revue Starlight (少女☆歌劇 レヴュースタァライト) ~/少女☆歌劇 レヴュースタァライト 舞台奏像劇 遙かなるエルドラド 劇中歌アルバム/Disc 1/08. LIFE IS LIKE A VOYAGE (香子×真矢ver.)_alt.flac"
]

print("=== PURGING REMAINING 21 REDUNDANT DUP/ALT FILES ===")
count = 0
for rel_f in files_to_purge:
    fp = os.path.join(ROOT, rel_f)
    if os.path.exists(fp):
        os.remove(fp)
        print(f"Purged: {rel_f}")
        count += 1
print(f"Total purged: {count}")
