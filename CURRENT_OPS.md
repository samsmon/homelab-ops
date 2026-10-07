# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry
- [Claude-Code] 2026-10-04: running | homelab-dashboard: add SERVICE_PROBES (gamdl-dashboard) + server-side metric history; then rebuild | Locks: container homelab-dashboard, docker-host:/mnt/homelab_projects/homelab-dashboard, repo homelab-dashboard
- [Claude-Code] 2026-10-04: done | gamdl-dashboard: patch cap to not count skipped tracks (app/store.py, app/runner.py) + restart service | Locks: media-hosts:/opt/gamdl-dashboard, service gamdl-dashboard
- [Claude-Code] 2026-10-04: done | n8n auto-deploy: dry-run script install (no pull/build yet) | Locks: scripts/n8n-deploy-check.sh, /opt/scripts/n8n-deploy-check.sh on personal-hosts + yado-hosts
- [Claude-Code] 2026-10-06: done | nhdl: git pull --ff-only + rebuild on personal-hosts | Locks: container nhdl, personal-hosts:/opt/projects/nhdl
- [Claude-Code] 2026-10-06: done | media-hosts: fix 5s DNS stall (resolv.conf options) for gamdl | Locks: media-hosts:/etc/resolv.conf
- [Claude-Code] 2026-10-06: done | gamdl-dashboard: fix auto-resume when 24h cap window is empty (app/runner.py, app/api.py) + restart | Locks: media-hosts:/opt/gamdl-dashboard, service gamdl-dashboard | patched + restarted, unit tests not run
- [Claude-Code] 2026-10-07: done | nhdl: bypass ISP DNS hijack via CoreDNS TCP sidecar + recreate | Locks: container nhdl, personal-hosts:/opt/projects/nhdl/docker-compose.yml



















---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file or critical doc, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Once your task is finished and verified, update `CHANGELOG.md`, clear your lock from this file, then run `git add <files> && git commit -m "..." && git push`.
