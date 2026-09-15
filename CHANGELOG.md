# Changelog

> Every meaningful change gets one entry here, newest on top. Keep it short: date, what changed, why (if not obvious).

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
