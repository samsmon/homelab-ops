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

---

## 2. Uma Musume (`Anime/Uma Musume ~`) Standard

All releases in `Uma Musume ~` are grouped into **5 canonical subseries folders** based on official Lantis discography lines:

```
Anime/Uma Musume ~/
├── 01. WINNING LIVE Series/                     (Smartphone game vocal & BGM albums 01..N)
├── 02. ANIMATION DERBY Series/                  (TV Anime Season 1, Season 2 & Umayon releases)
├── 03. STARTING GATE Series/                   (Early franchise vocal & unit collection singles)
├── 04. Theatrical & Specials/                  (Films & Web ONA: Shinjidai no Tobira, ROAD TO THE TOP)
└── 05. Compilations/                           (Audiophile & special editions: Astell&Kern Special CD)
```
- Folder naming within subseries: Preserve chronological release dates `[YYYY.MM.DD] ... [FLAC]`.
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
│   │   ├── 06. "CANVAS" (2023)/                     (01..08)
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

| Kategori Rilis | Karakteristik Cover Art | Ciri Audio & Metadata | Contoh Lagu | Folder Penempatan & Naming |
| :--- | :--- | :--- | :--- | :--- |
| **Birthday Singles** | Ilustrasi selebrasi ulang tahun, idol mengenakan pakaian pesta/kasual hangat (*warm celebratory pastel tones*), memegang hadiah/kue/bunga. | Dirilis tepat di tanggal ulang tahun idol. 2 track (`[Vocal]`, `[Instrumental]`). | `叶えたい、ことばかり` (Temari), `Wake up!!` (Lilja), `憧れをいっぱい` (China) | `01. Solo/[Karakter]/[Artist] - [Title] [Format]` |
| **1st Solo (Debut Song)** | Potret tunggal idol mengenakan **seragam sekolah resmi Hatsuboshi Gakuen** atau kostum debut awal dengan tipografi judul lagu minimalis/elegan. | Lagu debut solo pertama karakter. Format Web Hi-Res 96kHz/24bit. 2 track. | `Fighting My Way` (Saki), `Luna say maybe` (Temari), `世界一可愛い私` (Kotone), `Fluorite` (Mao), `白線` (Lilja) | `01. Solo/[Karakter]/[Artist] - [Title] [Format]` |
| **Physical CD Singles** | Artwork cover debut solo yang disesuaikan untuk jewel case CD, dilengkapi buklet cetak fisik (`BK/`), OBI, dan log rip EAC (`BNEI-*.log`). | Audio resolusi CD-DA standar **44.1kHz/16-bit**. Berisi **6 track lengkap** (Solo Song + Solo Ver `初` + Solo Ver `Campus mode!!` + 3 Instrumental). | `花海咲季 1stシングル「Fighting My Way」[FLAC+BK]` | `01. Solo/[Karakter]/[Artist] - [Title] [Format]` |
| **Solo Special (True End)** | Ilustrasi panggung dramatis dan intens (*dynamic stage lighting*, pose panggung ekspresif) yang menandakan pencapaian True End Produce Arc. | Lagu solo kedua karakter dari game. 2 track (`[Vocal]`, `[Instrumental]`). | `Boom Boom Pow` (Saki), `アイヴイ` (Temari), `Yellow Big Bang!` (Kotone), `Feel Jewel Dream` (Mao), `コントラスト` (Hiro) | `01. Solo/[Karakter]/[Artist] - [Title] [Format]` |
| **Solo Updates (2025+)** | Ilustrasi kostum panggung kartu SSR terbaru atau kartu cerita baru dari update game berkala. | Rilis digital Web Hi-Res 96kHz/24bit dengan penamaan folder diawali `[YYYY.MM.DD]`. | `Try it now`, `Sweet Magic`, `Top Secret`, `ときめきのソルフェージュ`, `Ride on Beat`, `Kira Kira`, `極光` | `01. Solo/[Karakter]/[Artist] - [Title] [Format]` |
| **Duo Releases** | Artwork menampilkan 2 karakter idol dengan interaksi/kostum tematik panggung. | Dinyanyikan oleh 2 karakter. Format penamaan: `[Artist 1・Artist 2] - [Title] [Format]` (urutan alfabetis). | *(Reserved)* | `02. Duo/[Artist 1・Artist 2] - [Title] [Format]` |
| **Event Songs (Trio Ver)** | Menampilkan **3 karakter idol sekaligus** dalam satu ilustrasi mengenakan kostum serasi sesuai tema event/musim di dalam game. | Dinyanyikan oleh 4 Trio Resmi Gakumas: <br>• Trio 1: Saki, Temari, Kotone<br>• Trio 2: Lilja, China, Rinami<br>• Trio 3: Mao, Sumika, Hiro<br>• Trio 4: Ume, Misuzu, Sena | `ENDLESS DANCE`, `Howling over the World`, `がむしゃらに行こう！`, `ミラクルナナウ(ﾟ∀ﾟ)！`, `古今東西ちょちょいのちょい` | `03. Trio/[Artist 1・Artist 2・Artist 3] - [Title] [Format]` <br>*(Artis wajib alfabetis)* |
| **All Stars & Seasons** | Artwork massal/seluruh murid (*all cast ensemble*), logo Hatsuboshi Gakuen, atau ilustrasi musiman (pantai/musim panas, kembang api/musim gugur, halloween, valentine, sakura). | Lagu kebangsaan akademi atau single festival musiman yang dibawakan secara kolektif. | `初 HAJIME`, `Campus mode!!`, `キミとセミブルー`, `冠菊`, `仮装狂騒曲`, `ハッピーミルフィーユ`, `桜フォトグラフ`, `SUPREMACY`, `ナイワ` | `04. All Stars & Units/[Artist] - [Title] [Format]` |
| **Official Units** | Logo unit resmi dan busana seragam unit panggung. | Rilis unit resmi dalam game. | `Begrazia - Star-mine` | `04. All Stars & Units/[Artist] - [Title] [Format]` |
| **Media Tie-in (Manga)** | Artwork gaya komik/manga, sampul tankobon, disertai booklet scan. | CD bundling komik resmi. | `GOLD RUSH (1) オリジナルCD「かちドキ」` | `01. Solo/[Karakter]/[Artist] - [Title] [Format]` |

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
