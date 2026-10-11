# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry
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
