# Architecture - Current State

> This file reflects what EXISTS right now. Update it whenever the actual topology changes.
> Last verified: 2026-09-13 (via live SSH verification)

## Hardware

- **Device:** Lenovo ThinkCentre M710q Tiny (product no. `10MQS1EU00`, confirmed via `dmidecode`)
- **CPU:** Intel Core i5-7500, 4 cores / 4 threads, 3.4GHz — **mismatch, unresolved:** the
  purchase decision below was for an **i7-7700 (4C/8T)**. Verified via SSH (`lscpu`): the
  installed chip has no hyperthreading and is a different SKU entirely, not just a TDP variant
  (unlike the earlier i7-7700 vs i7-7700T correction). User chose to proceed with setup and
  document this rather than pause for a seller dispute (2026-09-11) — worth following up.
- **RAM:** 32GB (confirmed via `free -h`, matches the decision below)
- **M.2 slot:** confirmed NVMe-capable — repurposed to host an expansion card (see storage
  topology below), not used for an OS NVMe drive
- **Internal storage:** see "Storage Topology (FINAL)" below — the OS drive and expansion setup
  are non-standard for this Tiny form factor, worth reading in full before doing hardware work

## Storage Topology (FINAL)

This device's 2 physical drive slots (1x M.2, 1x internal 2.5" bay) are used unconventionally to
get more drives than the chassis nominally supports, without an external USB enclosure:

- **M.2 slot (NVMe-capable) → LM418 card (M.2 NVMe to 5-port SATA expansion card).** The M.2 slot
  doesn't hold a drive directly — it hosts this expansion card, which breaks out to 5 SATA ports
  for additional HDDs.
- **Internal 2.5" bay (native SATA) → "SSD M.2 SATA/mSATA to SATA 3.0 2.5\"" adapter → OS SSD.**
  The OS drive is physically an **M.2 SATA SSD** (not a standard 2.5" SSD), so it needs this
  adapter to plug into the native 2.5" SATA bay. This is the OS/Docker/projects/DB-metadata
  drive.
- **3 additional HDDs → LM418's SATA ports → external docks.** The LM418 breaks out to 5 SATA
  ports; 3 are used for HDD-Music (Seagate Barracuda 2TB 3.5", port #1, single-bay dock with
  fan), HDD-Media (1TB 2.5"), and HDD-Cloud (1TB 3.5") — the latter two in a separate multi-bay
  dock. All physically external, outside the M710q chassis. See "Storage Drives" below for full
  per-drive detail.
- **Power for the external HDD dock:** separate **Enhance ENP-2320 PSU** (Flex ATX, 200W,
  Active PFC), not the M710q's internal PSU. Two independent power domains: internal M710q PSU
  for the mini PC itself, external Flex ATX PSU just for the HDD dock(s). Chosen over a cheap
  generic PSU specifically to avoid voltage-spike risk to the HDDs — see `decisions.md`. Since
  this PSU has no motherboard attached, it needs a 24-pin ATX jumper (shorts PS_ON to Ground) to
  power on, plus Molex-to-SATA power cables per drive.
- **Cable routing:** the case backplate is left open to route SATA data + power cables from the
  LM418 out to the external dock. The remaining backplate opening (over the RAM) is covered with
  a magnetic mesh panel for basic dust/physical protection.

**Net effect:** 1 internal M.2-SATA OS SSD (via adapter, in the native 2.5" bay) + 3 external
HDDs (via the LM418 card riser'd off the M.2 slot) — 4 drives total from a chassis that
nominally only takes 1+1, without needing a USB DAS enclosure.

- **Filesystem:** each of the 3 HDDs is single-drive, no RAID/pooling across them (see "Storage
  Drives" below and `decisions.md`).
- **Mount points:** `/mnt/hdd-music/`, `/mnt/hdd-media/`, `/mnt/hdd-cloud/` (see folder
  structure further down this file — supersedes the old single `/mnt/hdd2tb/` plan).

## Virtualization Layer

```
Proxmox VE 9.2.2 (bare metal hypervisor) — pve.suryatmaja.dev, 192.168.18.224
  ├── LXC 100: "docker-host" (Ubuntu Server 24.04 LTS) — 192.168.18.225
  │     RAM allocated: 12GB (of 32GB total)
  │     CPU allocated: 4 cores (of 4 total on i5-7500)
  │     Storage: 150GB (local-lvm thin pool)
  │     Proxmox container features "nesting=1,keyctl=1" enabled
  │     Docker Engine 29.8.0 + Compose plugin v5.5.1 + Tailscale
  │     Purpose: Core infrastructure, media stack, DB, tools, and personal web projects
  └── LXC 101: "apps-host" (Ubuntu Server 24.04 LTS) — 192.168.18.226
        RAM allocated: 4GB (of 32GB total)
        CPU allocated: 2 cores
        Storage: 30GB (local-lvm thin pool)
        Proxmox container features "nesting=1,keyctl=1" + TUN passthrough (/dev/net/tun)
        Docker Engine 29.8.0 + Compose plugin v5.5.1 + Tailscale
        Purpose: Dedicated environment for personal web projects (whitearchive, malas, etc.)
```

**LXC, not VM** — chosen over a VM for docker-host because LXC shares the host kernel (near-zero
overhead, RAM/CPU used efficiently) vs. a VM's full hardware virtualization (heavier, RAM/CPU
allocation less flexible). Trade-off: Docker running inside an LXC needs the Proxmox container
feature `nesting=1` enabled (and sometimes `keyctl=1`) to work — without it, Docker/container
operations inside the LXC fail with permission/cgroup errors. See `decisions.md`.

## Network

```
Router ISP (main house WiFi)
  └── Switch Gigabit: TP-Link TL-LS1005G (5-port)
        └── PC + Homelab (M710q)
```

- **Router:** the ISP's own router — no dedicated MikroTik router deployed for now (see
  `decisions.md`: skipped for budget efficiency, not currently needed).
- **Switch:** TP-Link TL-LS1005G, 5-port Gigabit — added specifically so PC↔Homelab file
  transfer gets full Gigabit speed.
- **Proxmox host:** `pve.suryatmaja.dev` — `192.168.18.224/24`, gateway `192.168.18.1`
- **Static IP for docker-host:** `192.168.18.225/24`, gateway `192.168.18.1`
- **Static IP for apps-host:** `192.168.18.226/24`, gateway `192.168.18.1`
- **DNS:** `1.1.1.1` primary, `192.168.18.1` fallback
- **Remote access:** Tailscale — installed and connected on docker-host (`100.89.249.96`, hostname `docker-host`, suffix `taila813af.ts.net`, tailnet `srytmj.github`). Joined via pre-generated auth key. `--accept-dns=false`.
- **Public Domain & Cloudflare Tunnel:** `cloudflared` publishes selected services to the internet (`suryatmaja.dev`, `whitearchive.my.id`) without opening router ports.

## Storage Path Convention

| Data type | Location |
|---|---|
| OS, Docker engine, images | OS SSD (M.2 SATA, via adapter in the internal 2.5" bay) |
| Project code + dependencies | OS SSD (`/mnt/homelab_projects/`) |
| Database metadata (Postgres/Redis) | OS SSD |
| Music (Jellyfin) | HDD-Music, 2TB 3.5" (`/mnt/hdd-music/`) |
| Movies/TV, anime (video), manga | HDD-Media, 1TB 2.5" (`/mnt/hdd-media/`) |
| Nextcloud + Syncthing + Shared | HDD-Cloud, 1TB 3.5" (`/mnt/hdd-cloud/`) |

**Rule:** never let bulk media default-write to the OS SSD. Always explicitly map Docker volumes to the correct HDD's path.

## Storage Drives — 3 HDDs, Each With a Dedicated Purpose

| Drive | Capacity | Form factor | Mount point | Purpose | Status |
|---|---|---|---|---|---|
| HDD-Music (Seagate Barracuda) | 2TB | 3.5" | `/mnt/hdd-music/` | Music library for Jellyfin (`jellyfin/music`), backups fallback | **Active.** Formatted ext4 (`/dev/sdc1`). 717GB music migrated here on 2026-09-13. Leftover migration staging cleaned. |
| HDD-Media | 1TB | 2.5" | `/mnt/hdd-media/` | Movies/TV, anime (video), manga raw + reader | **Active.** Physically `sdb2` (ext4, label `hdd-media`), mounted via fstab on PVE, bind-mounted to LXC 100. Jellyfin and Komga mounted. |
| HDD-Cloud | 1TB | 3.5" | `/mnt/hdd-cloud/` | Nextcloud, Syncthing, Shared LAN SMB folder | **Active.** Physically `sdd2` (ext4, label `hdd-cloud`), same fstab + LXC bind-mount pattern. Usage dropped to 13% after music relocation. |
| HDD-Backup (WD Blue) | 320GB | 3.5" | `/mnt/hdd-backup/` | Dedicated Restic backup target for DB dumps + config | **Pending.** Needs physical mounting/dock solution. |

### HDD-Music (`/mnt/hdd-music/`)

```
/mnt/hdd-music/
├── jellyfin/
│   └── music/            # 717GB relocated collection, scanned by Jellyfin
└── backups/              # Fallback local backup target
```

### HDD-Media (`/mnt/hdd-media/`)

```
/mnt/hdd-media/
├── jellyfin/
│   ├── movies/
│   ├── tv/
│   └── anime/            # video anime — watched through Jellyfin
├── manga-raw/            # Master raw collection (Samba \\docker-host\manga), user adds/edits files here
├── manga-reader/         # Auto-optimized WebP collection generated by manga-optimizer.service, mounted to Komga
└── qbittorrent/
    └── downloads/        # Completed and active torrent downloads
```

### HDD-Cloud (`/mnt/hdd-cloud/`)

```
/mnt/hdd-cloud/
├── nextcloud/            # Nextcloud data root
├── syncthing/            # P2P device sync folder
└── shared/               # ad-hoc file drop, accessed via SMB \\docker-host\shared
```

**Which folders are safe to drop files into manually (via SMB) vs. app-managed only:**

| Folder | Manual file drop via SMB? | Why |
|---|---|---|
| `jellyfin/movies/`, `/tv/`, `/anime/`, `/music/` | ✅ Yes — normal workflow | Jellyfin scans folder for new files |
| `manga-raw/` | ✅ Yes — master drop location | `manga-optimizer.service` automatically detects, optimizes to WebP, and updates `manga-reader/` |
| `manga-reader/` | ❌ No | Auto-generated target for Komga reader — managed solely by `manga-optimizer` |
| `nextcloud/` | ❌ No | Internal database tracks files — use Nextcloud UI/sync client |
| `syncthing/` | ⚠️ Handled via Syncthing | Managed by Syncthing sync protocol |
| `shared/` | ✅ Yes | General purpose LAN share |

## Windows Network Access (SMB/Samba & WSDD)

- **Native systemd services**: `smbd` and `wsdd` running on `docker-host`.
- Shares:
  - `shared` → `/mnt/hdd-cloud/shared`
  - `manga` → `/mnt/hdd-media/manga-raw`
  - `media` → `/mnt/hdd-media`
  - `music` → `/mnt/hdd-music`
- **WSDD (Web Services Dynamic Discovery)** enabled so docker-host is automatically discoverable in Windows File Explorer network neighborhood.
