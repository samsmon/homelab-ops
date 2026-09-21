# Decisions Log

> Records WHY something was chosen, so future-you (or Claude Code) doesn't re-litigate settled questions
> without new information. Add a new dated entry whenever a meaningful trade-off is decided.

## 2026-09-21 — Plan: post-mortem `fio` stress test on `hdd-music` (only if it stays in service)

- **Status: PLANNED, NOT EXECUTED.** Lowest priority of the open `hdd-music` plans — do this last, after the rescue finishes (`CHANGELOG.md` (57)/(59)) and the seller RMA/warranty outcome (see the wording drafted in-chat 2026-09-20) is known.
- **Goal**: find a rough, practical "safe usage" guideline for this drive's NCQ-heavy/random-small-file failure mode (see (59)'s root-cause writeup), in case it ends up staying in service for the cold-backup role instead of being replaced by the seller.
- **Explicitly NOT the goal**: finding a precise, reliable failure threshold. This is a controller/firmware-level intermittent fault, not a fixed performance ceiling — a test run could pass at high load one day and fail at low load another. Any numbers this produces are a rough caution guide, not a guarantee, and should be documented as such wherever they're written up.
- **Only run this if**: the seller does not replace/refund the drive, and the user decides to keep using it (in the cold-backup-only role from the 2026-09-21 3-drive-reshuffle plan above). **Skip entirely if the drive gets replaced** — a healthy replacement drive doesn't need this.
- **Planned approach**: use `fio` on `pve` (or wherever the drive ends up mounted) with a tiered set of scenarios, run one at a time, each observed live against `journalctl -kf | grep -i ata` (or whatever ata port it enumerates as) and `dmesg -Tw`:
  1. Large sequential write (backup-pattern baseline — expected to pass, per today's evidence).
  2. Random small-file read/write with increasing queue depth (iodepth 1 → 4 → 8 → 16 → 32), watching for the first sign of link resets / `failed to IDENTIFY` / command aborts at each tier.
  3. Stop increasing as soon as any failure signal appears — that tier and below becomes the rough "avoid going above this" guidance, not a certified-safe number.
- **Output**: a short guideline documented in `docs/architecture.md`'s drive table (e.g. "avoid concurrent/queued small-file I/O above iodepth N based on YYYY-MM-DD fio test — not a guarantee, controller fault is intermittent") to inform how `scripts/backup.sh`/`rclone`/whatever writes to this drive going forward (e.g. capping `rclone`'s `--transfers`/`--checkers` concurrency if it turns out concurrency is the real trigger, not just file-size/randomness).

## 2026-09-21 — Plan: full 3-drive role reshuffle (hdd-cloud→music, hdd-music→backup, Nextcloud/Syncthing→hdd-media)

- **Status: PLANNED, NOT EXECUTED.** Supersedes/extends the 2026-09-20 "repurpose `hdd-music` as cold-backup" plan below with a fuller picture — that plan only covered what happens *to* `hdd-music`; this one covers where everything currently *on* it and *on* `hdd-cloud` ends up. Blocked on the same thing: the in-progress `hdd-music` rescue (`CHANGELOG.md` (57)/(58)/(59)) finishing first.
- **New role assignment** (physical drive → new logical role):
  | Physical drive | Current role | New role |
  |---|---|---|
  | Toshiba 2.5" 5400RPM 1TB (currently `hdd-cloud`, `/dev/sdb2`) | Nextcloud, Syncthing, shared LAN drop | **becomes `hdd-music`** — serves the rescued music library going forward (already the rescue's destination, so this is a natural continuation, not a second move) |
  | WD Green 2TB (currently `hdd-music`, `/dev/sdd1`/floats, the unstable one) | Music library + `scripts/backup.sh` fallback target | **becomes `hdd-backup`** — cold-backup only, consistent with the 2026-09-20 decision below (sequential-write-only access pattern, given the NCQ/small-file failure mode found today) |
  | Seagate Barracuda 7200RPM 1TB (`hdd-media`, `/dev/sdc2`) | Video/manga/qbittorrent | **stays `hdd-media`**, plus absorbs two new things (see below) |
- **`hdd-media` absorbs two things**:
  1. **Nextcloud + Syncthing** (user's explicit call: "ikut pindah ke hdd-media aja" rather than leaving them on the drive being renamed to `hdd-music`, or sourcing a 4th drive).
  2. Everything currently on `hdd-music` **except** the `music/` folder — i.e. `backups/`, `download/`, `qbittorrent/`, `lost+found/` — into a **dedicated migration folder** (exact name TBD, e.g. `/mnt/hdd-media/from-hdd-music/`) rather than merging into `hdd-media`'s existing structure, so it's easy to review/re-sort later instead of silently interleaving with `hdd-media`'s own `videos/`/`manga-raw`/`manga-reader`/`qbittorrent` layout.
- **Capacity check**: in progress as of this entry — `hdd-media` was at 633G/916G (73%) as of the last check today; need actual sizes of `hdd-cloud`'s `nextcloud/`+`syncthing/`+`shared/` folders (du was slow/backgrounded, not yet returned) plus `hdd-music`'s non-music folders before confirming it fits. **Do not execute the migration until this is confirmed to fit** — `hdd-media` is already the fullest of the three drives.
- **Why this shape (not some other reshuffle)**: keeps the music library on a drive that's *not* the currently-flaky one (removes the drive most likely to fail from serving anything live), turns the flaky WD Green into the lowest-stakes role available (cold backup — matches today's finding that it tolerates sequential access fine), and consolidates Nextcloud/Syncthing (both frequent-small-file, live-sync workloads) onto `hdd-media`, which is the highest-performance drive of the three (7200RPM) and already handles a comparably bursty workload (qBittorrent/arr-stack).
- **Still needed once capacity is confirmed and rescue finishes**:
  1. Update every compose file that hardcodes the old paths: `jellyfin.yml` (`/mnt/hdd-music/jellyfin/music`), `navidrome.yml` (`/mnt/hdd-music/jellyfin/music:ro`), `feishin` (if path-dependent), `nextcloud.yml`/`syncthing.yml` (currently `/mnt/hdd-cloud/...`), `filebrowser.yml` (mounts all three), `scripts/backup.sh` (`BACKUP_DIR` fallback currently `/mnt/hdd-music/backups`, needs to become the new `hdd-backup` role instead).
  2. Update `/etc/fstab` labels/mount points on `pve` to match the new role names (or keep device labels as-is and just document the role mapping — TBD which is less error-prone).
  3. Update `docs/architecture.md`'s drive table and `docs/services.md` once the physical moves are done.
  4. Decide the exact migration-folder name/structure for the non-music `hdd-music` leftovers on `hdd-media`.

## 2026-09-20 — Plan: repurpose `hdd-music` as cold-backup only, add encrypted offsite sync to Google Drive

- **Status: `hdd-music`→cold-backup role EXECUTED 2026-09-21 (see `CHANGELOG.md` (69)); the Google Drive/`rclone crypt` part is still PLANNED, NOT EXECUTED.** User decided 2026-09-21 not to keep waiting on the pending seller RMA conversation before settling the drive's role — finalized as cold-backup regardless of RMA outcome (a successful RMA now just means a healthier replacement inherits this role later, doesn't block anything). Drive remounted rw at `/mnt/hdd-music`, `docker-host` rebooted to pick it up.
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

- **Status: PARTIALLY SUPERSEDED 2026-09-21.** The original 4-new-LXC version of this plan was attempted and found infeasible on storage (`CHANGELOG.md` (62): only ~18GB thin-pool headroom). Executed a reduced-scope version instead — renamed the existing friends'-projects LXC 103 to `personal-hosts` and merged the user's misc personal projects into it rather than creating new LXCs (see `CHANGELOG.md` (64)). **However, `CHANGELOG.md` (66) later found the storage blocker itself was largely artificial**: `local-lvm` thin pool was at 88.80% partly because deleted files inside LXC guests never get TRIM'd back to the pool automatically. Running `pct fstrim` across all 4 LXCs (from the `pve` host, not inside the guest — unprivileged LXCs can't self-trim) dropped pool usage to 55.24%, freeing real headroom back up to ~70GB. **This reopens the option to do the full original 4-LXC split (media/personal/drive/infra) if the user still wants it** — the storage math that ruled it out no longer holds. Below is the original proposal, kept as-is for reference; if revisiting, re-check current thin-pool usage first since `personal-hosts` already exists and covers part of the original "personal" scope.
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
