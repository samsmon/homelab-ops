#!/usr/bin/env python3
import os
import shutil
import subprocess

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

def execute_zero_redundancy(dry_run=True):
    print(f"=== ZERO REDUNDANCY & EXACT DUPLICATE PURGE (DRY RUN = {dry_run}) ===")
    actions = []

    def plan_delete(p, desc):
        actions.append(('DELETE', p, desc))
        if not dry_run:
            if os.path.isfile(p):
                os.remove(p)
            elif os.path.isdir(p):
                shutil.rmtree(p)

    def plan_move(src, dst, desc):
        actions.append(('MOVE', src, dst, desc))
        if not dry_run:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                if os.path.isfile(src) and os.path.isfile(dst):
                    if os.path.getsize(src) == os.path.getsize(dst):
                        os.remove(src)
                    else:
                        base, ext = os.path.splitext(dst)
                        shutil.move(src, f"{base}_dup{ext}")
                elif os.path.isdir(src) and os.path.isdir(dst):
                    for item in os.listdir(src):
                        plan_move(os.path.join(src, item), os.path.join(dst, item), desc)
                    if os.path.exists(src) and not os.listdir(src):
                        os.rmdir(src)
            else:
                shutil.move(src, dst)

    # 1. Towatsugai duplicate folder
    towa_dup = os.path.join(BASE_DIR, "Game", "Towatsugai (トワツガイ) ~", "トワツガイ キャラクターソング灰の棺／回転木馬とワルツ／花に願いを／偽りの救済／罪と罰／空の人魚」")
    if os.path.exists(towa_dup):
        plan_delete(towa_dup, "Delete exact duplicate Towatsugai character song collection")

    # 2. Rokudenashi duplicates -> merge into clean 'ユリイカ'
    roku_dir = os.path.join(BASE_DIR, "J-Pop", "Rokudenashi (ロクデナシ) ~")
    eureka_clean = os.path.join(roku_dir, "ユリイカ")
    eureka_vtcl = os.path.join(roku_dir, "ユリイカ [VTCL-35376]")
    eureka_ltd = os.path.join(roku_dir, "ユリイカ [初回限定盤]")

    if os.path.exists(eureka_vtcl):
        plan_delete(eureka_vtcl, "Delete duplicate Eureka VTCL")
    if os.path.exists(eureka_ltd):
        # copy exclusive 03 夜明けと蛍.flac and CD if exists
        yoake = os.path.join(eureka_ltd, "03 夜明けと蛍.flac")
        if os.path.exists(yoake):
            plan_move(yoake, os.path.join(eureka_clean, "03. 夜明けと蛍.flac"), "Move exclusive limited track")
        plan_delete(eureka_ltd, "Delete Eureka limited folder")

    # 3. Hatsune Miku Magical Mirai 2024 duplicate
    miku_dir = os.path.join(BASE_DIR, "Vocaloid", "Hatsune Miku Magical Mirai (初音ミク マジカルミライ) ~")
    miku_dup = os.path.join(miku_dir, "初音ミク「マジカルミライ 2024」OFFICIAL ALBUM (Hatsune Miku 'Magical Mirai 2024' OFFICIAL ALBUM)")
    if os.path.exists(miku_dup):
        plan_delete(miku_dup, "Delete duplicate Magical Mirai 2024 romaji copy")

    # 4. 2.5 Jigen no Ririsa duplicate single
    ririsa_single = os.path.join(BASE_DIR, "Anime", "2.5 Jigen no Ririsa (2.5次元の誘惑) ~", "Watch Me (Digital Single)")
    if os.path.exists(ririsa_single):
        plan_delete(ririsa_single, "Delete redundant 1-track Watch Me digital single")

    # 5. Cute Cutting Club duplicates
    ccc_dir = os.path.join(BASE_DIR, "Doujinshi", "Cute Cutting Club ~")
    ccc_empty = os.path.join(ccc_dir, "cut(e)vol.3")
    ccc_cd = os.path.join(ccc_dir, "cut(e)vol.3 {CUTE-003}")
    ccc_hires = os.path.join(ccc_dir, "cut(e) vol.3 {CUTE-003}")
    ccc_target = os.path.join(ccc_dir, "cut(e) vol.3")

    if os.path.exists(ccc_cd) and os.path.exists(os.path.join(ccc_cd, "Scans")):
        plan_move(os.path.join(ccc_cd, "Scans"), os.path.join(ccc_hires, "Scans"), "Move CD scans to Hi-Res album")
    if os.path.exists(ccc_cd):
        plan_delete(ccc_cd, "Delete redundant 16-bit CD copy")
    if os.path.exists(ccc_empty):
        plan_delete(ccc_empty, "Delete empty container")
    if os.path.exists(ccc_hires):
        plan_move(ccc_hires, ccc_target, "Rename cut(e) vol.3 to clean title")

    # 6. Mamyukka redundant WAV files
    mamy_wav_dir = os.path.join(BASE_DIR, "Doujinshi", "Mamyukka ~", "エトイリカの夜")
    if os.path.exists(mamy_wav_dir):
        for f in os.listdir(mamy_wav_dir):
            if f.endswith('.wav'):
                plan_delete(os.path.join(mamy_wav_dir, f), f"Delete redundant WAV: {f}")

    # 7. Split unsplit single-image CUE discs (Rule 6)
    cue_split_dirs = [
        # Love Live Liella SPCD
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Liella! (ラブライブ！スーパースター!!) ~", "Liella!", "SPCD 01 ｢探して! Future｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Liella! (ラブライブ！スーパースター!!) ~", "Liella!", "SPCD 02 ｢HAPPY TO DO WA!｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Liella! (ラブライブ！スーパースター!!) ~", "Liella!", "SPCD 03 ｢Stella!｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Liella! (ラブライブ！スーパースター!!) ~", "Liella!", "SPCD 04 ｢クレッシェンドゆ・ら｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Liella! (ラブライブ！スーパースター!!) ~", "Liella!", "SPCD 05 ｢変わらないすべて｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Liella! (ラブライブ！スーパースター!!) ~", "Liella!", "SPCD 06 ｢満開目指して!｣"),
        # Love Live Nijigasaki Original Song CDs
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~", "Original Song CD 01 ｢Fashionista｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~", "Original Song CD 02 ｢Fuwa Fuwaアワー！｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~", "Original Song CD 03 ｢ロマンスの中で｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~", "Original Song CD 04 ｢Look at me now｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~", "Original Song CD 05 ｢TOKIMEKI Runners (12人Ver.)｣"),
        os.path.join(BASE_DIR, "Anime", "Love Live! (ラブライブ！) ~", "Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~", "Original Song CD 06 ｢Love U my friends (12人Ver.)｣"),
        # Mamyukka
        os.path.join(BASE_DIR, "Doujinshi", "Mamyukka ~", "サハラムシカ"),
    ]

    for c_dir in cue_split_dirs:
        if not os.path.exists(c_dir):
            continue
        cues = [f for f in os.listdir(c_dir) if f.lower().endswith('.cue')]
        flacs = [f for f in os.listdir(c_dir) if f.lower().endswith('.flac')]
        if len(cues) == 1 and len(flacs) == 1:
            cue_f = cues[0]
            flac_f = flacs[0]
            actions.append(('SPLIT_CUE', os.path.join(c_dir, cue_f), f"Split disc image {flac_f} into tracks"))
            if not dry_run:
                try:
                    res = subprocess.run(['shnsplit', '-f', cue_f, '-t', '%n. %t', '-o', 'flac', flac_f], cwd=c_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    new_flacs = [f for f in os.listdir(c_dir) if f.lower().endswith('.flac') and f != flac_f]
                    if len(new_flacs) > 1:
                        # Splitting succeeded! Delete original whole disc image and cue
                        os.remove(os.path.join(c_dir, flac_f))
                        os.remove(os.path.join(c_dir, cue_f))
                        print(f"  Successfully split {len(new_flacs)} tracks in {os.path.basename(c_dir)}")
                    else:
                        print(f"  Warning: Splitting did not produce expected files: {res.stderr}")
                except Exception as e:
                    print(f"  Error splitting {c_dir}: {e}")

    print(f"Total planned actions: {len(actions)}")
    for item in actions:
        if len(item) == 4:
            act, src, dst, desc = item
            print(f"  [{act}] {os.path.basename(src)} -> {os.path.basename(dst)} ({desc})")
        else:
            act, p, desc = item
            print(f"  [{act}] {os.path.basename(p)} ({desc})")

if __name__ == '__main__':
    execute_zero_redundancy(dry_run=False)

