# n8n Auto-Deploy (git polling) — what, why, how

> Status (2026-10-04): **infrastructure ready, workflow being built by the user in n8n, dry-run only.**
> Nothing is pulled or built automatically yet. Decision log entry: `docs/decisions.md` (2026-10-04).
> Changelog: entries 190, 191.

## 1. Goal
When a project's `main` gets a new commit on GitHub, the server updates it automatically
(`git pull --ff-only` + `docker compose up -d --build`).

**Exception:** `gddl`, `nhdl` and `gamdl-dashboard` must never be updated while a download is in
progress (an update restarts the container/service and would kill the download).

## 2. Decisions and why
| Decision | Why |
|---|---|
| **Polling every 5 min**, not GitHub webhook | n8n has no public webhook URL (`WEBHOOK_URL` unset); servers are LAN/Tailscale only. Webhook can be added later. |
| **n8n as orchestrator** | Already running on `docker-host`; user wants to learn n8n. A standalone systemd timer/script (`scripts/git-auto-deploy.sh`, never installed) was the alternative. |
| **Logic lives in a script on each host** (`n8n-deploy-check.sh`), n8n only schedules/loops/notifies | Keeps the workflow simple and the safety rules in one testable place. |
| **gddl / nhdl: update only when idle ("opsi A")** | Busy detection per app (see section 4). Unknown status = busy (fail safe). |
| **gamdl-dashboard excluded entirely (for now)** | It runs on `media-hosts` as a systemd service (restart kills a running download via `KillMode=control-group`) and its checkout is on branch `feat/follow-artists`, not `main`. |
| **Skip projects with tracked local changes** | A pull could conflict or hide server-only config. They are reported as `skip-dirty`, never touched. |
| **Dedicated n8n SSH key restricted by a forced command** | n8n can only run `n8n-deploy-check <project> [--apply]`, not a shell. n8n holding root SSH to every host would be a big blast radius. |
| **Read-only GitHub deploy keys, one per private repo** | `portofolio` and `situlah` are private and the host had no git credentials. GitHub requires a unique deploy key per repo. |

## 3. Architecture
```
n8n (docker-host)
  Schedule(5 min) -> Code(project list) -> Switch(host) -> SSH node (per host credential)
        -> runs on the host:  n8n-deploy-check <project>   (via forced command gate)
        -> JSON result -> parse -> IF/notify
```
Per host files (`personal-hosts` 192.168.18.228, `yado-hosts` 192.168.18.226), repo copies in `scripts/`:
- `/opt/scripts/n8n-deploy-check.sh` — fetch, compare, safety checks, optional apply. Prints ONE JSON line:
  `{"project","branch","behind","dirty","busy","action","detail"}`.
  `action` = `uptodate | would-deploy | deployed | skip-dirty | skip-branch | skip-busy | skip-locked | error`.
  Default is **dry-run**; only `--apply` pulls/builds. Deploys only if: on `main`, no tracked local changes,
  fast-forward, not busy.
- `/opt/scripts/n8n-ssh-gate.sh` — forced command for the n8n key. Accepts only
  `[cd <path> ;] n8n-deploy-check <project> [--apply]` (the n8n SSH node always prepends `cd <dir> ;`).
- `~/.ssh/authorized_keys` line: `restrict,command="/opt/scripts/n8n-ssh-gate.sh" ssh-ed25519 ... n8n-deploy`
  (fingerprint `SHA256:tXi/3DU8LQxrZG3IJKfFwqqYYxSESLU71+UboXp+Djo`). The matching **private key lives only in the
  n8n credentials** (delete the copy on the PC).
- `personal-hosts:~/.ssh/deploy_portofolio`, `deploy_situlah` (+ `~/.ssh/config` aliases `github-portofolio`,
  `github-situlah`; repo remotes are `git@github-<repo>:samsmon/<repo>.git`).

Projects covered: `personal-hosts` = gddl, nhdl, portofolio, situlah, tabsync, group-checklist;
`yado-hosts` = yado, sso.yado, malas, pore-js. (`/opt/projects/portfolio` on personal-hosts is a stale duplicate
of `portofolio`, deliberately not listed.)

## 4. Busy detection (what "download in progress" means)
| App | Check (run on the host) | Notes |
|---|---|---|
| nhdl | `curl localhost:8098/api/status` -> `engineStatus` | idle only if `PAUSED`/`IDLE`/`STOPPED`; `RUNNING`, `COOLDOWN`, empty or unknown = busy |
| gddl | `/opt/projects/gddl/config/downloads.json` | busy if status `downloading`/`compressing`/`moving`, or file modified in last 2 min. Not yet proven that gddl writes `downloading` to this file during a live download — verify next time a download runs. Its HTTP API needs login, so it is not used. |
| gamdl-dashboard | would be `/api/state` item status `downloading` | not wired up (excluded) |

## 5. Current state of each project (dry-run 2026-10-04)
- Up to date: gddl, nhdl, group-checklist, yado, sso.yado, malas, pore-js
- Behind, would deploy: portofolio
- Behind but `skip-dirty`: **tabsync** (server-only `compose.yml` edit: `container_name` + port `8097:8080`; incoming commits don't touch it) and **situlah** (local edit of `database/seeders/IndSasSeeder.php` removing the `tsastw1..4` columns; unclear if intentional). Fix in each project's own repo (e.g. override file / commit), then they join automatically.

## 6. Build the n8n workflow (stages; run and check each before moving on)
1. **Manual Trigger** -> **Code** (Run Once for All Items) returning the 10 `{host, project}` items -> expect 10 items.
2. **Switch** on `{{ $json.host }}`: rule `personal` -> output 0, `yado` -> output 1 -> expect 6 and 4 items.
3. One **SSH** node per output (Execute Command, credential `personal-hosts` / `yado-hosts`), command
   `n8n-deploy-check {{ $json.project }}` (Expression mode). In node Settings enable **Continue On Fail** and
   **Always Output Data**. No `--apply` yet.
4. **Merge** (Append) both branches -> **Code**: `JSON.parse($json.stdout)` per item (catch -> action `error`).
5. **IF** on `action` in (`deployed`, `error`, `skip-busy`) -> notification (Telegram, optional).
6. Replace Manual Trigger with / add **Schedule Trigger** (every 5 min) **only after** dry-run output looks right.
7. Last: add `--apply` to the SSH command (only for the projects you trust first, e.g. portofolio), watch a few cycles.
8. Export the finished workflow JSON into `configs/n8n/` so it is tracked in git.

## 7. Things we ran into (so you don't re-debug them)
- PowerShell 5.1 drops `-N ""` for `ssh-keygen` -> use `-N '""'` or omit `-N` and press Enter twice. Linux commands
  (`ssh-keygen -f ~/.ssh/...`, `cat`) must run **on the server** (`ssh <host>`), PowerShell commands on the PC.
- GitHub "Key is invalid... OpenSSH public key format" = pasted a private key or a broken/multi-line public key.
- A GitHub deploy key can't be shared across repos; create the key **on the server that fetches**, keep it read-only
  (no "Allow write access"). Don't reuse the n8n SSH key as a deploy key.
- n8n SSH node sends `cd / ; <command>` even with an empty Working Directory -> the gate accepts that exact prefix.
- n8n credential Private Key = the whole `n8n_deploy` file incl. `BEGIN/END` lines (not the `.pub`).

## 8. Undo / rollback
- Disable: deactivate the n8n workflow (nothing else runs on a schedule).
- Remove n8n access: delete the `n8n-deploy` line from `~/.ssh/authorized_keys` on both hosts.
- Revert a repo remote: `git remote set-url origin https://github.com/samsmon/<repo>.git`.
- Remove deploy keys: GitHub repo Settings -> Deploy keys, and `rm ~/.ssh/deploy_<repo>*` + the `Host github-<repo>` block.
- Remove scripts: `rm /opt/scripts/n8n-deploy-check.sh /opt/scripts/n8n-ssh-gate.sh` on both hosts.

## 9. Open items
- [ ] Finish the n8n workflow (stages 3-8 above), then enable `--apply` gradually.
- [ ] Resolve `tabsync` and `situlah` dirty state (in their own repos).
- [ ] Verify gddl writes `downloading` to `downloads.json` during a real download (otherwise gddl busy detection is only the 2-min mtime guard).
- [ ] Decide on gamdl-dashboard: move to `main`, then add a busy check via `/api/state` (item status `downloading`).
- [ ] Optional: Telegram notifications; GitHub webhook trigger (needs public n8n URL).
- [ ] Make deploy keys read-only on GitHub (the `portofolio` one was added with write access).
- [ ] Delete the `n8n_deploy` private key file from the PC after it is stored in n8n; rotate the n8n login password
      (it was shared in chat).

## Appendix A — Session log (2026-10-04, chronological, who did what)
Legend: **[AI]** done by Claude Code, **[User]** done by the user, **[Blocked]** refused by the harness safety check.

1. **[AI] Pre-checks (read-only).** Git was in sync. `CURRENT_OPS.md` only had another agent's lock on `homelab-dashboard` (no overlap).
   Found: the web projects live on `personal-hosts` and `yado-hosts`, not `docker-host`; `scripts/git-auto-deploy.sh` exists
   but was never installed anywhere (docs say Cockpit handles deploy, yet portofolio redeploys were still manual);
   several repos had local edits; `/opt/projects/portfolio` duplicates `portofolio`; gamdl-dashboard is a systemd service on branch `feat/follow-artists`.
2. **[AI] Plan v1** (script + systemd timer) presented. **[User]** asked to use n8n instead (to learn). Decisions: polling first,
   opsi A (update when idle) for gddl/nhdl, gamdl excluded.
3. **[AI] n8n + endpoint checks (read-only).** n8n 2.38.7 on `docker-host`, SSH node present, TCP 22 reachable from the n8n container to all hosts,
   no `WEBHOOK_URL`. nhdl `/api/status` open (`engineStatus`); gddl API needs login (401) so busy is read from `downloads.json`;
   gamdl `/api/state` open.
4. **[AI] Wrote `scripts/n8n-deploy-check.sh`**, claimed a lock in `CURRENT_OPS.md`, installed it on `personal-hosts` + `yado-hosts` (dry-run default),
   ran it for all 10 projects. Result: `portofolio` + `situlah` fetch failed (private repos, no git credentials on the host). Released lock, commit `2e776d9` (changelog 190).
5. **[User]** Shared n8n login credentials in chat and invited a login. **[AI]** declined (entering passwords is not allowed) and recommended rotating the password.
6. **[AI] Tried to create the n8n SSH key + deploy keys. [Blocked]** by the auto-mode safety check ("unauthorized persistence": creating keys / editing `~/.ssh`).
   A background attempt produced nothing (verified: no key, no `authorized_keys` change). Decision: the **user** creates keys; the AI only creates inert files.
7. **[User] Generated `n8n_deploy` on the PC** (hit the PowerShell `-N ""` issue, fixed with `'""'`). **[AI]** wrote + installed the gate script
   `n8n-ssh-gate.sh` and tested allow/deny cases (injection, path traversal rejected).
8. **[User]** Added deploy keys on GitHub. **[AI]** compared fingerprints: situlah key matched the server; the "portofolio" key was actually the **n8n PC key**
   (wrong key, write access). User replaced it with a server-generated `deploy_portofolio`; both now verified by fingerprint.
9. **[User]** Created `~/.ssh/config` aliases and switched remotes to SSH (first attempt ran PowerShell in the server shell; redone correctly).
   **[AI]** re-ran dry-run: fetch OK for both repos.
10. **[AI] Diff review (read-only)** of `tabsync` and `situlah` dirty files (see section 5). Nothing changed.
11. **[User]** Installed the n8n public key into `authorized_keys` with `restrict,command=...` on both hosts (PowerShell pipe). **[AI]** verified lines, fingerprint, no stray `\r`.
12. **[User]** Created n8n SSH credentials and a test node. First runs returned `command not allowed`. **[AI]** added a temporary debug line to the gate (with approval),
    which showed n8n sends `cd / ; n8n-deploy-check <project>`. Gate pattern widened to accept only that prefix, debug removed (backup + log deleted),
    tests re-run; user confirmed the node works on both hosts. Commit `314d8b8` (changelog 191).
13. **[AI]** Wrote this runbook + decision entry (commit `2ab97c3`). **[User]** is building the workflow in n8n (section 6).

## Appendix B — State changes made on servers this session (for audit/rollback)
| Where | What | Who |
|---|---|---|
| `personal-hosts`, `yado-hosts` | `/opt/scripts/n8n-deploy-check.sh`, `/opt/scripts/n8n-ssh-gate.sh` (755) | AI |
| `personal-hosts`, `yado-hosts` | `~/.ssh/authorized_keys` + 1 line (n8n key, restricted) | User |
| `personal-hosts` | `~/.ssh/deploy_portofolio(.pub)`, `deploy_situlah(.pub)`, `~/.ssh/config`, `known_hosts` + github.com | User |
| `personal-hosts` | `/opt/projects/portofolio` and `/opt/projects/situlah` remote URL -> SSH alias | User |
| `/tmp` on both hosts | temp debug log + `.bak` created then deleted | AI |
| GitHub | deploy keys on `samsmon/portofolio`, `samsmon/situlah` (read/write currently) | User |
| n8n | SSH credentials `personal-hosts`, `yado-hosts`; workflow `test-ssh` / `auto-deploy` (in progress) | User |
| Containers / services | **No container, compose file or service was restarted, rebuilt or pulled.** | — |
