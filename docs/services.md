## Media Stack

| Service | Purpose | Port | Data location |
|---|---|---|---|
| Jellyfin | Movie/TV/anime streaming + music library (accessed via Feishin/foobar2000 as client, not Jellyfin web UI) | 8096 | `/mnt/hdd-media/videos/{movies,tv,anime}` (1TB Seagate 7200 RPM) + `/mnt/hdd-music/music` (2TB WD Green). |
| Nextcloud | File sync/storage | 8080 | `/mnt/hdd-cloud/nextcloud` — 1TB Toshiba 2.5" HDD (sdb), 765GB free space available. Uses shared Postgres + Redis. |
| Komga | Primary manga/comic/BD reader | 25600 | `/mnt/hdd-media/manga-reader` — lightweight optimized WebP library auto-generated and mirrored by `manga-optimizer.service` on 7200 RPM Barracuda. Deployed 2026-09-13 (`configs/docker-compose/komga.yml`). Replaced Kavita. |
| Navidrome | Modern self-hosted music server & Subsonic streaming API | 4533 | Ultra-lightweight Go music streamer. Zero server transcoding load, native FLAC/MP3 direct play. Web UI + Subsonic clients (Symfonium, Feishin, Sonixd). Library: `/mnt/hdd-music/music`. Deployed 2026-09-13 (`configs/docker-compose/navidrome.yml`). |
| Feishin | Modern web music player client for Navidrome/Subsonic | 9180 | Minimalist PWA web client with folder tree explorer, playlist management, and dark UI. CPU 0%, RAM ~6.5MB. Deployed 2026-09-13 (`configs/docker-compose/feishin.yml`). |
| StreamVault | Zero server-transcode video streaming (Anime, Movies, TV) with client-side JASSUB WASM subtitle rendering | 8090 | [srytmj/stream-vault](https://github.com/srytmj/stream-vault) — `/mnt/hdd-media/videos` mounted read-only (`/media:ro`), runs alongside Jellyfin. Ultra-lightweight (<30MB RAM, 0% CPU transcode). Deployed 2026-09-13 (`configs/docker-compose/stream-vault.yml`). |

## Storage & Processing Pipelines

| Service / Daemon | Purpose | Host / Runtime | Data Paths |
|---|---|---|---|
| `manga-optimizer.service` | Real-time filesystem watcher + image optimizer. Detects CBZ files in raw master directory, optimizes heavy archives to WebP (max 2048px width, Q85), hardlinks existing WebP archives (0 disk waste), and mirrors folder hierarchy / renames / moves / deletions. | `docker-host` systemd service (`/usr/local/bin/manga-optimizer.py`) | Ingest/Master: `/mnt/hdd-media/manga-raw` (Samba `\\docker-host\manga`) <br> Target/Reader: `/mnt/hdd-media/manga-reader` |