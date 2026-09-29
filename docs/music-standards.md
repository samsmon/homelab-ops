# Music Library Standards & Curation Guidelines (`hdd-backup` & `hdd-music`)

> Source of truth for music library organization, character classification, and naming standards across all AI agents and tools.

---

## 1. Universal Library Standards

1. **Zero Loose Albums Rule**:
   - Every single album or single must reside inside an official canonical artist or franchise folder ending with a tilde space (`~`), e.g., `Lossless/Anime/THE IDOLM@STER ~/` or `Lossless/J-Pop/＊Luna ~/`.
   - Never leave unparented loose album folders in category roots (`Anime`, `Doujinshi`, `J-Pop`, `Vtuber`, `Vocaloid`, `Global`).

2. **Windows SMB Safe Naming (Strict No-Mangling Rule)**:
   - Windows NTFS/FAT strictly forbids characters: `\ / : * ? " < > |`.
   - On Linux ext4, these characters are technically allowed, but Samba will mangle folder names into DOS 8.3 hashes (e.g. `_FCR9Q~X`, `_P6X4P~L`) when viewed from Windows SMB.
   - **Mandatory Replacement**:
     - Replace ASCII `*` with full-width asterisk `＊` (U+FF0A), e.g., `＊Luna ~`.
     - Remove ASCII `:` (colon) or replace with full-width colon `：` (U+FF1A), e.g., `[ahi] ~`.
     - Replace ASCII `?` with full-width `？` (U+FF1F) or omit.
     - Replace ASCII `/` or `\` with space or hyphen `-`.

3. **Master Repository Roles**:
   - `/mnt/hdd-backup/music/`: Comprehensive master repository containing all full discographies (`Lossless/`, `Lossy/`, `catalog.sqlite`).
   - `/mnt/hdd-music/music/`: Lightweight curated listening library (`Lossless/`).
   - Whenever tracks or folders are added, moved, or deleted, always re-index the master SQLite catalog at `/mnt/hdd-backup/music/catalog.sqlite`.

4. **Mandatory Album Ingestion & Consistency Protocol (Lossless & Lossy)**:
   Whenever adding, moving, downloading, or reorganizing new albums into `Lossless/` or `Lossy/`, all AI agents must follow this 8-point checklist:
   1. **Franchise/Artist Umbrella Check**: Check if an existing `~` folder already covers the release (e.g. `THE IDOLM@STER ~`, `Uma Musume ~`). If so, locate the correct subseries folder before placing the album. Never drop albums loose into the franchise root or category root.
   2. **Strict Hierarchy Compliance**: If a subseries pattern exists (e.g., `Song for Prism Series/`, `WINNING LIVE Series/`, `01. Solo/[Character]/`), place the album strictly into its matching tier.
   3. **Consistent Album Folder Naming**:
      - Canonical pattern: `[YYYY.MM.DD] [Artist] - [Title] [Format]` (or franchise standard, e.g. Gakumas: `[Artist] - [Title] [Format]`).
      - Format declaration is mandatory: e.g. `[FLAC]`, `[FLAC 96kHz／24bit]`, `[FLAC+BK]`, `[MP3 320k]`.
   4. **Flat Album Root (Zero Nested Audio)**:
      - All audio files (`.flac`, `.mp3`) must reside directly in the root of the album folder.
      - **FORBIDDEN**: Never leave files inside nested `FLAC/`, `WAV/`, or `MP3/` folders.
      - **PERMITTED SUBFOLDERS**: Only `BK/` (booklet scans) and `Disc 1/`, `Disc 2/` (for multi-disc releases).
   5. **Track Naming & Metadata Integrity**:
      - Track files must follow `01. [Title].[ext]` or `01 - [Artist] - [Title].[ext]`.
      - **FORBIDDEN**: Leaving raw web store download IDs (e.g. mora `1-0007...` or `10-0005...`).
      - All embedded Vorbis/ID3 tags (`TITLE`, `ARTIST`, `ALBUM`, `TRACKNUMBER`) must be filled and match official metadata.
   6. **No Redundant Disc Images / WAVs**:
      - Single uncompressed `.wav` or `.flac` disc images accompanied by `.cue` must be split into standalone tracks (`shnsplit`) and tagged. Delete the full-disc image if split tracks are present to avoid player errors and duplicate entries in MusicBee.
   7. **Zero Junk Policy**:
      - Strip all piracy forum links (`.url`), downloader advertisements (`Read.txt`, `Discord.txt`), and duplicate lowercase artwork (`cover.jpg` when `Cover.jpg` exists).
   8. **Permissions & Catalog Indexing**:
      - Execute `chown -R 100000:100000` and `chmod -R 775` (directories) / `664` (files) on all newly added paths to ensure seamless Windows SMB read/write access.
      - Execute `python3 scripts/update_catalog.py` to refresh `/mnt/hdd-backup/music/catalog.sqlite`.
   9. **Master Zero-Defect Audit Verification**:
      - After every reorganization, ingestion, or tag update, verify that the library maintains 100% Zero-Defect status against all 15 audit parameters in [`docs/music-audit.md`](music-audit.md) via `python3 scripts/generate_music_scorecard.py --write-storage`.
   10. **ReplayGain 2.0 (EBU R128) Volume Normalization**:
      - To eliminate volume discrepancies between modern loudness-war masters (-6 LUFS) and acoustic/streaming masters (-15 LUFS) without mutating raw audio, write non-destructive ReplayGain Vorbis metadata tags (`REPLAYGAIN_TRACK_GAIN`, `REPLAYGAIN_ALBUM_GAIN`) via `metaflac --add-replay-gain`.
      - Raw PCM audio streams MUST remain 100% pure and bit-perfect (verified MD5 matching). Never apply destructive volume scaling or re-encoding.

### Apple Music (`gamdl`) Ingestion & `.m4a` Classification
- **Staging**: gamdl on `media-hosts` writes to `/mnt/hdd-backup/music/_gamdl-incoming/` (`Artist/Album/NN Title.m4a` + `.lrc` + `Cover.jpg`). Files are reorganized into `Lossless/` or `Lossy/` per the rules above; never left in staging.
- **Decide by codec, not by extension.** `.m4a` is only a container. Check with `ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 <file>`:
  - `aac` (gamdl default `aac-web`, lossy) -> **`Lossy/`**, format tag `[AAC 256k]` (use the real bitrate; `[AAC WEB]` if unknown).
  - `alac` (Apple Lossless) -> `Lossless/` is valid, format tag `[ALAC]` (add `96kHz／24bit` etc. if Hi-Res). Some existing `.m4a` files under `Lossless/` are legitimate Apple Music WEB-DL ALAC rips: do NOT treat them as misplaced or convert them.
- **Never transcode AAC -> FLAC/ALAC** to pass it off as lossless. It adds no quality, bloats size 3-5x, and falsifies the library's quality tiers (violates Zero-Defect intent). Keep AAC as-is in `Lossy/`.
- Audit hint: any `aac` stream found under `Lossless/` (or `alac`/`flac` under `Lossy/`) is a misclassification to flag.

---

## 2. Uma Musume (`Anime/Uma Musume ~`) Standard

All releases in `Uma Musume ~` are grouped into **7 canonical subseries folders** based on official Lantis discography lines:

```
Anime/Uma Musume ~/
├── 01. WINNING LIVE Series/                     (Smartphone game vocal & BGM albums 01..N)
├── 02. ANIMATION DERBY Series/                  (TV Anime Season 1, Season 2 & 3 releases)
├── 03. STARTING GATE Series/                   (Early franchise vocal & unit collection singles 01..12)
├── 04. SOLO VOCAL TRACKS/                      (Special event solo vocal compilation albums Vol.1..N)
├── 05. UMAYURU & UMAYON/                       (Short anime spinoff singles and mini-albums)
├── 06. Singles, OST & Other/                   (Films, ONA ROAD TO THE TOP, Cinderella Gray, web singles)
└── 07. Compilations/                           (Audiophile & special editions: Astell&Kern Special CD)
```
- Folder naming within subseries: Preserve chronological release dates `[YYYY.MM.DD] ... [FLAC]` or `[FLAC 96kHz／24bit]`.
- Always purge whole-disc CD images (`LACM-*.flac`, `LACA-*.flac`) and root cuesheets when individual split tracks are already present to avoid duplicate tracks and cuesheet errors in MusicBee.

---

## 3. THE IDOLM@STER Umbrella (`Anime/THE IDOLM@STER ~/`) Standard

All branches of the Idolmaster franchise reside under `Anime/THE IDOLM@STER ~/`:

```
Anime/THE IDOLM@STER ~/
├── 学園アイドルマスター/
│   ├── 01. Solo/                                   (13 character subfolders, albums strictly named 'Artist - Title [Format]')
│   ├── 01. 花海咲季 (Saki Hanami)/
│   ├── 02. 月村手毬 (Temari Tsukimura)/
│   ├── 03. 藤田ことね (Kotone Fujita)/
│   ├── 04. 有村麻央 (Mao Arimura)/
│   ├── 05. 葛城リーリヤ (Lilja Katsuragi)/
│   ├── 06. 倉本千奈 (China Kuramoto)/
│   ├── 07. 紫雲清夏 (Sumika Shiun)/
│   ├── 08. 篠澤広 (Hiro Shinosawa)/
│   ├── 09. 姫崎莉波 (Rinami Himesaki)/
│   ├── 10. 花海佑芽 (Ume Hanami)/
│   ├── 11. 秦谷美鈴 (Misuzu Hataya)/
│   ├── 12. 十王星南 (Sena Juo)/
│   └── 13. 雨夜燕 (Tsubame Amaya)/
│
│   ├── 02. Duo/                                    (Folder reserved for future duo releases: '[Artist 1・Artist 2] - Title [Format]')
│   ├── 03. Trio/                                   (All 20 trio releases strictly named '[Artist 1・Artist 2・Artist 3] - Title [Format]' with artists sorted alphabetically)
│   └── 04. All Stars & Units/                      (Official units like Begrazia, student combinations, and academy-wide anthems)
│
├── シャイニーカラーズ/                               (THE IDOLM@STER SHINY COLORS - Canonical Option A Hierarchy)
│   ├── 01. WING & Main Game Series/                 (Annual unit CD cycles)
│   │   ├── 01. BRILLI@NT WING (2018)/               (01..05 Spread the Wings!!, etc.)
│   │   ├── 02. FR@GMENT WING (2019)/                (01..06 Ambitious Eve, etc.)
│   │   ├── 03. GR@DATE WING (2020)/                 (01..07 シャイノグラフィ, etc.)
│   │   ├── 04. L@YERED WING (2021)/                 (01..08 Resonance⁺, etc.)
│   │   ├── 05. PANOR@MA WING (2022)/                (01..08 虹の行方, etc.)
│   │   ├── 06. CANVAS (2023)/                       (01..08)
│   │   └── 07. ECHOES (2024)/                       (01..09)
│   ├── 02. Song for Prism Series/                   (Game Song for Prism / シャニソン singles 2024–2026)
│   ├── 03. Anime Series/                            (TV Anime S1 & S2 OP/ED, Theme Album, Halloween)
│   ├── 04. COLORFUL FE@THERS Series/                (Solo/Unit Album Series: Stella, Luna, Sol, SHHis, CoMETIK)
│   └── 05. Synthe-Side & Collaborations/            (Synthe-Side 01..03, Event singles)
│
└── vα-liv/                                         (PROJECT IM@S virtual idol releases, e.g. 上水流宇宙)
```

### Folder Naming Consistency Rules:
1. **Solo Releases**: Must always follow `[Artist] - [Title] [Format]`, e.g. `花海咲季 - Fighting My Way [FLAC 96kHz／24bit]`, `藤田ことね - 世界一可愛い私 [1st Single CD-FLAC]`.
2. **Duo & Trio Releases**: Artists must be listed in **alphabetical order**, followed by title: `[Artist 1・Artist 2・Artist 3] - [Title] [Format]`.
   - Example: `[藤田ことね・花海咲季・月村手毬] - ENDLESS DANCE [FLAC 96kHz／24bit]` (Fujita, Hanami, Tsukimura).
   - Example: `[有村麻央・篠澤広・紫雲清夏] - Howling over the World [FLAC 96kHz／24bit]` (Arimura, Shinosawa, Shiun).
3. **All Stars & Units**: Official unit name or all-stars artist name first: `Begrazia - Star-mine [FLAC 96kHz／24bit]`, `初星学園 - 初 HAJIME [FLAC]`.


### Visual & Metadata Classification Guide for Gakumas

| Release Category | Cover Art Characteristics | Audio & Metadata Traits | Song Examples | Target Folder & Naming |
| :--- | :--- | :--- | :--- | :--- |
| **Birthday Singles** | Birthday celebration artwork: idol in party or warm casual attire (*warm celebratory pastel tones*), holding gifts/cake/flowers. | Released on the idol's birthday. 2 tracks (`[Vocal]`, `[Instrumental]`). | `叶えたい、ことばかり` (Temari), `Wake up!!` (Lilja), `憧れをいっぱい` (China) | `01. Solo/[Character]/[Artist] - [Title] [Format]` |
| **1st Solo (Debut Song)** | Single idol portrait wearing **official Hatsuboshi Gakuen uniform** or debut costume with minimalist/elegant typography. | Character's first debut solo track. Web Hi-Res 96kHz/24bit format. 2 tracks. | `Fighting My Way` (Saki), `Luna say maybe` (Temari), `世界一可愛い私` (Kotone), `Fluorite` (Mao), `白線` (Lilja) | `01. Solo/[Character]/[Artist] - [Title] [Format]` |
| **Physical CD Singles** | Jewel-case CD artwork layout, complete with physical printed booklet (`BK/`), OBI, and EAC rip log (`BNEI-*.log`). | Standard CD-DA **44.1kHz/16-bit** resolution. Contains **6 full tracks** (Solo Song + Solo Ver `初` + Solo Ver `Campus mode!!` + 3 Instrumentals). | `花海咲季 1stシングル「Fighting My Way」[FLAC+BK]` | `01. Solo/[Character]/[Artist] - [Title] [Format]` |
| **Solo Special (True End)** | Dramatic, intense stage illustration (*dynamic stage lighting*, expressive stage pose) marking True End Produce Arc achievement. | Character's second solo song from game. 2 tracks (`[Vocal]`, `[Instrumental]`). | `Boom Boom Pow` (Saki), `アイヴイ` (Temari), `Yellow Big Bang!` (Kotone), `Feel Jewel Dream` (Mao), `コントラスト` (Hiro) | `01. Solo/[Character]/[Artist] - [Title] [Format]` |
| **Solo Updates (2025+)** | Latest SSR stage costume illustrations or periodic story card updates from game cycles. | Digital Web Hi-Res 96kHz/24bit releases. | `Try it now`, `Sweet Magic`, `Top Secret`, `ときめきのソルフェージュ`, `Ride on Beat`, `Kira Kira`, `極光` | `01. Solo/[Character]/[Artist] - [Title] [Format]` |
| **Duo Releases** | Artwork featuring 2 idol characters with stage/thematic interaction. | Performed by 2 characters. Naming format: `[Artist 1・Artist 2] - [Title] [Format]` (alphabetical order). | *(Reserved)* | `02. Duo/[Artist 1・Artist 2] - [Title] [Format]` |
| **Event Songs (Trio Ver)** | Features **3 idol characters** in matching event/seasonal costume theme from the game. | Sung by 4 official Gakumas trios: <br>• Trio 1: Saki, Temari, Kotone<br>• Trio 2: Lilja, China, Rinami<br>• Trio 3: Mao, Sumika, Hiro<br>• Trio 4: Ume, Misuzu, Sena | `ENDLESS DANCE`, `Howling over the World`, `がむしゃらに行こう！`, `ミラクルナナウ(ﾟ∀ﾟ)！`, `古今東西ちょちょいのちょい` | `03. Trio/[Artist 1・Artist 2・Artist 3] - [Title] [Format]` <br>*(Alphabetical artist order mandatory)* |
| **All Stars & Seasons** | Mass ensemble artwork (*all cast ensemble*), Hatsuboshi Gakuen logo, or seasonal event art (beach/summer, fireworks/autumn, halloween, valentine, sakura). | Academy anthem or seasonal festival single performed collectively. | `初 HAJIME`, `Campus mode!!`, `キミとセミブルー`, `冠菊`, `仮装狂騒曲`, `ハッピーミルフィーユ`, `桜フォトグラフ`, `SUPREMACY`, `ナイワ` | `04. All Stars & Units/[Artist] - [Title] [Format]` |
| **Official Units** | Official unit logo and unified stage uniform. | In-game official unit releases. | `Begrazia - Star-mine` | `04. All Stars & Units/[Artist] - [Title] [Format]` |
| **Media Tie-in (Manga)** | Comic/manga style cover, tankobon art with booklet scans. | Official manga tie-in bundled CD. | `GOLD RUSH (1) オリジナルCD「かちドキ」` | `01. Solo/[Character]/[Artist] - [Title] [Format]` |

---

## 4. Gochuumon wa Usagi Desu ka (`Anime/ご注文はうさぎですか？？ (Gochuumon wa Usagi Desu ka) ~`) Standard

All releases in `ご注文はうさぎですか？？ ~` are organized into **3 canonical subseries folders**:

```
Anime/ご注文はうさぎですか？？ (Gochuumon wa Usagi Desu ka) ~/
├── 01. Theme Songs (OP & ED)/                     (TV Anime OP & ED singles for Season 1, ??, BLOOM)
├── 02. Character Song Series/                     (Unit singles, Character Song Series 01..05, cup of chino, 10th Anniversary)
└── 03. Albums & Compilations/                     (ごちうさブレンド, order the songs [WEB-FLAC], メインテーマリアレンジ)
```

### Essential Rules for GochiUsa Releases:
1. **Never Nest Audio in `FLAC/` or `WAV/`**: Audio files (`.flac`) must reside directly in the root of the album folder. Only artwork scans may reside in a `BK/` subfolder.
2. **Split Whole-Disc Images**: Uncompressed single-file `.wav` or `.flac` disc images with `.cue` sheets must always be split into individual FLAC tracks (`shnsplit -o flac -f <cue> <audio>`) with proper vorbis tags embedded.
3. **No Raw mora IDs**: Always rename raw store IDs (`1-0007...`, `10-0005...`) to clean numbered track titles (`01. [Title].flac`).
4. **Zero Piracy/Tracker Junk**: Remove all `.url` shortcuts, forum promo `.txt` files (`Read.txt`, `Discord.txt`), and duplicate artwork.

---

## 5. Universal Music Folder Reorganization Framework (Standard Operating Procedure)

To ensure long-term consistency across all music curation tasks (in `/mnt/hdd-backup/download/`, staging `Torrent/`, or master `Lossless/`), all operations must strictly adhere to the following **5-Step Standard Framework**:

```
[Auditing & Metadata Extraction] ──> [Canonical Classification] ──> [Sanitization & Pure Naming] ──> [Dry-Run Plan & User Approval] ──> [Server-Side Execution]
```

### 1. Hierarchy & Folder Naming Rules (Strict)

Every album or single must be placed strictly according to the scheme:
```
[Category]/[Artist Folder] ~/[Album Folder]/
```

#### A. Category Selection (`[Category]`)
The top-level category must strictly be one of:
- `Anime/`: Anime OSTs, character songs, and official multimedia franchise umbrellas (e.g. `THE IDOLM@STER ~`, `Uma Musume ~`, `Gochuumon wa Usagi Desu ka ~`).
- `Vtuber/`: Virtual talents and VTuber agencies (Hololive, Nijisanji, Kamitsubaki Studio, RK Music, VSPO, etc.).
- `Vocaloid/`: VOCALOID, CeVIO, or Synthesizer V releases (Hatsune Miku, Kikuo, DECO*27, etc.).
- `Doujinshi/`: Indie circles, doujin artists, and non-commercial/M3 releases (e.g. `nayuta ~`, `Room97 ~`, `＊Luna ~`).
- `J-Pop/`: General commercial Japanese pop/rock artists outside anime/vtuber/vocaloid umbrellas.
- `Global/`: Non-Japanese artists (Western, K-Pop, soundtrack, etc.).

#### B. Artist & Franchise Folder Naming (`[Artist Folder] ~`)
- **Mandatory Tilde Suffix**: All artist, circle, and franchise directories **MUST** end with a tilde space (` ~`).
- **Standard Artists (Non-Franchise)**:
  - Japanese Artists: Must follow `Romaji (Kanji/Hira/Kana) ~` (e.g. `Aoki Hina (青木陽菜) ~`, `Natsunose (ナツノセ) ~`, `Hoshimachi Suisei (星街すいせい) ~`, `ZUTOMAYO (ずっと真夜中でいいのに。) ~`).
  - Latin/Western Artists: Official name without parentheses (e.g. `YOASOBI ~`, `Aimer ~`, `Eve ~`, `Taylor Swift ~`).
  
#### C. The Canonical Franchise Umbrellas (`Anime/[Franchise] ~/`)
All sub-units, character songs, soundtracks, and individual idols under multimedia, anime, or gaming franchises are **STRICTLY FORBIDDEN** from floating loose in `Anime/`. All of them **MUST** be nested under their canonical **Romaji / Global Text (Kanji/Hira/Kana) ~** umbrella:

1. `Anime/THE IDOLM@STER (アイドルマスター) ~/` (Gakumas, Shiny Colors, Cinderella Girls, Million Live, vα-liv)
2. `Anime/Uma Musume (ウマ娘) ~/` (WINNING LIVE, ANIMATION DERBY, SOLO VOCAL, etc.)
3. `Anime/BanG Dream! (バンドリ！) ~/` (MyGO!!!!!, Ave Mujica, Roselia, Poppin'Party, Pastel＊Palettes, Mugendai Mewtype, etc.)
4. `Anime/Love Live! (ラブライブ！) ~/` (Liella!, Aqours, Nijigaku, Hasunosora, Muse)
5. `Anime/D4DJ ~/` (Happy Around!, Peaky P-key, Photon Maiden, Merm4id, Rondo, Lyrical Lily)
6. `Anime/IDOLY PRIDE (アイドリープライド) ~/` (Sunny Peace, Tsuki no Tempest, TRINITYAiLE, LizNoir)
7. `Anime/Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~/`
8. `Anime/Girls Band Cry (ガールズバンドクライ) ~/` (Togenashi Togeari, Diamond Dust)
9. `Anime/Gochuumon wa Usagi Desu ka (ご注文はうさぎですか？？) ~/`
10. `Anime/Tokyo 7th Sisters (Tokyo 7th シスターズ) ~/` (777☆SISTERS, Le☆S☆Ca, The QUEEN of PURPLE)
11. `Anime/Denonbu (電音部) ~/`
12. `Anime/Ongeki (ONGEKI／オンゲキ) ~/`
13. `Anime/Princess Connect! Re：Dive (プリンセスコネクト！ Re：Dive) ~/`
14. `Anime/Blue Archive (ブルーアーカイブ) ~/`
15. `Anime/Project SEKAI (プロジェクトセカイ) ~/` (Leo/need, MORE MORE JUMP!, Vivid BAD SQUAD, Wonderlands×Showtime, 25-ji)
16. `Anime/Arknights (アークナイツ／塞壬唱片-MSR) ~/`
17. `Anime/Heaven Burns Red (ヘブンバーンズレッド) ~/` (She is Legend, Karafuru)
18. `Anime/Azur Lane (アズールレーン) ~/`
19. `Anime/Wuthering Waves (鳴潮) ~/`
20. `Anime/Macross Delta (マクロスΔ) ~/` (Walküre)
21. `Anime/Sound! Euphonium (響け！ユーフォニアム) ~/`
22. `Anime/Revue Starlight (少女☆歌劇 レヴュースタァライト) ~/`
23. `Anime/K-ON! (けいおん！) ~/` (Ho-kago Tea Time)
24. `Anime/Fate Series (Fateシリーズ) ~/`
25. `Anime/The Quintessential Quintuplets (五等分の花嫁) ~/`
26. `Anime/Sword Art Online (ソードアート・オンライン) ~/`

> [!IMPORTANT]
> **Strict Naming Standard & Anti-Split Policy**:
> 1. Directory names at root **MUST BE CONSISTENT**: `Romaji/Global (Original Japanese) ~`. Never reverse this order.
> 2. All legacy variations (e.g. `Arknight ~` vs `アークナイツ ~`, `DENONBU ~` vs `電音部 ~`, `GIRLS BAND CRY ~` vs `ガールズバンドクライ ~`) **MUST be merged** into the canonical names above, and outdated folders pruned.

#### D. Album / Single Folder Naming (`[Album Folder]`)
- **Pure Album Name Rule**:
  - **NO release date tags**: strip `[YYYY.MM.DD]`, `[YYYY-MM-DD]`, `[YYMMDD]`.
  - **NO release years in parentheses**: strip `(2025)`, `(2026)`.
  - **NO audio format, bitrate, or source tags**: strip `[FLAC]`, `[FLAC 24bit/48kHz]`, `[FLAC 96kHz／24bit]`, `[WEB-FLAC]`, `[Hi-Res]`, `[1st Single CD-FLAC]`, `[MP3 320k]`.
  - **NO duplicate artist name prefixes** in album names when already located inside an artist directory (unless official self-titled releases).
  - **Result**: Clean, pure album/single title.
    - *Incorrect*: `[2026.05.13] 青木陽菜 1stミニアルバム「BLAZE」[WEB-FLAC 24bit/48kHz]`
    - *Correct*: `BLAZE` (or `1stミニアルバム「BLAZE」` if the official commercial title includes the mini-album prefix).
    - *Incorrect*: `(2024.11.20) 最強未来衝動 [FLAC]`
    - *Correct*: `最強未来衝動`

---

### 2. Standard 5-Step Execution Workflow

1. **Step 1: Server-Side Vorbis Tag Metadata Extraction**:
   - Never trust legacy directory names (which often stem from broken auto-unrar/unpack pipelines like `100 ~`, `1stBLAZEFLAC ~`).
   - Extract `ARTIST`, `ALBUM`, and `TITLE` directly from audio files (`.flac`) via server-side tools (`metaflac` or `mutagen`).

2. **Step 2: Category Mapping & Normalized Naming**:
   - Match artist names against alias databases and `configs/music_grouping_rules.json`.
   - Convert Japanese artist names to canonical format: `Romaji (Original) ~`.
   - Sanitize album names from date/codec regex into `Pure Album Name`.

3. **Step 3: Dry-Run Plan Generation (`reorganize_plan.json`)**:
   - The script outputs a JSON mapping source directories (`source_dir`) to target directories (`target_dir`).
   - Validates potential collisions (e.g. duplicate album titles for the same artist).

4. **Step 4: Mandatory User Confirmation (Rule 0)**:
   - Present a clear sample mapping (Before ➔ After) to the user.
   - Report the number of albums to be relocated and re-categorized (e.g. VTubers moving out of `J-Pop/`).
   - **Always await explicit user approval before executing any filesystem mutations (`mv`, `rm`).**

5. **Step 5: Server-Side Background Execution (Rule 2 & 4)**:
   - Run batch filesystem mutations using a detached server-side process (`nohup ... &`).
   - Apply strict Linux permissions: `chown -R 100000:100000` and `chmod -R 775/664`.
   - Prune empty remnant directories.
   - Refresh master catalog via `python3 scripts/update_catalog.py`.

