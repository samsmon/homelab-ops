#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER STRUCTURAL FIX SCRIPT
Resolves all subfranchise split folders, mojibake names, loose albums in franchise umbrellas,
and remaining format tags across /mnt/hdd-backup/music/Lossless/.
"""

import os
import re
import sys
import shutil
from pathlib import Path

# Add homelab-ops script path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from master_music_centralization import (
    LOSSLESS_ROOT, safe_move, clean_album_title, log
)

# ==============================================================================
# 1. FIX THE IDOLM@STER (アイドルマスター) ~
# ==============================================================================
def fix_idolmaster():
    log("=== FIXING THE IDOLM@STER (アイドルマスター) ~ ===")
    imas_dir = LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~'
    if not imas_dir.exists():
        log("THE IDOLM@STER folder not found, skipping.")
        return

    # A. Remove Mojibake '?????????' (Samba _YK3YV~S)
    for p in list(imas_dir.iterdir()):
        if not p.is_dir():
            continue
        # Detect mojibake folder consisting of question marks
        if all(c == '?' for c in p.name) or '?' in p.name:
            log(f"Found mojibake folder: {repr(p.name)}, rescuing contents...")
            target_shiny = imas_dir / 'Shiny Colors (シャイニーカラーズ) ~'
            target_shiny.mkdir(parents=True, exist_ok=True)
            for item in list(p.iterdir()):
                safe_move(item, target_shiny / item.name)
            try:
                p.rmdir()
                log("  Mojibake folder removed.")
            except OSError:
                pass

    # B. Consolidate Shiny Colors: 'シャイニーカラーズ' -> 'Shiny Colors (シャイニーカラーズ) ~'
    shiny_canonical = imas_dir / 'Shiny Colors (シャイニーカラーズ) ~'
    shiny_canonical.mkdir(parents=True, exist_ok=True)
    
    # Subseries targets inside Shiny Colors
    s_wing = shiny_canonical / '01. WING & Main Game Series'
    s_prism = shiny_canonical / '02. Song for Prism Series'
    s_anime = shiny_canonical / '03. Anime Series'
    s_feathers = shiny_canonical / '04. COLORFUL FE@THERS Series'
    s_collab = shiny_canonical / '05. Synthe-Side & Collaborations'
    for d in [s_wing, s_prism, s_anime, s_feathers, s_collab]:
        d.mkdir(parents=True, exist_ok=True)

    # Subseries under WING
    s_canvas = s_wing / '06. CANVAS'
    s_echoes = s_wing / '07. ECHOES'
    s_panorma = s_wing / '05. PANOR@MA WING'
    s_halo = s_wing / '08. 円環 -Halo around-'
    for d in [s_canvas, s_echoes, s_panorma, s_halo]:
        d.mkdir(parents=True, exist_ok=True)

    shiny_raw = imas_dir / 'シャイニーカラーズ'
    if shiny_raw.exists() and shiny_raw.is_dir():
        log("Merging raw 'シャイニーカラーズ' into canonical umbrella...")
        # Clean tag on 神様は死んだ、って(WVP 96kHz_32bit)
        wvp = shiny_raw / '神様は死んだ、って(WVP 96kHz_32bit)'
        if wvp.exists():
            dest_wvp = s_prism / '神様は死んだ、って'
            log(f"  Moving & cleaning format tag: {wvp.name} -> {dest_wvp}")
            safe_move(wvp, dest_wvp)
        # Move all structured series into canonical
        for item in list(shiny_raw.iterdir()):
            safe_move(item, shiny_canonical / item.name)
        try:
            shiny_raw.rmdir()
        except OSError:
            pass

    # Organize loose albums inside Shiny Colors
    for item in list(shiny_canonical.iterdir()):
        if not item.is_dir():
            if item.suffix.lower() == '.flac':
                # e.g. 01 Borderline.flac
                dest = s_prism / 'ボーダーレス・ノンストレス／Oh Yeah!!' / item.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                safe_move(item, dest)
            continue
        name = item.name
        if name.startswith('01.') or name.startswith('02.') or name.startswith('03.') or name.startswith('04.') or name.startswith('05.'):
            continue # Already a series folder
            
        if 'Song for Prism' in name:
            safe_move(item, s_prism / name)
        elif '_CANVAS_' in name or 'CANVAS' in name:
            safe_move(item, s_canvas / name)
        elif 'ECHOES' in name:
            safe_move(item, s_echoes / name)
        elif 'PANOR@MA WING' in name:
            safe_move(item, s_panorma / name)
        elif '円環' in name or 'Halo around' in name:
            safe_move(item, s_halo / name)
        elif 'シャイニーPRオファー' in name:
            safe_move(item, s_collab / name)
        elif 'WING COLLECTION' in name:
            safe_move(item, s_wing / name)
        elif '明日もBeautiful Day' in name or '泡沫に染まる' in name:
            safe_move(item, s_prism / name)

    # C. Consolidate Gakuen Idolmaster: '学園アイドルマスター' -> 'Gakuen Idolmaster (学園アイドルマスター) ~'
    gakumas_canonical = imas_dir / 'Gakuen Idolmaster (学園アイドルマスター) ~'
    gakumas_canonical.mkdir(parents=True, exist_ok=True)

    g_solo = gakumas_canonical / '01. Solo'
    g_duo = gakumas_canonical / '02. Duo'
    g_trio = gakumas_canonical / '03. Trio'
    g_units = gakumas_canonical / '04. All Stars & Units'
    for d in [g_solo, g_duo, g_trio, g_units]:
        d.mkdir(parents=True, exist_ok=True)

    # Merge 'Solo Idol Singles ~' into '01. Solo'
    solo_singles = gakumas_canonical / 'Solo Idol Singles ~'
    if solo_singles.exists():
        for item in list(solo_singles.iterdir()):
            safe_move(item, g_solo / item.name)
        try:
            solo_singles.rmdir()
        except OSError:
            pass

    # Merge 'Unit & Group Singles ~' into '04. All Stars & Units'
    unit_singles = gakumas_canonical / 'Unit & Group Singles ~'
    if unit_singles.exists():
        for item in list(unit_singles.iterdir()):
            safe_move(item, g_units / item.name)
        try:
            unit_singles.rmdir()
        except OSError:
            pass

    # Merge raw '学園アイドルマスター' into canonical
    gakumas_raw = imas_dir / '学園アイドルマスター'
    if gakumas_raw.exists() and gakumas_raw.is_dir():
        log("Merging raw '学園アイドルマスター' into canonical umbrella...")
        # Move loose singles
        gold_rush = gakumas_raw / 'GOLD RUSH 第3巻 オリジナルCD付き特装版'
        if gold_rush.exists():
            safe_move(gold_rush, g_units / gold_rush.name)
        shuraku = gakumas_raw / '修楽旅行 (倉本千奈・紫雲清夏・十王星南・秦谷美鈴 ver.)'
        if shuraku.exists():
            safe_move(shuraku, g_units / shuraku.name)
        # Move series folders
        for item in list(gakumas_raw.iterdir()):
            safe_move(item, gakumas_canonical / item.name)
        try:
            gakumas_raw.rmdir()
        except OSError:
            pass

    # D. Normalize vα-liv -> 'vα-liv (ヴイアライヴ) ~'
    valiv = imas_dir / 'vα-liv'
    if valiv.exists() and valiv.is_dir():
        target_valiv = imas_dir / 'vα-liv (ヴイアライヴ) ~'
        safe_move(valiv, target_valiv)

    log("THE IDOLM@STER fixed successfully.")

# ==============================================================================
# 2. FIX BOCCHI THE ROCK!
# ==============================================================================
def fix_bocchi():
    log("=== FIXING BOCCHI THE ROCK! (結束バンド／ぼっち・ざ・ろっく！) ~ ===")
    bocchi_dir = LOSSLESS_ROOT / 'Anime' / 'Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~'
    if not bocchi_dir.exists():
        return

    physical = bocchi_dir / '[2022-2023] PHYSICAL RELEASES'
    special = bocchi_dir / '[2022-2023] SPECIAL DISCS'
    digital = bocchi_dir / '[2022-2022] DIGITAL SINGLES'
    physical.mkdir(parents=True, exist_ok=True)
    special.mkdir(parents=True, exist_ok=True)
    digital.mkdir(parents=True, exist_ok=True)

    # 1. We will (Mini-Album EP) -> Physical Releases
    we_will = bocchi_dir / 'We will'
    if we_will.exists():
        log("  Moving 'We will' -> [2022-2023] PHYSICAL RELEASES")
        safe_move(we_will, physical / 'We will')

    # 2. Tribute Collection -> Special Discs
    tribute = bocchi_dir / 'ぼっち・ざ・ろっく！ きらら トリビュート コレクション「結束バンドの歌ってみた」'
    if tribute.exists():
        log("  Moving Tribute Collection -> [2022-2023] SPECIAL DISCS")
        safe_move(tribute, special / 'ぼっち・ざ・ろっく！ きらら トリビュート コレクション「結束バンドの歌ってみた」')

    # 3. Vinyl release
    vinyl = bocchi_dir / '結束バンド [Vinyl][SVWJ-70613~4]'
    if vinyl.exists():
        log("  Moving Vinyl Edition -> [2022-2023] PHYSICAL RELEASES/結束バンド (Vinyl Edition)")
        safe_move(vinyl, physical / '結束バンド (Vinyl Edition)')

    log("Bocchi the Rock fixed successfully.")

# ==============================================================================
# 3. FIX UMA MUSUME
# ==============================================================================
def fix_uma_musume():
    log("=== FIXING UMA MUSUME (ウマ娘) ~ ===")
    uma_dir = LOSSLESS_ROOT / 'Anime' / 'Uma Musume (ウマ娘) ~'
    if not uma_dir.exists():
        return

    winning_live = uma_dir / '01. WINNING LIVE Series'
    singles_ost = uma_dir / '06. Singles, OST & Other'
    winning_live.mkdir(parents=True, exist_ok=True)
    singles_ost.mkdir(parents=True, exist_ok=True)

    loose_wl = uma_dir / 'WINNING LIVE Series ~'
    if loose_wl.exists():
        log("  Merging loose 'WINNING LIVE Series ~' into '01. WINNING LIVE Series'")
        for item in list(loose_wl.iterdir()):
            safe_move(item, winning_live / clean_album_title(item.name))
        try:
            loose_wl.rmdir()
        except OSError:
            pass

    loose_ost = uma_dir / 'Singles, OST & Other ~'
    if loose_ost.exists():
        log("  Merging loose 'Singles, OST & Other ~' into '06. Singles, OST & Other'")
        for item in list(loose_ost.iterdir()):
            safe_move(item, singles_ost / clean_album_title(item.name))
        try:
            loose_ost.rmdir()
        except OSError:
            pass

    log("Uma Musume fixed successfully.")

# ==============================================================================
# 4. FIX LOVE LIVE!
# ==============================================================================
def fix_love_live():
    log("=== FIXING LOVE LIVE! (ラブライブ！) ~ ===")
    ll_dir = LOSSLESS_ROOT / 'Anime' / 'Love Live! (ラブライブ！) ~'
    if not ll_dir.exists():
        return

    # Canonical generation folders
    g_hasu = ll_dir / 'Hasunosora (蓮ノ空女学院スクールアイドルクラブ) ~'
    g_niji = ll_dir / 'Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~'
    g_liella = ll_dir / 'Liella! (ラブライブ！スーパースター!!) ~'
    g_aqours = ll_dir / 'Aqours (ラブライブ！サンシャイン!!) ~'
    g_bluebird = ll_dir / 'Bluebird (イキヅライブ！) ~'
    g_series = ll_dir / 'Series & Cross-Generational ~'
    for d in [g_hasu, g_niji, g_liella, g_aqours, g_bluebird, g_series]:
        d.mkdir(parents=True, exist_ok=True)

    # Merge raw '蓮ノ空女学院スクールアイドルクラブ' into canonical
    raw_hasu = ll_dir / '蓮ノ空女学院スクールアイドルクラブ'
    if raw_hasu.exists() and raw_hasu.is_dir():
        for item in list(raw_hasu.iterdir()):
            safe_move(item, g_hasu / item.name)
        try:
            raw_hasu.rmdir()
        except OSError:
            pass

    # Sort loose albums
    for p in list(ll_dir.iterdir()):
        if not p.is_dir():
            continue
        name = p.name
        if name.endswith('~'):
            continue # Generation folder
            
        clean_name = clean_album_title(name)
        if 'イキヅライブ' in name or 'BLUEBIRD' in name or '恋のワンタイムパスワード' in name or '浅草Guilty Girl' in name or 'キミは夜のポラリス' in name:
            safe_move(p, g_bluebird / clean_name)
        elif '蓮ノ空' in name:
            safe_move(p, g_hasu / clean_name)
        elif 'スーパースター' in name or 'Liella' in name:
            safe_move(p, g_liella / clean_name)
        elif 'サンシャイン' in name or 'Aqours' in name:
            safe_move(p, g_aqours / clean_name)
        elif '虹ヶ咲' in name or 'A・ZU・NA' in name or '完結編' in name or 'トキメキの未来地図' in name:
            safe_move(p, g_niji / clean_name)
        elif '異次元フェス' in name or 'AiScReam' in name or 'オフィシャルカードゲーム' in name or '平成ギャルズ' in name or '雪舞う空' in name or 'オレンジのままで' in name:
            safe_move(p, g_series / clean_name)

    log("Love Live fixed successfully.")

# ==============================================================================
# 5. FIX D4DJ
# ==============================================================================
def fix_d4dj():
    log("=== FIXING D4DJ (ディーフォーディージェー) ~ ===")
    d4dj_dir = LOSSLESS_ROOT / 'Anime' / 'D4DJ (ディーフォーディージェー) ~'
    if not d4dj_dir.exists():
        return

    u_happy = d4dj_dir / 'Happy Around! ~'
    u_peaky = d4dj_dir / 'Peaky P-key ~'
    u_photon = d4dj_dir / 'Photon Maiden ~'
    u_merm4id = d4dj_dir / 'Merm4id ~'
    u_lyrical = d4dj_dir / 'Lyrical Lily ~'
    u_unichord = d4dj_dir / 'UniChørd ~'
    u_abyss = d4dj_dir / 'Abyssmare ~'
    u_allstars = d4dj_dir / 'All Stars & Compilations ~'
    for d in [u_happy, u_peaky, u_photon, u_merm4id, u_lyrical, u_unichord, u_abyss, u_allstars]:
        d.mkdir(parents=True, exist_ok=True)

    for p in list(d4dj_dir.iterdir()):
        if not p.is_dir():
            continue
        name = p.name
        if name.endswith('~'):
            continue # Unit folder
            
        clean_name = clean_album_title(name)
        if 'Happy Around' in name or 'ハピアラ' in name:
            safe_move(p, u_happy / clean_name)
        elif 'Lyrical Lily' in name:
            safe_move(p, u_lyrical / clean_name)
        elif 'Merm4id' in name or 'MAX!!!!' in name or 'femmes fatale' in name or 'Get out!' in name or 'FAKE OFF' in name or 'START' in name:
            safe_move(p, u_merm4id / clean_name)
        elif 'Photon Maiden' in name:
            safe_move(p, u_photon / clean_name)
        elif 'Peaky P-key' in name:
            safe_move(p, u_peaky / clean_name)
        elif 'UniCh' in name or 'UniChørd' in name:
            safe_move(p, u_unichord / clean_name)
        elif 'Abyssmare' in name:
            safe_move(p, u_abyss / clean_name)
        else:
            safe_move(p, u_allstars / clean_name)

    log("D4DJ fixed successfully.")

# ==============================================================================
# MAIN RUNNER
# ==============================================================================
def main():
    log("STARTING MASTER STRUCTURAL FIX...")
    fix_idolmaster()
    fix_bocchi()
    fix_uma_musume()
    fix_love_live()
    fix_d4dj()
    
    log("Applying final permissions & rebuilding master catalog...")
    import subprocess
    subprocess.run(['find', str(LOSSLESS_ROOT), '-type', 'd', '-exec', 'chmod', '775', '{}', '+'])
    subprocess.run(['find', str(LOSSLESS_ROOT), '-type', 'f', '-exec', 'chmod', '664', '{}', '+'])
    subprocess.run(['python3', '/mnt/hdd-backup/music/scripts/update_catalog.py'])
    log("MASTER STRUCTURAL FIX COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
