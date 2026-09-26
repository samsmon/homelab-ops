#!/usr/bin/env python3
import os
import shutil
import re

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

def safe_move(src, dst):
    if not os.path.exists(src):
        return
    if os.path.isfile(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        if os.path.exists(dst):
            if os.path.getsize(src) == os.path.getsize(dst):
                os.remove(src)
            else:
                base, ext = os.path.splitext(dst)
                shutil.move(src, f"{base}_dup{ext}")
        else:
            shutil.move(src, dst)
    elif os.path.isdir(src):
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            safe_move(os.path.join(src, item), os.path.join(dst, item))
        if os.path.exists(src) and not os.listdir(src):
            os.rmdir(src)

def execute_perfection(dry_run=True):
    print(f"=== FRANCHISE & ARTIST PERFECTION (DRY RUN = {dry_run}) ===")
    actions = []

    def plan_move(src, dst, desc):
        actions.append(('MOVE', src, dst, desc))
        if not dry_run:
            safe_move(src, dst)

    def plan_delete(path, desc):
        actions.append(('DELETE', path, '', desc))
        if not dry_run:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    # 1. Mori Calliope -> Vtuber/Hololive
    mori_src = os.path.join(BASE_DIR, "J-Pop", "Mori Calliope ~")
    mori_dst = os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~", "Mori Calliope ~")
    if os.path.exists(mori_src):
        plan_move(mori_src, mori_dst, "Move Mori Calliope to Hololive")

    # 2. Kobo Kanaeru -> Vtuber/Hololive
    kobo_src = os.path.join(BASE_DIR, "Vtuber", "Kobo Kanaeru ~")
    kobo_dst = os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~", "Kobo Kanaeru ~")
    if os.path.exists(kobo_src):
        plan_move(kobo_src, kobo_dst, "Move Kobo Kanaeru to Hololive")

    # 3. Shigure Ui consolidation
    ui_src = os.path.join(BASE_DIR, "Vtuber", "Shigure Ui (しぐれうい) ~")
    ui_dst = os.path.join(BASE_DIR, "Vtuber", "Ui Shigure (しぐれうい) ~")
    if os.path.exists(ui_src):
        plan_move(ui_src, ui_dst, "Consolidate Shigure Ui")

    # 4. Ryugasaki Rene consolidation
    rene_src = os.path.join(BASE_DIR, "Vtuber", "Ryuu Saki Rin (龍ヶ崎リン) ~")
    rene_dst = os.path.join(BASE_DIR, "Vtuber", "Ryugasaki Rene (龍ヶ崎リン) ~")
    if os.path.exists(rene_src):
        plan_move(rene_src, rene_dst, "Consolidate Ryugasaki Rene")

    # 5. Move FATE GEAR, KOIAI, OCHA NORMA from Vocaloid to J-Pop
    for band in ["FATE GEAR ~", "KOIAI ~", "OCHA NORMA ~"]:
        v_src = os.path.join(BASE_DIR, "Vocaloid", band)
        j_dst = os.path.join(BASE_DIR, "J-Pop", band)
        if os.path.exists(v_src):
            plan_move(v_src, j_dst, f"Move {band} from Vocaloid to J-Pop")

    # 6. Consolidate (K)NoW_NAME
    know_src = os.path.join(BASE_DIR, "Anime", "(K)NoW_NAME：NIKIIE ~")
    now_src = os.path.join(BASE_DIR, "J-Pop", "NoW_NAME ~")
    know_target = os.path.join(BASE_DIR, "J-Pop", "(K)NoW_NAME ~")
    if os.path.exists(now_src):
        plan_move(now_src, know_target, "Rename NoW_NAME to (K)NoW_NAME")
    if os.path.exists(know_src):
        plan_move(know_src, know_target, "Move (K)NoW_NAME single from Anime to J-Pop")

    # 7. Move mobile rhythm games from Anime to Game
    games_to_move = [
        "Tokyo 7th Sisters (Tokyo 7th シスターズ) ~",
        "Idoly Pride (アイドリープライド) ~",
        "IDOLiSH7 (アイドリッシュセブン) ~",
        "CUE! ~",
        "Lapis ReLiGHTs ~",
        "LiveRevolt ~"
    ]
    for gm in games_to_move:
        g_src = os.path.join(BASE_DIR, "Anime", gm)
        g_dst = os.path.join(BASE_DIR, "Game", gm)
        if os.path.exists(g_src):
            plan_move(g_src, g_dst, f"Move {gm} from Anime to Game")

    print(f"Total planned actions: {len(actions)}")
    for act, src, dst, desc in actions:
        print(f"  [{act}] {os.path.basename(src)} -> {os.path.basename(dst)} ({desc})")

if __name__ == '__main__':
    execute_perfection(dry_run=False)

