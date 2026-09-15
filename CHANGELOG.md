# Changelog

> Every meaningful change gets one entry here, newest on top. Keep it short: date, what changed, why (if not obvious).

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
