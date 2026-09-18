# homelab-ops

Infrastructure-as-docs repo for managing a personal homelab (Lenovo ThinkCentre M710q) with Claude Code.

## How this works

This repo is meant to be cloned on any device (laptop, desktop, etc.) and opened with Claude Code.
`CLAUDE.md` contains the operating instructions Claude Code reads automatically — it defines
four modes (planning, setup, maintenance, automation) so a fresh session on any device behaves
consistently, using this repo's files as the shared source of truth instead of chat memory.

## Structure

```
homelab-ops/
├── CLAUDE.md              # instructions Claude Code reads every session
├── docs/
│   ├── architecture.md    # current state of the infrastructure
│   ├── roadmap.md         # planned next steps
│   ├── decisions.md       # why things were chosen a certain way
│   └── services.md        # registry of every running service
├── configs/
│   └── docker-compose/    # compose files for each service
├── scripts/                # automation scripts (backup, health check, etc.)
├── CHANGELOG.md            # dated log of every change made
├── .env.example             # template for required secrets (copy to .env, gitignored)
└── .gitignore
```

## Usage

```bash
git clone https://github.com/<your-username>/homelab-ops.git
cd homelab-ops
claude
```

Then just talk to Claude Code normally — e.g. "install Jellyfin", "check why Immich is down",
"plan how to add the external HDD enclosure". It will read the docs, act according to the
detected mode in `CLAUDE.md`, and update the relevant files afterward.

## Physical hardware note

Lenovo M710q (Tiny form factor) only has 1 internal 2.5" bay + 1 M.2 NVMe slot. The planned
4x 2.5" HDD + 1 extra SSD do not fit internally — see `docs/decisions.md` for the external
USB enclosure (DAS) approach chosen instead.
