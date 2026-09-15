# Services Registry

> Every running service should have an entry here. Update when adding, removing, or changing a service.

## Infrastructure

| Service | Purpose | Port | Config file |
|---|---|---|---|
| Homelab Cockpit | Owner POV Dashboard & Real-time Homelab Monitor | 8050 | `/mnt/homelab_projects/homelab-dashboard/docker-compose.yml` (repo: [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard)) |
| Homelab IdP | Identity Provider (SSO, OIDC Provider, Forward Auth, Credential Vault) | 8300 | `/mnt/homelab_projects/homelab-idp/docker-compose.yml` (repo: [srytmj/homelab-idp](https://github.com/srytmj/homelab-idp)) |
| Samba & WSDD | Windows File Explorer LAN file sharing (all 3 HDDs) + auto-discovery | 445, 139, 3702 (wsdd) | Native systemd service `smbd` + `wsdd` on docker-host (`/etc/samba/smb.conf`). Also carries a dedicated `[projects]` share (restricted to `192.168.18.224`/`.227` via `hosts allow`) that exposes `/mnt/homelab_projects` to `dev-host` (LXC 102) — see the T3 Code entry below. |
| Nginx Proxy Manager | Reverse proxy + auto SSL (Let's Encrypt via GUI) | 80, 443 (proxy), 81 (admin UI) | `configs/docker-compose/npm.yml` |
| Tailscale | Remote access mesh VPN, no port forwarding | n/a (WireGuard mesh) | Native apt install on docker-host (not containerized). Node `docker-host` → `100.89.249.96` / `docker-host.taila813af.ts.net`. `--accept-dns=false`. **Not yet installed on `dev-host` (LXC 102)** — needs a Tailscale auth key from the user (admin console), pending. |
| cloudflared | Cloudflare Tunnel connector — outbound-only, publishes services to the internet without opening router ports | n/a (outbound QUIC to Cloudflare edge) | Native apt install on docker-host (systemd service `cloudflared`, `enabled`). Tunnel token set up via Cloudflare Zero Trust dashboard by the user directly — token never stored in this repo. Public hostname routing (which domain → which local port) is configured in the Cloudflare dashboard itself, not tracked here yet. **`t3.suryatmaja.dev` still points at the old `192.168.18.225:9001` and needs manual repointing to `192.168.18.227:9001` after the 2026-09-15 T3 Code migration to `dev-host`.** |
| PostgreSQL (shared) | Multi-database for all projects | 5432 (internal only) | `configs/docker-compose/postgres-redis.yml` |
| Redis (shared) | Caching, per-project key prefix | 6379 (internal only) | `configs/docker-compose/postgres-redis.yml` |
| CapRover | Mini hosting panel — lets friends self-deploy their own web apps (git push → auto build/deploy), auto SSL, per-app resource limits | 3000 (admin) | Deployed after base homelab is stable, see roadmap.md. Requires Docker Swarm mode. |
| MySQL/MariaDB (CapRover-only) | Database for friends'-apps hosted via CapRover | via CapRover One-Click App | **Separate from the shared PostgreSQL/Redis above** — different trust boundary, friends' app code isn't the user's own |

## Web Projects

### Domain: whitearchive.my.id

| Project | Repo | Domain | Port | Notes |
|---|---|---|---|---|
| malas | [srytmj/malas](https://github.com/srytmj/malas) | whitearchive.my.id (subpath/subdomain TBD) | - | Manga library system — tracks reading progress, aggregates latest chapters from multiple sources, manages personal manga collection. Inspired by Kenmei/AniList/MyAnimeList. |
| whitearchive | [srytmj/whitearchive](https://github.com/srytmj/whitearchive) | whitearchive.my.id (TBD) | 3000 | Deployed 2026-09-12 on `whitearchive-hosts` (LXC 101, `192.168.18.226:3000`). Multi-stage Next.js standalone container (`whitearchive`). |
| sso.whitearchive | [srytmj/sso.whitearchive](https://github.com/srytmj/sso.whitearchive) | sso.whitearchive.my.id (assumed) | - | Likely an auth/SSO dependency of whitearchive — confirm deploy order (SSO probably needs to be up before whitearchive) |
| pore-js | [srytmj/pore-js](https://github.com/srytmj/pore-js) | whitearchive.my.id (subpath/subdomain TBD) | - | Custom reader tied into the `malas` project ecosystem — not a general-purpose library like Kavita. Confirmed both are deployed: Kavita is the standalone generic manga/comic server, pore-js is the reader integrated with `malas`. |

### Domain: suryatmaja.dev

| Project | Repo | Domain | Port | Notes |
|---|---|---|---|---|
| filebrowser | [filebrowser/filebrowser](https://github.com/filebrowser/filebrowser) | drive.suryatmaja.dev | 8085 (container `filebrowser`) | Ultra-lightweight Web File Explorer & Google Drive alternative (~14MB RAM, 0% CPU). Directly browses all storage mounts (`/srv` = `/mnt/hdd-cloud`, `/srv/media` = `/mnt/hdd-media`, `/srv/music` = `/mnt/hdd-music`). Zero indexing lag with Samba. |
| portfolio | [srytmj/portofolio](https://github.com/srytmj/portofolio) | suryatmaja.dev | 3080 (internal, container `portofolio`) | **Consolidated 2026-09-13** to `/mnt/homelab_projects/portofolio/`. `docker-compose.yml` committed to [srytmj/portofolio](https://github.com/srytmj/portofolio) itself. SvelteKit static build served by nginx:alpine. **Only public-facing service** — exposed via Cloudflare Tunnel, not Tailscale-only like everything else. Also contains the **blog** (previously its own `srytmj.github.io` repo). Re-fetch this repo before assuming its current contents/structure — it's actively evolving in its own Claude Code session. |
| cloud-computing-docs | [srytmj/cloud-computing-docs](https://github.com/srytmj/cloud-computing-docs) | subdomain of suryatmaja.dev (TBD) | - | **Not yet built** — repo/web app doesn't exist yet, deploy later once created |
| ~~srytmj.github.io (blog)~~ | [srytmj/srytmj.github.io](https://github.com/srytmj/srytmj.github.io) | N/A — not deployed separately | - | **Not deployed as its own service.** Blog content now lives inside the `portfolio` repo instead. |
| homelab-sentinel | [srytmj/homelab-sentinel](https://github.com/srytmj/homelab-sentinel) | N/A (Telegram bot, no domain) | - | Telegram bot (was Discord) — monitoring alerts + interactive queries + management + short QnA. See roadmap and decisions.md. Not a web app. |

| ... | | | | (fill in as more are deployed — 10 personal projects total planned) |

## Media Stack

| Service | Purpose | Port | Data location |
|---|---|---|---|
| Jellyfin | Movie/TV/anime streaming + music library (accessed via Feishin/foobar2000 as client, not Jellyfin web UI) | 8096 | `/mnt/hdd-media/videos/{movies,tv,anime}` (1TB Seagate 7200 RPM) + `/mnt/hdd-music/music` (2TB WD Green). |
| Nextcloud | File sync/storage | 8080 | `/mnt/hdd-cloud/nextcloud` — 1TB Toshiba 2.5" HDD (sdb), 765GB free space available. Uses shared Postgres + Redis. |
| Komga | Primary manga/comic/BD reader | 25600 | `/mnt/hdd-media/manga-reader` — lightweight optimized WebP library auto-generated and mirrored by `manga-optimizer.service` on 7200 RPM Barracuda. Deployed 2026-09-13 (`configs/docker-compose/komga.yml`). Replaced Kavita. |
| Navidrome | Modern self-hosted music server & Subsonic streaming API | 4533 | Ultra-lightweight Go music streamer. Zero server transcoding load, native FLAC/MP3 direct play. Web UI + Subsonic clients (Symfonium, Feishin, Sonixd). Library: `/mnt/hdd-music/music`. Deployed 2026-09-13 (`configs/docker-compose/navidrome.yml`). |
| Feishin | Modern web music player client for Navidrome/Subsonic | 9180 | Minimalist PWA web client with folder tree explorer, playlist management, and dark UI. CPU 0%, RAM ~6.5MB. Deployed 2026-09-13 (`configs/docker-compose/feishin.yml`). |
| StreamVault | Zero server-transcode video streaming (Anime, Movies, TV) with client-side JASSUB WASM subtitle rendering | 8090 | [srytmj/stream-vault](https://github.com/srytmj/stream-vault) — `/mnt/hdd-media/videos` mounted read-only (`/media:ro`), runs alongside Jellyfin. Ultra-lightweight (<30MB RAM, 0% CPU transcode). Deployed 2026-09-13 (`configs/docker-compose/stream-vault.yml`). **Note:** despite the "zero server-side transcode" design, it does still shell out to `ffmpeg` for thumbnail/metadata generation — this caused an OOM crash-loop on 2026-09-14 that took the whole host down (see CHANGELOG). Root-cause fix (concurrency/timeout limits on that ffmpeg call) is tracked in the stream-vault repo itself, not yet merged. |

## Storage & Processing Pipelines

| Service / Daemon | Purpose | Host / Runtime | Data Paths |
|---|---|---|---|
| `manga-optimizer.service` | Real-time filesystem watcher + image optimizer. Detects archives in raw master directory (extracts safely via 7z), optimizes heavy archives to WebP (max 2048px width, Q85), compares sizes to keep the smallest, and mirrors folder hierarchy / renames / moves / deletions. Monitor progress via `watch -c -n 1 python3 /opt/homelab-ops/scripts/manga-status.py` (or use alias `manga-monitor`). | `docker-host` systemd service (`/usr/bin/python3 scripts/manga-optimizer.py`) | Ingest/Master: `/mnt/hdd-media/manga-raw` (Samba `\\docker-host\manga`) <br> Target/Reader: `/mnt/hdd-media/manga-reader` |

## Monitoring

> Overlap check: 5 tools touch "monitoring" — each is scoped to a distinct concern to avoid
> duplication. See the boundary notes below before adding alerting to more than one.

| Service | Purpose | Port | Scope (to avoid overlap) |
|---|---|---|---|
| Scrutiny | HDD health monitoring (S.M.A.R.T.) | - | Drive-specific: Power-On Hours, Reallocated Sectors, temperature, historical SMART trends + failure-prediction alerts — distinct from Netdata's general resource metrics and not an uptime/container tool. **Not yet deployed.** |
| homelab-sentinel (Telegram bot) | Docker container-level monitoring + Telegram alerts, PLUS interactive queries / whitelisted management / short QnA | - | Container health/resource (things Uptime Kuma's URL/TCP checks can't see) — owns Telegram notifications so Uptime Kuma's own alert integration isn't wired to Telegram in parallel. Also the interactive control surface (see decisions.md for the 3-tier capability design + guardrails). |

## Other Self-Hosted Apps

| Service | Purpose | Port | Notes |
|---|---|---|---|
| Syncthing | Continuous P2P file sync between specific devices | 8384 (Web UI), 22000 tcp+udp, 21027 udp | Different from Nextcloud: no central "cloud" browsing/share-links, just keeps folders in sync across devices (including this server). **Deployed 2026-09-11.** Sync data at `/mnt/hdd-cloud/syncthing`. **No login/auth configured** — the GUI is wide open on the LAN; worth setting a GUI username/password later via Settings. |
| Nextcloud | File storage + sharing (cloud-drive style) | 8080 | Central storage, share links, web/mobile access — the "cloud" experience; not redundant with Syncthing (different sync model, see above) |
| Shiori | Bookmark manager | 8081 | **Deployed 2026-09-11.** No admin account pre-created — first-run creates it via the web UI. |
| YOURLS | URL shortener | 8083 | **Deployed 2026-09-11.** Uses a **dedicated MariaDB** (`yourls-mariadb`), not the shared Postgres — YOURLS only officially supports MySQL/MariaDB. `YOURLS_SITE` is set to a `yourls.home.arpa` placeholder until a real domain exists. |
| n8n | Workflow automation | 5678 | **Deployed 2026-09-11.** Uses the shared Postgres (database `n8n`). `N8N_ENCRYPTION_KEY` generated server-side, never printed or committed. No account pre-created — first-run wizard. |
| Alexandrie | Self-hosted notes / knowledge base | 8200 (UI), 8201 (API), 9002 (RustFS S3), 3307 (MySQL) | **Deployed 2026-09-12.** Repo: [Smaug6739/Alexandrie](https://github.com/Smaug6739/Alexandrie). Has its own MySQL 8.0 + RustFS (S3-compatible storage) — separate from the shared Postgres/Redis. RustFS port remapped from default 9000 to 9002 (9000 collides with Portainer on this host). |
| Vaultwarden | Password manager (lightweight Bitwarden-compatible server) | 8222 | Community rewrite in Rust — NOT the official `bitwarden/server`, which is much heavier. **Deployed 2026-09-11.** `SIGNUPS_ALLOWED=true` for now — flip to `false` once accounts are created. |
| Firefly III | Personal finance / budgeting tracker | 8280 | **Deployed 2026-09-12.** Uses the **shared Postgres** (database `firefly`) instead of the app's normally-bundled MariaDB. Also runs a lightweight `firefly_iii_cron` sidecar. Port remapped from upstream default 80 to 8280 (80 is NPM's). |
| Home Assistant | Home automation | - | Deploy once the smart power plug (HA-compatible) arrives |
| Reclip | Self-hosted media downloader (yt-dlp wrapper, web UI) | 8899 | **Deployed 2026-09-12.** Repo: [averygan/reclip](https://github.com/averygan/reclip) — built from source, no pre-built image published. No admin/auth at all — anyone on the LAN can use it, matches the tool's minimal design. |
| LibreSpeed | Self-hosted internet/LAN speed test (open-source Speedtest alternative) | 8082 | Lightweight (PHP+JS). **Deployed 2026-09-11.** No password set on the results/admin page — fine for LAN-only use. |
| VaultS3 | Lightweight S3-compatible object storage | - | **Not yet deployed** — deferred until a real cross-drive home for it exists (see decisions.md). |
| SnapOtter | Self-hosted file-processing toolkit — 200+ tools across image/video/audio/PDF/files (convert, compress, OCR, transcribe). | - | Standing service (has its own Redis job queue for background jobs). Bundles its own Postgres 17 + Redis — do NOT wire to the shared instances. Limit concurrent workers since video transcode/OCR are CPU-heavy on the GPU-less M710q. |
| T3 Code | Agent coding harness (Claude Code, Antigravity/Gemini, etc.) | 9001 | **Migrated 2026-09-15 to its own dedicated LXC — `dev-host` (LXC 102, `192.168.18.227`)** — after repeated stability incidents while it shared `docker-host` with the media/core stack (see CHANGELOG 2026-09-14/15). Root causes found: (1) an unreaped `while true; sleep 5; find ...` background loop in the old `entrypoint.sh` constantly scanning disk for Antigravity binaries — removed, now runs once at startup only; (2) no CPU/memory limit at all, so any host-wide CPU spike (e.g. the stream-vault OOM-loop) starved its git subprocesses into repeated timeouts, leaving agent threads stuck "working" indefinitely. New setup: custom-built image `t3code-custom:latest` (`configs/docker-compose/t3code/Dockerfile` — `node:22-bookworm-slim` + git/ripgrep/curl/jq, no build tooling bloat), `init: true` (proper zombie reaping via `docker-init`), `mem_limit: 11g` / `cpus: 3.5` inside a 12GB/4-core dedicated LXC — so it can never again starve or be starved by the media stack. Existing Claude Code (`.claude`) and Antigravity/T3 (`.t3/userdata/secrets`) auth was migrated to the new instance (selectively — only credentials, not cached logs/thread history/binaries, ~2.3GB of which was excluded) so no re-login was needed; old per-workspace thread state referencing dead `/root/*` paths was intentionally dropped, not carried over. Project files reach `dev-host` via `/workspace`, a host-level CIFS bind mount (see architecture.md) since unprivileged LXC can't reliably do in-container NFS/CIFS mounts itself. **Still pending (needs the user, not an agent):** join `dev-host` to the Tailscale tailnet (needs an auth key from the admin console), and repoint `t3.suryatmaja.dev` in the Cloudflare Zero Trust dashboard from `192.168.18.225:9001` to `192.168.18.227:9001`. |
| Databasus | PostgreSQL backup (PITR, restore verification, notifications) | - | Candidate to **replace** `scripts/backup.sh`'s Postgres piece, not run alongside it. |
| qBittorrent | Torrent client (web UI) | 8480 (WebUI), 6881 (tcp+udp, torrenting) | **Deployed 2026-09-12.** Deployed **without a VPN wrapper** (Gluetun) for now. Downloads go to real HDD at `/mnt/hdd-media/qbittorrent/downloads`. |

## Automation Scripts

> Status: `docker-host` is active and operational. Container health monitoring, status tracking,
> and project auto-deploy are natively managed by **Homelab Cockpit** (`homelab-dashboard`, port 8050),
> superseding standalone host systemd timers. Scripts below remain available as standalone CLI fallbacks.

| Script | Purpose | Schedule | Unit files |
|---|---|---|---|
| `scripts/backup.sh` | Dumps shared PostgreSQL + copies `configs/` to `/mnt/external-storage/backups/<timestamp>`, prunes backups older than 30 days | Daily at 03:00 (+random delay up to 5min) | `configs/systemd/homelab-backup.service` + `.timer` |
| `scripts/health-check.sh` | Checks expected containers are running; auto-restarts any that are down (one restart attempt), logs to `/var/log/homelab-health-check.log` | Every 5 minutes | `configs/systemd/homelab-health-check.service` + `.timer` |
| `scripts/git-auto-deploy.sh` | Polls each project under `/opt/projects/*` for new commits on `main`; on change, `git pull` + `docker compose up -d --build`. Polling instead of a GitHub webhook because the server has no public-facing endpoint (Tailscale-only). Logs to `/var/log/homelab-git-deploy.log` | Every 5 minutes | `configs/systemd/homelab-git-deploy.service` + `.timer` |
