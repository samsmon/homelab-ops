import os
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

def get_prop(p):
    try:
        out = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', p], universal_newlines=True).strip().split()
        return f"{out[0]}Hz/{out[1]}bit, {os.path.getsize(p)} bytes"
    except Exception as e:
        return f"err: {e}"

files = [
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
    "Game/Idoly Pride (アイドリープライド) ~/Shining Days/01. Shining Days_alt.flac",
    "Game/Idoly Pride (アイドリープライド) ~/Daytime Moon/01. Daytime Moon_alt.flac",
    "Anime/Makeine (負けヒロインが多すぎる！) ~/つよがるガール/01. つよがるガール_dup.flac",
    "Anime/Spice and Wolf ~/In the Middle of a Journey/01. In the Middle of a Journey_alt.flac",
    "Anime/Spice and Wolf ~/Sign/01. Sign_dup.flac",
    "Anime/Revue Starlight (少女☆歌劇 レヴュースタァライト) ~/少女☆歌劇 レヴュースタァライト 舞台奏像劇 遙かなるエルドラド 劇中歌アルバム/Disc 1/08. LIFE IS LIKE A VOYAGE (香子×真矢ver.)_alt.flac"
]

for rel_f in files:
    fp_alt = os.path.join(ROOT, rel_f)
    base_rel = rel_f.replace("_alt.flac", ".flac").replace("_dup.flac", ".flac")
    fp_base = os.path.join(ROOT, base_rel)
    prop_alt = get_prop(fp_alt) if os.path.exists(fp_alt) else "NOT FOUND"
    prop_base = get_prop(fp_base) if os.path.exists(fp_base) else "NOT FOUND"
    print(f"Alt: {rel_f} ({prop_alt})\n  vs: {base_rel} ({prop_base})\n")
