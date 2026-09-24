# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry

- [Antigravity] [2026-09-24 14:29 WIB]: Ingesting and reorganizing THE IDOLM@STER SHINY COLORS discography archives into Option A hierarchy | Locks: /mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~/シャイニーカラーズ/
- [Claude-Code] [2026-09-24 14:45 WIB]: Building sync-config.conf + generic sync engine, updating sync-manga.sh (hdd-backup->hdd-media), deploying Cronicle for scheduling | Locks: scripts/sync-*.sh, configs/docker-compose/cronicle.yml



---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Selesai task, update `CHANGELOG.md`, bersihkan lock dari file ini, lalu `git add . && git commit && git push`.
