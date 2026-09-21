# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry

- [Claude Code] 2026-09-21: Renaming HDD mount points: old hdd-cloud (Toshiba, now pure music) -> hdd-music, old hdd-music (WD Green) -> hdd-backup. Touches /etc/fstab on pve, LXC mp configs for 100/103/104, Samba smb.conf, and compose files on docker-host/media-hosts/personal-hosts referencing these paths. | Locks: pve fstab, LXC 100/103/104 mp configs, docker-host Samba, all compose files referencing hdd-cloud/hdd-music


---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Selesai task, update `CHANGELOG.md`, bersihkan lock dari file ini, lalu `git add . && git commit && git push`.
