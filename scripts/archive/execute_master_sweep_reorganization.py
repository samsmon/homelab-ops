#!/usr/bin/env python3
import os
import shutil
import sys

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

def safe_merge_dir(src, dst):
    """Safely merges contents of src into dst, creating dst if needed."""
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s_item = os.path.join(src, item)
        d_item = os.path.join(dst, item)
        if os.path.isdir(s_item):
            if os.path.exists(d_item):
                safe_merge_dir(s_item, d_item)
                if os.path.exists(s_item) and not os.listdir(s_item):
                    os.rmdir(s_item)
            else:
                shutil.move(s_item, d_item)
        else:
            if not os.path.exists(d_item):
                shutil.move(s_item, d_item)
            else:
                # File exists, compare size
                if os.path.getsize(s_item) == os.path.getsize(d_item):
                    os.remove(s_item)
                else:
                    # Rename slightly to avoid overwrite loss
                    base, ext = os.path.splitext(item)
                    shutil.move(s_item, os.path.join(dst, f"{base}_dup{ext}"))
    if os.path.exists(src) and not os.listdir(src):
        os.rmdir(src)

def execute_reorganization():
    print("=" * 80)
    print("EXECUTING MASTER SWEEP REORGANIZATION")
    print("=" * 80)

    # ---------------------------------------------------------
    # 1. EVACUATE CONTAMINATION IN J-Pop/tuki. ~
    # ---------------------------------------------------------
    print("\n[STEP 1] Evacuating contamination in J-Pop/tuki. ~ ...")
    tuki_dir = os.path.join(BASE_DIR, "J-Pop", "tuki. ~")
    
    # 1a. D4DJ RONDO
    rondo_src = os.path.join(tuki_dir, "D4DJ 燐舞曲 メモリアルアルバム「-未来-」")
    rondo_dst = os.path.join(BASE_DIR, "Anime", "D4DJ (ディーフォーディージェー) ~", "RONDO (燐舞曲) ~", "メモリアルアルバム「-未来-」")
    if os.path.exists(rondo_src):
        print(f"  Moving D4DJ Rondo: {rondo_src} -> {rondo_dst}")
        os.makedirs(os.path.dirname(rondo_dst), exist_ok=True)
        safe_merge_dir(rondo_src, rondo_dst)
        if os.path.exists(rondo_src) and not os.listdir(rondo_src):
            os.rmdir(rondo_src)

    # 1b. Akari Kito
    kito_src = os.path.join(tuki_dir, "Journey")
    kito_dst = os.path.join(BASE_DIR, "J-Pop", "Akari Kito (鬼頭明里) ~", "Journey")
    if os.path.exists(kito_src):
        print(f"  Moving Kito Akari: {kito_src} -> {kito_dst}")
        safe_merge_dir(kito_src, kito_dst)
        if os.path.exists(kito_src) and not os.listdir(kito_src):
            os.rmdir(kito_src)

    # 1c. Riria.
    riria_src = os.path.join(tuki_dir, "軌跡")
    riria_dst = os.path.join(BASE_DIR, "J-Pop", "Riria . (りりあ。) ~", "軌跡")
    if os.path.exists(riria_src):
        print(f"  Moving Riria.: {riria_src} -> {riria_dst}")
        safe_merge_dir(riria_src, riria_dst)
        if os.path.exists(riria_src) and not os.listdir(riria_src):
            os.rmdir(riria_src)

    # 1d. TrySail in tuki. ~ -> Move & flatten into J-Pop/TrySail (トライセイル) ~
    trysail_tuki = os.path.join(tuki_dir, "TrySail トライセイル (麻倉もも・雨宮天・夏川椎菜) (2015-2023)")
    trysail_target = os.path.join(BASE_DIR, "J-Pop", "TrySail (トライセイル) ~")
    if os.path.exists(trysail_tuki):
        print(f"  Dismantling and moving TrySail -> {trysail_target}")
        os.makedirs(trysail_target, exist_ok=True)
        for era in os.listdir(trysail_tuki):
            era_path = os.path.join(trysail_tuki, era)
            if os.path.isdir(era_path):
                for album in os.listdir(era_path):
                    album_path = os.path.join(era_path, album)
                    clean_name = album
                    if clean_name.startswith("TrySail｜"):
                        clean_name = clean_name.replace("TrySail｜", "")
                    clean_name = clean_name.replace(" ・ ", "・").strip()
                    dst_album = os.path.join(trysail_target, clean_name)
                    safe_merge_dir(album_path, dst_album)
                    if os.path.exists(album_path) and not os.listdir(album_path):
                        os.rmdir(album_path)
                if os.path.exists(era_path) and not os.listdir(era_path):
                    os.rmdir(era_path)
        if os.path.exists(trysail_tuki):
            shutil.rmtree(trysail_tuki)

    # ---------------------------------------------------------
    # 2. HIBANA LOOSE TRACKS
    # ---------------------------------------------------------
    print("\n[STEP 2] Wrapping loose tracks in J-Pop/Hibana (ヒバナ) ~ ...")
    hibana_dir = os.path.join(BASE_DIR, "J-Pop", "Hibana (ヒバナ) ~")
    if os.path.exists(hibana_dir):
        for f in sorted(os.listdir(hibana_dir)):
            if f.endswith('.flac') and f.startswith('01_01_'):
                song_name = f.replace('01_01_', '').replace('.flac', '').strip()
                album_folder = os.path.join(hibana_dir, song_name)
                os.makedirs(album_folder, exist_ok=True)
                track_dst = os.path.join(album_folder, f"01. {song_name}.flac")
                print(f"  Wrapping {f} -> {album_folder}/01. {song_name}.flac")
                shutil.move(os.path.join(hibana_dir, f), track_dst)

    # ---------------------------------------------------------
    # 3. DEFORMED ARTIST FOLDERS & WHITE ALBUM 2
    # ---------------------------------------------------------
    print("\n[STEP 3] Normalizing deformed artist folders & moving White Album 2 ...")
    # White Album 2 -> Game/WHITE ALBUM2 (ホワイトアルバム2) ~
    wa2_src = os.path.join(BASE_DIR, "Anime", "White Album2 (Howaitoarubamu 2) (WHITE ALBUM2 (ホワイトアルバム2)) ~")
    wa2_dst = os.path.join(BASE_DIR, "Game", "WHITE ALBUM2 (ホワイトアルバム2) ~")
    if os.path.exists(wa2_src):
        print(f"  Moving White Album 2: {wa2_src} -> {wa2_dst}")
        safe_merge_dir(wa2_src, wa2_dst)
        if os.path.exists(wa2_src):
            shutil.rmtree(wa2_src)

    # Toyama Nao
    toyo_src = os.path.join(BASE_DIR, "J-Pop", "T Shou Yama Nao 東山 Go (Tōyama Nao 東山奈央) ~")
    toyo_dst = os.path.join(BASE_DIR, "J-Pop", "Touyama Nao (東山奈央) ~")
    if os.path.exists(toyo_src):
        print(f"  Flattening and renaming Toyama Nao -> {toyo_dst}")
        nemuri_path = os.path.join(toyo_src, "[Nemuri] Tōyama Nao 東山奈央 (2017-2023)")
        if os.path.exists(nemuri_path):
            for era in os.listdir(nemuri_path):
                era_path = os.path.join(nemuri_path, era)
                if os.path.isdir(era_path):
                    for alb in os.listdir(era_path):
                        alb_path = os.path.join(era_path, alb)
                        clean_alb = alb.replace("東山奈央｜", "").strip()
                        safe_merge_dir(alb_path, os.path.join(toyo_src, clean_alb))
                        if os.path.exists(alb_path) and not os.listdir(alb_path):
                            os.rmdir(alb_path)
                if os.path.exists(era_path) and not os.listdir(era_path):
                    os.rmdir(era_path)
            if os.path.exists(nemuri_path):
                shutil.rmtree(nemuri_path)
        safe_merge_dir(toyo_src, toyo_dst)
        if os.path.exists(toyo_src):
            shutil.rmtree(toyo_src)

    # Sakurarium
    sakura_src = os.path.join(BASE_DIR, "J-Pop", "Sakurariumu ( Yuu Nagi Michiru ) (yunagi Michiru) (サクラリウム (夕凪みちる) (Yunagi Michiru)) ~")
    sakura_dst = os.path.join(BASE_DIR, "J-Pop", "Sakurarium (サクラリウム) ~")
    if os.path.exists(sakura_src):
        print(f"  Renaming Sakurarium -> {sakura_dst}")
        safe_merge_dir(sakura_src, sakura_dst)
        if os.path.exists(sakura_src):
            shutil.rmtree(sakura_src)

    # Nohana Koyori
    koyori_src = os.path.join(BASE_DIR, "J-Pop", "Kokoro Hana Gaku ( No Hana Koyori ) (心花学 (乃花こより)) ~")
    koyori_dst = os.path.join(BASE_DIR, "J-Pop", "Nohana Koyori (乃花こより) ~")
    if os.path.exists(koyori_src):
        print(f"  Renaming Nohana Koyori -> {koyori_dst}")
        safe_merge_dir(koyori_src, koyori_dst)
        if os.path.exists(koyori_src):
            shutil.rmtree(koyori_src)

    # Kozue Kisaragi
    kozue_src = os.path.join(BASE_DIR, "J-Pop", "Kisaragi Kozue (priere * ) (如月梢 (Priere＊)) ~")
    kozue_dst = os.path.join(BASE_DIR, "J-Pop", "Kozue Kisaragi (如月梢) ~")
    if os.path.exists(kozue_src):
        print(f"  Renaming Kozue Kisaragi -> {kozue_dst}")
        safe_merge_dir(kozue_src, kozue_dst)
        if os.path.exists(kozue_src):
            shutil.rmtree(kozue_src)

    # Lampcat
    lamp_src = os.path.join(BASE_DIR, "Doujinshi", "Lampcat ?? Shitai Ron (Lampcat ─ 死体論) ~")
    lamp_dst = os.path.join(BASE_DIR, "Doujinshi", "Lampcat ~")
    if os.path.exists(lamp_src):
        print(f"  Renaming Lampcat -> {lamp_dst}")
        os.makedirs(lamp_dst, exist_ok=True)
        # Check if contents are already an album or audio files
        audio_in_lamp = [f for f in os.listdir(lamp_src) if f.endswith(('.flac', '.mp3', '.wav', '.cue', '.log'))]
        dirs_in_lamp = [d for d in os.listdir(lamp_src) if os.path.isdir(os.path.join(lamp_src, d))]
        if audio_in_lamp and not dirs_in_lamp:
            lamp_album = os.path.join(lamp_dst, "死体論")
            safe_merge_dir(lamp_src, lamp_album)
        else:
            safe_merge_dir(lamp_src, lamp_dst)
        if os.path.exists(lamp_src):
            shutil.rmtree(lamp_src)

    # ---------------------------------------------------------
    # 4. CHARACTER SONGS IN J-POP
    # ---------------------------------------------------------
    print("\n[STEP 4] Moving character songs out of J-Pop ...")
    # Nishiura Sora -> Anime/Maebashi Witches
    sora_src = os.path.join(BASE_DIR, "J-Pop", "Nishiura Sora (cv. Aikawa Nao ) (西浦そら(CV.相川奈央)) ~")
    if os.path.exists(sora_src):
        print(f"  Moving Nishiura Sora -> Anime/Maebashi Witches (前橋ウィッチーズ) ~")
        for alb in os.listdir(sora_src):
            safe_merge_dir(os.path.join(sora_src, alb), os.path.join(BASE_DIR, "Anime", "Maebashi Witches (前橋ウィッチーズ) ~", alb))
        if os.path.exists(sora_src):
            shutil.rmtree(sora_src)

    # Yura cv Oonishi Saori -> Game/Towatsugai
    yura_src = os.path.join(BASE_DIR, "J-Pop", "Yura (cv. Oonishi Saori ) (ユラ(CV.大西沙織)) ~")
    if os.path.exists(yura_src):
        print(f"  Moving Yura cv Oonishi Saori -> Game/Towatsugai (トワツガイ) ~")
        for alb in os.listdir(yura_src):
            safe_merge_dir(os.path.join(yura_src, alb), os.path.join(BASE_DIR, "Game", "Towatsugai (トワツガイ) ~", alb))
        if os.path.exists(yura_src):
            shutil.rmtree(yura_src)

    # ---------------------------------------------------------
    # 5. REONA & BOCCHI THE ROCK ERA FLATTENING
    # ---------------------------------------------------------
    print("\n[STEP 5] Flattening ReoNa and Bocchi the Rock! ERA containers ...")
    # ReoNa consolidation
    reona_glitch = os.path.join(BASE_DIR, "J-Pop", "Reona (レオナ) ~")
    reona_target = os.path.join(BASE_DIR, "J-Pop", "ReoNa ~")
    if os.path.exists(reona_glitch):
        print(f"  Consolidating ReoNa into {reona_target} ...")
        os.makedirs(reona_target, exist_ok=True)
        for item in os.listdir(reona_glitch):
            item_path = os.path.join(reona_glitch, item)
            if os.path.isdir(item_path) and "ERA" in item:
                for sub in os.listdir(item_path):
                    sub_path = os.path.join(item_path, sub)
                    clean_name = sub.replace("ReoNa｜", "").strip()
                    safe_merge_dir(sub_path, os.path.join(reona_target, clean_name))
            else:
                safe_merge_dir(item_path, os.path.join(reona_target, item))
        if os.path.exists(reona_glitch):
            shutil.rmtree(reona_glitch)

    # Bocchi the Rock! flattening
    bocchi_dir = os.path.join(BASE_DIR, "Anime", "Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~")
    if os.path.exists(bocchi_dir):
        print(f"  Flattening Bocchi the Rock! containers in {bocchi_dir} ...")
        for c in ["[2022-2022] DIGITAL SINGLES", "[2022-2023] PHYSICAL RELEASES", "[2022-2023] SPECIAL DISCS"]:
            cp = os.path.join(bocchi_dir, c)
            if os.path.exists(cp):
                for alb in os.listdir(cp):
                    alb_path = os.path.join(cp, alb)
                    clean_alb = alb.replace("ぼっち・ざ・ろっく！｜", "").strip()
                    safe_merge_dir(alb_path, os.path.join(bocchi_dir, clean_alb))
                if os.path.exists(cp):
                    shutil.rmtree(cp)

    # ---------------------------------------------------------
    # 6. WINDOWS FORBIDDEN CHARACTERS
    # ---------------------------------------------------------
    print("\n[STEP 6] Sanitizing Windows forbidden characters ...")
    # *Luna ~ -> ＊Luna ~
    luna_src = os.path.join(BASE_DIR, "J-Pop", "*Luna ~")
    luna_dst = os.path.join(BASE_DIR, "J-Pop", "＊Luna ~")
    if os.path.exists(luna_src):
        print(f"  Renaming *Luna ~ -> ＊Luna ~")
        safe_merge_dir(luna_src, luna_dst)
        if os.path.exists(luna_src):
            shutil.rmtree(luna_src)

    # RIOT MUSIC
    riot_dir = os.path.join(BASE_DIR, "Vtuber", "RIOT MUSIC ~")
    if os.path.exists(riot_dir):
        for item in os.listdir(riot_dir):
            if "Re : Volt" in item:
                old_p = os.path.join(riot_dir, item)
                new_p = os.path.join(riot_dir, "Re：Volt")
                print(f"  Renaming RIOT MUSIC album: {item} -> Re：Volt")
                safe_merge_dir(old_p, new_p)
                if os.path.exists(old_p):
                    shutil.rmtree(old_p)
            elif item.endswith(" ~") and os.path.isdir(os.path.join(riot_dir, item)):
                old_p = os.path.join(riot_dir, item)
                new_p = os.path.join(riot_dir, item[:-2])
                print(f"  Removing trailing tilde on album: {item} -> {item[:-2]}")
                safe_merge_dir(old_p, new_p)
                if os.path.exists(old_p):
                    shutil.rmtree(old_p)

    # Tokyo 7th Sisters files with '?'
    t7s_dir = os.path.join(BASE_DIR, "Anime", "Tokyo 7th Sisters (Tokyo 7th シスターズ) ~")
    if os.path.exists(t7s_dir):
        for root, dirs, files in os.walk(t7s_dir):
            for f in files:
                if '?' in f:
                    new_f = f.replace('?', '？')
                    print(f"  Sanitizing '?' in filename: {f} -> {new_f}")
                    os.rename(os.path.join(root, f), os.path.join(root, new_f))

    # Love Live file with '*'
    ll_file = os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~", "無敵級＊ビリーバー｣／中須かすみ", "01. 無敵級*ビリーバー.flac")
    if os.path.exists(ll_file):
        print(f"  Sanitizing '*' in Love Live track: {ll_file}")
        os.rename(ll_file, os.path.join(os.path.dirname(ll_file), "01. 無敵級＊ビリーバー.flac"))

    # Endorfin files with ':'
    for end_parent in ["J-Pop", "Doujinshi"]:
        for end_name in ["Endorfin ~", "Endorfin. ~"]:
            end_dir = os.path.join(BASE_DIR, end_parent, end_name, "Stories of Eve")
            if os.path.exists(end_dir):
                for f in os.listdir(end_dir):
                    if ':' in f:
                        print(f"  Sanitizing ':' in Endorfin track: {f}")
                        os.rename(os.path.join(end_dir, f), os.path.join(end_dir, f.replace(':', '：')))

    # ---------------------------------------------------------
    # 7. CROSS-CATEGORY SPLITS CONSOLIDATION
    # ---------------------------------------------------------
    print("\n[STEP 7] Consolidating cross-category splits ...")
    def merge_cat_artist(src_cat, src_artist, dst_cat, dst_artist):
        s_dir = os.path.join(BASE_DIR, src_cat, src_artist)
        d_dir = os.path.join(BASE_DIR, dst_cat, dst_artist)
        if os.path.exists(s_dir):
            print(f"  Merging [{src_cat}] {src_artist} -> [{dst_cat}] {dst_artist}")
            safe_merge_dir(s_dir, d_dir)
            if os.path.exists(s_dir):
                shutil.rmtree(s_dir)

    # Endorfin. -> Doujinshi/Endorfin. ~
    merge_cat_artist("J-Pop", "Endorfin. ~", "Doujinshi", "Endorfin. ~")
    merge_cat_artist("J-Pop", "Endorfin ~", "Doujinshi", "Endorfin. ~")

    # nayuta -> Doujinshi/nayuta ~
    merge_cat_artist("J-Pop", "nayuta ~", "Doujinshi", "nayuta ~")

    # Hanatan -> Doujinshi/Hanatan (花たん) ~
    merge_cat_artist("J-Pop", "Hanatan (花たん) ~", "Doujinshi", "Hanatan (花たん) ~")
    merge_cat_artist("Doujinshi", "Hanatan ~", "Doujinshi", "Hanatan (花たん) ~")

    # lapix -> Doujinshi/lapix ~
    merge_cat_artist("J-Pop", "lapix ~", "Doujinshi", "lapix ~")
    merge_cat_artist("J-Pop", "Lapix ~", "Doujinshi", "lapix ~")

    # TUYU -> J-Pop/TUYU (ツユ) ~
    tuyu_voc = os.path.join(BASE_DIR, "Vocaloid", "TUYU (ツユ) ~")
    tuyu_jpop = os.path.join(BASE_DIR, "J-Pop", "TUYU (ツユ) ~")
    if os.path.exists(tuyu_voc):
        print(f"  Unifying TUYU into {tuyu_jpop} ...")
        nested = os.path.join(tuyu_voc, "TUYU (ツユ)")
        if os.path.exists(nested):
            safe_merge_dir(nested, tuyu_jpop)
            if os.path.exists(nested):
                shutil.rmtree(nested)
        safe_merge_dir(tuyu_voc, tuyu_jpop)
        if os.path.exists(tuyu_voc):
            shutil.rmtree(tuyu_voc)

    # Lucia -> J-Pop/Lucia ~
    merge_cat_artist("Vocaloid", "Lucia ~", "J-Pop", "Lucia ~")

    # Islet -> Doujinshi/Islet (Tayori) ~
    merge_cat_artist("J-Pop", "Islet (Tayori) ~", "Doujinshi", "Islet (Tayori) ~")

    # Tsukino -> Doujinshi/Tsukino (月乃) ~
    merge_cat_artist("J-Pop", "Tsukino (月乃) ~", "Doujinshi", "Tsukino (月乃) ~")

    # Ruru -> Doujinshi/Ruru (るる) ~
    merge_cat_artist("J-Pop", "Ruru (るる) ~", "Doujinshi", "Ruru (るる) ~")

    # FloweRiЯy -> Vocaloid/FloweRiЯy ~
    merge_cat_artist("J-Pop", "FloweRiЯy ~", "Vocaloid", "FloweRiЯy ~")

    # NEUN -> Vtuber/NEUN ~
    merge_cat_artist("J-Pop", "NEUN ~", "Vtuber", "NEUN ~")

    # Dadaizu -> Doujinshi/Dadaizu (打打だいず) ~
    merge_cat_artist("J-Pop", "Dadaizu (打打だいず) ~", "Doujinshi", "Dadaizu (打打だいず) ~")

    # Hagali -> Doujinshi/Hagali ~
    merge_cat_artist("J-Pop", "Hagali ~", "Doujinshi", "Hagali ~")

    # Imy -> Doujinshi/Imy ~
    merge_cat_artist("J-Pop", "Imy ~", "Doujinshi", "Imy ~")
    merge_cat_artist("J-Pop", "Imy & Endorfin. ~", "Doujinshi", "Imy ~")

    # Isle & Notes -> Doujinshi/Isle & Notes ~
    merge_cat_artist("J-Pop", "Isle & Notes ~", "Doujinshi", "Isle & Notes ~")

    # ubique -> Doujinshi/ubique ~
    merge_cat_artist("J-Pop", "ubique ~", "Doujinshi", "ubique ~")

    # Vivid Lila -> Doujinshi/Vivid Lila ~
    merge_cat_artist("J-Pop", "Vivid Lila ~", "Doujinshi", "Vivid Lila ~")

    print("\n" + "=" * 80)
    print("MASTER REORGANIZATION COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    execute_reorganization()
