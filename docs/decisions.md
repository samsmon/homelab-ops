# Decisions Log

> Records WHY something was chosen, so future-you (or Claude Code) doesn't re-litigate settled questions
> without new information. Add a new dated entry whenever a meaningful trade-off is decided.

## 2026-09-20 — Plan: repurpose `hdd-music` as cold-backup only, add encrypted offsite sync to Google Drive

- **Status: PLANNED, NOT EXECUTED.** Waiting on the in-progress `hdd-music` rescue rsync (see `CHANGELOG.md` (57)/(58)) to finish and the drive's fate (RMA vs. keep-using) to settle before starting this.
- **Context**: `hdd-music` (WD Green 2TB) has dropped from the kernel twice in 2 days — see (55)/(56). Root-cause analysis (same day, in chat) found the failure correlates with **NCQ-heavy random/small-file I/O** (torrent random writes in (40), MusicBee's thousands-of-small-file SMB library scan in (55)) — not with total data volume or write vs. read. Evidence: the 2026-09-15 (2) 1.5TB-class drive-role-swap migration (large sequential file copies) ran on this same drive with zero issues, and the in-progress rescue rsync (large sequential files) has run stable for 60+ minutes, while throughput visibly drops and risk visibly rises whenever it hits directories of many small files (e.g. individual JPEGs). Conclusion: this drive can plausibly still be trusted for **sequential, infrequent, write-once/read-rarely** access, but not for anything with frequent small-file/random I/O (active media library scanning, torrent downloads, live sync).
- **Decision**: repurpose `hdd-music` (and evaluate doing the same for other drives holding music/manga/video) as a **cold-backup target only** — data written in large sequential batches on a schedule, then left untouched, never used as a live-serving library (Navidrome/Jellyfin/MusicBee point elsewhere; qBittorrent does not write here). Primary contents to protect this way: **music, manga (raw + reader library), and video** currently spread across `hdd-media`/`hdd-cloud`/`hdd-music`.
- **Also decided**: add an **encrypted** offsite copy on Google Drive, using `rclone crypt` (client-side AES encryption of both file contents and filenames) layered on top of an existing/new `rclone` `gdrive` remote — not a plain/unencrypted `rclone` sync.
  - **Why encryption is required, not optional**: user is (rightly) worried about DMCA takedowns. Cloud providers' automated copyright enforcement is based on **content hash-matching**, not filenames — renaming/obfuscating filenames does nothing against it. Risk is uneven by category: doujin/circle music (low risk, rarely in rightsholder hash databases) vs. manga-raw and commercial video/anime (high risk, aggressively hash-matched). `rclone crypt` encrypts the actual bytes client-side before upload, so Google's servers only ever see opaque ciphertext blobs — there is nothing for a hash-matching system to match against. This is the standard, well-established mitigation in the self-hosting community for exactly this scenario, not a workaround of unknown reliability.
  - **Trade-off accepted**: an encrypted remote can't be browsed via the Google Drive web UI or shared normally — only accessible through `rclone` (with the encryption config/password) on `docker-host` or wherever it's set up. Acceptable since this is a cold backup, not a working library.
  - **Capacity**: user confirmed ~5TB combined across 3 separate Google accounts — comfortably enough for the current ~1-2TB+ combined music/manga/video footprint; exact per-account allocation and which account(s) to use not yet decided.
  - **Optional hardening not yet decided**: whether to use a Google account dedicated to this backup (separate from the user's primary/personal account) to further contain any account-level action Google might take, vs. reusing an existing account. Leaning toward a dedicated account but the user hasn't confirmed.
- **Not yet decided / follow-up needed once rescue finishes**:
  1. Final verdict on `hdd-music` itself — RMA/replace vs. cautiously keep using for cold-backup only (this whole plan assumes it's usable in a limited role; if the seller replaces it, the new drive takes over this role instead and can be trusted more broadly).
  2. Backup schedule/cadence (systemd timer? manual trigger? tied into the existing `scripts/backup.sh` / `homelab-cockpit`-native backup approach from the 2026-09-13 decision?).
  3. Exact `rclone crypt` remote name/config location, and which of the 3 Google accounts + how much quota to allocate.
  4. Whether manga/video get moved into this cold-backup scheme too (user mentioned "kedua hdd itu, terutama folder musik, manga, sama video" — implies `hdd-media`'s manga-raw/manga-reader and video libraries are in scope too, not just `hdd-music`'s music), and whether those live libraries stay served from their current active drives while only a *copy* goes cold, or whether serving moves too (default assumption: **copy only** — Jellyfin/Komga keep serving from their current active drives; cold-backup is a second copy, not a migration of the live library).

## 2026-09-20 — Plan: split `docker-host` LXC into domain-scoped LXCs (media / personal / drive / infra)

- **Status: PLANNED, NOT EXECUTED.** This is a proposal only — no container, compose file, or LXC has been touched. Requires explicit user go-ahead per-phase before any live change (per `CLAUDE.md` setup-mode rules).
- **Context**: today's qBittorrent password reset + `hdd-music` rw remount required `pct reboot 100` (the single `docker-host` LXC), which restarted **all 24 containers** at once — media, personal projects, and Nextcloud/Syncthing all went down together for an unrelated fix. User wants domain separation so a blast radius like that stays contained to one category next time.
- **Current state (as of today)**: single LXC `docker-host` (VMID 100), 12GB RAM allocated (9.2GB free / 12GB, so headroom exists but is not unlimited), 4 vCPU, running all 24 containers on one Docker bridge network (`shared_net`). Two other LXCs already exist on the same Proxmox host: `yado-hosts` (101), `dev-host` (102).
- **Proposed split** (4 LXCs, not 3 — see "infra" below):
  - **`media-hosts`**: `jellyfin`, `navidrome`, `feishin`, `komga`, `qbittorrent`, `prowlarr`, `sonarr`, `radarr`, `jdownloader2`. Rationale: these are the containers most likely to get rebooted/updated frequently (arr-stack tuning, qBittorrent config) and the ones where a restart is lowest-stakes for the user personally.
  - **`personal-hosts`**: `nhdl`, `yorha-portfolio`, `group-checklist`, `reclip`, `headless-browser` (nhdl's scraping dependency). Rationale: user's own projects, iterated on most often — isolating these means a broken deploy here can't take down Jellyfin or Nextcloud.
  - **`drive-hosts`**: `nextcloud`, `syncthing`, `filebrowser`. Rationale: personal file storage/sync — different backup cadence and uptime expectations (Nextcloud sync breaking mid-transfer is worse than a media-server blip) justify its own blast radius.
  - **`infra-hosts`** (not explicitly requested, but necessary — see below): `nginx-proxy-manager`, `adguardhome`, `shared-postgres`, `shared-redis`, `homelab-cockpit`, `vaultwarden`, `n8n`, `librespeed`. These are cross-cutting: nearly every other container depends on `nginx-proxy-manager` for its public route, several use `shared-postgres`/`shared-redis`, and `adguardhome` is the whole LAN's DNS — none of these belong inside media/personal/drive without recreating the same "one fix reboots everything" problem, just relabeled.
- **Open problems that must be resolved before executing** (this is why it's a plan, not a migration yet):
  1. **Cross-LXC networking for `shared-postgres`/`shared-redis`.** Docker's `shared_net` bridge network only works within one LXC's Docker daemon. Once `nhdl`/`reclip`/etc. move to `personal-hosts`, they can no longer reach `shared-postgres` by container DNS name. Options: (a) publish `shared-postgres`/`shared-redis` ports bound to `infra-hosts`'s LXC IP and have other LXCs connect via that IP (simplest, but opens the DB to the whole LAN subnet unless firewalled — needs a Proxmox/host firewall rule restricting to the other 3 LXC IPs only); (b) Tailscale between LXCs instead of relying on the LAN bridge (more setup, better isolation); (c) run a second Postgres/Redis per LXC that needs one (defeats "shared", doubles maintenance). **Leaning (a) with a firewall rule**, but not decided.
  2. **`nginx-proxy-manager` stays central.** All public hostnames route through one NPM instance in `infra-hosts`; moving a container to another LXC means NPM's upstream target changes from a container name to `<lxc-ip>:<port>`, and every LXC needs its Docker ports actually published (not just internal bridge) for NPM to reach them. This is mechanical but touches every proxy host entry — needs to be done one service at a time, verified live before moving to the next.
  3. **RAM/CPU budget across 4+2 LXCs.** Host has 32GB total; `docker-host` alone currently uses 12GB allocated. Need to check current allocation to `yado-hosts` (101) and `dev-host` (102) before carving out 3 more LXCs — each new LXC also duplicates OS + Docker engine overhead (roughly 300-600MB idle each based on `docker-host`'s current footprint). Must verify total doesn't oversubscribe 32GB/4C before committing, especially since `pve` host itself needs headroom.
  4. **`filebrowser`'s cross-domain mounts.** It currently bind-mounts `/mnt/hdd-media`, `/mnt/hdd-cloud`, and `/mnt/hdd-music` all at once (see `configs/docker-compose/filebrowser.yml`) — i.e. it's designed to browse everything, which cuts against putting it only in `drive-hosts`. Either accept it only browses cloud-relevant paths going forward, or keep it in `infra-hosts` instead.
- **Proposed migration order** (if/when approved): (1) resolve networking approach for shared-postgres/redis and test it with one low-stakes container first (e.g. `reclip`) before moving anything user-facing; (2) stand up `media-hosts` first since it's the most self-contained (no shared-postgres dependency to verify — confirm which `arr`/`qbittorrent`/`*arr` containers actually use it); (3) `personal-hosts`; (4) `drive-hosts` last, since Nextcloud/Syncthing are the most failure-sensitive to get wrong mid-migration.
- **Not yet decided**: exact RAM/vCPU allocation per new LXC, whether `infra-hosts` keeps the `docker-host` (VMID 100) name/ID or gets renumbered, and whether this happens in one working session or is staged over several with `CURRENT_OPS.md` locks between phases.

## 2026-09-18 — Rebrand "White Archive" ecosystem to "Yado" (apex domain yado.my.id)

- **Context**: User felt "White Archive" was too close to existing names (Blue Archive, a well-known game, plus some existing manga-scanlation sites/groups already using similar naming). Brainstormed alternatives in chat and settled on "Yado" (宿, Japanese for "inn/lodging") — short, easy to remember, not tied to an existing brand.
- **Decision**: New apex domain `yado.my.id` (not purchased yet, same as `whitearchive.my.id` never was) replaces `whitearchive.my.id` as the intended public domain for this project family: `yado.my.id` (whitearchive/frontend), `sso.yado.my.id`, `malas.yado.my.id`.
- **What changed**: NPM proxy hosts repointed to the new `*.yado.my.id` hostnames (still unreachable publicly until the domain is bought and DNS/Cloudflare Tunnel is set up — Tailscale IP `100.110.235.57:<port>` remains the only way to actually reach these right now). `whitearchive`'s `.env` (`NEXT_PUBLIC_SSO_URL`, `NEXT_PUBLIC_MALAS_URL`, health-check URLs) updated and the app **rebuilt** (Next.js bakes `NEXT_PUBLIC_*` vars into the static build, so an env change alone doesn't take effect without a rebuild). `malas` and `sso.whitearchive`'s `APP_URL`/`SSO_BASE_URL`/`SSO_REDIRECT_URI` updated to match.
- **Explicitly NOT done**: the actual GitHub repos (`srytmj/whitearchive`, `srytmj/malas`, `srytmj/sso.whitearchive`, `srytmj/pore-js`) keep their current names — renaming those, and any in-app hardcoded "White Archive" branding/copy, is source-code work that belongs in each repo's own session, not this infra repo. `pore-js`'s domain (`pore.suryatmaja.dev`) and `group-checklist`'s (`checklist.suryatmaja.dev`) are unaffected — they were never part of the whitearchive/yado family.

## 2026-09-17 — Do not downgrade Jellyfin across major versions; stay on 12.x pinned by digest

- **Context**: ElegantFin's theme doesn't render fully on Jellyfin 12's Modern web client (see CHANGELOG 2026-09-17 entries). Tried downgrading to `10.10.7` to get the old Legacy client/theme back.
- **Outcome**: Downgrade is not viable. Jellyfin's EF Core DB migrations are one-way — 12.0.0 had already altered the SQLite schema, so 10.10.7 crash-looped on missing columns, and reverting back to 12.x afterward also broke (corrupted migration-tracking state) until restored from a pre-downgrade backup.
- **Decision**: `configs/docker-compose/jellyfin.yml` now pins the image by digest (`jellyfin/jellyfin@sha256:baba630419915985442f315f08b0cf46d9f4c8a0cc4bd38e94a6d35751dd5ef5`, the 12.0.0 build) instead of floating `latest`, so it can't silently jump versions again in either direction. If a version change is ever needed, always back up `jellyfin_config` first — never rely on being able to roll back after the fact.
- **Theme status**: Staying on the `elegantfin-jf12` overlay CSS approach (partial compatibility) rather than chasing full Legacy-UI parity, since that would require a fresh non-migrated Jellyfin instance.

## 2026-09-14 — Finalized Physical Hardware Specifications & Drive Mappings

- **Context**: The physical assembly and operating hardware configuration was formally verified against live system metrics (`lscpu`, `lsblk`, `lspci`, `dmidecode`).
- **Settled Hardware Configuration**:
  - **Host Mini PC**: Lenovo ThinkCentre M710q Tiny with Intel Core i5-7500 (4C/4T, 3.40GHz) and 32GB DDR4 RAM. The CPU specification is finalized as i5-7500 Gen-7.
  - **Gigabit Switch**: Mercusys MS105G (5-Port Gigabit Desktop Switch) deployed between the ISP router, Main PC, and Homelab node for full 1Gbps LAN throughput.
  - **M.2 NVMe Expansion**: LM 418 M.2 NVMe NGFF M Key to 5-Port SATA III 3.0 Card with Taiwan JMicron JMB585 chipset heatsink used to breakout PCIe into 5 native SATA III ports.
  - **OS Drive Adapter**: Native internal 2.5" bay fitted with a SATA to M.2 SATA NGFF B+M Key converter card running a 256GB MidasForce M.2 SATA SSD.
  - **Active 3-HDD Topology**:
    - `sdc1`: 2TB 3.5" WD Green (`WD20EZRX-00DC0B0`) mounted at `/mnt/hdd-music` for music streaming + local backups.
    - `sdb2`: 1TB 2.5" Toshiba (`MQ04ABF100`) mounted at `/mnt/hdd-media` for movies, anime, manga, and downloads.
    - `sdd2`: 1TB 3.5" Seagate Barracuda (`ST1000DM010-2EP102`) mounted at `/mnt/hdd-cloud` for Nextcloud, Syncthing, and shared LAN storage.

## 2026-09-13 — Adopt Komga as primary manga reader; decommission Kavita

- **Context**: Evaluated Kavita vs Komga side-by-side using the identical WebP reader library at `/mnt/hdd-media/manga-reader`.
- **Reasoning**:
  - Komga natively maps nested directories (`<Category>/<Artist>/<Title>.cbz`) directly to Series and Books without requiring archive metadata alterations or SQLite manual patching.
  - Komga delivers a cleaner reading UI, faster scanning, lightweight resource usage, and first-class Mihon/Tachiyomi OPDS sync.
- **Action**:
  - Deployed `gotson/komga:latest` on port `25600` via `configs/docker-compose/komga.yml`.
  - Stopped and removed Kavita container and `kavita_config` volume on `docker-host`.
  - Removed `configs/docker-compose/kavita.yml`.

## 2026-09-13 — Homelab Dashboard absorbs health-check, git auto-deploy, and backup timer; Tailscale serve & Scrutiny dropped

- **Systemd Timers (`health-check.timer`, `git-deploy.timer`, `homelab-backup.timer`) skipped**:
  - The user requested skipping these host-level systemd timers because **Homelab Dashboard (Cockpit)** already handles live container monitoring, health states, and project deploys natively.
  - Backup triggers and scheduling will also be built as a native feature directly into Homelab Dashboard / Cockpit rather than managing background systemd timers.
- **`tailscale serve` & `scrutiny` dropped**:
  - Container health and system metrics are visualized in Homelab Cockpit; drive SMART scrutiny is unnecessary for current scope.
  - Services are reached via Tailscale IP or Cloudflare Tunnel, eliminating the need for `tailscale serve` subdomains.
- **Backup Stack (`rclone` + `restic`) & HDD Music Staging Cleanup**:
  - `rclone` (v1.60.1) and `restic` (v0.16.4) installed on `docker-host` (LXC 100).
  - Cleaned up 1.3 TB of leftover migration staging (`from-sdb`, `from-sdd`) on `/mnt/hdd-music` (`/dev/sdc1`).
  - Relocated ~717 GB of music (`/mnt/hdd-cloud/Music` and `/mnt/hdd-media/Music`) into `/mnt/hdd-music/jellyfin/music`. This dropped HDD-Cloud usage from 90% down to 11% (freeing 779 GB).
  - Updated `scripts/backup.sh` with automatic fallback to `/mnt/hdd-music/backups` and optional offsite sync to `gdrive:homelab-backups` via `rclone`.

## 2026-09-10 — homelab-sentinel moved to Telegram, consolidated + scope expanded

Supersedes the 2026-08-26 "Discord monitoring bot scoped to monitoring only" decision. The bot
(`srytmj/homelab-sentinel` repo, still built in its own Claude Code session) moves from Discord
to **Telegram** (`python-telegram-bot`) and consolidates 4 roles into one bot:

1. **Push alerts** (the original monitoring job — container down, resource thresholds)
2. **Interactive read-only queries** — "disk usage?", "what's running?", "last backup?" — no
   state changes, low risk
3. **Short QnA** — general questions, via **Gemini API free tier** (Google AI Studio). This is
   a real, separate API product — NOT the Google AI Pro consumer subscription (which has no API
   and must not be reverse-engineered), and unrelated to the earlier-declined 9router.
4. **Whitelisted management** — a fixed menu of vetted actions (`/restart <service>`,
   `/deploy <project>`, `/backup-now`, `/logs <service>`), each mapped to a specific safe
   script. Destructive actions require a `/confirm` step.

**Explicitly NOT built:** arbitrary LLM-driven command execution (the "AI ops-agent" idea
already dropped). The bot cannot do anything outside its command whitelist — the LLM only
phrases answers / handles QnA, it does not decide and run shell commands.

**Auth:** the bot only responds to the owner's Telegram user ID (hardcoded allowlist); messages
from anyone else are ignored. Outbound-only connection to Telegram's API, consistent with
Tailscale-only (no inbound port).

**Why consolidate (vs. keeping a separate Discord alert bot + Telegram interactive bot):** one
bot, one codebase, one platform to check. Discord is dropped entirely.
