# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry
















---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file or critical doc, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Once your task is finished and verified, update `CHANGELOG.md`, clear your lock from this file, then run `git add <files> && git commit -m "..." && git push`.
