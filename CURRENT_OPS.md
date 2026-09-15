# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry

*(Format: `- [Agent-Name] [Timestamp]: <Task Description> | Locks: <Files/Containers affected>`)*

- [Claude-Code] [2026-09-15 12:25 UTC+7]: Creating LXC 102 (dev-host) and migrating t3code to a dedicated custom Docker image | Locks: t3code container/volume on docker-host, configs/docker-compose/t3code.yml, docs/architecture.md, docs/services.md

---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Selesai task, update `CHANGELOG.md`, bersihkan lock dari file ini, lalu `git add . && git commit && git push`.
