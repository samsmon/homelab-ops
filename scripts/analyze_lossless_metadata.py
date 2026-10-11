#!/usr/bin/env python3
"""
analyze_lossless_metadata.py
Server-side read-only analysis script for /mnt/hdd-backup/music/Lossless/.
Extracts Vorbis comment metadata and SQLite catalog info to propose reorganization plan:
  1. Artist naming: Romaji (Kanji/Kana) ~
  2. Album naming: Pure Album Name (no dates, no formats, no years)
  3. Proper franchise umbrella structuring (THE IDOLM@STER ~, Uma Musume ~, etc.)
  4. Real-time progress tracking with percentage and ETA calculation.
Output: /tmp/lossless_reorganize_plan.json
Progress file: /tmp/lossless_analyze_progress.json
"""

import os
import sys
import json
import re
import time
import struct
import sqlite3
from pathlib import Path

BASE_DIR = "/mnt/hdd-backup/music/Lossless"
OUTPUT_PLAN = "/tmp/lossless_reorganize_plan.json"
OUTPUT_SUMMARY = "/tmp/lossless_analyze_summary.txt"
PROGRESS_FILE = "/tmp/lossless_analyze_progress.json"

ARTIST_ROMAJI_MAP = {
    "青木陽菜": "Aoki Hina (青木陽菜) ~",
    "ナツノセ": "Natsunose (ナツノセ) ~",
    "藍月なくる": "Aitsuki Nakuru (藍月なくる) ~",
    "星街すいせい": "Hoshimachi Suisei (星街すいせい) ~",
    "さくらみこ": "Sakura Miko (さくらみこ) ~",
    "白上フブキ": "Shirakami Fubuki (白上フブキ) ~",
    "天音かなた": "Amane Kanata (天音かなた) ~",
    "角巻わため": "Tsunomaki Watame (角巻わため) ~",
    "博衣こより": "Hakui Koyori (博衣こより) ~",
    "ときのそら": "Tokino Sora (ときのそら) ~",
    "湊あくあ": "Minato Aqua (湊あくあ) ~",
    "戌神ころね": "Inugami Korone (戌神ころね) ~",
    "獅白ぼたん": "Shishiro Botan (獅白ぼたん) ~",
    "白銀ノエル": "Shirogane Noel (白銀ノエル) ~",
    "猫又おかゆ": "Nekomata Okayu (猫又おかゆ) ~",
    "桃鈴ねね": "Momosuzu Nene (桃鈴ねね) ~",
    "癒月ちょこ": "Yuzuki Choco (癒月ちょこ) ~",
    "星川サラ": "Hoshikawa Sara (星川サラ) ~",
    "しぐれうい": "Shigure Ui (しぐれうい) ~",
    "稀羽すう": "Usuwa Suu (稀羽すう) ~",
    "焔魔るり": "Enma Ruri (焔魔るり) ~",
    "龍ヶ崎リン": "Ryugasaki Rene (龍ヶ崎リン) ~",
    "千代浦蝶美": "Chiyoura Chomi (千代浦蝶美) ~",
    "月ノ美兎": "Tsukino Mito (月ノ美兎) ~",
    "樋口楓": "Higuchi Kaede (樋口楓) ~",
    "町田ちま": "Machita Chima (町田ちま) ~",
    "花譜": "KAF (花譜) ~",
    "理芽": "RIM (理芽) ~",
    "春猿火": "Harusaruhi (春猿火) ~",
    "ヰ世界情緒": "Isekaijoucho (ヰ世界情緒) ~",
    "長瀬有花": "Nagase Yuka (長瀬有花) ~",
    "棗いつき": "Natsume Itsuki (棗いつき) ~",
    "中恵光城": "Nakae Mitsuki (中恵光城) ~",
    "波乗りザッパ": "Naminori Zappa (波乗りザッパ) ~",
    "まめこ": "Mameko (まめこ) ~",
    "ずっと真夜中でいいのに。": "ZUTOMAYO (ずっと真夜中でいいのに。) ~",
    "ヨルシカ": "Yorushika (ヨルシカ) ~",
    "そらる": "Soraru (そらる) ~",
    "ゴホウビ": "Gohobi (ゴホウビ) ~",
    "藤川千愛": "Fujikawa Chiai (藤川千愛) ~",
    "ナナヲアカリ": "Nanawoakari (ナナヲアカリ) ~",
    "七海うらら": "Nanami Urara (七海うらら) ~",
    "小倉唯": "Ogura Yui (小倉唯) ~",
    "小玉ひかり": "Kodama Hikari (小玉ひかり) ~",
    "田中有紀": "Tanaka Yuki (田中有紀) ~",
    "青山なぎさ": "Aoyama Nagisa (青山なぎさ) ~",
    "楠木ともり": "Kusunoki Tomori (楠木ともり) ~",
    "鈴木愛奈": "Suzuki Aina (鈴木愛奈) ~",
    "柚木梨沙": "Yuzuki Risa (柚木梨沙) ~",
    "ツユ": "TUYU (ツユ) ~",
    "ピノキオピー": "PinocchioP (ピノキオピー) ~",
    "結束バンド": "Kessoku Band (結束バンド) ~",
    "トゲナシトゲアリ": "Togenashi Togeari (トゲナシトゲアリ) ~",
    "初星学園": "Hatsuboshi Gakuen (初星学園) ~",
    "初音ミク": "Hatsune Miku (初音ミク) ~",
    "鏡音リン": "Kagamine Rin (鏡音リン) ~",
    "鏡音レン": "Kagamine Len (鏡音レン) ~",
    "巡音ルカ": "Megurine Luka (巡音ルカ) ~",
    "まふまふ": "Mafumafu (まふまふ) ~",
    "96猫": "96Neko (96猫) ~",
    "P丸様。": "P-Maru-sama. (P丸様。) ~",
    "緑黄色社会": "Ryokuoushoku Shakai (緑黄色社会) ~",
    "羊文学": "Hitsujibungaku (羊文学) ~",
    "優里": "Yuuri (優里) ~",
    "なとり": "Natori (なとり) ~",
    "須田景凪": "Suda Keina (須田景凪) ~",
    "三月のパンタシア": "Sangatsu no Phantasia (三月のパンタシア) ~",
    "藍井エイル": "Aoi Eir (藍井エイル) ~",
    "高橋李依": "Takahashi Rie (高橋李依) ~",
    "岡咲美保": "Okasaki Miho (岡咲美保) ~",
    "あたらよ": "Atarayo (あたらよ) ~",
    "ゆこぴ": "Yukopi (ゆこぴ) ~",
    "Official髭男dism": "Official HIGE DANdism (Official髭男dism) ~",
    "夏央": "Natsuo (夏央) ~",
    "式浦躁吾": "Shikiura Sogo (式浦躁吾) ~",
    "前田佳織里": "Maeda Kaori (前田佳織里) ~",
    "サクラリウム (夕凪みちる)": "Sakurarium (Yunagi Michiru) ~",
}

VTUBER_KEYWORDS = [
    "hololive", "nijisanji", "kamitsubaki", "rk music", "vspo", "hoshimachi", "suisei",
    "azki", "fubuki", "miko", "watame", "kanata", "koyori", "kaf", "rim", "harusaruhi",
    "isekaijoucho", "botan", "noel", "tokino sora", "minato aqua", "korone", "tsukino mito",
    "higuchi kaede", "machita chima", "nornis", "regloss", "flow glow", "kobo kanaeru",
    "soraz", "babacorn", "aitsuki nakuru", "natsume itsuki", "hachi", "airi kanna", "yuni",
    "nagase yuka", "星街すいせい", "さくらみこ", "白上フブキ", "角巻わため", "天音かなた",
    "博衣こより", "花譜", "理芽", "春猿火", "ヰ世界情緒", "獅白ぼたん", "白銀ノエル",
    "ときのそら", "湊あくあ", "戌神ころね", "月ノ美兎", "樋口楓", "町田ちま", "長瀬有花",
    "棗いつき", "藍月なくる", "理芽"
]

VOCALOID_KEYWORDS = [
    "vocaloid", "hatsune miku", "初音ミク", "deco*27", "deco_27", "deco∗27", "kikuo", "pinocchiop",
    "ピノキオピー", "tuyu", "ツユ", "cevio", "synthesizer v", "gumi", "ia", "flower", "kasane teto"
]

ANIME_FRANCHISES = {
    "gakumas": "Anime/THE IDOLM@STER ~/学園アイドルマスター",
    "学園アイドルマスター": "Anime/THE IDOLM@STER ~/学園アイドルマスター",
    "shiny colors": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "シャイニーカラーズ": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "イルミネーションスターズ": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "アンティーカ": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "放課後クライマックスガールズ": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "アルストロメリア": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "ストレイライト": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "ノクチル": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "シーズ": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "コメティック": "Anime/THE IDOLM@STER ~/シャイニーカラーズ",
    "idolm@ster": "Anime/THE IDOLM@STER ~",
    "アイドルマスター": "Anime/THE IDOLM@STER ~",
    "uma musume": "Anime/Uma Musume ~",
    "ウマ娘": "Anime/Uma Musume ~",
    "bang dream": "Anime/BanG Dream! ~",
    "バンドリ": "Anime/BanG Dream! ~",
    "mygo": "Anime/BanG Dream! ~",
    "ave mujica": "Anime/BanG Dream! ~",
    "girls band cry": "Anime/ガールズバンドクライ (Girls Band Cry) ~",
    "トゲナシトゲアリ": "Anime/ガールズバンドクライ (Girls Band Cry) ~",
    "bocchi the rock": "Anime/結束バンド (Bocchi the Rock!) ~",
    "結束バンド": "Anime/結束バンド (Bocchi the Rock!) ~",
    "d4dj": "Anime/D4DJ ~",
    "love live": "Anime/Love Live ~",
    "ラブライブ": "Anime/Love Live ~",
    "idoly pride": "Anime/IDOLY PRIDE ~",
    "ご注文はうさぎですか": "Anime/ご注文はうさぎですか？？ (Gochuumon wa Usagi Desu ka) ~",
    "b小町": "Anime/【推しの子】 (Oshi no Ko) ~"
}

def write_progress(phase, current, total, start_time):
    elapsed = time.time() - start_time
    pct = (current / total * 100) if total > 0 else 0
    eta_sec = (elapsed / current * (total - current)) if current > 0 else 0
    data = {
        "phase": phase,
        "current": current,
        "total": total,
        "percentage": round(pct, 2),
        "elapsed_sec": round(elapsed, 1),
        "eta_sec": round(eta_sec, 1),
        "eta_formatted": time.strftime("%H:%M:%S", time.gmtime(eta_sec)),
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_vorbis_comment(filepath):
    tags = {}
    try:
        with open(filepath, 'rb') as f:
            header = f.read(4)
            if header != b'fLaC':
                return tags
            while True:
                block_header = f.read(4)
                if len(block_header) < 4:
                    break
                is_last = bool(block_header[0] & 0x80)
                block_type = block_header[0] & 0x7F
                length = struct.unpack('>I', b'\x00' + block_header[1:4])[0]
                if block_type == 4: # VORBIS_COMMENT
                    vendor_length = struct.unpack('<I', f.read(4))[0]
                    f.read(vendor_length)
                    user_comment_list_length = struct.unpack('<I', f.read(4))[0]
                    for _ in range(user_comment_list_length):
                        comment_length = struct.unpack('<I', f.read(4))[0]
                        comment = f.read(comment_length).decode('utf-8', errors='replace')
                        if '=' in comment:
                            k, v = comment.split('=', 1)
                            tags[k.upper()] = v.strip()
                    return tags
                else:
                    f.seek(length, 1)
                if is_last:
                    break
    except Exception:
        pass
    return tags

def clean_smb_name(s):
    s = s.replace('*', '＊')
    s = s.replace(':', '：')
    s = s.replace('?', '？')
    s = s.replace('"', "''")
    s = s.replace('<', '＜')
    s = s.replace('>', '＞')
    s = s.replace('|', '｜')
    s = s.replace('/', '／')
    s = s.replace('\\', '＼')
    return s.strip()

def clean_album_title(album_raw, artist_name=""):
    title = album_raw
    # Remove leading dates [YYYY.MM.DD] or [YYYY-MM-DD] or (YYYY.MM.DD) or [YYYY-YYYY]
    title = re.sub(r'^[\[\(]\d{2,4}[\.\-\/]\d{1,2}[\.\-\/]\d{1,2}[\]\)]\s*', '', title)
    title = re.sub(r'^[\[\(]\d{4}[\.\-\/]\d{4}[\]\)]\s*', '', title)
    title = re.sub(r'^[\[\(]\d{4}\.\d{2}[\]\)]\s*', '', title)
    title = re.sub(r'^[\[\(]\d{4}[\]\)]\s*', '', title)
    
    # Remove trailing/internal formats: [FLAC 96kHz／24bit], [WEB-FLAC], (2025), [CD], [16B-44.1kHz] etc.
    title = re.sub(r'\s*[\[\(]?(?:WEB-)?(?:FLAC|MP3|Hi-Res|CD-FLAC|BK|EAC|CUE|LOG).*?[\]\)]?', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*[\[\(]\d{1,3}(?:\.\d+)?(?:k|K)?Hz[\/／]\d{1,2}bit[\]\)]', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*[\[\(]\d{1,2}B-\d{1,3}(?:\.\d+)?kHz[\]\)]', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*[\[\(]\d{4}[\]\)]', '', title)
    
    # Remove redundant "Artist - " prefix
    if artist_name and title.lower().startswith(artist_name.lower() + " - "):
        title = title[len(artist_name) + 3:].strip()
    elif artist_name and title.lower().startswith(artist_name.lower() + " — "):
        title = title[len(artist_name) + 3:].strip()

    title = clean_smb_name(title)
    return title.strip()

def format_artist_folder(artist_raw):
    artist = artist_raw.strip()
    if not artist:
        return "Unknown Artist ~"
    
    # Check known table
    for k, v in ARTIST_ROMAJI_MAP.items():
        if k == artist or k in artist:
            return v
            
    # Check if artist already has Romaji (Kanji) pattern
    if re.search(r'^[A-Za-z0-9\s\.\'\-]+\s*\([^\)]+\)', artist):
        return f"{clean_smb_name(artist)} ~"
    
    # If pure ASCII / English
    if all(ord(c) < 128 for c in artist):
        return f"{clean_smb_name(artist)} ~"
        
    return f"{clean_smb_name(artist)} ~"

def main():
    start_time = time.time()
    print("Finding all album directories in /mnt/hdd-backup/music/Lossless/...")
    write_progress("Discovery", 0, 1, start_time)

    # Use existing SQLite catalog to quickly get all unique album directories
    conn = sqlite3.connect('/mnt/hdd-backup/music/catalog.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT relative_path FROM tracks WHERE is_lossless = 1;")
    album_rel_dirs = set()
    for row in cur.fetchall():
        rel = row[0]
        # rel looks like: Lossless/J-Pop/Artist ~/Album/01.flac
        parts = rel.split('/')
        if len(parts) >= 4:
            # Check if innermost is Disc 1 / CD1
            if re.match(r'^(?:disc|cd)\s*\d+$', parts[-2], re.IGNORECASE) and len(parts) >= 5:
                album_rel = '/'.join(parts[1:-2])
            else:
                album_rel = '/'.join(parts[1:-1])
            album_rel_dirs.add(album_rel)
    conn.close()

    total_albums = len(album_rel_dirs)
    print(f"Discovered {total_albums} unique album directories.")

    plan = []
    scanned_count = 0

    for album_rel in sorted(list(album_rel_dirs)):
        scanned_count += 1
        full_path = os.path.join("/mnt/hdd-backup/music", "Lossless", album_rel)
        if not os.path.exists(full_path):
            continue

        parts = album_rel.split('/')
        current_cat = parts[0]
        current_artist = parts[1] if len(parts) > 1 else ""
        current_album = parts[-1]

        # Read tags from first available flac
        tags = {}
        try:
            for root, dirs, files in os.walk(full_path):
                flacs = [f for f in files if f.lower().endswith('.flac')]
                if flacs:
                    tags = parse_vorbis_comment(os.path.join(root, flacs[0]))
                    if tags:
                        break
        except Exception:
            pass

        artist_raw = tags.get('ARTIST') or current_artist.replace(' ~', '')
        album_raw = tags.get('ALBUM') or current_album

        # Check franchise umbrella
        is_franchise = False
        target_path = None

        if "THE IDOLM@STER ~" in album_rel or "学園アイドルマスター" in album_rel or "シャイニーカラーズ" in album_rel:
            is_franchise = True
            # Keep franchise subseries intact, just clean the album folder name
            clean_alb = clean_album_title(album_raw, artist_raw) or clean_album_title(current_album, artist_raw)
            parent_dir = os.path.dirname(full_path)
            target_path = os.path.join(parent_dir, clean_alb)

        elif "Uma Musume ~" in album_rel or "ウマ娘" in album_rel:
            is_franchise = True
            clean_alb = clean_album_title(album_raw, artist_raw) or clean_album_title(current_album, artist_raw)
            parent_dir = os.path.dirname(full_path)
            target_path = os.path.join(parent_dir, clean_alb)

        else:
            # Regular Artist
            target_cat = current_cat
            # Reclassify Vtuber
            for kw in VTUBER_KEYWORDS:
                if kw.lower() in f"{artist_raw} {album_raw}".lower():
                    target_cat = "Vtuber"
                    break

            target_artist_folder = format_artist_folder(artist_raw)
            clean_alb = clean_album_title(album_raw, artist_raw) or clean_album_title(current_album, artist_raw)
            target_path = os.path.join(BASE_DIR, target_cat, target_artist_folder, clean_alb)

        if full_path != target_path:
            plan.append({
                "source": full_path,
                "target": target_path,
                "needs_rename": True
            })

        if scanned_count % 50 == 0 or scanned_count == total_albums:
            write_progress("Analyzing Metadata", scanned_count, total_albums, start_time)

    with open(OUTPUT_PLAN, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    write_progress("Completed", total_albums, total_albums, start_time)
    print(f"Analysis complete. Total albums needing rename/reorganization: {len(plan)} out of {total_albums}")

if __name__ == '__main__':
    main()
