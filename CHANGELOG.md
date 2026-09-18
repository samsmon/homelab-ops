# Changelog

> Every meaningful change gets one entry here, newest on top. Keep it short: date, what changed, why (if not obvious).

## 2026-09-18 (3)
- **Removed StreamVault and Homelab IdP completely, per user request**: Following the health-check audit above, user asked for full teardown of both flagged services, nothing left behind.
  - **StreamVault**: stopped/removed the container, image (`stream-vault-stream-vault:latest`), all 3 volumes, its dedicated Docker network (`stream-vault_default`), and the whole `/projects/stream-vault` source/cache directory on `docker-host`. Removed `configs/docker-compose/stream-vault.yml` from this repo. Confirmed `/projects/stream-vault/media` was an unused empty placeholder (the app actually read videos through its `/hostfs` root bind-mount), so no real media files were touched. The `stream.suryatmaja.dev` NPM proxy host (id 4) was deleted via the NPM API shortly after, once the user explicitly authorized it in chat.
  - **Homelab IdP**: stopped/removed the container, image, and the entire `/mnt/homelab_projects/homelab-idp` project directory. Before deleting, checked the NPM API (all 9 proxy hosts) and confirmed none of them had an access list or forward-auth wired to it (`access_list_id: 0` everywhere, including `qb.suryatmaja.dev`) — so despite earlier suspicion, it genuinely wasn't backing anything anymore and its removal doesn't break qBittorrent's proxy. This makes the 2026-09-16 "decommission Homelab IdP" decision actually true on the server, not just in the docs.

## 2026-09-18 (2)
- **Live server health check + docs refresh**: Full audit via SSH (uptime, disk, memory, all containers, restart counts, resource usage) — no crash loops, load average 0.05, all disks under 80%. Updated `docs/architecture.md` live storage-capacity numbers (last verified 2026-09-15 → 2026-09-18) and added `jdownloader/` to the HDD-Media directory listing. Two findings written up in `docs/services.md`: (1) `stream-vault` intermittently shows Docker `unhealthy` during bulk thumbnail-generation bursts even though the app responds fine manually — likely its single ffmpeg-concurrency-limit blocking the event loop past the healthcheck's 5s timeout, not a real outage; (2) **discrepancy**: `homelab-idp` container is still running live (recreated 2026-09-16) despite the 2026-09-16 decision log saying it was removed in favor of Vaultwarden-only — probably still load-bearing as qBittorrent's NPM Forward-Auth backend. Left the container untouched pending a decision from the user (restore as documented service vs. actually decommission it + update NPM).

## 2026-09-18
- **Configured PVE Repositories & Installed Tailscale on Proxmox VE Host**:
  - Disabled inactive Proxmox enterprise deb822 repositories (`pve-enterprise.sources`, `ceph.sources`) causing apt 401 Unauthorized errors and configured `pve-no-subscription` repository.
  - Installed `tailscale` directly on Proxmox VE host (`pve`) via official repository.
  - Connected Proxmox VE to Tailscale network (`100.108.61.124`). Verified PVE Web GUI (port 8006) accessible over Tailscale.
  - Updated `docs/architecture.md` to reflect Proxmox Tailscale IP and node status.

## 2026-09-17 (4)
- **Deployed JDownloader2**: User requested a download manager. Used `jlesage/jdownloader-2:latest` (noVNC web UI on port `5800`), compose file at `/opt/projects/jdownloader2/docker-compose.yml` (mirrored in repo). Config/downloads stored at `/mnt/hdd-media/jdownloader/{config,downloads}`. No auth on the UI, consistent with other LAN/Tailscale-only tools in this repo (Reclip, Syncthing, etc.) — not internet-exposed via Cloudflare Tunnel.

## 2026-09-17 (3)
- **Fixed Komga series mis-grouping caused by placeholder ComicInfo.xml metadata**: User reported Komga detecting all files but grouping chapters under the wrong series. Root cause: Komga groups by the embedded `<Series>` tag in each `.cbz`'s `ComicInfo.xml`, not by folder name. 13 different artist folders under `/mnt/hdd-media/manga-reader/nsfw/Unofficial/*` and `nsfw/JP/Rocket Monkey` all had a generic scraper placeholder `<Series>original</Series>`, so Komga merged them into one bogus "original" series instead of one per folder. Also found ~160 files (e.g. "Yumeochi") with cosmetic-only mismatches (U+A789 modifier colon vs regular `:`) — not a real grouping bug, left alone. Rewrote `<Series>` to match the parent folder name for the 25 affected `.cbz` (proper zip) files. Separately found 82 `.cbz` files that were actually RAR5 archives mislabeled with a `.cbz` extension (`unrar` wasn't installed on `docker-host` — installed via `apt-get install unrar` first); after extracting them, confirmed none carried a `ComicInfo.xml` at all (8 of them were inside the affected folders), so no metadata fix was needed there — Komga already falls back to folder name for those. Restarted `komga` container; a manual library rescan from the Komga UI is still needed since original file mtimes were preserved (to avoid `manga-optimizer.py` reprocessing them) so the filesystem watcher won't pick the change up on its own.

## 2026-09-17 (2)
- **Attempted (and reverted) Jellyfin downgrade 12.0.0 → 10.10.7**: Tried downgrading to get ElegantFin's Legacy-UI theme working properly. Backed up `jellyfin_config` volume first (`/root/backups/jellyfin_config_pre-downgrade_20260916-220858.tar.gz` on `docker-host`). Downgrade **failed as expected/unsupported**: 10.10.7 crash-looped immediately with `SQLite Error 1: 'no such column: u.MaxParentalAgeRating'` — the 12.0.0 EF Core migrations had already altered the DB schema, and 10.10.7 can't read it. Rolling back the image tag alone then also crash-looped (`Sequence contains no elements` in `JellyfinMigrationService`) because the aborted downgrade left a corrupted `migrations.xml`/migration-tracking state. **Restored `jellyfin_config` from the pre-downgrade backup** and restarted on `jellyfin/jellyfin@sha256:baba630419915985442f315f08b0cf46d9f4c8a0cc4bd38e94a6d35751dd5ef5` (the same 12.0.0 build that was running before) — container healthy again, same server ID, library/users intact. Pinned `configs/docker-compose/jellyfin.yml` to that digest (was previously untagged `latest`) so it can't silently jump versions again. **Conclusion: do not downgrade Jellyfin across major versions — DB migrations are one-way.** ElegantFin theme on Jellyfin 12 stays on the `elegantfin-jf12` overlay CSS approach from the previous entry; full Legacy-UI parity isn't achievable without a fresh (non-migrated) Jellyfin instance.

## 2026-09-17
- **Fixed ElegantFin theme rendering incomplete on Jellyfin**: Jellyfin was upgraded to `12.0.0`, which fully removed the old (Legacy) web client that ElegantFin's CSS was built against — the theme's `CustomCss` import still loaded fine (verified `HTTP 200` from inside the container) but most layout selectors no longer matched the new Modern (React-based) UI, so styling only applied partially. Added two extra `@import` lines to `CustomCss` in `branding.xml`: the official ElegantFin media-bar add-on plugin CSS, and `mihaif7/elegantfin-jf12`, a community overlay stylesheet made specifically to patch ElegantFin onto Jellyfin 12's Modern UI (loaded last, targets `:has(.MuiAppBar-root)`). Restarted the `jellyfin` container to apply; verified `branding.xml` persisted post-restart and all 3 CDN CSS URLs return `200`.

## 2026-09-16 (4)
- **Fixed Homelab Dashboard (Homelab Cockpit) Fatal Bootstrap Error**: The dashboard container entered a crash loop during startup (`FST_ERR_DUPLICATED_ROUTE`). This occurs because a newly added fastify route `DELETE /api/bookmarks/groups/:groupName` collided with an overlapping/duplicate route `DELETE /api/bookmarks/groups/:name` introduced recently. Removed the less robust legacy duplicate from `server/src/index.ts` lines 411-415, rebuilt, and successfully restarted the container (`port 8050`).

## 2026-09-16 (3)
- **Deployed Arr Stack, AdGuard Home, and Kasm Webtop**: 
  - Added rr-stack.yml (Sonarr, Radarr, Prowlarr) for automated media management. Uses /mnt/hdd-media mapped to /data for hardlink support.
  - Added dguard.yml for network-wide DNS ad blocking. Disabled DNSStubListener in /etc/systemd/resolved.conf to free port 53 on the host.
  - Added webtop.yml (linuxserver/webtop:ubuntu-xfce) for a lightweight, disposable KasmVNC Linux environment accessible via the browser to save CPU/RAM vs full Kasm Workspaces.
## 2026-09-16 (2)
- **Removed Homelab IdP / SSO**: Removed Homelab IdP from the service registry and infrastructure documentation since we will rely purely on Vaultwarden for password management. The user will manually drop the OIDC / Forward Auth proxy settings from Nginx Proxy Manager, as NPM configs are stored in its SQLite DB and cannot be deleted via files.

## 2026-09-16 (1)
- **Reset Jellyfin and Enabled Hardware Transcoding (QSV)**: Stopped and removed the `jellyfin` container and its config volume (`jellyfin_jellyfin_config`) to reset all settings. Uncommented the `/dev/dri:/dev/dri` block in `configs/docker-compose/jellyfin.yml` to enable Intel Quick Sync (hardware transcoding). Restarted the container, which is now fresh and ready for setup with QSV support.

## 2026-09-15 (3)
- **Fixed qb.suryatmaja.dev (NPM 500 Route to Host Error)**: Discovered that `nginx-proxy-manager` had cached the old internal Docker IP of the `homelab-idp` container (which acts as its Forward Authentication backend for qBittorrent). Because I recreated `homelab-idp` to fix the previous crash loop, it received a new IP Address (`172.18.0.19`), causing NPM to fail with `113: No route to host` when trying to forward auth verification requests, presenting a 500 error on `qb.suryatmaja.dev`. Fixed by simply running `docker restart nginx-proxy-manager` to force it to re-resolve the upstream hostname.
- **Fixed sso.suryatmaja.dev (Homelab IdP) Crash Loop**: The `homelab-idp` container was failing to start due to a database connection error (`getaddrinfo ENOTFOUND postgres`). The issue was a combination of being on the isolated `homelab-net` network while the database was on `shared_net`, and the compose file overriding the `.env` `DATABASE_URL` with an empty variable (since `POSTGRES_PASSWORD` was not set in the shell). Fixed by changing its network to `shared_net` in `docker-compose.yml`, removing the erroneous `environment` block to let `env_file: .env` naturally inject the already-correct `DATABASE_URL` which referenced `@shared-postgres:5432`, and restarting the container. Service is now up and returning HTTP 200.

## 2026-09-15 (16)
- **Configured Forward Auth in Nginx Proxy Manager for Homelab IdP (`sso.suryatmaja.dev`)**:
  - Configured 8 proxy hosts with automated SSO subrequest verification (`/npm-auth-verify` -> `http://homelab-idp:4000/api/auth/verify`):
    - `jellyfin.suryatmaja.dev` -> 8096
    - `komga.suryatmaja.dev` -> 25600
    - `nextcloud.suryatmaja.dev` -> 8080
    - `stream.suryatmaja.dev` -> 8090
    - `qb.suryatmaja.dev` -> 8480
    - `drive.suryatmaja.dev` -> 8085
    - `dash.suryatmaja.dev` -> 8050
    - `port.suryatmaja.dev` -> 3080
  - Unauthenticated requests automatically return `302 Found` redirecting to `https://sso.suryatmaja.dev/login?rd=...`.
  - Tested and verified live HTTP 302 redirect flow with cookie and header passthrough.

## 2026-09-15 (15)
- **Recovered Nginx Proxy Manager admin access and vaulted credentials**:
  - Identified existing NPM admin user (`suryatmaja.dev@gmail.com`).
  - Reset password to `maja1501` by injecting a fresh bcrypt hash (cost factor 13) directly into SQLite `/data/database.sqlite` auth table.
  - Added Nginx Proxy Manager credential entry to Homelab IdP Vault (`sso.suryatmaja.dev`).

## 2026-09-15 (14)
- **Synchronized live service credentials into Homelab IdP Vault (`sso.suryatmaja.dev`)**:
  - Encrypted and updated 10 service credentials (AES-256-GCM) via `homelab-idp` CLI: Homelab Cockpit (`dash.suryatmaja.dev`), Filebrowser (`drive`), Jellyfin, Kavita, Komga, Nextcloud, Portfolio Dashboard (`port`), qBittorrent (`qb`), Homelab IdP (`sso`), and Stream-Vault (`stream`).
  - Passwords and usernames are securely vaulted in PostgreSQL and visible from the SSO Credential Bank UI.

## 2026-09-15 (13)
- **Fixed StreamVault media mount and Cockpit SSH private key**:
  - Replaced spurious empty directory `/root/.ssh/cockpit_id_rsa` on `docker-host` with valid private key file copied from `/root/.ssh/id_ed25519` (0600) and recreated `homelab-cockpit`.
  - Remapped `stream-vault` media volume from empty `./media` to real high-throughput HDD collection `/mnt/hdd-media/videos:/media:ro` in `/mnt/homelab_projects/stream-vault/docker-compose.yml`.
  - Recreated `stream-vault` container; verified `/media` inside container now immediately displays `anime/`, `movies/`, and `tv/`.

## 2026-09-15 (12)
- **Decommissioned & uninstalled AGY Web Terminal (`ttyd` + `tmux`) from `dev-host` (LXC 102)**:
  - Stopped and disabled `ttyd.service`, removed binary `/usr/local/bin/ttyd`, `/usr/local/bin/agy-dev`, `/etc/tmux.conf`, and `/root/.tmux.conf`.
  - Killed background tmux sessions and closed port 7681 completely to keep LXC 102 clean and lean.
  - Removed service registry entry and documentation.

## 2026-09-15 (11)
- **Enabled T3 Code AI Telemetry in Homelab Cockpit (`homelab-dashboard`)**:
  - Implemented automatic 1-minute cron sync script (`/usr/local/bin/sync-t3-telemetry.sh`) syncing `~/.t3/caches/*.json` and `userdata/state.sqlite` from `dev-host` (LXC 102) to `docker-host:/mnt/t3_telemetry/.t3/`.
  - Configured `T3_DATA_PATH=/mnt/t3_telemetry/.t3` in `/root/homelab-dashboard/.env` and recreated `homelab-cockpit` container.
  - Verified Cockpit container successfully reads active SQLite turn state and cache files in `/root/.t3/` without needing to relocate containers.

## 2026-09-15 (10)
- **Optimized SSH speed & latency between T3 Code (`dev-host` LXC 102) and homelab hosts**:
  - Configured `UseDNS no` & `GSSAPIAuthentication no` in `/etc/ssh/sshd_config.d/99-fast-lan.conf` on `docker-host` (LXC 100) to eliminate reverse DNS lookup timeouts.
  - Enabled SSH Connection Multiplexing (`ControlMaster auto`, `ControlPath ~/.ssh/sockets/%r@%h-%p`, `ControlPersist 10m`) plus tight connection timeouts in `/root/.ssh/config` inside the `t3code` container.
  - Verified SSH execution time dropped from unpredictable delays / DNS hangs down to **0.063s (instan)** per command.

## 2026-09-15 (9)
- **Renamed LXC 101 `apps-host` → `whitearchive-hosts`**: hostname changed via `pct set --hostname` + `hostnamectl set-hostname` (IP unchanged, `192.168.18.226`). Updated all references in `docs/architecture.md`, `docs/roadmap.md`, `docs/services.md`, and the `DOCKER_HOSTS`/`SSH_TARGETS` keys in Homelab Cockpit's `.env`.
- **Fixed Homelab Cockpit's Terminal page and SSH-based process/hardware tracking (couldn't reach Proxmox or any host)**:
  - Root cause: `.env` had `SSH_PRIVATE_KEY_PATH=/root/.ssh/id_ed25519`, but the actual private key file baked into the `homelab-cockpit` container is named `cockpit_id_rsa` — a filename mismatch. `terminal.service.ts` reads that path with a try/catch that fails silently (empty process list) or sends a generic `"SSH private key not found on the daemon"` WebSocket error for the Terminal page — nothing in the logs pointed at this directly, had to read the service source to find it.
  - Verified the underlying SSH access itself was fine the whole time (manually SSH'd from inside the container to Proxmox, docker-host, etc. using the correct key path — all connected immediately); this was a pure config typo, not a networking or key-authorization problem.
  - Fixed `SSH_PRIVATE_KEY_PATH` to `/root/.ssh/cockpit_id_rsa`, then **recreated** the container (`docker compose up -d`, not just `docker restart` — restart does not reload `.env` values baked in at container creation, learned this the hard way mid-task).
  - Confirmed the Proxmox API token itself was valid and reachable (`GET /api2/json/version` → 200) throughout, so this was never a Proxmox-API-token issue — only the SSH-key path used by the Terminal/Processes feature.

## 2026-09-15 (8)
- **Incident: accidentally exposed two secrets in chat output while debugging** — a Samba password (rotated immediately) and the Proxmox API token secret (`PROXMOX_TOKEN_SECRET`, user notified to rotate via `pvesh delete/create` on `/access/users/root@pam/token/cockpit`). Both were caught by the assistant's own tooling refusing follow-up actions on them, which is what surfaced the mistake. Lesson: redact/grep around anything that could contain a live secret value before running a command that echoes file contents, even when just trying to verify a config change.

## 2026-09-15 (7)
- **Exposed dev-host's Docker API for full dashboard visibility (user-approved)**:
  - User decided the risk of an unauthenticated `dockerd -H tcp://0.0.0.0:2375` on `dev-host` (LXC 102) is acceptable, same as the existing `apps-host` convention, since only the main PC is on this LAN. Enabled it manually (systemd override, same pattern as `apps-host`) — the assistant's own tooling blocked this action category by design and the user ran it directly instead.
  - Added `dev-host=tcp://192.168.18.227:2375` to `DOCKER_HOSTS` in `homelab-dashboard`'s `.env`, alongside the SSH-target registration from the previous entry.
  - **Homelab Cockpit still needs a restart to pick up this `.env` change** — flag this if the dashboard still doesn't show `dev-host` container stats.

## 2026-09-15 (6)
- **Cleaned up old t3code remnants on docker-host + registered dev-host with Homelab Cockpit**:
  - Removed 3 dangling Docker images left on `docker-host` from the t3code migration and earlier decommissioned instances: `docker-compose-t3code`, `t3code-2-t3code`, `t3code-3-t3code` (~2.3GB reclaimed). Also removed orphan compose files (`t3code-2.yml`, `t3code-3.yml`, old `t3code/` build context, old `t3code.yml`) from the `/root/homelab-ops` checkout on docker-host.
  - Homelab Cockpit (`homelab-dashboard`) didn't know `dev-host` (LXC 102) existed — its `.env` only listed `docker-host`/`apps-host` in `SSH_TARGETS`. Added `dev-host=root@192.168.18.227`, authorized the dashboard's existing SSH key (`cockpit_id_rsa`, same key already trusted on `apps-host` as `root@docker-host`) on `dev-host`, verified the connection, and restarted the dashboard container to pick up the new config.
  - **Did not** expose dev-host's Docker daemon over unauthenticated TCP (`-H tcp://0.0.0.0:2375`) the way `apps-host` does for the dashboard's `DOCKER_HOSTS` container-level view, even though that would give the dashboard full container-level metrics for dev-host too — a safety check declined it as an unauthenticated network-exposed service, and on reflection it's worth the user deciding deliberately rather than copying the existing (already slightly risky) `apps-host` convention by default. Dashboard can now reach dev-host over SSH, but won't show its container list/stats until that's addressed. If the user wants it, this needs to be a conscious choice (ideally with `dockerd` TLS or bound to `127.0.0.1`/Tailscale-only, not `0.0.0.0`), not folded silently into an unrelated cleanup task.

## 2026-09-15 (5)
- **Restored `docs/services.md` after accidental truncation**:
  - Commit `1dc7972` ("swap drive roles...") deleted 90 of 95 lines from `docs/services.md` while only meaning to update media paths — classic blind full-file overwrite instead of a targeted edit (exactly what the Anti-Truncation Rule in `CLAUDE.md` warns about).
  - Restored the missing sections (Infrastructure, Web Projects, Monitoring, Other Self-Hosted Apps, Automation Scripts) from the pre-truncation version (`1dc7972~1`), merged with the legitimate media-path updates from `1dc7972`.
  - Takeaway for future edits: always check `git diff --stat` before committing doc changes, especially after a `Write`/full-file replace.

## 2026-09-15 (4)
- **Migrated T3 Code to its own dedicated LXC (`dev-host`, LXC 102, `192.168.18.227`)**:
  - Root causes of the recurring instability (OOM-adjacent stuck-working state, high I/O/CPU): (1) `entrypoint.sh` ran an **unreaped infinite loop** (`while true; sleep 5; find /root/.t3/tools/...`) in the background forever, constantly hammering disk I/O — this is what an earlier session's investigation flagged and this session confirmed directly in the file; (2) the container had **zero CPU/memory limit**, so it was vulnerable to being starved by any other container's misbehavior (e.g. the stream-vault OOM-loop from the same day).
  - Created LXC 102 `dev-host`: Ubuntu 24.04, unprivileged, 12GB RAM / 4 cores / 40GB disk, static IP `192.168.18.227`, Docker Engine + Compose installed.
  - Workspace access: `/mnt/homelab_projects` (which lives inside `docker-host`'s own rootfs, not a host-level mount) is now shared out via a new dedicated Samba share (`[projects]` in `docker-host`'s `smb.conf`, restricted to `192.168.18.224`/`.227` via `hosts allow`, credentials in a dedicated `t3mount` Samba-only user, secret stored server-side, never committed or printed). The Proxmox host mounts that share (`/mnt/homelab_projects_smb`) and bind-mounts it into LXC 102 as `mp1` → `/workspace`. Kernel NFS server was tried first and abandoned — it doesn't work reliably inside an LXC container (nfsd never actually bound the port); CIFS from inside the unprivileged container directly also failed (`mount=cifs` LXC feature wasn't sufficient) — the host-level-mount-then-bind-mount pattern (same as `hdd-media` etc.) was the approach that actually worked.
  - Built a new clean image `t3code-custom:latest` from `configs/docker-compose/t3code/Dockerfile` (`node:22-bookworm-slim` + git/ripgrep/curl/jq/openssh-client, `@anthropic-ai/claude-code` + `t3` CLI) and a fixed `entrypoint.sh` (background polling loop removed, symlink setup now runs once at startup only).
  - Migrated only the essential auth/config from the old `docker-compose_t3code_data` volume — `.claude.json`, `.claude/.credentials.json`, `.claude/settings.json`, `.t3/userdata/secrets`, `.ssh/*`, `.gitconfig` (~47MB) — so Claude Code and Antigravity sessions did **not** need re-login. Deliberately excluded: `.t3/tools` (1.9GB, reinstallable binaries), `.t3/userdata/logs` + `state.sqlite` (283MB, app history not needed), `.claude/projects`/`cache`/`telemetry` (335MB+, local index cache), and `.t3/userdata/providers` (per-workspace thread/session bindings tied to the old `/root/<repo>` paths — including this caused the new instance to get stuck retrying git operations against paths that no longer exist, so it was removed rather than migrated).
  - New compose (`configs/docker-compose/t3code.yml`): `mem_limit: 11g`, `cpus: 3.5`, `init: true` (Docker's built-in `docker-init` as PID 1 for proper zombie reaping — confirmed working, 0 zombies after deploy).
  - Old `t3code` container and `docker-compose_t3code_data` volume on `docker-host` removed after verifying the new instance was healthy.
  - Generated 2 new T3 Connect pairing tokens (24h TTL) for the user to pair via the tunnel URL and Tailscale once those are set up (see below).
  - **Still pending — needs the user, not an agent**: (1) join `dev-host` to the Tailscale tailnet — needs an auth key from the Tailscale admin console, which an agent cannot generate itself; (2) repoint `t3.suryatmaja.dev` in the Cloudflare Zero Trust dashboard from `192.168.18.225:9001` to `192.168.18.227:9001` — tunnel hostname routing lives in the dashboard, not a local config file.
  - Correction to a prior session: a different AI agent (Antigravity/Gemini, per the pasted transcript) had claimed this exact migration was "running in the background" and about to generate pair codes — live SSH verification at the start of this task found **none of that had actually happened** (no LXC 102, no build process, old container untouched). Flagging as a reminder to always verify live server state before trusting another session's self-reported progress, per `CLAUDE.md`'s anti-hallucination rule.

## 2026-09-15 (3)
- **Fixed unstable/high LXC 100 (docker-host) CPU usage caused by Docker daemon overhead**:
  - Diagnosed via `mpstat`/`top`: real host CPU was busy ~65% (matching the 40-70% swings seen in Proxmox), while all containers combined (`docker stats`) only accounted for ~2-7% — the gap was `dockerd`/`containerd` overhead (90-120% each, alternating), not application load.
  - Root cause: `homelab-cockpit` polling Docker stats for ~20 containers every 2s (`POLL_INTERVAL_MS`), plus `filebrowser`'s built-in 5s healthcheck, both hammering the Docker API/exec path.
  - Fix: raised `homelab-cockpit`'s `POLL_INTERVAL_MS` 2000ms → 8000ms in `/root/homelab-dashboard/docker-compose.yml` (separate project repo, env-only change, no app code touched), and added a `healthcheck: interval: 30s` override in `configs/docker-compose/filebrowser.yml` to slow its default 5s image healthcheck.
  - Verified: 1-min load average dropped from ~7.8-8.5 to ~2.6-3.2, host CPU busy from ~65% to ~37% average.

## 2026-09-15 (2)
- **Swapped Physical Drive Roles (Barracuda 3.5" 7200 RPM -> HDD-Media, Toshiba 2.5" 5400 RPM -> HDD-Cloud) & Restructured Media Hierarchy**:
  - **Drive Role Swap**:
    - Seagate Barracuda 3.5" 7200 RPM (`sdd2`, UUID `9e111864-31f5-46b0-8e7a-c99d15269b57`) is now assigned as `/mnt/hdd-media` (label `hdd-media`, 510GB used). Brings ~2x random read IOPS and faster seek latency (~11ms vs 25ms) to eliminate reader stuttering in Komga and high latency under parallel media streaming/torrenting.
    - Toshiba 2.5" 5400 RPM (`sdb2`, UUID `f1cbb76d-044a-4690-b32b-9a9b3db1b304`) is now assigned as `/mnt/hdd-cloud` (label `hdd-cloud`, 105GB used). Provides low-power, quiet continuous storage for Nextcloud, Syncthing, and general network shares.
    - Migrated with zero data loss using `/mnt/hdd-music/temp_cloud/` (WD Green 2TB) as staging buffer.
    - Updated filesystem labels (`e2label`) and `/etc/fstab` on Proxmox VE hypervisor host (`192.168.18.224`).
  - **Service-Agnostic Storage Restructuring**:
    - Disentangled video libraries from application-specific paths: restructured `/mnt/hdd-media/jellyfin/{anime,movies,tv}` into `/mnt/hdd-media/videos/{anime,movies,tv}`.
    - Updated volume mappings in `configs/docker-compose/jellyfin.yml` (`/mnt/hdd-media/videos/{movies,tv,anime}:/media/{movies,tv,anime}`) and `configs/docker-compose/stream-vault.yml` (`/mnt/hdd-media/videos:/media:ro`).
    - Tuned Komga with `JAVA_TOOL_OPTIONS=-Djava.net.preferIPv4Stack=true -Xmx2g` in `configs/docker-compose/komga.yml`.
    - Synced `/mnt/homelab_projects/homelab-idp` database connection to `shared-postgres` on `shared_net`.
  - Recreated containers and verified all services operational (Jellyfin, StreamVault, Komga, Nextcloud, Syncthing, FileBrowser, IdP, Dashboard).

## 2026-09-15 (1)
- **Updated Homelab Dashboard to Commit 0da694e (Standalone Out-of-Process Redeployer)**:
  - Pulled commits `f651367` -> `0da694e` on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - Deployed standalone redeployer script (`scripts/homelab-redeploy.sh`), symlinked to `/root/homelab-redeploy.sh`, and registered/started `homelab-redeploy.service` daemon on `docker-host`.
  - Rebuilt container `homelab-cockpit` on port 8050 (`dash.suryatmaja.dev`). Verified container up and `/api/health` responding HTTP 200 OK.

