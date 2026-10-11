#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REORGANIZE ROMAJI-FIRST & VTUBER REALIGNMENT
1. Rescues Tanaka Yuki's Idolmaster album to Shiny Colors.
2. Relocates all VTuber talents out of J-Pop into Vtuber/ (Hololive, Nijisanji, VSPO, RK Music, etc.).
3. Enforces strict Romaji-First: inverts all 'Japanese (Romaji) ~' to 'Romaji (Japanese) ~'.
4. Romanizes all pure Japanese folders 'Japanese ~' to 'Romaji (Japanese) ~' using dictionary + kakasi.
5. Rebuilds permissions and master catalog.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

LOSSLESS = Path('/mnt/hdd-backup/music/Lossless')

def log(msg):
    print(f"[ROMAJI-FIX] {msg}", flush=True)

def safe_move(src: Path, dst: Path):
    if not src.exists():
        return
    if src == dst:
        return

    # Guard against Errno 36: File name too long
    dst_name_bytes = dst.name.encode('utf-8')
    if len(dst_name_bytes) > 230:
        # truncate safely
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
    except Exception as e:
        log(f"  Move Error {src} -> {dst}: {e}")

# Kakasi Romanizer Wrapper
def kakasi_romanize(text: str) -> str:
    try:
        # Strip trailing ~ or parens
        clean = text.strip('~').strip()
        p1 = subprocess.Popen(["iconv", "-f", "utf-8", "-t", "euc-jp", "-c"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p2 = subprocess.Popen(["kakasi", "-Ja", "-Ha", "-Ka", "-Ea", "-s"], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p1.stdout.close()
        p3 = subprocess.Popen(["iconv", "-f", "euc-jp", "-t", "utf-8", "-c"], stdin=p2.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p2.stdout.close()
        p1.communicate(clean.encode('utf-8'))
        out, _ = p3.communicate()
        raw_romaji = out.decode('utf-8', errors='ignore').strip()
        # Clean up kakasi artifacts
        raw_romaji = raw_romaji.replace("^", "").replace("'", "")
        # Title case words
        words = [w.capitalize() for w in raw_romaji.split() if w]
        return " ".join(words)
    except Exception:
        return ""

# Known well-formatted artist names dict (Priority mapping)
KNOWN_MAPPINGS = {
    # Anime / Franchise
    'うたごえはミルフィーユ': 'Utagoe wa Mille-Feuille',
    'ウルトラマンアーク': 'Ultraman Arc',
    'ご注文はうさぎですか？？': 'Gochuumon wa Usagi Desu ka',
    'スローループ': 'Slow Loop',
    'ソードアート・オンライン': 'Sword Art Online',
    'テトリス': 'Tetris',
    'トワツガイ': 'Towatsugai',
    'バクプリチャンネル': 'Bakupuri Channel',
    'ハコニワリリィ': 'Hakoniwa Lily',
    'ばっどがーる': 'Bad Girl',
    'ヒーラー・ガール': 'Healer Girl',
    'ひとりぼっちの○○生活': 'Hitoribocchi',
    'プロジェクトセカイ': 'Project SEKAI',
    'マクロスΔ': 'Macross Delta',
    'メメントモリ': 'MementoMori',
    'ゆるキャン△': 'Yuru Camp',
    'らぶフォー': 'Love4',
    '三ツ星カラーズ': 'Mitsuboshi Colors',
    '中嶋イッキュウ': 'Ikkyu Nakajima',
    '五等分の花嫁': 'Gotoubun no Hanayome',
    '君のことが大大大大大好きな100人の彼女': '100 Kanojo',
    '女神のカフェテラス': 'Megami no Cafe Terrace',
    '新米オッサン冒険者': 'Shinmai Ossan Boukensha',
    '艦隊これくしょん -艦これ-': 'Kancolle',
    '菜なれ花なれ': 'Narenare',
    '負けヒロインが多すぎる！': 'Makeine',
    '魔王2099': 'Maou 2099',
    
    # Doujinshi
    'イオシス': 'IOSYS',
    'イシカダス': 'Ishikadasu',
    'まめこ': 'Sugar Bunny',
    '中恵光城': 'ABSOLUTE CASTAWAY',
    '帝國交響楽団': 'Empire Ensemble',
    '朱落秋乡': 'Zhu Luo Qiu Xiang',
    '森羅万象': 'Shinra-Bansho',
    '波乗りザッパ': 'Naminori Zappa',
    '葉月ゆら': 'Hatsuki Yura',

    # Famous J-Pop Artists
    'アイナ・ジ・エンド': 'Aina The End',
    'いきものがかり': 'Ikimonogakari',
    'アド': 'Ado',
    'キタニタツヤ': 'Tatsuya Kitani',
    'きゃりーぱみゅぱみゅ': 'Kyary Pamyu Pamyu',
    'ヒトリエ': 'Hitorie',
    '女王蜂': 'Queen Bee',
    '家入レオ': 'Leo Ieiri',
    'サイダーガール': 'Cidergirl',
    'パスピエ': 'Passepied',
    'ちゃんみな': 'Chanmina',
    'ポルノグラフィティ': 'Porno Graffitti',
    'マカロニえんぴつ': 'Macaroni Empitsu',
    'ポルカドットスティングレイ': 'Polkadot Stingray',
    '米津玄師': 'Kenshi Yonezu',
    '花澤香菜': 'Kana Hanazawa',
    '水樹奈々': 'Nana Mizuki',
    '水瀬いのり': 'Inori Minase',
    '雨宮天': 'Sora Amamiya',
    '鬼頭明里': 'Akari Kito',
    '西川貴教': 'Takanori Nishikawa',
    '西野カナ': 'Kana Nishino',
    '直田姫奈': 'Hina Suguta',
    '小倉 唯': 'Yui Ogura',
    '上田麗奈': 'Reina Ueda',
    '内田真礼': 'Maaya Uchida',
    '楠木ともり': 'Tomori Kusunoki',
    '大西亜玖璃': 'Aguri Oonishi',
    '石原夏織': 'Kaori Ishihara',
    '田所あずさ': 'Azusa Tadokoro',
    '鈴木愛理': 'Airi Suzuki',
    '鈴木このみ': 'Konomi Suzuki',
    '鈴木愛奈': 'Aina Suzuki',
    '麻倉もも': 'Momo Asakura',
    '豊崎 愛生': 'Aki Toyosaki',
    '日向坂46': 'Hinatazaka46',
    '櫻坂46': 'Sakurazaka46',
    '乃木坂46': 'Nogizaka46',
    '手嶌葵': 'Aoi Teshima',
    '秦基博': 'Motohiro Hata',
    '阿部真央': 'Mao Abe',
    '由薫': 'YU-KA',
    '優里': 'Yuuri',
    '美波': 'Minami',
    'ロクデナシ': 'Rokudenashi',
    '緑黄色社会': 'Ryokuoushoku Shakai',
    'あたらよ': 'Atarayo',
    'クレナズム': 'Culenasm',
    'ナナヲアカリ': 'Nanawoakari',
    'くじら': 'Kujira',
    '上白石萌音': 'Mone Kamishiraishi',
    '藤川千愛': 'Chiai Fujikawa',
    'レオナ': 'ReoNa',
    '佐々木恵梨': 'Eri Sasaki',
    '小玉ひかり': 'Hikari Kodama',
    'ゴホウビ': 'Gohobi',
    'シユイ': 'Shiyui',
    'ミセカイ': 'Misekai',
    '空白ごっこ': 'Kuhaku Gokko',
    '現実みろ': 'Real Miro',
    '青山なぎさ': 'Nagisa Aoyama',
    '酔シグレ': 'Yoishigure',
    '雨宿り': 'Amayadori',
    '田中有紀': 'Yuki Tanaka',
    '八木海莉': 'Kairi Yagi',
    'はるまきごはん': 'Harumaki Gohan',
    '花たん': 'Hanatan',
    'そらる': 'Soraru',
    '煮ル果実': 'NILFRUITS',
    'すりぃ': 'Surii',
    'なとり': 'Natori',
    'ねぐせ。': 'Neguse',
    'ネクライトーキー': 'Necry Talkie',
    '新しい学校のリーダーズ': 'Atarashii Gakko!',
    '重音テト': 'Kasane Teto',
    '私立恵比寿中学': 'Shiritsu Ebisu Chugaku',
    '超特急': 'Bullet Train',
    '和楽器バンド': 'Wagakki Band',
}

# VTuber Specific Mappings out of J-Pop -> (Target Umbrella, Canonical Name)
VTUBER_MAPPINGS = {
    # Hololive
    '不知火フレア': ('Hololive (ホロライブ) ~', 'Shiranui Flare (不知火フレア) ~'),
    '夏色まつり': ('Hololive (ホロライブ) ~', 'Natsuiro Matsuri (夏色まつり) ~'),
    '大空スバル': ('Hololive (ホロライブ) ~', 'Oozora Subaru (大空スバル) ~'),
    '宝鐘マリン': ('Hololive (ホロライブ) ~', 'Houshou Marine (宝鐘マリン) ~'),
    '常闇トワ': ('Hololive (ホロライブ) ~', 'Tokoyami Towa (常闇トワ) ~'),
    '雪花ラミィ': ('Hololive (ホロライブ) ~', 'Yukihana Lamy (雪花ラミィ) ~'),
    '風真いろは': ('Hololive (ホロライブ) ~', 'Kazama Iroha (風真いろは) ~'),
    '儒烏風亭らでん': ('Hololive (ホロライブ) ~', 'Juufuutei Raden (儒烏風亭らでん) ~'),
    '儒烏風亭らでん & 轟はじめ': ('Hololive (ホロライブ) ~', 'Juufuutei Raden (儒烏風亭らでん) ~'),
    '一条莉々華': ('Hololive (ホロライブ) ~', 'Ichijou Ririka (一条莉々華) ~'),
    '音乃瀬奏': ('Hololive (ホロライブ) ~', 'Otonose Kanade (音乃瀬奏) ~'),
    '轟はじめ': ('Hololive (ホロライブ) ~', 'Todoroki Hajime (轟はじめ) ~'),
    '鷹嶺ルイ': ('Hololive (ホロライブ) ~', 'Takane Lui (鷹嶺ルイ) ~'),
    '兎田ぺこら': ('Hololive (ホロライブ) ~', 'Usada Pekora (兎田ぺこら) ~'),
    '魔法少女ホロウィッチ!': ('Hololive (ホロライブ) ~', 'ホロウィッチ! (HoloWitches) ~'),
    
    # Nijisanji
    '剣持刀也': ('Nijisanji (にじさんじ) ~', 'Kenmochi Toya (剣持刀也) ~'),
    '夢追翔': ('Nijisanji (にじさんじ) ~', 'Yumeoi Kakeru (夢追翔) ~'),
    '葛葉': ('Nijisanji (にじさんじ) ~', 'Kuzuha (葛葉) ~'),

    # VSPO (ぶいすぽっ！)
    '橘ひなの': ('VSPO (ぶいすぽっ！) ~', 'Tachibana Hinano (橘ひなの) ~'),
    '神成きゅぴ': ('VSPO (ぶいすぽっ！) ~', 'Kaminari Qpi (神成きゅぴ) ~'),
    '空澄セナ': ('VSPO (ぶいすぽっ！) ~', 'Asumi Sena (空澄セナ) ~'),
    '猫汰つな': ('VSPO (ぶいすぽっ！) ~', 'Nekota Tsuna (猫汰つな) ~'),
    '兎咲ミミ': ('VSPO (ぶいすぽっ！) ~', 'Tosaki Mimi (兎咲ミミ) ~'),
    'のあ': ('VSPO (ぶいすぽっ！) ~', 'Kurumi Noah (胡桃のあ) ~'),
    '胡桃のあ': ('VSPO (ぶいすぽっ！) ~', 'Kurumi Noah (胡桃のあ) ~'),
    '英リサ': ('VSPO (ぶいすぽっ！) ~', 'Hanabusa Lisa (英リサ) ~'),
    '八雲べに': ('VSPO (ぶいすぽっ！) ~', 'Yakumo Beni (八雲べに) ~'),
    '小森めと': ('VSPO (ぶいすぽっ！) ~', 'Komori Meto (小森めと) ~'),
    '藍沢エマ': ('VSPO (ぶいすぽっ！) ~', 'Aizawa Ema (藍沢エマ) ~'),
    '紫宮るな': ('VSPO (ぶいすぽっ！) ~', 'Shinomiya Runa (紫宮るな) ~'),
    '白波らむね': ('VSPO (ぶいすぽっ！) ~', 'Shiranami Ramune (白波らむね) ~'),
    '夢野あかり': ('VSPO (ぶいすぽっ！) ~', 'Yumeno Akari (夢野あかり) ~'),
    '夜乃くろむ': ('VSPO (ぶいすぽっ！) ~', 'Yano Kuromu (夜乃くろむ) ~'),
    '紡木こかげ': ('VSPO (ぶいすぽっ！) ~', 'Tsumugi Kokage (紡木こかげ) ~'),
    '千燈ゆうひ': ('VSPO (ぶいすぽっ！) ~', 'Sendo Yuuhi (千燈ゆうひ) ~'),

    # RK Music / RIOT MUSIC / Other
    '瀬戸乃とと': ('RK Music ~', 'Setono Toto (瀬戸乃とと) ~'),
    '深影': ('RK Music ~', 'Mikage (深影) ~'),
    '明透': ('KAMITSUBAKI STUDIO (神椿スタジオ) ~', 'ASU (明透) ~'),
    '結城さくな': ('', 'Yuuki Sakuna (結城さくな) ~'),
    '緋月ゆい': ('', 'Hizuki Yui (緋月ゆい) ~'),
    '宗谷いちか': ('', 'Ichika Souya (宗谷いちか) ~'),
    '神楽めあ': ('', 'Kagura Mea (神楽めあ) ~'),
    '碧依さくら': ('', 'Aoi Sakura (碧依さくら) ~'),
    '七海うらら': ('', 'Nanami Urara (七海うらら) ~'),
    'ピーナッツくん': ('', 'Peanuts-kun (ピーナッツくん) ~'),
    'さえきやひろ': ('', 'Saeki Yahiro (さえきやひろ) ~'),
    'しぐれうい': ('', 'Ui Shigure (しぐれうい) ~'),
    '凛々咲': ('', 'Ririsya (凛々咲) ~'),
    '勿忘うた': ('', 'Uta Wasurena (勿忘うた) ~'),
    '東雪蓮': ('', 'Azuma Seren (東雪蓮) ~'),
    '燦鳥ノム': ('', 'Suntory Nomu (燦鳥ノム) ~'),
    '白雪ひな': ('', 'Shirayuki Hina (白雪ひな) ~'),
    '織姫はるか': ('', 'Orihime Haruka (織姫はるか) ~'),
    '花鋏キョウ': ('', 'Hanabasami Kyo (花鋏キョウ) ~'),
    '藍月なくる': ('', 'Aitsuki Nakuru (藍月なくる) ~'),
    '釣鐘ふうり': ('', 'Fuuri Tsurigane (釣鐘ふうり) ~'),
    '陽月るるふ': ('', 'Hizuki Ruruhu (陽月るるふ) ~'),
    '音門るき': ('', 'Ruki Otokado (音門るき) ~'),
    '龍ヶ崎リン': ('', 'Ryugasaki Rene (龍ヶ崎リン) ~'),
}

# ==============================================================================
# 1. FIX TANAKA YUKI'S SHINY COLORS ALBUM
# ==============================================================================
def fix_tanaka_yuki():
    log("=== FIXING TANAKA YUKI SHINY COLORS ALBUM ===")
    imas_shiny_collab = LOSSLESS / 'Anime' / 'THE IDOLM@STER (アイドルマスター) ~' / 'Shiny Colors (シャイニーカラーズ) ~' / '05. Synthe-Side & Collaborations'
    imas_shiny_collab.mkdir(parents=True, exist_ok=True)

    for cat in ['Anime', 'J-Pop']:
        for tanaka in (LOSSLESS / cat).glob('*Tanaka Yuki*'):
            album = tanaka / 'THE IDOLM@STER SHINY COLORS シャイニーPRオファー Vol.3'
            if album.exists():
                log(f"  Found Shiny Colors Vol.3 in {tanaka} -> moving to Shiny Colors Collab...")
                safe_move(album, imas_shiny_collab / album.name)
            # check if any other imas album inside
            for item in list(tanaka.iterdir()):
                if 'IDOLM@STER' in item.name:
                    safe_move(item, imas_shiny_collab / item.name)

# ==============================================================================
# 2. RELOCATE VTUBERS OUT OF J-POP
# ==============================================================================
def fix_vtubers_in_jpop():
    log("=== RELOCATING VTUBERS OUT OF J-POP ===")
    jpop = LOSSLESS / 'J-Pop'
    vtuber = LOSSLESS / 'Vtuber'

    for folder in list(jpop.iterdir()):
        if not folder.is_dir():
            continue
        raw_name = folder.name.strip('~').strip()
        
        # Match against known VTubers
        matched = False
        for vt_key, (agency, canon_name) in VTUBER_MAPPINGS.items():
            if raw_name == vt_key or raw_name.startswith(vt_key + ' ') or f'({vt_key})' in raw_name or f' {vt_key}' in raw_name:
                matched = True
                if agency:
                    target_dir = vtuber / agency / canon_name
                else:
                    target_dir = vtuber / canon_name
                log(f"  Moving VTuber from J-Pop: {folder.name} -> {target_dir.relative_to(LOSSLESS)}")
                safe_move(folder, target_dir)
                break

    # Also clean existing loose vtuber folders in Vtuber/
    for folder in list(vtuber.iterdir()):
        if not folder.is_dir() or folder.name.endswith('~') is False:
            continue
        raw_name = folder.name.strip('~').strip()
        for vt_key, (agency, canon_name) in VTUBER_MAPPINGS.items():
            if (raw_name == vt_key or raw_name.startswith(vt_key + ' ') or f'({vt_key})' in raw_name) and agency:
                target_dir = vtuber / agency / canon_name
                if folder != target_dir and folder != (vtuber / agency):
                    log(f"  Consolidating Vtuber into {agency}: {folder.name} -> {target_dir.relative_to(LOSSLESS)}")
                    safe_move(folder, target_dir)
                    break

# ==============================================================================
# 3. UNIVERSAL ROMAJI-FIRST INVERSION & CONVERSION
# ==============================================================================
def normalize_folder_name(name: str) -> str:
    """Returns canonical 'Romaji (Japanese) ~' for a folder name."""
    clean = name.strip('~').strip()

    # Rule 0: If name contains '(' and ends with ')', check if already Romaji-First or inverted
    if '(' in clean and clean.endswith(')'):
        paren_idx = clean.find('(')
        before_paren = clean[:paren_idx].strip()
        inside_paren = clean[paren_idx + 1 : -1].strip()

        is_before_ascii = all(ord(c) < 128 for c in before_paren) if before_paren else False
        is_inside_cjk = any('\u4e00' <= c <= '\u9fff' or '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in inside_paren)
        
        # Already Romaji (Japanese) ~
        if is_before_ascii and is_inside_cjk:
            return f"{before_paren} ({inside_paren}) ~"

        is_before_cjk = any('\u4e00' <= c <= '\u9fff' or '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in before_paren)
        is_inside_ascii = all(ord(c) < 128 for c in inside_paren)
        
        # Inverted: Japanese (Romaji) ~ -> Invert to Romaji (Japanese) ~
        if is_before_cjk and is_inside_ascii:
            ro = " ".join(w.capitalize() if not w.isupper() else w for w in inside_paren.split())
            return f"{ro} ({before_paren}) ~"

    # Rule 1: Check known mappings
    if clean in KNOWN_MAPPINGS:
        return f"{KNOWN_MAPPINGS[clean]} ({clean}) ~"

    # Rule 2: If entirely ASCII (Latin alphabet/symbols), leave with tilde
    if all(ord(c) < 128 for c in clean):
        return f"{clean} ~"

    # Rule 3: Pure Japanese -> Romanize via kakasi
    has_cjk = any('\u4e00' <= c <= '\u9fff' or '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in clean)
    if has_cjk:
        ro = kakasi_romanize(clean)
        if ro:
            # Clamp length to prevent Errno 36
            if len(ro.encode('utf-8')) + len(clean.encode('utf-8')) > 180:
                ro = ro[:40].strip()
            return f"{ro} ({clean}) ~"

    return f"{clean} ~"

def clean_album_title(name: str) -> str:
    # Remove "Artist 1stアルバムTitle" pattern -> Title
    m_alb = re.search(r'\d+(?:st|nd|rd|th)?アルバム[「『]?([^」』]+)[」』]?', name)
    if m_alb:
        name = m_alb.group(1).strip()
    m_sing = re.search(r'\d+(?:st|nd|rd|th)?シングル[「『]?([^」』]+)[」』]?', name)
    if m_sing:
        name = m_sing.group(1).strip()
    name = re.sub(r'^\[\d{4}[.\-_]\d{2}[.\-_]\d{2}\]\s*', '', name)
    name = re.sub(r'\[(?:FLAC|MP3|WEB|CD|EAC|Hi-Res|Lossless|24bit|16bit|44\.1kHz|48kHz|96kHz|192kHz|Qobuz|Mora|Ototoy|Vinyl)[^\]]*\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\((?:FLAC|MP3|WEB|CD|EAC|Hi-Res|Lossless|24bit|16bit|44\.1kHz|48kHz|96kHz|192kHz)[^\)]*\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\{[A-Z0-9\-_]+\}\s*\[(?:CD-)?FLAC\][^\s]*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*\[\d{4}[.\-_]\d{2}[.\-_]\d{2}\]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def execute_romaji_first_across_categories():
    log("=== ENFORCING ROMAJI-FIRST ACROSS ALL CATEGORIES ===")
    for cat in ['Anime', 'J-Pop', 'Vtuber', 'Doujinshi']:
        cat_dir = LOSSLESS / cat
        if not cat_dir.exists():
            continue
        log(f"Processing category: {cat}...")
        for folder in list(cat_dir.iterdir()):
            if not folder.is_dir():
                continue
            
            # If it's an agency folder in Vtuber, process its children!
            if cat == 'Vtuber' and folder.name in ['Hololive (ホロライブ) ~', 'Nijisanji (にじさんじ) ~', 'VSPO (ぶいすぽっ！) ~', 'KAMITSUBAKI STUDIO (神椿スタジオ) ~', 'RK Music ~', 'RIOT MUSIC ~']:
                for sub in list(folder.iterdir()):
                    if not sub.is_dir():
                        continue
                    new_sub_name = normalize_folder_name(sub.name)
                    if new_sub_name != sub.name:
                        log(f"  Renaming agency subfolder: {sub.name} -> {new_sub_name}")
                        safe_move(sub, folder / new_sub_name)
                continue

            new_name = normalize_folder_name(folder.name)
            dst = cat_dir / new_name
            if new_name != folder.name:
                log(f"  Renaming {folder.name} -> {new_name}")
                safe_move(folder, dst)

            # Clean album titles inside
            target_folder = dst if dst.exists() else folder
            if target_folder.exists():
                for alb in list(target_folder.iterdir()):
                    if alb.is_dir() and not alb.name.endswith('~'):
                        calb = clean_album_title(alb.name)
                        if calb != alb.name:
                            log(f"    Cleaning album title: {alb.name} -> {calb}")
                            safe_move(alb, target_folder / calb)

def main():
    log("STARTING MASTER ROMAJI-FIRST & VTUBER REALIGNMENT...")
    fix_tanaka_yuki()
    fix_vtubers_in_jpop()
    execute_romaji_first_across_categories()

    log("Applying permissions (775/664)...")
    subprocess.run(['find', str(LOSSLESS), '-type', 'd', '-exec', 'chmod', '775', '{}', '+'])
    subprocess.run(['find', str(LOSSLESS), '-type', 'f', '-exec', 'chmod', '664', '{}', '+'])

    log("Rebuilding master catalog & M3U8 playlists...")
    subprocess.run(['python3', '/mnt/hdd-backup/music/scripts/update_catalog.py'])
    log("ROMAJI-FIRST & VTUBER REALIGNMENT COMPLETED!")

if __name__ == '__main__':
    main()
