# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry

- [Claude Code] 2026-09-18: Redeploying yado, malas, sso-yado (fresh install, wiping old containers/volumes/DB) | Locks: yado-hosts (yado, malas, sso-yado-app-1, sso-yado-nginx-1, shared-postgres DBs `malas`/`db_sso`)

---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Selesai task, update `CHANGELOG.md`, bersihkan lock dari file ini, lalu `git add . && git commit && git push`.
