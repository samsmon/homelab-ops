# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry

- [Claude Code] 2026-09-21: Migrating portfolio to personal-hosts (LXC 103), full 4-LXC split (media-hosts, drive-hosts), hdd-music finalized as cold-backup role. Verified previous portfolio lock was stale (clean git tree, no active cherry-pick/merge, matching last commit) before proceeding. | Locks: portfolio, docker-host media/drive containers, LXC 100/101/103, new LXCs, docs/architecture.md, docs/services.md, docs/decisions.md


---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Selesai task, update `CHANGELOG.md`, bersihkan lock dari file ini, lalu `git add . && git commit && git push`.
