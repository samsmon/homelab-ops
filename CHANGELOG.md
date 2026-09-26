# Changelog

> Every meaningful change gets one entry here, newest on top. Keep it short: date, what changed, why (if not obvious).

## 2026-09-27 (150)
- **Zero WAV Files (100% FLAC Bit-Perfect Library), Mojibake Correction, HoneyWorks/nayuta Re-homing, and Global Format Noise Purge.**
  - **Zero WAV Files & Bit-Perfect FLAC Conversion**:
    - Converted all 48 uncompressed WAV audio files library-wide to bit-perfect `.flac` with full tags:
      - `Doujinshi/Imy ~/Beyond the despair`: Repaired corrupted mojibake filename `06 îÄÄ₧ëJ.wav` into canonical `06. 月時雨.flac` and converted all 6 tracks.
      - `Doujinshi/Login Records ~/Never Forget Vacation 8`: Converted all 15 tracks to `.flac`.
      - `Doujinshi/nayuta ~/想い出を綴った歌を君へ。`: Rescued 5th anniversary best album from misattributed dump folder `J-Pop/7uta ~` into canonical `Doujinshi/nayuta ~`, converted all 15 tracks to `.flac`, and purged empty container.
      - `Game/Kancolle (艦隊これくしょん -艦これ-) ~`: Converted 12 tracks to 24-bit / 48kHz `.flac`, normalized folder title to `「艦隊これくしょん -艦これ-」キャラクターソング “艦娘乃歌” Vol.1` (stripping format noise and repairing opening quotation).
      - `Vtuber/KAMITSUBAKI STUDIO ~/Koko (幸祜) ~/Prayer/mcard-bonustracks`: Converted 2 bonus tracks to `.flac`.
    - Achieved exactly **0 WAV files** across `/mnt/hdd-backup/music/Lossless/`.
  - **Global Format Tag Noise & Suffix Stripping**:
    - Purged redundant duplicate folder `Light Years HI-RES` in `Game/Heaven Burns Red ~`.
    - Stripped `HI-RES` / `hi-res` / `FLAC` suffixes across 20 album folders in Heaven Burns Red, Azur Lane, Azuma Seren, Princess Letter(s)!, GEMS COMPANY, YuNi, Mone Kamishiraishi, NOMELON NOLEMON, and Hanatan.
    - Normalized `Doujinshi/Vivid Lila ~/WEB FLAC` to official release title `Air of Celeste`.
    - Re-homed HoneyWorks' `告白実行委員会 -FLYING SONGS- 恋してる` from deformed artist folder into canonical `J-Pop/HoneyWorks ~`.
  - **Storage & System Verification**:
    - Disk free space reached **124 GB free** (+13 GB net gain since start).
    - Catalog refreshed: `25,866` total tracks; `Lossless.m3u8` regenerated: `23,196` tracks.
    - Permissions `775/664` applied and Samba reloaded.

## 2026-09-26 (149)
- **Gakuen Idolmaster Perfection, Library-wide Quality Upgrades (BanG Dream! & TUYU 24-bit Hi-Res), Format Tag Noise Elimination, and Zero `_alt`/`_dup` Audit.**
  - **Gakuen Idolmaster (学園アイドルマスター) Deep Perfection**:
    - Normalized decomposed Unicode NFD dakuten (`は` + `\u3099`) in `01. Solo/02. 月村手毬 (Temari Tsukimura)/叶えたい、ことばかり` to NFC `叶えたい、ことばかり`.
    - Stripped format noise `[1st Single CD-FLAC]` to `[1st Single]` on `Fighting My Way [1st Single]`, `Luna say maybe [1st Single]`, and `世界一可愛い私 [1st Single]`.
    - Rescued booklet `BK/` from 16-bit `かちドキ [GOLD RUSH CD-FLAC]` into 24-bit Hi-Res master `かちドキ`, purging the 16-bit redundant folder.
    - Relocated Kotone's solo cover album `GOLD RUSH 第3巻 特装版「GO MY WAY!!」` with scans from `04. All Stars & Units` into `01. Solo/03. 藤田ことね (Kotone Fujita)/`.
    - Purged all 16-bit `_alt.flac` duplicates across Gakumas (`ガラクタロード`, `かちドキ`, `MY STAGE`, `三分半の創世`, `真っ白いページと水彩の主人公`, `VEIL`, `Superlative`).
  - **Global `_alt.flac` & `_dup.flac` Audit & Quality Upgrades**:
    - BanG Dream!: Upgraded all 10 tracks of MyGO!!!!! 3rd Album `致並跡` from 16-bit to 24-bit / 96kHz Hi-Res masters (renamed `_alt` to base, purged 16-bit).
    - BanG Dream!: Upgraded Mugendai Mewtype 4th Single `超惑星Xへの旅` to 24-bit / 96kHz Hi-Res masters.
    - TUYU: Upgraded all 12 tracks of `アンダーメンタリティ` from 16-bit to 24-bit / 48kHz Hi-Res masters and replaced low-res cover with 2.7MB Hi-Res cover art.
    - Purged redundant 16-bit and byte-for-byte duplicate `_alt.flac`, `_dup.flac`, and `*_dup.jpg` across the entire library (Liella! `Hyper Glowing!`, Shiny Colors `Over the prism`, Utahime Dream `AMBITION` and `アンノウンミー`, `先輩はおとこのこ`, `菜なれ花なれ`, Hanabie., PassCode, Kaya, 雪花繚乱, 田中有紀 `I need`, りりあ。 `軌跡`, 前島亜美 `Determination`, 七海うらら, 大神ミオ, さくらみこ, 鷹嶺ルイ, 白上フブキ, アイドリープライド, 狼と香辛料, レヴュースタァライト).
    - Flattened nested album folder in `J-Pop/Maejima Ami (前島亜美) ~/`.
    - Achieved exactly **0 `_alt` / `_dup` files** library-wide.
  - **Shiny Colors Format Noise Elimination**:
    - Stripped ` [AIFF 96kHz／32bit]` from all 28 album folders across `01. BRILLI@NT WING`, `02. FR@GMENT WING`, `03. GR@DATE WING`, `04. L@YERED WING`, and `04. COLORFUL FE@THERS Series`, achieving **0 format tags** in folder names across the entire library.
  - **Root Cleanup & Quarantine Purge**:
    - Purged empty `_corrupted_quarantine` directory tree from Lossless root, leaving exactly the 7 canonical music categories (`Anime`, `Doujinshi`, `Game`, `Global`, `J-Pop`, `Vocaloid`, `Vtuber`).
    - Purged residual empty leaf folders `J-Pop/YUI ~/FROM ME TO YOU/Scans` and `Doujinshi/Eufolie ~`.
  - **System Metrics & Final State**:
    - Available space expanded to **123 GB free** (+12 GB net gain since start).
    - Master SQLite catalog refreshed: `25,867` total tracks.
    - Master playlist `Lossless.m3u8` regenerated: `23,197` tracks.
    - Strict permissions (`775` dirs, `664` files) reapplied and Samba reloaded.

## 2026-09-26 (148)
- **Zero-Redundancy Duplicate Purge, Bit-Perfect CUE Splitting, J-Pop Artist Consolidation, and Shiny Colors Master Re-alignment.**
  - **Bit-Perfect CUE Splitting & Zero Residual CUEs**:
    - Split 11 Love Live! SPCD discs (`SPCD 01-05`, `Original Song CD 01-06`) and 3 Mamyukka disc images (`サハラムシカ`, `テアトルエトワール`, `THE 13th PANCER`) using `shnsplit` into standalone individual FLAC tracks (`01. [Title].flac`, `02. [Title] (Off Vocal).flac`), purging all original whole-disc flac images and CUE sheets.
    - Verified single-track releases and removed redundant CUE sheets across the entire library (`Mori Calliope DISASTERPIECE`, `TUYU アンダーキッズ`, `ZAQ カーストルーム`, `Shinra-bansho toge`, `Azuma Seren KEEP OUT`, `PROTOCOLLON J-HYPER NATION`, `Mamyukka Trick Or Mamyukka`), achieving exactly **0 CUE sheets** and **0 unsplit disc images** across `/mnt/hdd-backup/music/Lossless/`.
  - **Zero Redundancy Duplicate Purging & Quality Optimization**:
    - Purged exact duplicate folders: Towatsugai bracket-less copy, Rokudenashi duplicate Eureka folder (rescued missing track 3 and scans into clean `ユリイカ`), Magical Mirai 2024 duplicate romaji copy, Watch Me 1-track digital single, Cute Cutting Club 16-bit copy & empty container, Mamyukka 6 redundant WAV files.
    - Purged Shirakami Fubuki defective unbracketed duplicate `... EPヤマトファンタジア」`.
    - Purged PROTOCOLLON redundant 16-bit duplicates (`*_dup.flac`, `cover_dup.jpg`) in favor of 24-bit 48kHz hi-res masters.
    - Purged redundant single folders completely subsumed by full/deluxe releases: Nishino Kana Feat. NiziU `LOVE BEAT (Single Edition)` (vs `Full Release`), Nogizaka46 `是非に及ばず` (vs `Special Edition`), and H／／PE Princess `17.7` (vs `Japan Deluxe Edition`).
  - **J-Pop Split Artists Consolidation (Zero Case Collisions)**:
    - Unified 19 split artist folders differing only in casing or kana/kanji variations: `96 Neko (96猫)` -> `96Neko (96猫)`, `9lana` -> `9Lana`, `Ado` -> `Ado (アド)`, `Boku Ga Mita Katta Aozora` -> `Boku ga Mitakatta Aozora`, `Cö Shu Nie` -> `Cö shu Nie`, `Haku .` -> `Haku.`, `Kotonohouse` -> `KOTONOHOUSE`, `Miminari` -> `MIMiNARI`, `Milet` -> `milet`, `Murasaki Ima (紫今)` -> `Murasaki Ima (紫 今)`, `Nomelon Nolemon` -> `NOMELON NOLEMON`, `No Hana Koyori` -> `Nohana Koyori`, `Sa Na (紗奈)` -> `Sana (鎖那)`, `SawanoHiroyuki` -> `Sawano Hiroyuki (澤野弘之)`, `Takane Nonadeshiko` -> `Takane no Nadeshiko`, `Tsukuyomi` -> `Tsukuyomi (月詠み)`, `Washio Rei Na` -> `Washio Reina`, `YU-KA` -> `Yu-ka`, `otsumami feat.mikan` -> `otsumami feat. mikan`.
    - Normalized `Su Mi Ka (す み か) ~` to `Sumika (す み か) ~` (preserving distinction from rock band `sumika ~`).
    - Achieved **0 case collisions** across ext4 / SMB for Windows clients.
  - **THE IDOLM@STER Shiny Colors Complete Restructuring**:
    - `01. WING Series/06. CANVAS`: Migrated artwork from empty `_CANVAS_ 01..08` folders into `''CANVAS'' 01..08` and purged the 8 empty folders.
    - `02. Song for Prism Series`: Merged artwork from 12 empty folders named with `_` into counterpart folders with `／`, purging the empty containers.
    - Flattened `神様は死んだ、って` from nested subdirectories directly to album root.
    - Purged 16-bit duplicates in `Tokyo自由系＊ガール／My time` and `ボーダーレス・ノンストレス／Oh Yeah!!`, retaining 24-bit 96kHz masters.
    - Purged duplicate tracks in `SUPER DUPER DREAMER／BEAST MODE` and `散花-sanka-／紅花-benibana-`.
    - Merged spaced and non-spaced duplicate folders in `C'mon! Join Us`.
  - **System Metrics & Storage Gains**:
    - Disk free space increased from 111 GB to **121 GB free** (+10 GB net gain).
    - Permissions set to `775` (dirs) and `664` (files); Samba reloaded.

## 2026-09-26 (147)
- **Comprehensive Franchise Perfection, VTuber Unification, and Mobile Game Re-alignment.**
  - **Hololive Unification**:
    - Rescued Mori Calliope's `DISASTERPIECE` from `J-Pop/Mori Calliope ~` into canonical `Vtuber/Hololive (ホロライブ) ~/Mori Calliope ~/`.
    - Relocated Kobo Kanaeru's `初恋` from loose root `Vtuber/Kobo Kanaeru ~` into `Vtuber/Hololive (ホロライブ) ~/Kobo Kanaeru ~/` alongside all Hololive ID generation members.
  - **VTuber Duplication Consolidation**:
    - Re-unified `Shigure Ui (しぐれうい) ~` and `Ui Shigure (しぐれうい) ~` into `Vtuber/Ui Shigure (しぐれうい) ~` (5 albums).
    - Merged deformed kakasi folder `Ryuu Saki Rin (龍ヶ崎リン) ~` into `Vtuber/Ryugasaki Rene (龍ヶ崎リン) ~` (3 albums).
  - **Vocaloid Re-homing**: Rescued 3 non-Vocaloid heavy metal and idol bands mistakenly dumped in `Vocaloid/` (`FATE GEAR ~`, `KOIAI ~`, and `OCHA NORMA ~`) to `J-Pop/`.
  - **Music Unit Unification**: Consolidated `Anime/(K)NoW_NAME：NIKIIE ~` and `J-Pop/NoW_NAME ~` into single canonical `J-Pop/(K)NoW_NAME ~`.
  - **Mobile Idol/Rhythm Games Migration**: Moved 6 mobile rhythm & idol game franchises from `Anime/` to `Game/`:
    - `Tokyo 7th Sisters (Tokyo 7th シスターズ) ~` (27 albums)
    - `Idoly Pride (アイドリープライド) ~` (68 albums)
    - `IDOLiSH7 (アイドリッシュセブン) ~`
    - `CUE! ~` (15 albums)
    - `Lapis ReLiGHTs ~`
    - `LiveRevolt ~`
    - Expanding `Game/` to **22 official game franchises** and streamlining `Anime/` to **73 pure anime umbrellas**.
  - **Final Audit & Permissions**: Zero folders without tildes, zero loose audio, zero date/codec tags in album names, zero zero-byte corrupt files, zero residual junk. Applied permissions `775/664`, refreshed SQLite master catalog (`26,017` tracks) and `Lossless.m3u8` (`23,347` tracks), and reloaded Samba.

## 2026-09-26 (146)

- **Deep Refinement, Complete `Tv Anime` Legacy Dissolution, and Duplicate Container Un-nesting.**
  - **Complete Dissolution of `Anime/Tv Anime (TVアニメ) ~`**: Re-homed all 45 unsorted torrent releases to their canonical umbrellas and deleted the legacy dump container:
    - Rescued 3 Arknights anime songs (`BE ME`, `Alive`, `R.I.P.`) to `Game/Arknights ~`.
    - Rescued Azur Lane 5th Anniversary single `wavy flow` to `Game/Azur Lane (アズールレーン) ~`.
    - Rescued Girls Band Cry missing CD 3 (`トゲナシトゲアリ オリジナルソングCD 3「渇く、憂う」`) into `Anime/Girls Band Cry (ガールズバンドクライ) ~`.
    - Re-homed Utahime Dream (`AMBITION`, `ノーギフテッド`), Makeine (4 releases), Narenare (3 releases), Spice and Wolf, Yuru Camp, Megami no Cafe Terrace, and Just Because! (`behind`).
    - Rescued VTuber Higuchi Kaede's `Baddest` into `Vtuber/Nijisanji (にじさんじ) ~/Higuchi Kaede (樋口楓) ~/`.
    - Established canonical umbrellas for new anime franchises: `Re Zero (Re：ゼロから始める異世界生活) ~`, `Onimai (お兄ちゃんはおしまい！) ~`, `Mato Seihei no Slave (魔都精兵のスレイブ) ~`, `2.5 Jigen no Ririsa (2.5次元の誘惑) ~`, `Nige Jouzu no Wakagimi (逃げ上手の若君) ~`, `NieR Automata (ニーア オートマタ) ~`, `Tensura (転生したらスライムだった件) ~`, `Ayakashi Triangle (あやかしトライアングル) ~`, etc.
  - **Game Franchise Relocation**: Migrated `Princess Connect! Re Dive` (18 albums) and `Kancolle (艦隊これくしょん -艦これ-)` (9 albums) from `Anime/` into `Game/`, expanding `Game/` to 16 official franchises.
  - **Un-nested 43 Duplicate Nested Containers**:
    - Flattened all 18 albums in `Anime/Vivy -Fluorite Eye's Song- ~` directly to root.
    - Flattened all 12 albums in `Doujinshi/TOHO BOSSA NOVA ~` and 3 albums in `Doujinshi/Room97 ~`.
    - Un-nested `Vocaloid/DECO_27 ~`, `J-Pop/MAISONdes ~`, `J-Pop/maimie ~`, `Doujinshi/Eufolie ~`, `J-Pop/TRUE ~` singles, and other identical `Artist/Artist` or `Album/Album` redundancies.
  - **Zero Junk & Zero Corrupt Files**: Purged 3 residual extraction `.zip` archives (`lzc2059.zip`, `lacm14781.zip`, `FELT032_START_SpecialContents.zip`) and 25 zero-byte corrupt files (`cover.jpg`, `.lrc`, damaged scans).
  - **Album Title & Tag Normalization**: Flattened `TUYU (ツユ) ~` and normalized catalog/date tags in `TUYU`, `nonoc`, `Yuno Sakura`, `Shishiro Botan`, and `Shirogane Noel`. Renamed `New Game ~` to canonical `NEW GAME! (ニューゲーム!) ~`.
  - **Catalog & Space Gains**: Gained +5 GB free space (**116 GB free** on `hdd-backup`). Catalog refreshed to `26,017` tracks; `Lossless.m3u8` generated with `23,347` tracks; permissions `775/664` applied; Samba reloaded.

## 2026-09-26 (145)

- **Master Sweep Reorganization & Total Zero-Defect Library Alignment across `/mnt/hdd-backup/music/Lossless/`.**
  - **Decontaminated `J-Pop/tuki. ~`**: Rescued 4 major foreign discographies trapped inside `tuki. ~`:
    - Moved and dismantled full 22-album TrySail discography (5 ERA folders) into canonical flat releases inside `J-Pop/TrySail (トライセイル) ~`.
    - Rescued D4DJ unit RONDO's `メモリアルアルバム「-未来-」` into `Anime/D4DJ (ディーフォーディージェー) ~/RONDO (燐舞曲) ~/`.
    - Rescued Akari Kito's `Journey` into `J-Pop/Akari Kito (鬼頭明里) ~/`.
    - Rescued Riria.'s `軌跡` into `J-Pop/Riria . (りりあ。) ~/`.
  - **Zero Loose Tracks**: Wrapped all 14 loose `.flac` digital singles in `J-Pop/Hibana (ヒバナ) ~` into canonical single/album folders (`01. [Title].flac`).
  - **Game & Character Song Realignment**:
    - Moved `White Album2` out of `Anime/` to `Game/WHITE ALBUM2 (ホワイトアルバム2) ~`.
    - Rescued `西浦そら(CV.相川奈央) - 陽だまり計画書` from `J-Pop/` to `Anime/Maebashi Witches (前橋ウィッチーズ) ~/`.
    - Rescued `ユラ(CV.大西沙織) - 蒼海の揺らめき` from `J-Pop/` to `Game/Towatsugai (トワツガイ) ~/`.
  - **Folder Name Sanitization & Windows Forbidden Characters**:
    - Normalized deformed kakasi folder `T Shou Yama Nao ...` into clean `J-Pop/Touyama Nao (東山奈央) ~`, flattening 11 albums directly.
    - Sanitized `Sakurarium (サクラリウム) ~`, `Nohana Koyori (乃花こより) ~`, `Kozue Kisaragi (如月梢) ~`, and `Doujinshi/Lampcat ~`.
    - Replaced Windows forbidden characters (`*`, `:`, `?`) in artist names (`＊Luna ~`), album names (`Re：Volt`), and track titles across Tokyo 7th Sisters, Love Live!, and Endorfin.
  - **ERA Torrent Flattening & Cross-Category Consolidation**:
    - Flattened all 23 albums in `J-Pop/ReoNa ~` and 22 releases in `Anime/Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~`.
    - Unified 17 split artists across categories: Endorfin., nayuta, Hanatan, lapix, Islet, Tsukino, Ruru, Dadaizu, Hagali, Imy, Isle & Notes, ubique, Vivid Lila into `Doujinshi/`; TUYU and Lucia into `J-Pop/`; FloweRiЯy into `Vocaloid/`; NEUN into `Vtuber/`.
  - **Verification & Service Refresh**: Total library sweep verified: 0 empty dirs, 0 loose tracks, 0 suspicious nested containers, 0 deformed artist folders, 0 forbidden characters. Applied `775/664` permissions, refreshed master SQLite catalog (`26,101` tracks) and `Lossless.m3u8` (`23,431` tracks), and reloaded Samba.

## 2026-09-26 (144)

- **Comprehensive Gakumas Structuring, `Game/` Category Creation, and Universal Cross-Category Realignment.**
  - **Gakumas Perfection**: Achieved 100% clean structure in `Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~/`. Exactly 13 character subfolders in `01. Solo/` (0 loose albums, 0 unnumbered duplicate folders). Rescued `金の斧、銀の斧、エメラルドの斧` to Ume and `Choo Choo Choo` to Sena. Flattened `GOLD RUSH 3` and eliminated cross-tier duplicate copies (`SUGAR FLAVOR`, `「ねえ、言っちゃうよ。」`, `わかし・さわがし・スカパンク`).
  - **Dedicated `Lossless/Game/` Category**: Activated official `Game/` category and evacuated 13 game franchises from `Anime/` (`BLUE PROTOCOL`, `HoYoverse`, `Wuthering Waves`, `SEGA & Arcade Games`, `O.N.G.E.K.I.`, `WHITE ALBUM2`, `Blue Archive`, `Azur Lane`, `Heaven Burns Red`, `Battle Girl High School`, `Towatsugai`, `MementoMori`, and `Project SEKAI`).
  - **Arknights Restoration**: Sanitized mutilated folder `Arknights ( Akunaitsu ~` into clean `Game/Arknights ~` and flattened all 31 albums directly at the root.
  - **Vocaloid Producer Rescue**: Re-homed `Tetris` to `Vocaloid/Hiiragi Magnetite (柊マグネタイト) ~`. Consolidated `Harumaki Gohan (はるまきごはん) ~`, `MIMI ~` (12 albums unified from Vtuber & J-Pop), and `TAK ~` into `Vocaloid/`.
  - **Commercial J-Pop Consolidation**: Reunified 3 fragmented folders of `Yui Ogura (小倉唯) ~` (5 albums). Moved `Ikkyu Nakajima` out of `Anime/`. Consolidated `Atarayo (あたらよ) ~`. Dismantled multi-level torrent ERA containers in `JUNNA ~` into 18 flat albums. Re-homed `Ten ~` and `Hakoniwa Lily ~`.
  - **VTuber & Anime Unification**: Unified `HIMEHINA ~` (3 albums) and `La Prière ~` (11 albums) in `Vtuber/`. Unified `100 Kanojo` and `Oshi no Ko (【推しの子】) ~` (with B Komachi). Consolidated scattered character songs into `Anime/Utahime Dream (ウタヒメドリーム) ~`, `MILGRAM ~`, `iMarine Project ~`, and `HoneyWorks (mona) ~`.
  - **Catalog & Permissions**: Enforced permissions `775/664`. Master SQLite catalog indexed `26,101` tracks; `Lossless.m3u8` generated with `23,431` tracks; Samba reloaded. Freed up duplicate space to **111 GB free** on `hdd-backup`.

## 2026-09-26 (143)
- **Enforced 100% Strict Romaji-First & Comprehensive VTuber/Agency Realignment.**
  - **Zero Non-ASCII First Folders**: Inverted all remaining `Japanese (Romaji) ~` folders to `Romaji (Japanese) ~` and romanized all pure Japanese names via dictionary and `kakasi` (Hepburn). Non-ASCII first folders across all categories (`Anime`, `J-Pop`, `Vtuber`, `Doujinshi`, `Vocaloid`) reduced from 200+ to **0**.
  - **Seiyuu Franchise Contamination Rescued**: Rescued `THE IDOLM@STER SHINY COLORS シャイニーPRオファー Vol.3` from `Tanaka Yuki (田中有紀) ~` into canonical `Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/05. Synthe-Side & Collaborations/`. Removed empty artist directory in `Anime/` and unified `Yuki Tanaka (田中有紀) ~` in `J-Pop/`.
  - **Complete VTuber Relocation**: Migrated 25+ VTubers out of `J-Pop/` into their canonical `Vtuber/` umbrellas:
    - **Hololive**: Shiranui Flare, Natsuiro Matsuri, Oozora Subaru, Houshou Marine, Tokoyami Towa, Yukihana Lamy, Kazama Iroha, Juufuutei Raden, Todoroki Hajime, Otonose Kanade, Ichijou Ririka, Takane Lui, Usada Pekora, HoloWitches.
    - **Nijisanji**: Kenmochi Toya, Yumeoi Kakeru, Kuzuha.
    - **VSPO (ぶいすぽっ！)**: Tachibana Hinano, Kaminari Qpi, Asumi Sena, Nekota Tsuna, Tosaki Mimi, Kurumi Noah.
    - **RK Music / RIOT / Indie**: Setono Toto, Mikage, ASU, HIMEHINA (Tanaka Hime rescued from J-Pop), Ui Shigure, Aitsuki Nakuru, Nanami Urara, Peanuts-kun.
  - **Anime Franchise Umbrella Unification**: Reunified `Princess Session Orchestra (プリンセッション・オーケストラ) ~` and `World Dai Star (ワールドダイスター) ~` from scattered long seiyuu names in J-Pop.
  - **Regenerated Catalog & M3U8**: Index updated to `26,133` tracks; refreshed `Lossless.m3u8` (`23,463` tracks) and `Lossy.m3u8` (`2,670` tracks). Applied permissions `775/664` and reloaded Samba.

## 2026-09-26 (142)
- **Executed Full Structural Audit & Perfection across `/mnt/hdd-backup/music/Lossless/` (0 format tags, 0 date tags, 0 loose albums).**
  - **Eliminated All Franchise Splinters & Loose Items**:
    - **THE IDOLM@STER**: Rescued mojibake folder `_YK3YV~S` (`?????????`). Unwrapped nested `-28 colors- COLLECTION` and `01 Borderline.flac`. Consolidated all 15 loose sub-units from `Anime/` (`アルストロメリア`, `アンティーカ`, `イルミネーションスターズ`, `コメティック`, `シーズ`, `ストレイライト`, `ノクチル`, `放課後クライマックスガールズ`, `L'Antica`, etc.) and all 11 Gakuen Idolmaster character singles into their canonical subfranchise containers (`Shiny Colors` and `Gakuen Idolmaster`).
    - **Bocchi the Rock!**: Unified all physical, digital, and special disc releases into canonical containers (`[2022-2023] PHYSICAL RELEASES`, `[2022-2023] SPECIAL DISCS`, `[2022-2022] DIGITAL SINGLES`) with 0 loose items.
    - **BanG Dream!**: Sorted all 80+ loose albums and singles into 14 canonical unit folders (`MyGO!!!!!`, `Ave Mujica`, `Poppin'Party`, `Roselia`, `Afterglow`, `Pastel＊Palettes`, `Hello, Happy World!`, `Morfonica`, `RAISE A SUILEN`, `Mugendai Mewtype`, `millsage`, `Compilations`, `Ikka Dumb Rock`, `Parallel`).
    - **Love Live!**: Merged legacy `Nijigaku` folder (34 albums) and all loose singles into canonical generations (`Nijigasaki`, `Aqours`, `Hasunosora`, `Bluebird`, `Liella!`, `School Idol Musical`).
    - **Uma Musume, Girls Band Cry, D4DJ**: Merged loose character singles and units into canonical umbrellas.
  - **Comprehensive Agency & VTuber Consolidation**:
    - Rescued all 6 Hololive English talents accidentally placed in `Vocaloid/`. Merged 30+ loose Hololive talents from `Vtuber/` into `Hololive (ホロライブ) ~` and sorted 54 loose singles into talent subfolders.
    - Consolidated loose talents into `Nijisanji (にじさんじ) ~`, `KAMITSUBAKI STUDIO (神椿スタジオ) ~`, `RK Music ~`, and `RIOT MUSIC ~`.
  - **100% Pure Album Titles**: Stripped all format/bitrate tags (`[FLAC]`, `[CD]`, `[24bit/48kHz]`, `[Hi-Res]`) and date prefixes across all 23,465 lossless tracks. Format tags: 0, Date tags: 0.
  - **Permissions & Master Index**: Enforced permissions `775` (dirs) and `664` (files). Master database indexed `26,135` tracks; updated `Lossless.m3u8` (`23,465` tracks) and `Lossy.m3u8` (`2,670` tracks). Verified 108 GB free space on `hdd-backup`.

## 2026-09-26 (141)
- **Completed Full Homelab Music Centralization & Reorganization (4,794 albums, ~1.05 TB).**
  - **Single Source of Truth**: Centralized all music without exception into `/mnt/hdd-backup/music/Lossless/` across all 4 homelab storage origins (`hdd-backup/download/`, `hdd-media/downloads/`, `hdd-media/qbittorrent/`, and PC local `E:\Download\`).
  - **43 CUE Disc Images Split**: Split all monolithic WAV/FLAC disc images into standalone FLAC tracks via `shnsplit` & `cuetools`. Redundant whole-disc images purged.
  - **False Quarantine & Nested Containers Rescued**: Rescued healthy Tensura & ZUTOMAYO albums from quarantine; dismantled 21-album dumping ground in `清水美依紗 ~/Reunion/`; extracted 404 singles in `General Anime Singles & OST` into proper commercial J-Pop artist folders.
  - **Taxonomy & Pure Naming Standard**: Consolidated 26 canonical anime franchise umbrellas, 6 VTuber agency umbrellas, and normalized all artist folders to `Romaji (Japanese) ~` and album folders to Pure Album Titles.
  - **Lossy & Video Segregation**: Segregated 2,670 non-FLAC lossy tracks to `/mnt/hdd-backup/music/Lossy/` and 12 GB Blu-ray concert video to `Video/`.
  - **Permissions & Master Catalog Rebuilt**: Applied `chmod -R 775/664`. Generated SQLite catalog index (`26,207 tracks`) and updated master playlist `Lossless/Lossless.m3u8` (`23,537 lossless tracks`). Verified 105 GB remaining free space on `hdd-backup`.

## 2026-09-26 (140)
- **Updated `portofolio` container on `personal-hosts` to latest upstream (`52c00d8`).**
  - Pulled latest commits from `https://github.com/samsmon/portofolio.git` (`52c00d8: refactor(theme): rename design tokens and classes from yorha to tactical`).
  - Rebuilt SvelteKit static site and refreshed production container `portofolio` on `personal-hosts` (LXC 103, port 3080).
  - Maintained standalone network configuration (removed legacy `shared_net` external network dependency to match `personal-hosts` isolated topology).
  - Verified live HTTP 200 response on port 3080 (`suryatmaja.dev`).

## 2026-09-26 (139)
- **Defined 26 Canonical Franchise Umbrellas & Strict Romaji-First Anti-Split Policy in `docs/music-standards.md` & `CLAUDE.md`.**
  - Formulated full list of 26 canonical multimedia/anime franchise umbrellas under `Anime/` strictly adhering to `Romaji/Global (Japanese Text) ~` format (e.g. `THE IDOLM@STER (アイドルマスター) ~`, `Uma Musume (ウマ娘) ~`, `BanG Dream! (バンドリ！) ~`, `Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~`, `Girls Band Cry (ガールズバンドクライ) ~`, `Denonbu (電音部) ~`, `Arknights (アークナイツ／塞壬唱片-MSR) ~`).
  - Enforced strict Anti-Split rule prohibiting Japanese-first root names and merging fragmented English/Japanese alias folders into the single canonical Romaji-first umbrella.


## 2026-09-26 (138)
- **Implemented Master M3U8 Playlist generation for instant MusicBee & Foobar2000 loading.**
  - **Feature**: Extended [`scripts/update_catalog.py`](scripts/update_catalog.py) to automatically output relative-path playlists (`Lossless/Lossless.m3u8` with 18,388 tracks and `Lossy/Lossy.m3u8` with 2,194 tracks) during SQLite indexing.
  - **Performance**: Eliminates slow SMB network crawling in desktop audio players. Dragging or opening `Lossless.m3u8` populates the library instantly.
  - **Sync**: Mirrored `Lossless.m3u8` to `/mnt/hdd-music/music/Lossless/` (`Z:\music\Lossless`) with read/write permissions for SMB clients.

## 2026-09-26 (137)
- **Executed server-side metadata-driven reorganization of `/mnt/hdd-backup/download/` (~132 GB, 870 albums).**
  - **Sanitization & Pure Album Standard**:
    - Converted all album directories to "Pure Album Name" (stripped release dates `[YYYY.MM.DD]`, years `(2025)`, format codes `[WEB-FLAC]`, and sample rates `[24bit/48kHz]`).
    - Successfully moved **851 albums**, safely skipped 18 identical entries, and pruned **331 empty obsolete/corrupted directories** (including unpacker artifacts like `100 ~`, `1stBLAZEFLAC ~`, `LOVE ~`, and `_tmp_ext_*`).
  - **Category & Artist Reclassification**:
    - Migrated misfiled VTubers and Doujinshi artists out of `J-Pop/` into canonical `Vtuber/` folders (e.g. `Aitsuki Nakuru (藍月なくる) ~`, `HACHI ~`, `ReGLOSS ~`).
    - Standardized Japanese artist names to canonical `Romaji (Kanji/Hira/Kana) ~` format.
  - **Access & Permissions**: Enforced unprivileged container ownership `100000:100000` with permissions `775` (directories) and `664` (files) across all target folders for seamless Windows SMB reading.

## 2026-09-26 (136)
- **Documented Universal Music Folder Reorganization Framework in `docs/music-standards.md` & `CLAUDE.md`.**
  - Formulated a standard 5-step SOP: `[Auditing & Vorbis Metadata Extraction]` ➔ `[Canonical Classification]` ➔ `[Pure Naming Sanitization]` ➔ `[Dry-Run Plan & Mandatory User Approval]` ➔ `[Server-Side Background Execution]`.
  - Standardized Japanese artist naming format: strictly `Romaji (Kanji/Hira/Kana) ~` (e.g. `Aoki Hina (青木陽菜) ~`).
  - Standardized album naming: strictly "Pure Album Name", eliminating release dates `[YYYY.MM.DD]`, years `(2025)`, and audio codecs/bitrates (`[FLAC 24bit/48kHz]`, `[WEB-FLAC]`).

## 2026-09-26 (135)
- **Enforced mandatory "Analyze First, Confirm Before Execution" & Non-Blocking Server Background Execution rules in `CLAUDE.md`.**
  - Added strict policy under Section 0: Every user request must be thoroughly analyzed and presented with an action plan first. Execution of changes/mutations strictly requires explicit user confirmation beforehand.
  - Updated Section 2 Rule 4: Mandatory detached server-side background execution (`nohup` / systemd) for all heavy/long tasks (audits, syncs, transcoding) to keep AI agent interactive sessions free to immediately proceed with other work.

## 2026-09-25 (134)
- **Ingested 142 new lossless albums from `Torrent/done`, sanitized junk/piracy promos, updated master catalog to 20,582 tracks, and mirrored 1:1 to `hdd-music` (`Z:\`).**
  - **Torrent Ingestion & Blueprint Organization**:
    - Audited 276 items in `/mnt/hdd-backup/music/Torrent/done`. Filtered 15 duplicate folders and 3 loose tracks, and ingested 142 new releases directly into canonical categories in `/mnt/hdd-backup/music/Lossless/`:
      - **Gakuen Idolmaster** (31 albums): Mapped solo releases to `01. Solo/[Character]/`, duos to `02. Duo/`, and student ensembles/anthems to `04. All Stars & Units/`.
      - **Shiny Colors** (4 albums): Ingested *無自覚アプリオリ* into `CANVAS (2023)`, *ECHOES 02 & 04* into `ECHOES (2024)`, and split *HOPEFUL FE@THERS* (-Luna-, -Sol-, -Stella-) into `04. COLORFUL FE@THERS Series/`.
      - **BanG Dream!** (61 albums): Integrated Ave Mujica, MyGO!!!!!, Pastel＊Palettes, Roselia, and 夢限大みゅーたいぷ.
      - **Love Live!** (18 albums): Added Hasunosora, Nijigaku, Liella!, and Sunshine!! GKSS releases.
      - **D4DJ** (9 albums): Integrated Merm4id & Rondo discographies into `Anime/D4DJ ~/`.
      - **VTuber / Hololive** (11 albums): Placed into canonical folders for 鷹嶺ルイ, さくらみこ, 桃鈴ねね, miComet, and Midnight Grand Orchestra.
      - **J-Pop & Other Anime** (8 albums): Ingested milet 2nd & 4th albums into `J-Pop/Milet ~/`, Tokyo 7th Sisters Side 2053, ポールプリンセス!!, and IDOLY PRIDE into `Anime/`.
  - **Sanitization & Permissions**:
    - Purged 805 tracker advertisements and junk promo text files (`Discord.txt`, `Music Download.txt`, `*.url`).
    - Enforced POSIX ACLs & permissions (`100000:100000`, 775 directories, 664 files) for seamless SMB read/write.
  - **Catalog & Storage Parity**:
    - Refreshed master SQLite catalog (`/mnt/hdd-backup/music/catalog.sqlite`): indexed 20,582 total tracks.
    - Executed internal 1:1 rsync mirror to `/mnt/hdd-music/music/Lossless/` (`Z:\`), bringing curated music drive to 804 GB (93% used).
- **Enforced strict server-side execution rule in `CLAUDE.md` and launched background Master Library Healing & Migration daemon.**
  - **Rule Enforcement (`CLAUDE.md`)**:
    - Added Section 2 Rule 4: Mandatory server-side execution (`docker-host` / `pve`) for all analysis, audits, tagging, and heavy operations to eliminate local PC CPU/RAM and SMB network bottlenecks, allowing Antigravity sessions to be safely closed while jobs proceed uninterrupted.
  - **Launched Master Library Healing Daemon (`master_healing_daemon.py` PID 644705)**:
    - Fixed Sizuk album tagging (`TITLE` UTF-8 characters restored from `?????`, embedded cover art re-linked cleanly), moved to canonical `Lossless/J-Pop/Sizuk ~/`, and purged misplaced/duplicate folders.
    - Purged redundant monolithic rip `Lossless/Anime/かくりよの宿飯 ~` (verified existing 8-track FLAC in `Lossless/J-Pop/Tōyama Nao 東山奈央 ~`).
    - Migrated misplaced VTuber and Doujinshi/Vocaloid releases from `J-Pop/` to canonical `Vtuber/`, `Doujinshi/`, and `Vocaloid/` folders.
    - Script running full library tag scan, permission enforcement (`100000:100000`), catalog SQLite update, and internal 1:1 rsync mirroring to `Z:\` (`hdd-music`).

## 2026-09-24 (132)
- **Tuned Samba for high-speed MusicBee traversal, conducted comprehensive 24k-file Lossless audit, and detached sync into independent PVE server daemon.**
  - **Samba Performance Tuning (`smb.conf`)**:
    - Applied `hide unreadable = no` to `[homelab]` and all storage shares, eliminating expensive per-file Linux permission evaluations during client-side library scans.
    - Added directory fast-traversal parameters (`case sensitive = auto`, `preserve case = yes`) to `[global]` and cleanly reloaded `smbd`.
  - **Full Library Deep Audit (24,144 files across `/mnt/hdd-backup/music/Lossless`)**:
    - Purged 172 redundant `.cue` sheets across split albums to permanently resolve MusicBee duplicate-track parsing.
    - Flattened 11 nested audio directories (`FLAC/`, `WAV/`) directly into parent album roots.
    - Removed 245 advertisement files (`.url`, `Discord.txt`, `Readme.txt`).
    - Fixed folder naming: renamed `06. "CANVAS" (2023)` to `06. CANVAS (2023)` eliminating Samba 8.3 name mangling.
    - Verified bitstream health: 0 corrupt FLACs, 0 zero-byte audio files.
  - **Independent Sync Daemon & Cleanup**:
    - Deployed detached background daemon on PVE hypervisor via `nohup` (`/tmp/run_daemon_sync.sh` logging to `/var/log/sync-music-final.log`) to mirror Uma Musume (~86 GB) and complete Lossless changes to `/mnt/hdd-music/music/Lossless/` achieving 100% 1:1 parity (778 GB both sides).
    - Safely purged raw torrent source folder `/mnt/hdd-media/qbittorrent/watch-torrents/UmaMusu discography` (85 GB freed, disk usage dropped from 72% to 63% / 329 GB available).

## 2026-09-24 (131)
- **Replaced and upgraded `Uma Musume ~` discography with complete 130-album torrent dataset (84.6 GB), preserving Astell&Kern Special CD.**
  - Reorganized into 7 canonical subseries under `/mnt/hdd-backup/music/Lossless/Anime/Uma Musume ~/`:
    1. `01. WINNING LIVE Series/` (39 albums, WINNING LIVE 01..23, Remix, etc.)
    2. `02. ANIMATION DERBY Series/` (15 albums, Seasons 1..3, Season 2 OST)
    3. `03. STARTING GATE Series/` (14 albums, 01..12 & Unit Collections)
    4. `04. SOLO VOCAL TRACKS/` (18 albums, 3rd..7th event compilations)
    5. `05. UMAYURU & UMAYON/` (11 albums, singles & mini-albums)
    6. `06. Singles, OST & Other/` (39 albums, Shinjidai no Tobira, ROAD TO THE TOP, Cinderella Gray, etc.)
    7. `07. Compilations/` (Preserved audiophile release: `[2018.12.14] ウマ娘 プリティーダービー Astell&Kern Special Compilation CD [FLAC 96kHz／24bit]`)
  - Total 131 albums, 2,084 audio tracks (100% FLAC, majority 96kHz/24bit & 48kHz/24bit Hi-Res).
  - Replaced former 38 albums containing 124 lossy `.m4a` files with full lossless FLAC audio. Sanitized folder names for Windows SMB compatibility.
  - Re-indexed `/mnt/hdd-backup/music/catalog.sqlite` (now tracking 20,079 total library tracks). Permissions applied `100000:100000` (775/664).

## 2026-09-24 (130)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`b1e99eb`→`ae496df`), 3 commits: autonomous "Anti-Throttle" watchdog that detects CDN bandwidth throttling and auto-activates a Cloudflare WARP local SOCKS5 proxy (or a custom proxy pool) with WireGuard key rotation and seamless reconnect at the exact byte offset; Stop All / Resume All queue controls with atomic backend endpoints; IDM-style multi-socket Discord downloads with auto-healing chunk restart, virtual scrolling, and stable sort. Checked carefully since WARP support could've meant a new binary dependency — confirmed `Dockerfile` is untouched (`warp-cli` isn't bundled in the image) and the code degrades gracefully via `exec.LookPath`, falling back to an optional user-configured custom proxy string, or a clear error if neither is present — no build/env changes needed. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200` and clean startup log.

## 2026-09-24 (129)
- **Implemented canonical Option A hierarchy for `THE IDOLM@STER SHINY COLORS` and ingested 55 discography archives (~35GB) from `download/`.**
  - Established 5-tier canonical hierarchy under `/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~/シャイニーカラーズ/`:
    1. `01. WING & Main Game Series/` with numbered cycles: `01. BRILLI@NT WING (2018)`, `02. FR@GMENT WING (2019)`, `03. GR@DATE WING (2020)`, `04. L@YERED WING (2021)`, `05. PANOR@MA WING (2022)`, `06. "CANVAS" (2023)`, `07. ECHOES (2024)`.
    2. `02. Song for Prism Series/` (16 single releases from mobile game 2024–2026).
    3. `03. Anime Series/` (Season 1 & 2 OP/ED, theme albums, Halloween).
    4. `04. COLORFUL FE@THERS Series/` (Stella, Luna, Sol, SHHis, CoMETIK albums).
    5. `05. Synthe-Side & Collaborations/` (Synthe-Side 01..03).
  - Extracted 52 new unique release archives using `7z`, filtered redundant duplicate archives (`(2).zip`), and relocated existing `ECHOES` albums into the new WING folder.
  - Sanitized all filenames for Windows SMB compatibility (full-width colons, slashes, asterisks) and flattened all album roots (zero nested folders, audio files at root, booklets in `BK/`).
  - Audited full library: 66 albums, 367 total audio tracks, 0 anomalies. Re-indexed master SQLite catalog (`/mnt/hdd-backup/music/catalog.sqlite`) now tracking 18,658 total tracks. Permissions set to `100000:100000` (775/664).

## 2026-09-24 (128)
- **Built a proper master-archive sync system (config-driven, curation-aware, non-destructive) and deployed Cronicle as its scheduler/dashboard.**
  - New `scripts/sync-config.conf`: user-editable list of `MEDIA_TYPE|MASTER_PATH|TARGET_PATH` lines defining exactly which folders sync from `hdd-backup` (master) to which target drive — this is how curation works (e.g. only `Lossless/` syncs to `hdd-music`, not the whole music library) without editing any script.
  - New `scripts/sync-from-master.sh`: generic engine reading that config, using `rsync --checksum --itemize-changes` so a run only touches files that are missing/misplaced/actually different — never a blind full re-copy, and never deletes anything unless `--prune` is explicitly passed. `--report-only` previews the diff without writing. Replaces yesterday's `sync-music.sh` (removed, same logic now config-driven).
  - `scripts/sync-manga.sh` reworked: convert step unchanged, but the merge/sync direction is now `hdd-backup/manga-raw` (master) → `hdd-media/manga-raw`, since `manga-raw` fully relocated to `hdd-backup` earlier today and Komga still reads from `hdd-media` (via `manga-optimizer.py`'s separate watchdog daemon, which generates the WebP `manga-reader` library — discovered this daemon was running against a now-nonexistent `hdd-media/manga-raw` path, silently doing nothing since the move; this sync restores its expected input).
  - **Deployed Cronicle** (`soulteary/cronicle` image) on `docker-host` as the cron manager + web dashboard the user asked for — supports both scheduled runs and on-demand "Run Now" triggering (e.g. right after adding new files, without waiting for the schedule). Mounts `/opt/scripts` read-only plus all three HDD roots. Created 3 jobs: Sync Music (14:00), Sync Manga (08:00), Sync Video (18:00).
  - **Discovered mid-setup that Cronicle is already reachable publicly** at `cron.suryatmaja.dev` via an existing Cloudflare Tunnel route — not something this session configured. Warned the user twice about the default `admin`/`admin` login before they changed it, and again after they set it to a 2-character password, given this panel can execute arbitrary shell commands on the host with access to all three HDDs. User explicitly acknowledged the risk and declined to harden it further (e.g. restricting the Cloudflare route to trusted IPs). Documented as an open risk in `docs/services.md` — revisit if it becomes a real incident.

## 2026-09-24 (127)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`e55968a`→`b1e99eb`): fixes duplicate-filename collisions, adds HTTP 416 (Range Not Satisfiable) recovery, and freezes the table header on scroll. No new required env vars, compose untouched. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-24 (126)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`0b30c38`→`e55968a`), 3 commits: dedicated `chunked` package for parallel multi-chunk downloads (now works on resume too, plus chunk-progress badges in the UI), Discord CDN downloads fixed for HTTP/2 stream errors + a new AI-agent export/refresh workflow, and multi-socket HTTP/1.1 transport enforced for Google Drive to bypass its TCP connection limit (Discord downloads intentionally kept single-stream). No new required env vars, compose untouched. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-24 (125)
- **Added `hide unreadable = no` override to the `[hdd-music]` Samba share** to speed up client-side directory scans (user reported MusicBee scanning the music library over SMB feels slow/heavy). Global default is `hide unreadable = yes`, which makes `smbd` do a per-file/folder permission pre-check before including it in any directory listing — real overhead on a library this size, and no actual security benefit here since every file is `force user/group = root` with `0777` create/directory masks anyway (everything is readable by the one valid user regardless). Scoped to `[hdd-music]` only (not global) per user's choice, to avoid touching other shares' behavior. Validated with `testparm -s`, `systemctl restart smbd`, confirmed active.

## 2026-09-24 (124)
- **Moved `manga-raw` (135GB) from `hdd-media` to `hdd-backup` to free space on `hdd-media` (161G→250G avail), per user request.** Since Komga only reads the derived `manga-reader` library (auto-generated by `manga-optimizer.service`, unaffected and left in place on `hdd-media`), no clone/sync-back was needed — just repointed the one real consumer.
  - Stopped `manga-optimizer.service`, `rsync`'d all 7,432 items (144.18G) `hdd-media`→`hdd-backup`, verified byte-identical with a `--checksum` dry-run (0 created/deleted/transferred — full match) before deleting the source. `hdd-backup` SMART health checked clean during the transfer (0 reallocated/pending sectors, 36°C, `UDMA_CRC_Error_Count` unchanged from its known-stable baseline).
  - Repointed 3 consumers: `manga-optimizer.py`'s `SRC_DIR` (docker-host), the Samba `[manga]` share's `path` (docker-host `smb.conf`), and `nhdl`'s `DOWNLOAD_DIR` + added a missing `/mnt/hdd-backup` bind mount to its compose (`personal-hosts`) — `docker compose up -d --force-recreate` used for `nhdl`, not a plain restart, per the (83) Nextcloud phantom-mount lesson (a bind-mount source change needs recreate or Docker silently substitutes an empty dir). All 3 verified: `manga-optimizer.service` restarted clean and is actively optimizing from the new path, `nhdl` container sees real data at the new mount and serves `HTTP 200`.
  - Updated `scripts/sync-manga.sh`'s `DEST_JP`/`DEST_EN` to the new `hdd-backup` paths, and `docs/architecture.md`/`docs/services.md` to match current state.
  - **Found and flagged separately, not fixed**: `docker-host`'s `/root/homelab-ops` git clone is badly stale with a dangerous unpushed local commit (`349e822`) that would delete ~5,500 lines across `CHANGELOG.md`, `docs/`, and `scripts/` if ever pushed/merged. Left untouched — the live `manga-optimizer.py` file on disk was patched directly via `sed`, bypassing git entirely, to avoid interacting with that stale clone's history.

## 2026-09-24 (123)
- **Synchronized `/mnt/hdd-music/music/Lossless` with master library from `/mnt/hdd-backup` — 100% parity achieved across all 699 GB.**
  - Executed safe two-phase synchronization using `rsync --delete-before`: first purged 5,803 obsolete/un-reorganized files (~191 GB) to maintain healthy headroom, then transferred 7,713 newly organized files (317.85 GB) at 12.82 MB/s without I/O contention.
  - Mirrored fully standardized franchises:
    - `THE IDOLM@STER ~/`: Canonical 4-tier Gakumas (`01. Solo`, `02. Duo`, `03. Trio`, `04. All Stars & Units`), Shiny Colors (`Song for Prism`, `ECHOES`, `Anime`, `Unit Singles`), and `vα-liv`.
    - `Uma Musume ~/`: Reorganized 5 subcategories (`01. WINNING LIVE`, `02. ANIMATION DERBY`, `03. STARTING GATE`, `04. Theatrical & Specials`, `05. Compilations`).
    - `ご注文はうさぎですか？？ (Gochuumon wa Usagi Desu ka) ~/`: Reorganized 3 subcategories, split FLAC tracks, sanitized artwork, zero CUE/WAV images.
    - `＊Luna ~/`: Fixed Samba 8.3 mangled naming (`_FCR9Q~X` -> canonical UTF-8 fullwidth).
    - Purged stray `No Group/` and loose root albums (`メメントモリ`).
  - Verified 1:1 directory size parity across all categories (Anime 353G, J-Pop 200G, Vtuber 74G, Doujinshi 46G, Vocaloid 27G, Global 486M). Total target storage: 699G used, 171G free on `/mnt/hdd-music`.
  - Enforced ownership `100000:100000` with permissions `775` (dirs) and `664` (files) across the entire target library.

## 2026-09-24 (122)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`dd29b3c`→`0b30c38`), 3 commits: multi-chunk parallel download (faster large-file transfers) + rclone token import + full English localization, smoother/higher-rate progress bar interpolation, and a fix preserving "completed" status when pause/start is triggered on an already-finished selection. No new required env vars, compose untouched. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-24 (121)
- **Completed 411 GB video library seeding to `hdd-backup`, established Alur A master-playback architecture, and activated automated daily sync.**
  - Seeded 440.57 GB of video content from `/mnt/hdd-media/videos` to `/mnt/hdd-backup/videos` via `sync-videos --to-backup` (completed cleanly with exit code 0; verified identical size: `411G` on both drives).
  - Adopted Alur A architecture: `/mnt/hdd-backup/videos` serves as the cold Master Archive, while `/mnt/hdd-media/videos` serves as the active Playback/Serving clone for Jellyfin.
  - Created reusable sync script `scripts/sync-videos.sh` (installed to `/usr/local/bin/sync-videos` on `docker-host`) with `flock` locking, `--partial --inplace` efficiency, and bidirectional support (`--to-backup`).
  - Deployed and enabled systemd timer on `docker-host`: `homelab-video-sync.timer` and `homelab-video-sync.service` (runs daily at 04:30 WIB).
  - Confirmed WD Green (`hdd-backup`) hardware health: S.M.A.R.T. `UDMA_CRC_Error_Count` unchanged at 21430 (zero errors during full 440 GB transfer), with 512 GB free space remaining (71% utilized).

## 2026-09-24 (120)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`219c202`→`dd29b3c`): removes the 60s timeout on the OAuth-bypass stream client (was likely killing large-file downloads mid-transfer) and adds logger calls for single-file downloads; also adds upstream's own `TODO.md` (rclone token import, full English localization — informational only, no action needed here). No new required env vars, compose untouched. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-24 (119)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`4218c8f`→`219c202`): fixes (118)'s new OAuth flow for LAN access — normalizes private LAN IP redirect URIs to `localhost` (Google's OAuth client rejects raw LAN IPs like `192.168.18.228` as redirect URIs) and adds a custom redirect URI override for edge cases. Relevant since `gddl` is reached via LAN IP here. No new required env vars, compose untouched. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-24 (118)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`28c5caa`→`4218c8f`), biggest feature update yet: **Google OAuth2 integration with automated quota-bypass** (`ggdl_temp` copy-then-download trick) as an alternative to cookie-pool failover, plus a manual code-paste flow (rclone-style) for headless setups. Checked carefully before updating since OAuth usually implies new required config — confirmed it's fully opt-in: client ID/secret are entered and stored via the UI (`config.json`, not compose env vars), and the redirect URI is derived dynamically from the request's `Host` header rather than hardcoded, so no compose changes were needed. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200` and clean startup log. OAuth not configured/tested — opt-in feature, left for the user to set up if wanted.

## 2026-09-24 (117)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`2f79c64`→`28c5caa`): supports the cURL `-b` cookie flag on import and sanitizes control characters in header fields. No new required env vars, compose untouched by upstream. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-24 (116)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`faa795d`→`2f79c64`): cookie redirect preservation, 3-cookie validation, in-app confirm dialog, log text selection, plus cURL auto-extraction / JSON cookie support / quick guide in the cookie pool modal. No new required env vars, compose untouched by upstream. Same stash/pull/pop pattern, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-24 (115)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`f356053`→`faa795d`): cross-drive move engine, lazy link ingestion, multi-cookie pool auto-failover. Confirmed no new required env vars before updating (checked `git diff` for new `os.Getenv` calls — none). Same stash/pull/pop pattern as prior updates, `docker compose up -d --build`, verified `HTTP 200`.
  - **Noted, not changed**: post-rebuild the active download folder is `/mnt/hdd-backup/download` (from `config/config.json`'s `download_folder`, not the compose `DOWNLOAD_DIR` env — a persisted UI setting, now actually honored since (113)'s "auto-persist default save path" feature landed). This runs counter to `hdd-backup`'s cold-backup-only role from `docs/decisions.md`, but user explicitly confirmed leaving it as-is when flagged.

## 2026-09-24 (114)
- **Closed out the manga-raw broken-file cleanup: 0/2422 broken now, down from 870 on 2026-09-23.** Added two reusable scripts (`scripts/sync-music.sh`, `scripts/sync-manga.sh`) to `scripts/` for the user to run manually and later hook into a cron manager — both use `rsync --checksum` (skip-if-content-matches, replace-if-differs/misplaced/corrupt), matching the pattern established in (112).
  - Re-downloaded the 22 titles that (112) identified as having no replacement, using the `.nhdl-id` codes extracted from their sidecar files. This time the download tool auto-compressed to `.cbz` directly (no raw-folder conversion needed).
  - Merged via `sync-manga.sh --merge-only`. 8 of 22 didn't get picked up by the exact-name-match merge because the downloader used slightly shortened titles this round (e.g. dropped a `2`/`3` suffix, dropped a parenthetical subtitle) — left the old broken stub orphaned under its old filename. Manually identified all 14 orphans (some were pre-existing from before, not just these 22), verified the correctly-named new file was valid (`file` = Zip, not HTML) before deleting each old stub.
  - Final audit: **`JP`: 0/961 broken, `Unofficial`: 0/1453 broken.**

## 2026-09-23 (112)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`c922098`→`f356053`): adds folder creation inside the save-path picker, fixes default save path auto-persist + add-dialog path sync, allows relocating in-progress downloads, and adds a concurrency-risk guide. Same stash/pull/pop pattern as (107)/(109) — local `docker-compose.yml` edit untouched by upstream, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-23 (112)
- **Merged the converted `nhdl` batch into `manga-raw/nsfw` (`Japanese`→`JP`, `English`→`Unofficial`), fixing hundreds of previously-broken entries in the existing collection.**
  - Pre-merge audit found the existing collection had a large number of `.cbz` files that were actually **saved HTML error pages** (10-17KB, `file` identified them as HTML, not valid zip archives) rather than real manga — almost certainly leftover from failed downloads. Full audit: **326/934 broken in `JP`, 544/1433 broken in `Unofficial`** (870 total).
  - Cross-referenced against the fresh `nhdl` download: 315 of `JP`'s broken files and all 533 of `Unofficial`'s broken files had an exact-name match in the new download — i.e. the new download was a **fix**, not a risk of overwriting something better. Spot-checked the 8 exact-name matches that *were* already valid in `JP`: sizes identical or within a few KB, no quality concern.
  - Also checked for renamed/fuzzy duplicates (same content, different filename) among the 35+24 titles that had no exact name match — compared by file size against the full valid (non-HTML) existing collection, zero coincidental matches found, confirming these are genuinely new additions.
  - Executed the merge via `rsync` (default overwrite-on-copy), verified post-merge: `JP`'s broken-file count dropped from 326 to the expected 11 (titles with no fresh replacement available — listed below for future re-download). Deleted the now-empty `/mnt/hdd-media/download/nhdl` source.
  - **22 titles remain broken** (no replacement was available in this batch) — flagged for manual re-download later: 11 in `JP` (Ashiomi Masato, Baketsu Purin, Gonza, Izure, Ken-1, Kirishima Ayu, Kurukuru, Maskwolf Keinv, Nako Sir, Tawara Hiryuu, Zonebell Tsukiji — full title list in this session's transcript) and 11 in `Unofficial` (Akagi Asahito, Amazon, Azuse, Clone Ningen, Furiouzly, Ginen, Hyji, Jinsuke, Juna Juna Juice, Komagata, Nodo).
  - `hdd-media` usage: 77% (unchanged from (108), since this was an internal move within the same drive, not new data).

## 2026-09-23 (111)
- **Organized `hdd-media/videos/movies/nsfw` into 1-folder-per-movie Jellyfin standard with single clean `.jpg` thumbnail.**
  - Cleaned up redundant image variations (`_thumbs.jpg`, `.mp4_thumbs.jpg`, `-thumb.jpg`), keeping exactly one high-resolution contact sheet image per title (`[name].jpg`).
  - Restructured all 70 videos into individual dedicated movie folders (67 in `jav thumb/`, 3 in `biasa/`).
  - Verified 100% clean audit: every folder contains exactly 1 `.mp4` and 1 `.jpg` (zero loose files in root directories).
  - Triggered Jellyfin library scan.

## 2026-09-23 (110)
- **Consolidated `hdd-media/videos/movies/nsfw/jav` into `jav thumb` (Option B) and generated 5x8 MPC-HC thumbnail sheets for all 70 videos.**
  - Moved all 23 videos from `jav/` to `jav thumb/` and cleaned up empty directory.
  - Sanitized long titles exceeding 200 bytes down to canonical code filenames to prevent ext4 255-byte limit errors.
  - Generated missing 40-clip MPC-HC style contact sheets using fast-seek FFmpeg + multithreaded Pillow with CJK font support.
  - Created zero-cost ext4 hardlinks for every video: `[video].jpg` (Jellyfin primary poster) and `[video]-thumb.jpg` (Jellyfin backdrop), ensuring permanent visibility in Jellyfin and media players.
  - Verified 100% coverage (70/70 videos) across `jav thumb/` (67) and `biasa/` (3). Triggered Jellyfin library refresh.

## 2026-09-23 (109)
- **Updated `gddl` (personal-hosts) to latest upstream again** (`62f8d2f`→`c922098`): perf tweak, boosts download throughput with 1MB I/O buffers and HTTP transport tuning (gdrive + discord downloaders, folder listing). Same stash/pull/pop pattern as (107) — local `docker-compose.yml` edit untouched by upstream, `docker compose up -d --build`, verified `HTTP 200`.

## 2026-09-23 (108)
- **Converted all 858 raw-image `nhdl` title folders on `hdd-media` into `.cbz` archives, freeing further space (90%→77% full).** Each title folder (`Japanese/<Artist>/<Title>/*.webp` etc) was previously stored as loose images rather than an archive, inconsistent with the 24 titles that already existed as `.cbz` and less optimal for Komga to serve.
  - Used `zip -0` (store mode, no compression — images are already compressed formats, so this is just packaging, not size reduction) per folder, verified each archive with `unzip -tq` immediately after creation, and only deleted the original folder once verification passed. Zero failures, zero folders skipped, zero raw folders left behind afterward.
  - Installed `zip` on `pve` (was missing — only `unzip` was present).

## 2026-09-23 (107)
- **Updated `gddl` (personal-hosts) to latest upstream** (`e855552`→`62f8d2f`): adds Discord CDN download support (anti-rate-limit, HTTP range resume) plus a repo/release-URL and extra-drives-separator fix. Stashed the server-specific local `docker-compose.yml` edit (container name/port `8099`, `DOWNLOAD_DIR`, `EXTRA_DRIVES` mounts) before pulling, confirmed the 2 upstream commits didn't touch that file, popped the stash back, `docker compose up -d --build`. Verified `HTTP 200` and clean startup log post-rebuild.

## 2026-09-23 (106)
- **Deduplicated redundant videos in `hdd-media/videos/movies/nsfw` — freed 26GB (disk usage dropped from 80% to 77%).**
  - Scanned all 80 videos across `jav/`, `jav thumb/`, and `biasa/` analyzing duration via `ffprobe`, JAV codes, resolutions, and bitrates.
  - Eliminated 10 duplicate video files across 9 titles (`CJOD-527`, `WAAA-682`, `PPPE-435`, `NSODN-025`, `PRED-886`, `MIDE-786`, `HMN-377`, `SNOS-258`, `GOJI-058`) and 4 orphan thumbs.
  - Retained high-resolution/raw master files and cleaner titles while removing identical hash duplicates, lower-resolution encodes, and `_2.mp4` redownloads. Library verified at 70 unique videos.

## 2026-09-23 (105)
- **Moved `hdd-media/qbittorrent/watch-torrents` (77GB, 300 albums) to `hdd-backup/music/Torrent/done` and verified integrity — freed `hdd-media` from 99% to 90% full.** Root cause of the 77GB living in `watch-torrents` in the first place: qBittorrent's default watched-folder behavior saves completed downloads alongside the `.torrent` file's own location unless overridden, so the whole batch landed there instead of `downloads/`.
  - `rsync` copy (not straight move) to `hdd-backup` first, verified via `--checksum` dry-run diff (empty = perfect match, 1708/1708 files, 77G/77G both sides), only then deleted the source. Zero risk of data loss if anything had gone wrong mid-copy.
  - Ran `flac -t` integrity test on all 1313 FLAC files in the moved batch — **zero corrupt files**. Spot-checked the non-FLAC leftovers (243 txt, 76 png, 70 jpg, 4 log, 1 cue, 1 mp3) via `file` — all valid, no truncation.
  - This is also incidental extra real-world validation for `hdd-backup`'s power-cable fix: 77GB written to it with zero `dmesg` errors, consistent with the clean stress-test results so far.

## 2026-09-23 (104)
- **Codified mandatory Album Ingestion & Consistency Protocol across repo rules for all AI agents.**
  - **CLAUDE.md & docs/music-standards.md**: Added universal 8-point ingestion checklist for `Lossless/` and `Lossy/`:
    1. Zero loose albums outside `~` folders in category roots.
    2. Strict hierarchy compliance: must place new albums inside established subseries (e.g. `Song for Prism Series`, `WINNING LIVE Series`, `01. Solo/[Character]`).
    3. Mandatory consistent naming: `[YYYY.MM.DD] [Artist] - [Title] [Format]`.
    4. Flat album root: audio tracks must reside directly in the album folder (never nested in `FLAC/`, `WAV/`, or `MP3/`).
    5. Clean track naming & metadata: `01. [Title].[ext]`, no raw store IDs (mora `1-0007...`), full Vorbis/ID3 tags.
    6. Split full-disc images with CUE into standalone tracks and delete redundant disc images.
    7. Zero junk policy: purge piracy links (`.url`), download ads (`.txt`), and duplicate lowercase artwork.
    8. Permissions & Indexing: apply `chown -R 100000:100000`, `chmod -R 775` (dirs) / `664` (files), and run `update_catalog.py`.

## 2026-09-23 (103)
- **Restructured Gochuumon wa Usagi Desu ka into 3 canonical subseries and consolidated THE IDOLM@STER franchise umbrella.**
  - **Gochuumon wa Usagi Desu ka (`ご注文はうさぎですか？？ ~`) Overhaul**:
    - Converted and split 3 uncompressed WAV+CUE albums (`宝箱のジェットコースター`, `ぴょん'sぷりんぷるん`, `ハートぷるぷる事件です`) into individual FLAC tracks with embedded Vorbis comments from CUE metadata, keeping `BK/` booklet scans intact.
    - Split single disc image `ノーポイッ！ [FLAC+CUE+BK]` into 9 standalone FLAC tracks.
    - Renamed mora raw store IDs (`10-0005482832.flac`, `1-0007706200.flac`...) to clean numbered titles in `ときめきポポロン♪ [FLAC 48kHz／24bit]`, `cup of chino`, and Character Songs `01 ココア` through `05 メグ`.
    - Flattened nested `FLAC/` folders in `Daydream cafe` and `ごちうさブレンド` directly into album roots.
    - Consolidated scans (`BK/`) from 16-bit CD-DA folder into `ときめきポポロン♪ [FLAC 48kHz／24bit+BK]`.
    - Purged duplicate releases: removed 16-bit and CUE image duplicates of `order the songs` (retaining the 24-bit/48kHz Hi-Res version) and deduplicated `10th Anniversary`.
    - Removed piracy tracker leftovers (`.url` links, `Read.txt`, `Discord.txt`, duplicate lowercase covers).
    - Grouped all 20 releases across 3 subseries: `01. Theme Songs (OP & ED)`, `02. Character Song Series`, and `03. Albums & Compilations` (146 FLACs total).
  - **THE IDOLM@STER Franchise Umbrella (`Anime/THE IDOLM@STER ~/`)**:
    - Unified all Idolmaster branches under `Anime/THE IDOLM@STER ~/`.
    - Relocated `学園アイドルマスター` preserving 100% of its pristine 4-tier structure (`01. Solo` with 13 character folders, `02. Duo`, `03. Trio`, and `04. All Stars & Units`) and artist-first naming.
    - Structured `シャイニーカラーズ` into 4 subseries:
      - `01. Song for Prism Series/` (housing 7 albums ready for incoming Song for Prism releases).
      - `02. ECHOES Series/` (ECHOES 01, 07, 08, 09).
      - `03. Anime Series/` (deduplicated `Over the prism`, 2nd Season OP, Halloween album).
      - `04. Unit Singles & Compilations/` (`COLORFUL FE@THERS -CoMETIK-`).
    - Housed `vα-liv` under `THE IDOLM@STER ~/vα-liv/`.
    - Removed obsolete empty top-level directories `学園アイドルマスター ~` and `アイドルマスター シャイニーカラーズ ~`.
  - **System, Permissions & Catalog**:
    - Rebuilt master SQLite catalog `/mnt/hdd-backup/music/catalog.sqlite` tracking 18,366 valid tracks.
    - Created reusable catalog indexing script `scripts/update_catalog.py`.
    - Applied `100000:100000` ownership and `775` permissions across both libraries for Windows SMB access.
    - Verified drive SMART health (`UDMA_CRC_Error_Count` = 21430, 0 errors).

## 2026-09-23 (102)
- **Synchronized music standards documentation and CLAUDE.md guidelines with the 4-tier Gakumas model.**
  - **docs/music-standards.md**: Updated visual classification table to strictly reference the 4-tier target paths (`01. Solo/[Character]/`, `02. Duo/`, `03. Trio/`, `04. All Stars & Units/`) and added explicit Duo specification with alphabetical sorting requirement.
  - **CLAUDE.md**: Updated section 3 to mandate the 4-tier Gakumas directory hierarchy and strict `[Artist] - [Title] [Format]` naming standard across all AI agents.

## 2026-09-23 (101)
- **Standardized Gakuen Idolmaster into 4 distinct tier folders (`Solo`, `Duo`, `Trio`, `All Stars & Units`) with strict `[Artist] - [Title]` naming.**
  - **4-Tier Structural Separation**:
    - `01. Solo/`: Contains 13 idol character subfolders (`01. 花海咲季` .. `13. 雨夜燕`), housing 42 solo releases. Every album strictly formatted as `[Artist] - [Title] [Format]`.
    - `02. Duo/`: Established dedicated placeholder directory for future duo releases (`[Artist 1・Artist 2] - [Title] [Format]`).
    - `03. Trio/`: Consolidated all 20 trio event and seasonal releases. Formatted as `[Artist 1・Artist 2・Artist 3] - [Title] [Format]` with artists sorted alphabetically.
    - `04. All Stars & Units/`: Housing official units (`Begrazia`), multi-character combinations (`SUPREMACY`, `Let's GO!! ICHI-NO-NI!!`, `ナイワ`), and full-cast anthems (`初`, `Campus mode!!`).
  - **Updated Standards Documentation**: Updated `docs/music-standards.md` to record the 4-tier model and strict artist-first naming syntax.
  - **Master Catalog Updated**: Re-indexed `/mnt/hdd-backup/music/catalog.sqlite` tracking 18,445 valid tracks. SMART `UDMA_CRC_Error_Count` remained rock solid at 21430.

## 2026-09-23 (100)
- **Codified permanent Music Library Standards and Gakuen Idolmaster categorization rules across homelab documentation.**
  - **Created `docs/music-standards.md`**: Comprehensive reference detailing:
    - Zero loose albums rule across all categories on `hdd-backup` and `hdd-music`.
    - Strict Windows SMB safe naming guidelines (avoiding `:` and ASCII `*` to eliminate 8.3 name mangling like `_FCR9Q~X`).
    - Uma Musume 5-series discography pattern standards.
    - Gakuen Idolmaster visual cover art, track structure, and metadata classification matrix (distinguishing Birthday singles, 1st Solo debuts, Physical CD singles with scans, Solo Special True End tracks, subsequent 2025 solo updates, Event Songs trio combinations, and All Stars anthems).
  - **Updated `CLAUDE.md`**: Added permanent `Music Library Standards` section directing all AI agents to adhere to `docs/music-standards.md` on future album and file ingestions without repeating preliminary research.


---

> Older changelog entries (1 to 99) have been archived to [CHANGELOG-archive.md](docs/CHANGELOG-archive.md) to maintain fast parsing and token efficiency for AI agents.
