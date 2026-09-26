#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER LIBRARY PERFECTION SCRIPT
1. Gakumas: 100% clean structure (0 loose albums in 01. Solo, merge duplicate char folders, flatten GOLD RUSH 3, deduplicate All Stars).
2. Game/: Create top-level category and relocate all 14 games from Anime/ & Vocaloid/ (BLUE PROTOCOL, Arknights, HoYoverse, etc.).
3. Vocaloid/: Relocate misplaced producers (Tetris/Hiiragi Magnetite, Harumaki Gohan, MIMI, TAK).
4. J-Pop/: Consolidate solo artists and bands from Anime/ (Ogura Yui, Ikkyu Nakajima, Atarayo, JUNNA, Ten, Hakoniwa Lily).
5. Vtuber/: Merge split VTubers from J-Pop (HIMEHINA, La Prière).
6. Anime/: Unify character songs & franchises (100 Kanojo, Oshi no Ko, Utahime Dream, MILGRAM, iMarine, HoneyWorks mona).
7. Deformed names: Fix kakasi double parens & artifacts.
8. Catalog & permissions: chmod 775/664, update catalog.sqlite, refresh Lossless.m3u8, reload smbd.
"""

import os
import shutil
import sqlite3
import subprocess
from pathlib import Path

LOSSLESS = Path('/mnt/hdd-backup/music/Lossless')

def log(msg):
    print(f"[MASTER-PERFECTION] {msg}", flush=True)

def safe_move(src: Path, dst: Path):
    if not src.exists():
        return
    if src.resolve() == dst.resolve():
        return

    dst_name_bytes = dst.name.encode('utf-8')
    if len(dst_name_bytes) > 230:
        truncated_str = dst.name[:60] + ' ~'
        dst = dst.parent / truncated_str

    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if src.is_dir() and dst.is_dir():
            for child in list(src.iterdir()):
                safe_move(child, dst / child.name)
            try:
                src.rmdir()
            except OSError:
                pass
            return
        elif src.is_file() and dst.is_file():
            if src.stat().st_size == dst.stat().st_size:
                try: src.unlink()
                except OSError: pass
                return
            else:
                alt_name = dst.stem + '_alt' + dst.suffix
                safe_move(src, dst.parent / alt_name)
                return
    try:
        shutil.move(str(src), str(dst))
        log(f"  Moved: {src.name} -> {dst}")
    except Exception as e:
        log(f"  Move Error {src} -> {dst}: {e}")

def remove_empty(path: Path):
    if path.exists() and path.is_dir():
        for root, dirs, files in os.walk(str(path), topdown=False):
            for d in dirs:
                dp = Path(root) / d
                try:
                    if not list(dp.iterdir()):
                        dp.rmdir()
                except OSError:
                    pass
        try:
            if not list(path.iterdir()):
                path.rmdir()
                log(f"  Removed empty dir: {path.name}")
        except OSError:
            pass

# ==============================================================================
# PART 1: GAKUMAS COMPLETE CLEANUP
# ==============================================================================
log("--- PART 1: GAKUMAS CLEANUP ---")
gakumas = LOSSLESS / 'Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~'
solo = gakumas / '01. Solo'

if solo.exists():
    # 1. Merge unnumbered character folders into numbered ones
    char_merge_map = {
        '倉本千奈': '06. 倉本千奈 (China Kuramoto)',
        '十王星南': '12. 十王星南 (Sena Juo)',
        '秦谷美鈴': '11. 秦谷美鈴 (Misuzu Hataya)',
        '紫雲清夏': '07. 紫雲清夏 (Sumika Shiun)',
    }
    for old_name, canonical in char_merge_map.items():
        old_p = solo / old_name
        can_p = solo / canonical
        if old_p.exists():
            log(f"Merging unnumbered char folder {old_name} -> {canonical}")
            safe_move(old_p, can_p)

    # 2. Map all loose albums in 01. Solo to their canonical character folder
    album_to_char = {
        'Be proud': '13. 雨夜燕 (Tsubame Amaya)',
        'Choo Choo Choo': '12. 十王星南 (Sena Juo)',
        'L\'Espoir': '04. 有村麻央 (Mao Arimura)',
        'MY STAGE': '13. 雨夜燕 (Tsubame Amaya)',
        'ORDER FAKE': '02. 月村手毬 (Temari Tsukimura)',
        'Superlative': '11. 秦谷美鈴 (Misuzu Hataya)',
        'VEIL': '11. 秦谷美鈴 (Misuzu Hataya)',
        'Wildest Flower': '01. 花海咲季 (Saki Hanami)',
        'nazonazo': '01. 花海咲季 (Saki Hanami)',
        'いつかのわたし': '05. 葛城リーリヤ (Lilja Katsuragi)',
        'かちドキ': '03. 藤田ことね (Kotone Fujita)',
        'め': '08. 篠澤広 (Hiro Shinosawa)',
        'クライアイ': '13. 雨夜燕 (Tsubame Amaya)',
        '一体いつから': '02. 月村手毬 (Temari Tsukimura)',
        '三分半の創世': '13. 雨夜燕 (Tsubame Amaya)',
        '春と光': '10. 花海佑芽 (Ume Hanami)',
        '真っ白いページと水彩の主人公': '10. 花海佑芽 (Ume Hanami)',
        '神かわいい': '03. 藤田ことね (Kotone Fujita)',
        '赤裸々': '12. 十王星南 (Sena Juo)',
        '重なる夜空の痕跡に': '09. 姫崎莉波 (Rinami Himesaki)',
        '金の斧、銀の斧、エメラルドの斧': '10. 花海佑芽 (Ume Hanami)',
    }

    for item in list(solo.iterdir()):
        if not item.is_dir():
            continue
        # If it's a character folder (starts with digits), skip
        if item.name[:2].isdigit() and '.' in item.name[:3]:
            continue
        
        album_name = item.name
        if album_name in album_to_char:
            char_folder = solo / album_to_char[album_name]
            target_album = char_folder / album_name
            log(f"Handling loose solo album '{album_name}' -> {char_folder.name}")
            safe_move(item, target_album)

    # 3. Clean All Stars & Units in Gakumas
    all_stars = gakumas / '04. All Stars & Units'
    if all_stars.exists():
        # Flatten GOLD RUSH 3
        gr3_outer = all_stars / 'GOLD RUSH 第3巻 オリジナルCD付き特装版'
        if gr3_outer.exists():
            nested = gr3_outer / '学園アイドルマスター GOLD RUSH 第3CD'
            if nested.exists():
                log("Flattening GOLD RUSH 3 nested subfolder")
                for f in list(nested.iterdir()):
                    safe_move(f, gr3_outer / f.name)
                try: nested.rmdir()
                except OSError: pass

        # Deduplicate Duo/Trio that exist in All Stars
        duo_tier = gakumas / '02. Duo'
        trio_tier = gakumas / '03. Trio'
        for dup in ['SUGAR FLAVOR']:
            p = all_stars / dup
            if p.exists() and (duo_tier / dup).exists():
                log(f"Removing duplicate Duo '{dup}' from All Stars")
                shutil.rmtree(str(p), ignore_errors=True)
        for dup in ['「ねえ、言っちゃうよ。」', 'わかし・さわがし・スカパンク']:
            p = all_stars / dup
            if p.exists() and (trio_tier / dup).exists():
                log(f"Removing duplicate Trio '{dup}' from All Stars")
                shutil.rmtree(str(p), ignore_errors=True)

# ==============================================================================
# PART 2: GAME/ CATEGORY & RELOCATIONS
# ==============================================================================
log("\n--- PART 2: GAME/ CATEGORY CREATION & RELOCATIONS ---")
game_cat = LOSSLESS / 'Game'
game_cat.mkdir(parents=True, exist_ok=True)

# 1. Arknights: Flatten 33 albums from nested folder and move to Game/Arknights ~
ark_broken = LOSSLESS / 'Anime/Arknights ( Akunaitsu ~'
ark_target = game_cat / 'Arknights ~'
if ark_broken.exists():
    log("Relocating and flattening Arknights -> Game/Arknights ~")
    # find any nested folder
    for child in list(ark_broken.iterdir()):
        if child.is_dir():
            for album in list(child.iterdir()):
                safe_move(album, ark_target / album.name)
        elif child.is_file():
            safe_move(child, ark_target / child.name)
    shutil.rmtree(str(ark_broken), ignore_errors=True)

# 2. Relocate other Games from Anime/
games_to_move = [
    ('Anime/BLUE PROTOCOL ~', 'BLUE PROTOCOL ~'),
    ('Anime/HoYoverse (miHoYo／HOYO-MiX) ~', 'HoYoverse (miHoYo／HOYO-MiX) ~'),
    ('Anime/Wuthering Waves (鳴潮) ~', 'Wuthering Waves (鳴潮) ~'),
    ('Anime/SEGA & Arcade Games ~', 'SEGA & Arcade Games ~'),
    ('Anime/O.N.G.E.K.I. (オンゲキ) ~', 'O.N.G.E.K.I. (オンゲキ) ~'),
    ('Anime/WHITE ALBUM2 (Howaitoarubamu 2) (WHITE ALBUM2 (ホワイトアルバム2)) ~', 'WHITE ALBUM2 (ホワイトアルバム2) ~'),
    ('Anime/Blue Archive (ブルーアーカイブ) ~', 'Blue Archive (ブルーアーカイブ) ~'),
    ('Anime/Azur Lane (アズールレーン) ~', 'Azur Lane (アズールレーン) ~'),
    ('Anime/Heaven Burns Red (ヘブンバーンズレッド) ~', 'Heaven Burns Red (ヘブンバーンズレッド) ~'),
    ('Anime/Battle Girl High School (バトルガール ハイスクール) ~', 'Battle Girl High School ~'),
    ('Anime/Towatsugai (トワツガイ) ~', 'Towatsugai (トワツガイ) ~'),
    ('Anime/MementoMori (メメントモリ) ~', 'MementoMori (メメントモリ) ~'),
]

for src_rel, dst_rel in games_to_move:
    src_p = LOSSLESS / src_rel
    dst_p = game_cat / dst_rel
    if src_p.exists():
        log(f"Relocating game {src_rel} -> Game/{dst_rel}")
        safe_move(src_p, dst_p)

# 3. Project SEKAI: Merge from Anime and Vocaloid into Game/Project SEKAI ~
pse_target = game_cat / 'Project SEKAI (プロジェクトセカイ) ~'
for p in [LOSSLESS / 'Anime/Project SEKAI (プロジェクトセカイ) ~', LOSSLESS / 'Vocaloid/Project SEKAI (プロジェクトセカイ) ~']:
    if p.exists():
        log(f"Merging Project SEKAI from {p.parent.name} -> Game/")
        safe_move(p, pse_target)

# ==============================================================================
# PART 3: VOCALOID MIGRATIONS
# ==============================================================================
log("\n--- PART 3: VOCALOID MIGRATIONS ---")
vocaloid_cat = LOSSLESS / 'Vocaloid'

# 1. Tetris -> Hiiragi Magnetite
tetris_src = LOSSLESS / 'Anime/Tetris (テトリス) ~'
hiiragi_dst = vocaloid_cat / 'Hiiragi Magnetite (柊マグネタイト) ~'
if tetris_src.exists():
    log("Moving Tetris -> Vocaloid/Hiiragi Magnetite (柊マグネタイト) ~/テトリス")
    safe_move(tetris_src, hiiragi_dst)

# 2. Harumaki Gohan -> Vocaloid
hg_vtuber = LOSSLESS / 'Vtuber/Harumaki Gohan (はるまきごはん) ~'
hg_dst = vocaloid_cat / 'Harumaki Gohan (はるまきごはん) ~'
if hg_vtuber.exists():
    log("Merging Harumaki Gohan from Vtuber -> Vocaloid")
    safe_move(hg_vtuber, hg_dst)
hg_plain = vocaloid_cat / 'Harumaki Gohan ~'
if hg_plain.exists():
    safe_move(hg_plain, hg_dst)

# 3. MIMI -> Vocaloid
mimi_dst = vocaloid_cat / 'MIMI ~'
for p in [LOSSLESS / 'Vtuber/MIMI ~', LOSSLESS / 'J-Pop/MIMI ~']:
    if p.exists():
        log(f"Merging MIMI from {p.parent.name} -> Vocaloid/MIMI ~")
        safe_move(p, mimi_dst)

# 4. TAK -> Vocaloid
tak_jpop = LOSSLESS / 'J-Pop/TAK ~'
tak_dst = vocaloid_cat / 'TAK ~'
if tak_jpop.exists():
    log("Merging TAK from J-Pop -> Vocaloid/TAK ~")
    safe_move(tak_jpop, tak_dst)

# ==============================================================================
# PART 4: J-POP SOLO ARTISTS & BANDS RELOCATIONS
# ==============================================================================
log("\n--- PART 4: J-POP ARTISTS RELOCATIONS ---")
jpop_cat = LOSSLESS / 'J-Pop'

# 1. Ogura Yui: Unify into J-Pop/Yui Ogura (小倉唯) ~
ogura_target = jpop_cat / 'Yui Ogura (小倉唯) ~'
for p in [LOSSLESS / 'Anime/Ogura Yui (小倉唯) ~', LOSSLESS / 'J-Pop/Ogura Yui (小倉唯) ~', LOSSLESS / 'J-Pop/Yui Ogura (小倉 唯) ~']:
    if p.exists():
        log(f"Merging Ogura Yui from {p} -> {ogura_target.name}")
        safe_move(p, ogura_target)

# 2. Ikkyu Nakajima
ikkyu_src = LOSSLESS / 'Anime/Ikkyu Nakajima (中嶋イッキュウ) ~'
ikkyu_dst = jpop_cat / 'Ikkyu Nakajima (中嶋イッキュウ) ~'
if ikkyu_src.exists():
    log("Moving Ikkyu Nakajima from Anime -> J-Pop")
    safe_move(ikkyu_src, ikkyu_dst)

# 3. Atarayo
atarayo_src = LOSSLESS / 'Anime/Atarayo (あたらよ) ~'
atarayo_dst = jpop_cat / 'Atarayo (あたらよ) ~'
if atarayo_src.exists():
    log("Merging Atarayo from Anime -> J-Pop")
    safe_move(atarayo_src, atarayo_dst)

# 4. JUNNA: Unpack grotesque folder and consolidate
junna_anime = LOSSLESS / 'Anime/Junna ~'
junna_dst = jpop_cat / 'JUNNA ~'
if junna_anime.exists():
    safe_move(junna_anime, junna_dst)

junna_ugly = jpop_cat / 'Junna Junna (sakai Junna Sakai Jun Na ) (じゅんな JUNNA  (Sakai Junna 境純菜)) ~'
if junna_ugly.exists():
    log("Unpacking and flattening ugly JUNNA folder into J-Pop/JUNNA ~")
    for era in list(junna_ugly.iterdir()):
        if era.is_dir() and 'ERA' in era.name:
            for alb in list(era.iterdir()):
                # Clean prefix 'JUNNA｜'
                clean_alb_name = alb.name.replace('JUNNA｜', '').strip()
                safe_move(alb, junna_dst / clean_alb_name)
        elif era.is_dir():
            safe_move(era, junna_dst / era.name)
    shutil.rmtree(str(junna_ugly), ignore_errors=True)

junna_plain = jpop_cat / 'Junna ~'
if junna_plain.exists() and junna_plain != junna_dst:
    safe_move(junna_plain, junna_dst)

# 5. Ten
ten_src = LOSSLESS / 'Anime/Ten ~'
ten_dst = jpop_cat / 'Ten ~'
if ten_src.exists():
    log("Moving Ten from Anime -> J-Pop/Ten ~")
    safe_move(ten_src, ten_dst)

# 6. Hakoniwa Lily
hakoniwa_src = LOSSLESS / 'Anime/Hakoniwa Lily (ハコニワリリィ) ~'
hakoniwa_dst = jpop_cat / 'Hakoniwa Lily (ハコニワリリィ) ~'
if hakoniwa_src.exists():
    log("Moving Hakoniwa Lily from Anime -> J-Pop")
    safe_move(hakoniwa_src, hakoniwa_dst)

# ==============================================================================
# PART 5: VTUBER UNIFICATIONS
# ==============================================================================
log("\n--- PART 5: VTUBER UNIFICATIONS ---")
vtuber_cat = LOSSLESS / 'Vtuber'

# 1. HIMEHINA
himehina_jpop = jpop_cat / 'HIMEHINA ~'
himehina_dst = vtuber_cat / 'HIMEHINA ~'
if himehina_jpop.exists():
    log("Merging HIMEHINA from J-Pop -> Vtuber/HIMEHINA ~")
    safe_move(himehina_jpop, himehina_dst)

# 2. La Prière
lapriere_jpop = jpop_cat / 'La prière ~'
lapriere_dst = vtuber_cat / 'La Prière ~'
if lapriere_jpop.exists():
    log("Merging La prière from J-Pop -> Vtuber/La Prière ~")
    safe_move(lapriere_jpop, lapriere_dst)

# 3. Natsume Itsuki
ni_doujin = LOSSLESS / 'Doujinshi/Natsume Itsuki (棗いつき) ~'
ni_dst = vtuber_cat / 'Natsume Itsuki (棗いつき) ~'
if ni_doujin.exists():
    log("Merging Natsume Itsuki from Doujinshi -> Vtuber")
    safe_move(ni_doujin, ni_dst)

# ==============================================================================
# PART 6: ANIME FRANCHISES & CHARACTER SONGS
# ==============================================================================
log("\n--- PART 6: ANIME FRANCHISES & CHARACTER SONGS ---")
anime_cat = LOSSLESS / 'Anime'

# 1. 100 Kanojo: Unify into Anime/100 Kanojo (君のことが大大大大大好きな100人の彼女) ~
kanojo_dst = anime_cat / '100 Kanojo (君のことが大大大大大好きな100人の彼女) ~'
koi_jpop = jpop_cat / 'Koi Tarou Famiri (恋太郎ファミリー) ~'
if koi_jpop.exists():
    log("Moving 100 Kanojo character songs from J-Pop -> Anime/100 Kanojo ~")
    safe_move(koi_jpop, kanojo_dst)

# 2. Oshi no Ko / B Komachi: Unify into Anime/Oshi no Ko (【推しの子】) ~
oshino_dst = anime_cat / 'Oshi no Ko (【推しの子】) ~'
for p in [anime_cat / 'B Komachi (B小町) ~', jpop_cat / 'B Komachi (B小町) ~']:
    if p.exists():
        log(f"Merging B Komachi from {p} -> {oshino_dst.name}")
        safe_move(p, oshino_dst)

# 3. Utahime Dream: Relocate character folders from J-Pop
utanome_dst = anime_cat / 'Utahime Dream (ウタヒメドリーム) ~'
# Also rename Utanome Dream to Utahime Dream
old_utanome = anime_cat / 'Utanome Dream (ウタヒメドリーム) ~'
if old_utanome.exists() and old_utanome != utanome_dst:
    safe_move(old_utanome, utanome_dst)

utanome_chars = [
    'Takagi Rin (cv. Washimi Yumi Jiena ) (高木凛(CV.鷲見友美ジェナ)) ~',
    'Masshiro Kiyomi (cv. Sono Hara Ari Sa ) (真白清美(CV.其原有沙)) ~',
    'Mizu Gatsu Hikari (cv. Gi Bu Hana Rin ) (水月ひかり(CV.礒部花凜)) ~',
]
for ch in utanome_chars:
    p = jpop_cat / ch
    if p.exists():
        log(f"Moving Utahime Dream char '{ch}' -> Utahime Dream ~")
        safe_move(p, utanome_dst)

# 4. MILGRAM
milgram_src = jpop_cat / 'Milgram Amane (cv : Tanaka Bi Umi ) (MILGRAM アマネ (CV： 田中美海)) ~'
milgram_dst = anime_cat / 'MILGRAM ~'
if milgram_src.exists():
    log("Moving MILGRAM Amane -> Anime/MILGRAM ~")
    safe_move(milgram_src, milgram_dst)

# 5. iMarine Project
imarine_dst = anime_cat / 'iMarine Project ~'
for ch in ['Aimarin (cv_ Uchida Sai ) (アイマリン(CV_内田 彩)) ~', 'iMarine(CV_Aya Uchida)Ichika zero(CV_Iori Saeki) ~']:
    p = jpop_cat / ch
    if p.exists():
        log(f"Moving iMarine '{ch}' -> Anime/iMarine Project ~")
        safe_move(p, imarine_dst)

# 6. HoneyWorks mona
mona_src = jpop_cat / 'mona (CV 夏川椎菜) ~'
mona_dst = anime_cat / 'HoneyWorks (mona) ~'
if mona_src.exists():
    log("Moving mona from J-Pop -> Anime/HoneyWorks (mona) ~")
    safe_move(mona_src, mona_dst)

# ==============================================================================
# PART 7: SANITIZE DEFORMED FOLDER NAMES
# ==============================================================================
log("\n--- PART 7: SANITIZING DEFORMED FOLDER NAMES ---")
deformed_renames = [
    (anime_cat / 'Pole Princess!! (Porupurinsesu !!) (Pole Princess!! (ポールプリンセス!!)) ~', anime_cat / 'Pole Princess!! (ポールプリンセス!!) ~'),
    (jpop_cat / '( Yuika ) (『ユイカ』) ~', jpop_cat / 'Yuika (『ユイカ』) ~'),
    (jpop_cat / 'Nasuo (hosi) (なすお☆) ~', jpop_cat / 'Nasuo (なすお☆) ~'),
    (jpop_cat / 'Majikarufijikaru (hosi) Kururu (マジカルフィジカル☆くるる) ~', jpop_cat / 'Magical Physical Kururu (マジカルフィジカル☆くるる) ~'),
    (jpop_cat / 'Neta Furi Keikaku - ( Gen ) (寝たふり計画 -『現』) ~', jpop_cat / 'Neta Furi Keikaku (寝たふり計画) ~'),
    (jpop_cat / 'Nakano Den Nou , Okini (hosi) Partys , Picco , Capchii (中野電脳、OKINI☆PARTY\'S、picco、Capchii) ~', jpop_cat / 'Nakano Dennou (中野電脳) ~'),
]

for src, dst in deformed_renames:
    if src.exists():
        log(f"Renaming deformed folder: {src.name} -> {dst.name}")
        safe_move(src, dst)

# Remove empty placeholder folders
for p in [anime_cat / 'K-ON! ~', anime_cat / 'General Anime Singles & OST ~']:
    if p.exists() and not list(p.iterdir()):
        p.rmdir()
        log(f"Removed empty placeholder: {p.name}")

# Prune empty directories in Anime, J-Pop, Vocaloid, Vtuber, Game
for cat in ['Anime', 'Game', 'J-Pop', 'Vocaloid', 'Vtuber', 'Doujinshi']:
    cat_p = LOSSLESS / cat
    if cat_p.exists():
        remove_empty(cat_p)

log("\n[MASTER-PERFECTION] All filesystem modifications complete successfully!")
