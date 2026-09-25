#!/usr/bin/env python3
"""
analyze_download_metadata.py
Server-side read-only analysis script for /mnt/hdd-backup/download/.
Extracts Vorbis comment metadata from FLAC files and proposes a reorganization plan:
  1. Artist naming: Romaji (Kanji/Kana) ~
  2. Album naming: Pure Album Name (no dates, no formats, no years)
  3. Proper category classification (Anime, Vtuber, Vocaloid, Doujinshi, J-Pop)
  4. Collision detection & disambiguation marking
Output: /tmp/download_reorganize_plan.json
"""

import os
import sys
import json
import re
import struct
from pathlib import Path

BASE_DIR = "/mnt/hdd-backup/download"
OUTPUT_PLAN = "/tmp/download_reorganize_plan.json"
OUTPUT_SUMMARY = "/tmp/download_analyze_summary.txt"

# Known Artist Japanese -> Romaji Canonical Table
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
    "棗いつき", "藍月なくる"
]

VOCALOID_KEYWORDS = [
    "vocaloid", "hatsune miku", "初音ミク", "deco*27", "deco_27", "deco∗27", "kikuo", "pinocchiop",
    "ピノキオピー", "tuyu", "ツユ", "cevio", "synthesizer v", "gumi", "ia", "flower", "kasane teto"
]

ANIME_FRANCHISES = {
    "gakumas": "Anime/THE IDOLM@STER ~/学園アイドルマスター",
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
    except Exception as e:
        pass
    return tags

def clean_smb_name(s):
    # Windows NTFS forbidden chars: \ / : * ? " < > |
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
    """
    Strips dates, years, formats, bitrates, and redundant artist prefix to produce Pure Album Name.
    """
    title = album_raw
    # Remove leading dates [YYYY.MM.DD] or [YYYY-MM-DD] or (YYYY.MM.DD)
    title = re.sub(r'^[\[\(]\d{2,4}[\.\-\/]\d{1,2}[\.\-\/]\d{1,2}[\]\)]\s*', '', title)
    title = re.sub(r'^[\[\(]\d{4}\.\d{2}[\]\)]\s*', '', title)
    title = re.sub(r'^[\[\(]\d{4}[\]\)]\s*', '', title)
    
    # Remove trailing/internal formats: [FLAC 96kHz／24bit], [WEB-FLAC], (2025), etc.
    title = re.sub(r'\s*[\[\(]?(?:WEB-)?(?:FLAC|MP3|Hi-Res|CD-FLAC|BK|EAC).*?[\]\)]?', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*[\[\(]\d{1,3}(?:\.\d+)?(?:k|K)?Hz[\/／]\d{1,2}bit[\]\)]', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*[\[\(]\d{4}[\]\)]', '', title) # year like (2025)
    
    # Remove redundant "Artist - " prefix if present at start
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
        
    # Japanese without mapping yet
    return f"{clean_smb_name(artist)} ~"

def classify_album(current_cat, artist_raw, album_raw, track_meta):
    combined = f"{current_cat} {artist_raw} {album_raw} {track_meta.get('TITLE', '')} {track_meta.get('COMMENT', '')}".lower()
    
    # Check Anime Franchise
    for kw, target_cat in ANIME_FRANCHISES.items():
        if kw.lower() in combined:
            return target_cat.split('/')[0] # Anime
            
    # Check Vtuber
    for kw in VTUBER_KEYWORDS:
        if kw.lower() in combined:
            return "Vtuber"
            
    # Check Vocaloid
    for kw in VOCALOID_KEYWORDS:
        if kw.lower() in combined:
            return "Vocaloid"
            
    # Default to current category or J-Pop
    if current_cat in ["Anime", "Doujinshi", "Vtuber", "Vocaloid", "J-Pop", "Global"]:
        return current_cat
    return "J-Pop"

def main():
    print(f"Scanning {BASE_DIR}...")
    album_dirs = []
    for root, dirs, files in os.walk(BASE_DIR):
        flacs = [f for f in files if f.lower().endswith('.flac')]
        if flacs:
            # We found a folder containing FLAC tracks
            # Check if this is a subdisc like Disc 1, Disc 2, CD1
            base_name = os.path.basename(root)
            if re.match(r'^(?:disc|cd)\s*\d+$', base_name, re.IGNORECASE):
                continue
            album_dirs.append((root, flacs))

    print(f"Found {len(album_dirs)} album directories containing FLAC.")
    
    plan = []
    artist_albums = {} # (target_cat, artist_folder) -> list of album titles
    
    for album_path, flacs in album_dirs:
        # Sample first 2 flacs for metadata
        tags = {}
        for flac_name in flacs[:2]:
            t = parse_vorbis_comment(os.path.join(album_path, flac_name))
            if t.get('ARTIST') and t.get('ALBUM'):
                tags = t
                break
            if not tags and t:
                tags = t
                
        rel_path = os.path.relpath(album_path, BASE_DIR)
        parts = rel_path.split(os.sep)
        current_cat = parts[0] if len(parts) > 1 else "Unknown"
        
        folder_album_raw = os.path.basename(album_path)
        artist_raw = tags.get('ARTIST') or (parts[1] if len(parts) > 2 else "")
        album_raw = tags.get('ALBUM') or folder_album_raw
        
        target_cat = classify_album(current_cat, artist_raw, album_raw, tags)
        artist_folder = format_artist_folder(artist_raw)
        pure_album = clean_album_title(album_raw, artist_raw)
        
        if not pure_album:
            pure_album = clean_album_title(folder_album_raw, artist_raw)
            
        key = (target_cat, artist_folder)
        if key not in artist_albums:
            artist_albums[key] = []
        artist_albums[key].append({
            "source_path": album_path,
            "pure_album": pure_album,
            "date": tags.get('DATE') or tags.get('YEAR') or ""
        })

    # Collision Resolution:
    # If same artist has identical pure_album names, qualify with edition / release index
    for key, albums in artist_albums.items():
        cat, art = key
        # Group by pure_album
        grouped = {}
        for a in albums:
            t = a["pure_album"]
            grouped.setdefault(t, []).append(a)
            
        for title, items in grouped.items():
            if len(items) == 1:
                target_path = os.path.join(BASE_DIR, cat, art, title)
                plan.append({
                    "source": items[0]["source_path"],
                    "target": target_path,
                    "category_from": os.path.relpath(items[0]["source_path"], BASE_DIR).split(os.sep)[0],
                    "category_to": cat,
                    "artist_folder": art,
                    "pure_album": title,
                    "tags_found": bool(items[0]["date"])
                })
            else:
                for idx, a in enumerate(items, 1):
                    date = a["date"][:4] if a["date"] else ""
                    if "feat." in a["source_path"] or "Single" in a["source_path"]:
                        final_title = f"{title} (Single Edition)"
                    elif idx == 1:
                        final_title = f"{title} (Full Release)"
                    else:
                        final_title = f"{title} (Release {idx})"
                        
                    target_path = os.path.join(BASE_DIR, cat, art, final_title)
                    plan.append({
                        "source": a["source_path"],
                        "target": target_path,
                        "category_from": os.path.relpath(a["source_path"], BASE_DIR).split(os.sep)[0],
                        "category_to": cat,
                        "artist_folder": art,
                        "pure_album": final_title,
                        "tags_found": bool(a["date"])
                    })


    with open(OUTPUT_PLAN, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
        
    # Write summary
    category_shifts = {}
    for item in plan:
        cf = item["category_from"]
        ct = item["category_to"]
        if cf != ct:
            pair = f"{cf} -> {ct}"
            category_shifts[pair] = category_shifts.get(pair, 0) + 1

    summary_text = [
        f"Reorganization Metadata Analysis Summary",
        f"Total Albums Scanned: {len(plan)}",
        f"Category Reclassifications: {sum(category_shifts.values())}",
    ]
    for pair, count in sorted(category_shifts.items(), key=lambda x: x[1], reverse=True):
        summary_text.append(f"  - {pair}: {count} albums")
        
    summary_text.append("\nSample Mappings (First 15):")
    for item in plan[:15]:
        summary_text.append(f"FROM: {item['source']}")
        summary_text.append(f"TO:   {item['target']}\n")
        
    with open(OUTPUT_SUMMARY, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_text))
        
    print(f"Analysis complete. Plan written to {OUTPUT_PLAN}")
    print('\n'.join(summary_text[:15]))

if __name__ == '__main__':
    main()
