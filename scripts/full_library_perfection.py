#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FULL LIBRARY PERFECTION SCRIPT
Resolves every single structural anomaly across /mnt/hdd-backup/music/Lossless/:
1. Format & date tags stripped, nested archive folders unwrapped.
2. Complete Anime franchise consolidation:
   - THE IDOLM@STER (Shiny Colors subseries unwrap, Gakuen Idolmaster units merge)
   - Love Live! (all generations unified, Nijigaku legacy merged, Bluebird sorted)
   - BanG Dream! (all 80+ loose albums/singles sorted into unit folders)
   - Uma Musume (loose character singles sorted)
   - Girls Band Cry (Togenashi Togeari merged, format tags stripped)
   - D4DJ (Peaky P-key merged)
   - Anime Japanese/Romaji duplicates consolidated
3. Complete Vtuber consolidation:
   - Hololive: all 30+ loose talents merged from Vtuber/ and Vocaloid/, 54 loose singles sorted
   - Nijisanji: all loose talents merged into umbrella, singles sorted
   - RK Music & RIOT MUSIC: talents unified
   - KAMITSUBAKI STUDIO: talents unified, RIM/RiME duplicate merged
   - Kizuna AI merged
4. Vocaloid cleanup: non-Vocaloid idol/J-Pop groups moved to J-Pop
5. J-Pop perfection: album-named artist folders consolidated, Utada Hikaru moved from Anime
6. Permissions (775/664) and full master catalog + M3U8 regeneration
"""

import os
import re
import sys
import shutil
import subprocess
from pathlib import Path

LOSSLESS_ROOT = Path('/mnt/hdd-backup/music/Lossless')

def log(msg):
    print(f"[PERFECTION] {msg}", flush=True)

def safe_move(src: Path, dst: Path):
    """Safely move src to dst. If dst exists as directory, merge contents."""
    if not src.exists():
        return
    if src == dst:
        return

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
            # If same size, remove src
            if src.stat().st_size == dst.stat().st_size:
                try:
                    src.unlink()
                except OSError:
                    pass
                return
            else:
                # rename src
                alt_name = dst.stem + '_alt' + dst.suffix
                safe_move(src, dst.parent / alt_name)
                return

    try:
        shutil.move(str(src), str(dst))
    except Exception as e:
        log(f"  Error moving {src} -> {dst}: {e}")

def clean_album_title(name: str) -> str:
    """Strip brackets, dates, bitrates, audio formats."""
    # Date prefix [YYYY.MM.DD] or [YYYY-MM-DD]
    name = re.sub(r'^\[\d{4}[.\-_]\d{2}[.\-_]\d{2}\]\s*', '', name)
    name = re.sub(r'^\[\d{6}\]\s*', '', name)
    # Tags like [FLAC], (Hi-Res), [24bit/48kHz], etc.
    name = re.sub(r'\[(?:FLAC|MP3|WEB|CD|EAC|Hi-Res|Lossless|24bit|16bit|44\.1kHz|48kHz|96kHz|192kHz|Qobuz|Mora|Ototoy|Vinyl)[^\]]*\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\((?:FLAC|MP3|WEB|CD|EAC|Hi-Res|Lossless|24bit|16bit|44\.1kHz|48kHz|96kHz|192kHz)[^\)]*\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\{[A-Z0-9\-_]+\}\s*\[(?:CD-)?FLAC\][^\s]*', '', name, flags=re.IGNORECASE)
    # Trailing dates like (2023) or [2021.07.21]
    name = re.sub(r'\s*\[\d{4}[.\-_]\d{2}[.\-_]\d{2}\]', '', name)
    # Clean whitespace
    name = re.sub(r'\s+', ' ', name).strip()
    return name

# ==============================================================================
# 1. PURE ALBUM TITLES & UNWRAP NESTED FOLDERS
# ==============================================================================
def stage1_pure_albums():
    log("=== STAGE 1: PURE ALBUM TITLES & UNWRAP NESTED FOLDERS ===")
    
    # Girls Band Cry
    gbc_old = LOSSLESS_ROOT / 'Anime' / 'Girls Band Cry (ガールズバンドクライ) ~' / '[Hi-Res][240424]TVアニメ『ガールズバンドクライ』トゲナシトゲアリ 1stアルバム「棘アリ」'
    if gbc_old.exists():
        safe_move(gbc_old, LOSSLESS_ROOT / 'Anime' / 'Girls Band Cry (ガールズバンドクライ) ~' / '棘アリ')

    # Idoly Pride
    ip_base = LOSSLESS_ROOT / 'Anime' / 'Idoly Pride (アイドリープライド) ~'
    for old_name, new_name in [
        ('Gemstones [初回生産限定盤] [CD][FLAC+CUE+LOG+BK][SMCL-819~20]', 'Gemstones'),
        ('IDOLY PRIDE Collection Album [Chronicle] [CD][FLAC+CUE+LOG+BK][SMCL-877]', 'IDOLY PRIDE Collection Album [Chronicle]')
    ]:
        p = ip_base / old_name
        if p.exists():
            safe_move(p, ip_base / new_name)

    # Doujinshi / Empire Ensemble
    ee_base = LOSSLESS_ROOT / 'Doujinshi' / '帝國交響楽団 (Empire Ensemble) ~'
    for old_name, new_name in [
        ('MILLION HEAD SMASH (2017) [FLAC] {EMPE-0007}', 'MILLION HEAD SMASH'),
        ('気高き者達の碑 {EMPE-0006} [CD-FLAC] (No Log)', '気高き者達の碑'),
        ('艦隊これくしょん CLUB REMIX　-Over The Raging Waves- (2014) [FLAC] {EMPE-0005}', '艦隊これくしょん CLUB REMIX -Over The Raging Waves-')
    ]:
        p = ee_base / old_name
        if p.exists():
            safe_move(p, ee_base / new_name)

    # J-Pop Cleanups
    jpop_renames = [
        (LOSSLESS_ROOT / 'J-Pop' / '7uta ~' / '空に架かる君の声。 {7UTA-0002} [CD-FLAC] (no log)', LOSSLESS_ROOT / 'J-Pop' / '7uta ~' / '空に架かる君の声。'),
        (LOSSLESS_ROOT / 'J-Pop' / 'Armony ~' / 'Armonico [CD-FLAC] (100%)', LOSSLESS_ROOT / 'J-Pop' / 'Armony ~' / 'Armonico'),
        (LOSSLESS_ROOT / 'J-Pop' / 'Motto Music ~' / 'Version (2022) [FLAC] [16B-44.1kHz]', LOSSLESS_ROOT / 'J-Pop' / 'Motto Music ~' / 'Version'),
        (LOSSLESS_ROOT / 'J-Pop' / 'Sennzai (Seardrop) ~' / "L'éveil (2017) [FLAC] {SECD-0002}", LOSSLESS_ROOT / 'J-Pop' / 'Sennzai (Seardrop) ~' / "L'éveil"),
        (LOSSLESS_ROOT / 'J-Pop' / 'Yuiko ~' / 'From GardeN {PRMY-0021} [CD-FLAC] (60%)', LOSSLESS_ROOT / 'J-Pop' / 'Yuiko ~' / 'From GardeN'),
        (LOSSLESS_ROOT / 'J-Pop' / 'アド (Ado) ~' / '魔性少女 [FLAC] Adoプロデュースのアイドルグループ', LOSSLESS_ROOT / 'J-Pop' / 'アド (Ado) ~' / '魔性少女'),
        (LOSSLESS_ROOT / 'J-Pop' / '上白石萌音 (Mone Kamishiraishi) ~' / 'and... (2017) (Hi-Res FLAC) (H13MQ5HDCDED24)', LOSSLESS_ROOT / 'J-Pop' / '上白石萌音 (Mone Kamishiraishi) ~' / 'and...'),
        (LOSSLESS_ROOT / 'J-Pop' / '前田佳織里 ~' / 'Grab the World [CD][FLAC+CUE+LOG+BK][AZCS-1126]', LOSSLESS_ROOT / 'J-Pop' / '前田佳織里 ~' / 'Grab the World'),
        (LOSSLESS_ROOT / 'J-Pop' / '咲良ゆの (Yuno Sakura) ~' / 'Futurize me [WEB-FLAC] [1656662912] [16-44.1]', LOSSLESS_ROOT / 'J-Pop' / '咲良ゆの (Yuno Sakura) ~' / 'Futurize me'),
        (LOSSLESS_ROOT / 'J-Pop' / 'WaMi ~' / 'Loop (feat. WaMi) [2021.02.19]', LOSSLESS_ROOT / 'J-Pop' / 'WaMi ~' / 'Loop (feat. WaMi)'),
        (LOSSLESS_ROOT / 'J-Pop' / '雨宿り (Amayadori) ~' / '傘をなくして [2024.06.06]', LOSSLESS_ROOT / 'J-Pop' / '雨宿り (Amayadori) ~' / '傘をなくして'),
    ]
    for old_p, new_p in jpop_renames:
        if old_p.exists():
            safe_move(old_p, new_p)

    # YUI nested folder unwrap
    yui_dir = LOSSLESS_ROOT / 'J-Pop' / 'YUI ~'
    if yui_dir.exists():
        yui_nested = yui_dir / 'FROM ME TO YOU [FLAC+BK][SRCL-6237]'
        if yui_nested.exists():
            inner = yui_nested / 'FROM ME TO YOU [FLAC+BK][SRCL-6237]'
            target = yui_dir / 'FROM ME TO YOU'
            if inner.exists():
                for item in list(inner.iterdir()):
                    safe_move(item, target / item.name)
            for item in list(yui_nested.iterdir()):
                if item != inner:
                    safe_move(item, target / item.name)
            try:
                shutil.rmtree(str(yui_nested))
            except OSError:
                pass

    # 緑黄色社会 unwrap
    ryoku_dir = LOSSLESS_ROOT / 'J-Pop' / '緑黄色社会 (Ryokuoushoku Shakai) ~'
    if ryoku_dir.exists():
        r_nested = ryoku_dir / 'Hana ni Natte FLAC'
        if r_nested.exists():
            inner = list(r_nested.iterdir())
            target = ryoku_dir / '花になって'
            target.mkdir(parents=True, exist_ok=True)
            for item in inner:
                if item.is_dir():
                    for sub in list(item.iterdir()):
                        safe_move(sub, target / sub.name)
                else:
                    safe_move(item, target / item.name)
            try:
                shutil.rmtree(str(r_nested))
            except OSError:
                pass

    # Vtuber Cleanups
    vtuber_renames = [
        (LOSSLESS_ROOT / 'Vtuber' / 'Hololive (ホロライブ) ~' / 'Tokoyami Towa (常闇トワ) ~' / 'シルベ (2026) [WEB-FLAC 24bit／48kHz]_2',
         LOSSLESS_ROOT / 'Vtuber' / 'Hololive (ホロライブ) ~' / 'Tokoyami Towa (常闇トワ) ~' / 'シルベ'),
        (LOSSLESS_ROOT / 'Vtuber' / 'KAMITSUBAKI STUDIO (神椿スタジオ) ~' / 'RIM (理芽) ~' / 'RIM 理芽 1stアルバム「NEW ROMANCER」[FLAC] [2021.07.21]',
         LOSSLESS_ROOT / 'Vtuber' / 'KAMITSUBAKI STUDIO (神椿スタジオ) ~' / 'RIM (理芽) ~' / 'NEW ROMANCER'),
        (LOSSLESS_ROOT / 'Vtuber' / 'RK Music ~' / 'HACHI ~' / 'Close to heart (2023) [FLAC] {QRM-1005}',
         LOSSLESS_ROOT / 'Vtuber' / 'RK Music ~' / 'HACHI ~' / 'Close to heart'),
    ]
    for old_p, new_p in vtuber_renames:
        if old_p.exists():
            safe_move(old_p, new_p)

    # La Priere BOOTH unwrap
    lapriere = LOSSLESS_ROOT / 'Vtuber' / 'La Prière ~' / '純情アンビバレンス'
    if lapriere.exists():
        booth = lapriere / 'BOOTH(44.1kHz 16bit)'
        if booth.exists():
            for item in list(booth.iterdir()):
                safe_move(item, lapriere / item.name)
            try:
                booth.rmdir()
            except OSError:
                pass

# ==============================================================================
# 2. THE IDOLM@STER (アイドルマスター) ~
# ==============================================================================
def stage2_idolmaster():
    log("=== STAGE 2: THE IDOLM@STER (アイドルマスター) ~ ===")
    imas_dir = LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~'
    shiny = imas_dir / 'Shiny Colors (シャイニーカラーズ) ~'
    gakumas = imas_dir / 'Gakuen Idolmaster (学園アイドルマスター) ~'
    
    s_wing = shiny / '01. WING & Main Game Series'
    s_prism = shiny / '02. Song for Prism Series'
    s_anime = shiny / '03. Anime Series'
    s_collab = shiny / '05. Synthe-Side & Collaborations'
    s_canvas = s_wing / '06. CANVAS'
    s_echoes = s_wing / '07. ECHOES'
    s_panorma = s_wing / '05. PANOR@MA WING'
    s_halo = s_wing / '08. 円環 -Halo around-'

    g_solo = gakumas / '01. Solo'
    g_duo = gakumas / '02. Duo'
    g_trio = gakumas / '03. Trio'
    g_units = gakumas / '04. All Stars & Units'

    # A. Unwrap 01 Borderline.flac folder
    border_dir = shiny / '01 Borderline.flac'
    if border_dir.exists():
        log("  Unwrapping Shiny Colors '01 Borderline.flac'...")
        target_album = s_prism / 'THE IDOLM@STER SHINY COLORS Song for Prism Borderline／クローバー／Summer Night Paradise'
        target_album.mkdir(parents=True, exist_ok=True)
        inner = border_dir / 'THE IDOLM@STER SHINY COLORS Song for Pr'
        if inner.exists():
            for f in list(inner.iterdir()):
                safe_move(f, target_album / f.name)
        for f in list(border_dir.iterdir()):
            if f != inner:
                safe_move(f, target_album / f.name)
        try:
            shutil.rmtree(str(border_dir))
        except OSError:
            pass

    # B. Unwrap -28 colors- COLLECTION
    twenty_eight = shiny / 'THE IDOLM@STER SHINY COLORS -28 colors- COLLECTION'
    if twenty_eight.exists():
        log("  Unwrapping -28 colors- COLLECTION...")
        target_dir = s_wing / 'THE IDOLM@STER SHINY COLORS -28 colors- COLLECTION'
        target_dir.mkdir(parents=True, exist_ok=True)
        # Check deep nested
        deep = twenty_eight / 'シャイニーカラーズ' / 'THE IDOLM@STER SHINY COLORS -28 colors- COLLECTION'
        if deep.exists():
            for item in list(deep.iterdir()):
                safe_move(item, target_dir / item.name)
        for item in list(twenty_eight.iterdir()):
            if item.name != 'シャイニーカラーズ':
                safe_move(item, target_dir / item.name)
        try:
            shutil.rmtree(str(twenty_eight))
        except OSError:
            pass

    # C. Merge loose Shiny Colors unit folders from Anime/
    anime_root = LOSSLESS_ROOT / 'Anime'
    shiny_sources = [
        'シャイニーカラーズ ~', 'アルストロメリア ~', 'アンティーカ ~', 'アンティーカ×シーズ ~',
        'イルミネーションスターズ ~', 'イルミネーションスターズ×ノクチル ~', 'コメティック ~',
        'シーズ ~', 'ストレイライト ~', 'ノクチル ~', '放課後クライマックスガールズ ~',
        '放課後クライマックスガールズ×ストレイライト ~', '大崎甘奈 (CV.黒木ほの香) ~',
        '小宮果穂 (CV.河野ひより) ~', "L'Antica ~"
    ]
    for src_name in shiny_sources:
        p = anime_root / src_name
        if not p.exists():
            continue
        log(f"  Merging Shiny Colors unit: {src_name}...")
        for album in list(p.iterdir()):
            if not album.is_dir():
                safe_move(album, shiny / album.name)
                continue
            aname = album.name
            if 'Song for Prism' in aname or '裸足じゃイラレナイ' in aname or '明日もBeautiful Day' in aname:
                safe_move(album, s_prism / aname)
            elif "''CANVAS''" in aname or 'CANVAS' in aname:
                safe_move(album, s_canvas / aname)
            elif 'ECHOES' in aname:
                safe_move(album, s_echoes / aname)
            elif 'PANOR@MA WING' in aname:
                safe_move(album, s_panorma / aname)
            elif '円環' in aname or 'Halo around' in aname:
                safe_move(album, s_halo / aname)
            elif 'シャイニーPRオファー' in aname:
                safe_move(album, s_collab / aname)
            elif 'WING COLLECTION' in aname:
                safe_move(album, s_wing / aname)
            else:
                safe_move(album, s_wing / aname)
        try:
            p.rmdir()
        except OSError:
            pass

    # D. Merge loose Gakuen Idolmaster units from Anime/
    gakumas_duos = [
        '倉本千奈(CV.伊藤舞音)、篠澤広(CV.川村玲奈) ~',
        '葛城リーリヤ(CV.花岩香奈)、紫雲清夏(CV.湊みや) ~',
    ]
    gakumas_trios = [
        '月村手毬(CV.小鹿なお)、十王星南(CV.陽高真白)、秦谷美鈴(CV.春咲暖) ~',
        '花海佑芽(CV.松田彩音)、秦谷美鈴(CV.春咲暖)、十王星南(CV.陽高真白) ~',
    ]
    gakumas_solos = [
        '十王星南(CV.陽高真白) ~', '姫崎莉波(CV.薄井友里) ~', '月村手毬(CV.小鹿なお) ~',
        '篠澤広(CV.川村玲奈) ~', '花海佑芽(CV.松田彩音) ~', '藤田ことね(CV.飯田ヒカル) ~',
        '雨夜燕(CV.天音ゆかり) ~'
    ]

    for d in gakumas_duos:
        p = anime_root / d
        if p.exists():
            log(f"  Moving Gakumas Duo: {d} -> 02. Duo")
            for item in list(p.iterdir()):
                safe_move(item, g_duo / item.name)
            try: p.rmdir()
            except OSError: pass

    for t in gakumas_trios:
        p = anime_root / t
        if p.exists():
            log(f"  Moving Gakumas Trio: {t} -> 03. Trio")
            for item in list(p.iterdir()):
                safe_move(item, g_trio / item.name)
            try: p.rmdir()
            except OSError: pass

    for s in gakumas_solos:
        p = anime_root / s
        if p.exists():
            log(f"  Moving Gakumas Solo: {s} -> 01. Solo")
            for item in list(p.iterdir()):
                safe_move(item, g_solo / item.name)
            try: p.rmdir()
            except OSError: pass

    # Hatsuboshi Gakuen -> Gakumas units
    hatsuboshi = anime_root / 'Hatsuboshi Gakuen (初星学園) ~'
    if hatsuboshi.exists():
        log("  Moving Hatsuboshi Gakuen -> Gakumas 04. All Stars & Units")
        for item in list(hatsuboshi.iterdir()):
            safe_move(item, g_units / item.name)
        try: hatsuboshi.rmdir()
        except OSError: pass

# ==============================================================================
# 3. LOVE LIVE! (ラブライブ！) ~
# ==============================================================================
def stage3_love_live():
    log("=== STAGE 3: LOVE LIVE! (ラブライブ！) ~ ===")
    ll_dir = LOSSLESS_ROOT / 'Anime' / 'Love Live! (ラブライブ！) ~'
    g_hasu = ll_dir / 'Hasunosora (蓮ノ空女学院スクールアイドルクラブ) ~'
    g_niji = ll_dir / 'Nijigasaki (虹ヶ咲学園スクールアイドル同好会) ~'
    g_liella = ll_dir / 'Liella! (ラブライブ！スーパースター!!) ~'
    g_aqours = ll_dir / 'Aqours (ラブライブ！サンシャイン!!) ~'
    g_bluebird = ll_dir / 'Bluebird (イキヅライブ！) ~'
    g_series = ll_dir / 'Series & Cross-Generational ~'
    for d in [g_hasu, g_niji, g_liella, g_aqours, g_bluebird, g_series]:
        d.mkdir(parents=True, exist_ok=True)

    # Sub-units in Nijigasaki
    u_azuna = g_niji / 'A・ZU・NA ~'
    u_diver = g_niji / 'DiverDiva ~'
    u_qu4rtz = g_niji / 'QU4RTZ ~'
    u_r3birth = g_niji / 'R3BIRTH ~'
    for u in [u_azuna, u_diver, u_qu4rtz, u_r3birth]:
        u.mkdir(parents=True, exist_ok=True)

    # Merge duplicates in Love Live generations
    dup_gens = [
        ('Ikizuraibu! (イキヅライブ！) ~', g_bluebird),
        ('Liella! ~', g_liella),
        ('Special & Crossover Units ~', g_series),
    ]
    for old_g, new_g in dup_gens:
        p = ll_dir / old_g
        if p.exists():
            log(f"  Merging duplicate Love Live generation: {old_g} -> {new_g.name}...")
            safe_move(p, new_g)

    # A. Merge Anime/朝香果林... ~ into Nijigasaki
    anime_root = LOSSLESS_ROOT / 'Anime'
    karin_unit = anime_root / '朝香果林(CV.久保田未夢)、近江彼方(CV.鬼頭明里)、エマ・ヴェルデ(CV.指出毬亜)、ミア・テイラー(CV.内田秀) ~'
    if karin_unit.exists():
        for item in list(karin_unit.iterdir()):
            safe_move(item, g_niji / clean_album_title(item.name))
        try: karin_unit.rmdir()
        except OSError: pass

    # B. Merge School Idol Musical
    musical = anime_root / 'スクールアイドルミュージカル ~'
    if musical.exists():
        target_mus = ll_dir / 'School Idol Musical (スクールアイドルミュージカル) ~'
        safe_move(musical, target_mus)

    # C. Merge Nijigaku legacy folder
    nijigaku_legacy = ll_dir / 'Nijigaku'
    if nijigaku_legacy.exists():
        log("  Merging legacy 'Nijigaku' into Nijigasaki...")
        # Sub-units
        sub_units = nijigaku_legacy / 'Sub-Units'
        if sub_units.exists():
            for item in list(sub_units.iterdir()):
                iname = item.name
                if 'A・ZU・NA' in iname or 'AZUNA' in iname:
                    safe_move(item, u_azuna)
                elif 'DiverDiva' in iname:
                    safe_move(item, u_diver)
                elif 'QU4RTZ' in iname:
                    safe_move(item, u_qu4rtz)
                elif 'R3BIRTH' in iname:
                    safe_move(item, u_r3birth)
                else:
                    safe_move(item, g_niji / clean_album_title(iname))
            try: sub_units.rmdir()
            except OSError: pass

        for item in list(nijigaku_legacy.iterdir()):
            safe_move(item, g_niji / clean_album_title(item.name))
        try: nijigaku_legacy.rmdir()
        except OSError: pass

    # D. Move all 20 loose albums in Love Live
    bluebird_titles = [
        'Public Style', 'Little Green委員会', 'HIBANA―火花―', 'Pray for love',
        'イキタクナイevery day', 'HomeRun Queen!!', 'いつか碧', 'IcHiGo milK love'
    ]
    for p in list(ll_dir.iterdir()):
        if not p.is_dir() or p.name.endswith('~'):
            continue
        pname = p.name
        cname = clean_album_title(pname)
        if any(bt in pname for bt in bluebird_titles):
            safe_move(p, g_bluebird / cname)
        elif 'NIJIGAKU' in pname or 'White Delight' in pname or 'Dress Code' in pname or 'SUMMER WARNING' in pname or 'Starry Night Serenade' in pname or '酸欠' in pname:
            safe_move(p, g_niji / cname)
        elif 'Fourth Solo Concert' in pname or 'WAKE：WOKE' in pname or 'BURN：BORN' in pname:
            safe_move(p, g_aqours / cname)
        elif 'はじまりの羽音' in pname:
            safe_move(p, g_hasu / cname)
        else:
            safe_move(p, g_series / cname)

# ==============================================================================
# 4. BANG DREAM! (バンドリ！) ~
# ==============================================================================
def stage4_bang_dream():
    log("=== STAGE 4: BANG DREAM! (バンドリ！) ~ ===")
    bang_dir = LOSSLESS_ROOT / 'Anime' / 'BanG Dream! (バンドリ！) ~'
    if not bang_dir.exists():
        return

    # Canonical Unit folders
    u_popipa = bang_dir / "Poppin'Party ~"
    u_roselia = bang_dir / 'Roselia ~'
    u_afterglow = bang_dir / 'Afterglow ~'
    u_pasupare = bang_dir / 'Pastel＊Palettes ~'
    u_harohapi = bang_dir / 'Hello, Happy World! (ハロー、ハッピーワールド！) ~'
    u_morfonica = bang_dir / 'Morfonica ~'
    u_ras = bang_dir / 'RAISE A SUILEN ~'
    u_mygo = bang_dir / 'MyGO!!!!! ~'
    u_ave = bang_dir / 'Ave Mujica ~'
    u_mew = bang_dir / 'Mugendai Mewtype (夢限大みゅーたいぷ) ~'
    u_millsage = bang_dir / 'millsage ~'
    u_comp = bang_dir / 'Compilations & Cover Collections ~'
    u_ikka = bang_dir / 'Ikka Dumb Rock (一家Dumb Rock!) ~'
    u_collab = bang_dir / 'Parallel & Collab Singles ~'

    for d in [u_popipa, u_roselia, u_afterglow, u_pasupare, u_harohapi, u_morfonica,
              u_ras, u_mygo, u_ave, u_mew, u_millsage, u_comp, u_ikka, u_collab]:
        d.mkdir(parents=True, exist_ok=True)

    # Merge duplicates outside and inside
    anime_root = LOSSLESS_ROOT / 'Anime'
    outer_mygo = anime_root / 'MyGO!!!!! ~'
    if outer_mygo.exists():
        log("  Merging outer MyGO!!!!! into BanG Dream...")
        for item in list(outer_mygo.iterdir()):
            safe_move(item, u_mygo / clean_album_title(item.name))
        try: outer_mygo.rmdir()
        except OSError: pass

    inner_mygo_raw = bang_dir / 'MyGO!!!!!'
    if inner_mygo_raw.exists():
        for item in list(inner_mygo_raw.iterdir()):
            safe_move(item, u_mygo / clean_album_title(item.name))
        try: inner_mygo_raw.rmdir()
        except OSError: pass

    inner_ave_raw = bang_dir / 'Ave Mujica'
    if inner_ave_raw.exists():
        for item in list(inner_ave_raw.iterdir()):
            safe_move(item, u_ave / clean_album_title(item.name))
        try: inner_ave_raw.rmdir()
        except OSError: pass

    # Sort all loose albums/singles in BanG Dream root
    for p in list(bang_dir.iterdir()):
        if not p.is_dir() or p.name.endswith('~'):
            continue
        pname = p.name
        cname = clean_album_title(pname)
        
        # Identify unit
        if 'Ave Mujica' in pname or 'Crucifix X' in pname or 'Imprisoned XII' in pname or '天球のMúsica' in pname or '顔' in pname or 'DIVINE' in pname or '碧い瞳の中に' in pname:
            safe_move(p, u_ave / cname)
        elif 'MyGO' in pname or '跡暖空' in pname or '致並跡' in pname or '静降想' in pname or 'だれかの心臓になれたなら' in pname or 'エガクミライ' in pname or '証命讃歌' in pname or '過去を喰らう' in pname or '霧周途' in pname:
            safe_move(p, u_mygo / cname)
        elif 'Morfonica' in pname or 'Polyphony' in pname or 'Tempest' in pname or 'Resonant Strings' in pname or 'Polyphonyscape' in pname or 'ビューティ・フォー' in pname or 'メロウ' in pname or '胡蝶翔る星月夜' in pname:
            safe_move(p, u_morfonica / cname)
        elif "Poppin'Party" in pname or 'POPIGENIC' in pname or 'START!! True dreams' in pname or 'MATSURI BAYASHI' in pname:
            safe_move(p, u_popipa / cname)
        elif 'Roselia' in pname or 'Lehre der Rose' in pname or 'Dazzle the Destiny' in pname or 'Requiem for Fate' in pname or 'Floral Haven' in pname or 'HONEY' in pname or 'XV' in pname or 'この蒼き闇と光' in pname:
            safe_move(p, u_roselia / cname)
        elif 'Afterglow' in pname or 'DAY×DAY' in pname or 'STAY GLOW' in pname or '忘れらんない日々のこと' in pname:
            safe_move(p, u_afterglow / cname)
        elif 'Pastel' in pname or 'きみと Stage by Stage' in pname or 'Pastel à la mode' in pname or '♡桃色片想い♡' in pname or 'いろとりどり' in pname or '金曜日のおはよう' in pname:
            safe_move(p, u_pasupare / cname)
        elif 'ハロー、ハッピーワールド' in pname or 'Hello, Happy World' in pname or 'SMILE ON PARADE' in pname or 'どうしたってカーニバル' in pname or 'スマイリーキャロル' in pname or '許婚っきゅん' in pname:
            safe_move(p, u_harohapi / cname)
        elif 'RAISE A SUILEN' in pname or 'Bad Kids All Bet' in pname or '革命道中' in pname:
            safe_move(p, u_ras / cname)
        elif 'みゅーたいぷ' in pname or 'むーたいぷ' in pname or 'Hi-Vision' in pname or '超惑星Xへの旅' in pname or 'Calling' in pname or 'Face The Next' in pname or 'TRASH LIFE' in pname or 'TearJerker' in pname or 'in my words' in pname or 'うちゅうのふしぎ' in pname or 'これはぼくたちの生存のあらすじ' in pname or 'にこいちミライ' in pname or 'コハク' in pname or 'チューニング' in pname or '一番のひかり' in pname or '愛は衝動' in pname:
            safe_move(p, u_mew / cname)
        elif 'millsage' in pname or 'everscape' in pname or 'カーネーションの咲く日に' in pname or '起死開戦' in pname:
            safe_move(p, u_millsage / cname)
        elif 'カバーコレクション' in pname or 'Cover Collection' in pname:
            safe_move(p, u_comp / cname)
        elif 'Dumb Rock' in pname or 'Keep on Riddim' in pname or 'Mela!' in pname or 'ジャイアント・キラー・チューン' in pname or 'ホーミー・タイッ' in pname:
            safe_move(p, u_ikka / cname)
        else:
            safe_move(p, u_collab / cname)

# ==============================================================================
# 5. UMA MUSUME, GIRLS BAND CRY, D4DJ & ANIME DUPLICATES
# ==============================================================================
def stage5_anime_cleanups():
    log("=== STAGE 5: UMA MUSUME, GIRLS BAND CRY, D4DJ & ANIME DUPLICATES ===")
    anime_root = LOSSLESS_ROOT / 'Anime'

    # Uma Musume loose seiyuu folders
    uma_dir = anime_root / 'Uma Musume (ウマ娘) ~'
    uma_singles = uma_dir / '06. Singles, OST & Other'
    uma_singles.mkdir(parents=True, exist_ok=True)
    uma_loose_artists = [
        'トウカイテイオー(CV.Machico)、オグリキャップ(CV.高柳知葉)、ゴールドシップ(CV.上田瞳)、スティルインラブ(CV.宮下早紀)、アーモンドアイ(CV.石原夏織) ~',
        'ファインモーション(CV.橋本ちなみ)、ダンツフレーム(CV.福嶋晴菜)、ビリーヴ(CV.秋山実咲)、ラインクラフト(CV.小島菜々恵)、カルストンライトオ(CV.望月ゆみこ)、デュランダル(CV.野木奏) ~',
        'ファインモーション(CV.橋本ちなみ)、メイショウドトウ(CV.和多田美咲)、ナイスネイチャ(CV.前田佳織里)、ナリタトップロード(CV.中村カンナ)、カルストンライトオ(CV.望月ゆみこ) ~'
    ]
    for artist_folder in uma_loose_artists:
        p = anime_root / artist_folder
        if p.exists():
            log(f"  Moving Uma Musume character single: {artist_folder}...")
            for album in list(p.iterdir()):
                safe_move(album, uma_singles / clean_album_title(album.name))
            try: p.rmdir()
            except OSError: pass

    # Girls Band Cry / Togenashi Togeari
    togenashi = anime_root / 'Togenashi Togeari (トゲナシトゲアリ) ~'
    gbc_dir = anime_root / 'Girls Band Cry (ガールズバンドクライ) ~'
    gbc_dir.mkdir(parents=True, exist_ok=True)
    if togenashi.exists():
        log("  Merging Togenashi Togeari into Girls Band Cry...")
        for item in list(togenashi.iterdir()):
            safe_move(item, gbc_dir / clean_album_title(item.name))
        try: togenashi.rmdir()
        except OSError: pass

    # D4DJ / Peaky P-key
    peaky = anime_root / 'Peaky P-key ~'
    d4dj_peaky = anime_root / 'D4DJ (ディーフォーディージェー) ~' / 'Peaky P-key ~'
    if peaky.exists():
        log("  Merging Peaky P-key into D4DJ...")
        for item in list(peaky.iterdir()):
            safe_move(item, d4dj_peaky / clean_album_title(item.name))
        try: peaky.rmdir()
        except OSError: pass

    # Duplicate Anime folders (Japanese vs Romaji)
    duplicates = [
        ('うたの☆プリンセスさまっ♪ ~', 'Uta no Princess-sama (うたの☆プリンセスさまっ♪) ~'),
        ('ワールドダイスター ~', 'World Dai Star (ワールドダイスター) ~'),
        ('前橋ウィッチーズ ~', 'Maebashi Witches (前橋ウィッチーズ) ~'),
        ('ポールプリンセス!! ~', 'Pole Princess!! (ポールプリンセス!!) ~'),
        ('響け！ユーフォニアム ~', 'Sound! Euphonium (響け！ユーフォニアム) ~'),
    ]
    for raw_jp, canonical in duplicates:
        src = anime_root / raw_jp
        dst = anime_root / canonical
        if src.exists():
            log(f"  Merging anime duplicate: {raw_jp} -> {canonical}...")
            for item in list(src.iterdir()):
                safe_move(item, dst / clean_album_title(item.name))
            try: src.rmdir()
            except OSError: pass

# ==============================================================================
# 6. VTUBER (HOLOLIVE, NIJISANJI, KAMITSUBAKI, RK MUSIC)
# ==============================================================================
def stage6_vtuber():
    log("=== STAGE 6: VTUBER UNIFICATION ===")
    v_root = LOSSLESS_ROOT / 'Vtuber'
    voc_root = LOSSLESS_ROOT / 'Vocaloid'

    holo_dir = v_root / 'Hololive (ホロライブ) ~'
    niji_dir = v_root / 'Nijisanji (にじさんじ) ~'
    kami_dir = v_root / 'KAMITSUBAKI STUDIO (神椿スタジオ) ~'
    rk_dir = v_root / 'RK Music ~'
    riot_dir = v_root / 'RIOT MUSIC ~'

    for d in [holo_dir, niji_dir, kami_dir, rk_dir, riot_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # A. Hololive in Vocaloid
    voc_holo = [
        ('Cecilia Immergreen ~', holo_dir / 'Cecilia Immergreen ~'),
        ('Cecilia Immergreen & Gigi Murin ~', holo_dir / 'Cecilia Immergreen ~'),
        ('Elizabeth Rose Bloodflame, Raora Panthera, Cecilia Immergreen, Gigi Murin ~', holo_dir / 'Hololive Official ~'),
        ('Takanashi Kiara ~', holo_dir / 'Takanashi Kiara ~'),
        ('Takanashi Kiara, Hakos Baelz, Koseki Bijou & Raora Panthera ~', holo_dir / 'Hololive Official ~'),
        ('Vestia Zeta ~', holo_dir / 'Vestia Zeta ~'),
    ]
    for src_name, dst_path in voc_holo:
        src = voc_root / src_name
        if src.exists():
            log(f"  Rescuing Hololive talent from Vocaloid: {src_name}...")
            safe_move(src, dst_path)

    # B. Hololive loose talents in Vtuber/
    holo_loose_talents = [
        ('AZKi & 鈴木このみ ~', holo_dir / 'AZKi ~'),
        ('Azki ~', holo_dir / 'AZKi ~'),
        ('BABACORN(宝鐘マリン／白上フブキ) ~', holo_dir / 'Hololive Official ~'),
        ('FLOW GLOW ~', holo_dir / 'FLOW GLOW ~'),
        ('FUWAMOCO ~', holo_dir / 'FUWAMOCO ~'),
        ('Hakos Baelz ~', holo_dir / 'Hakos Baelz ~'),
        ('Hakui Koyori (博衣こより) ~', holo_dir / 'Hakui Koyori (博衣こより) ~'),
        ('博衣こより (Hakui Koyori) ~', holo_dir / 'Hakui Koyori (博衣こより) ~'),
        ('Inugami Korone (戌神ころね) ~', holo_dir / 'Inugami Korone (戌神ころね) ~'),
        ('戌神ころね (Inugami Korone) ~', holo_dir / 'Inugami Korone (戌神ころね) ~'),
        ('Momosuzu Nene (桃鈴ねね) ~', holo_dir / 'Momosuzu Nene (桃鈴ねね) ~'),
        ('桃鈴ねね (Nene Momosuzu) ~', holo_dir / 'Momosuzu Nene (桃鈴ねね) ~'),
        ('Mori Calliope ~', holo_dir / 'Mori Calliope ~'),
        ('Mori Calliope, IRyS & Hakos Baelz ~', holo_dir / 'Mori Calliope ~'),
        ('Nekomata Okayu (猫又おかゆ) ~', holo_dir / 'Nekomata Okayu (猫又おかゆ) ~'),
        ('Nerissa Ravencroft ~', holo_dir / 'Nerissa Ravencroft ~'),
        ('Ouro Kronii ~', holo_dir / 'Ouro Kronii ~'),
        ('Raora Panthera ~', holo_dir / 'Raora Panthera ~'),
        ('ReGLOSS & 轟はじめ ~', holo_dir / 'ReGLOSS ~'),
        ('ReGLOSS ~', holo_dir / 'ReGLOSS ~'),
        ('ReGLOSS, 音乃瀬奏, 一条莉々華 ~', holo_dir / 'ReGLOSS ~'),
        ('Sakura Miko (さくらみこ) ~', holo_dir / 'Sakura Miko (さくらみこ) ~'),
        ('さくらみこ (Sakura Miko) ~', holo_dir / 'Sakura Miko (さくらみこ) ~'),
        ('Shirakami Fubuki (白上フブキ) ~', holo_dir / 'Shirakami Fubuki (白上フブキ) ~'),
        ('白上フブキ (Shirakami Fubuki) ~', holo_dir / 'Shirakami Fubuki (白上フブキ) ~'),
        ('Shishiro Botan (獅白ぼたん) ~', holo_dir / 'Shishiro Botan (獅白ぼたん) ~'),
        ('獅白ぼたん ~', holo_dir / 'Shishiro Botan (獅白ぼたん) ~'),
        ('SorAZ ~', holo_dir / 'SorAZ ~'),
        ('Tokino Sora (ときのそら) ~', holo_dir / 'Tokino Sora (ときのそら) ~'),
        ('ときのそら (Tokino Sora) ~', holo_dir / 'Tokino Sora (ときのそら) ~'),
        ('Tsunomaki Watame (角巻わため) ~', holo_dir / 'Tsunomaki Watame (角巻わため) ~'),
        ('角巻わため (Tsunomaki Watame) ~', holo_dir / 'Tsunomaki Watame (角巻わため) ~'),
        ('Yuzuki Choco (癒月ちょこ) ~', holo_dir / 'Yuzuki Choco (癒月ちょこ) ~'),
        ('miComet ~', holo_dir / 'miComet ~'),
        ('ホロウィッチ! (HoloWitches) ~', holo_dir / 'ホロウィッチ! (HoloWitches) ~'),
        ('大神ミオ (Mio Ookami) ~', holo_dir / 'Ookami Mio (大神ミオ) ~'),
        ('天音かなた (Kanata Amane) ~', holo_dir / 'Amane Kanata (天音かなた) ~'),
        ('宝鐘マリン (Marine Houshou) ~', holo_dir / 'Houshou Marine (宝鐘マリン) ~'),
        ('常闇トワ (Towa Tokoyami) ~', holo_dir / 'Tokoyami Towa (常闇トワ) ~'),
        ('白銀ノエル ~', holo_dir / 'Shirogane Noel (白銀ノエル) ~'),
        ('紫咲シオン (Murasaki Shion) ~', holo_dir / 'Murasaki Shion (紫咲シオン) ~'),
        ('赤井はあと (Haato Akai) ~', holo_dir / 'Akai Haato (赤井はあと) ~'),
        ('鷹嶺ルイ (Takane Lui) ~', holo_dir / 'Takane Lui (鷹嶺ルイ) ~'),
    ]
    for src_name, dst_path in holo_loose_talents:
        src = v_root / src_name
        if src.exists():
            log(f"  Moving Hololive talent to umbrella: {src_name}...")
            safe_move(src, dst_path)

    # C. Sort loose singles inside Hololive (ホロライブ) ~
    holo_off = holo_dir / 'Hololive Official ~'
    holo_off.mkdir(parents=True, exist_ok=True)
    regloss_dir = holo_dir / 'ReGLOSS ~'
    calli_dir = holo_dir / 'Mori Calliope ~'
    marine_dir = holo_dir / 'Houshou Marine (宝鐘マリン) ~'
    raden_dir = holo_dir / 'Juufuutei Raden (儒烏風亭らでん) ~'
    watame_dir = holo_dir / 'Tsunomaki Watame (角巻わため) ~'
    kanata_dir = holo_dir / 'Amane Kanata (天音かなた) ~'
    shion_dir = holo_dir / 'Murasaki Shion (紫咲シオン) ~'
    iroha_dir = holo_dir / 'Kazama Iroha (風真いろは) ~'
    mio_dir = holo_dir / 'Ookami Mio (大神ミオ) ~'

    for p in list(holo_dir.iterdir()):
        if not p.is_dir() or p.name.endswith('~'):
            continue
        pname = p.name
        cname = clean_album_title(pname)
        if 'ReGLOSS' in pname or '音乃瀬奏' in pname or '一条莉々華' in pname or '火威青' in pname or 'サクラミラージュ' in pname or 'シンメトリー' in pname or 'フィーリングラデーション' in pname or 'ミッドサマーシトラス' in pname or '泡沫メイビー' in pname or 'アワータイムイエロー' in pname:
            safe_move(p, regloss_dir / cname)
        elif 'Mori Calliope' in pname or 'UnAlive' in pname or 'FLASH BANG' in pname:
            safe_move(p, calli_dir / cname)
        elif '宝鐘マリン' in pname or 'Ahoy' in pname or pname == 'I I I':
            safe_move(p, marine_dir / cname)
        elif '儒烏風亭らでん' in pname or 'しめじダンス' in pname:
            safe_move(p, raden_dir / cname)
        elif '角巻わため' in pname or 'Now on step' in pname or 'amazing swing' in pname:
            safe_move(p, watame_dir / cname)
        elif '天音かなた' in pname or 'Knock it out!' in pname or 'START UP' in pname or '純粋心' in pname:
            safe_move(p, kanata_dir / cname)
        elif '紫咲シオン' in pname or 'ゴメンねメディスン' in pname:
            safe_move(p, shion_dir / cname)
        elif '風真いろは' in pname or 'ハードモード' in pname:
            safe_move(p, iroha_dir / cname)
        elif '大神ミオ' in pname or '小心旅行' in pname:
            safe_move(p, mio_dir / cname)
        else:
            safe_move(p, holo_off / cname)

    # D. Nijisanji loose talents
    niji_loose = [
        ('Higuchi Kaede (樋口楓) ~', niji_dir / 'Higuchi Kaede (樋口楓) ~'),
        ('樋口楓 (Higuchi Kaede) ~', niji_dir / 'Higuchi Kaede (樋口楓) ~'),
        ('星川サラ (Sara Hoshikawa) ~', niji_dir / 'Hoshikawa Sara (星川サラ) ~'),
        ('月ノ美兎 (Tsukino Mito) ~', niji_dir / 'Tsukino Mito (月ノ美兎) ~'),
        ('本間ひまわり (Himawari Honma) ~', niji_dir / 'Honma Himawari (本間ひまわり) ~'),
        ('町田ちま (Machita Chima) ~', niji_dir / 'Machita Chima (町田ちま) ~'),
        ('葉加瀬冬雪 (Hakase Fuyuki) ~', niji_dir / 'Hakase Fuyuki (葉加瀬冬雪) ~'),
        ('Nornis ~', niji_dir / 'Nornis ~'),
    ]
    for src_name, dst_path in niji_loose:
        src = v_root / src_name
        if src.exists():
            log(f"  Moving Nijisanji talent to umbrella: {src_name}...")
            safe_move(src, dst_path)

    # E. RK Music / RIOT MUSIC
    rk_loose = [
        ('KMNZ ~', rk_dir / 'KMNZ ~'),
        ('MEDA ~', rk_dir / 'MEDA ~'),
        ('VESPERBELL ~', rk_dir / 'VESPERBELL ~'),
        ('瀬戸乃とと ~', rk_dir / 'Setono Toto (瀬戸乃とと) ~'),
        ('水瀬 凪 (MINASE Nagi) ~', rk_dir / 'Minase Nagi (水瀬凪) ~'),
        ('涼海ネモ (Suzumi Nemo) ~', rk_dir / 'Suzumi Nemo (涼海ネモ) ~'),
    ]
    for src_name, dst_path in rk_loose:
        src = v_root / src_name
        if src.exists():
            safe_move(src, dst_path)

    # Suzuna Nagihara
    for p in v_root.glob('*Suzuna Nagihara*'):
        if p.is_dir():
            safe_move(p, riot_dir / 'Nagihara Suzuna (凪原涼菜) ~')

    # F. KAMITSUBAKI STUDIO
    kami_loose = [
        ('CIEL ~', kami_dir / 'CIEL ~'),
        ('Guiano ~', kami_dir / 'Guiano ~'),
        ('存流 (ARU) ~', kami_dir / 'ARU (存流) ~'),
        ('明透 (ASU) ~', kami_dir / 'ASU (明透) ~'),
    ]
    for src_name, dst_path in kami_loose:
        src = v_root / src_name
        if src.exists():
            safe_move(src, dst_path)

    # RIM / RiME duplicate
    rime = kami_dir / 'RiME (理芽) ~'
    rim = kami_dir / 'RIM (理芽) ~'
    if rime.exists():
        safe_move(rime, rim)

    # G. Kizuna AI
    kizuna_voc = voc_root / 'Kizuna AI ~'
    kizuna_vt = v_root / 'Kizuna AI ~'
    if kizuna_voc.exists():
        safe_move(kizuna_voc, kizuna_vt)

# ==============================================================================
# 7. DOUJINSHI DUPLICATE CONSOLIDATION
# ==============================================================================
def stage7_doujinshi():
    log("=== STAGE 7: DOUJINSHI DUPLICATE CONSOLIDATION ===")
    d_root = LOSSLESS_ROOT / 'Doujinshi'
    v_root = LOSSLESS_ROOT / 'Vtuber'

    # La Priere from Doujinshi to Vtuber
    la_priere_doujin = d_root / 'La prière ~'
    la_priere_vtuber = v_root / 'La Prière ~'
    if la_priere_doujin.exists():
        log("  Merging Doujinshi 'La prière ~' into 'Vtuber/La Prière ~'...")
        safe_move(la_priere_doujin, la_priere_vtuber)

    # Natsume Itsuki duplicate in Doujinshi
    itsuki_jp = d_root / '棗いつき (Itsuki Natsume) ~'
    itsuki_canon = d_root / 'Natsume Itsuki (棗いつき) ~'
    if itsuki_jp.exists():
        log("  Merging '棗いつき (Itsuki Natsume) ~' into 'Natsume Itsuki (棗いつき) ~'...")
        safe_move(itsuki_jp, itsuki_canon)

    # nayuta duplicate in Doujinshi
    seven_uta = d_root / '7uta.com (nayuta) ~'
    nayuta_canon = d_root / 'nayuta ~'
    if seven_uta.exists():
        log("  Merging '7uta.com (nayuta) ~' into 'nayuta ~'...")
        safe_move(seven_uta, nayuta_canon)

# ==============================================================================
# 8. VOCALOID MISPLACED ARTISTS -> J-POP
# ==============================================================================
def stage8_vocaloid_to_jpop():
    log("=== STAGE 8: VOCALOID MISPLACED ARTISTS -> J-POP ===")
    voc_root = LOSSLESS_ROOT / 'Vocaloid'
    jpop_root = LOSSLESS_ROOT / 'J-Pop'

    misplaced = [
        ('ASIAN KUNG-FU GENERATION ~', jpop_root / 'ASIAN KUNG-FU GENERATION ~'),
        ('Official HIGE DANdism (Official髭男dism) ~', jpop_root / 'Official HIGE DANdism (Official髭男dism) ~'),
        ('DIALOGUE+ ~', jpop_root / 'DIALOGUE+ ~'),
        ('SKE48 ~', jpop_root / 'SKE48 ~'),
        ('STU48 ~', jpop_root / 'STU48 ~'),
        ('乃木坂46 ~', jpop_root / '乃木坂46 ~'),
        ('僕が見たかった青空 ~', jpop_root / '僕が見たかった青空 ~'),
        ('宮本佳林 ~', jpop_root / 'Miyamoto Karin (宮本佳林) ~'),
        ('りんご娘 ~', jpop_root / 'Ringo Musume (りんご娘) ~'),
    ]
    for src_name, dst_path in misplaced:
        src = voc_root / src_name
        if src.exists():
            log(f"  Moving misplaced Vocaloid folder to J-Pop: {src_name}...")
            safe_move(src, dst_path)

# ==============================================================================
# 9. J-POP ALBUM-NAMED ARTIST CONSOLIDATIONS & UTADA HIKARU
# ==============================================================================
def stage9_jpop_cleanups():
    log("=== STAGE 9: J-POP ARTIST CONSOLIDATIONS & UTADA HIKARU ===")
    jpop_root = LOSSLESS_ROOT / 'J-Pop'
    anime_root = LOSSLESS_ROOT / 'Anime'

    # Move Utada Hikaru from Anime -> J-Pop
    utada_anime = anime_root / '宇多田ヒカル ~'
    utada_jpop = jpop_root / 'Utada Hikaru (宇多田ヒカル) ~'
    if utada_anime.exists():
        log("  Moving Utada Hikaru from Anime to J-Pop...")
        safe_move(utada_anime, utada_jpop)

    # Yohane single from J-Pop to Love Live
    yohane = jpop_root / '劇場総集編 幻日のヨハネ -SUNSHINE in the MIRROR- オリジナルソングCD「ふたりでひとつ」[FLAC] ~'
    if yohane.exists():
        log("  Moving Genjitsu no Yohane single to Love Live Aqours...")
        dest = LOSSLESS_ROOT / 'Anime' / 'Love Live! (ラブライブ！) ~' / 'Aqours (ラブライブ！サンシャイン!!) ~' / 'ふたりでひとつ'
        safe_move(yohane, dest)

    # Suisoh (水槽)
    suisoh_canon = jpop_root / 'Suisoh (水槽) ~'
    suisoh_raw = jpop_root / '水槽 ~'
    suisoh_album = jpop_root / '水槽 4thアルバム「FLTR」[FLAC 48kHz ~'
    if suisoh_raw.exists():
        safe_move(suisoh_raw, suisoh_canon)
    if suisoh_album.exists():
        safe_move(suisoh_album, suisoh_canon / 'FLTR')

    # Yanagi Nagi (やなぎなぎ)
    yanagi_canon = jpop_root / 'Yanagi Nagi (やなぎなぎ) ~'
    yanagi_raw = jpop_root / 'やなぎなぎ ~'
    yanagi_album = jpop_root / 'やなぎなぎ 20周年記念アルバム「ENcore」[FLAC] ~'
    if yanagi_raw.exists():
        safe_move(yanagi_raw, yanagi_canon)
    if yanagi_album.exists():
        safe_move(yanagi_album, yanagi_canon / 'ENcore')

    # Aoki Hina (青木陽菜)
    aoki_canon = jpop_root / 'Aoki Hina (青木陽菜) ~'
    aoki_raw = jpop_root / '青木陽菜 ~'
    aoki_album = jpop_root / '青木陽菜 1stアルバム「Letters」[FLAC 96kHz ~'
    if aoki_raw.exists():
        safe_move(aoki_raw, aoki_canon)
    if aoki_album.exists():
        safe_move(aoki_album, aoki_canon / 'Letters')

    # Maejima Ami (前島亜美)
    ami_canon = jpop_root / 'Maejima Ami (前島亜美) ~'
    ami_raw = jpop_root / '前島亜美 ~'
    ami_album = jpop_root / '前島亜美 1stアルバム「Determination」[FLAC 96kHz ~'
    if ami_raw.exists():
        safe_move(ami_raw, ami_canon)
    if ami_album.exists():
        safe_move(ami_album, ami_canon / 'Determination')

    # Inami Anju (伊波杏樹)
    anju_canon = jpop_root / 'Inami Anju (伊波杏樹) ~'
    anju_album = jpop_root / '伊波杏樹 1stアルバム「Fiesta」[FLAC 48kHz ~'
    if anju_album.exists():
        safe_move(anju_album, anju_canon / 'Fiesta')

    # Tomita Miyu (富田美憂)
    tomita_canon = jpop_root / 'Tomita Miyu (富田美憂) ~'
    tomita_album = jpop_root / '富田美憂 2ndアルバムViolet Bullet」[FLAC 96kHz ~'
    if tomita_album.exists():
        safe_move(tomita_album, tomita_canon / 'Violet Bullet')

    # mona
    mona_canon = jpop_root / 'mona (CV 夏川椎菜) ~'
    mona_album = jpop_root / 'mona 2ndアルバム超絶あざといお前らの姫」[FLAC 48kHz ~'
    if mona_album.exists():
        safe_move(mona_album, mona_canon / '超絶あざといお前らの姫')

    # fhana
    fhana_canon = jpop_root / 'fhana (fhána) ~'
    fhana_album = jpop_root / 'fhána 5thアルバム「The Look of Life」[FLAC 96kHz ~'
    if fhana_album.exists():
        safe_move(fhana_album, fhana_canon / 'The Look of Life')

    # Nakae Mitsuki (中恵光城)
    nakae_canon = jpop_root / 'Nakae Mitsuki (中恵光城) ~'
    nakae_album = jpop_root / 'Mitsuki Nakae Theme Song & Piano Collection 「STELLA-ステラ-」 ~'
    if nakae_album.exists():
        safe_move(nakae_album, nakae_canon / 'STELLA-ステラ-')

    # Uchida Aya (内田彩)
    uchida_canon = jpop_root / 'Uchida Aya (内田彩) ~'
    uchida_album = jpop_root / '内田彩 10周年記念アルバム「Re：birthday」[FLAC] ~'
    if uchida_album.exists():
        safe_move(uchida_album, uchida_canon / 'Re：birthday')

# ==============================================================================
# MAIN RUNNER
# ==============================================================================
def main():
    log("STARTING COMPREHENSIVE LIBRARY PERFECTION...")
    stage1_pure_albums()
    stage2_idolmaster()
    stage3_love_live()
    stage4_bang_dream()
    stage5_anime_cleanups()
    stage6_vtuber()
    stage7_doujinshi()
    stage8_vocaloid_to_jpop()
    stage9_jpop_cleanups()
    
    log("Applying permissions (775 dirs, 664 files)...")
    subprocess.run(['find', str(LOSSLESS_ROOT), '-type', 'd', '-exec', 'chmod', '775', '{}', '+'])
    subprocess.run(['find', str(LOSSLESS_ROOT), '-type', 'f', '-exec', 'chmod', '664', '{}', '+'])

    log("Rebuilding master catalog & M3U8 playlists...")
    subprocess.run(['python3', '/mnt/hdd-backup/music/scripts/update_catalog.py'])

    log("LIBRARY PERFECTION COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
