# Homelab Operations - Instructions for Claude Code, Antigravity & All AI Agents

## Context

This repo manages a homelab server (Lenovo ThinkCentre M710q Tiny — purchased as i7-7700 4C/8T,
but the CPU physically installed verified as i5-7500 4C/4T, unresolved discrepancy, see
`docs/architecture.md` — 32GB RAM). Full current spec and topology: see `docs/architecture.md`.

Server runs Proxmox VE (hypervisor) + Docker (inside 1 Ubuntu LXC, `docker-host`), hosting a
growing list of personal web projects, a media stack (Jellyfin, Nextcloud, Komga), shared PostgreSQL + Redis, and self-hosted tools. **`docs/services.md` is the actual current/planned service list.**

## Before doing anything

0. **`git pull` first, every session, before reading anything else or making any change.**
   This repo is worked on across multiple devices and parallel AI agents. Local files can be stale the moment a session starts. Never trust a file's on-disk state without pulling first.
1. Read `CURRENT_OPS.md` to ensure no active file or container lock exists from another agent.
2. Read `docs/architecture.md` for current infrastructure state (source of truth for "what exists now").
3. Read `docs/roadmap.md` for planned next steps (source of truth for "what's planned").
4. Read `docs/decisions.md` if unsure why something is configured a certain way.
5. Read ONLY the top 20-30 lines of `CHANGELOG.md` (`head -n 30 CHANGELOG.md`). Never read the full file (wastes 16k+ tokens).

Never assume the state of the server — always verify via SSH before making changes.

## Multi-Agent / Multi-Tool Synchronization Rules (STRICT)

Multiple AI agents (Claude Code, Google Antigravity/Gemini, Roo Code, Cursor, etc.) operate on this repository in parallel. There is NO shared runtime memory between different AI sessions. **Git + `CURRENT_OPS.md` + `CHANGELOG.md` is the sole source of truth.**

### 🛑 0. SESSION SCOPE & USER APPROVAL RULE (STRICT)
- **Homelab-Ops Session Boundary**: Sesi di repo ini murni untuk **admin, infrastruktur, ops, monitoring, dan maintenance homelab**. JANGAN membuat/scaffold aplikasi atau codebase baru dari nol di dalam repo/sesi ini. Pembuatan project/aplikasi baru harus dikerjakan di sesi/workspace terpisah oleh user.
- **Mandatory User Confirmation Before Editing Code/Containers**: Jika ada kebutuhan untuk mengubah kode aplikasi, mengedit konfigurasi project yang sedang berjalan, memodifikasi environment container, atau merestart/menghapus container, **WAJIB konsultasi dan minta izin eksplisit kepada USER terlebih dahulu**. Jangan pernah bypass atau langsung coding/deploy sendiri tanpa persetujuan user.

### 🚨 1. TASK REGISTRY & LOCKING (`CURRENT_OPS.md`)
- **Claim Before Touch**: If you are about to modify a container, service configuration (`configs/docker-compose/*.yml`), or critical doc, record your active task and lock target in `CURRENT_OPS.md`:
  `"- [Agent-Name] [Timestamp]: Modifying <service> | Locks: <files/containers>"`
- **Respect Active Locks**: If another agent has locked a service or file in `CURRENT_OPS.md`, do NOT touch it until released.
- **Release Promptly**: As soon as the task is finished and verified, clear your lock from `CURRENT_OPS.md`, log to `CHANGELOG.md`, and commit/push.

### ⚡ 2. EXECUTION PERFORMANCE & TOKEN EFFICIENCY
1. **Never Allow Tool Commands to Hang or Spawn Ghost Tasks**:
   - Always set `WaitMsBeforeAsync: 10000` (max sync) or run bounded commands (`timeout 30s ...`).
   - Never run `pct reboot` over blocking SSH inside the same container being rebooted.
2. **One-Shot Batched SSH Scripts**:
   - Instead of running 5-10 separate sequential read/check commands, batch inspection and execution into a single clean Bash heredoc script over SSH (`ssh docker-host 'bash -s' << 'EOF' ... EOF`).
3. **Strict Token Conservation**:
   - **DO NOT read full `CHANGELOG.md`** (~65KB). Only read `head -n 30 CHANGELOG.md`.
   - Restrict log outputs (`docker logs --tail 30 ...`, `git log -n 5`, `docker ps --format ...`).
   - Keep conversational explanations direct, concise, and factual.
4. **Strict No-Polling Rule (Prevent ACP RPC Deadlock & Cancel Failures)**:
   - **DILARANG KERAS** melakukan loop polling aktif di bash (`while ...; do sleep 2; done`, `sleep X && check`).
   - **DILARANG KERAS** memanggil tool secara berulang-ulang (`view_file` pada task log, loop `ps aux`, dll.) saat menunggu perintah panjang (`docker build`, `docker pull`, download besar).
   - Begitu sebuah command beralih ke background task async, **AI WAJIB SEGERA BERHENTI MEMANGGIL TOOL**. Biarkan event reactive wakeup T3 Code yang membangunkan secara otomatis saat selesai.
   - Melanggar aturan ini membanjiri antrean JSON-RPC ACP harness hingga freeze dan gagal merespons sinyal cancel user (`ACP transport operation call-rpc failed for method session/cancel`).

### 🛡️ 3. ANTI-HALLUCINATION & LIVE VERIFICATION
1. **Never Hallucinate / Guess Server State**:
   - Do NOT assume a service is running, installed, or broken based on outdated chat history or training assumptions.
   - **ALWAYS check live server state first** via SSH (`docker ps`, `systemctl status`, `df -h`, `ls -la`) before taking action or giving advice.
2. **Safe File Editing (Anti-Truncation Rule)**:
   - When updating large existing files (`architecture.md`, `services.md`, `CHANGELOG.md`), do NOT blindly replace from line 1.
   - Always run `git diff --stat` before committing to ensure no content was accidentally wiped out.
3. **Keep `docs/services.md` and `docs/architecture.md` in Sync**:
   - When a service or storage mount is added, removed, or remapped, immediately update the table in `docs/services.md` or `docs/architecture.md`.

### 🔄 4. GIT SYNC LIFECYCLE
### Fast Git Commits
- Git config (Maja / suryatmaja.dev@gmail.com) is already permanently configured.
- NEVER check `gh api`, `gh auth`, or inspect other repos before committing.
- Commit directly: `git add <specific-code-files> && git commit -m "..." && git push`
- NEVER stage or diff media/binary directories (`media/`, video files, etc.).

1. **Start of Task**: Run `git pull` before reading or modifying anything.
2. **End of Task**:
   - Verify server is healthy and change works.
   - Log entry in `CHANGELOG.md`.
   - Clear lock in `CURRENT_OPS.md`.
   - Run `git add <files>`, commit as user Maja (`git config user.name "Maja" && git config user.email "suryatmaja.dev@gmail.com"`), and push:
     `git commit -m "<type>: <concise description>" && git push`
   - Never add `Co-Authored-By` trailers.

---

## Modes of operation

### 1. Planning mode
- **Homelab infrastructure planning**: Hardware capacity, service architecture trade-offs, scaling roadmap.
- **Operational planning**: Deciding what to automate next, flagging stale docs.
- **In planning mode: discuss first, don't execute.** Only write to `docs/decisions.md` and/or `docs/roadmap.md` once something is actually decided. Never touch live server config in this mode.

### 2. Setup mode
When asked to install/configure something new:
1. `git pull` & check `CURRENT_OPS.md`.
2. Register lock in `CURRENT_OPS.md`.
3. SSH into server, execute setup via batched commands.
4. Save docker-compose file to `configs/docker-compose/<service-name>.yml`.
5. Update `docs/services.md` (port, purpose, data location).
6. Update `docs/architecture.md` if topology changed.
7. Clear lock in `CURRENT_OPS.md`, log in `CHANGELOG.md`, commit and push.

### 3. Maintenance mode
When asked to check/fix/troubleshoot:
1. `git pull` & check `CURRENT_OPS.md`.
2. SSH in, check logs (`docker logs --tail 50`, `journalctl`, etc.).
3. Diagnose issue, explain what's wrong before fixing.
4. Ask before making any destructive change (e.g. deleting volumes, stopping active production containers).
5. Apply fix, verify live state.
6. Clear lock in `CURRENT_OPS.md`, log in `CHANGELOG.md`, commit and push.

### 4. Automation mode
When asked to automate a recurring task:
1. Write script in `scripts/`.
2. Set up cron job or systemd timer.
3. Document in `docs/services.md`.
4. Clear lock in `CURRENT_OPS.md`, log in `CHANGELOG.md`, commit and push.

---

## Execution preference
When Superpowers reaches the execution phase, always use `executing-plans`
(inline, single-context) instead of `subagent-driven-development`, unless
explicitly told otherwise. This keeps token usage lower for infrastructure
tasks that are typically straightforward.

---

## Storage Convention Reminder
- OS, Docker engine, images, project code, and DB metadata live on internal SSD (`/`).
- Bulk media lives on dedicated external HDDs:
  - `/mnt/hdd-music/`: Music library (Jellyfin) + fallback backup target
  - `/mnt/hdd-media/`: Movies/TV, anime, manga-raw, manga-reader (Komga), torrent downloads
  - `/mnt/hdd-cloud/`: Nextcloud data, Syncthing, shared LAN SMB drop

---

## 🎵 Music Library Standards (`hdd-backup` & `hdd-music`)
Full specifications are recorded in [`docs/music-standards.md`](docs/music-standards.md). Always follow these rules:
1. **Zero Loose Albums Rule**: Every album/single must live inside a canonical artist or franchise folder ending with `~` (e.g. `Anime/学園アイドルマスター ~/`, `J-Pop/＊Luna ~/`).
2. **Windows SMB Safe Naming**: Never use characters forbidden in Windows NTFS/FAT (`\ / : * ? " < > |`) in folder or file names. Use full-width equivalents (e.g. `＊` instead of `*`, remove colons `:`) to prevent Samba 8.3 DOS name mangling (`_FCR9Q~X`, `_P6X4P~L`).
3. **Franchise Hierarchies**:
   - **Uma Musume**: 5 canonical subseries folders (`01. WINNING LIVE Series`, `02. ANIMATION DERBY Series`, `03. STARTING GATE Series`, `04. Theatrical & Specials`, `05. Compilations`). Remove redundant full-CD images (`LACM-*.flac`, `LACA-*.flac`) and root cuesheets when split tracks exist.
   - **THE IDOLM@STER**: Master franchise umbrella (`Anime/THE IDOLM@STER ~/`). Sub-branches include `学園アイドルマスター` (strict 4-tier model: `01. Solo`, `02. Duo`, `03. Trio`, `04. All Stars & Units`), `シャイニーカラーズ` (subseries: `01. Song for Prism Series`, `02. ECHOES Series`, `03. Anime Series`, `04. Unit Singles & Compilations`), and `vα-liv`. Refer to `docs/music-standards.md` for full categorization rules.
   - **Gochuumon wa Usagi Desu ka**: 3 canonical subseries folders (`01. Theme Songs (OP & ED)`, `02. Character Song Series`, `03. Albums & Compilations`). Audio tracks must reside in the album root (never nest in `FLAC/`). Split all uncompressed WAV+CUE images into FLAC tracks and purge piracy tracker junk.
4. **Master Catalog**: Always re-index `/mnt/hdd-backup/music/catalog.sqlite` whenever music tracks or folders are added, moved, or deleted.

