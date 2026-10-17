# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry
- [Claude-Code] 2026-10-17: done | cloud-course-aws (cabang migrasi/astro): audit bahasa tahap 2 (praktikum, prasesi, peta karier, output/input), deploy staging | Locks: Documents/GitHub/cloud-course-aws-astro (site/src/content, tools/, diagrams/), personal-hosts staging
- [Claude-Code] 2026-10-17: done | cloud-course-aws (cabang migrasi/astro): audit bahasa dan diagram (panah svgkit, istilah pengaman, hapus Ringkasan), deploy staging | Locks: Documents/GitHub/cloud-course-aws-astro (site/src/content, tools/, diagrams/), personal-hosts staging
- [Claude-Code] 2026-10-17: done | cloud-course-aws (cabang migrasi/astro): sidebar halaman /guru/ memakai daftar pengajar, deploy staging | Locks: Documents/GitHub/cloud-course-aws-astro (site/src/layouts/Kursus.astro), personal-hosts:/opt/projects/cloud-course-aws (staging)
- [Claude-Code] 2026-10-17: done | cloud-course-aws migrasi Astro: deploy cabang migrasi/astro (202c9db) ke staging, kursus-staging di-recreate (image tidak dibangun ulang, Node 22.23.3 sudah cukup) | Locks: released. Repo server /opt/projects/cloud-course-aws/repo kini di cabang migrasi/astro; rollback: balik symlink staging/web/current ke releases/20261017-122307
- [Claude-Code] 2026-10-17: cancelled | cloud-course-aws migrasi Astro: rebuild image + deploy staging dibatalkan sebelum menyentuh server (main kursus sudah maju 16 commit; cabang harus di-rebase dulu) | Locks: released
- [Claude-Code] 2026-10-17: done | cloud-course-aws: header keamanan, CSP report-only, pembatas kode, hardening container, recreate kursus-staging | Locks: personal-hosts:/opt/projects/cloud-course-aws (repo/deploy), container kursus-staging
- [Claude-Code] 2026-10-17: done | cloud-course-aws: UX fase develop (tombol salin, zoom gambar, nav sesi, landing sesi + form kode), deploy staging | Locks: personal-hosts:/opt/projects/cloud-course-aws (repo), container kursus-staging
- [Claude-Code] 2026-10-17: done | cloud-course-aws: nginx cookie akses tanpa Secure bila bukan HTTPS (akses LAN fase develop), recreate kursus-staging | Locks: personal-hosts:/opt/projects/cloud-course-aws (repo/deploy/nginx.conf), container kursus-staging
- [Gemini] 2026-10-17: done | music library ingest (Phases 1-5): quick wins, JAV evacuation, qbittorrent & slskd ingest, vα-liv split, Denonbu & gamdl ALAC selesai 100%, 26.565 track catalog.sqlite aktif | Locks: released
- [Gemini] 2026-10-17: done | manga-raw/nsfw: ingest 6 titles from local PC staging (meng, meoff, meraw) selesai 100% (2 JP, 2 Unofficial, 2 Official Translate, verifikasi integritas ZIP & SHA256 OK, 3 folder staging lokal dibersihkan) | Locks: released
- [Gemini] 2026-10-17: done | manga-raw/nsfw server-side consolidation (Phase 1-4: legacy folders, nhdl staging, hdd-media/download ingest) selesai 100% (durasi 162s, 39 duplikat dibersihkan, 706 file termigrasi, 7.06 GB bebas di hdd-media, 0 error) | Locks: released
- [Claude-Code] 2026-10-17: done | cloud-course-aws: gerbang kode+cookie di nginx (akses.conf generated, hapus htpasswd), skrip rotate-codes/set-code, reload kursus-staging | Locks: personal-hosts:/opt/projects/cloud-course-aws (docker-compose.yml, staging/teacher, staging/akses-state), container kursus-staging, kursus-prod
- [Claude-Code] 2026-10-17: done | cloud-course-aws spike UI/UX: build dua prototipe (Astro, Starlight) di container kursus-builder dan uji nginx sementara di personal-hosts | Locks: released (container spike-nginx-* dihapus, direktori uji nginx dihapus; klon spikes/astro dan spikes/starlight dibiarkan, bisa dihapus)
- [Claude-Code] 2026-10-17: done | cloud-course-aws: nginx location /guru + mount teacher/ + htpasswd guru + skrip rotate-codes, recreate kursus-staging | Locks: personal-hosts:/opt/projects/cloud-course-aws (docker-compose.yml, staging/teacher), containers kursus-staging, kursus-prod
- [Claude-Code] 2026-10-16: done | cloud-course-aws: rebuild image kursus-builder (cairosvg, libcairo2, fonts-liberation) + deploy staging (dicatat setelah pengerjaan; lock tidak diklaim sebelumnya) | Locks: released
- [Claude-Code] 2026-10-16: done (staging; prod menunggu htpasswd user) | cloud-course-aws Task 2: compose kursus-staging/kursus-prod (nginx) di personal-hosts, port 8120/8121 | Locks: personal-hosts:/opt/projects/cloud-course-aws, containers kursus-staging, kursus-prod
- [Claude-Code] 2026-10-16: done | cloud-course-aws Task 1: klon repo + image builder kursus-builder di personal-hosts (cek ukuran dulu, disk sempit 3 GB bebas) | Locks: personal-hosts:/opt/projects/cloud-course-aws, image kursus-builder
- [Claude-Code] 2026-10-14: running | claude-desktop-web: webtop + Claude Desktop di docker-host (akses browser via Tailscale) | Locks: configs/docker-compose/claude-desktop-web*, docker-host:/opt/claude-desktop, docs/services.md
- [Gemini] 2026-10-13: done | repurpose Toshiba 1TB HDD /mnt/hdd-music -> /mnt/hdd-placeholder (ext4), migrate anime from hdd-media (148GB), update Jellyfin & arr-stack | Locks: released
- [Claude-Code] 2026-10-13: done | copy C:\Users\Sam\Downloads\Video\jav (58 file, 176 GB) ke hdd-media/videos/movies/nsfw/jav thumb/downloads via robocopy dari PC, sumber TIDAK dihapus | Locks: docker-host:/mnt/hdd-media/videos/movies/nsfw/jav thumb/downloads
- [Claude-Code] 2026-10-11: done | dev-host: pg-backup per-target retention (rag-postgres 2d), dirs /opt/data/aws-corpus + /opt/projects/rag-kb, pull python:3.12-slim | Locks: dev-host:/opt/scripts/pg-backup.sh, scripts/pg-backup.sh, dev-host:/opt/data, dev-host:/opt/projects/rag-kb
- [Claude-Code] 2026-10-11: done | malas: prune stale hashed assets in volume malas_public_build (files not in manifest.json), 2nd time | Locks: container malas-app-1 (exec only), volume malas_public_build
- [Claude-Code] 2026-10-11: done | malas navigation speed: sidebar prefetch on hover, idle preload of main page chunks, progress delay 100ms; then release (rebuild image, recreate app+queue) | Locks: C:/Users/Sam/Documents/GitHub/malas, yado-hosts:/opt/projects/malas, containers malas-app-1, malas-queue-1
- [Claude-Code] 2026-10-11: done | malas user-side fixes (catalog status filter as segmented control + skeleton only for same-page visits, collection table fit) previewed on malas-dev; NOT committed/deployed, waiting for user OK | Locks: C:/Users/Sam/Documents/GitHub/malas (3 files uncommitted), yado-hosts:/opt/projects/malas working tree (same 3 files, dev preview only)
- [Claude-Code] 2026-10-11: done | malas: prune stale hashed assets in volume malas_public_build (files not in manifest.json) | Locks: container malas-app-1 (exec only), volume malas_public_build
- [Claude-Code] 2026-10-11: done | malas fixes: remove PageTransition fade (all sides), case-insensitive series search, delete keeps page; dev-preview on malas-dev, release deploy only after user OK | Locks: C:/Users/Sam/Documents/GitHub/malas (PC clone), yado-hosts:/opt/projects/malas (dev preview files only), malas-dev stack
- [Claude-Code] 2026-10-11: done | malas-dev stack (read-only prod DB role malas_dev, port 8092 + tailscale serve) + nginx upstream re-resolve fix on prod nginx; login via emergency link (C2), no SSO change | Locks: yado-hosts:/opt/projects/malas/deploy, container malas-nginx-1 (reload only), shared-postgres role malas_dev
- [Claude-Code] 2026-10-11: cancelled | (superseded by user decision 2026-10-11: single owner, C2 no SSO change) malas-dev stack on yado-hosts (read-only DB role malas_dev, port 8092, tailscale serve 8443), nginx upstream re-resolve fix on malas-nginx-1, add dev redirect URI to sso-yado client | Locks: yado-hosts:/opt/projects/malas/deploy, malas-nginx-1 (conf reload only), shared-postgres (role malas_dev), sso-yado oauth client (redirect URI), tailscale serve
- [Claude-Code] 2026-10-11: done | malas admin: fix series save errors (cover limit, visible errors), alphabetical default sort, activity log for ALL admin mutations (middleware), rebuild image | Locks: yado-hosts:/opt/projects/malas, containers malas-app-1, malas-queue-1
- [Claude-Code] 2026-10-11: done | malas admin series: card layout + windowed pager (new AdminPagination), edit on yado-hosts, rebuild image malas:latest | Locks: yado-hosts:/opt/projects/malas, containers malas-app-1, malas-queue-1
- [Claude-Code] 2026-10-11: done | harness token-efficiency + KB integration (hooks, settings, CLAUDE.md slim, rag-kb source homelab-ops) | Locks: CLAUDE.md, .claude/settings*.json, rag-kb/kb.toml (local), docs/harness-kb.md
- [Claude-Code] 2026-10-11: done | gamdl-dashboard: unavailable-storefront fallback + finish-with-condition patch (app/runner.py), remove items 356-385 | Locks: media-hosts:/opt/gamdl-dashboard/app/runner.py, service gamdl-dashboard | patched+restarted+items removed; test_api autostart test fails with and without patch (pre-existing)
- [Claude-Code] 2026-10-09: done | dev-host: deploy rag-postgres (pgvector/pg16) + local pg-backup timer, for cloud-ops RAG | Locks: dev-host:/opt/projects/rag-postgres, dev-host:/opt/scripts/pg-backup.*, configs/docker-compose/rag-postgres.yml
- [Claude-Code] 2026-10-09: done | hdd-backup/videos removed by user (Plan B), homelab-video-sync.timer disabled, docs updated | Locks: docker-host:homelab-video-sync.timer, docs/architecture.md, docs/decisions.md
- [Claude-Code] 2026-10-09: done | manga-raw/nsfw tidy: removed 2 verified-duplicate cbz from Japanese/Eda, moved Japanese/Dokurosan -> JP/Dokurosan | Locks: docker-host:/mnt/hdd-backup/manga-raw/nsfw/{Japanese,JP/Dokurosan}
- [Claude-Code] 2026-10-04: done | homelab-dashboard: add SERVICE_PROBES (gamdl-dashboard) + server-side metric history; then rebuild (closed 2026-10-11 after verify: commit d3fe1e7 in repo, container Up 6 days, repo clean) | Locks: container homelab-dashboard, docker-host:/mnt/homelab_projects/homelab-dashboard, repo homelab-dashboard
- [Claude-Code] 2026-10-04: done | gamdl-dashboard: patch cap to not count skipped tracks (app/store.py, app/runner.py) + restart service | Locks: media-hosts:/opt/gamdl-dashboard, service gamdl-dashboard
- [Claude-Code] 2026-10-04: done | n8n auto-deploy: dry-run script install (no pull/build yet) | Locks: scripts/n8n-deploy-check.sh, /opt/scripts/n8n-deploy-check.sh on personal-hosts + yado-hosts
- [Claude-Code] 2026-10-06: done | nhdl: git pull --ff-only + rebuild on personal-hosts | Locks: container nhdl, personal-hosts:/opt/projects/nhdl
- [Claude-Code] 2026-10-06: done | media-hosts: fix 5s DNS stall (resolv.conf options) for gamdl | Locks: media-hosts:/etc/resolv.conf
- [Claude-Code] 2026-10-06: done | gamdl-dashboard: fix auto-resume when 24h cap window is empty (app/runner.py, app/api.py) + restart | Locks: media-hosts:/opt/gamdl-dashboard, service gamdl-dashboard | patched + restarted, unit tests not run
- [Claude-Code] 2026-10-07: done | nhdl: bypass ISP DNS hijack via CoreDNS TCP sidecar + recreate | Locks: container nhdl, personal-hosts:/opt/projects/nhdl/docker-compose.yml
- [Claude-Code] 2026-10-07: done | nhdl: skip stuck gallery (com:locking-horns-norasuko-chapter-2) + cap not-an-image retries in engine.js | Locks: container nhdl, personal-hosts:/opt/projects/nhdl
- [Claude-Code] 2026-10-08: done | portofolio: git pull --ff-only (19 commits) + rebuild on personal-hosts | Locks: container portofolio, personal-hosts:/opt/projects/portofolio
- [Claude-Code] 2026-10-07: done | sso-yado: start containers + add restart policy via local override | Locks: yado-hosts:/opt/projects/sso.yado/docker-compose.override.yml, containers sso-yado-*
- [Claude-Code] 2026-10-07: done | yado-hosts DB centralization: malas + sso-yado migrated to shared-postgres (bundled DBs stopped, volumes kept; cleanup + group-checklist pending user): backup script+timer, roles/db on shared-postgres, migrate sso-yado then malas to shared-postgres | Locks: yado-hosts:/opt/projects/{shared-postgres,sso.yado,malas}, containers shared-postgres, sso-yado-*, malas-*, scripts/pg-backup.sh
- [Claude-Code] 2026-10-07: done | personal-hosts: new shared-postgres + migrate group-checklist DB onto it (bundled DB stopped, volume kept) + pg-backup timer | Locks: personal-hosts:/opt/projects/shared-postgres, personal-hosts:/opt/projects/group-checklist/{docker-compose.yml,.env}, containers group-checklist*, scripts/pg-backup.sh
- [Claude-Code] 2026-10-07: done | offsite backup yado-hosts+personal-hosts -> docker-host:/mnt/hdd-backup/offsite (restricted user backup-recv, rrsync write-only, rotation 14d) | Locks: docker-host:/mnt/hdd-backup/offsite, docker-host user backup-recv + its authorized_keys, /opt/scripts/offsite-sync.sh on yado-hosts+personal-hosts



















---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file or critical doc, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Once your task is finished and verified, update `CHANGELOG.md`, clear your lock from this file, then run `git add <files> && git commit -m "..." && git push`.
