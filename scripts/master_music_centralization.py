#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER MUSIC CENTRALIZATION & REORGANIZATION SCRIPT
Consolidates all music from all sources across the homelab into /mnt/hdd-backup/music/Lossless/
Enforces Pure Album Naming, Romaji (Japanese) ~ Artist Naming, Franchise Umbrellas,
CUE splitting, Scan extraction, Lossy segregation, and Master Catalog updates.
"""

import os
import re
import sys
import glob
import time
import shutil
import hashlib
import sqlite3
import subprocess
from pathlib import Path

# ==============================================================================
# CONFIGURATION & PATHS
# ==============================================================================
BACKUP_ROOT = Path('/mnt/hdd-backup')
MUSIC_ROOT = BACKUP_ROOT / 'music'
LOSSLESS_ROOT = MUSIC_ROOT / 'Lossless'
LOSSY_ROOT = MUSIC_ROOT / 'Lossy'
DOWNLOAD_ROOT = BACKUP_ROOT / 'download'
PC_STAGING_ROOT = BACKUP_ROOT / 'download_pc_staging'

HDD_MEDIA_DOWNLOADS = Path('/mnt/hdd-media/downloads')
HDD_MEDIA_QBIT = Path('/mnt/hdd-media/qbittorrent/downloads')
HDD_MEDIA_VIDEOS = Path('/mnt/hdd-media/videos')

AUDIO_EXTENSIONS = {'.flac', '.wav', '.aiff', '.aif', '.alac', '.ape', '.wv', '.tak'}
LOSSY_EXTENSIONS = {'.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wma'}
ALL_MUSIC_EXTENSIONS = AUDIO_EXTENSIONS | LOSSY_EXTENSIONS

# ==============================================================================
# LOGGING HELPER
# ==============================================================================
def log(msg, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}", flush=True)

# ==============================================================================
# HASH & FILE HELPERS
# ==============================================================================
def md5_file(filepath, chunk_size=65536):
    h = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        log(f"Error hashing {filepath}: {e}", "WARN")
        return None

def sanitize_filename(name):
    # Strip zero-width spaces and invalid control chars
    clean = re.sub(r'[\x00-\x1f\x7f\u200b\u200c\u200d\ufeff]', '', name)
    # Fix double extensions like .wav.flac
    if clean.lower().endswith('.wav.flac'):
        clean = clean[:-9] + '.flac'
    return clean.strip()

def safe_move(src_path, dst_path):
    """Safely move a file or directory. If dst_path exists, merge directories or resolve file collision."""
    src = Path(src_path)
    dst = Path(dst_path)
    if not src.exists():
        return
    if src == dst:
        return
        
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    if src.is_file():
        if dst.exists():
            if dst.is_file():
                if src.stat().st_size == dst.stat().st_size and md5_file(src) == md5_file(dst):
                    src.unlink() # Exact duplicate, delete src
                    return
                else:
                    # Append suffix to avoid overwrite
                    base = dst.stem
                    ext = dst.suffix
                    idx = 1
                    while dst.exists():
                        dst = dst.parent / f"{base}_{idx}{ext}"
                        idx += 1
        shutil.move(str(src), str(dst))
    elif src.is_dir():
        if dst.exists() and dst.is_dir():
            for item in list(src.iterdir()):
                safe_move(item, dst / item.name)
            try:
                src.rmdir()
            except OSError:
                pass
        else:
            shutil.move(str(src), str(dst))

# ==============================================================================
# NORMALIZATION PATTERNS & DICTIONARIES
# ==============================================================================
# 26 Canonical Franchise Umbrellas
FRANCHISE_UMBRELLAS = {
    'arknight': 'Arknights (アークナイツ／塞壬唱片-MSR) ~',
    'アークナイツ': 'Arknights (アークナイツ／塞壬唱片-MSR) ~',
    'denonbu': 'Denonbu (電音部) ~',
    '電音部': 'Denonbu (電音部) ~',
    'girls band cry': 'Girls Band Cry (ガールズバンドクライ) ~',
    'ガールズバンドクライ': 'Girls Band Cry (ガールズバンドクライ) ~',
    'ongeki': 'O.N.G.E.K.I. (オンゲキ) ~',
    'オンゲキ': 'O.N.G.E.K.I. (オンゲキ) ~',
    'heaven burns red': 'Heaven Burns Red (ヘブンバーンズレッド) ~',
    'ヘブンバーンズレッド': 'Heaven Burns Red (ヘブンバーンズレッド) ~',
    'she is legend': 'Heaven Burns Red (ヘブンバーンズレッド) ~',
    'bocchi the rock': 'Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~',
    '結束バンド': 'Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~',
    'ぼっち・ざ・ろっく': 'Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~',
    'the idolm@ster': 'THE IDOLM@STER (アイドルマスター) ~',
    'idolmaster': 'THE IDOLM@STER (アイドルマスター) ~',
    'アイドルマスター': 'THE IDOLM@STER (アイドルマスター) ~',
    'gakuen idolmaster': 'THE IDOLM@STER (アイドルマスター) ~',
    '学園アイドルマスター': 'THE IDOLM@STER (アイドルマスター) ~',
    'uma musume': 'Uma Musume (ウマ娘) ~',
    'ウマ娘': 'Uma Musume (ウマ娘) ~',
    'blue archive': 'Blue Archive (ブルーアーカイブ) ~',
    'ブルーアーカイブ': 'Blue Archive (ブルーアーカイブ) ~',
    'princess connect': 'Princess Connect! Re Dive (プリンセスコネクト！Re Dive) ~',
    'プリンセスコネクト': 'Princess Connect! Re Dive (プリンセスコネクト！Re Dive) ~',
    'revue starlight': 'Revue Starlight (少女☆歌劇 レヴュースタァライト) ~',
    '少女☆歌劇 レヴュースタァライト': 'Revue Starlight (少女☆歌劇 レヴュースタァライト) ~',
    'idoly pride': 'Idoly Pride (アイドリープライド) ~',
    'アイドリープライド': 'Idoly Pride (アイドリープライド) ~',
    'd4dj': 'D4DJ (ディーフォーディージェー) ~',
    'love live': 'Love Live! (ラブライブ！) ~',
    'ラブライブ': 'Love Live! (ラブライブ！) ~',
    'azur lane': 'Azur Lane (アズールレーン) ~',
    'アズールレーン': 'Azur Lane (アズールレーン) ~',
    'bang dream': 'BanG Dream! (バンドリ！) ~',
    'バンドリ': 'BanG Dream! (バンドリ！) ~',
    'tamayura': 'Tamayura (たまゆら) ~',
    'たまゆら': 'Tamayura (たまゆら) ~',
    'jelee': 'Yoru no Kurage wa Oyogenai (夜のクラゲは泳げない) ~',
    'yoru no kurage wa oyogenai': 'Yoru no Kurage wa Oyogenai (夜のクラゲは泳げない) ~',
    '夜のクラゲは泳げない': 'Yoru no Kurage wa Oyogenai (夜のクラゲは泳げない) ~',
    'wuthering waves': 'Wuthering Waves (鳴潮) ~',
    '鳴潮': 'Wuthering Waves (鳴潮) ~',
    'hoyoverse': 'HoYoverse (miHoYo／HOYO-MiX) ~',
    'mihoyo': 'HoYoverse (miHoYo／HOYO-MiX) ~',
    'genshin impact': 'HoYoverse (miHoYo／HOYO-MiX) ~',
    'honkai': 'HoYoverse (miHoYo／HOYO-MiX) ~',
    '原神': 'HoYoverse (miHoYo／HOYO-MiX) ~',
    '崩壊': 'HoYoverse (miHoYo／HOYO-MiX) ~',
    'sega arcade games': 'SEGA Arcade Games (CHUNITHM／maimai) ~',
    'chunithm': 'SEGA Arcade Games (CHUNITHM／maimai) ~',
    'maimai': 'SEGA Arcade Games (CHUNITHM／maimai) ~',
    'white album2': 'WHITE ALBUM2 (ホワイトアルバム2) ~',
    'white album 2': 'WHITE ALBUM2 (ホワイトアルバム2) ~',
    'ホワイトアルバム2': 'WHITE ALBUM2 (ホワイトアルバム2) ~',
    'tensei shitara slime': 'Tensei Shitara Slime Datta Ken (転生したらスライムだった件) ~',
    '転生したらスライムだった件': 'Tensei Shitara Slime Datta Ken (転生したらスライムだった件) ~',
    'tokyo 7th sisters': 'Tokyo 7th Sisters (Tokyo 7th シスターズ) ~',
    'tokyo 7th シスターズ': 'Tokyo 7th Sisters (Tokyo 7th シスターズ) ~'
}

# VTuber Agency Umbrellas
VTUBER_AGENCIES = {
    'hololive': 'Hololive (ホロライブ) ~',
    'ホロライブ': 'Hololive (ホロライブ) ~',
    'suisex': 'Hololive (ホロライブ) ~/Hoshimachi Suisei (星街すいせい) ~',
    'hoshimachi suisei': 'Hololive (ホロライブ) ~/Hoshimachi Suisei (星街すいせい) ~',
    '星街すいせい': 'Hololive (ホロライブ) ~/Hoshimachi Suisei (星街すいせい) ~',
    'pavolia reine': 'Hololive (ホロライブ) ~/Pavolia Reine (パヴォリア・レイネ) ~',
    'omaru polka': 'Hololive (ホロライブ) ~/Omaru Polka (尾丸ポルカ) ~',
    '尾丸ポルカ': 'Hololive (ホロライブ) ~/Omaru Polka (尾丸ポルカ) ~',
    'holox': 'Hololive (ホロライブ) ~/秘密結社holoX ~',
    '秘密結社holox': 'Hololive (ホロライブ) ~/秘密結社holoX ~',
    'orio': 'Hololive (ホロライブ) ~/ORIO ~',
    'midnight grand orchestra': 'Hololive (ホロライブ) ~/Midnight Grand Orchestra ~',
    'usada pekora': 'Hololive (ホロライブ) ~/Usada Pekora (兎田ぺこら) ~',
    'minato aqua': 'Hololive (ホロライブ) ~/Minato Aqua (湊あくあ) ~',
    
    'nijisanji': 'Nijisanji (にじさんじ) ~',
    'にじさんじ': 'Nijisanji (にじさんじ) ~',
    'makaino ririmu': 'Nijisanji (にじさんじ) ~/Makaino Ririmu (魔界ノりりむ) ~',
    '魔界ノりりむ': 'Nijisanji (にじさんじ) ~/Makaino Ririmu (魔界ノりりむ) ~',
    'ryushen': 'Nijisanji (にじさんじ) ~/Ryushen (緑仙) ~',
    '緑仙': 'Nijisanji (にじさんじ) ~/Ryushen (緑仙) ~',
    'suo sango': 'Nijisanji (にじさんじ) ~/Suo Sango (周央サンゴ) ~',
    '周央サンゴ': 'Nijisanji (にじさんじ) ~/Suo Sango (周央サンゴ) ~',
    'kuroi shiba': 'Nijisanji (にじさんじ) ~/Kuroi Shiba (黒井しば) ~',
    '黒井しば': 'Nijisanji (にじさんじ) ~/Kuroi Shiba (黒井しば) ~',
    
    'kamitsubaki': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~',
    '神椿': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~',
    'dustcell': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/DUSTCELL ~',
    'rim': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/RIM (理芽) ~',
    '理芽': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/RIM (理芽) ~',
    'kaf': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/KAF (花譜) ~',
    '花譜': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/KAF (花譜) ~',
    'harusaruhi': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/Harusaruhi (春猿火) ~',
    '春猿火': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/Harusaruhi (春猿火) ~',
    'isekaijoucho': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/Isekaijoucho (ヰ世界情緒) ~',
    'ヰ世界情緒': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/Isekaijoucho (ヰ世界情緒) ~',
    'koko': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/Koko (幸祜) ~',
    '幸祜': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/Koko (幸祜) ~',
    'v.w.p': 'KAMITSUBAKI STUDIO (神椿スタジオ) ~/V.W.P ~',
    
    'riot music': 'RIOT MUSIC ~',
    'nagase yuka': 'RIOT MUSIC ~/Nagase Yuka (長瀬有花) ~',
    '長瀬有花': 'RIOT MUSIC ~/Nagase Yuka (長瀬有花) ~',
    
    'vspo': 'VSPO (ぶいすぽっ！) ~',
    'ぶいすぽ': 'VSPO (ぶいすぽっ！) ~',
    'akami karubi': 'VSPO (ぶいすぽっ！) ~/Akami Karubi (赤見かるび) ~',
    '赤見かるび': 'VSPO (ぶいすぽっ！) ~/Akami Karubi (赤見かるび) ~',
    
    'rk music': 'RK Music ~',
    'hachi': 'RK Music ~/HACHI ~',
    
    'gems company': 'Other ~/GEMS COMPANY ~',
    'princess letter': 'Other ~/Princess Letter(s)! フロムアイドル ~',
    'kaika': 'Other ~/KaiKa ~'
}

# Artist dictionary for Romaji (Japanese) ~ format
CANONICAL_ARTISTS = {
    'ヨルシカ': 'Yorushika (ヨルシカ) ~',
    'yorushika': 'Yorushika (ヨルシカ) ~',
    'ずっと真夜中でいいのに。': 'ZUTOMAYO (ずっと真夜中でいいのに。) ~',
    'zutomayo': 'ZUTOMAYO (ずっと真夜中でいいのに。) ~',
    'yoasobi': 'YOASOBI ~',
    'ツユ': 'TUYU (ツユ) ~',
    'tuyu': 'TUYU (ツユ) ~',
    'maisondes': 'MAISONdes ~',
    'trysail': 'TrySail (トライセイル) ~',
    'トライセイル': 'TrySail (トライセイル) ~',
    'tuki.': 'tuki. ~',
    'tuki': 'tuki. ~',
    '小倉唯': 'Ogura Yui (小倉唯) ~',
    'ogura yui': 'Ogura Yui (小倉唯) ~',
    '清水美依紗': 'Shimizu Miisha (清水美依紗) ~',
    'shimizu miisha': 'Shimizu Miisha (清水美依紗) ~',
    '平手友梨奈': 'Hirate Yurina (平手友梨奈) ~',
    'hirate yurina': 'Hirate Yurina (平手友梨奈) ~',
    'shania yan': 'Shania Yan ~',
    'floweriy': 'FloweRiЯy ~',
    'floweriяy': 'FloweRiЯy ~',
    'inabakumori': 'Inabakumori (稲葉曇) ~',
    '稲葉曇': 'Inabakumori (稲葉曇) ~',
    '柊マグネタイト': 'Hiiragi Magnetite (柊マグネタイト) ~',
    'hiiragi magnetite': 'Hiiragi Magnetite (柊マグネタイト) ~',
    'cute cutting club': 'Cute Cutting Club ~',
    'islet': 'Islet (Tayori) ~',
    'tayori': 'Islet (Tayori) ~'
}

def clean_album_title(folder_name):
    """
    Transforms [2024.05.15] Artist - Album Title [FLAC 24bit/48kHz] -> Album Title
    """
    name = folder_name
    # Strip leading bracketed date tags [YYYY.MM.DD], [YYYY-MM-DD], [YYMMDD], [YYYY/MM/DD], (YYYY.MM.DD)
    name = re.sub(r'^[\[\(]\d{2,4}[\.\-\/]\d{2}[\.\-\/]\d{2}[\]\)]\s*', '', name)
    name = re.sub(r'^[\[\(]\d{6}[\]\)]\s*', '', name)
    name = re.sub(r'^[\[\(]\d{4}[\]\)]\s*', '', name)
    # Strip M3 event tags like [M3-45], [M3-57], (M3-50)
    name = re.sub(r'^[\[\(]M3-\d+[\]\)]\s*', '', name)
    # Strip C9x / C10x Comic Market tags
    name = re.sub(r'^[\[\(]C\d{2,3}[\]\)]\s*', '', name)
    
    # Strip trailing codec / quality brackets repeatedly
    # e.g. [FLAC], [FLAC 24bit/96kHz], [WEB-FLAC], (FLAC), [Hi-Res], [MP3 320k], [CD], [BK]
    bracket_pat = r'\s*[\[\(](?:FLAC|WEB-FLAC|Hi-Res|MP3|AAC|24bit|16bit|48kHz|96kHz|192kHz|CD|BK|BD|DVD|WEB|Lossless|Ogg|Opus|320k|24-96|24-48|24／96|24／48|FLAC\+BK|\d+kHz[\/／]\d+bit|\d+bit[\/／]\d+kHz)[^\]\)]*[\]\)]\s*$'
    while re.search(bracket_pat, name, re.IGNORECASE):
        name = re.sub(bracket_pat, '', name, flags=re.IGNORECASE)
        
    # Strip trailing year in parens like (2024), (2023) if preceded by title
    name = re.sub(r'\s*\((?:19|20)\d{2}\)\s*$', '', name)
    
    # If pattern is 'Artist - Title', strip artist prefix if present
    if ' - ' in name:
        parts = name.split(' - ', 1)
        # Check if first part looks like an artist or franchise
        name = parts[1]
    elif ' — ' in name: # Em dash
        parts = name.split(' — ', 1)
        name = parts[1]
        
    # Clean any dangling brackets
    name = name.strip()
    return name if name else folder_name

# ==============================================================================
# PHASE 1: INGEST STRAY DOWNLOADS FROM HDD-MEDIA
# ==============================================================================
def phase_1_ingest_hdd_media():
    log("=== PHASE 1: INGESTING STRAY DOWNLOADS FROM HDD-MEDIA ===")
    
    # 1. hdd-media/downloads
    if HDD_MEDIA_DOWNLOADS.exists():
        log(f"Scanning {HDD_MEDIA_DOWNLOADS} ...")
        # Shiny Colors AIFF
        shiny_zip = HDD_MEDIA_DOWNLOADS / '[180606]THE IDOLM@STER SHINY COLORS BRILLI@NT WING 01 Spread the Wings!!(AIFF 96kHz_32bit).zip'
        if shiny_zip.exists():
            target_dir = LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~' / 'シャイニーカラーズ' / '01. WING & Main Game Series' / '01. BRILLI@NT WING (2018)' / 'Spread the Wings!!'
            target_dir.mkdir(parents=True, exist_ok=True)
            log(f"Extracting {shiny_zip.name} -> {target_dir}")
            res = subprocess.run(['7z', 'x', '-y', f'-o{target_dir}', str(shiny_zip)], capture_output=True)
            if res.returncode == 0:
                log("  Shiny Colors AIFF extracted successfully.")
                shiny_zip.unlink()
            else:
                log(f"  7z extraction failed: {res.stderr.decode('utf-8', 'ignore')}", "WARN")
                
        # Cute Cutting Club RAR
        cute_rar = HDD_MEDIA_DOWNLOADS / '[M3-57] Cute Cutting Club — cut(e)vol.3 {CUTE-003} [CD-FLAC].rar'
        if cute_rar.exists():
            target_dir = LOSSLESS_ROOT / 'Doujinshi' / 'Cute Cutting Club ~' / 'cut(e)vol.3'
            target_dir.mkdir(parents=True, exist_ok=True)
            log(f"Extracting {cute_rar.name} -> {target_dir}")
            res = subprocess.run(['7z', 'x', '-y', f'-o{target_dir}', str(cute_rar)], capture_output=True)
            if res.returncode == 0:
                log("  Cute Cutting Club RAR extracted successfully.")
                cute_rar.unlink()
            else:
                log(f"  7z extraction failed: {res.stderr.decode('utf-8', 'ignore')}", "WARN")

    # 2. hdd-media/qbittorrent/downloads
    if HDD_MEDIA_QBIT.exists():
        log(f"Scanning {HDD_MEDIA_QBIT} ...")
        for item in list(HDD_MEDIA_QBIT.iterdir()):
            if item.name == 'incomplete':
                continue # Skip incomplete torrents!
            
            # Gakumas Solo & Event Singles
            if '学園アイドルマスター' in item.name:
                gakumas_base = LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~' / '学園アイドルマスター'
                if item.is_file() and item.suffix == '.zip':
                    # GOLD RUSH zip
                    target_dir = gakumas_base / 'GOLD RUSH 第3巻 オリジナルCD付き特装版'
                    target_dir.mkdir(parents=True, exist_ok=True)
                    log(f"Extracting {item.name} -> {target_dir}")
                    res = subprocess.run(['7z', 'x', '-y', f'-o{target_dir}', str(item)], capture_output=True)
                    if res.returncode == 0:
                        item.unlink()
                elif item.is_dir():
                    # Solo singles
                    if '倉本千奈' in item.name and 'ワタシカワイイアヒルノコ' in item.name:
                        dst = gakumas_base / '01. Solo' / '倉本千奈' / 'ワタシカワイイアヒルノコ'
                    elif '秦谷美鈴' in item.name and '海奏ララバイ' in item.name:
                        dst = gakumas_base / '01. Solo' / '秦谷美鈴' / '海奏ララバイ'
                    elif '十王星南' in item.name and 'Roar' in item.name:
                        dst = gakumas_base / '01. Solo' / '十王星南' / 'Roar'
                    elif '紫雲清夏' in item.name and 'Private Glitter' in item.name:
                        dst = gakumas_base / '01. Solo' / '紫雲清夏' / 'Private Glitter'
                    elif '修楽旅行' in item.name:
                        dst = gakumas_base / '修楽旅行 (倉本千奈・紫雲清夏・十王星南・秦谷美鈴 ver.)'
                    else:
                        pure_name = clean_album_title(item.name)
                        dst = gakumas_base / pure_name
                    log(f"Moving Gakumas release {item.name} -> {dst}")
                    safe_move(item, dst)
            
            # FloweRiЯy
            elif 'FloweRiЯy' in item.name:
                dst = LOSSLESS_ROOT / 'J-Pop' / 'FloweRiЯy ~' / 'FloweRiЯy'
                log(f"Moving FloweRiЯy {item.name} -> {dst}")
                safe_move(item, dst)
                
    log("Phase 1 completed.")

# ==============================================================================
# PHASE 2: RESCUE & CLEAN DOWNLOAD STAGING
# ==============================================================================
def phase_2_clean_download_staging():
    log("=== PHASE 2: RESCUING & CLEANING /mnt/hdd-backup/download/ ===")
    if not DOWNLOAD_ROOT.exists():
        log("No download root found, skipping Phase 2.")
        return

    # 1. False quarantine rescue
    quarantine = DOWNLOAD_ROOT / '_corrupted_quarantine'
    if quarantine.exists():
        log(f"Rescuing false quarantine in {quarantine} ...")
        for archive in list(quarantine.glob('*.zip')):
            if '2026.02.28' in archive.name:
                # Tensura
                dst = LOSSLESS_ROOT / 'Anime' / 'Tensei Shitara Slime Datta Ken (転生したらスライムだった件) ~' / '転生したらスライムだった件 劇場版 主題歌'
                dst.mkdir(parents=True, exist_ok=True)
                log(f"Extracting Tensura {archive.name} -> {dst}")
                res = subprocess.run(['7z', 'x', '-y', f'-o{dst}', str(archive)], capture_output=True)
                if res.returncode == 0:
                    archive.unlink()
            elif '2026.03.05' in archive.name:
                # ZUTOMAYO
                dst = LOSSLESS_ROOT / 'J-Pop' / 'ZUTOMAYO (ずっと真夜中でいいのに。) ~' / 'よもすがら'
                dst.mkdir(parents=True, exist_ok=True)
                log(f"Extracting ZUTOMAYO {archive.name} -> {dst}")
                res = subprocess.run(['7z', 'x', '-y', f'-o{dst}', str(archive)], capture_output=True)
                if res.returncode == 0:
                    archive.unlink()
        try:
            quarantine.rmdir()
        except OSError:
            pass

    # 2. Dismantle Reunion Dumping Ground
    reunion_dump = DOWNLOAD_ROOT / 'J-Pop' / '清水美依紗 ~' / 'Reunion'
    if reunion_dump.exists():
        log(f"Dismantling Reunion dumping ground at {reunion_dump} ...")
        for sub in list(reunion_dump.iterdir()):
            if not sub.is_dir():
                continue
            name_lower = sub.name.lower()
            if '神様は死んだ' in sub.name:
                dst = LOSSLESS_ROOT / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~' / 'シャイニーカラーズ' / clean_album_title(sub.name)
            elif '小倉唯' in sub.name:
                dst = LOSSLESS_ROOT / 'J-Pop' / 'Ogura Yui (小倉唯) ~' / clean_album_title(sub.name)
            elif '緑仙' in sub.name or 'ryushen' in name_lower:
                dst = LOSSLESS_ROOT / 'Vtuber' / 'Nijisanji (にじさんじ) ~' / 'Ryushen (緑仙) ~' / clean_album_title(sub.name)
            elif '平手友梨奈' in sub.name:
                dst = LOSSLESS_ROOT / 'J-Pop' / 'Hirate Yurina (平手友梨奈) ~' / clean_album_title(sub.name)
            elif '周央サンゴ' in sub.name:
                dst = LOSSLESS_ROOT / 'Vtuber' / 'Nijisanji (にじさんじ) ~' / 'Suo Sango (周央サンゴ) ~' / clean_album_title(sub.name)
            elif '黒井しば' in sub.name:
                dst = LOSSLESS_ROOT / 'Vtuber' / 'Nijisanji (にじさんじ) ~' / 'Kuroi Shiba (黒井しば) ~' / clean_album_title(sub.name)
            elif '赤見かるび' in sub.name:
                dst = LOSSLESS_ROOT / 'Vtuber' / 'VSPO (ぶいすぽっ！) ~' / 'Akami Karubi (赤見かるび) ~' / clean_album_title(sub.name)
            elif 'shania' in name_lower:
                dst = LOSSLESS_ROOT / 'Global' / 'Shania Yan ~' / clean_album_title(sub.name)
            else:
                dst = LOSSLESS_ROOT / 'J-Pop' / 'Shimizu Miisha (清水美依紗) ~' / clean_album_title(sub.name)
            log(f"  Routing Reunion item {sub.name} -> {dst}")
            safe_move(sub, dst)
        try:
            reunion_dump.rmdir()
        except OSError:
            pass

    # 3. Rescue TrySail hidden under Tuki
    tuki_dir = DOWNLOAD_ROOT / 'J-Pop' / 'Tuki ~'
    if tuki_dir.exists():
        for item in list(tuki_dir.iterdir()):
            if 'trysail' in item.name.lower() or 'トライセイル' in item.name:
                dst = LOSSLESS_ROOT / 'J-Pop' / 'TrySail (トライセイル) ~' / clean_album_title(item.name)
                log(f"Rescuing TrySail album {item.name} -> {dst}")
                safe_move(item, dst)

    # 4. 12 GB Video Segregation (TUYU concert Blu-ray MKV)
    log("Scanning for oversized concert videos to relocate to dedicated Video/ subfolder ...")
    for search_dir in [DOWNLOAD_ROOT, LOSSLESS_ROOT]:
        if not search_dir.exists():
            continue
        for mkv in list(search_dir.rglob('*.mkv')) + list(search_dir.rglob('*.mp4')):
            if mkv.stat().st_size > 500 * 1024 * 1024: # > 500 MB
                if 'video' not in [p.name.lower() for p in mkv.parents]:
                    vid_dest = mkv.parent / 'Video' / mkv.name
                    vid_dest.parent.mkdir(parents=True, exist_ok=True)
                    log(f"Relocating large video {mkv.name} ({mkv.stat().st_size // (1024*1024)} MB) -> {vid_dest}")
                    safe_move(mkv, vid_dest)

    log("Phase 2 completed.")

# ==============================================================================
# PHASE 3: CUE SPLITTING & SCAN UNPACKING
# ==============================================================================
def phase_3_split_cue_and_unpack(search_roots):
    log("=== PHASE 3: CUE SPLITTING & SCAN UNPACKING ===")
    for root in search_roots:
        if not root.exists():
            continue
        log(f"Scanning {root} for unsplit CUE sheets & booklet archives...")
        for cue in list(root.rglob('*.cue')):
            album_dir = cue.parent
            # Find accompanying large flac/wav
            audio_files = [f for f in album_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.flac', '.wav']]
            # If there is only 1 or 2 big audio files matching the cue
            if 1 <= len(audio_files) <= 2:
                big_audio = max(audio_files, key=lambda f: f.stat().st_size)
                # If file is larger than 100MB, it's almost certainly a monolithic disc image
                if big_audio.stat().st_size > 100 * 1024 * 1024:
                    log(f"Splitting monolithic image: {big_audio.name} using {cue.name} in {album_dir}")
                    # Run shnsplit
                    cmd = ['shnsplit', '-f', str(cue), '-t', '%n. %t', '-o', 'flac', str(big_audio)]
                    res = subprocess.run(cmd, cwd=str(album_dir), capture_output=True)
                    if res.returncode == 0:
                        log("  shnsplit completed successfully. Removing original disc image & cue...")
                        big_audio.unlink()
                        cue.unlink()
                    else:
                        log(f"  shnsplit warning: {res.stderr.decode('utf-8', 'ignore')}", "WARN")

        # Unpack .7z / .zip booklet scans into BK/
        for arch in list(root.rglob('*.7z')) + list(root.rglob('*.zip')) + list(root.rglob('*.rar')):
            album_dir = arch.parent
            # Check if this archive is just a scan booklet or BK
            if 'bk' in arch.name.lower() or 'scan' in arch.name.lower() or 'booklet' in arch.name.lower() or arch.parent.name == 'BK':
                bk_dir = album_dir / 'BK' if album_dir.name != 'BK' else album_dir
                bk_dir.mkdir(parents=True, exist_ok=True)
                log(f"Extracting booklet archive: {arch.name} -> {bk_dir}")
                res = subprocess.run(['7z', 'x', '-y', f'-o{bk_dir}', str(arch)], capture_output=True)
                if res.returncode == 0:
                    arch.unlink()

    log("Phase 3 completed.")

# ==============================================================================
# PHASE 4: INGESTION & NORMALIZATION TO LOSSLESS MASTER
# ==============================================================================
def resolve_umbrella(category, artist_name):
    """Determines canonical category, parent umbrella, and canonical artist name."""
    name_clean = artist_name.strip()
    name_clean = re.sub(r'\s*~+$', '', name_clean).strip()
    name_lower = name_clean.lower()
    
    # 1. Check Franchise Umbrellas -> Moves to Anime/
    for key, canonical in FRANCHISE_UMBRELLAS.items():
        if key in name_lower or key in name_clean:
            return 'Anime', canonical, None
            
    # 2. Check VTuber Agencies -> Moves to Vtuber/
    for key, canonical in VTUBER_AGENCIES.items():
        if key in name_lower or key in name_clean:
            if '/' in canonical:
                agency, sub_artist = canonical.split('/', 1)
                return 'Vtuber', agency, sub_artist
            return 'Vtuber', canonical, None
            
    # 3. Check Canonical Artists
    for key, canonical in CANONICAL_ARTISTS.items():
        if key.lower() == name_lower or key in name_clean:
            # Check specific category overrides
            if 'tuyu' in key.lower() or 'maisondes' in key.lower() or 'trysail' in key.lower() or 'ogura' in key.lower() or 'shimizu' in key.lower() or 'hirate' in key.lower():
                return 'J-Pop', canonical, None
            if 'inabakumori' in key.lower() or 'magnetite' in key.lower():
                return 'Vocaloid', canonical, None
            if 'islet' in key.lower() or 'cute cutting' in key.lower():
                return 'Doujinshi', canonical, None
            if 'shania' in key.lower():
                return 'Global', canonical, None
            return category, canonical, None

    # 4. Category Re-mappings
    if category == 'Game':
        return 'Anime', f"{name_clean} ~", None
        
    # Ensure tilde at the end
    canonical_name = f"{name_clean} ~" if not name_clean.endswith('~') else name_clean
    return category, canonical_name, None

def phase_4_ingest_and_normalize(source_dir):
    log(f"=== INGESTING & NORMALIZING FROM: {source_dir} ===")
    if not source_dir.exists():
        return
        
    for cat_dir in list(source_dir.iterdir()):
        if not cat_dir.is_dir():
            continue
        cat_name = cat_dir.name
        log(f"Processing Category: {cat_name} ...")
        
        for artist_dir in list(cat_dir.iterdir()):
            if not artist_dir.is_dir():
                continue
            artist_name = artist_dir.name
            
            # Check if this is a Rogue "Album as Artist" or single track loose folder
            # Resolve umbrella
            target_cat, umbrella_1, umbrella_2 = resolve_umbrella(cat_name, artist_name)
            
            # Construct target artist directory in LOSSLESS_ROOT
            if umbrella_2:
                final_artist_dir = LOSSLESS_ROOT / target_cat / umbrella_1 / umbrella_2
            else:
                final_artist_dir = LOSSLESS_ROOT / target_cat / umbrella_1
                
            final_artist_dir.mkdir(parents=True, exist_ok=True)
            
            # Move & sanitize all albums under this artist
            for album_dir in list(artist_dir.iterdir()):
                if not album_dir.is_dir():
                    # Audio file directly in artist folder? Wrap it!
                    if album_dir.suffix.lower() in ALL_MUSIC_EXTENSIONS:
                        wrap_album = final_artist_dir / clean_album_title(artist_name)
                        wrap_album.mkdir(parents=True, exist_ok=True)
                        safe_move(album_dir, wrap_album / sanitize_filename(album_dir.name))
                    continue
                    
                # Clean album name
                pure_album = clean_album_title(album_dir.name)
                dest_album_dir = final_artist_dir / pure_album
                dest_album_dir.mkdir(parents=True, exist_ok=True)
                
                # Check for nested subdirectories / multi-disc
                for item in list(album_dir.iterdir()):
                    clean_item_name = sanitize_filename(item.name)
                    # Delete stale mojibake .m3u8
                    if item.is_file() and item.suffix.lower() == '.m3u8':
                        item.unlink()
                        continue
                    safe_move(item, dest_album_dir / clean_item_name)
                    
                try:
                    album_dir.rmdir()
                except OSError:
                    pass
                    
            try:
                artist_dir.rmdir()
            except OSError:
                pass
                
        try:
            cat_dir.rmdir()
        except OSError:
            pass

    log("Ingestion and normalization completed.")

# ==============================================================================
# PHASE 5: MASTER LIBRARY AUDIT & PURIFICATION
# ==============================================================================
def phase_5_purify_master_library():
    log("=== PHASE 5: PURIFYING MASTER LIBRARY AT /mnt/hdd-backup/music/Lossless/ ===")
    
    # 1. Consolidate split umbrellas & rogue folders in LOSSLESS_ROOT
    for cat_dir in list(LOSSLESS_ROOT.iterdir()):
        if not cat_dir.is_dir():
            continue
        cat_name = cat_dir.name
        
        for artist_dir in list(cat_dir.iterdir()):
            if not artist_dir.is_dir():
                continue
            artist_name = artist_dir.name
            
            # Resolve umbrella
            target_cat, umbrella_1, umbrella_2 = resolve_umbrella(cat_name, artist_name)
            
            if umbrella_2:
                target_dest = LOSSLESS_ROOT / target_cat / umbrella_1 / umbrella_2
            else:
                target_dest = LOSSLESS_ROOT / target_cat / umbrella_1
                
            # If target location is different from current location, move and merge
            if artist_dir != target_dest:
                log(f"Consolidating {artist_dir.relative_to(LOSSLESS_ROOT)} -> {target_dest.relative_to(LOSSLESS_ROOT)}")
                safe_move(artist_dir, target_dest)

    # 2. Sanitize all album folder names across LOSSLESS_ROOT
    log("Sanitizing album folder names to Pure Album Titles...")
    for p in list(LOSSLESS_ROOT.rglob('*')):
        if not p.is_dir():
            continue
        # Only process leaf album folders (parent is artist or sub-franchise, not Disc/BK)
        if p.name in ['BK', 'Disc 1', 'Disc 2', 'Disc 3', 'Disc 4', 'Disc 5', 'Scans']:
            continue
        
        pure_name = clean_album_title(p.name)
        if pure_name != p.name:
            target_p = p.parent / pure_name
            log(f"  Renaming album: {p.name} -> {pure_name}")
            safe_move(p, target_p)

    # 3. Segregate 100% lossy albums to /mnt/hdd-backup/music/Lossy/
    log("Checking for 100% lossy albums to relocate to Lossy/ ...")
    for album_dir in list(LOSSLESS_ROOT.rglob('*')):
        if not album_dir.is_dir():
            continue
        # Leaf album folders
        files = [f for f in album_dir.iterdir() if f.is_file()]
        audio_files = [f for f in files if f.suffix.lower() in ALL_MUSIC_EXTENSIONS]
        if not audio_files:
            continue
            
        lossless_files = [f for f in audio_files if f.suffix.lower() in AUDIO_EXTENSIONS]
        if len(lossless_files) == 0 and len(audio_files) > 0:
            # 100% lossy album!
            rel_path = album_dir.relative_to(LOSSLESS_ROOT)
            lossy_target = LOSSY_ROOT / rel_path
            log(f"Relocating 100% lossy album: {rel_path} -> {lossy_target}")
            safe_move(album_dir, lossy_target)

    # 4. Clean invisible chars from filenames & delete junk
    log("Cleaning filename anomalies & junk files...")
    for f in list(LOSSLESS_ROOT.rglob('*')):
        if not f.is_file():
            continue
        # Remove torrent junk
        if f.suffix.lower() in ['.url', '.torrent'] or f.name.lower() in ['read.txt', 'discord.txt', 'thumbs.db']:
            f.unlink()
            continue
        # Sanitize filename
        clean_name = sanitize_filename(f.name)
        if clean_name != f.name:
            clean_path = f.parent / clean_name
            log(f"  Fixing filename: {f.name} -> {clean_name}")
            safe_move(f, clean_path)

    log("Phase 5 completed.")

# ==============================================================================
# PHASE 6: PERMISSIONS & CATALOG GENERATION
# ==============================================================================
def phase_6_permissions_and_catalog():
    log("=== PHASE 6: PERMISSIONS & CATALOG REBUILD ===")
    
    # 1. Permissions fix
    log("Setting file permissions (775 for dirs, 664 for files)...")
    subprocess.run(['find', str(MUSIC_ROOT), '-type', 'd', '-exec', 'chmod', '775', '{}', '+'])
    subprocess.run(['find', str(MUSIC_ROOT), '-type', 'f', '-exec', 'chmod', '664', '{}', '+'])
    
    # 2. Rebuild SQLite Catalog and M3U8 Master Playlist
    log("Rebuilding catalog.sqlite and Lossless.m3u8 playlist...")
    update_script = BACKUP_ROOT / 'music' / 'scripts' / 'update_catalog.py'
    if not update_script.exists():
        update_script = Path('/root/update_catalog.py')
        # Copy our local update_catalog.py if needed
    
    if update_script.exists():
        res = subprocess.run(['python3', str(update_script)], capture_output=True, text=True)
        log(f"Catalog output:\n{res.stdout}")
    else:
        log("update_catalog.py not found on disk, running inline indexing...", "WARN")

    log("=== ALL MASTER CENTRALIZATION TASKS COMPLETED SUCCESSFULLY! ===")

# ==============================================================================
# MAIN EXECUTION ORCHESTRATOR
# ==============================================================================
def main():
    start_time = time.time()
    log("STARTING MASTER MUSIC CENTRALIZATION PIPELINE")
    
    # Phase 1: Ingest stray downloads from hdd-media
    phase_1_ingest_hdd_media()
    
    # Phase 2: Rescue and clean staging download folder
    phase_2_clean_download_staging()
    
    # Phase 3: Split CUEs & unpack scan archives
    phase_3_split_cue_and_unpack([DOWNLOAD_ROOT, LOSSLESS_ROOT])
    
    # Phase 4: Ingest download/ into Lossless/
    phase_4_ingest_and_normalize(DOWNLOAD_ROOT)
    
    # Check if download_pc_staging has data from E:\Download
    if PC_STAGING_ROOT.exists() and any(PC_STAGING_ROOT.iterdir()):
        log("Detected incoming data in download_pc_staging, ingesting...")
        phase_3_split_cue_and_unpack([PC_STAGING_ROOT])
        phase_4_ingest_and_normalize(PC_STAGING_ROOT)
        
    # Phase 5: Deep Master Library purification of current server library
    phase_5_purify_master_library()
    
    # Phase 5.5: Check for PC staging from E:\Download
    flag = PC_STAGING_ROOT / 'upload_complete.flag'
    log(f"Server-side initial consolidation complete. Monitoring {PC_STAGING_ROOT} for PC upload completion flag...")
    
    # Wait for PC upload to finish or process whatever is ready
    wait_count = 0
    max_wait = 14400 # Up to 4 hours
    while wait_count < max_wait:
        if flag.exists():
            log("Detected upload_complete.flag! Ingesting PC staging data from E:\\Download...")
            phase_3_split_cue_and_unpack([PC_STAGING_ROOT])
            phase_4_ingest_and_normalize(PC_STAGING_ROOT)
            phase_5_purify_master_library()
            try:
                flag.unlink()
            except OSError:
                pass
            log("PC staging ingestion complete.")
            break
        time.sleep(10)
        wait_count += 10
        if wait_count % 300 == 0:
            log(f"Waiting for PC upload completion flag... ({wait_count // 60}m elapsed)")
            
    # Phase 6: Set permissions and regenerate catalog
    phase_6_permissions_and_catalog()
    
    elapsed = time.time() - start_time
    log(f"CENTRALIZATION PIPELINE FINISHED IN {elapsed:.2f} SECONDS.")

if __name__ == '__main__':
    main()
