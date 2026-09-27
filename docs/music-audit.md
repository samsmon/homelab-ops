# Master Zero-Defect Music Audit & Library Health

> **Source of Truth** for music library integrity, cleanliness, and format compliance (`Lossless/`, `Lossy/`, `catalog.sqlite`).
> This document updates automatically in real time via systemd timer and on every catalog refresh.

---

### 🏆 Live Master Audit Scorecard

```
======================================================================
MASTER ZERO-DEFECT AUDIT (LIVE SYSTEM SCORECARD)
Target Host : docker-host (192.168.18.225)
Storage Root: /mnt/hdd-backup/music/
Timestamp   : 2026-09-27 13:59:13
======================================================================
Disk Usage  : 171G free (91% used)

--- 1. LOSSLESS LIBRARY AUDIT (/mnt/hdd-backup/music/Lossless) ---
Total Directories         : 6,592
Total Files               : 28,602
Bit-Perfect FLAC Tracks   : 22,759  (100% FLAC)
Non-FLAC Audio Files      : 0       (0 WAV, 0 AIFF, 0 WV, 0 MP3, 0 M4A, 0 AAC)
CUE Sheets (.cue)         : 0       (100% Standalone split tracks)
Clutter Files (.log/.url) : 0       (100% Clean from logs/ads)
In-album M3U Playlists    : 0       (100% Centralized Master Lossless.m3u8)
Duplicate Cover Art       : 0       (100% Single official Cover.jpg per album)
Case Collisions (SMB/NTFS): 0       (100% Safe for Windows clients)
Artists Missing Tilde (~) : 0       (100% of 1,207 artists ending with ~)
Loose Audio in Roots      : 0       (100% Located inside official album folders)
Empty Directories         : 0       (100% Clean from ghost folders)
Album Format Noise Tags   : 0       (0 [FLAC], 0 [WEB-FLAC], 0 [Hi-Res])
Album Raw Date Prefixes   : 0       (0 YYYY.MM.DD date prefixes)

--- 2. LOSSY COMPANION LIBRARY AUDIT (/mnt/hdd-backup/music/Lossy) ---
Lossy Audio Tracks        : 2,357   (MP3, M4A, AAC)
FLAC Files in Lossy       : 0       (100% Clean, all FLAC rescued to Lossless)
Clutter Files in Lossy    : 0       (0 .cue, 0 .log, 0 .htm)
Empty Dirs in Lossy       : 0       (0 Empty folders)
Case Collisions in Lossy  : 0       (100% Safe for Windows clients)

--- 3. MASTER CATALOG & PLAYLISTS ---
catalog.sqlite Tracks     : 25,123  (Lossless: 22,759 | Lossy: 2,364)
Lossless.m3u8 Tracks      : 22,759  (100% FLAC Bit-Perfect)
Lossy.m3u8 Tracks         : 2,364
Samba Daemon Status       : Active & Serving LAN
Permissions Standard      : 775 (Directories) / 664 (Files) root:root
Total Defects Detected    : 0 (ZERO-DEFECT STATUS: VERIFIED PASS)
======================================================================
```

---

## 1. The 15 Zero-Defect Audit Parameters

All parameters below enforce a strict **Zero-Defect Tolerance (Defects = 0)**:

| No | Audit Parameter | Target | Description & Validation |
| :---: | :--- | :---: | :--- |
| **1** | **Bit-Perfect FLAC** | 100% | All audio files in `Lossless/` must be pure bit-perfect `.flac`. |
| **2** | **Non-FLAC Audio in Lossless** | **0** | No WAV, AIFF, WV, MP3, M4A, AAC, APE, or Tak allowed in `Lossless/`. Raw/lossy formats must be transcoded or moved to `Lossy/`. |
| **3** | **CUE Sheets** | **0** | All `.cue` sheets must be split into standalone tracks and deleted to prevent duplicate entries in media players. |
| **4** | **Clutter Files** | **0** | Zero clutter files allowed (.log, .accurip, .html, .url, .ini, Read.txt piracy ads, etc.). |
| **5** | **In-album M3U Playlists** | **0** | No local in-album `.m3u`/`.m3u8` ripper playlists (only master root playlists `Lossless.m3u8` and `Lossy.m3u8` are permitted). |
| **6** | **Duplicate Cover Art** | **0** | Every album folder must contain exactly one canonical artwork: `Cover.jpg`. No large uncompressed `cover.png` or duplicate image files. |
| **7** | **Case Collisions (SMB/NTFS)** | **0** | No case-insensitive filename or folder collisions (e.g. `Cover.jpg` vs `cover.jpg`) to ensure seamless Windows SMB compatibility. |
| **8** | **Artists Missing Tilde (~)** | **0** | Every artist or franchise umbrella directory in category roots must end with a tilde space (` ~`), e.g., `BanG Dream! (バンドリ！) ~`. |
| **9** | **Loose Audio in Roots** | **0** | No audio files floating loose in category roots or franchise roots without an official album parent directory. |
| **10** | **Empty Directories** | **0** | Total elimination of empty folders ("ghost directories"). |
| **11** | **Album Format Noise Tags** | **0** | Album folder names must be clean titles; forbidden to contain codec tags like `[FLAC]`, `[WEB-FLAC]`, `(Hi-Res)`, `24bit/96kHz`, etc. |
| **12** | **Album Raw Date Prefixes** | **0** | Album folder names must not start with raw date prefixes `YYYY.MM.DD`. |
| **13** | **FLAC in Lossy** | **0** | Zero FLAC files misplaced in `Lossy/`. All FLAC tracks must be rescued to `Lossless/`. |
| **14** | **Lossy Clutter Files** | **0** | The `Lossy/` directory must be pristine and clean of clutter (.cue, .log, .htm, duplicate files). |
| **15** | **Samba & Permissions** | 775/664 | All directories set to 775, files set to 664, ownership `root:root` (mapped via Samba to SMB users). |

---

## 2. Real-Time Update Mechanism

1. **Automatic Trigger on Ingestion / Catalog Refresh**:
   - The script `/mnt/hdd-backup/music/scripts/update_catalog.py` automatically executes this generator whenever the SQLite database is re-indexed.
2. **Systemd Automation (Periodic Background Verification)**:
   - Executed via `homelab-music-audit.timer` every 6 hours and on system boot on `docker-host`.
   - The Markdown scorecard on storage `/mnt/hdd-backup/music/AUDIT_SCORECARD.md` is accessible live via:
     - **Windows SMB**: `\\docker-host\hdd-backup\music\AUDIT_SCORECARD.md`
     - **FileBrowser Web UI**: `http://192.168.18.225:8085` (under `HDD-Backup/music/AUDIT_SCORECARD.md`).
3. **Manual Trigger**:
   ```bash
   python3 /mnt/hdd-backup/music/scripts/generate_music_scorecard.py --all
   ```

*Last Updated: 2026-09-26 20:48:02*
