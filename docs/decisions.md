# Decisions Log

> Records WHY something was chosen, so future-you (or Claude Code) doesn't re-litigate settled questions
> without new information. Add a new dated entry whenever a meaningful trade-off is decided.

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
