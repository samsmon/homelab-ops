# Architecture - Current State

> This file reflects what EXISTS right now. Update it whenever the actual topology changes.
> Last verified: 2026-09-18 (via live SSH verification of docker-host)

## Hardware

- **Device:** Lenovo ThinkCentre M710q Tiny (product no. `10MQS1EU00`, confirmed via `dmidecode`)
- **CPU:** Intel Core i5-7500 (7th Gen Kaby Lake), 4 cores / 4 threads, 3.40 GHz base (up to 3.80 GHz max turbo), 65W TDP. Confirmed via `lscpu`.
- **Integrated GPU (iGPU):** Intel HD Graphics 630 (`[8086:5912]`), kernel driver `i915`. Direct Rendering Infrastructure (DRI) passed through to `docker-host` via `/dev/dri/card0` and `/dev/dri/renderD128` for hardware-accelerated transcoding.
- **RAM:** 32GB DDR4 (recognized as 31GiB in Proxmox / `free -h`).
- **Ethernet (NIC):** Intel I219-V Gigabit Ethernet (`[8086:15b8]`), kernel driver `e1000e`.
- **M.2 Slot (PCIe/NVMe M-Key) -> LM 418 Expansion Card:**
  - The internal M.2 NVMe slot is populated with an **LM 418 M.2 NVMe NGFF M Key TO 5 Ports SATA III 3.0 Card + Heatsink Chipset Taiwan J-Micron JMB585** (`01:00.0 SATA controller: JMicron Technology Corp. JMB58x AHCI SATA controller [197b:0585]`).
  - This card breaks out PCIe bandwidth into 5 native SATA III (6Gbps) ports, dedicated to running external HDDs without relying on unreliable USB enclosures.
- **Internal 2.5" SATA Bay -> M.2 SATA Adapter -> OS SSD:**
  - The native internal 2.5" SATA bay is fitted with a **SATA to M.2 SATA NGFF B + M KEY Converter Adapter Card (SATA III 6Gbps)**.
  - Houses an internal **256GB M.2 SATA SSD** (`MidasForce SSD 256GB`, serial `RE202410151200000921`, partition `/dev/sda`).
  - Contains Proxmox VE rootfs (`pve-root`), swap (`pve-swap` 8GB), and `pve-data` LVM-thin pool (`vm-100-disk-0` 150GB, `vm-101-disk-0` 30GB, `vm-102-disk-0` 40GB).

## Storage Topology (FINAL)

This device's 2 physical drive slots (1x M.2, 1x internal 2.5" bay) are used unconventionally to host 4 storage drives (1 SSD + 3 HDDs) without an external USB DAS enclosure:

1. **Internal OS SSD (256GB M.2 SATA SSD via 2.5" Bay Adapter)**:
   - Drive: `MidasForce SSD 256GB` (`/dev/sda`).
   - Role: Proxmox VE host OS, swap, VM/LXC virtual disks, and database metadata.
2. **HDD-Music (2TB 3.5" Western Digital Green via LM 418 SATA Port)**:
   - Drive: `WDC WD20EZRX-00DC0B0`, serial `WD-WCC1T0899623` (`/dev/sdc1`, 1.8TB usable).
   - Role: Dedicated music streaming library (`jellyfin/music` scanned by Navidrome & Jellyfin) + local backup staging destination (`backups/`).
3. **HDD-Media (1TB 3.5" Seagate Barracuda 7200 RPM via LM 418 SATA Port)**:
   - Drive: `ST1000DM010-2EP102`, serial `W9AS0LSD` (`/dev/sdd2`, label `hdd-media`, 916GB usable).
   - Role: High-throughput media storage — Videos (`videos/{anime,movies,tv}`), raw manga master (`manga-raw`), auto-optimized reader library (`manga-reader` for Komga), and torrent downloads (`qbittorrent`).
   - *Note on disk allocation:* The physical 3.5" 7200 RPM Seagate Barracuda drive is dedicated to `hdd-media` (`sdd2`) for high-IOPS random seek performance, while the 2.5" 5400 RPM Toshiba drive is dedicated to `hdd-cloud` (`sdb2`).
4. **HDD-Cloud (1TB 2.5" Toshiba HDD 5400 RPM via LM 418 SATA Port)**:
   - Drive: `TOSHIBA MQ04ABF100`, serial `Y9CSTR0WT` (`/dev/sdb2`, label `hdd-cloud`, 916GB usable).
   - Role: Nextcloud data directory, Syncthing continuous device sync, and general LAN shared drop (`shared/`). Quiet and low-power operation.

- **Power for the external HDD dock:** Separate **Enhance ENP-2320 PSU** (Flex ATX, 200W, Active PFC), not the M710q's internal 65W/90W adapter. Two independent power domains prevent power starvation and voltage-spike risks to the HDDs. Uses a 24-pin ATX jumper (shorts PS_ON to Ground) to power on without a motherboard, plus Molex-to-SATA power cables per drive and cooling fans.
- **Cable routing:** Case backplate is open to route SATA data cables from the LM 418 out to the external drive dock. The backplate opening over the RAM is covered with a magnetic dust mesh panel.

## Virtualization Layer

```
Proxmox VE 9.2.2 (bare metal hypervisor, kernel 7.0.2-6-pve) — pve.suryatmaja.dev, 192.168.18.224, Tailscale 100.108.61.124
  ├── LXC 100: "docker-host" (Ubuntu Server 24.04 LTS) — 192.168.18.225
  │     RAM allocated: 12GB (of 32GB total)
  │     CPU allocated: 4 cores (of 4 total on i5-7500)
  │     Storage: 150GB (local-lvm thin pool: vm-100-disk-0)
  │     Proxmox container features "nesting=1,keyctl=1" enabled
  │     Hardware Pass-through: /dev/dri/card0, /dev/dri/renderD128 (Intel HD 630 iGPU)
  │     Bind Mounts: /mnt/hdd-media, /mnt/hdd-cloud, /mnt/hdd-music
  │     Docker Engine 29.8.0 + Compose plugin v5.5.1 + Tailscale + cloudflared
  │     Purpose: Core infrastructure, homelab cockpit, media stack, DB, tools, portfolio
  └── LXC 101: "yado-hosts" (renamed 2026-09-18, was "whitearchive-hosts") (Ubuntu Server 24.04 LTS) — 192.168.18.226
        RAM allocated: 4GB (of 32GB total)
        CPU allocated: 2 cores
        Storage: 30GB (local-lvm thin pool: vm-101-disk-0)
        Proxmox container features "nesting=1,keyctl=1" + TUN passthrough (/dev/net/tun)
        Docker Engine 29.8.0 + Compose plugin v5.5.1
        Purpose: Dedicated environment for personal web projects (yado, malas, sso-yado, pore-js, etc.)
  └── LXC 102: "dev-host" (Ubuntu Server 24.04 LTS) — 192.168.18.227
        RAM allocated: 12GB (of 32GB total)
        CPU allocated: 4 cores
        Storage: 40GB (local-lvm thin pool: vm-102-disk-0)
        Proxmox container features "nesting=1,keyctl=1"
        Docker Engine 29.8.0 + Compose plugin v5.5.1
        Purpose: Dedicated isolated environment for T3 Code (agent coding harness) — created
        2026-09-15 to stop T3 Code's I/O/CPU load from ever affecting the media stack /
        core services on docker-host again (see CHANGELOG for the incident that prompted this).
        /workspace mounted via a host-level CIFS mount bound into the container (mp1) — NOT a
        direct in-container network mount, because unprivileged LXC cannot reliably do kernel
        NFS/CIFS mounts itself. The actual project files still live on docker-host
        (`/mnt/homelab_projects`), shared out via a dedicated Samba share (`[projects]`,
        restricted to `192.168.18.224` and `.227` by `hosts allow`) — the Proxmox host mounts
        that share at `/mnt/homelab_projects_smb` and bind-mounts it into LXC 102.
  └── LXC 103: "personal-hosts" (renamed 2026-09-21, was "shared-hosts") (Ubuntu Server 24.04 LTS) — 192.168.18.228, Tailscale 100.88.119.26
        RAM allocated: 4GB (of 32GB total)
        CPU allocated: 2 cores
        Storage: 15GB (local-lvm thin pool: vm-103-disk-0, resized 10G->15G on 2026-09-21)
        Proxmox container features "nesting=1,keyctl=1" + TUN passthrough (/dev/net/tun)
        Bind Mounts: /mnt/hdd-media (mp0), /mnt/hdd-music (mp1, currently a dead mount — see hdd-music's
        entry in the storage table; `nhdl` no longer depends on it since its DOWNLOAD_DIR moved to hdd-media)
        Docker Engine (official docker-ce, download.docker.com repo) + Compose plugin + Tailscale
        Purpose: Renamed 2026-09-21 from a friends'-projects-only host into a combined **personal +
        friends' projects** host, after the 2026-09-20 "split docker-host into media/personal/drive/infra"
        plan turned out infeasible at full scope (see CHANGELOG (62) — `local-lvm` thin pool only had
        ~18GB real headroom, not enough for 4 new LXCs). User's own call: merge personal misc projects into
        this LXC rather than create a 5th one, accepting the reduced trust-boundary isolation from friends'
        code as a worthwhile tradeoff for the storage/resource savings.
        Tenants: `situlah` (samsmon/situlah, friend's project — unchanged, see below), `nhdl` (migrated
        2026-09-21 from `docker-host`, port 8098, no NPM proxy host — LAN/Tailscale IP:port access only),
        `group-checklist` (migrated 2026-09-21 from `docker-host`, port 3001, NPM proxy host
        `checklist.suryatmaja.dev` updated to point here — **now runs its own bundled Postgres**
        (`group-checklist-db` container + named volume) instead of the cross-LXC `shared-postgres` on
        `docker-host`, deliberately isolated rather than exposing `shared-postgres` across LXC boundaries).
        `portofolio` migration deferred — locked by a concurrent session doing its Yado rename as of
        2026-09-21, see `CURRENT_OPS.md`. `reclip` and `headless-browser` were **not** migrated — user had
        them deleted outright (container, image, and `/opt/projects/{reclip,headless-browser}` removed from
        `docker-host`); `headless-browser` also had a stale `tailscale serve` config on `docker-host`
        proxying to it (port 3010) left over from before the 2026-09-13 "tailscale serve dropped" decision
        — this was still actively bound to port 443 and caused an `nginx-proxy-manager` outage (all 15
        proxy hosts down) when NPM was restarted for an unrelated reason during this same session; fixed
        with `tailscale serve reset` + a full NPM container recreate. No further `tailscale serve` configs
        should exist anywhere in this infra per that standing decision — if one is found again, remove it.
        **Storage warning (from original 2026-09-21 creation, still relevant):** `local-lvm` thin pool on
        `pve` was already at 85.89% actual usage when this LXC was first created — `pct create` was refused
        by LVM's `thin_pool_autoextend_threshold` safety check (VG has 0 free PE, so autoextend is
        impossible either way). Worked around by raising `thin_pool_autoextend_threshold` from 80 to 95 in
        `/etc/lvm/lvm.conf` on `pve` (backed up as `lvm.conf.bak-<date>`) — this only raises the
        warning/block threshold, it does NOT add physical capacity. The thin pool is now genuinely
        overcommitted (sum of all LXC disk sizes exceeds pool size) — **next storage cleanup pass should
        address this properly** (see roadmap.md). As of this LXC's resize to 15GB, thin pool headroom is
        down to roughly ~13GB — do not add more LXCs or grow existing ones without addressing this first.
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
              ├── LXC 101 yado-hosts: 192.168.18.226
              ├── LXC 102 dev-host: 192.168.18.227
              └── LXC 103 shared-hosts: 192.168.18.228
```

- **Switch:** **Mercusys MS105G (5-Port Gigabit Desktop Switch)** connects the ISP router, Main PC, and Homelab node, ensuring full 1000 Mbps line-rate file transfers between Main PC and Samba/media shares.
- **Static IPs**:
  - Proxmox VE: `192.168.18.224/24`, gateway `192.168.18.1`
  - docker-host (LXC 100): `192.168.18.225/24`, gateway `192.168.18.1`
  - yado-hosts (LXC 101): `192.168.18.226/24`, gateway `192.168.18.1`
  - dev-host (LXC 102): `192.168.18.227/24`, gateway `192.168.18.1`
  - shared-hosts (LXC 103): `192.168.18.228/24`, gateway `192.168.18.1`
- **DNS:** `192.168.18.225` (AdGuard Home on docker-host) primary for LAN, `1.1.1.1` upstream fallback. Host `systemd-resolved` stub disabled to free port 53.
- **Remote Access (Tailscale):** Native systemd agent on Proxmox VE host (`100.108.61.124`, node `pve`), `docker-host` (`100.89.249.96`, node `docker-host.taila813af.ts.net`), and **`yado-hosts`** (LXC 101, `100.110.235.57`) — confirmed 2026-09-18 that the Tailscale node named `apps-host` in the admin console is actually this same machine, originally `hostname` = `whitearchive-hosts`, renamed again the same day to `yado-hosts` (see CHANGELOG/decisions.md for the "Yado" rebrand) — the Tailscale node name itself is still `apps-host` (an even older label from before either rename; Tailscale doesn't auto-follow OS hostname changes, so this would need to be renamed manually in the admin console if desired). Use `100.110.235.57` to reach anything on `yado-hosts` over Tailscale (e.g. `malas` on `:8082`, `sso-yado` on `:8081`, `pore-js` demo on `:8083`, `yado` on `:3000`) without needing DNS or the `.my.id` domain to be purchased/configured yet. **`dev-host` (LXC 102) is not yet joined to the tailnet** — pending a Tailscale auth key from the user (not something an agent can self-generate, needs the Tailscale admin console). Until then, `dev-host` is only reachable via LAN IP (`192.168.18.227`). **`shared-hosts`** (LXC 103, `100.88.119.26`) joined the tailnet 2026-09-21, node name `shared-hosts`.
- **Public Access (Cloudflare Tunnel):** Native systemd `cloudflared` service on `docker-host` securely exposing public services (`suryatmaja.dev`, `dash.suryatmaja.dev`, `drive.suryatmaja.dev`, `t3.suryatmaja.dev`, `komga.suryatmaja.dev`, etc.) without opening router ports. Public hostname routing is managed in the Cloudflare Zero Trust dashboard, not a local config file. **`t3.suryatmaja.dev`'s route still points at the old `192.168.18.225:9001` (docker-host) and needs to be manually repointed to `192.168.18.227:9001` (dev-host)** after the 2026-09-15 t3code migration — see CHANGELOG.

## Storage Path Convention & Live Capacity

| Data type | Location | Filesystem & Disk | Live Usage (2026-09-18) |
|---|---|---|---|
| OS, Proxmox, Docker engine | OS SSD (`/`) | ext4, `MidasForce SSD 256GB` (sda) | 50G / 147G (36%) on docker-host |
| Project code + repositories | OS SSD (`/mnt/homelab_projects/`) | ext4, OS SSD (sda) | Included in `/` |
| Database metadata (Postgres/Redis) | OS SSD (named volumes) | ext4, OS SSD (sda) | Included in `/` |
| Music library (Navidrome & Jellyfin) | HDD-Music (`/mnt/hdd-music/`) | ext4, `WD Green 2TB` (sdc1) | 717G / 1.8T (42%) |
| Movies, TV, Anime, Manga, Torrents, JDownloader | HDD-Media (`/mnt/hdd-media/`) | ext4, `Seagate Barracuda 1TB 7200 RPM` (sdd2) | 627G / 916G (73%) |
| Nextcloud, Syncthing, LAN Shared | HDD-Cloud (`/mnt/hdd-cloud/`) | ext4, `Toshiba 1TB 2.5"` (sdb2) | 105G / 916G (13%) |

## Storage Drives — Physical Inventory

| Drive Role | Hardware Model | Form Factor & Capacity | Serial Number | Mount Point | Status |
|---|---|---|---|---|---|
| **OS SSD** | MidasForce SSD 256GB (via SATA-to-M.2 adapter) | M.2 SATA in 2.5" Bay (256GB) | `RE202410151200000921` | `/` (sda) | **Active.** Boot, PVE LVM-thin pool, LXC root disks. |
| **HDD-Music** | Western Digital Green (`WD20EZRX-00DC0B0`) | 3.5" SATA III (2TB) | `WD-WCC1T0899623` | `/mnt/hdd-music` (device letter now floats — currently `sdd1`, was `sdc1`; identify by serial, not letter) | **⚠️ OFFLINE — likely drive-side (controller) failure, not cable.** 2026-09-19: first scare, `CHANGELOG.md` (40)/(42) blamed a degrading SATA data cable (SMART `PASSED`, clean CRC counters post-swap), declared safe. 2026-09-20 (55): dropped again under a light read-only workload (SMB scan + playback), reopening that verdict. 2026-09-20 (56): user physically reseated SATA data+power cables (confirmed good) and live-rescanned — `ata9` link now comes up clean and repeatedly (6.0 Gbps, no more link-down cycling), but `ata9.00: failed to IDENTIFY (INIT_DEV_PARAMS failed, err_mask=0x80)` still fails every time. Link/electrical layer is confirmed fine now; the ATA protocol handshake itself fails — points to the drive's own controller board, not the cable. **Treat as a failing drive for warranty/RMA purposes.** Still not enumerating in `lsblk`. 717GB music collection intact as of last mount, but currently inaccessible. |
| **HDD-Media** | Seagate Barracuda (`ST1000DM010-2EP102`) | 3.5" SATA III 7200 RPM (1TB) | `W9AS0LSD` | `/mnt/hdd-media` (sdd2) | **Active.** High-throughput Media: `videos/`, `manga-raw`, `manga-reader`, `qbittorrent`. |
| **HDD-Cloud** | Toshiba 2.5" HDD (`MQ04ABF100`) | 2.5" SATA III 5400 RPM (1TB) | `Y9CSTR0WT` | `/mnt/hdd-cloud` (sdb2) | **Active.** Quiet/low-power: Nextcloud, Syncthing, LAN Shared folder. |
| **HDD-Backup** | Western Digital Blue | 3.5" SATA (320GB) | - | `/mnt/hdd-backup` | **Pending.** Standby for 4th external dock solution. |

### Directory Hierarchy

#### HDD-Media (`/mnt/hdd-media/`)
```
/mnt/hdd-media/
├── videos/                 # Service-agnostic media root (Jellyfin)
│   ├── anime/              # Anime series & movies
│   ├── movies/             # General movies
│   └── tv/                 # TV Shows
├── manga-raw/              # Raw manga master archive
├── manga-reader/           # Optimized WebP manga library (scanned by Komga)
├── qbittorrent/            # Staging download torrents
└── jdownloader/            # JDownloader2 config + downloads
```

#### HDD-Music (`/mnt/hdd-music/`)
```
/mnt/hdd-music/
├── music/                 # 717GB clean music collection scanned by Navidrome
├── jellyfin/
│   └── music/         # Legacy Jellyfin music mount
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
  - `projects` → `/mnt/homelab_projects` (Read/Write, restricted to PVE and dev-host for T3 Code /workspace)
- **WSDD (Web Services Dynamic Discovery):** Allows the homelab server to appear automatically under Windows Explorer "Network" without manual IP typing.