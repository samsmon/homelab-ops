# Architecture - Current State

> This file reflects what EXISTS right now. Update it whenever the actual topology changes.
> Last verified: 2026-09-14 (via live SSH verification across Proxmox, docker-host, and apps-host)

## Hardware

- **Device:** Lenovo ThinkCentre M710q Tiny (product no. `10MQS1EU00`, confirmed via `dmidecode`)
- **CPU:** Intel Core i5-7500 (7th Gen Kaby Lake), 4 cores / 4 threads, 3.40 GHz base (up to 3.80 GHz max turbo), 65W TDP. Confirmed via `lscpu`.
- **Integrated GPU (iGPU):** Intel HD Graphics 630 (`[8086:5912]`), kernel driver `i915`. Direct Rendering Infrastructure (DRI) passed through to `docker-host` via `/dev/dri/card0` and `/dev/dri/renderD128` for hardware-accelerated transcoding.
- **RAM:** 32GB DDR4 (recognized as 31GiB in Proxmox / `free -h`).
- **Ethernet (NIC):** Intel I219-V Gigabit Ethernet (`[8086:15b8]`), kernel driver `e1000e`.
- **M.2 Slot (PCIe/NVMe M-Key) → LM 418 Expansion Card:**
  - The internal M.2 NVMe slot is populated with an **LM 418 M.2 NVMe NGFF M Key TO 5 Ports SATA III 3.0 Card + Heatsink Chipset Taiwan J-Micron JMB585** (`01:00.0 SATA controller: JMicron Technology Corp. JMB58x AHCI SATA controller [197b:0585]`).
  - This card breaks out PCIe bandwidth into 5 native SATA III (6Gbps) ports, dedicated to running external HDDs without relying on unreliable USB enclosures.
- **Internal 2.5\" SATA Bay → M.2 SATA Adapter → OS SSD:**
  - The native internal 2.5\" SATA bay is fitted with a **SATA to M.2 SATA NGFF B + M KEY Converter Adapter Card (SATA III 6Gbps)**.
  - Houses an internal **256GB M.2 SATA SSD** (`MidasForce SSD 256GB`, serial `RE202410151200000921`, partition `/dev/sda`).
  - Contains Proxmox VE rootfs (`pve-root`), swap (`pve-swap` 8GB), and `pve-data` LVM-thin pool (`vm-100-disk-0` 150GB, `vm-101-disk-0` 30GB).

## Storage Topology (FINAL)

This device's 2 physical drive slots (1x M.2, 1x internal 2.5\" bay) are used unconventionally to host 4 storage drives (1 SSD + 3 HDDs) without an external USB DAS enclosure:

1. **Internal OS SSD (256GB M.2 SATA SSD via 2.5\" Bay Adapter)**:
   - Drive: `MidasForce SSD 256GB` (`/dev/sda`).
   - Role: Proxmox VE host OS, swap, VM/LXC virtual disks, and database metadata.
2. **HDD-Music (2TB 3.5\" Western Digital Green via LM 418 SATA Port)**:
   - Drive: `WDC WD20EZRX-00DC0B0`, serial `WD-WCC1T0899623` (`/dev/sdc1`, 1.8TB usable).
   - Role: Dedicated music streaming library (`jellyfin/music` scanned by Navidrome & Jellyfin) + local backup staging destination (`backups/`).
3. **HDD-Media (1TB 2.5\" Toshiba HDD via LM 418 SATA Port)**:
   - Drive: `TOSHIBA MQ04ABF100`, serial `Y9CSTR0WT` (`/dev/sdb2`, label `hdd-media`, 916GB usable).
   - Role: Movies/TV, anime video, raw manga master (`manga-raw`), auto-optimized reader library (`manga-reader` for Komga), and torrent downloads (`qbittorrent/downloads`).
   - *Note on disk allocation:* The physical 2.5\" Toshiba drive is partitioned as `hdd-media` (`sdb2`), while the 3.5\" Barracuda is `hdd-cloud` (`sdd2`).
4. **HDD-Cloud (1TB 3.5\" Seagate Barracuda via LM 418 SATA Port)**:
   - Drive: `ST1000DM010-2EP102`, serial `W9AS0LSD` (`/dev/sdd2`, label `hdd-cloud`, 916GB usable).
   - Role: Nextcloud data directory, Syncthing continuous device sync, and general LAN shared drop (`shared/`).

- **Power for the external HDD dock:** Separate **Enhance ENP-2320 PSU** (Flex ATX, 200W, Active PFC), not the M710q's internal 65W/90W adapter. Two independent power domains prevent power starvation and voltage-spike risks to the HDDs. Uses a 24-pin ATX jumper (shorts PS_ON to Ground) to power on without a motherboard, plus Molex-to-SATA power cables per drive and cooling fans.
- **Cable routing:** Case backplate is open to route SATA data cables from the LM 418 out to the external drive dock. The backplate opening over the RAM is covered with a magnetic dust mesh panel.

## Virtualization Layer

```
Proxmox VE 9.2.2 (bare metal hypervisor, kernel 7.0.2-6-pve) — pve.suryatmaja.dev, 192.168.18.224
  ├── LXC 100: \"docker-host\" (Ubuntu Server 24.04 LTS) — 192.168.18.225
  │     RAM allocated: 12GB (of 32GB total)
  │     CPU allocated: 4 cores (of 4 total on i5-7500)
  │     Storage: 150GB (local-lvm thin pool: vm-100-disk-0)
  │     Proxmox container features \"nesting=1,keyctl=1\" enabled
  │     Hardware Pass-through: /dev/dri/card0, /dev/dri/renderD128 (Intel HD 630 iGPU)
  │     Bind Mounts: /mnt/hdd-media, /mnt/hdd-cloud, /mnt/hdd-music
  │     Docker Engine 29.8.0 + Compose plugin v5.5.1 + Tailscale + cloudflared
  │     Purpose: Core infrastructure, homelab cockpit, media stack, DB, tools, portfolio
  └── LXC 101: \"apps-host\" (Ubuntu Server 24.04 LTS) — 192.168.18.226
        RAM allocated: 4GB (of 32GB total)
        CPU allocated: 2 cores
        Storage: 30GB (local-lvm thin pool: vm-101-disk-0)
        Proxmox container features \"nesting=1,keyctl=1\" + TUN passthrough (/dev/net/tun)
        Docker Engine 29.8.0 + Compose plugin v5.5.1
        Purpose: Dedicated environment for personal web projects (whitearchive, malas, etc.)
```

**LXC, not VM** — chosen over a VM for minimal virtualization overhead, direct host kernel efficiency, and easy filesystem bind-mounting. Requires `nesting=1,keyctl=1` for Docker engine container isolation.

## Network Architecture

```
Router ISP (Main Gateway: 192.168.18.1)
  └── Mercusys MS105G | Switch 5 Port Gigabit
        ├── Main PC (Gigabit LAN)
        └── Homelab (Lenovo ThinkCentre M710q — Intel I219-V Gigabit)
              ├── PVE Hypervisor: 192.168.18.224 (pve.suryatmaja.dev)
              ├── LXC 100 docker-host: 192.168.18.225
              └── LXC 101 apps-host: 192.168.18.226
```

- **Switch:** **Mercusys MS105G (5-Port Gigabit Desktop Switch)** connects the ISP router, Main PC, and Homelab node, ensuring full 1000 Mbps line-rate file transfers between Main PC and Samba/media shares.
- **Static IPs**:
  - Proxmox VE: `192.168.18.224/24`, gateway `192.168.18.1`
  - docker-host (LXC 100): `192.168.18.225/24`, gateway `192.168.18.1`
  - apps-host (LXC 101): `192.168.18.226/24`, gateway `192.168.18.1`
- **DNS:** `1.1.1.1` primary, `192.168.18.1` fallback.
- **Remote Access (Tailscale):** Native systemd agent on `docker-host` (`100.89.249.96`, node `docker-host.taila813af.ts.net`, tailnet `srytmj.github`).
- **Public Access (Cloudflare Tunnel):** Native systemd `cloudflared` service on `docker-host` securely exposing public services (`suryatmaja.dev`, `dash.suryatmaja.dev`, `drive.suryatmaja.dev`, `t3.suryatmaja.dev`, `komga.suryatmaja.dev`, etc.) without opening router ports.

## Storage Path Convention & Live Capacity

| Data type | Location | Filesystem & Disk | Live Usage (2026-09-14) |
|---|---|---|---|
| OS, Proxmox, Docker engine | OS SSD (`/`) | ext4, `MidasForce SSD 256GB` (sda) | 43G / 147G (31%) on docker-host |
| Project code + repositories | OS SSD (`/mnt/homelab_projects/`) | ext4, OS SSD (sda) | Included in `/` |
| Database metadata (Postgres/Redis) | OS SSD (named volumes) | ext4, OS SSD (sda) | Included in `/` |
| Music library (Navidrome & Jellyfin) | HDD-Music (`/mnt/hdd-music/`) | ext4, `WD Green 2TB` (sdc1) | 717G / 1.8T (42%) |
| Movies, TV, Anime, Manga, Torrents | HDD-Media (`/mnt/hdd-media/`) | ext4, `Toshiba 1TB` (sdb2) | 492G / 916G (57%) |
| Nextcloud, Syncthing, LAN Shared | HDD-Cloud (`/mnt/hdd-cloud/`) | ext4, `Barracuda 1TB` (sdd2) | 105G / 916G (13%) |

## Storage Drives — Physical Inventory

| Drive Role | Hardware Model | Form Factor & Capacity | Serial Number | Mount Point | Status |
|---|---|---|---|---|---|
| **OS SSD** | MidasForce SSD 256GB (via SATA-to-M.2 adapter) | M.2 SATA in 2.5\" Bay (256GB) | `RE202410151200000921` | `/` (sda) | **Active.** Boot, PVE LVM-thin pool, LXC root disks. |
| **HDD-Music** | Western Digital Green (`WD20EZRX-00DC0B0`) | 3.5\" SATA III (2TB) | `WD-WCC1T0899623` | `/mnt/hdd-music` (sdc1) | **Active.** 717GB music collection + local backup staging. |
| **HDD-Media** | Toshiba 2.5\" HDD (`MQ04ABF100`) | 2.5\" SATA III (1TB) | `Y9CSTR0WT` | `/mnt/hdd-media` (sdb2) | **Active.** Movies, Anime, Manga raw/reader, qBittorrent. |
| **HDD-Cloud** | Seagate Barracuda (`ST1000DM010-2EP102`) | 3.5\" SATA III (1TB) | `W9AS0LSD` | `/mnt/hdd-cloud` (sdd2) | **Active.** Nextcloud, Syncthing, LAN Shared folder. |
| **HDD-Backup** | Western Digital Blue | 3.5\" SATA (320GB) | - | `/mnt/hdd-backup` | **Pending.** Standby for 4th external dock solution. |

### Directory Hierarchy

#### HDD-Music (`/mnt/hdd-music/`)
```
/mnt/hdd-music/
├── music/                 # 717GB clean music collection scanned by Navidrome
├── jellyfin/
│   └── music/         # Legacy Jellyfin music mount
└── backups/              # Local backup target for PostgreSQL dumps & configs
```

#### HDD-Media (`/mnt/hdd-media/`)
```
/mnt/hdd-media/
├── jellyfin/
│   ├── movies/
│   ├── tv/
│   └── anime/         # Video anime (StreamVault & Jellyfin direct-play)
├── manga-raw/            # Master raw CBZ collection (Samba \\docker-host\manga)
├── manga-reader/         # Optimized WebP library (auto-mirrored by manga-optimizer, served by Komga)
└── qbittorrent/
    └── downloads/        # Active and completed torrent downloads
```

#### HDD-Cloud (`/mnt/hdd-cloud/`)
```
/mnt/hdd-cloud/
├── nextcloud/            # Nextcloud primary storage root
├── syncthing/            # P2P multi-device sync
└── shared/               # LAN drop, accessible via SMB \\docker-host\shared
```

## Windows Network Access (SMB/Samba & WSDD)

- **Active Daemons:** `smbd` and `wsdd` systemd services running on `docker-host`.
- **Samba Shares (`/etc/samba/smb.conf`):**
  - `shared` → `/mnt/hdd-cloud/shared` (Read/Write, LAN drop)
  - `manga` → `/mnt/hdd-media/manga-raw` (Read/Write, ingest for manga optimizer)
  - `media` → `/mnt/hdd-media` (Movies, TV, Anime)
  - `music` → `/mnt/hdd-music` (Music collection)
- **WSDD (Web Services Dynamic Discovery):** Allows the homelab server to appear automatically under Windows Explorer "Network" without manual IP typing.
