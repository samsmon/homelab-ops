# Changelog

> Every meaningful change gets one entry here, newest on top. Keep it short: date, what changed, why (if not obvious).

## 2026-09-14 (1)
- **Updated Homelab Dashboard (Cockpit) to Commit a5877a4 (v1.1.3)**:
  - Pulled commits (`e77c21b` -> `a5877a4`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - **Fleet Card Sorting (`7a6860b`)**: Changed default container grid sort to Name (A-Z) and added interactive sort dropdown (Name, CPU, RAM, Network) with direction toggles.
  - **Antigravity Google Email Display (`868e3cb`)**: Dynamically extracted and displayed user's Google account email on Antigravity agent cards.
  - **Real-Time Update Engine v1.1.3 (`a5877a4`)**: Added auto-fetch git detection, 30s background polling in update banner, rebase/reset fallback for diverged branches, and T3 Code volume mapping.
  - Multi-stage image built cleanly and container `homelab-cockpit` recreated on `docker-host:8050` (`dash.suryatmaja.dev`). Verified HTTP 200 OK.

## 2026-09-13 (27)
- **Fixed Cockpit AI Agents Monitor (404) & Removed rclone Container Bloat (Commit a9b6f5b)**:
  - Fixed `Failed to fetch AI telemetry (404)` on the dashboard by registering the missing Fastify route handler `app.get('/api/ai-agents/telemetry')` connected to `AiAgentsService`.
  - Mounted T3 Code data volume (`/var/lib/docker/volumes/docker-compose_t3code_data/_data/.t3:/root/.t3:ro`) into `homelab-cockpit` to allow live monitoring of Claude Pro & Gemini turn usage, 5-hour rolling limits, and cooldowns.
  - Removed `rclone` and its unused volume mount from Dockerfile and docker-compose.yml, dropping runner alpine package footprint by over 105 MiB (from 191 MiB down to 85 MiB) and slashing rebuild times down to ~27 seconds.
  - Rebuilt and restarted `homelab-cockpit` on `docker-host:8050` (`dash.suryatmaja.dev`). Verified telemetry output with active session token.

## 2026-09-13 (26)
- **Updated StreamVault to Commit c7c8d32**:
  - Pulled commit `c7c8d32` on [srytmj/stream-vault](https://github.com/srytmj/stream-vault).
  - Resolved UI bug where modal overlay persisted on screen; added backdrop click & ESC key dismissal support across modals (`SeriesModal`, `StatsModal`, `KeyboardShortcutsModal`, `AddLibraryModal`).
  - Rebuilt image and recreated container on `docker-host:8090`. Verified healthy container status.

## 2026-09-13 (26)
- **Updated Homelab Dashboard (Cockpit) to Commit e77c21b (v1.1.2)**:
  - Pulled commits (`40362d7` -> `e77c21b`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - Portaled UI modals to document body and fixed table clipping issues in Git Projects page (`0f5e01a`).
  - Configured monorepo workspaces in root package.json, hardened updater subprocess PATH and dev dependencies, and published v1.1.2 update announcements (`e77c21b`).
  - Rebuilt production image cleanly with multi-stage build and recreated `homelab-cockpit` on `docker-host:8050` (`dash.suryatmaja.dev`). Verified live WebSocket metrics and HTTP 200.

## 2026-09-13 (25)
- **Updated StreamVault to v1.1.0 (Commit 9beab63)**:
  - Pulled latest commit `9beab63` on [srytmj/stream-vault](https://github.com/srytmj/stream-vault).
  - New features: Custom libraries management (`/api/libraries`), Folder Explorer mode, enhanced view modes, and improved softsub discovery.
  - Added named volume `stream-vault-data` mounted to `/app/server/data` for persistent custom library storage across container updates.
  - Rebuilt image and recreated container on `docker-host:8090`. Verified healthy status and tested endpoints `/api/health` and `/api/libraries`.

## 2026-09-13 (24)
- **Updated Homelab Dashboard (Cockpit) to Commit 40362d7**:
  - Pulled commits (`df24768` -> `40362d7`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - Deployed AI Agents usage monitor & T3 Code telemetry (`578c1b0`).
  - Applied prepare script dependency fix (`40362d7`) and updated versioning to `1.1.1`.
  - Rebuilt container cleanly (`homelab-cockpit`), running healthy on port 8050 (`dash.suryatmaja.dev`).

## 2026-09-13 (23)
- **Deployed StreamVault (Zero-Transcode Video Streaming) on docker-host:8090**:
  - Tested and reviewed [srytmj/stream-vault](https://github.com/srytmj/stream-vault). Confirmed zero server-side transcode architecture with JASSUB WebAssembly client-side subtitle rendering (.ass/.srt).
  - Deployed alongside Jellyfin on `docker-host` (port 8090) so Jellyfin continues serving the 717GB music collection without interruption.
  - Mounted `/mnt/hdd-media/jellyfin:/media:ro` (read-only).
  - Scanned and indexed 857 video files (416.2 GB across Anime, Movies, and TV) in milliseconds.
  - Resource usage: ~35MB RAM, 0.0% CPU transcode load during playback. Tested HTTP 206 partial content streaming successfully.
  - Committed compose definition to `configs/docker-compose/stream-vault.yml` and documented in `docs/services.md`.

## 2026-09-13 (23)
- **Deployed Feishin Web (Music Player Frontend) on Port 9180**:
  - Deployed `feishin` container (`ghcr.io/jeffvli/feishin:latest`) on `docker-host` port `9180` via `configs/docker-compose/feishin.yml`.
  - Configured to connect seamlessly with backend Navidrome (`http://192.168.18.225:4533`).
  - Provides modern dark-mode music player UI with native folder tree hierarchy navigation, playlist management, and PWA capabilities.
  - Verified resource consumption: CPU 0.00%, RAM ~6.5MB. Web UI returns HTTP 200 OK.
  - Updated `docs/services.md` and cleared task lock.

## 2026-09-13 (22)
- **Updated Homelab Dashboard (Cockpit) to Commit df24768**:
  - Pulled commits (`86aef65` -> `df24768`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - Fixed semantic version matching on `AppUpdateBanner` to eliminate false-positive update alerts and prevent stuck update modals.
  - Added baseline `version.json`, injected `AppVersionInfo` into collector snapshot, and displayed app version, git SHA, and branch in footer.
  - Added `AGENT_LOG.md` live task locking rules to the dashboard repository.
  - Built image cleanly and recreated container on `docker-host`. Live verification confirmed: `homelab-cockpit` Up, port 8050 HTTP 200 OK.

## 2026-09-13 (22)
- **Deployed Navidrome (Music Streaming Server) & Reorganized `/mnt/hdd-music`**:
  - Reorganized `/mnt/hdd-music/`: Moved music collection directly out of legacy `jellyfin/` subfolder to `/mnt/hdd-music/music` (clean root-level media structure, preparing for Jellyfin phase-out).
  - Deployed `navidrome` container (`deluan/navidrome:latest`) on `docker-host` port `4533` via `configs/docker-compose/navidrome.yml`.
  - Configured zero-transcode direct streaming (`ND_ENABLETRANSCODINGCONFIG=false`), scanning `/mnt/hdd-music/music:ro`.
  - Verified Web UI and initial scan completed across music files (FLAC/MP3) with HTTP 200 OK.
  - Updated `configs/docker-compose/jellyfin.yml`, `docs/services.md`, and `docs/architecture.md` to reflect the updated path.

## 2026-09-13 (21)
- **Updated Homelab Dashboard (Cockpit) to Commit 86aef65**:
  - Pulled latest commits (`43abd62` -> `86aef65`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - **Self Updater & Glassmorphism UI**: Added AppUpdateBanner, app-update backend service, robust transition animations, and maximized glassmorphism styling.
  - Built image cleanly via `docker compose build` then executed recreation cycle `docker compose down && docker compose up -d` on `docker-host` to prevent Compose v5.5.1 recreate race condition.
  - Verified container healthy on port 8050 (`dash.suryatmaja.dev`), live WebSocket streaming active, HTTP 200 OK.

## 2026-09-13 (21)
- **Added Mandatory User Confirmation & Session Scope Rule to Agent Protocol**:
  - Clarified that `homelab-ops` is strictly an administrative, infrastructure, and maintenance session. Prohibited agents from scaffolding new projects/apps in this workspace.
  - Enforced a strict rule in `CLAUDE.md`: any modification to running code, container configurations, or application environments requires explicit prior approval from the user.

## 2026-09-13 (20)
- **Implemented Multi-Agent Synchronization, Task Locking & Token Conservation Protocol**:
  - Added `CURRENT_OPS.md` as active task/service lock registry across parallel AI agents (T3 Code multi-session, Claude Code, Gemini/Antigravity, Cursor, Roo) to eliminate race conditions and collisions.
  - Updated `CLAUDE.md` and created symlinks `AGENTS.md` and `.cursorrules` establishing strict agent behavior: mandatory `git pull` on start, lock registration in `CURRENT_OPS.md`, token-saving rules (no full CHANGELOG reads, log tail capping), single-shot batched SSH heredocs, anti-truncation git diff verification, and immediate commit & push upon task completion.

## 2026-09-13 (19)
- **Decommissioned extra T3 Code instances (`t3code-2`, `t3code-3`, and `apps-host:t3code`)**:
  - Per user request, consolidated back to a single primary T3 Code instance (`t3code` on `docker-host` port 9001).
  - Stopped and removed containers `t3code-2` and `t3code-3` on `docker-host` (LXC 100), deleted their named volumes (`t3code-2_t3code_data_2`, `t3code-3_t3code_data_3`), and removed compose configs `configs/docker-compose/t3code-2.yml` and `configs/docker-compose/t3code-3.yml`.
  - Stopped and removed container `t3code` on `apps-host` (LXC 101), removed volume `t3code_t3code_data`, and removed directory `/opt/t3code`.
  - Updated `docs/services.md` and verified only the primary `t3code` instance remains active.

## 2026-09-13 (19)
- **Restored and synchronized `docs/architecture.md` & initialized session maintenance**:
  - Found `docs/architecture.md` was accidentally truncated in commit `9714fd7` down to a single snippet. Fully restored hardware specs, storage topology, virtualization topology (PVE, LXC 100 docker-host, LXC 101 apps-host), network IPs, active HDD allocation, and Windows Samba configuration while maintaining the updated manga-raw / manga-reader / Komga topology.
  - Verified live server state across all nodes (`proxmox` 192.168.18.224, `docker-host` 192.168.18.225, `apps-host` 192.168.18.226). All 18 docker-host containers, 2 apps-host containers, systemd services (`smbd`, `wsdd`, `cloudflared`, `manga-optimizer`, `tailscaled`), and mounts are running healthy.
  - Configured persistent SSH configuration for fast, reliable heredoc batching.

## 2026-09-13 (18)
- **Deployed 2 more T3 Code instances on docker-host + 1 on apps-host**, per user request, so remote/mobile sessions no longer contend for a single instance.
  - docker-host: `t3code-2` (port 9002) and `t3code-3` (port 9003), added via `configs/docker-compose/t3code-2.yml` / `t3code-3.yml`, reusing the existing `./t3code` build context (same Dockerfile as the original `t3code` on 9001). Each compose file has an explicit `name:` line since all 3 files live in the same directory and would otherwise collide on Compose's default project-name-from-directory behavior.
  - apps-host (LXC 101, `192.168.18.226`, discovered this session to be a fully independent LXC with its own Docker daemon, no `shared_net`, no `/mnt/homelab_projects`): new standalone `t3code` instance on port 9001, deployed to `/opt/t3code/` on that LXC with a copy of the same Dockerfile/entrypoint. Not yet under git — apps-host doesn't have an established repo-checkout convention like docker-host's `GIT_PROJECTS_ROOT`, worth deciding later.
  - Builds initially failed to start in-session (background shell task was lost before the build ran) — re-ran via `nohup ... & disown` so they'd survive independently of the SSH session; all 3 came up clean on retry.
  - Minted a T3 Connect pairing token for each new instance via `npx t3 pair --ttl 168h --label <name>` (168h = 7 days, matching the user's explicit request). Tokens given to the user directly in-session — never committed here, they're bearer credentials.
  - Each new instance still needs `claude auth login` run interactively by the user themselves inside the container — not something the assistant can or should do on the user's behalf.

## 2026-09-13 (17)
- **Fixed the homelab dashboard going down when used to redeploy itself**: user triggered the dashboard's own "pull and redeploy" feature on the `homelab-dashboard` project (i.e. the dashboard redeploying itself), which hit the same Docker Compose container-naming race condition seen twice before (2026-09-13 (11) and (14)) — the old `homelab-cockpit` container got killed (exit 137) but the replacement got stuck in `Created` state under a mangled name (`4274352760e7_homelab-cockpit`), leaving the dashboard completely unreachable (connection refused on port 8050) with no way to self-recover since the tool that would fix it was the thing that was down. Fixed via SSH: `docker rm -f` both broken containers, then a full `docker compose down && docker compose up -d` cycle. Verified HTTP 200.
  - **Root cause identified, not just patched again**: Docker Compose v5.5.1 (fairly new major version) appears to have a recreate race — the default rebuild command this project uses, `compose up -d --build` (defined in `server/src/services/git-projects.service.ts` as `'compose-up-build'`), doesn't reliably wait for the old container to fully release its name before creating the replacement.
  - **The dashboard's own codebase already has a safer built-in option**: `'compose-up-build-force-recreate'` (`compose up -d --build --force-recreate`) is defined alongside the default but isn't what's configured for the dashboard's own project entry. Recommended switching the dashboard's own "Rebuild Command" setting (in its Git Projects UI) to the force-recreate variant, since that's an existing toggle rather than something needing a source patch — did not change it myself, since it's a per-project UI setting the user should choose deliberately, especially given the dashboard would be redeploying itself.
  - **Standing risk while unresolved**: using the dashboard's pull-and-redeploy feature to redeploy the dashboard itself is self-referential and risky given this Compose bug — if it hits, the dashboard goes down and needs external SSH intervention to recover (the fix can't be applied from within the tool that's broken). Worth deciding whether to switch the rebuild command, or add a documented manual-recovery runbook, or both.

## 2026-09-13 (16)
- **Fixed `/blog/` and `/projects/` returning 403 Forbidden** on the public `portfolio` site. SvelteKit's static adapter emits list routes as a flat `blog.html`/`projects.html` file alongside a same-named directory holding only the child-slug pages (no `index.html` inside). With `try_files $uri $uri/ $uri.html /404.html`, a trailing-slash request like `/blog/` matched the directory at the `$uri/` step, found no index file inside (autoindex is off), and nginx returned 403 without ever trying `$uri.html`.
  - **First fix attempt was wrong** (commit `f51e993`): reordered to `try_files $uri $uri.html $uri/ /404.html`, assuming `$uri.html` would resolve to `blog.html`. It doesn't — `$uri.html` is plain string concatenation, and when `$uri` already ends in `/` (as it does for a directory-style request), the result is the literal path `/blog/.html`, not `/blog.html`. Verified still 403 after rebuild — did not guess a third blind fix, investigated instead.
  - **Correct fix** (commit `1ef0a9c`): added a regex location `location ~ ^(?<base>.+)/$ { try_files $base.html $uri $uri/ /404.html; }` that captures everything before the trailing slash into `$base`, so `$base.html` correctly resolves to `blog.html`/`projects.html`. Confirmed by testing directly inside the container (`docker exec ... curl http://localhost/blog/`) before trusting the external result, since an external retest immediately after redeploy briefly still showed 403 (right after container recreation — resolved a few seconds later on retest, likely a startup race rather than a real fix failure).
  - Verified stable across repeated checks: homepage, an individual blog post, an individual project detail page, `/blog/`, and `/projects/` — all 200, both via direct LAN IP (`192.168.18.225:3080`) and the public Cloudflare Tunnel domain (`suryatmaja.dev`).
  - Both commits pushed to [srytmj/portofolio](https://github.com/srytmj/portofolio) (as user Maja).

## 2026-09-13 (15)
- **Consolidated the `portfolio` project's two divergent git checkouts, fixed a real gap in its GitHub repo, renamed the container**:
  - Found two separate clones of [srytmj/portofolio](https://github.com/srytmj/portofolio) on docker-host: the original `/opt/projects/portfolio/` (created when this repo was first deployed, 2026-09-11) and a newer `/mnt/homelab_projects/portofolio/` (created by another agent, matching the homelab dashboard's `GIT_PROJECTS_ROOT` convention for its Git Projects pull-and-redeploy feature) — only the *old* location was actually wired to the running container.
  - Root cause of the user's reported error (dashboard's pull-and-redeploy: `Command failed: docker compose up -d --build / no configuration file provided: not found`): `docker-compose.yml` had only ever existed as a file manually placed on the server back on 2026-09-11 — it was never committed to the actual `srytmj/portofolio` GitHub repo (only `Dockerfile`/`nginx.conf` were). The newer git-clone-based checkout therefore had no compose file at all.
  - Fixed by committing `docker-compose.yml` to the `portofolio` repo itself (as user Maja, per that repo's own contributor rules) so the dashboard's git-pull-based redeploy is now self-sufficient. Also renamed the container from `yorha-portfolio` to `portofolio`, matching the repo's actual name and removing the container-name-vs-folder-name mismatch that caused earlier confusion in this session too.
  - **Git history note**: the compose file was first committed directly on docker-host's checkout, but that environment has no push credentials (different from this session's own environment, which does) — pushing from two different clones with the same diff would have created divergent branch tips. Avoided that by `git reset --hard HEAD~1` on docker-host's local commit, pushing the equivalent commit (`e21c0cc`) from this session's own clone instead, then a clean `git pull` (fast-forward) back on docker-host.
  - Redeployed from `/mnt/homelab_projects/portofolio/` (stopped and removed the old `yorha-portfolio` container first to avoid a port 3080 conflict). Verified: local HTTP 200 on port 3080, and the public site (`https://suryatmaja.dev`, via the existing Cloudflare Tunnel — unaffected by the container rename since the tunnel points at `localhost:3080`, not a container name) also HTTP 200.
  - Updated `docs/services.md` and `configs/docker-compose/portfolio.yml` in this repo to match. The stale `/opt/projects/portfolio/` checkout was left in place (untouched, no longer used) rather than deleted, in case anything else still references it — worth a cleanup pass later.

## 2026-09-13 (14)
- **Updated Homelab Dashboard (Cockpit) to Commit 048e35b**:
  - Pulled commits (`c37af9d` -> `048e35b`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard) — these had already been `git pull`ed into the working tree at some earlier point (repo showed a commit timestamp newer than the running container's build time) but never rebuilt/redeployed, so the live dashboard was 2 commits stale until this fix.
  - **Deploy Baseline Self-Heal**: fixes a stale deploy baseline getting permanently stuck, and adds a manual resync button as a backup.
  - Docs updated to describe the self-heal + resync button.
  - **Real Docker bug hit and fixed**: `docker compose up -d --build` failed to recreate the container — `Error when allocating new name: Conflict. The container name "/homelab-cockpit" is already in use` — the old container failed to fully stop/remove before Compose tried to recreate it in the same command. Manually `docker stop && docker rm -f` cleared it, but that left a second issue: Compose then created the replacement under a mangled name (`2977d6d47dfb_homelab-cockpit`) instead of the clean `homelab-cockpit` from `container_name:` in the compose file — likely leftover project-state confusion from the interrupted recreate. Fixed with a full `docker compose down && docker compose up -d` cycle, which recreated it correctly. Verified HTTP 200 on port 8050 (`dash.suryatmaja.dev`).

## 2026-09-13 (13)
- **Patched `scripts/manga-optimizer.py` to add a fallback for optimization failures**: any archive that fails the ZIP-based optimization step (e.g. a RAR file mislabeled `.cbz`, or any other unreadable-as-zip case) is now hardlinked (falling back to a copy if hardlinking fails) into `manga-reader` unmodified, instead of being silently dropped with just a log line — this is exactly what caused the 93-file gap fixed in the previous entry, and would have recurred for any future non-ZIP archive added to `manga-raw`. Restarted `manga-optimizer.service` on docker-host to load the patch (confirmed via a fresh full re-scan of all 2227 archives, clean startup, no new errors — the previously-failing 93 files were already present from the manual fix so the daemon skipped them rather than re-triggering the new fallback path, but the code is in place for the next occurrence).

## 2026-09-13 (12)
- **Fixed 93 manga archives missing from the optimized reader library**: checked progress of the `manga-optimizer.service` daemon (running since 04:26 UTC, ~3h13m CPU time) and found it had genuinely finished all work it *could* do — 2134 of 2227 raw archives successfully optimized/hardlinked into `/mnt/hdd-media/manga-reader`, but 93 files failed with `File is not a zip file` and were silently dropped with **no fallback copy**, meaning those 93 titles were completely invisible to Komga (mounted on `/mnt/hdd-media/manga-reader`) despite existing fine in the raw source. Root cause: these are RAR-format archives mislabeled with a `.cbz` extension (`file` confirmed "RAR archive data, v5") — the optimizer script only handles ZIP-based CBZ, so it can't compress them, but the correct fallback (copy the original through unmodified) wasn't in place for this failure case. Fixed by hardlinking all 93 files from `manga-raw` into the matching path under `manga-reader` as-is (0 additional disk usage, same as the optimizer's own "already light" hardlink path) — reader library now has full 2227/2227 parity with the raw source. **User needs to manually trigger a Komga library rescan** to pick up the newly-visible files (didn't do this myself — no stored Komga admin credentials in this session). Worth a follow-up fix to `scripts/manga-optimizer.py` itself: add a fallback hardlink-original step when optimization fails, so this doesn't silently recur for future non-ZIP archives added to `manga-raw`.

## 2026-09-13 (11)
- **Updated Homelab Dashboard (Cockpit) to Commit c37af9d**:
  - Pulled commits (`7a23c1c` -> `c37af9d`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - **Automatic Deploy Baseline**: Deploy baseline is now set automatically when a project starts being tracked, instead of requiring a manual first mark.
  - **Sidebar/Content Centering Fix**: Centered the sidebar and content area as a single block (previous layout had them drifting independently).
  - **Docs**: Documented the automatic deploy baseline behavior.
  - Rebuilt (`docker compose up -d --build`) and verified running on port 8050 (`dash.suryatmaja.dev`), HTTP 200.

## 2026-09-13 (10)
- **Updated Homelab Dashboard (Cockpit) to Commit 7a23c1c**:
  - Pulled commits (`b9497bf` -> `7a23c1c`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - **Header & Sidebar Layout Fix**: Positioned the header above the sidebar row (full width top header) instead of beside it.
  - **Git Projects Auto-Deploy & Deployed Marker**: Added opt-in auto-deploy for tracked git repositories and a manual "Mark as Deployed" action.
  - Cleaned orphaned containers and verified running on port 8050 (`dash.suryatmaja.dev`).

## 2026-09-13 (9)
- **Updated Homelab Dashboard (Cockpit) to Commit b9497bf**:
  - Pulled latest commits (`fa16940` -> `b9497bf`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - **Collapsible Floating Sidebar**: Relocated navigation tabs to a modern left floating sidebar with expand/collapse toggle.
  - **Clock & Weather Widget**: Integrated dynamic live clock and opt-in geolocation weather widget in the header.
  - **Personal Bookmarks / Shortcuts Section**: Added bookmarks management on the Overview page with custom categories, icons, and URLs backed by `/api/bookmarks`.
  - **Docker & Remote SSH Processes**: Enhanced Processes page with tabs for host processes, Docker container processes, and remote SSH host processes.
  - **Git Projects**: Fixed transmission of `localPath` and `rebuildCommand` to the frontend client.
  - Rebuilt and verified running on port 8050 (`dash.suryatmaja.dev`).

## 2026-09-13 (8)
- **Updated Homelab Dashboard (Cockpit) to Commit fa16940**:
  - Pulled commits (`028f7fa` -> `fa16940`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - **New Processes Page (`/processes`)**: Added per-process tracking for CPU%, Memory%, and Disk I/O backed by `/api/processes`.
  - **Split Infra View**: Restyled Disk Performance Panel and reorganized Infra page layout into dual views.
  - **Git Projects Picker Upgrades**: Added host filter and search filter to Git Project Modal, plus manual refresh button on Git Projects page.
  - Rebuilt and verified running on port 8050 (`dash.suryatmaja.dev`).

## 2026-09-13 (7)
- **Deployed FileBrowser on Port 8085 ()**:
  - Deployed `filebrowser/filebrowser:latest` as an ultra-lightweight Google Drive alternative.
  - Resource consumption: ~14MB RAM (compared to Nextcloud's 2GB) and 0% CPU at idle.
  - Multi-drive unified storage mount:
    - Root (`/srv`): `/mnt/hdd-cloud` (Personal cloud, Downloads, Images, Tugas, etc.)
    - Submount (`/srv/media`): `/mnt/hdd-media` (Raw manga, reader, media)
    - Submount (`/srv/music`): `/mnt/hdd-music` (Music library)
  - Full drag-and-drop, public link sharing with password/expiry, direct video/audio/photo/code previews.
  - Zero database indexing lag: any files created or modified via Samba/Windows Explorer appear instantly in the web UI.
  - Initial admin user created: `admin` / `Admin@Homelab2026!`.
  - Service ready to be routed via Cloudflare Zero Trust tunnel to `drive.suryatmaja.dev` pointing to `http://100.89.249.96:8085` (or LAN `http://192.168.18.225:8085`).

## 2026-09-13 (6)
- **Decommissioned Kavita in Favor of Komga as Primary Manga Reader**:
  - Stopped and removed `kavita` container and `kavita_config` volume on `docker-host` (LXC 100), freeing port `5000`.
  - Removed `/opt/infra/kavita` and `configs/docker-compose/kavita.yml`.
  - Formally adopted Komga on port `25600` (`/opt/infra/komga`) as the homelab standard manga reader.
  - Documented decision in `docs/decisions.md` and updated `docs/services.md`.

## 2026-09-13 (6)
- **Hardened Nextcloud Resource Limits & Apache Worker Tuning**:
  - Configured strict Docker CPU and memory caps (`cpus: 1.25`, `mem_limit: 2048m`) in `configs/docker-compose/nextcloud.yml`.
  - Added Apache MPM prefork tuning snippet (`mpm-tuning.conf`) mounted to `/etc/apache2/conf-enabled/mpm-tuning.conf`, restricting `MaxRequestWorkers` from unconstrained 150 workers down to 15.
  - Set Nextcloud system preview limits (`preview_max_x: 1024`, `preview_max_y: 1024`, `preview_max_filesize_image: 25MB`) via `occ`.
  - Prevents uncontrolled CPU and RAM spikes during bulk folder/image browsing.

## 2026-09-13 (5)
- **Deployed Komga Manga & Comic Server for Direct Comparison with Kavita**:
  - Deployed `gotson/komga:latest` on `docker-host` (LXC 100) via `configs/docker-compose/komga.yml` (`/opt/infra/komga`).
  - Exposed on dedicated port `25600` (`http://192.168.18.225:25600`), connected to `shared_net`.
  - Mounted optimized reader volume `/mnt/hdd-media/manga-reader` to `/data` so both Komga and Kavita share the exact same lightweight WebP reader source for side-by-side evaluation.
  - Initialized SQLite database and verified HTTP 200 health response.
  - Registered Komga in `docs/services.md`.

## 2026-09-13 (5)
- **Updated Homelab Dashboard (Cockpit) to Commit 028f7fa**:
  - Pulled latest commits (`d631c72` -> `028f7fa`) on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - **New In-Browser SSH Terminal**: Integrated interactive shell bridge (`xterm.js` + `ssh2`) with WebSocket PTY streaming.
  - Generated dedicated ED25519 keypair (`/root/.ssh/id_ed25519`) on `docker-host`, authorized across:
    - `proxmox` (`root@192.168.18.224`)
    - `docker-host` (`root@192.168.18.225`)
    - `apps-host` (`root@192.168.18.226`)
  - Configured `SSH_TARGETS` and `SSH_PRIVATE_KEY_PATH` in `.env`.
  - **New Disk Performance Panel**: Real-time throughput metrics (read/write MB/s) per storage volume calculated from `/proc/diskstats`.
  - Rebuilt container image and verified live on port 8050 (`dash.suryatmaja.dev`).

## 2026-09-13 (4)
- **Updated Homelab Dashboard (Cockpit) to Commit d631c72 (9 Commits)**:
  - Pulled commits from [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard) (`fbd5e84` -> `d631c72`).
  - **New Git Projects Page**: Track remote GitHub commits on homelab repos, with interactive Git Pull and container Rebuild buttons directly in UI.
  - **New Backup Panel in Infra Page**: On-demand and scheduled rclone sync, snapshot restore, and configuration archive import.
  - Added `GIT_PROJECTS_ROOT=/mnt/homelab_projects`, `RCLONE_CONFIG_PATH=/root/.config/rclone/rclone.conf`, and `BACKUP_SOURCE_PATHS=/app/data,/projects` into `.env`.
  - Rebuilt Docker image with `git`, `docker-cli`, `rclone`, and `unzip`.
  - Verified live deployment on port 8050 (`dash.suryatmaja.dev`).

## 2026-09-13 (3)
- **Deployed Manga Auto-Optimizer Pipeline Daemon & Kavita Mount Migration**:
  - Implemented event-driven background pipeline [scripts/manga-optimizer.py](scripts/manga-optimizer.py) registered as systemd service `manga-optimizer.service` on `docker-host` (LXC 100).
  - Configured two-tier manga architecture:
    - Master Ingest (`/mnt/hdd-media/manga-raw`): original source files, directly accessible via dedicated Samba share `\docker-host\manga` for management, adding files, and organizing folders.
    - Optimized Reader Target (`/mnt/hdd-media/manga-reader`): auto-generated WebP archives (max 2048px width, quality 85) with exact folder mirroring, mounted to Kavita container (`/manga`).
  - Implemented smart hardlinking: lightweight archives (already <=45MB and WebP) are hardlinked instantaneously with 0 additional disk usage.
  - Heavy raw archives (e.g. 933MB) shrink by 91-94% down to ~57-84MB, reducing single-page image payloads from 13MB down to ~250KB for instant page flipping without stream timeouts.
  - Watchdog daemon handles real-time file creation, folder renames, file moves, and deletions with zero manual intervention.
  - Updated `configs/docker-compose/kavita.yml`, `docs/architecture.md`, `docs/services.md`, and `docs/decisions.md`.

## 2026-09-13 (2)
- **Organized Kavita Manga/NSFW Library Structure by Artist Grouping**:
  - Processed 309 manga/doujinshi files (`.cbz`) across `/mnt/hdd-media/kavita/manga/nsfw/` (`Official Translate`, `Unofficial`, `JP`).
  - Extracted artist tags matching regex `^\[(.*?)\]\s*(.+)$` and grouped items into dedicated artist directories (`<Artist>/<Title>.cbz`).
  - Total grouped: 184 files into 45 artist folders in `Official Translate`, 104 files into 35 artist folders in `Unofficial`, and 21 files into 10 artist folders in `JP`.
  - Maintained full `777` permissions and file access for Samba share (`\\192.168.18.225\homelab\...`) and Kavita docker container.
  - Triggered Kavita library scan via API (`/api/Library/scan?libraryId=2`) to re-index all artist series and covers.

## 2026-09-13 (1)
- **Completed HDD Staging Cleanup, Music Relocation, and Backup Stack Setup**:
  - Relocated ~717 GB of music from `/mnt/hdd-cloud/Music` (683 GB) and `/mnt/hdd-media/Music` (34 GB) into `/mnt/hdd-music/jellyfin/music/`.
  - Purged leftover migration staging folders (`from-sdb` and `from-sdd`) on `/mnt/hdd-music` (`/dev/sdc1`), recovering over 580 GB of staging clutter.
  - Slashed `hdd-cloud` disk usage from 90% (96 GB free) down to 11% (779 GB free), leaving ample room for Nextcloud and sync storage.
  - Installed `rclone` (v1.60.1) and `restic` (v0.16.4) on `docker-host` (LXC 100).
  - Enhanced `scripts/backup.sh` with automatic target fallback to `/mnt/hdd-music/backups` and optional offsite sync to Google Drive (`gdrive:homelab-backups`) via rclone. Verified successful test backup run in 2 seconds.
  - Documented architectural decision to integrate backup and watchdog management into Homelab Dashboard / Cockpit rather than standalone systemd timers.

## 2026-09-12 (21)
- **Updated Homelab Cockpit to Commit fbd5e84**:
  - Pulled commit `fbd5e84` on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - Fixed Command Palette hover state: prevented mouse hover from constantly snapping selection to the last item.
  - Rebuilt image and restarted container `homelab-cockpit` on port `8050`. Verified active live snapshot & WebSocket stream.

## 2026-09-12 (20)
- **Updated Homelab Cockpit to Commit 5d8fbde**:
  - Pulled commits `930c088`, `6fe9318`, and `5d8fbde` on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard).
  - Pinned containers only: command palette launcher redesigned to focus purely on pinned services.
  - Added self-healing URL migration for older pinned URLs in `pins.service.ts`.
  - Rebuilt image and restarted container `homelab-cockpit` on port `8050`. Verified live WebSocket connection.

## 2026-09-12 (19)
- **Updated Homelab Cockpit Compose Configuration & Multi-Host Proxmox Sync**:
  - Injected `env_file: .env` into `/mnt/homelab_projects/homelab-dashboard/docker-compose.yml`.
  - Enabled `NODE_TLS_REJECT_UNAUTHORIZED=0` inside container, resolving Proxmox VE API SSL verification failures and restoring real-time hypervisor telemetry.
  - Enabled multi-host docker polling (`apps-host=tcp://192.168.18.226:2375`) and container monitoring across docker-host and apps-host.
  - Committed and pushed commit `39c80b0` to `srytmj/homelab-dashboard` and pushed `homelab-ops` upstream.

## 2026-09-12 (18)
- **Restored Jellyfin to Clean Stock Configuration**:
  - Removed `/dev/dri` passthrough mount from `/opt/infra/jellyfin/docker-compose.yml` to match repository specification.
  - Reset `encoding.xml` options (`HardwareAccelerationType: none`, `EnableHardwareEncoding: false`, cleared `VaapiDevice` and `HardwareDecodingCodecs`).
  - Purged stale transcode cache and cleanly recreated container via `docker compose down && docker compose up -d`.
  - Verified healthy HTTP 200 responses for playback API, HLS remuxing, and subtitle delivery.

## 2026-09-12 (17)
- **Reverted Jellyfin Hardware Acceleration**:
  - Reverted `<HardwareAccelerationType>` back to `none` in Jellyfin encoding configuration.
  - Resolved subtitle rendering/extraction regression caused by hardware transcoding pipeline.

## 2026-09-12 (16)
- **Updated Homelab Cockpit to Commit 06a17f4**:
  - Pulled commits `cabb1db`, `dc00430`, and `06a17f4` (dynamic storage label detection, dynamic hardware detection, pinned link priority fix).
  - Rebuilt and restarted container `homelab-cockpit` on port `8050`.
  - Storage matrix and dashboard now natively read dynamic hardware specs without hardcoded labels.

## 2026-09-12 (15)
- **Standardized Execution Performance & Anti-Freeze Protocol in CLAUDE.md**:
  - Enforced one-shot batched SSH execution to eliminate round-trip latency.
  - Mandated bounded timeouts (`timeout`) and clean foreground command execution to permanently prevent ghost background task accumulation in T3 Code.
  - Updated agent rules across all AI harnesses and sessions.

## 2026-09-12 (14)
- **Enabled Intel QuickSync Hardware Acceleration on Jellyfin & Updated Cockpit Storage Labels**:
  - Configured Proxmox LXC 100 passthrough for `/dev/dri` (Intel HD Graphics 630, `card0` & `renderD128`).
  - Passed device `/dev/dri:/dev/dri` into `jellyfin` container and verified VA-API/iHD driver entrypoints via `vainfo` bytes.
  - Configured hardware acceleration to `qsv` (Intel QuickSync) in Jellyfin encoding configuration.
  - Updated storage capacity labels in Cockpit dashboard to match actual disk capacities (Bay 1: 1TB HDD, Bay 2: 1TB HDD, Bay 3: 2TB HDD). Rebuilt and redeployed `homelab-cockpit`.

## 2026-09-12 (13)
- **Resolved Nextcloud Admin Password & Storage Canary Watchdog**:
  - Generated and set new secure password for Nextcloud user `admin` via `occ user:resetpassword`.
  - Created missing `.mounted` canary files on DAS HDD mounts (`/mnt/hdd-media`, `/mnt/hdd-cloud`, `/mnt/hdd-music`) so Cockpit watchdog reliably detects mounts as attached and healthy.
  - Investigated Jellyfin playback delay: Identified root causes (no /dev/dri GPU passthrough in LXC 100 + container resulting in software direct-stream remuxing from USB-DAS HDDs).

## 2026-09-12 (12)
- **Homelab Cockpit Multi-Docker Monitoring Integration**:
  - Exposed Docker Engine daemon over TCP (`0.0.0.0:2375`) on node `apps-host` (LXC 101) via systemd drop-in override.
  - Pulled commits up to `4bea746` on [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard) (multi-docker host telemetry, fleet filtering, command palette, pages, pins).
  - Configured `DOCKER_HOST_NAME=docker-host` and `DOCKER_HOSTS=apps-host=tcp://192.168.18.226:2375` in `.env` and `docker-compose.yml`.
  - Rebuilt and deployed container `homelab-cockpit` on port `8050`.
  - Verified multi-host telemetry: Cockpit aggregates 15 containers from `docker-host` and 1 container (`whitearchive`) from `apps-host` seamlessly.
  - Confirmed `apps-host` is authenticated and active on Tailscale mesh (`100.110.235.57`).

## 2026-09-12 (11)
- **Created Dedicated LXC 101 (`apps-host`) for Web Applications**:
  - Configured Unprivileged LXC 101 on Proxmox VE (`192.168.18.226/24`, 2 Cores, 4GB RAM, 2GB Swap, 30GB local-lvm SSD).
  - Configured `nesting=1,keyctl=1` and TUN passthrough (`/dev/net/tun`) for Docker and Tailscale.
  - Installed Docker Engine 29.8.0 and Tailscale natively.
- **Deployed `whitearchive` Web Application**:
  - Cloned [srytmj/whitearchive](https://github.com/srytmj/whitearchive) to `/opt/projects/whitearchive`.
  - Configured Next.js `output: \"standalone\"` with an optimized multi-stage Alpine Dockerfile.
  - Successfully built and started container `whitearchive` on port `3000`. Verified HTTP 200 OK.
  - Initiated Tailscale pairing session for `apps-host`.

## 2026-09-12 (10)
- **Resolved Cloudflare Tunnel Integration Issues**:
  - **Nextcloud**:
    - Fixed `Access through untrusted domain` error by registering `nextcloud.suryatmaja.dev` and `100.89.249.96:8080` to Nextcloud `trusted_domains` via `occ`.
    - Enabled `overwriteprotocol=https` and `overwrite.cli.url=https://nextcloud.suryatmaja.dev` to prevent HTTPS reverse proxy mixed content.
  - **qBittorrent**:
    - Disabled `WebUI\CSRFProtection` and `WebUI\HostHeaderValidation`, and enabled `WebUI\ReverseProxySupportEnabled` in `qBittorrent.conf` to allow web access through reverse proxy / Cloudflare Tunnel.
    - Noted that qBittorrent WebUI runs on host port `8480` (not `8080`, which is used by Nextcloud).
  - **T3 Code**:
    - Retrieved pair token `GBUAXZJ7FJJW` for pairing via `t3.suryatmaja.dev` or LAN.

## 2026-09-12 (9)
- **Updated Homelab Dashboard (Homelab Cockpit)**:
  - Pulled commits up to `4e759e6` on `srytmj/homelab-dashboard` (`build(repo): enforce conventional commits with husky and commitlint`, `feat(auth): add owner auth wall on the new interface`, docs and UI improvements).
  - Rebuilt and restarted container `homelab-cockpit` on port `8050`.
  - Verified `/api/health` returned HTTP 200.

## 2026-09-12 (8)
- **Decommissioned redundant services replaced by Homelab Cockpit**:
  - Stopped, removed containers, volumes, and infra directories for:
    - **Portainer** (`:9000`): container logs, restart, and prune are now natively handled by Cockpit.
    - **Netdata** (`:19999`): host CPU, RAM, thermal sensors, and network I/O are streamed directly via Proxmox VE API and Docker socket.
    - **Uptime Kuma** (`:3001`): HTTP L7 probing and latency monitoring are built into Cockpit.
    - **Homelable** (`:3000`, `:8001`): topology replaced by Cockpit dashboard.
  - Executed `docker system prune -af --volumes`: **reclaimed 15.27 GB of disk space** on internal NVMe SSD and freed over 600 MB of system RAM.
  - Updated `docs/services.md` accordingly.

## 2026-09-12 (7)
- **Updated Homelab Dashboard (Homelab Cockpit)**:
  - Pulled commit `79a66ed` (`feat: add 1x owner registration auth wall, explicit Tailscale container routing, and minimalist utilitarian UI`).
  - Rebuilt and restarted container `homelab-cockpit` on port `8050`.
  - Auth wall active with 1-time owner setup wizard protecting telemetry APIs.

## 2026-09-12 (6)
- **Deployed Homelab Dashboard (Homelab Cockpit)**:
  - Cloned and built [srytmj/homelab-dashboard](https://github.com/srytmj/homelab-dashboard) at `/mnt/homelab_projects/homelab-dashboard`.
  - Configured Proxmox API token (`root@pam!cockpit`), Docker socket, Tailscale socket, and live HDD storage telemetry mounts (`/`, `/mnt/hdd-media`, `/mnt/hdd-cloud`, `/mnt/hdd-music`).
  - Container `homelab-cockpit` deployed and exposed at `http://192.168.18.225:8050`.

## 2026-09-12 (5)
- **Deployed Samba Share & WSDD Daemon on docker-host**:
  - Installed and configured Samba (`smbd`) exposing `/mnt/hdd-cloud/shared/` as `shared` with full read/write permissions.
  - Installed and configured `wsdd` (Web Services Dynamic Discovery host daemon as systemd unit) advertising hostname `HOMELAB` on `WORKGROUP`, enabling Windows 10/11 File Explorer network discovery.
  - Removed `shiori` container and volume per user request.

## 2026-09-12 (4)
- **Cleaned up unused services and reset Shiori**:
  - Stopped and removed containers/volumes for unused services: **Alexandrie** (`:8200`), **Firefly III** (`:8280`), and **YOURLS** (`:8083`). Removed corresponding directories in `/opt/infra/`. Frees up CPU, RAM, and MySQL/MariaDB overhead.
  - Reset **Shiori** (`:8081`) named volume to restore fresh default state (`shiori` / `gopher`).

## 2026-09-12 (3)
- **Migrated Kavita to new Docker repository**: Upstream Kavita deprecated `kizaing/kavita` after v0.7.8 and moved officially to `jvmilazz0/kavita:latest`. Updated `configs/docker-compose/kavita.yml` and `/opt/infra/kavita/docker-compose.yml` on docker-host. Pulled the latest image and recreated the container; existing data/config in `kavita_config` volume and manga volume intact.

## 2026-09-12 (8)
- **Deployed qBittorrent** (`lscr.io/linuxserver/qbittorrent:latest`) on docker-host, WebUI port remapped from the image's default 8080 to 8480 (8080 is Nextcloud's) — `WEBUI_PORT` env var set to match, since qBittorrent's CSRF host-header check rejects the WebUI otherwise. Downloads go to `/mnt/hdd-media/qbittorrent/downloads` (real HDD, not a placeholder). No VPN wrapper (Gluetun) — this is the already-accepted cost/risk trade-off from `decisions.md`, not a new decision. Did **not** hit the UID 1000 permission bug this time despite bind-mounting a freshly-`mkdir`'d host path (same risk pattern as Syncthing) — worth re-checking if it ever does act up, but this image apparently handles ownership itself via its own init script (`/init`, PUID/PGID env vars) rather than relying on the mount already being correctly owned. First-boot temporary admin password (random, printed once to `docker logs qbittorrent`) was given to the user directly in chat and not written to any file in this repo — it regenerates on every restart until a permanent one is set in the Web UI.

## 2026-09-12 (7)
- **Deployed Reclip** ([averygan/reclip](https://github.com/averygan/reclip)) on docker-host, port 8899. Built from source (`git clone` to `/opt/projects/reclip/`, `docker compose up -d --build` using the repo's own Dockerfile + compose file as-is — no pre-built image exists for this small Flask/yt-dlp tool). Clean deploy, no bugs — notably did **not** hit the UID-1000-vs-root-owned-directory permission bug seen with Syncthing, because Reclip uses a Docker-managed **named volume** (`reclip-downloads`) rather than a bind-mount to a host path; a fresh named volume inherits the ownership already baked into the image's directory (the Dockerfile's `chown -R reclip:reclip /app` at build time), whereas a bind-mount to a host directory freshly created by `mkdir` (as root) does not. No authentication on this app at all — anyone on the LAN can use it, which matches its minimal-by-design scope.

## 2026-09-12 (6)
- **Deployed Firefly III** ([firefly-iii/docker](https://github.com/firefly-iii/docker)) on docker-host, port 8280 (upstream default 80 collides with NPM). New `configs/docker-compose/firefly-iii.yml`: 2 containers (`app`, `cron`) — **deliberately skipped the upstream compose's bundled MariaDB `db` service** and pointed Firefly at the shared Postgres instead (new `firefly` database, same `admin` user), since Firefly III natively supports `pgsql` and this repo's convention is to prefer the shared DB when an app actually supports it (unlike YOURLS/Alexandrie, which are MySQL-only). `APP_KEY` and `STATIC_CRON_TOKEN` generated server-side; the shared Postgres password was injected into Firefly's `.env` via a script run entirely on the server (`sed` reading one `.env` into another) so it was never printed in this session's output. Clean deploy, no bugs this time — verified via the app's own log line ("Firefly III should be ready for use") confirming the Postgres connection and migrations succeeded, plus HTTP 302 (normal redirect to login/register).

## 2026-09-12 (5)
- **Deployed Alexandrie** ([Smaug6739/Alexandrie](https://github.com/Smaug6739/Alexandrie)) on docker-host — 4 containers (mysql, rustfs, backend, frontend) via new `configs/docker-compose/alexandrie.yml`. Own MySQL 8.0 + RustFS S3-compatible storage (not the shared Postgres/Redis — same intentional-exception reasoning as YOURLS). RustFS remapped from its default port 9000 to 9002 since 9000 collides with Portainer on this host. Credentials (JWT secret, MySQL passwords, RustFS access/secret keys) generated server-side. No admin account pre-created — the app has its own signup flow.
  - **Real bug hit and fixed**: first deploy attempt used a hand-written compose file based on a summarized reading of the upstream `.env.example`, which doesn't show how the real `docker-compose.yml` translates `.env` variable names into what the app containers actually expect. Backend crash-looped on `BACKEND_PORT environment variable not set` (needs `BACKEND_PORT`/`GIN_MODE` hardcoded, plus `DATABASE_*`/`MINIO_*` env vars — not just the `MYSQL_*`/`RUSTFS_*` names from `.env.example`), and frontend silently had empty `API`/`CDN`/`URL` config (needs `NUXT_PUBLIC_*`-prefixed vars, a Nuxt runtime-config convention, plus an explicit `PORT: 8200`). Fixed by fetching the upstream `docker-compose.yml` directly via `curl` (raw content) instead of relying on a summarizing fetch tool, then using it verbatim — it already handles the `.env`-to-internal-var translation correctly by design, so this repo's `.env` (with the plain `.env.example`-style names) works fine once paired with the *real* compose file's env-mapping layer. **Lesson for future service setups: always get compose files as raw/verbatim text, never a paraphrased summary, since the exact variable-name mapping between `.env` and the container's actual expected env vars can only live in the compose file itself.**

## 2026-09-12 (4)
- **Deployed Homelable** ([Pouzor/homelable](https://github.com/Pouzor/homelable)) on docker-host — 3 containers (backend, frontend, mcp) via new `configs/docker-compose/homelable.yml`, using pre-built GHCR images. Frontend on port 3000, MCP server on 8001 (exposes the canvas to AI clients like Claude Code). `SECRET_KEY`/`MCP_API_KEY`/`MCP_SERVICE_KEY` generated server-side (machine-to-machine credentials, safe to generate directly — not a human login). `SCANNER_RANGES` set to the real LAN (`192.168.18.0/24`). **Login is still the project's documented default (`admin`/`admin`)** — no first-run wizard exists for this app (auth is env-var-only), so unlike NPM/Portainer/Nextcloud there's no way to defer credential creation to the user; flagged clearly instead. Change it via: `docker exec homelable-backend python -c 'import bcrypt; print(bcrypt.hashpw(b"newpassword", bcrypt.gensalt()).decode())'`, then update `AUTH_PASSWORD_HASH` in `/opt/infra/homelable/.env` on docker-host (keep the single quotes — bcrypt hashes contain `$`) and restart. Verified HTTP 200.

## 2026-09-12 (3)
- **HDD migration fully complete**: the sdb/sdd restore (staging on sdc → freshly-formatted ext4 sdb/sdd) finished cleanly with zero errors — `rsync` summary confirmed `sent 543.11G / total size 542.97G` (sdb) and `sent 850.03G / total size 849.82G` (sdd), matching source almost exactly (small delta is the intentionally-excluded `DumpStack.log.tmp`). Verified via a fresh Claude Code session (T3 Code, running as its own container on docker-host) after generating a dedicated SSH keypair for that session and adding it to the Proxmox host's `authorized_keys` — the original laptop-only key never left the laptop.
- **Mounted both drives permanently**: added `/etc/fstab` entries on the Proxmox host keyed by UUID (not `/dev/sdX`, which can reorder) with `nofail` so boot isn't blocked if a drive is ever missing — `sdb2` → `/mnt/hdd-media` (label `hdd-media`), `sdd2` → `/mnt/hdd-cloud` (label `hdd-cloud`). Bind-mounted both into the `docker-host` LXC at the identical paths via `pct set 100 -mp0/-mp1`, then `pct reboot 100` to apply (same pattern as the earlier TUN-device fix — LXC mount point changes need a restart). All 18 containers came back up automatically (`restart: unless-stopped`).
- **Confirmed with the user before swapping Nextcloud's mount**: Nextcloud's compose mounts its *entire webroot* (not just a data folder) to the host path, so swapping to the real HDD would have reset it to a fresh install if setup had already happened. User confirmed Nextcloud was never actually set up, so the swap was safe — no migration of the 873MB placeholder needed.
- **Re-hit and re-fixed the Syncthing UID 1000 permission bug** (same root cause as the original deploy): the real HDD's `hdd-cloud/syncthing/` folder was freshly created by `mkdir` as root, so it needed `chown -R 1000:1000` again before Syncthing could write to it. Restarted the container after the fix — confirmed HTTP 200.
- **Found and fixed a real doc inconsistency**: `services.md` said VaultS3 should live at `/mnt/hdd-cloud/vaults3/`, but `decisions.md` requires VaultS3 to be **cross-drive** from HDD-Cloud (it backs up Nextcloud, which lives on HDD-Cloud — same-drive placement would defeat the backup's purpose). Deferred VaultS3 deployment until `hdd-music` (sdc, still in staging use) or HDD-Backup (not physically installed yet) is ready as a proper cross-drive home, instead of deploying it in the wrong place. Corrected both `services.md` and `roadmap.md` to reflect this.
- **Fixed stale roadmap checkboxes**: Syncthing, Shiori, YOURLS, n8n, Vaultwarden, and LibreSpeed were already deployed (see 2026-09-11 (13)) but `roadmap.md` still showed them unchecked — never updated at the time. Marked done with a CHANGELOG cross-reference.
- Updated `services.md` and `architecture.md` to remove now-inaccurate "placeholder on internal SSD" language for Jellyfin, Nextcloud, Kavita, and Syncthing now that their real HDD paths are live. `architecture.md`'s drive table gained a **Status** column reflecting actual mount state per drive (hdd-media/hdd-cloud mounted, hdd-music still staging, hdd-backup not physically installed).
- **Next in the user-requested setup queue** (services not yet deployed, going in order: Homelable, Alexandrie, Firefly III, Reclip, qBittorrent, SnapOtter — VaultS3 deferred per above, CapRover/Home Assistant/homelab-sentinel/Databasus intentionally excluded from this queue, see roadmap.md for why).

## 2026-09-12 (2)
- **Fixed recurring 502 / Model Unreachable in T3 Code**: The Antigravity (`agy`) ACP server binary resides in persistent storage (`/root/.t3/tools/antigravity-acp/...`), but T3 Code and CLI expect `agy` and `antigravity` symlinks in `/usr/local/bin`. Container restarts or recreations wiped the ephemeral container root filesystem, breaking the symlinks and throwing 502 Bad Gateway / unreachable errors.
  - Created `configs/docker-compose/t3code/entrypoint.sh` to automatically detect `agy_acp_server.par`, make it executable, ensure `localharness_external` permissions, create symlinks in `/usr/local/bin` and `/usr/bin`, verify `active.json`, and maintain a 5s background loop to self-heal symlinks even after runtime runtime updates.
  - Updated `configs/docker-compose/t3code/Dockerfile` to bake in `openssh-client`, `procps`, `iputils-ping`, and set `ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]`.
  - Updated `configs/docker-compose/t3code.yml` with explicit `entrypoint` and mounted `entrypoint.sh:ro` for immediate resilience across container recreate without requiring immediate manual image rebuild.
  - Added self-healing hook in persistent `/root/.bashrc`.

## 2026-09-12 (1)
- **Deployed T3 Code** ([pingdotgg/t3code](https://github.com/pingdotgg/t3code)) on docker-host, port 9001 (internal 9000). Created `configs/docker-compose/t3code.yml` and `configs/docker-compose/t3code/Dockerfile` (uses `node:22-bookworm-slim` with build-essential tools to build native `node-pty`, bundles `@anthropic-ai/claude-code` and `t3` CLI). Mapped host port 9001 because port 9000 is occupied by Portainer. Marked done in `roadmap.md` and added to `services.md`.

## 2026-09-11 (14)
- Updated `CLAUDE.md`: added "git pull first, every session" as step 0 (repo is now worked from multiple devices), added a "Multi-agent / multi-tool use" section covering cross-device sync (git is the only mechanism) and using non-Claude-Code tools (e.g. Antigravity/Gemini) on this repo. Also refreshed the stale Context section (M920q→M710q, dropped Immich/Navidrome, pointed to `services.md` as the actual current list instead of a hardcoded summary).

## 2026-09-11 (13)
- **Deployed 6 lightweight services**: Vaultwarden (8222), n8n (5678), Syncthing (8384), Shiori (8081), YOURLS (8083, + dedicated `yourls-mariadb`), LibreSpeed (8082). New compose files for all 6 in `configs/docker-compose/`. n8n uses a new `n8n` database in the shared Postgres; YOURLS needed its own MariaDB since it doesn't support Postgres (documented as an intentional exception). Resource check before starting: docker-host had ~11GB/12GB RAM free and 128GB/147GB disk free — comfortable headroom.
- **Two real bugs hit and fixed during this batch, not just slow pulls:**
  - **Syncthing crash-looped** on `permission denied` opening its config lock file. Root cause: the official `syncthing/syncthing` image runs as UID 1000 by default, but the Docker-created named volume was owned by `root`. Fixed with `chown -R 1000:1000` on the volume and the `/mnt/hdd-cloud/syncthing` data dir.
  - **YOURLS returned "connection reset by peer"**, then 403, before working. Root cause #1: the official `yourls` image's Apache listens on **port 8080** internally, not 80 — the compose file's `8083:80` mapping was wrong, fixed to `8083:8080`. Root cause #2 (cosmetic, not fixed — it's an upstream quirk): the image's shipped rewrite rule excludes existing directories from the `/yourls-loader.php` rewrite, so the bare `/` path 403s since the docroot itself is a directory; `/admin/` (the actual setup entry point) works fine and returns 200.
- **Portainer's setup session timed out** (5-minute security window to create the first admin account) before the user got to it — fixed with `docker restart portainer`, which reopens the setup window. Not a bug, just a heads-up for next time: create the admin account promptly after any Portainer (re)start.
- Deferred (not yet deployed, no immediate need): Alexandrie, Firefly III, Home Assistant, Reclip, VaultS3, SnapOtter, Databasus, qBittorrent — all still listed in `services.md`/`roadmap.md` for later.

## 2026-09-11 (12)
- **Deployed Uptime Kuma** (port 3001, new `configs/docker-compose/uptime-kuma.yml`) and **Netdata** (port 19999, new `configs/docker-compose/netdata.yml`) on docker-host. Both verified HTTP 200. No monitors/alerts configured in Uptime Kuma yet, and no admin account pre-created (first-run wizard, same pattern as other services). Netdata needed `SYS_PTRACE`/`SYS_ADMIN` capabilities + AppArmor unconfined to get host-level metrics from inside the unprivileged LXC — the unprivileged LXC didn't block this, but its `cgroup-network` plugin still fails to resolve per-container network interfaces (nested-cgroup limitation) — core CPU/RAM/disk/network metrics are unaffected, just that one sub-feature. Skipped Scrutiny (HDD SMART monitoring) — no real HDDs attached yet, external storage not physically assembled. Checked resource headroom before deploying more: docker-host was at ~1GB/12GB RAM used and 12GB/147GB disk used, comfortable room to keep adding services.

## 2026-09-11 (11)
- **Deployed Nextcloud** on docker-host, port 8080 (new `configs/docker-compose/nextcloud.yml`, no prior draft existed). Created a `nextcloud` database inside the existing shared Postgres container via `docker exec shared-postgres psql -U admin -c "CREATE DATABASE nextcloud;"` (local superuser exec, no password needed) rather than spinning up a dedicated DB container — consistent with the shared-DB decision in `decisions.md`. Reused the same Postgres password already in `/opt/infra/postgres-redis/.env` by copying the file server-side (`cp`) — the value was never printed in this session's output. Also wired to the shared Redis for caching. **No admin account was pre-created** via `NEXTCLOUD_ADMIN_USER`/`PASSWORD` env vars — left for the user to create through Nextcloud's own first-run web setup wizard, same pattern as NPM/Portainer/Kavita. Data path `/mnt/hdd-cloud/nextcloud` is a placeholder on the internal SSD (external HDD not physically assembled yet). Verified HTTP 200.

## 2026-09-11 (10)
- **Deployed Jellyfin** on docker-host, port 8096. Updated the stale draft `configs/docker-compose/jellyfin.yml` (old `/mnt/external-storage/movies` single-mount path, Traefik labels) to the current multi-mount convention: `/mnt/hdd-music/jellyfin/music`, `/mnt/hdd-media/jellyfin/{movies,tv,anime}`, dropped Traefik labels. Same as Kavita earlier today — **these are placeholder directories on the internal SSD for now**, external HDDs not physically assembled yet. Verified HTTP 302 (normal first-run redirect to setup wizard).

## 2026-09-11 (9)
- **Fixed the `portfolio` Cloudflare Tunnel Public Hostname**: it was configured as `https://localhost:3080` in the Cloudflare Zero Trust dashboard, but the `yorha-portfolio` nginx container only serves plain HTTP on 3080 (no TLS) — cloudflared logged `tls: first record does not look like a TLS handshake` on every request. User fixed the scheme to `http://localhost:3080` in the dashboard. Verified: `https://suryatmaja.dev` now returns HTTP 200 publicly.
- **Deployed Kavita** (manga/comic reader) on docker-host, port 5000. Updated the stale draft `configs/docker-compose/kavita.yml` (had an old `/mnt/external-storage/manga` path and Traefik labels from before the storage-topology and NPM decisions) to the current path convention (`/mnt/hdd-media/kavita/manga`) and dropped the Traefik labels (not used — this homelab uses NPM). **The manga path is currently a placeholder empty directory on the internal SSD** — the external HDD dock isn't physically assembled yet (see roadmap.md), so this will need remounting to the real drive later; no data loss risk since it's empty either way.
- **Deferred `sso.whitearchive`/`whitearchive` deployment** — user hasn't purchased the domain yet for the whitearchive product line. Investigated the repo enough to know it's a substantial Laravel + Passport OAuth2 SSO provider that bundles its own Postgres in `docker/compose.prod.yml` (would need adapting to the shared Postgres instance) and needs real secrets this session shouldn't fabricate (Resend API key for email, admin credentials, production domain) — picking back up once the domain exists.
- **Clarified Kavita vs. Komga**: user asked about Komga (not previously documented anywhere in this repo) but confirmed sticking with the already-decided Kavita rather than switching or running both.

## 2026-09-11 (8)
- **Installed `cloudflared` on docker-host** (native apt package, not Docker — user's explicit choice, provided the Debian install recipe directly) and registered it as a Cloudflare Tunnel connector via `cloudflared service install <token>`, using a tunnel token the user generated in the Cloudflare Zero Trust dashboard and pasted directly in chat (never written to any file in this repo, shell history cleared after use — same handling as the Tailscale auth key earlier today). Service is `enabled` (survives reboot) and confirmed connected: 4 registered QUIC connections to Cloudflare edge (Singapore/Jakarta PoPs), all connectivity prechecks passed. **Not yet done:** routing a public hostname (e.g. `suryatmaja.dev`) to this tunnel and pointing it at the `portfolio` container (3080) — that's configured in the Cloudflare Zero Trust dashboard itself (Public Hostname mapping), not something this session did.
- **Hit two apt hangs while installing `cloudflared`, both self-inflicted, not real network bugs:** (1) `apt-get update` hung after adding the cloudflared repo — a `pkill -9` on a previous stuck process had left stale `/var/lib/apt/lists/lock` and `/var/lib/dpkg/lock*` files; clearing them and retrying fixed it. (2) After that, a full `apt-get update` across all sources hung again on `archive.ubuntu.com`'s `noble-updates` (unrelated to cloudflared) — worked around by scoping `apt-get update` to just the cloudflared source list (`-o Dir::Etc::sourcelist=... -o Dir::Etc::sourceparts=-`) instead of updating every configured repo. Lesson for future package installs on this LXC: prefer a source-scoped `apt-get update` over a full one when only one new repo was added, to avoid unrelated slow/flaky mirrors blocking the whole operation.

## 2026-09-11 (7)
- **Installed Tailscale on docker-host**, joined tailnet `srytmj.github` as `docker-host` (`100.89.249.96`, MagicDNS `docker-host.taila813af.ts.net`). Enabled TUN device passthrough for the unprivileged LXC first (`lxc.cgroup2.devices.allow: c 10:200 rwm` + `lxc.mount.entry: /dev/net dev/net none bind,create=dir` in `/etc/pve/lxc/100.conf`), which required a container reboot to apply (all `restart: unless-stopped` containers came back up automatically — no manual intervention needed). Authenticated using a pre-generated Tailscale auth key the user supplied directly (not interactive browser login, not stored anywhere in this repo or left in shell history — cleared after use). Used `--accept-dns=false` so Tailscale's DNS doesn't fight with the LXC's own resolver setup (tuned earlier today to fix registry DNS issues). **Not yet done:** per-service MagicDNS subdomains (`tailscale serve`) and Cloudflare Tunnel bridging — user will handle the Tailscale→Cloudflare bridging personally, per the sequencing decision logged in the previous entry.

## 2026-09-11 (6)
- **Deployed the first web project: `portfolio`.** Added `Dockerfile` + `nginx.conf` to the [srytmj/portofolio](https://github.com/srytmj/portofolio) repo itself (commit `3542728`, pushed as Maja per that repo's own `AI_GUIDELINES.md` — Claude Code never adds itself as commit author there), implementing the "Option 3: Homelab Self-Hosted" deployment guide that repo had already documented but never had files for. Multi-stage build (`node:20-alpine` builds the SvelteKit static-adapter output, `nginx:alpine` serves it). Cloned to `/opt/projects/portfolio/` on docker-host (matches the path convention `scripts/git-auto-deploy.sh` already expects), compose file also tracked at `configs/docker-compose/portfolio.yml`. Container `yorha-portfolio` published on port 3080, verified HTTP 200.
- **Sequencing decision from the user:** Tailscale gets installed and given to *every* service first (not just internal ones) before any Cloudflare Tunnel work — the user will personally bridge a service's Tailscale address to Cloudflare Tunnel themselves once Tailscale is up, rather than Claude Code setting up `cloudflared` directly. This applies to `portfolio` too, superseding the assumption that Cloudflare Tunnel setup would happen as part of this deploy. No `cloudflared` container was deployed as part of this task.
- **Found and fixed a second, distinct DNS bug** (not the earlier `GODEBUG=netdns=cgo` one): `docker compose up --build` failed during BuildKit's image-metadata resolution step with `Temporary failure in name resolution` for `registry-1.docker.io`, even though `curl`/`getent ahosts` worked fine on the host at the same time. Root cause was the router's DNS forwarder (`192.168.18.1`) intermittently failing **A-record** queries specifically for high-record-count hostnames like `registry-1.docker.io` (many load-balanced IPs), while AAAA queries succeeded — confirmed via `dig @192.168.18.1` timing out on A. Fixed by reordering the LXC's resolvers to put `1.1.1.1` first and the router second (`pct set 100 --nameserver '1.1.1.1 192.168.18.1'`), rather than router-first with `1.1.1.1` as fallback. Also noted `getent hosts` (legacy call) is unreliable for diagnosing this class of bug on this system — it silently returned IPv6-only results even after the fix; `getent ahosts` or a direct `curl` is the trustworthy check.

## 2026-09-11 (5)
- **Created NPM admin account** (user did this manually via the browser — account creation/passwords are never entered by Claude Code) and **added the first proxy host**: `portainer.home.arpa` → `http://192.168.18.225:9000` (Portainer), with Block Common Exploits + Websockets Support enabled, no SSL (HTTP only — not a real domain, so no Let's Encrypt cert). Chosen as a placeholder hostname pattern since Tailscale (and its planned MagicDNS subdomains, per `decisions.md`) isn't installed yet. Verified end-to-end with `curl -H "Host: portainer.home.arpa"` — request reached Portainer correctly (redirected to `/timeout.html`, its normal pre-login behavior). **Note:** `portainer.home.arpa` only resolves for clients that have a hosts-file entry or local DNS override pointing it at `192.168.18.225` — nothing publishes this hostname on the network yet.

## 2026-09-11 (4)
- **Deployed Portainer CE** on docker-host. New compose file `configs/docker-compose/portainer.yml` (referenced in `services.md` but hadn't actually been written yet). Running under `/opt/infra/portainer/`, ports 9000 (HTTP) and 9443 (HTTPS), docker.sock mounted read-write for container management. Hit a transient `Temporary failure in name resolution` for `registry-1.docker.io` on first attempt (unrelated to the earlier GODEBUG fix — `getent hosts` resolved fine moments later); added `1.1.1.1` directly to the LXC's `/etc/resolv.conf` as a fallback (the `pct set --nameserver` change from earlier hadn't propagated into the running container — Proxmox writes resolv.conf at container start, not live) and retried successfully. Verified: `docker ps` shows it running, HTTP 200 on port 9000.

## 2026-09-11 (3)
- **Deployed shared PostgreSQL 16 + Redis 7** on docker-host, using the existing `configs/docker-compose/postgres-redis.yml`. Running under `/opt/infra/postgres-redis/` on the server, both bound to `127.0.0.1` only (internal use by other containers on `shared_net`, not exposed on the LAN). Password generated randomly and stored in a server-local `.env` (not committed — gitignored). Verified: `pg_isready` accepting connections, `redis-cli ping` → `PONG`.
- **Found and fixed a real Docker networking bug, not just flaky DNS:** image pulls kept failing with `dial tcp [IPv6]: cannot assign requested address` when hitting `auth.docker.io` / Cloudflare-fronted endpoints, even after IPv6 was disabled at the kernel level and `/etc/gai.conf` was set to prefer IPv4 (from the earlier NPM deploy). Root cause: Docker/containerd is a Go binary and by default uses its own internal DNS resolver, which ignores `/etc/gai.conf` entirely. Fixed by forcing the daemon onto the system (cgo) resolver via a systemd override — `/etc/systemd/system/docker.service.d/override.conf` setting `GODEBUG=netdns=cgo` — then `systemctl daemon-reload && systemctl restart docker`. This is the actual fix for the IPv6-on-an-IPv4-only-network class of failures; the earlier `gai.conf` change alone was insufficient for Go-based tools.
- Added a fallback public DNS (`1.1.1.1`) to the docker-host LXC's nameserver config (`pct set 100 --nameserver`) alongside the router's `192.168.18.1`, since two separate pulls hit `auth.docker.io` resolution timeouts before the real bug was found — cheap resilience even though the underlying fix was the resolver override above.

## 2026-09-11 (2)
- **Deployed Nginx Proxy Manager** on docker-host. User chose NPM over Traefik (GUI-first, easier than docker-label-driven config for this setup) — the choice had been left open in `architecture.md`/`services.md` as "Traefik / NPM", never actually decided. Compose file at `configs/docker-compose/npm.yml`, running under `/opt/infra/npm/` on docker-host, published on ports 80/443 (proxy) and 81 (admin UI). Created a `shared_net` external Docker network on docker-host for this and future services to join. Image pull was slow (~5+ min for ~38 layers) but completed and container verified healthy (HTTP 200 on admin UI, clean startup logs).

## 2026-09-11
- **Proxmox VE installed on the M710q.** Hostname `pve.suryatmaja.dev`, static IP `192.168.18.224/24`, gateway/DNS `192.168.18.1`. Set up SSH key-based auth (`~/.ssh/id_ed25519_homelab`) instead of relying on the root password for future automation.
- **Hardware verification found a CPU mismatch:** `lscpu` on the actual server shows **Intel i5-7500 (4C/4T, 3.4GHz)**, not the **i7-7700 (4C/8T)** that was purchased/decided in `decisions.md`. RAM (32GB) and the M710q model (`10MQS1EU00`) match. User chose to proceed with setup and document rather than pause for a seller dispute — worth following up separately. See `docs/architecture.md`.
- **Created `docker-host` LXC** (VMID 100, Ubuntu Server 24.04, unprivileged, `nesting=1,keyctl=1`), static IP `192.168.18.225/24`. Allocated 12GB RAM / 150GB disk; cores corrected from 5→4 after discovering the host only has 4 physical cores (initial config over-allocated based on the documented-but-wrong 6-core/8-thread specs).
- **Fixed LVM thin-pool overcommit:** `local-lvm`'s thin pool was only 140.87GB while the LXC's rootfs requested 150GB. Extended the pool to ~156.88GB using the volume group's remaining free space, and set `thin_pool_autoextend_threshold`/`_percent` in `/etc/lvm/lvm.conf` per Proxmox's own warning.
- **Installed Docker Engine 29.8.0 + Compose plugin v5.5.1** inside docker-host. Hit an IPv6 dead-route issue (container had only a link-local IPv6 address, no route) that broke image pulls — fixed by disabling IPv6 (`sysctl`) and setting `/etc/gai.conf` to prefer IPv4 in DNS resolution. Verified with `docker run hello-world`.
- Synced `docs/architecture.md` and `docs/roadmap.md` to actual verified server state (they still referenced the superseded M920q/16GB plan in some sections despite `decisions.md` already having the M710q/32GB revision).

## 2026-08-26
- **Hardware finalized, checked out.** Considered and rejected a used Xeon E5 server PC (12-20 cores) — idle power draw over 24/7 use would cost more in electricity than the hardware price difference within 1-2 years, and the workload doesn't benefit from that many cores (see decisions.md). PSU switched to Enhance ENP-2320 (200W, Active PFC) instead of a cheap generic PSU, to avoid voltage-spike risk to the HDDs. Storage expanded from 1 HDD to 3 dedicated drives (HDD-Music, HDD-Media, HDD-Cloud) each single-purpose, no RAID. Original Toshiba 2TB HDD sold out — replaced with Seagate Barracuda 2TB (also desktop-class, not NAS-rated). Final cart cost ~Rp6.79 juta (excl. HDD-Media, HDD-Cloud, and their dock, still unpurchased). Also decided: Homepage dashboard dropped in favor of a custom hidden page in the existing `portfolio` repo, which becomes the only publicly-exposed service (via Cloudflare Tunnel) — everything else stays Tailscale-only.
- **Storage topology finalized, corrected from earlier assumption.** Original plan assumed the OS SSD would be a standard 2.5" SATA SSD sitting in the internal 2.5" bay, with a separate USB DAS enclosure for extra HDDs. Corrected: the OS SSD is actually **M.2 SATA** form factor, so it needs an "M.2 SATA/mSATA to SATA 3.0 2.5\"" adapter to fit the internal bay at all. The M.2 NVMe slot is repurposed to host an **LM418 (M.2 NVMe to 5-port SATA) card** instead of holding a drive — this card's SATA ports are what an additional HDD (Toshiba 2TB) connects through, housed in an external powered dock (separate Imperion ATX 500W PSU) rather than a USB DAS enclosure. See `decisions.md` for full reasoning.
- Dropped the dedicated router purchase (MikroTik) for now — topology is ISP router → TP-Link TL-LS1005G Gigabit switch → PC + Homelab. Revisit a dedicated router only when VLAN isolation is actually implemented.
- Dropped from plan: 2nd HDD (single Toshiba 2TB is enough to start), electric dehumidifier (silica gel as cheaper fallback if needed), and likely the separate 2.5" HDD dock (superseded by the M.2-SATA-adapter-in-internal-bay setup).
- Logged final shopping list with reference pricing in `decisions.md`.
- Revised hardware pick from M920q (i5-9500T, 6C/6T, 16GB RAM) to M710q (i7-7700T, 4C/8T, 32GB RAM) — traded 2 physical cores for double RAM + higher clock speed after characterizing the actual workload as mostly I/O-bound (see decisions.md for full reasoning). Also decided Immich runs with ML disabled, removing the main compute-bound argument for prioritizing core count.

- Automation mode: added `scripts/git-auto-deploy.sh` — polls each project under `/opt/projects/*` every 5min for new commits on `main`, auto `git pull` + `docker compose up -d --build`. Chose polling over a GitHub webhook since the server has no public endpoint (Tailscale-only, see decisions.md). Added `configs/systemd/homelab-git-deploy.service` + `.timer`. Not yet deployed — same as the other automation, waiting on docker-host to exist.
- Automation mode: finalized `scripts/backup.sh` (daily PG dump + config backup, 30-day retention) and `scripts/health-check.sh` (now auto-restarts down containers instead of just warning). Added systemd unit/timer files under `configs/systemd/` for both, plus a deploy README. Not yet deployed — docker-host LXC/VM doesn't exist yet, so this is prep work ahead of the roadmap's Proxmox/docker-host setup step.
- Repo initialized. Planning phase — hardware chosen (M920q), storage strategy decided (external USB enclosure for 4x 2.5" HDD + extra SSD). No server setup has happened yet.
