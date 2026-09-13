# Services Registry

> Every running service should have an entry here. Update when adding, removing, or changing a service.

## Infrastructure

| Service | Purpose | Port | Config file |
|---|---|---|---|
| Homelab Cockpit | Owner POV Dashboard & Real-time Homelab Monitor | 8050 | `/mnt/homelab_projects/homelab-dashboard/docker-compose.yml` (repo: [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard)) |
| Samba & WSDD | Windows File Explorer LAN file sharing (all 3 HDDs) + auto-discovery | 445, 139, 3702 (wsdd) | Native systemd service `smbd` + `wsdd` on docker-host (`/etc/samba/smb.conf`) |
| Nginx Proxy Manager | Reverse proxy + auto SSL (Let's Encrypt via GUI) | 80, 443 (proxy), 81 (admin UI) | `configs/docker-compose/npm.yml` |
| Tailscale | Remote access mesh VPN, no port forwarding | n/a (WireGuard mesh) | Native apt install on docker-host (not containerized). Node `docker-host` → `100.89.249.96` / `docker-host.taila813af.ts.net`. `--accept-dns=false`. |
| cloudflared | Cloudflare Tunnel connector — outbound-only, publishes services to the internet without opening router ports | n/a (outbound QUIC to Cloudflare edge) | Native apt install on docker-host (systemd service `cloudflared`, `enabled`). Tunnel token set up via Cloudflare Zero Trust dashboard by the user directly — token never stored in this repo. Public hostname routing (which domain → which local port) is configured in the Cloudflare dashboard itself, not tracked here yet. |
| PostgreSQL (shared) | Multi-database for all projects | 5432 (internal only) | `configs/docker-compose/postgres-redis.yml` |
| Redis (shared) | Caching, per-project key prefix | 6379 (internal only) | `configs/docker-compose/postgres-redis.yml` |
| CapRover | Mini hosting panel — lets friends self-deploy their own web apps (git push → auto build/deploy), auto SSL, per-app resource limits | 3000 (admin) | Deployed after base homelab is stable, see roadmap.md. Requires Docker Swarm mode. |
| MySQL/MariaDB (CapRover-only) | Database for friends'-apps hosted via CapRover | via CapRover One-Click App | **Separate from the shared PostgreSQL/Redis above** — different trust boundary, friends' app code isn't the user's own |

## Web Projects

### Domain: whitearchive.my.id

| Project | Repo | Domain | Port | Notes |
|---|---|---|---|---|
| malas | [srytmj/malas](https://github.com/srytmj/malas) | whitearchive.my.id (subpath/subdomain TBD) | - | Manga library system — tracks reading progress, aggregates latest chapters from multiple sources, manages personal manga collection. Inspired by Kenmei/AniList/MyAnimeList. |
| whitearchive | [srytmj/whitearchive](https://github.com/srytmj/whitearchive) | whitearchive.my.id (TBD) | 3000 | Deployed 2026-09-12 on `apps-host` (LXC 101, `192.168.18.226:3000`). Multi-stage Next.js standalone container (`whitearchive`). |
| sso.whitearchive | [srytmj/sso.whitearchive](https://github.com/srytmj/sso.whitearchive) | sso.whitearchive.my.id (assumed) | - | Likely an auth/SSO dependency of whitearchive — confirm deploy order (SSO probably needs to be up before whitearchive) |
| pore-js | [srytmj/pore-js](https://github.com/srytmj/pore-js) | whitearchive.my.id (subpath/subdomain TBD) | - | Custom reader tied into the `malas` project ecosystem — not a general-purpose library like Kavita. Confirmed both are deployed: Kavita is the standalone generic manga/comic server, pore-js is the reader integrated with `malas`. |

### Domain: suryatmaja.dev

| Project | Repo | Domain | Port | Notes |
|---|---|---|---|---|
| filebrowser | [filebrowser/filebrowser](https://github.com/filebrowser/filebrowser) | drive.suryatmaja.dev | 8085 (container `filebrowser`) | Ultra-lightweight Web File Explorer & Google Drive alternative (~14MB RAM, 0% CPU). Directly browses all storage mounts (`/srv` = `/mnt/hdd-cloud`, `/srv/media` = `/mnt/hdd-media`, `/srv/music` = `/mnt/hdd-music`). Zero indexing lag with Samba. |
| portfolio | [srytmj/portofolio](https://github.com/srytmj/portofolio) | suryatmaja.dev | 3080 (internal, container `portofolio`) | **Consolidated 2026-09-13** to `/mnt/homelab_projects/portofolio/` (was split across two divergent checkouts — the original `/opt/projects/portfolio/` and a newer clone Gemini made under the dashboard's `GIT_PROJECTS_ROOT` convention). `docker-compose.yml` was only ever a local file on the server, never committed to the actual GitHub repo — that gap broke the homelab dashboard's pull-and-redeploy feature ("no configuration file provided"). Fixed by committing `docker-compose.yml` to [srytmj/portofolio](https://github.com/srytmj/portofolio) itself, and renamed the container from `yorha-portfolio` to `portofolio` to match the repo's actual name/the new folder convention. SvelteKit static build served by nginx:alpine. **Only public-facing service** — exposed via Cloudflare Tunnel, not Tailscale-only like everything else. Now also contains the **blog** (previously its own `srytmj.github.io` repo — see below, that's no longer deployed separately). Has a hidden page that itself IS the dashboard (custom-built, replaces the separate Homepage/gethomepage.dev plan) — lists hrefs to every homelab service by its Tailscale subdomain, an easter egg only the owner can actually reach. Re-fetch this repo before assuming its current contents/structure — it's actively evolving in its own Claude Code session. |
| cloud-computing-docs | [srytmj/cloud-computing-docs](https://github.com/srytmj/cloud-computing-docs) | subdomain of suryatmaja.dev (TBD) | - | **Not yet built** — repo/web app doesn't exist yet, deploy later once created |
| ~~srytmj.github.io (blog)~~ | [srytmj/srytmj.github.io](https://github.com/srytmj/srytmj.github.io) | N/A — not deployed separately | - | **Not deployed as its own service.** Blog content now lives inside the `portfolio` repo instead — see the `portfolio` entry above. If this changes, re-check the `portfolio` repo for current state before assuming this is still accurate. |
| homelab-sentinel | [srytmj/homelab-sentinel](https://github.com/srytmj/homelab-sentinel) | N/A (Telegram bot, no domain) | - | Telegram bot (was Discord) — monitoring alerts + interactive queries + management + short QnA. See roadmap and decisions.md. Not a web app. |

| ... | | | | (fill in as more are deployed — 10 personal projects total planned) |

## Media Stack

| Service | Purpose | Port | Data location |
|---|---|---|---|
| Jellyfin | Movie/TV/anime streaming + music library (accessed via Feishin/foobar2000 as client, not Jellyfin web UI) | 8096 | `/mnt/hdd-media/jellyfin/{movies,tv,anime}` (1TB HDD) + `/mnt/hdd-music/jellyfin/music` (2TB HDD, 717GB live collection relocated 2026-09-13). |
| Nextcloud | File sync/storage | 8080 | `/mnt/hdd-cloud/nextcloud` — real HDD (sdd), 779GB free space available. Uses shared Postgres + Redis. |
| Komga | Primary manga/comic/BD reader | 25600 | `/mnt/hdd-media/manga-reader` — lightweight optimized WebP library auto-generated and mirrored by `manga-optimizer.service`. Deployed 2026-09-13 (`configs/docker-compose/komga.yml`). Replaced Kavita. |

## Storage & Processing Pipelines

| Service / Daemon | Purpose | Host / Runtime | Data Paths |
|---|---|---|---|
| `manga-optimizer.service` | Real-time filesystem watcher + image optimizer. Detects CBZ files in raw master directory, optimizes heavy archives to WebP (max 2048px width, Q85), hardlinks existing WebP archives (0 disk waste), and mirrors folder hierarchy / renames / moves / deletions. | `docker-host` systemd service (`/usr/local/bin/manga-optimizer.py`) | Ingest/Master: `/mnt/hdd-media/manga-raw` (Samba `\\docker-host\manga`) <br> Target/Reader: `/mnt/hdd-media/manga-reader` |

## Monitoring

> Overlap check: 5 tools touch "monitoring" — each is scoped to a distinct concern to avoid
> duplication. See the boundary notes below before adding alerting to more than one.

| Service | Purpose | Port | Scope (to avoid overlap) |
|---|---|---|---|
| Scrutiny | HDD health monitoring (S.M.A.R.T.) | - | Drive-specific: Power-On Hours, Reallocated Sectors, temperature, historical SMART trends + failure-prediction alerts — distinct from Netdata's general resource metrics and not an uptime/container tool. **Not yet deployed** — needs real HDDs with SMART data, external storage not physically assembled yet. |
| homelab-sentinel (Telegram bot) | Docker container-level monitoring + Telegram alerts, PLUS interactive queries / whitelisted management / short QnA | - | Container health/resource (things Uptime Kuma's URL/TCP checks can't see) — owns Telegram notifications so Uptime Kuma's own alert integration isn't wired to Telegram in parallel. Also the interactive control surface (see decisions.md for the 3-tier capability design + guardrails). |

## Other Self-Hosted Apps

| Service | Purpose | Port | Notes |
|---|---|---|---|
| Syncthing | Continuous P2P file sync between specific devices | 8384 (Web UI), 22000 tcp+udp, 21027 udp | Different from Nextcloud: no central "cloud" browsing/share-links, just keeps folders in sync across devices (including this server). **Deployed 2026-09-11.** Sync data at `/mnt/hdd-cloud/syncthing` — **real HDD (sdd) mounted 2026-09-12**, chowned to UID 1000 again after the mount swap (same fix as the original crash-loop, since a fresh root-owned dir was created at the real mount point). Hit a startup crash loop (`permission denied` on its config volume) because the image runs as UID 1000 by default but the Docker-created volume was owned by root — fixed with `chown -R 1000:1000` on the volume + config dir. **No login/auth configured** — the GUI is wide open on the LAN; worth setting a GUI username/password later via Settings. |
| Nextcloud | File storage + sharing (cloud-drive style) | 8080 | Central storage, share links, web/mobile access — the "cloud" experience; not redundant with Syncthing (different sync model, see above) |
| Shiori | Bookmark manager | 8081 | **Deployed 2026-09-11.** No admin account pre-created — first-run creates it via the web UI. |
| YOURLS | URL shortener | 8083 | **Deployed 2026-09-11.** Uses a **dedicated MariaDB** (`yourls-mariadb`), not the shared Postgres — YOURLS only officially supports MySQL/MariaDB. Intentional exception to the shared-DB convention, isolated from CapRover's future MySQL pool too (different trust boundary again). **Known quirk:** the bare root path `/` returns 403 (an upstream image config quirk — its rewrite rule excludes existing directories, and the docroot itself is one) — go straight to `/admin/` for the first-run setup wizard instead. `YOURLS_SITE` is set to a `yourls.home.arpa` placeholder until a real domain exists. |
| n8n | Workflow automation | 5678 | **Deployed 2026-09-11.** Uses the shared Postgres (database `n8n`). `N8N_ENCRYPTION_KEY` generated server-side, never printed or committed. No account pre-created — first-run wizard. |
| Alexandrie | Self-hosted notes / knowledge base | 8200 (UI), 8201 (API), 9002 (RustFS S3), 3307 (MySQL) | **Deployed 2026-09-12.** Repo: [Smaug6739/Alexandrie](https://github.com/Smaug6739/Alexandrie). Has its own MySQL 8.0 + RustFS (S3-compatible storage) — separate from the shared Postgres/Redis, same reasoning as YOURLS. RustFS port remapped from default 9000 to 9002 (9000 collides with Portainer on this host). No admin account pre-created — the app has its own signup page (`CONFIG_DISABLE_SIGNUP=false`), first-run creates it via the web UI. |
| Vaultwarden | Password manager (lightweight Bitwarden-compatible server) | 8222 | Community rewrite in Rust — NOT the official `bitwarden/server`, which is much heavier. **Deployed 2026-09-11.** `SIGNUPS_ALLOWED=true` for now — flip to `false` in `configs/docker-compose/vaultwarden.yml` once accounts are created, per Vaultwarden's own security recommendation. |
| Firefly III | Personal finance / budgeting tracker | 8280 | **Deployed 2026-09-12.** Uses the **shared Postgres** (database `firefly`, same `admin` user) instead of the app's normally-bundled MariaDB — Firefly III supports pgsql natively, so no separate DB engine was needed (unlike YOURLS/Alexandrie, which require MySQL). Also runs a lightweight `firefly_iii_cron` sidecar (Alpine + cron) that hits Firefly's `/api/v1/cron/$STATIC_CRON_TOKEN` daily at 03:00 for scheduled tasks (recurring transactions, etc.). Port remapped from the upstream default 80 to 8280 (80 is NPM's). No admin account pre-created — Firefly's own registration page handles it. |
| Home Assistant | Home automation | - | Deploy once the smart power plug (HA-compatible) arrives |
| Reclip | Self-hosted media downloader (yt-dlp wrapper, web UI) | 8899 | **Deployed 2026-09-12.** Repo: [averygan/reclip](https://github.com/averygan/reclip) — built from source (Python+Flask, ~150 lines, yt-dlp+ffmpeg), no pre-built image published. Cloned to `/opt/projects/reclip/` on docker-host. No admin/auth at all — anyone on the LAN can use it, matches the tool's minimal design. |
| LibreSpeed | Self-hosted internet/LAN speed test (open-source Speedtest alternative) | 8082 | Lightweight (PHP+JS), useful for testing PC↔Homelab LAN speed and WAN speed without relying on a third-party server. **Deployed 2026-09-11.** No password set on the results/admin page (`PASSWORD` env left empty) — fine for LAN-only use, set one if this ever gets exposed further. |
| VaultS3 | Lightweight S3-compatible object storage | - | **Not yet deployed 2026-09-12** — previous plan to put this at `/mnt/hdd-cloud/vaults3/` contradicts decisions.md's cross-drive backup requirement (VaultS3 backs up Nextcloud, which lives on hdd-cloud). Deferred until hdd-music (sdc) or HDD-Backup is ready as the real cross-drive home. |
| SnapOtter | Self-hosted file-processing toolkit — 200+ tools across image/video/audio/PDF/files (convert, compress, OCR, transcribe). Replaces CloudConvert/Smallpdf/TinyPNG/Otter.ai. | - | Standing service (has its own Redis job queue for background jobs). Bundles its own Postgres 17 + Redis — do NOT wire to the shared instances. Limit concurrent workers since video transcode/OCR are CPU-heavy on the GPU-less M710q. Replaced the earlier FileWizard plan (SnapOtter is the superset). |
| T3 Code | Agent harness control surface for Claude Code, Antigravity/Gemini, etc. | 9001, 9002, 9003 (docker-host) + 9001 (apps-host) | **docker-host**: 3 instances total — original `t3code` (9001, deployed 2026-09-12) plus 2 new ones added 2026-09-13: `t3code-2` (9002, `configs/docker-compose/t3code-2.yml`) and `t3code-3` (9003, `configs/docker-compose/t3code-3.yml`), each with its own named volume (`t3code_data_2`/`_3`) and an explicit `name:` in the compose file to avoid a Compose project-name collision since all 3 files share one directory. **apps-host** (LXC 101, `192.168.18.226`): new independent `t3code` instance on 9001 (`/opt/t3code/docker-compose.yml` on that LXC — not yet under git, apps-host has no established repo-checkout convention). All share the same custom Dockerfile (`@anthropic-ai/claude-code` + `t3` CLI). Each instance needs `claude auth login` run interactively by the user themselves (never by the assistant) before it's usable. T3 Connect pairing tokens minted with `npx t3 pair --ttl 168h` (7 days) per the user's request — tokens themselves given to the user directly in-session, never committed to git (they're bearer credentials). |
| Databasus | PostgreSQL backup (PITR, restore verification, notifications) | - | Candidate to **replace** `scripts/backup.sh`'s Postgres piece, not run alongside it — avoid running two backup mechanisms against the same DB |
| qBittorrent | Torrent client (web UI) | 8480 (WebUI), 6881 (tcp+udp, torrenting) | **Deployed 2026-09-12.** Deployed **without a VPN wrapper** (Gluetun) for now — user's own cost/risk trade-off, see decisions.md. Public IP is exposed to torrent swarms as a result. Downloads go to real HDD at `/mnt/hdd-media/qbittorrent/downloads`. First-boot admin password is a random temporary value printed once in `docker logs qbittorrent` — already retrieved and changed by the user; check container logs again if a fresh one is ever needed (regenerates on every restart until a permanent password is set in Web UI preferences). |

## Automation Scripts

> Status: scripts + systemd units are written and committed, but NOT yet deployed —
> docker-host doesn't exist yet (see `docs/roadmap.md`). Deploy steps in
> `configs/systemd/README.md` once the LXC/VM is up.

| Script | Purpose | Schedule | Unit files |
|---|---|---|---|
| `scripts/backup.sh` | Dumps shared PostgreSQL + copies `configs/` to `/mnt/external-storage/backups/<timestamp>`, prunes backups older than 30 days | Daily at 03:00 (+random delay up to 5min) | `configs/systemd/homelab-backup.service` + `.timer` |
| `scripts/health-check.sh` | Checks expected containers are running; auto-restarts any that are down (one restart attempt), logs to `/var/log/homelab-health-check.log` | Every 5 minutes | `configs/systemd/homelab-health-check.service` + `.timer` |
| `scripts/git-auto-deploy.sh` | Polls each project under `/opt/projects/*` for new commits on `main`; on change, `git pull` + `docker compose up -d --build`. Polling instead of a GitHub webhook because the server has no public-facing endpoint (Tailscale-only). Logs to `/var/log/homelab-git-deploy.log` | Every 5 minutes | `configs/systemd/homelab-git-deploy.service` + `.timer` |
