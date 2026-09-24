# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry







---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Selesai task, update `CHANGELOG.md`, bersihkan lock dari file ini, lalu `git add . && git commit && git push`.
- [Claude Code] 2026-09-24: Moving manga-raw (135G) hdd-media->hdd-backup, repointing manga-optimizer.service + Samba [manga] share | Locks: docker-host manga-optimizer.service, /mnt/hdd-media/manga-raw, /mnt/hdd-backup/manga-raw, smb.conf [manga]
