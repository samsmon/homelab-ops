#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reorganize and clean music library on hdd-backup.
"""
import os
import sys
import shutil
import hashlib
import sqlite3
import subprocess
from pathlib import Path

MUSIC_ROOT = Path('/mnt/hdd-backup/music')
LOSSLESS_ROOT = MUSIC_ROOT / 'Lossless'
LOSSY_ROOT = MUSIC_ROOT / 'Lossy'
TORRENT_ROOT = MUSIC_ROOT / 'Torrent'
TORRENT_DONE = TORRENT_ROOT / 'done'
TORRENT_LEECH = TORRENT_ROOT / '!leeching'
EXTRACT_ROOT = MUSIC_ROOT / '~Extract'
CORRUPT_ROOT = MUSIC_ROOT / '_corrupted_needs_redownload'

def md5_file(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def test_flac(filepath):
    try:
        res = subprocess.run(['flac', '-t', '-s', str(filepath)], capture_output=True, timeout=30)
        return res.returncode == 0
    except Exception as e:
        return False

def safe_move(src_path, dst_path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    if dst_path.exists():
        # If destination already exists, merge contents
        for item in src_path.iterdir():
            target_item = dst_path / item.name
            if target_item.exists():
                if item.is_file():
                    if item.stat().st_size == target_item.stat().st_size and md5_file(item) == md5_file(target_item):
                        item.unlink() # duplicate, remove source
                    else:
                        # rename source
                        stem = item.stem
                        suffix = item.suffix
                        new_target = dst_path / f"{stem}_alt{suffix}"
                        shutil.move(str(item), str(new_target))
                elif item.is_dir():
                    safe_move(item, target_item)
            else:
                shutil.move(str(item), str(target_item))
        # remove src dir if empty
        try:
            src_path.rmdir()
        except OSError:
            pass
    else:
        shutil.move(str(src_path), str(dst_path))

# ==============================================================================
# SECTION 1: ISLET / TAYORI CONSOLIDATION
# ==============================================================================
def step_1_consolidate_islet():
    print("\n" + "="*60)
    print("STEP 1: CONSOLIDATING ISLET / TAYORI DISCOGRAPHY")
    print("="*60)
    
    target_dir = LOSSLESS_ROOT / 'Doujinshi' / 'Islet (Tayori) ~'
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Move albums from Lossless/J-Pop/Tayori (Islet)~
    jpop_islet = LOSSLESS_ROOT / 'J-Pop' / 'Tayori (Islet)~'
    if jpop_islet.exists():
        for album in list(jpop_islet.iterdir()):
            if not album.is_dir():
                continue
            if album.name == 'Tayori (Islet) - CYANIDE':
                dst = target_dir / '[M3-45] Islet — CYANIDE [FLAC 24bit]'
            elif album.name == 'Islet - ASTER [WEB-FLAC 24bit／48kHz]':
                dst = target_dir / '[M3-49] Islet — ASTER [WEB-FLAC 24bit／48kHz]'
            else:
                dst = target_dir / album.name
            print(f"  Moving {album.name} -> {dst.name}")
            safe_move(album, dst)
        try:
            jpop_islet.rmdir()
            print("  Removed empty J-Pop/Tayori (Islet)~")
        except OSError:
            pass
            
    # 2. Move loose Islet albums in Lossless/Doujinshi
    m3_cyanide = LOSSLESS_ROOT / 'Doujinshi' / '[M3-45] Islet — CYANIDE [FLAC]'
    if m3_cyanide.exists() and m3_cyanide != target_dir:
        dst = target_dir / '[M3-45] Islet — CYANIDE [FLAC 16bit]'
        print(f"  Moving loose {m3_cyanide.name} -> {dst.name}")
        safe_move(m3_cyanide, dst)
        
    m3_aster = LOSSLESS_ROOT / 'Doujinshi' / '[M3-49] Islet — ASTER [WEB-FLAC]'
    if m3_aster.exists() and m3_aster != target_dir:
        dst = target_dir / '[M3-49] Islet — ASTER [WEB-FLAC 16bit]'
        print(f"  Moving loose {m3_aster.name} -> {dst.name}")
        safe_move(m3_aster, dst)
        
    print(f"Step 1 Complete! Islet consolidated at {target_dir}")

# ==============================================================================
# SECTION 2: HANDLE ~Extract
# ==============================================================================
def step_2_handle_extract():
    print("\n" + "="*60)
    print("STEP 2: EXTRACTING ARCHIVES & MOVING EXTRACTED ALBUMS")
    print("="*60)
    
    if not EXTRACT_ROOT.exists():
        print("~Extract does not exist, skipping.")
        return

    # A. Extract archives
    archives = [f for f in EXTRACT_ROOT.iterdir() if f.is_file() and f.suffix.lower() in ['.zip', '.7z', '.rar']]
    print(f"Found {len(archives)} unextracted archives in ~Extract")
    
    for a in archives:
        stem = a.stem
        # Determine category
        lower = stem.lower()
        if 'hololive' in lower or '天音かなた' in lower or 'vtuber' in lower:
            cat_dir = LOSSLESS_ROOT / 'Vtuber'
        elif 'アイドルマスター' in lower or 'シャイニーカラーズ' in lower or 'anime' in lower:
            cat_dir = LOSSLESS_ROOT / 'Anime'
        else:
            cat_dir = LOSSLESS_ROOT / 'Anime'
            
        dest_folder = cat_dir / stem
        dest_folder.mkdir(parents=True, exist_ok=True)
        print(f"  Extracting {a.name} -> {dest_folder.relative_to(MUSIC_ROOT)} ...")
        
        if a.suffix.lower() == '.zip':
            cmd = ['unzip', '-q', '-o', str(a), '-d', str(dest_folder)]
        else:
            cmd = ['7z', 'x', f'-o{dest_folder}', '-y', str(a)]
            
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0:
            print(f"    Success! Verifying FLACs...")
            # Verify flacs
            flacs = list(dest_folder.rglob('*.flac'))
            all_ok = True
            for f in flacs:
                if not test_flac(f):
                    print(f"    WARNING: corrupt flac {f.name}")
                    all_ok = False
            if all_ok:
                print(f"    All {len(flacs)} FLACs valid. Removing archive file.")
                a.unlink()
        else:
            print(f"    ERROR extracting {a.name}: {res.stderr.decode('utf-8', errors='ignore')}")

    # B. Move 36 folders in ~Extract/flac
    flac_dir = EXTRACT_ROOT / 'flac'
    if flac_dir.exists():
        for item in list(flac_dir.iterdir()):
            if not item.is_dir():
                continue
            name = item.name
            lower = name.lower()
            
            # Check empty
            files = [f for f in item.rglob('*') if f.is_file()]
            if not files:
                print(f"  Removing empty dir: {item.name}")
                shutil.rmtree(str(item))
                continue
                
            # Classify
            if any(k in lower for k in ['のえさんぽ', '白銀ノエル', 'lights', '獅白ぼたん', 'orbital period', '星街すいせい', '310phz', '月ノ美兎', 'rule the world', '春猿火']):
                cat = 'Vtuber'
            elif any(k in lower for k in ['k-on', 'spice and wolf', 'ookami to koushinryou', 'tabi no tochuu', 'mitsu no yoake', 'ringo hiyori', 'perfect world', 'カラーズ', '三ツ星カラーズ', 'sound! euphonium', 'ユーフォニアム', 'ウマ娘', 'priconne', 'プリンセスコネクト', '学園アイドルマスター', 'morfonica', 'bang dream', 'idoly pride', 'ワールドダイスター', '電音部', 'テトリス', 'galaxy triangle', 'white delight', 'ミア・テイラー']):
                cat = 'Anime'
            elif any(k in lower for k in ['そらる', 'ユメトキ', '笑顔のおかわり', 'jelee', '箱庭共鳴', 'hanon']):
                cat = 'J-Pop'
            elif any(k in lower for k in ['deco', 'テレパシ']):
                cat = 'Vocaloid'
            elif any(k in lower for k in ['never forget vacation', 'sauna', '[ahi]', 'login records']):
                cat = 'Doujinshi'
            else:
                cat = 'Anime'
                
            target_cat_dir = LOSSLESS_ROOT / cat
            
            # Special grouping for known anime series
            if 'k-on' in lower or 'fuwa fuwa' in lower:
                dst = target_cat_dir / 'K-ON! ~' / name
            elif any(k in lower for k in ['spice and wolf', 'ookami to koushinryou', 'tabi no tochuu', 'mitsu no yoake', 'ringo hiyori', 'perfect world']):
                dst = target_cat_dir / 'Spice and Wolf ~' / name
            elif 'カラーズ' in lower:
                dst = target_cat_dir / '三ツ星カラーズ ~' / name
            elif 'ユーフォニアム' in lower or 'sound! euphonium' in lower:
                dst = target_cat_dir / '響け！ユーフォニアム ~' / name
            elif 'ウマ娘' in lower:
                dst = target_cat_dir / 'Uma Musume ~' / name
            elif '学園アイドルマスター' in lower:
                dst = target_cat_dir / '学園アイドルマスター ~' / name
            elif 'のえさんぽ' in lower or '白銀ノエル' in lower:
                dst = target_cat_dir / '白銀ノエル ~' / name
            elif 'lights' in lower or '獅白ぼたん' in lower:
                dst = target_cat_dir / '獅白ぼたん ~' / name
            elif '星街すいせい' in lower:
                dst = target_cat_dir / '星街すいせい ~' / name
            elif 'そらる' in lower:
                dst = target_cat_dir / 'そらる ~' / name
            elif 'deco' in lower:
                dst = target_cat_dir / 'DECO_27' / name
            else:
                dst = target_cat_dir / name
                
            print(f"  Moving {name} -> {dst.relative_to(MUSIC_ROOT)}")
            safe_move(item, dst)
            
        # Clean flac_dir
        try:
            flac_dir.rmdir()
        except OSError:
            pass
            
    # Clean ~Extract if empty
    try:
        EXTRACT_ROOT.rmdir()
        print("  Removed empty ~Extract directory!")
    except OSError:
        pass
    print("Step 2 Complete!")

# ==============================================================================
# SECTION 3: HANDLE Torrent/done
# ==============================================================================
def step_3_handle_torrent_done():
    print("\n" + "="*60)
    print("STEP 3: CLEANING & REORGANIZING TORRENT/DONE")
    print("="*60)
    
    if not TORRENT_DONE.exists():
        print("Torrent/done does not exist, skipping.")
        return
        
    # 1. Clean empty and orphan cover folders
    empty_ado = TORRENT_DONE / '[2024.11.01] Ado - きっとコースター [FLAC 48kHz／24bit]'
    if empty_ado.exists():
        print(f"  Deleting empty folder: {empty_ado.name}")
        shutil.rmtree(str(empty_ado))
        
    vivy_orphan = TORRENT_DONE / "TVアニメVivy -Fluorite Eye's Song-」OPテーマSing My Pleasure」／ヴィヴィ(Vo.八木海莉) [FLAC]"
    if vivy_orphan.exists():
        print(f"  Deleting orphan cover folder: {vivy_orphan.name}")
        shutil.rmtree(str(vivy_orphan))
        
    # 2. Iterate remaining folders
    folders = sorted([d for d in TORRENT_DONE.iterdir() if d.is_dir()])
    print(f"Processing {len(folders)} folders in Torrent/done...")
    
    moved_count = 0
    dup_count = 0
    
    for d in folders:
        files = [f for f in d.rglob('*') if f.is_file()]
        audio = [f for f in files if f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a']]
        
        if not audio:
            print(f"  Deleting folder with no audio: {d.name}")
            shutil.rmtree(str(d))
            continue
            
        name = d.name
        lower = name.lower()
        
        # Determine category
        # Vtuber
        if any(k in lower for k in ['hololive', 'ホロライブ', '角巻わため', '博衣こより', '白上フブキ', '戌神ころね', 
                                   '星街すいせい', '宝鐘マリン', '猫又おかゆ', '湊あくあ', '大空スバル', '兎田ぺこら', 
                                   '常闇トワ', '天音かなた', 'azki', 'nijisanji', 'にじさんじ', 'nornis', 
                                   '月ノ美兎', '町田ちま', 'vspo', 'ぶいすぽ', 'hachi', '理芽', '花譜', '春猿火', '幸祜', 'sekai', 'rosette']):
            cat = 'Vtuber'
        # Vocaloid
        elif any(k in lower for k in ['deco*27', 'deco∗27', 'ピノキオピー', 'pinocchiop', 'ツユ', 'tuyu', 'maisondes', 
                                     'kanaria', 'chinozo', 'かいりきベア', 'すりぃ', 'syudou', 'vocaloid']):
            cat = 'Vocaloid'
        # Doujinshi
        elif any(k in lower for k in ['m3-', 'c10', 'c9', 'comicup', 'comiket', 'doujin', 'toho', 'touhou', '東方', 
                                     'circle', 'absolute castaway', 'aintops', 'felt', 'tamusic', 'iosys', 
                                     'shinra-bansho', '森羅万象', 'nayuta', 'なゆ茶', 'hatsuki yura', '葉月ゆら', '茶太']):
            cat = 'Doujinshi'
        # Anime
        elif any(k in lower for k in ['tvアニメ', 'アニメ', '劇場版', 'ost', 'soundtrack', 'character song', 
                                     'opテーマ', 'edテーマ', '主題歌', '挿入歌', 'bang dream', 'バンドリ', 
                                     'mygo', 'ave mujica', 'morfonica', 'poppin', 'roselia', 'afterglow', 
                                     'ラブライブ', 'love live', 'aqours', 'liella', '蓮ノ空', '虹ヶ咲', 'nijigaku', 
                                     'アイドルマスター', 'idolm@ster', 'アイマス', 'シャイニーカラーズ', 'shiny colors', 
                                     '学園アイドルマスター', 'ウマ娘', 'uma musume', 'ガールズバンドクライ', 'トゲナシトゲアリ', 
                                     'ぼっち・ざ・ろっく', '結束バンド', 'プリンセスコネクト', 'priconne', 'アークナイツ', 
                                     'arknights', 'ブルーアーカイブ', 'blue archive', 'アズールレーン', 'azur lane', 
                                     '鳴潮', 'wuthering waves', 'ゼンレスゾーンゼロ', 'zenless zone zero', 
                                     'ソードアート・オンライン', 'sao', '五等分の花嫁', '負けヒロイン', '狼と香辛料', 
                                     'ヒーラー・ガール', '女神のカフェテラス', '新米オッサン', '菜なれ花なれ', 
                                     '前橋ウィッチーズ', '少女☆歌劇', 'レヴュースタァライト', 'idoly pride', 
                                     'スクールアイドルミュージカル', 'うたごえはミルフィーユ', 'らぶフォー', 'ongeki', 
                                     'tokyo 7th', 'うたの☆プリンセスさまっ', '魔王2099', 'synduality']):
            cat = 'Anime'
        # J-Pop (default for Japanese commercial singles/albums)
        else:
            cat = 'J-Pop'
            
        target_dir = LOSSLESS_ROOT / cat / name
        
        # Check if already exists in Lossless
        existing_matches = [m for m in LOSSLESS_ROOT.rglob(name) if m.is_dir() and not str(m).startswith(str(TORRENT_ROOT))]
        if existing_matches:
            # Check if files match
            ex = existing_matches[0]
            ex_files = [f for f in ex.rglob('*') if f.is_file() and f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a']]
            if len(ex_files) == len(audio):
                print(f"  Exact duplicate of {ex.relative_to(MUSIC_ROOT)} -> Deleting from Torrent/done: {name}")
                shutil.rmtree(str(d))
                dup_count += 1
                continue
                
        # Move to target
        print(f"  [{cat}] Moving {name} -> Lossless/{cat}/")
        safe_move(d, target_dir)
        moved_count += 1
        
    print(f"Step 3 Complete! Moved: {moved_count}, Duplicates deleted: {dup_count}")

# ==============================================================================
# SECTION 4: HANDLE Torrent/!leeching
# ==============================================================================
def step_4_handle_torrent_leeching():
    print("\n" + "="*60)
    print("STEP 4: CLEANING TORRENT/!LEECHING")
    print("="*60)
    
    if not TORRENT_LEECH.exists():
        print("Torrent/!leeching does not exist, skipping.")
        return
        
    for item in list(TORRENT_LEECH.iterdir()):
        if not item.is_dir():
            continue
        files = [f for f in item.rglob('*') if f.is_file()]
        audio = [f for f in files if f.suffix.lower() in ['.flac', '.wav', '.mp3', '.m4a']]
        name = item.name
        
        if not audio:
            print(f"  Deleting ghost/empty folder: {name}")
            shutil.rmtree(str(item))
        elif '角巻わため' in name:
            print(f"  Watame already in library -> Deleting duplicate from !leeching: {name}")
            shutil.rmtree(str(item))
        elif '博衣こより' in name:
            # check if Koyori was moved to Lossless/Vtuber
            koyori_dest = LOSSLESS_ROOT / 'Vtuber' / name
            if koyori_dest.exists():
                print(f"  Koyori already in Lossless/Vtuber -> Deleting duplicate from !leeching: {name}")
                shutil.rmtree(str(item))
            else:
                print(f"  Moving Koyori from !leeching -> Lossless/Vtuber/")
                safe_move(item, koyori_dest)
        elif 'tokyo 7th' in name.lower():
            t7s_dir = LOSSLESS_ROOT / 'Anime' / 'Tokyo 7th シスターズ ~'
            target_sub = t7s_dir / 'Tokyo 7th シスターズ 2ndアルバム「Are You Ready 7th-TYPES？？」[FLAC Tracks]'
            print(f"  Moving Tokyo 7th Sisters tracks -> {target_sub.relative_to(MUSIC_ROOT)}")
            safe_move(item, target_sub)
        else:
            print(f"  Unknown folder with audio in !leeching: {name} (preserving)")
            
    print("Step 4 Complete!")

# ==============================================================================
# SECTION 5: CLEAN LOOSE FOLDERS IN ROOT
# ==============================================================================
def step_5_clean_loose_root():
    print("\n" + "="*60)
    print("STEP 5: CLEANING LOOSE FOLDERS IN LOSSLESS AND LOSSY ROOT")
    print("="*60)
    
    # 1. Memento Mori
    memento = LOSSLESS_ROOT / '株式会社バンク・オブ・イノベーション - メメントモリ Lament Collection Vol.2 (Memento Mori Lament Collection Vol.2) [FLAC]'
    if memento.exists():
        dst = LOSSLESS_ROOT / 'Anime' / memento.name
        print(f"  Moving Memento Mori to Lossless/Anime/")
        safe_move(memento, dst)
        
    # 2. No Group
    no_group = LOSSLESS_ROOT / 'No Group'
    if no_group.exists():
        for album in list(no_group.iterdir()):
            if album.is_dir():
                dst = LOSSLESS_ROOT / 'Anime' / album.name
                print(f"  Moving {album.name} from No Group to Lossless/Anime/")
                safe_move(album, dst)
        try:
            no_group.rmdir()
            print("  Removed empty Lossless/No Group/")
        except OSError:
            pass
            
    # 3. Lossy root loose folders
    lossy_moves = [
        ('fishpond - あおいとりがみる世界', LOSSY_ROOT / 'Doujinshi'),
        ('Bassy - 現代ポップスC & 続・現代ポップスC', LOSSY_ROOT / 'Doujinshi'),
        ('Ray - Hajimete Girls!', LOSSY_ROOT / 'Anime'),
        ('BotchiBoromaru - BOTCHI BOX vol.1', LOSSY_ROOT / 'Anime')
    ]
    for folder_name, target_dir in lossy_moves:
        p = LOSSY_ROOT / folder_name
        if p.exists():
            dst = target_dir / folder_name
            print(f"  Moving {folder_name} -> {dst.relative_to(MUSIC_ROOT)}")
            safe_move(p, dst)
            
    print("Step 5 Complete!")

# ==============================================================================
# SECTION 6: UPDATE SQLITE CATALOG
# ==============================================================================
def step_6_rebuild_catalog():
    print("\n" + "="*60)
    print("STEP 6: REBUILDING CATALOG.SQLITE")
    print("="*60)
    
    db_path = MUSIC_ROOT / 'catalog.sqlite'
    if db_path.exists():
        db_path.unlink() # rebuild cleanly
        
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute('''
        CREATE TABLE tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            relative_path TEXT UNIQUE,
            filename TEXT,
            category TEXT,
            format TEXT,
            size_bytes INTEGER,
            is_lossless INTEGER
        )
    ''')
    c.execute('CREATE INDEX idx_category ON tracks(category)')
    c.execute('CREATE INDEX idx_format ON tracks(format)')
    
    print("Indexing all tracks under /mnt/hdd-backup/music ...")
    batch = []
    count = 0
    
    for root_dir in [LOSSLESS_ROOT, LOSSY_ROOT]:
        if not root_dir.exists():
            continue
        is_lossless = 1 if root_dir == LOSSLESS_ROOT else 0
        for p in root_dir.rglob('*'):
            if not p.is_file():
                continue
            ext = p.suffix.lower()
            if ext not in ['.flac', '.wav', '.mp3', '.m4a', '.aac', '.ogg', '.opus', '.ape', '.wv', '.tak']:
                continue
                
            rel = str(p.relative_to(MUSIC_ROOT)).replace('\\', '/')
            parts = rel.split('/')
            category = parts[1] if len(parts) > 1 else 'Unknown'
            fmt = ext.replace('.', '').upper()
            size = p.stat().st_size
            
            batch.append((rel, p.name, category, fmt, size, is_lossless))
            count += 1
            if len(batch) >= 1000:
                c.executemany('''
                    INSERT OR IGNORE INTO tracks 
                    (relative_path, filename, category, format, size_bytes, is_lossless)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', batch)
                conn.commit()
                batch = []
                
    if batch:
        c.executemany('''
            INSERT OR IGNORE INTO tracks 
            (relative_path, filename, category, format, size_bytes, is_lossless)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', batch)
        conn.commit()
        
    conn.close()
    print(f"Catalog successfully rebuilt with {count} tracks indexed at {db_path}!")

if __name__ == '__main__':
    step_1_consolidate_islet()
    step_2_handle_extract()
    step_3_handle_torrent_done()
    step_4_handle_torrent_leeching()
    step_5_clean_loose_root()
    step_6_rebuild_catalog()
    print("\n" + "="*60)
    print("ALL STEPS EXECUTED SUCCESSFULLY!")
    print("="*60)
