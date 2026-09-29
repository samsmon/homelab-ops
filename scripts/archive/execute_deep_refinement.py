#!/usr/bin/env python3
import os
import shutil
import re

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

def safe_move(src, dst):
    """Safely moves a file or merges a directory from src to dst."""
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
            s_item = os.path.join(src, item)
            d_item = os.path.join(dst, item)
            safe_move(s_item, d_item)
        if os.path.exists(src) and not os.listdir(src):
            os.rmdir(src)

def execute_refinement(dry_run=True):
    print(f"=== DEEP REFINEMENT (DRY RUN = {dry_run}) ===")
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

    # -------------------------------------------------------------
    # 1. PURGE 0-BYTE FILES & RESIDUAL ARCHIVES
    # -------------------------------------------------------------
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            fp = os.path.join(root, f)
            if f.lower() in ('lzc2059.zip', 'lacm14781.zip', 'felt032_start_specialcontents.zip'):
                plan_delete(fp, "Residual ZIP archive")
            elif os.path.getsize(fp) == 0:
                plan_delete(fp, "0-byte empty file")

    # -------------------------------------------------------------
    # 2. RELOCATE GAMES FROM ANIME/ TO GAME/
    # -------------------------------------------------------------
    # Princess Connect
    priconne_src = os.path.join(BASE_DIR, "Anime", "Princess Connect! Re Dive (プリンセスコネクト！Re Dive) ~")
    priconne_dst = os.path.join(BASE_DIR, "Game", "Princess Connect! Re Dive (プリンセスコネクト！Re Dive) ~")
    if os.path.exists(priconne_src):
        plan_move(priconne_src, priconne_dst, "Move Priconne from Anime to Game")

    # Kancolle
    kancolle_src = os.path.join(BASE_DIR, "Anime", "Kancolle (艦隊これくしょん -艦これ-) ~")
    kancolle_dst = os.path.join(BASE_DIR, "Game", "Kancolle (艦隊これくしょん -艦これ-) ~")
    if os.path.exists(kancolle_src):
        plan_move(kancolle_src, kancolle_dst, "Move Kancolle from Anime to Game")

    # -------------------------------------------------------------
    # 3. UN-NEST 43 DUPLICATE NESTED FOLDERS
    # -------------------------------------------------------------
    # 3a. Vivy
    vivy_nested = os.path.join(BASE_DIR, "Anime", "Vivy -Fluorite Eye's Song- ~", "Vivy -Fluorite Eye's Song-")
    vivy_root = os.path.join(BASE_DIR, "Anime", "Vivy -Fluorite Eye's Song- ~")
    if os.path.exists(vivy_nested):
        for alb in os.listdir(vivy_nested):
            plan_move(os.path.join(vivy_nested, alb), os.path.join(vivy_root, alb), "Un-nest Vivy albums")
        plan_delete(vivy_nested, "Remove empty Vivy container")

    # 3b. TOHO BOSSA NOVA
    toho_nested = os.path.join(BASE_DIR, "Doujinshi", "TOHO BOSSA NOVA ~", "TOHO BOSSA NOVA")
    toho_root = os.path.join(BASE_DIR, "Doujinshi", "TOHO BOSSA NOVA ~")
    if os.path.exists(toho_nested):
        for alb in os.listdir(toho_nested):
            plan_move(os.path.join(toho_nested, alb), os.path.join(toho_root, alb), "Un-nest TOHO BOSSA NOVA albums")
        plan_delete(toho_nested, "Remove empty TOHO BOSSA NOVA container")

    # 3c. Room97
    room_nested = os.path.join(BASE_DIR, "Doujinshi", "Room97 ~", "Room97")
    room_root = os.path.join(BASE_DIR, "Doujinshi", "Room97 ~")
    if os.path.exists(room_nested):
        for alb in os.listdir(room_nested):
            plan_move(os.path.join(room_nested, alb), os.path.join(room_root, alb), "Un-nest Room97 albums")
        plan_delete(room_nested, "Remove empty Room97 container")

    # 3d. DECO_27
    deco_nested = os.path.join(BASE_DIR, "Vocaloid", "DECO_27 ~", "DECO_27")
    deco_root = os.path.join(BASE_DIR, "Vocaloid", "DECO_27 ~")
    if os.path.exists(deco_nested):
        for alb in os.listdir(deco_nested):
            plan_move(os.path.join(deco_nested, alb), os.path.join(deco_root, alb), "Un-nest DECO_27 albums")
        plan_delete(deco_nested, "Remove empty DECO_27 container")

    # 3e. maimie
    maimie_nested = os.path.join(BASE_DIR, "J-Pop", "maimie ~", "maimie", "maimie")
    maimie_root = os.path.join(BASE_DIR, "J-Pop", "maimie ~")
    if os.path.exists(maimie_nested):
        for alb in os.listdir(maimie_nested):
            clean_alb = re.sub(r'\s*\{.*?\}', '', alb).strip()
            plan_move(os.path.join(maimie_nested, alb), os.path.join(maimie_root, clean_alb), "Un-nest maimie albums")
        plan_delete(os.path.join(BASE_DIR, "J-Pop", "maimie ~", "maimie"), "Remove maimie nested container")

    # 3f. MAISONdes
    maisondes_nested = os.path.join(BASE_DIR, "J-Pop", "MAISONdes ~", "MAISONdes")
    maisondes_root = os.path.join(BASE_DIR, "J-Pop", "MAISONdes ~")
    if os.path.exists(maisondes_nested):
        for alb in os.listdir(maisondes_nested):
            if os.path.isdir(os.path.join(maisondes_nested, alb)):
                if alb == "MAISONdes":
                    # inner MAISONdes
                    inner = os.path.join(maisondes_nested, alb)
                    for f in os.listdir(inner):
                        plan_move(os.path.join(inner, f), os.path.join(maisondes_root, "いつのまに", f), "Un-nest MAISONdes single")
                else:
                    plan_move(os.path.join(maisondes_nested, alb), os.path.join(maisondes_root, alb), "Un-nest MAISONdes album")
        plan_delete(maisondes_nested, "Remove MAISONdes container")

    # 3g. Eufolie
    eufolie_nested = os.path.join(BASE_DIR, "Doujinshi", "Eufolie ~", "Eufolie", "Eufolie")
    eufolie_root = os.path.join(BASE_DIR, "Doujinshi", "Eufolie ~", "Eufolie")
    if os.path.exists(eufolie_nested):
        plan_move(eufolie_nested, eufolie_root, "Un-nest Eufolie album")
        plan_delete(os.path.join(BASE_DIR, "Doujinshi", "Eufolie ~", "Eufolie"), "Clean Eufolie")

    # 3h. Scan and un-nest any remaining identical Album/Album folders
    for cat in ["Anime", "Doujinshi", "Game", "Global", "J-Pop", "Vocaloid", "Vtuber"]:
        cat_p = os.path.join(BASE_DIR, cat)
        if not os.path.exists(cat_p):
            continue
        for artist in os.listdir(cat_p):
            artist_p = os.path.join(cat_p, artist)
            if not os.path.isdir(artist_p):
                continue
            for item in os.listdir(artist_p):
                item_p = os.path.join(artist_p, item)
                if not os.path.isdir(item_p):
                    continue
                # Check if item contains an inner folder with the same name
                subdirs = [d for d in os.listdir(item_p) if os.path.isdir(os.path.join(item_p, d))]
                for sd in subdirs:
                    clean_sd = re.sub(r'[\s\~\(\)\[\]]+', '', sd).lower()
                    clean_item = re.sub(r'[\s\~\(\)\[\]]+', '', item).lower()
                    if clean_sd and clean_sd == clean_item:
                        nested_p = os.path.join(item_p, sd)
                        # Check if audio is inside nested_p
                        audio_in_nested = [f for f in os.listdir(nested_p) if f.endswith(('.flac', '.mp3', '.m4a', '.wav'))]
                        if audio_in_nested:
                            for f in os.listdir(nested_p):
                                plan_move(os.path.join(nested_p, f), os.path.join(item_p, f), f"Un-nest audio from {sd}")
                            plan_delete(nested_p, f"Remove redundant inner folder {sd}")

    # -------------------------------------------------------------
    # 4. DISMANTLE ANIME/TV ANIME (TVアニメ) ~ (45 ITEMS)
    # -------------------------------------------------------------
    tv_dir = os.path.join(BASE_DIR, "Anime", "Tv Anime (TVアニメ) ~")
    if os.path.exists(tv_dir):
        # 1. Re:Zero
        rezero = os.path.join(tv_dir, "TVアニメ 「Re：ゼロから始める異世界生活」 キャラクターソングアルバム")
        if os.path.exists(rezero):
            plan_move(rezero, os.path.join(BASE_DIR, "Anime", "Re Zero (Re：ゼロから始める異世界生活) ~", "キャラクターソングアルバム"), "Move Re:Zero character songs")

        # 2. Higuchi Kaede (Baddest)
        baddest = os.path.join(tv_dir, "TVアニメ100万の命の上に俺は立っている 2nd Season」OPテーマBaddest」／樋口楓")
        if os.path.exists(baddest):
            plan_move(baddest, os.path.join(BASE_DIR, "Vtuber", "Nijisanji (にじさんじ) ~", "Higuchi Kaede (樋口楓) ~", "Baddest"), "Move Higuchi Kaede to Nijisanji")

        # 3. 2.5 Jigen no Ririsa
        ririsa1 = os.path.join(tv_dir, "TVアニメ2.5次元の誘惑」EDテーマWatch Me」／天乃リリサ(CV.前田佳織里)、橘美花莉(CV.鬼頭明里)")
        ririsa2 = os.path.join(tv_dir, "Watch Me")
        ririsa_dst = os.path.join(BASE_DIR, "Anime", "2.5 Jigen no Ririsa (2.5次元の誘惑) ~")
        if os.path.exists(ririsa1):
            plan_move(ririsa1, os.path.join(ririsa_dst, "Watch Me"), "Move 2.5 Jigen ED")
        if os.path.exists(ririsa2):
            plan_move(ririsa2, os.path.join(ririsa_dst, "Watch Me (Digital Single)"), "Move 2.5 Jigen Watch Me")

        # 4. NieR Automata
        nier = os.path.join(tv_dir, "TVアニメ「NieR：Automata Ver1.1a」ED2テーマ「灰ト祈リ」／GEMS COMPANY")
        if os.path.exists(nier):
            plan_move(nier, os.path.join(BASE_DIR, "Anime", "NieR Automata (ニーア オートマタ) ~", "灰ト祈リ"), "Move NieR ED2")

        # 5. Ayakashi Triangle
        aya = os.path.join(tv_dir, "TVアニメ「あやかしトライアングル」EDテーマ「厭わない」／MIMiNARI feat.富田美憂&市ノ瀬加那")
        if os.path.exists(aya):
            plan_move(aya, os.path.join(BASE_DIR, "Anime", "Ayakashi Triangle (あやかしトライアングル) ~", "厭わない"), "Move Ayakashi Triangle ED")

        # 6. Arknights
        for ark_item in [
            "TVアニメ「アークナイツ 黎明前奏」EDテーマ「BE ME」／Doul",
            "TVアニメ「アークナイツ 黎明前奏」OPテーマ「Alive」／ReoNa",
            "TVアニメ『アークナイツ【冬隠帰路／PERISH IN FROST】』ED「R.I.P.(Special Edition)」ReoNa"
        ]:
            src = os.path.join(tv_dir, ark_item)
            clean_title = re.search(r'「(.*?)」', ark_item)
            title = clean_title.group(1) if clean_title else ark_item
            if os.path.exists(src):
                plan_move(src, os.path.join(BASE_DIR, "Game", "Arknights ~", title), f"Move Arknights: {title}")

        # 7. Utahime Dream
        for u_item in [
            "TVアニメ「俺は全てを【パリイ】する～逆勘違いの世界最強は冒険者になりたい～」OPテーマ「AMBITION」／桜木舞華 【ウタヒメドリーム】 (CV.鈴木杏奈)",
            "TVアニメ俺は全てを【パリイ】する～逆勘違いの世界最強は冒険者になりたい～」EDテーマノーギフテッド」／ウタヒメドリーム オールスターズ",
            "TVアニメ俺は全てを【パリイ】する～逆勘違いの世界最強は冒険者になりたい～」OPテーマAMBITION」／桜木舞華 【ウタヒメドリーム】 (CV.鈴木杏奈)"
        ]:
            src = os.path.join(tv_dir, u_item)
            if "AMBITION" in u_item:
                dst = os.path.join(BASE_DIR, "Anime", "Utahime Dream (ウタヒメドリーム) ~", "AMBITION")
            else:
                dst = os.path.join(BASE_DIR, "Anime", "Utahime Dream (ウタヒメドリーム) ~", "ノーギフテッド")
            if os.path.exists(src):
                plan_move(src, dst, "Move Utahime Dream single")

        # 8. Senpai wa Otokonoko
        for s_item in [
            "TVアニメ「先輩はおとこのこ」EDテーマ「あれが恋だったのかな」／くじら feat.にしな",
            "TVアニメ「先輩はおとこのこ」OPテーマ「我がまま」／くじら"
        ]:
            src = os.path.join(tv_dir, s_item)
            clean_title = re.search(r'「(.*?)」', s_item)
            title = clean_title.group(1) if clean_title else s_item
            if os.path.exists(src):
                plan_move(src, os.path.join(BASE_DIR, "Anime", "Senpai wa Otokonoko (先輩はおとこのこ) ~", title), f"Move Senpai wa Otokonoko: {title}")

        # 9. Spice and Wolf
        for sw_item in [
            "TVアニメ「狼と香辛料 MERCHANT MEETS THE WISE WOLF」OP2テーマ「Sign」／Aimer",
            "TVアニメ狼と香辛料 MERCHANT MEETS THE WISE WOLF」OP2テーマSign」／Aimer"
        ]:
            src = os.path.join(tv_dir, sw_item)
            if os.path.exists(src):
                plan_move(src, os.path.join(BASE_DIR, "Anime", "Spice and Wolf ~", "Sign"), "Move Spice and Wolf OP2")

        # 10. Isekai Yururi Kikou
        yururi = os.path.join(tv_dir, "TVアニメ「異世界ゆるり紀行 ～子育てしながら冒険者します～」EDテーマ「MAKUAKE」／ゴホウビ")
        if os.path.exists(yururi):
            plan_move(yururi, os.path.join(BASE_DIR, "Anime", "Isekai Yururi Kikou (異世界ゆるり紀行) ~", "MAKUAKE"), "Move Isekai Yururi ED")

        # 11. Giji Harem
        giji = os.path.join(tv_dir, "TVアニメ「疑似ハーレム」OPテーマ「ブラウス」／ゴホウビ")
        if os.path.exists(giji):
            plan_move(giji, os.path.join(BASE_DIR, "Anime", "Giji Harem (疑似ハーレム) ~", "ブラウス"), "Move Giji Harem OP")

        # 12. Narenare
        for n_item in [
            "TVアニメ「菜なれ花なれ」挿入歌「Fever Festa Fever!」／PoMPoMs",
            "TVアニメ「菜なれ花なれ」挿入歌「YOU for YOU」／PoMPoMs",
            "TVアニメ菜なれ花なれ」挿入歌スロウスターター」／小父内涼葉(CV.中島由貴)、谷崎詩音(CV.佳原萌枝)"
        ]:
            src = os.path.join(tv_dir, n_item)
            clean_title = re.search(r'[「](.*?)[」]', n_item)
            title = clean_title.group(1) if clean_title else n_item
            if os.path.exists(src):
                plan_move(src, os.path.join(BASE_DIR, "Anime", "Narenare (菜なれ花なれ) ~", title), f"Move Narenare: {title}")

        # 13. Makeine
        for m_item in [
            "TVアニメ「負けヒロインが多すぎる！」OPテーマ「つよがるガール」／ぼっちぼろまる feat.もっさ",
            "TVアニメ『負けヒロインが多すぎる！』OP主題歌つよがるガール (feat.もっさ)」／ぼっちぼろまる",
            "TVアニメ負けヒロインが多すぎる！」EDテーマLOVE 2000」／八奈見杏菜(CV.遠野ひかる)",
            "TVアニメ負けヒロインが多すぎる！」OPテーマつよがるガール」／ぼっちぼろまる feat.もっさ"
        ]:
            src = os.path.join(tv_dir, m_item)
            clean_title = re.search(r'[「『](.*?)[」』]', m_item)
            title = clean_title.group(1) if clean_title else m_item
            if "つよがるガール" in m_item:
                title = "つよがるガール"
            elif "LOVE 2000" in m_item:
                title = "LOVE 2000"
            if os.path.exists(src):
                plan_move(src, os.path.join(BASE_DIR, "Anime", "Makeine (負けヒロインが多すぎる！) ~", title), f"Move Makeine: {title}")

        # 14. Maou Gakuin
        maou = os.path.join(tv_dir, "TVアニメ「魔王学院の不適合者 Ⅱ ～史上最強の魔王の始祖、転生して子孫たちの学校へ通う～」ED2テーマ「シンゲツ」／楠木ともり")
        if os.path.exists(maou):
            plan_move(maou, os.path.join(BASE_DIR, "Anime", "Maou Gakuin no Futekigousha (魔王学院の不適合者) ~", "シンゲツ"), "Move Maou Gakuin ED2")

        # 15. Onimai
        onimai1 = os.path.join(tv_dir, "TVアニメ『お兄ちゃんはおしまい！』EDテーマ「ひめごと＊クライシスターズ」ONIMAI SISTERS")
        onimai2 = os.path.join(tv_dir, "TVアニメ『お兄ちゃんはおしまい！』OP&ED「アイデン貞貞メルトダウン feat.P丸様。」「ひめごと＊クライシスターズ」")
        if os.path.exists(onimai1):
            plan_move(onimai1, os.path.join(BASE_DIR, "Anime", "Onimai (お兄ちゃんはおしまい！) ~", "ひめごと＊クライシスターズ"), "Move Onimai ED")
        if os.path.exists(onimai2):
            plan_delete(onimai2, "Remove empty Onimai folder")

        # 16. Yuru Camp
        for y_item in [
            "TVアニメ『ゆるキャン△ SEASON2』EDはるのとなり」／佐々木恵梨",
            "TVアニメゆるキャン△ SEASON2」EDテーマはるのとなり」／佐々木恵梨"
        ]:
            src = os.path.join(tv_dir, y_item)
            if os.path.exists(src):
                plan_move(src, os.path.join(BASE_DIR, "Anime", "Yuru Camp (ゆるキャン△) ~", "はるのとなり"), "Move Yuru Camp ED")

        # 17. Nige Jouzu no Wakagimi
        for nj_item in [
            "TVアニメ『逃げ上手の若君』OP & ED鎌倉STYLE」プランA」",
            "TVアニメ逃げ上手の若君」EDテーマ鎌倉STYLE」／ぼっちぼろまる"
        ]:
            src = os.path.join(tv_dir, nj_item)
            clean_title = "プランA ／ 鎌倉STYLE" if "プランA" in nj_item else "鎌倉STYLE"
            if os.path.exists(src):
                plan_move(src, os.path.join(BASE_DIR, "Anime", "Nige Jouzu no Wakagimi (逃げ上手の若君) ~", clean_title), "Move Nige Jouzu songs")

        # 18. Kono Sekai wa Fukanzensugiru
        fukanzen = os.path.join(tv_dir, "TVアニメこの世界は不完全すぎる」OPテーマNo Complete」／Liyuu")
        if os.path.exists(fukanzen):
            plan_move(fukanzen, os.path.join(BASE_DIR, "Anime", "Kono Sekai wa Fukanzensugiru (この世界は不完全すぎる) ~", "No Complete"), "Move Kono Sekai OP")

        # 19. Girls Band Cry CD 3
        gbc3 = os.path.join(tv_dir, "TVアニメガールズバンドクライ」トゲナシトゲアリ オリジナルソングCD 3渇く、憂う」")
        if os.path.exists(gbc3):
            plan_move(gbc3, os.path.join(BASE_DIR, "Anime", "Girls Band Cry (ガールズバンドクライ) ~", "TVアニメ「ガールズバンドクライ」トゲナシトゲアリ オリジナルソングCD 3「渇く、憂う」"), "Rescue Girls Band Cry CD 3")

        # 20. Megami no Cafe Terrace
        megami = os.path.join(tv_dir, "TVアニメ女神のカフェテラス 2nd Season」OPテーマチャージ！」／小玉ひかり")
        if os.path.exists(megami):
            plan_move(megami, os.path.join(BASE_DIR, "Anime", "Megami no Cafe Terrace (女神のカフェテラス) ~", "チャージ！"), "Move Megami no Cafe Terrace OP")

        # 21. Wistoria (Tsue to Tsurugi no Wistoria)
        wistoria = os.path.join(tv_dir, "TVアニメ杖と剣のウィストリア」EDテーマフローズン」／TRUE")
        if os.path.exists(wistoria):
            plan_move(wistoria, os.path.join(BASE_DIR, "Anime", "Tsue to Tsurugi no Wistoria (杖と剣のウィストリア) ~", "フローズン"), "Move Wistoria ED")

        # 22. Tate no Yuusha no Nariagari
        tate = os.path.join(tv_dir, "TVアニメ盾の勇者の成り上がり Season 2」EDテーマゆずれない」／藤川千愛")
        if os.path.exists(tate):
            plan_move(tate, os.path.join(BASE_DIR, "Anime", "Tate no Yuusha no Nariagari (盾の勇者の成り上がり) ~", "ゆずれない"), "Move Shield Hero ED")

        # 23. Mayonaka Punch
        mayonaka = os.path.join(tv_dir, "TVアニメ真夜中ぱんチ」第8話EDテーマナイトダイバー」／りぶ(CV.ファイルーズあい)、苺子(CV.伊藤ゆいな)、譜風(CV.羊宮妃那)、十景(CV.上田瞳)")
        if os.path.exists(mayonaka):
            plan_move(mayonaka, os.path.join(BASE_DIR, "Anime", "Mayonaka Punch (真夜中ぱんチ) ~", "ナイトダイバー"), "Move Mayonaka Punch ED")

        # 24. Tensura
        tensura = os.path.join(tv_dir, "TVアニメ転生したらスライムだった件 3rd Season」OP2テーマレナセールセレナーデ」／ももいろクローバーZ")
        if os.path.exists(tensura):
            plan_move(tensura, os.path.join(BASE_DIR, "Anime", "Tensura (転生したらスライムだった件) ~", "レナセールセレナーデ"), "Move Tensura OP2")

        # 25. Just Because! (behind)
        behind = os.path.join(tv_dir, "behind")
        if os.path.exists(behind):
            plan_move(behind, os.path.join(BASE_DIR, "Anime", "Just Because! ~", "behind"), "Move Just Because! ED")

        # 26. Mato Seihei no Slave
        ms1 = os.path.join(tv_dir, "「魔都精兵のスレイブ」キャラクターソングミニアルバム 01 「嵐を駆けよ波乱の鬣よ」")
        ms2 = os.path.join(tv_dir, "「魔都精兵のスレイブ」キャラクターソングミニアルバム 02 「六番組COLLECTION」")
        ms_dst = os.path.join(BASE_DIR, "Anime", "Mato Seihei no Slave (魔都精兵のスレイブ) ~")
        if os.path.exists(ms1):
            plan_move(ms1, os.path.join(ms_dst, "キャラクターソングミニアルバム 01「嵐を駆けよ波乱の鬣よ」"), "Move Mato Seihei Album 1")
        if os.path.exists(ms2):
            plan_move(ms2, os.path.join(ms_dst, "キャラクターソングミニアルバム 02「六番組COLLECTION」"), "Move Mato Seihei Album 2")

        # 27. Azur Lane wavy flow
        wavy = os.path.join(tv_dir, "ゲーム『アズールレーン』5周年記念テーマソングwavy flow」／Aimer")
        if os.path.exists(wavy):
            plan_move(wavy, os.path.join(BASE_DIR, "Game", "Azur Lane (アズールレーン) ~", "wavy flow"), "Move Azur Lane 5th Anniv")

        # 28. Empty Aobuta folders
        for ab in ["青春ブタ野郎はおでかけシスターの夢を見ない", "青春ブタ野郎はランドセルガールの夢を見ない"]:
            ab_p = os.path.join(tv_dir, ab)
            if os.path.exists(ab_p):
                plan_delete(ab_p, f"Delete empty folder: {ab}")

        # 29. TUYU album flattening & tag cleanup
        tuyu_dir = os.path.join(BASE_DIR, "J-Pop", "TUYU (ツユ) ~")
        if os.path.exists(tuyu_dir):
            for sub in ["Bonus CDs", "Albums"]:
                sub_p = os.path.join(tuyu_dir, sub)
                if os.path.exists(sub_p):
                    for alb in os.listdir(sub_p):
                        clean_alb = re.sub(r'\s*\(.*?\)', '', alb)
                        clean_alb = re.sub(r'\s*\[.*?\]', '', clean_alb)
                        clean_alb = re.sub(r'\s*\{.*?\}', '', clean_alb).strip()
                        plan_move(os.path.join(sub_p, alb), os.path.join(tuyu_dir, clean_alb), f"Flatten TUYU album {clean_alb}")
                    plan_delete(sub_p, f"Delete empty {sub} folder")

        # 30. nonoc, Yuno Sakura, Shishiro Botan, Shirogane Noel tag cleanup
        nonoc_p = os.path.join(BASE_DIR, "J-Pop", "nonoc ~", "Believe in you (2021) {ZMCZ-14612}")
        if os.path.exists(nonoc_p):
            plan_move(nonoc_p, os.path.join(BASE_DIR, "J-Pop", "nonoc ~", "Believe in you"), "Clean nonoc album name")

        yuno_p = os.path.join(BASE_DIR, "J-Pop", "Yuno Sakura (咲良ゆの) ~", "宝石の降る夜 [WEB-FLAC")
        if os.path.exists(yuno_p):
            plan_move(yuno_p, os.path.join(BASE_DIR, "J-Pop", "Yuno Sakura (咲良ゆの) ~", "宝石の降る夜"), "Clean Yuno Sakura album name")

        botan_p = os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~", "Shishiro Botan (獅白ぼたん) ~", "Lights (2024) {HOLOEC-035}")
        if os.path.exists(botan_p):
            plan_move(botan_p, os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~", "Shishiro Botan (獅白ぼたん) ~", "Lights"), "Clean Botan album name")

        noel_p = os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~", "Shirogane Noel (白銀ノエル) ~", "のえさんぽ (2023) {HOLOEC-026}")
        if os.path.exists(noel_p):
            plan_move(noel_p, os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~", "Shirogane Noel (白銀ノエル) ~", "のえさんぽ"), "Clean Noel album name")

        # 31. Rename New Game ~ -> NEW GAME! (ニューゲーム!) ~
        newgame_src = os.path.join(BASE_DIR, "Anime", "New Game ~")
        newgame_dst = os.path.join(BASE_DIR, "Anime", "NEW GAME! (ニューゲーム!) ~")
        if os.path.exists(newgame_src):
            plan_move(newgame_src, newgame_dst, "Normalize New Game umbrella name")

        # If tv_dir is now empty, delete it
        actions.append(('RMDIR', tv_dir, '', 'Dissolve legacy Tv Anime container'))
        if not dry_run and os.path.exists(tv_dir) and not os.listdir(tv_dir):
            os.rmdir(tv_dir)

    print(f"Total planned actions: {len(actions)}")
    for act, src, dst, desc in actions[:30]:
        print(f"  [{act}] {os.path.basename(src)} -> {os.path.basename(dst) if dst else ''} ({desc})")
    if len(actions) > 30:
        print(f"  ... and {len(actions) - 30} more actions.")

if __name__ == '__main__':
    execute_refinement(dry_run=False)

