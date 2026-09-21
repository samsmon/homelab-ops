# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry

- [Claude Code] 2026-09-21: Resolving cherry-pick conflict + doing White Archive -> Yado rename in external repo samsmon/portofolio (SSH direct edit on docker-host at /opt/projects/portfolio) | Locks: portfolio container/repo (not homelab-ops files)
- [Claude Code] 2026-09-21: Renaming LXC 103 (shared-hosts -> personal-hosts), resizing its disk, migrating nhdl + group-checklist from docker-host to it, deleting reclip + headless-browser entirely. Portfolio migration deferred (see lock above) until that clears. | Locks: LXC 103, nhdl/group-checklist/reclip/headless-browser containers on docker-host, docs/architecture.md, docs/services.md


---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Selesai task, update `CHANGELOG.md`, bersihkan lock dari file ini, lalu `git add . && git commit && git push`.
