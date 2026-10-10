# Music Library Agent Rules (moved verbatim from CLAUDE.md)

WAJIB dibaca penuh sebelum ingest/download/move/rename/reorganize album di `Lossless/` atau `Lossy/`.

## 🎵 Music Library Standards (`hdd-backup` & `hdd-music`)
Full specifications are recorded in [`docs/music-standards.md`](docs/music-standards.md). ALL AI agents MUST enforce these rules when ingesting, downloading, moving, or reorganizing albums in `Lossless/` or `Lossy/`:

1. **Zero Loose Albums Rule**: Every single album/single must reside inside an official canonical artist or franchise folder ending with `~` (e.g. `Anime/THE IDOLM@STER ~/`, `J-Pop/＊Luna ~/`). Never place loose albums in category roots (`Anime`, `Doujinshi`, `J-Pop`, `Vtuber`, `Vocaloid`, `Global`).
2. **Strict Hierarchy Compliance**: Always inspect and respect established franchise subseries before dropping files. If a franchise has canonical subfolders, new albums MUST be placed in their matching subfolder (e.g. `THE IDOLM@STER ~/シャイニーカラーズ/01. Song for Prism Series/`, `Uma Musume ~/01. WINNING LIVE Series/`, or `Gakumas/01. Solo/[Idol]/`). Never leave unparented albums at the franchise root.
3. **Consistent Album Folder Naming**:
   - Universal pattern: `[YYYY.MM.DD] [Artist] - [Title] [Format]` (or franchise-specific convention like Gakumas `[Artist] - [Title] [Format]`).
   - Format tag is mandatory: e.g. `[FLAC]`, `[FLAC 96kHz／24bit]`, `[FLAC+BK]`, `[MP3 320k]`.
4. **Flat Album Root (Zero Nested Audio)**:
   - Audio tracks (`.flac`, `.mp3`) must always sit directly in the album folder. Never create nested `FLAC/`, `WAV/`, or `MP3/` folders. Only `BK/` (booklet scans) and `Disc 1/`, `Disc 2/` (for multi-disc releases) are permitted subdirectories.
5. **Track Naming & Metadata Integrity**:
   - Track files must follow `01. [Title].[ext]` or `01 - [Artist] - [Title].[ext]`. Never leave raw store IDs (mora `1-0007...`) or unnamed tracks. Embedded Vorbis/ID3 tags (`TITLE`, `ARTIST`, `ALBUM`, `TRACKNUMBER`) must be filled and accurate.
6. **No Redundant Disc Images / WAVs**:
   - Split single-file WAV/FLAC images with CUE into individual standalone tracks. Delete redundant whole-disc images when split tracks exist.
7. **Windows SMB Safe Naming**: Never use characters forbidden in Windows NTFS/FAT (`\ / : * ? " < > |`) in folder or file names. Use full-width equivalents (e.g. `＊` instead of `*`, remove colons `:` or use full-width `：`) to prevent Samba 8.3 DOS name mangling (`_FCR9Q~X`, `_P6X4P~L`).
8. **Zero Junk Policy**: Strip piracy forum links (`.url`), downloader `.txt` ads (`Read.txt`, `Discord.txt`, etc.), and duplicate lowercase cover files (`cover.jpg` when `Cover.jpg` exists).
9. **Ownership & Master Catalog**:
   - Apply `chown -R 100000:100000` and `chmod -R 775` (dirs) / `664` (files) on new additions so SMB users have immediate access.
   - Always run `python3 /mnt/hdd-backup/music/scripts/update_catalog.py` (or repository `scripts/update_catalog.py`) to refresh `catalog.sqlite`.
10. **Universal Reorganization Framework (Pure Album & Romaji Artist)**:
    - Follow [`docs/music-standards.md#5-universal-music-folder-reorganization-framework-standard-operating-procedure`](docs/music-standards.md#5-universal-music-folder-reorganization-framework-standard-operating-procedure) for every batch cleanup.
    - **Artist Folder**: Japanese names must strictly follow `Romaji (Kanji/Hira/Kana) ~` (e.g. `Aoki Hina (青木陽菜) ~`).
    - **Album Folder**: Must be pure album title without date tags (`[YYYY.MM.DD]`), without years `(2025)`, and without audio codecs/bitrates (`[FLAC 24bit/48kHz]`, `[WEB-FLAC]`).
11. **Canonical Franchise Umbrellas & Anti-Split Policy**:
    - Multimedia/anime/game releases MUST reside inside their designated umbrella in `Anime/` using strictly `Romaji/Global (Japanese Text) ~` format (e.g. `THE IDOLM@STER (アイドルマスター) ~`, `Uma Musume (ウマ娘) ~`, `BanG Dream! (バンドリ！) ~`, `Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~`, `Girls Band Cry (ガールズバンドクライ) ~`, `Denonbu (電音部) ~`, `Arknights (アークナイツ／塞壬唱片-MSR) ~`, dll.).
    - Never allow fragmented split folders (e.g. `Arknight ~` vs `アークナイツ ~`, `DENONBU ~` vs `電音部 ~`). Always merge into the canonical `Romaji (Japanese) ~` folder defined in [`docs/music-standards.md`](docs/music-standards.md).

