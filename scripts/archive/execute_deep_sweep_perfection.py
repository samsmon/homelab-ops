import os
import shutil
import unicodedata

ROOT = "/mnt/hdd-backup/music/Lossless"

print("==================================================================")
print("=== EXECUTING DEEP SWEEP & GAKUMAS PERFECTION ===")
print("==================================================================")

# -----------------------------------------------------------------
# 1. GAKUMAS PERFECTION
# -----------------------------------------------------------------
print("\n--- 1. GAKUMAS PERFECTION ---")
gakumas = os.path.join(ROOT, "Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~")

# 1a. Normalize NFD dakuten in Temari's album
temari_dir = os.path.join(gakumas, "01. Solo/02. 月村手毬 (Temari Tsukimura)")
if os.path.exists(temari_dir):
    for d in os.listdir(temari_dir):
        if "叶えたい" in d:
            nfc_d = unicodedata.normalize('NFC', d)
            if nfc_d != d:
                src = os.path.join(temari_dir, d)
                dst = os.path.join(temari_dir, nfc_d)
                print(f"Normalizing Unicode NFD->NFC: '{d}' -> '{nfc_d}'")
                os.rename(src, dst)

# 1b. Rename [1st Single CD-FLAC] -> [1st Single]
singles_to_rename = [
    ("01. Solo/01. 花海咲季 (Saki Hanami)", "Fighting My Way [1st Single CD-FLAC]", "Fighting My Way [1st Single]"),
    ("01. Solo/02. 月村手毬 (Temari Tsukimura)", "Luna say maybe [1st Single CD-FLAC]", "Luna say maybe [1st Single]"),
    ("01. Solo/03. 藤田ことね (Kotone Fujita)", "世界一可愛い私 [1st Single CD-FLAC]", "世界一可愛い私 [1st Single]")
]
for parent_sub, old_n, new_n in singles_to_rename:
    old_p = os.path.join(gakumas, parent_sub, old_n)
    new_p = os.path.join(gakumas, parent_sub, new_n)
    if os.path.exists(old_p):
        print(f"Renaming: '{old_n}' -> '{new_n}'")
        os.rename(old_p, new_p)

# 1c. Kotone's かちドキ: Merge BK from 16-bit CD-FLAC into 24-bit Hi-Res, then purge 16-bit folder
kotone_dir = os.path.join(gakumas, "01. Solo/03. 藤田ことね (Kotone Fujita)")
kachi_cd = os.path.join(kotone_dir, "かちドキ [GOLD RUSH CD-FLAC]")
kachi_hires = os.path.join(kotone_dir, "かちドキ")
if os.path.exists(kachi_cd) and os.path.exists(kachi_hires):
    bk_src = os.path.join(kachi_cd, "BK")
    bk_dst = os.path.join(kachi_hires, "BK")
    if os.path.exists(bk_src):
        print("Moving BK from かちドキ [GOLD RUSH CD-FLAC] to かちドキ...")
        shutil.move(bk_src, bk_dst)
    print("Purging redundant 16-bit かちドキ [GOLD RUSH CD-FLAC]...")
    shutil.rmtree(kachi_cd)

# 1d. Kotone's GO MY WAY!! from GOLD RUSH 第3巻: Move from All Stars to Kotone Solo
gr3_src = os.path.join(gakumas, "04. All Stars & Units/GOLD RUSH 第3巻 オリジナルCD付き特装版")
gr3_dst = os.path.join(kotone_dir, "GOLD RUSH 第3巻 特装版「GO MY WAY!!」")
if os.path.exists(gr3_src):
    print("Relocating Kotone's GO MY WAY!! from 04. All Stars & Units to 01. Solo/03. 藤田ことね...")
    shutil.move(gr3_src, gr3_dst)

# 1e. Purge all 16-bit _alt.flac files in Gakumas
gakumas_alt_dirs = [
    "01. Solo/03. 藤田ことね (Kotone Fujita)/かちドキ",
    "01. Solo/10. 花海佑芽 (Ume Hanami)/真っ白いページと水彩の主人公",
    "01. Solo/11. 秦谷美鈴 (Misuzu Hataya)/Superlative",
    "01. Solo/11. 秦谷美鈴 (Misuzu Hataya)/VEIL",
    "01. Solo/13. 雨夜燕 (Tsubame Amaya)/MY STAGE",
    "01. Solo/13. 雨夜燕 (Tsubame Amaya)/三分半の創世",
    "04. All Stars & Units/ガラクタロード"
]
for ad in gakumas_alt_dirs:
    ad_p = os.path.join(gakumas, ad)
    if os.path.exists(ad_p):
        for f in os.listdir(ad_p):
            if "_alt.flac" in f:
                fp = os.path.join(ad_p, f)
                print(f"Removing Gakumas 16-bit duplicate: {ad}/{f}")
                os.remove(fp)

# -----------------------------------------------------------------
# 2. BANG DREAM! QUALITY UPGRADES
# -----------------------------------------------------------------
print("\n--- 2. BANG DREAM! QUALITY UPGRADES ---")
# 2a. MyGO!!!!! 3rd Album: Replace 16-bit with 24-bit 96kHz _alt
mygo_dir = os.path.join(ROOT, "Anime/BanG Dream! (バンドリ！) ~/MyGO!!!!! ~/BanG Dream! MyGO!!!!! 3rdアルバム「致並跡」")
if os.path.exists(mygo_dir):
    for f in list(os.listdir(mygo_dir)):
        if f.endswith("_alt.flac"):
            base_f = f.replace("_alt.flac", ".flac")
            base_p = os.path.join(mygo_dir, base_f)
            alt_p = os.path.join(mygo_dir, f)
            if os.path.exists(base_p):
                os.remove(base_p)
            os.rename(alt_p, base_p)
            print(f"Upgraded MyGO track to 24-bit Hi-Res: {base_f}")

# 2b. Mugendai Mewtype 4th Single: Replace 16-bit with 24-bit 96kHz _alt
mew_dir = os.path.join(ROOT, "Anime/BanG Dream! (バンドリ！) ~/Mugendai Mewtype (夢限大みゅーたいぷ) ~/BanG Dream! 夢限大みゅーたいぷ 4thシングル「超惑星Xへの旅」")
if os.path.exists(mew_dir):
    for f in list(os.listdir(mew_dir)):
        if f.endswith("_alt.flac"):
            base_f = f.replace("_alt.flac", ".flac")
            base_p = os.path.join(mew_dir, base_f)
            alt_p = os.path.join(mew_dir, f)
            if os.path.exists(base_p):
                os.remove(base_p)
            os.rename(alt_p, base_p)
            print(f"Upgraded Mugendai Mewtype track to 24-bit Hi-Res: {base_f}")

# -----------------------------------------------------------------
# 3. TUYU QUALITY UPGRADES
# -----------------------------------------------------------------
print("\n--- 3. TUYU QUALITY UPGRADE ---")
tuyu_dir = os.path.join(ROOT, "J-Pop/TUYU (ツユ) ~/アンダーメンタリティ")
if os.path.exists(tuyu_dir):
    for f in list(os.listdir(tuyu_dir)):
        if f.endswith("_dup.flac"):
            base_f = f.replace("_dup.flac", ".flac")
            base_p = os.path.join(tuyu_dir, base_f)
            dup_p = os.path.join(tuyu_dir, f)
            if os.path.exists(base_p):
                os.remove(base_p)
            os.rename(dup_p, base_p)
            print(f"Upgraded TUYU track to 24-bit Hi-Res: {base_f}")
    if os.path.exists(os.path.join(tuyu_dir, "cover_dup.jpg")):
        cov_base = os.path.join(tuyu_dir, "cover.jpg")
        cov_dup = os.path.join(tuyu_dir, "cover_dup.jpg")
        if os.path.exists(cov_base):
            os.remove(cov_base)
        os.rename(cov_dup, cov_base)
        print("Upgraded TUYU cover to Hi-Res cover.jpg")

# -----------------------------------------------------------------
# 4. PURGE REDUNDANT _alt, _dup, cover_dup.jpg
# -----------------------------------------------------------------
print("\n--- 4. PURGE REDUNDANT _alt, _dup, cover_dup.jpg ---")
files_to_remove = [
    # Liella Hyper Glowing 16-bit alts
    "Anime/Love Live! (ラブライブ！) ~/Liella! (ラブライブ！スーパースター!!) ~/ラブライブ！スーパースター!! Liella!と結ぶプロジェクト ミニアルバム「Hyper Glowing!」/01. Hyper Glowing!_alt.flac",
    "Anime/Love Live! (ラブライブ！) ~/Liella! (ラブライブ！スーパースター!!) ~/ラブライブ！スーパースター!! Liella!と結ぶプロジェクト ミニアルバム「Hyper Glowing!」/02. トクベツじゃない魔法_alt.flac",
    "Anime/Love Live! (ラブライブ！) ~/Liella! (ラブライブ！スーパースター!!) ~/ラブライブ！スーパースター!! Liella!と結ぶプロジェクト ミニアルバム「Hyper Glowing!」/03. Winds of YELL_alt.flac",
    "Anime/Love Live! (ラブライブ！) ~/Liella! (ラブライブ！スーパースター!!) ~/ラブライブ！スーパースター!! Liella!と結ぶプロジェクト ミニアルバム「Hyper Glowing!」/04. 芽生え_alt.flac",
    # Shiny Colors 2nd Season Over the prism
    "Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/03. Anime Series/TVアニメ「アイドルマスター シャイニーカラーズ 2nd Season」主題歌アルバム「Over the prism」/Disc 1/06. さあ舞い上がれ_alt.flac",
    # Utahime Dream duplicates
    "Anime/Utahime Dream (ウタヒメドリーム) ~/AMBITION/01. AMBITION_dup.flac",
    "Anime/Utahime Dream (ウタヒメドリーム) ~/AMBITION/Cover_dup.jpg",
    "Anime/Utahime Dream (ウタヒメドリーム) ~/TVアニメ「無自覚聖女は今日も無意識に力を垂れ流す」EDテーマ「アンノウンミー」／ウタヒメドリーム オールスターズ/01. アンノウンミー_dup.flac",
    # Senpai wa Otokonoko & Narenare covers
    "Anime/Senpai wa Otokonoko (先輩はおとこのこ) ~/先輩はおとこのこ/Cover_dup.jpg",
    "Anime/Narenare (菜なれ花なれ) ~/菜なれ花なれ/Cover_dup.jpg",
    # J-Pop duplicate tracks & covers
    "J-Pop/Hanabie. (花冷え。) ~/TVアニメ「対ありでした。 ～お嬢さまは格闘ゲームなんてしない～」OPテーマ「命短し対する乙女よ」／花冷え。/01. 命短し対する乙女よ_dup.flac",
    "J-Pop/PassCode ~/Liberator/01. Liberator_dup.flac",
    "J-Pop/Kaya (花耶) ~/TVアニメ「ヘルモード ～やり込み好きのゲーマーは廃設定の異世界で無双する～」EDテーマ「Sanctuary」／花耶/01. Sanctuary_dup.flac",
    "J-Pop/Various Artists ~/雪花繚乱/01. 雪花繚乱_dup.flac",
    "J-Pop/Various Artists ~/雪花繚乱/cover_dup.jpg",
    "J-Pop/Yuki Tanaka (田中有紀) ~/I need/01. I need_dup.flac",
    "J-Pop/Riria . (りりあ。) ~/軌跡/10. 色彩_alt.flac",
    "J-Pop/Maejima Ami (前島亜美) ~/Determination/前島亜美 1stアルバム「Determination」/03. SCARLET LOVE_alt.flac",
    "J-Pop/Maejima Ami (前島亜美) ~/Determination/前島亜美 1stアルバム「Determination」/06. MAKE IT NOW_alt.flac"
]

for rel_f in files_to_remove:
    fp = os.path.join(ROOT, rel_f)
    if os.path.exists(fp):
        os.remove(fp)
        print(f"Purged redundant file: {rel_f}")

# Flatten Maejima Ami nested album folder
maejima_parent = os.path.join(ROOT, "J-Pop/Maejima Ami (前島亜美) ~/Determination")
maejima_nested = os.path.join(maejima_parent, "前島亜美 1stアルバム「Determination」")
if os.path.exists(maejima_nested):
    print("Flattening Maejima Ami nested folder...")
    maejima_target = os.path.join(ROOT, "J-Pop/Maejima Ami (前島亜美) ~/前島亜美 1stアルバム「Determination」")
    shutil.move(maejima_nested, maejima_target)
    if os.path.exists(maejima_parent) and not os.listdir(maejima_parent):
        os.rmdir(maejima_parent)

# -----------------------------------------------------------------
# 5. STRIP FORMAT TAG NOISE [AIFF 96kHz／32bit] IN SHINY COLORS
# -----------------------------------------------------------------
print("\n--- 5. STRIP FORMAT NOISE IN SHINY COLORS ---")
sc_root = os.path.join(ROOT, "Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~")
if os.path.exists(sc_root):
    for r, d, f in os.walk(sc_root):
        for dir_name in list(d):
            if " [AIFF 96kHz／32bit]" in dir_name:
                clean_name = dir_name.replace(" [AIFF 96kHz／32bit]", "")
                old_p = os.path.join(r, dir_name)
                new_p = os.path.join(r, clean_name)
                print(f"Stripping tag: '{dir_name}' -> '{clean_name}'")
                os.rename(old_p, new_p)

# -----------------------------------------------------------------
# 6. PURGE EMPTY DIRECTORIES
# -----------------------------------------------------------------
print("\n--- 6. PURGE RESIDUAL EMPTY DIRECTORIES ---")
empty_dirs_to_purge = [
    os.path.join(ROOT, "_corrupted_quarantine/2026.02.28_FLAC_48kHz_24bit ~"),
    os.path.join(ROOT, "_corrupted_quarantine/2026.03.05_WebOP_FLAC_48kHz_24bit ~"),
    os.path.join(ROOT, "_corrupted_quarantine"),
    os.path.join(ROOT, "J-Pop/YUI ~/FROM ME TO YOU/Scans"),
    os.path.join(ROOT, "Doujinshi/Eufolie ~")
]

for ed in empty_dirs_to_purge:
    if os.path.exists(ed):
        try:
            if os.path.isdir(ed) and not os.listdir(ed):
                os.rmdir(ed)
                print(f"Removed empty dir: {ed}")
            elif os.path.isdir(ed):
                shutil.rmtree(ed)
                print(f"Removed directory tree: {ed}")
        except Exception as e:
            print(f"Error removing {ed}: {e}")

print("\n==================================================================")
print("=== DEEP SWEEP & GAKUMAS PERFECTION COMPLETED ===")
print("==================================================================")
