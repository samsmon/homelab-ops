#!/usr/bin/env python3
import os
import re
from pathlib import Path
from collections import defaultdict

MUSIC_ROOT = Path('/mnt/hdd-backup/music/Lossless')

def build_plan():
    plan = defaultdict(list) # cat -> list of (src_name, target_folder_name)
    
    # =========================================================================
    # 1. DOUJINSHI
    # =========================================================================
    doujin_dir = MUSIC_ROOT / 'Doujinshi'
    if doujin_dir.exists():
        for d in sorted(doujin_dir.iterdir()):
            if not d.is_dir() or d.name.endswith('~'):
                continue
            name = d.name
            target = None
            if name == 'ABSOLUTE CASTAWAY':
                target = '中恵光城 (ABSOLUTE CASTAWAY) ~'
            elif '棗いつき' in name or name == 'HAPPY ENFORCER':
                target = '棗いつき (Itsuki Natsume) ~'
            elif 'Lunatic★Melody' in name:
                target = 'Lunatic★Melody ~'
            elif name in ['Room97', 'Assortment']:
                target = 'Room97 ~'
            elif name in ['Luna']:
                target = '*Luna ~'
            elif 'なゆ茶' in name or 'nayuta' in name.lower():
                target = 'nayuta ~'
            elif 'あなたしかイラナイ' in name:
                target = '波乗りザッパ ~'
            elif name in ['180℃Girl', '[M3-43] Sugar Bunny — ぷちプリマヴェーラ [FLAC]']:
                target = 'まめこ (Sugar Bunny) ~'
            elif name == '[ahi] - sauna [FLAC]':
                target = '[ahi:] ~'
            elif name == 'fishpond':
                target = 'fishpond ~'
            elif name == 'Eufolie':
                target = 'Eufolie ~'
            elif name == 'Login Records - Never Forget Vacation 8':
                target = 'Login Records ~'
            elif 'U-ske' in name:
                target = 'U-ske SOUNDS ~'
            elif 'Ether' in name:
                target = 'Ether ~'
            elif 'Fujian' in name:
                target = 'Fujian Series ~'
            elif 'Static World' in name:
                target = 'Static World ~'
            elif 'TOHO BOSSA NOVA' in name:
                target = 'TOHO BOSSA NOVA ~'
            elif 'イシカダス' in name:
                target = 'イシカダス ~'
            elif '夏掛く先に君を待つ' in name:
                target = 'YO1YO ~'
            elif '朱落秋乡' in name:
                target = '朱落秋乡 ~'
            elif name == 'sukidesuost':
                # special handling: subfolders go to different places
                target = 'SPECIAL_SUKIDESUOST'
                
            if target:
                plan['Doujinshi'].append((name, target))

    # =========================================================================
    # 2. VTUBER
    # =========================================================================
    vtuber_dir = MUSIC_ROOT / 'Vtuber'
    if vtuber_dir.exists():
        for d in sorted(vtuber_dir.iterdir()):
            if not d.is_dir() or d.name.endswith('~'):
                continue
            name = d.name
            lower = name.lower()
            target = None
            
            # Match existing artist folders
            if any(k in lower for k in ['星街すいせい', 'suisei']):
                target = '星街すいせい (Suisex) ~'
            elif any(k in lower for k in ['azki', 'カゲロウノ調', '少年よ我に帰れ', '夢屑ケーキ']):
                target = 'Azki ~'
            elif any(k in lower for k in ['白上フブキ', 'fubuki', 'hi fine fox', 'konkon beats', 'letter☆彡', '僕らの星座', 'kingworld']):
                target = '白上フブキ (Shirakami Fubuki) ~'
            elif any(k in lower for k in ['さくらみこ', 'miko', 'flower rhapsody', 'さくらんぼメッセージ', 'イケ贄']):
                target = 'さくらみこ (Sakura Miko) ~'
            elif any(k in lower for k in ['角巻わため', 'watame']):
                target = '角巻わため (Tsunomaki Watame) ~'
            elif any(k in lower for k in ['天音かなた', 'kanata', '中空の庭', 'unknown diva', 'trigger']):
                target = '天音かなた (Kanata Amane) ~'
            elif any(k in lower for k in ['博衣こより', 'koyori']):
                target = '博衣こより (Hakui Koyori) ~'
            elif any(k in lower for k in ['花譜', 'kaf']):
                target = '花譜 (KAF) ~'
            elif any(k in lower for k in ['理芽', 'rim']):
                target = '理芽 (RIM) ~'
            elif any(k in lower for k in ['春猿火', 'harusaruhi', 'rule the world']):
                target = '春猿火 (Harusaruhi) ~'
            elif any(k in lower for k in ['ヰ世界情緒', 'isekaijoucho']):
                target = 'ヰ世界情緒 (Isekaijoucho) ~'
            elif any(k in lower for k in ['獅白ぼたん', 'botan', 'lights']):
                target = '獅白ぼたん ~'
            elif any(k in lower for k in ['白銀ノエル', 'noel', 'のえさんぽ']):
                target = '白銀ノエル ~'
            elif any(k in lower for k in ['ときのそら', 'tokino sora', 'ブルーバード']):
                target = 'ときのそら (Tokino Sora) ~'
            elif any(k in lower for k in ['湊あくあ', 'minato aqua']):
                target = '湊あくあ (Minato Aqua) ~'
            elif any(k in lower for k in ['戌神ころね', 'korone']):
                target = '戌神ころね (Inugami Korone) ~'
            elif any(k in lower for k in ['月ノ美兎', 'tsukino mito', '310phz']):
                target = '月ノ美兎 (Tsukino Mito) ~'
            elif any(k in lower for k in ['樋口楓', 'higuchi kaede', 'game girl']):
                target = '樋口楓 (Higuchi Kaede) ~'
            elif any(k in lower for k in ['町田ちま', 'machita chima']):
                target = '町田ちま (Machita Chima) ~'
            elif any(k in lower for k in ['nornis', 'salvia', 'tensegrity']):
                target = 'Nornis ~'
            elif any(k in lower for k in ['regloss', 'フィーリングラデーション', '泡沫メイビー', 'サクラミラージュ', 'ミッドサマーシトラス', '落噺', 'cheerful vibes echo', 'happiness phenomenon', 'ビリラビリラ', 'アワータイムイエロー']):
                target = 'Hololive Regloss ~'
            elif 'flow glow' in lower:
                target = 'FLOW GLOW ~'
            elif any(k in lower for k in ['kobo kanaeru', 'juara khatulistiwa', 'hololive-id', 'hololive indonesia']):
                target = 'hololive Indonesia ~'
            elif any(k in lower for k in ['soraz']):
                target = 'SorAZ ~'
            elif any(k in lower for k in ['babacorn']):
                target = 'BABACORN(宝鐘マリン／白上フブキ) ~'
            elif any(k in lower for k in ['藍月なくる', 'aitsuki nakuru']):
                target = '藍月なくる (Aitsuki Nakuru) ~'
            elif any(k in lower for k in ['棗いつき']):
                target = '棗いつき (Natsume Itsuki) ~'
            elif any(k in lower for k in ['hachi', 'close to heart']):
                target = 'Hachi ~'
            elif any(k in lower for k in ['airi kanna']):
                target = 'Airi Kanna ~'
            elif any(k in lower for k in ['yuni']):
                target = 'YuNi ~'
            elif any(k in lower for k in ['長瀬有花']):
                target = '長瀬有花 (Nagase Yuka) ~'
            elif any(k in lower for k in ['hololive', 'ホロライブ']):
                target = 'hololive Official ~'
                
            if target:
                plan['Vtuber'].append((name, target))

    # =========================================================================
    # 3. ANIME
    # =========================================================================
    anime_dir = MUSIC_ROOT / 'Anime'
    if anime_dir.exists():
        for d in sorted(anime_dir.iterdir()):
            if not d.is_dir() or d.name.endswith('~'):
                continue
            name = d.name
            lower = name.lower()
            target = None
            
            if any(k in lower for k in ['学園アイドルマスター', 'がむしゃらに行こう', 'ときめきのソルフェージュ', '桜フォトグラフ', 'endless dance', 'star-mine', 'ナイワ', '理論武装して', 'かちドキ', 'sweet magic', 'ハッピーミルフィーユ', 'たいせつなもの', 'ツキノカメ', 'top secret', 'コンテンポラリのダンス', '極光', '歌声は君いろ', 'kira kira', 'fragile heart', 'つよつよ最強エクササイズ', 'try it now', 'ミラクルナナウ', '自己肯定感爆上げ', 'supremacy', 'let\'s go!! ichi-no-ni!!', '空と約束', '見て']):
                target = '学園アイドルマスター ~'
            elif any(k in lower for k in ['シャイニーカラーズ', 'shiny colors', 'echoes', 'prism flare', 'over the prism', 'happy surprise trick', 'song for prism', 'real mind shakes']):
                target = 'アイドルマスター シャイニーカラーズ ~'
            elif any(k in lower for k in ['アイドルマスター', 'idolm@ster', 'シンデレラガールズ', 'cinderella girls', 'ミリオンライブ', 'million live']):
                target = 'THE IDOLM@STER ~'
            elif any(k in lower for k in ['bang dream', 'バンドリ', 'mygo', 'ave mujica', 'morfonica', 'poppin', 'roselia', 'raise a suilen', '夢限大みゅーたいぷ', '迷星叫', 'killkiss', 'polyphony', 'popigenic', 'completeness', 'bad kids all bet']):
                target = 'BanG Dream! ~'
            elif any(k in lower for k in ['idoly pride', 'trinityaile', 'liznoir', 'サニーピース', '月のテンペスト']):
                target = 'IDOLY PRIDE ~'
            elif any(k in lower for k in ['love live', 'ラブライブ', 'nijigaku', '虹ヶ咲', '蓮ノ空', 'aqours', 'liella', 'kurosawa dia', 'matsuura kanan', 'starry night serenade', 'compass', 'ユメワズライ', '全方位キュン', 'white delight']):
                target = 'Love Live ~'
            elif any(k in lower for k in ['ウマ娘', 'uma musume', 'animation derby', 'ロライズ']):
                target = 'Uma Musume ~'
            elif any(k in lower for k in ['ガールズバンドクライ', 'トゲナシトゲアリ', '吹き消した灯火', '最期の禱り']):
                target = 'ガールズバンドクライ (Girls Band Cry) ~'
            elif any(k in lower for k in ['結束バンド', 'ぼっち・ざ・ろっく', 'we will']):
                target = '結束バンド (Bocchi the Rock!) ~'
            elif any(k in lower for k in ['プリンセスコネクト', 'priconne', 'character song 41', 'character song 43', 'character song 44', 'character song album vol.6']):
                target = 'プリンセスコネクト！ Re：Dive ~'
            elif any(k in lower for k in ['アークナイツ', 'arknights', 'runaway', '5周年記念']):
                target = 'アークナイツ (Arknights) ~'
            elif any(k in lower for k in ['アズールレーン', 'azur lane']):
                target = 'アズールレーン (Azur Lane) ~'
            elif any(k in lower for k in ['d4dj', 'peaky p-key', 'photon maiden']):
                target = 'D4DJ ~'
            elif any(k in lower for k in ['五等分の花嫁', '五等分の笑顔']):
                target = '五等分の花嫁 ~'
            elif any(k in lower for k in ['負けヒロインが多すぎる', 'マケイン']):
                target = '負けヒロインが多すぎる！ ~'
            elif any(k in lower for k in ['spice and wolf', '狼と香辛料', 'ookami to koushinryou', 'りんごと君', 'tonari ni iruyo', 'perfect world', 'tabi no tochuu', 'mitsu no yoake', 'ringo hiyori']):
                target = 'Spice and Wolf ~'
            elif any(k in lower for k in ['三ツ星カラーズ', 'カラーズ']):
                target = '三ツ星カラーズ ~'
            elif any(k in lower for k in ['響け!ユーフォニアム', 'sound! euphonium', '北宇治高校吹奏楽部']):
                target = '響け！ユーフォニアム ~'
            elif any(k in lower for k in ['k-on', 'けいおん', 'fuwa fuwa time']):
                target = 'K-ON! ~'
            elif any(k in lower for k in ['ソードアート・オンライン', 'sao', '私たちの讃歌']):
                target = 'ソードアート・オンライン (SAO) ~'
            elif any(k in lower for k in ['少女☆歌劇', 'レヴュースタァライト', 'kleinod', '遙かなるエルドラド']):
                target = '少女☆歌劇 レヴュースタァライト ~'
            elif any(k in lower for k in ['うたごえはミルフィーユ', 'my way', 'brain hack']):
                target = 'うたごえはミルフィーユ ~'
            elif any(k in lower for k in ['tokyo 7th', 't7s']):
                target = 'Tokyo 7th シスターズ ~'
            elif any(k in lower for k in ['電音部']):
                target = '電音部 ~'
            elif any(k in lower for k in ['鳴潮', 'wuthering waves', 'never let it go']):
                target = '鳴潮 (Wuthering Waves) ~'
            elif any(k in lower for k in ['ヒーラー・ガール']):
                target = 'ヒーラー・ガール ~'
            elif any(k in lower for k in ['女神のカフェテラス']):
                target = '女神のカフェテラス ~'
            elif any(k in lower for k in ['新米オッサン']):
                target = '新米オッサン冒険者 ~'
            elif any(k in lower for k in ['菜なれ花なれ', '花になれ']):
                target = '菜なれ花なれ ~'
            elif any(k in lower for k in ['前橋ウィッチーズ']):
                target = '前橋ウィッチーズ ~'
            elif any(k in lower for k in ['スクールアイドルミュージカル']):
                target = 'スクールアイドルミュージカル ~'
            elif any(k in lower for k in ['らぶフォー', 'the magician']):
                target = 'らぶフォー ~'
            elif any(k in lower for k in ['ongeki', '音撃', 'オンゲキ']):
                target = 'ONGEKI (オンゲキ) ~'
            elif any(k in lower for k in ['うたの☆プリンセスさまっ']):
                target = 'うたの☆プリンセスさまっ♪ ~'
            elif any(k in lower for k in ['魔王2099', 'スピラ']):
                target = '魔王2099 ~'
            elif any(k in lower for k in ['vivy']):
                target = 'Vivy -Fluorite Eye\'s Song- ~'
            elif any(k in lower for k in ['メメントモリ']):
                target = 'メメントモリ ~'
                
            if target:
                plan['Anime'].append((name, target))

    # =========================================================================
    # 4. J-POP
    # =========================================================================
    jpop_dir = MUSIC_ROOT / 'J-Pop'
    if jpop_dir.exists():
        for d in sorted(jpop_dir.iterdir()):
            if not d.is_dir() or d.name.endswith('~'):
                continue
            name = d.name
            lower = name.lower()
            target = None
            
            if any(k in lower for k in ['ado', 'アド', '桜日和とタイムマシン', 'きっとコースター', '魔性少女']):
                target = 'アド (Ado) ~'
            elif any(k in lower for k in ['reona', 'レオナ', '神崎エルザ', 'elza']):
                target = 'レオナ (ReoNa) ~'
            elif any(k in lower for k in ['claris', 'クラリス', '木枯しに抱かれて', '秋のグラディエント', 'autumn tracks', '風は秋色']):
                target = 'ClariS ~'
            elif any(k in lower for k in ['ずっと真夜中でいいのに', 'zutomayo', '虚仮の一念海馬に託す']):
                target = 'ずっと真夜中でいいのに。(ZUTOMAYO ) ~'
            elif any(k in lower for k in ['ヨルシカ', 'yorushika', 'forget it']):
                target = 'ヨルシカ (Yorushika) ~'
            elif any(k in lower for k in ['yoasobi', 'new me', 'the book']):
                target = 'YOASOBI ~'
            elif any(k in lower for k in ['aimer', 'wavy flow']):
                target = 'Aimer ~'
            elif any(k in lower for k in ['そらる', 'soraru', 'ユメトキ', '創空とメルヒェン讃歌']):
                target = 'そらる ~'
            elif any(k in lower for k in ['ゴホウビ', 'gohobi']):
                target = 'ゴホウビ (Gohobi) ~'
            elif any(k in lower for k in ['藤川千愛', 'chiai fujikawa', 'さがしもの', 'kick back']):
                target = '藤川千愛 (Chiai Fujikawa) ~'
            elif any(k in lower for k in ['ナナヲアカリ', 'nanawoakari']):
                target = 'ナナヲアカリ (Nanawoakari) ~'
            elif any(k in lower for k in ['七海うらら', 'nanami urara', 'kiss and cry']):
                target = '七海うらら (Nanami Urara) ~'
            elif any(k in lower for k in ['小倉唯', 'ogura yui', 'bloomy']):
                target = '小倉唯 (Yui Ogura) ~'
            elif any(k in lower for k in ['小玉ひかり', 'kodama hikari', 'ヒロイン症候群']):
                target = '小玉ひかり (Hikari Kodama) ~'
            elif any(k in lower for k in ['田中有紀', 'tanaka yuki', 'crier']):
                target = '田中有紀 (Yuki Tanaka) ~'
            elif any(k in lower for k in ['青山なぎさ', 'aoyama nagisa', '解放']):
                target = '青山なぎさ (Nagisa Aoyama) ~'
            elif any(k in lower for k in ['楠木ともり', 'kusunoki tomori']):
                target = '楠木ともり ~'
            elif any(k in lower for k in ['鈴木愛奈', 'suzuki aina', 'ほんのスパークル']):
                target = '鈴木愛奈 ~'
            elif any(k in lower for k in ['22／7', 'yesとnoの間に']):
                target = '22／7 ~'
            elif any(k in lower for k in ['cö shu nie', 'co shu nie', '7 deadly guilt']):
                target = 'Cö Shu Nie ~'
            elif any(k in lower for k in ['hanon×kotoha', 'hanon']):
                target = 'Hanon×Kotoha ~'
            elif any(k in lower for k in ['honeyworks']):
                target = 'HoneyWorks ~'
            elif any(k in lower for k in ['risa yuzuki', '柚木梨沙']):
                target = '柚木梨沙 (Risa Yuzuki) ~'
            elif any(k in lower for k in ['feryquitous']):
                target = 'Feryquitous ~'
            elif any(k in lower for k in ['szno']):
                target = 'SZNO ~'
            elif any(k in lower for k in ['tuki', '15']):
                target = 'Tuki ~'
            elif any(k in lower for k in ['alia']):
                target = 'AliA~'
            elif any(k in lower for k in ['jelee']):
                target = 'JELEE ~'
                
            if target:
                plan['J-Pop'].append((name, target))

    # =========================================================================
    # 5. VOCALOID
    # =========================================================================
    vocaloid_dir = MUSIC_ROOT / 'Vocaloid'
    if vocaloid_dir.exists():
        for d in sorted(vocaloid_dir.iterdir()):
            if not d.is_dir() or d.name.endswith('~'):
                continue
            name = d.name
            lower = name.lower()
            target = None
            if any(k in lower for k in ['deco*27', 'deco∗27', 'deco_27', 'テレパシ', 'サッドガール', 'ラビットホール']):
                target = 'DECO_27 ~'
            elif any(k in lower for k in ['tuyu', 'ツユ']):
                target = 'ツユ (TUYU) ~'
            elif any(k in lower for k in ['pinocchio', 'ピノキオピー']):
                target = 'ピノキオピー (PinocchioP) ~'
            elif any(k in lower for k in ['maisondes']):
                target = 'MAISONdes ~'
            elif any(k in lower for k in ['sekai', 'enigma']):
                target = 'Sekai ~'
                
            if target:
                plan['Vocaloid'].append((name, target))

    return plan

if __name__ == '__main__':
    p = build_plan()
    print("="*60)
    print("GROUPING SIMULATION RESULTS")
    print("="*60)
    for cat in ['Doujinshi', 'Vtuber', 'Anime', 'J-Pop', 'Vocaloid']:
        items = p[cat]
        print(f"\n[{cat.upper()}] Groupable Loose Albums: {len(items)}")
        for src, dst in items:
            print(f"  '{src}'\n    -> '{cat}/{dst}'")
