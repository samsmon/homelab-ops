   - Role: Dedicated music streaming library (`jellyfin/music` scanned by Navidrome & Jellyfin) + local backup staging destination (`backups/`).
3. **HDD-Media (1TB 3.5\" Seagate Barracuda 7200 RPM via LM 418 SATA Port)**:
   - Drive: `ST1000DM010-2EP102`, serial `W9AS0LSD` (`/dev/sdd2`, label `hdd-media`, 916GB usable).
   - Role: High-throughput media storage — Videos (`videos/{anime,movies,tv}`), raw manga master (`manga-raw`), auto-optimized reader library (`manga-reader` for Komga), and torrent downloads (`qbittorrent`).
   - *Note on disk allocation:* The physical 3.5" 7200 RPM Seagate Barracuda drive is dedicated to `hdd-media` (`sdd2`) for high-IOPS random seek performance, while the 2.5" 5400 RPM Toshiba drive is dedicated to `hdd-cloud` (`sdb2`).
4. **HDD-Cloud (1TB 2.5\" Toshiba HDD 5400 RPM via LM 418 SATA Port)**:
   - Drive: `TOSHIBA MQ04ABF100`, serial `Y9CSTR0WT` (`/dev/sdb2`, label `hdd-cloud`, 916GB usable).
   - Role: Nextcloud data directory, Syncthing continuous device sync, and general LAN shared drop (`shared/`). Quiet and low-power operation.

- **Power for the external HDD dock:** Separate **Enhance ENP-2320 PSU** (Flex ATX, 200W, Active PFC), not the M710q's internal 65W/90W adapter. Two independent power domains prevent power starvation and voltage-spike risks to the HDDs. Uses a 24-pin ATX jumper (shorts PS_ON to Ground) to power on without a motherboard, plus Molex-to-SATA power cables per drive and cooling fans.
- **Cable routing:** Case backplate is open to route SATA data cables from the LM 418 out to the external drive dock. The backplate opening over the RAM is covered with a magnetic dust mesh panel.

## Virtualization Layer

```
Proxmox VE 9.2.2 (bare metal hypervisor, kernel 7.0.2-6-pve) — pve.suryatmaja.dev, 192.168.18.224
  ├── LXC 100: "docker-host" (Ubuntu Server 24.04 LTS) — 192.168.18.225
  │     RAM allocated: 12GB (of 32GB total)
  │     CPU allocated: 4 cores (of 4 total on i5-7500)
  │     Storage: 150GB (local-lvm thin pool: vm-100-disk-0)
  │     Proxmox container features "nesting=1,keyctl=1" enabled
  │     Hardware Pass-through: /dev/dri/card0, /dev/dri/renderD128 (Intel HD 630 iGPU)
  │     Bind Mounts: /mnt/hdd-media, /mnt/hdd-cloud, /mnt/hdd-music
  │     Docker Engine 29.8.0 + Compose plugin v5.5.1 + Tailscale + cloudflared
  │     Purpose: Core infrastructure, homelab cockpit, media stack, DB, tools, portfolio
  └── LXC 101: "apps-host" (Ubuntu Server 24.04 LTS) — 192.168.18.226
        RAM allocated: 4GB (of 32GB total)
        CPU allocated: 2 cores
        Storage: 30GB (local-lvm thin pool: vm-101-disk-0)
        Proxmox container features "nesting=1,keyctl=1" + TUN passthrough (/dev/net/tun)
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

| Data type | Location | Filesystem & Disk | Live Usage (2026-09-15) |
|---|---|---|---|
| OS, Proxmox, Docker engine | OS SSD (`/`) | ext4, `MidasForce SSD 256GB` (sda) | 43G / 147G (31%) on docker-host |
| Project code + repositories | OS SSD (`/mnt/homelab_projects/`) | ext4, OS SSD (sda) | Included in `/` |
| Database metadata (Postgres/Redis) | OS SSD (named volumes) | ext4, OS SSD (sda) | Included in `/` |
| Music library (Navidrome & Jellyfin) | HDD-Music (`/mnt/hdd-music/`) | ext4, `WD Green 2TB` (sdc1) | 717G / 1.8T (42%) |
| Movies, TV, Anime, Manga, Torrents | HDD-Media (`/mnt/hdd-media/`) | ext4, `Seagate Barracuda 1TB 7200 RPM` (sdd2) | 510G / 916G (59%) |
| Nextcloud, Syncthing, LAN Shared | HDD-Cloud (`/mnt/hdd-cloud/`) | ext4, `Toshiba 1TB 2.5"` (sdb2) | 105G / 916G (13%) |

## Storage Drives — Physical Inventory

| Drive Role | Hardware Model | Form Factor & Capacity | Serial Number | Mount Point | Status |
|---|---|---|---|---|---|
| **OS SSD** | MidasForce SSD 256GB (via SATA-to-M.2 adapter) | M.2 SATA in 2.5" Bay (256GB) | `RE202410151200000921` | `/` (sda) | **Active.** Boot, PVE LVM-thin pool, LXC root disks. |
| **HDD-Music** | Western Digital Green (`WD20EZRX-00DC0B0`) | 3.5" SATA III (2TB) | `WD-WCC1T0899623` | `/mnt/hdd-music` (sdc1) | **Active.** 717GB music collection + local backup staging. |
| **HDD-Media** | Seagate Barracuda (`ST1000DM010-2EP102`) | 3.5" SATA III 7200 RPM (1TB) | `W9AS0LSD` | `/mnt/hdd-media` (sdd2) | **Active.** High-throughput Media: `videos/`, `manga-raw`, `manga-reader`, `qbittorrent`. |
| **HDD-Cloud** | Toshiba 2.5" HDD (`MQ04ABF100`) | 2.5" SATA III 5400 RPM (1TB) | `Y9CSTR0WT` | `/mnt/hdd-cloud` (sdb2) | **Active.** Quiet/low-power: Nextcloud, Syncthing, LAN Shared folder. |
| **HDD-Backup** | Western Digital Blue | 3.5" SATA (320GB) | - | `/mnt/hdd-backup` | **Pending.** Standby for 4th external dock solution. |

### Directory Hierarchy

#### HDD-Media (`/mnt/hdd-media/`)
```
/mnt/hdd-media/
├── videos/                 # Service-agnostic media root (Jellyfin, StreamVault)
│   ├── anime/              # Anime series & movies
│   ├── movies/             # General movies
│   └── tv/                 # TV Shows
├── manga-raw/              # Raw manga master archive
├── manga-reader/           # Optimized WebP manga library (scanned by Komga)
└── qbittorrent/            # Staging download torrents
```

#### HDD-Music (`/mnt/hdd-music/`)
```
/mnt/hdd-music/
├── music/                 # 717GB clean music collection scanned by Navidrome
├── jellyfin/
│   └── music/         # Legacy Jellyfin music mount
```