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
2. **HDD-Backup (2TB 3.5" Western Digital Green via LM 418 SATA Port)** — renamed 2026-09-21, was `HDD-Music`:
   - Drive: `WDC WD20EZRX-00DC0B0`, serial `WD-WCC1T0899623` (device letter floats, currently detached — see status row below).
   - Role (intended, not currently reliable): cold-backup target. **⚠️ Failed a sequential-write test on 2026-09-21 and dropped from the kernel** — its safety even for this role is now in question. See the drive-status table below before trusting it with anything.
   - Mounted at `/mnt/hdd-backup` when up.
3. **HDD-Media (1TB 3.5" Seagate Barracuda 7200 RPM via LM 418 SATA Port)**:
   - Drive: `ST1000DM010-2EP102`, serial `W9AS0LSD` (`/dev/sdd2`, label `hdd-media`, 916GB usable).
   - Role: High-throughput media storage — Videos (`videos/{anime,movies,tv}`), raw manga master (`manga-raw`), auto-optimized reader library (`manga-reader` for Komga), torrent downloads (`qbittorrent`), **plus Nextcloud + Syncthing data + misc personal folders** (absorbed from the old `hdd-cloud` on 2026-09-21).
4. **HDD-Music (1TB 2.5" Toshiba HDD 5400 RPM via LM 418 SATA Port)** — renamed 2026-09-21, was `HDD-Cloud`:
   - Drive: `TOSHIBA MQ04ABF100`, serial `Y9CSTR0WT` (`/dev/sdb2`, 916GB usable).
   - Role: **Pure music library only** (`music/`, scanned by Navidrome & Jellyfin). Nextcloud/Syncthing/LAN-drop data that used to live here moved to `hdd-media`. Mounted at `/mnt/hdd-music`.

- **Power for the external HDD dock:** Separate **Enhance ENP-2320 PSU** (Flex ATX, 200W, Active PFC), not the M710q's internal 65W/90W adapter. Two independent power domains prevent power starvation and voltage-spike risks to the HDDs. Uses a 24-pin ATX jumper (shorts PS_ON to Ground) to power on without a motherboard, plus Molex-to-SATA power cables per drive and cooling fans.
- **Cable routing:** Case backplate is open to route SATA data cables from the LM 418 out to the external drive dock. The backplate opening over the RAM is covered with a magnetic dust mesh panel.

## Virtualization Layer

```
Proxmox VE 9.2.2 (bare metal hypervisor, kernel 7.0.2-6-pve) — pve.suryatmaja.dev, 192.168.18.224, Tailscale 100.108.61.124
  ├── LXC 100: "docker-host" (Ubuntu Server 24.04 LTS) — 192.168.18.225
  │     RAM allocated: 8GB (of 32GB total, adjusted 2026-09-22 for Postgres/Redis tuning)
  │     CPU allocated: 4 cores (of 4 total on i5-7500)
  │     Storage: 150GB (local-lvm thin pool: vm-100-disk-0)
  │     Proxmox container features "nesting=1,keyctl=1" enabled
  │     Hardware Pass-through: /dev/dri/card0, /dev/dri/renderD128 (Intel HD 630 iGPU)
  │     Bind Mounts: /mnt/hdd-media, /mnt/hdd-music, /mnt/hdd-backup (renamed 2026-09-21, was hdd-cloud/hdd-music)
  │     Docker Engine 29.8.0 + Compose plugin v5.5.1 + Tailscale + cloudflared
  │     Purpose: Core infrastructure, homelab cockpit, media stack, DB, tools, portfolio
  └── LXC 101: "yado-hosts" (renamed 2026-09-18, was "whitearchive-hosts") (Ubuntu Server 24.04 LTS) — 192.168.18.226
        RAM allocated: 4GB (of 32GB total)
        CPU allocated: 2 cores
        Storage: 30GB (local-lvm thin pool: vm-101-disk-0)
        Proxmox container features "nesting=1,keyctl=1" + TUN passthrough (/dev/net/tun)
        Docker Engine 29.8.0 + Compose plugin v5.5.1
        Purpose: Dedicated environment for personal web projects (yado, malas, sso-yado, pore-js, etc.)
  └── LXC 102: "dev-host" (Ubuntu Server 24.04 LTS) — 192.168.18.227, Tailscale 100.73.165.64
        RAM allocated: 6GB (of 32GB total, adjusted 2026-09-22 from 12GB to rebalance into media-hosts)
        CPU allocated: 4 cores
        Storage: 40GB (local-lvm thin pool: vm-102-disk-0)
        Proxmox container features "nesting=1,keyctl=1" + TUN passthrough (/dev/net/tun, added 2026-09-21)
        Docker Engine 29.8.0 + Compose plugin v5.5.1 + Tailscale (joined 2026-09-21)
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
        Bind Mounts: /mnt/hdd-media (mp0), /mnt/hdd-music (mp1 — healthy again as of 2026-09-21's rename,
        this is the former hdd-cloud/Toshiba drive, pure music now; `nhdl` doesn't depend on its content
        since its DOWNLOAD_DIR moved to hdd-media, mount just happens to be named the same)
        Docker Engine (official docker-ce, download.docker.com repo) + Compose plugin + Tailscale.
        **Docker API exposed on `tcp://0.0.0.0:2375`** (no TLS/auth, LAN-only — added 2026-09-21 for
        `homelab-cockpit` monitoring, same pattern as `yado-hosts`/`dev-host`, user confirmed).
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
        `portfolio` (migrated 2026-09-21, after confirming a stale lock in `CURRENT_OPS.md` from an
        earlier session's Yado rename work was actually done — clean git tree, no in-progress
        cherry-pick/merge — before proceeding; port 3080, NPM's `port.suryatmaja.dev` proxy host
        `forward_host` updated to point here, dropped the `shared_net` external-network dependency since
        it doesn't exist on this LXC and wasn't actually needed). `reclip` and `headless-browser` were **not** migrated — user had
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
        **Update 2026-09-21 (later same day): this headroom concern is stale** — `pct fstrim` across all
        LXCs recovered thin-pool usage from 88.80% to 55.24% (~70GB real headroom), see `CHANGELOG.md` (66).
        This is what unblocked creating LXC 104 below.
  └── LXC 104: "media-hosts" (Ubuntu Server 24.04 LTS) — 192.168.18.229, Tailscale 100.113.250.97
        RAM allocated: 12GB (of 32GB total, boosted 2026-09-22 with 8GB tmpfs for Jellyfin transcoding)
        CPU allocated: 2 cores
        Storage: 30GB (local-lvm thin pool: vm-104-disk-0)
        Proxmox container features "nesting=1,keyctl=1" + TUN passthrough (/dev/net/tun, added 2026-09-21)
        Bind Mounts: /mnt/hdd-media (mp0), /mnt/hdd-music (mp2, pure music, renamed 2026-09-21 from hdd-cloud), /mnt/hdd-backup (mp3, renamed 2026-09-21 from hdd-music, unstable)
        Docker Engine (official docker-ce) + Compose plugin, own `shared_net` bridge network (separate
        Docker network namespace from `docker-host`'s `shared_net` — same name, different network, since
        Docker networks don't span LXCs). **Docker API exposed on `tcp://0.0.0.0:2375`** (no TLS/auth,
        LAN-only — same pattern as `yado-hosts`/`dev-host`, added 2026-09-21 so `homelab-cockpit` can
        monitor it, user explicitly confirmed accepting this risk). Tailscale installed and joined
        2026-09-21 (`100.113.250.97`) — reachable via LAN IP or Tailscale.
        Purpose: Created 2026-09-21 as part of finally executing the full-scope version of the
        2026-09-20 "split docker-host into media/personal/drive/infra" plan (see `docs/decisions.md`),
        once (66)'s `fstrim` fix reopened enough storage headroom. Hosts the entire media stack, migrated
        from `docker-host` in one session: `qbittorrent` (port 8480, NPM `qb.suryatmaja.dev` updated),
        `prowlarr`/`sonarr`/`radarr` (arr-stack, ports 9696/8989/7878, no NPM proxy hosts, no download
        client was ever configured in Sonarr/Radarr so nothing needed updating there), `jellyfin` (port
        8096, NPM `jellyfin.suryatmaja.dev` updated, `ServerId` confirmed unchanged post-migration —
        config genuinely preserved, not a fresh install), `navidrome` + `feishin` (ports 4533/9180,
        Feishin's `SERVER_URL` changed from a hardcoded IP to `http://navidrome:4533` — container-name
        DNS resolution, since both now live on the same LXC's `shared_net`; Navidrome's 17,619-track
        index confirmed intact post-migration), `komga` (port 25600, NPM `komga.suryatmaja.dev` updated),
        `jdownloader2` (port 5800, config/downloads bind-mounted straight to `hdd-media`, no volume to
        migrate). All config/data volumes migrated via `docker run --rm -v <vol>:/from -v /tmp:/to alpine
        tar czf ...` → `scp` → `pct push` → import (same pattern proven on `personal-hosts`). Verified
        every service live post-migration (HTTP checks, and for Jellyfin/Navidrome specifically confirmed
        actual persisted data survived, not just that a container started) before stopping/removing the
        old instance on `docker-host` each time. All 15 NPM-proxied domains re-verified working after the
        full migration. **`docker-host` (LXC 100) is now infra + `nextcloud`/`syncthing` permanently** —
        user explicitly decided 2026-09-21 against a `drive-hosts` split, so Nextcloud/Syncthing staying
        on `docker-host` is the final shape, not a pending gap. See `docs/decisions.md`'s 2026-09-20 split
        plan entry for the closed-out status of the whole 4-LXC effort.
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
              ├── LXC 103 personal-hosts: 192.168.18.228
              └── LXC 104 media-hosts: 192.168.18.229
```

- **Switch:** **Mercusys MS105G (5-Port Gigabit Desktop Switch)** connects the ISP router, Main PC, and Homelab node, ensuring full 1000 Mbps line-rate file transfers between Main PC and Samba/media shares.
- **Static IPs**:
  - Proxmox VE: `192.168.18.224/24`, gateway `192.168.18.1`
  - docker-host (LXC 100): `192.168.18.225/24`, gateway `192.168.18.1`
  - yado-hosts (LXC 101): `192.168.18.226/24`, gateway `192.168.18.1`
  - dev-host (LXC 102): `192.168.18.227/24`, gateway `192.168.18.1`
  - personal-hosts (LXC 103, was "shared-hosts"): `192.168.18.228/24`, gateway `192.168.18.1`
  - media-hosts (LXC 104): `192.168.18.229/24`, gateway `192.168.18.1`
- **DNS:** `192.168.18.225` (AdGuard Home on docker-host) primary for LAN, `1.1.1.1` upstream fallback. Host `systemd-resolved` stub disabled to free port 53.
- **Remote Access (Tailscale):** Native systemd agent on Proxmox VE host (`100.108.61.124`, node `pve`), `docker-host` (`100.89.249.96`, node `docker-host.taila813af.ts.net`), and **`yado-hosts`** (LXC 101, `100.110.235.57`) — confirmed 2026-09-18 that the Tailscale node named `apps-host` in the admin console is actually this same machine, originally `hostname` = `whitearchive-hosts`, renamed again the same day to `yado-hosts` (see CHANGELOG/decisions.md for the "Yado" rebrand) — the Tailscale node name itself is still `apps-host` (an even older label from before either rename; Tailscale doesn't auto-follow OS hostname changes, so this would need to be renamed manually in the admin console if desired). Use `100.110.235.57` to reach anything on `yado-hosts` over Tailscale (e.g. `malas` on `:8082`, `sso-yado` on `:8081`, `pore-js` demo on `:8083`, `yado` on `:3000`) without needing DNS or the `.my.id` domain to be purchased/configured yet. **`shared-hosts`** (LXC 103, `100.88.119.26`) joined the tailnet 2026-09-21, node name `shared-hosts`. **`dev-host`** (LXC 102, `100.73.165.64`) and **`media-hosts`** (LXC 104, `100.113.250.97`) joined the tailnet 2026-09-21 — required adding `lxc.cgroup2.devices.allow: c 10:200 rwm` + `lxc.mount.entry: /dev/net dev/net none bind,create=dir` to both LXC configs (unprivileged containers don't get `/dev/net/tun` by default, so `tailscaled` failed to start until this was added, matching the pattern already present on `docker-host`/`shared-hosts`), then user completed interactive browser login for both. All 5 LXCs plus the `pve` host itself are now on the tailnet.
- **WAN connection is behind CGNAT** — confirmed 2026-09-22: the router's WAN IPv4 (`10.108.25.111`) is a private RFC1918 address, not the real public IP (`182.253.228.241`). The ISP NATs upstream of the router, so **no IPv4 port-forward on the home router will ever work** for inbound connections (e.g. BitTorrent). The ISP does hand out a real, non-NATed IPv6 prefix (`2404:8000:105f:d2d::/64`) — this is now the path for anything needing inbound connectivity. `vmbr0` on `pve` and LXC 104 (`media-hosts`) both hold global IPv6 addresses via SLAAC (`accept_ra 2`/`autoconf 1` in `/etc/network/interfaces` + `ip6=auto` on the LXC's `net0`, persisted via `/etc/sysctl.d/99-ipv6-lxc.conf` on both). Extend to other LXCs the same way if they ever need inbound reachability. Verified end-to-end: external TCP connect to `[2404:8000:105f:d2d:be24:11ff:feca:5f5a]:6881` (qBittorrent on `media-hosts`) succeeds.
- **Public Access (Cloudflare Tunnel):** Native systemd `cloudflared` service on `docker-host` securely exposing public services (`suryatmaja.dev`, `dash.suryatmaja.dev`, `drive.suryatmaja.dev`, `t3.suryatmaja.dev`, `komga.suryatmaja.dev`, etc.) without opening router ports. Public hostname routing is managed in the Cloudflare Zero Trust dashboard, not a local config file. **`t3.suryatmaja.dev`'s route still points at the old `192.168.18.225:9001` (docker-host) and needs to be manually repointed to `192.168.18.227:9001` (dev-host)** after the 2026-09-15 t3code migration — see CHANGELOG.

## Storage Path Convention & Live Capacity

| Data type | Location | Filesystem & Disk | Live Usage (2026-09-18) |
|---|---|---|---|
| OS, Proxmox, Docker engine | OS SSD (`/`) | ext4, `MidasForce SSD 256GB` (sda) | 50G / 147G (36%) on docker-host |
| Project code + repositories | OS SSD (`/mnt/homelab_projects/`) | ext4, OS SSD (sda) | Included in `/` |
| Database metadata (Postgres/Redis) | OS SSD (named volumes) | ext4, OS SSD (sda) | Included in `/` |
| Music library (Navidrome & Jellyfin) | **HDD-Music (`/mnt/hdd-music/music/`)** — this is the *renamed* drive (was `hdd-cloud`/Toshiba, mount point renamed 2026-09-21). Not the old WD Green (that's `hdd-backup` now). | ext4, `Toshiba 1TB 2.5"` (sdb2) | 717G / 916G (78%) — otherwise empty except `lost+found` |
| Movies, TV, Anime, Manga, Torrents, JDownloader, Nextcloud, Syncthing, misc personal folders | HDD-Media (`/mnt/hdd-media/`) — **absorbed Nextcloud/Syncthing/misc folders from the old `hdd-cloud` on 2026-09-21** (~112GB combined) as part of that drive becoming pure music | ext4, `Seagate Barracuda 1TB 7200 RPM` (sdd2) | ~791G / 916G (86%) |

## Storage Drives — Physical Inventory

| Drive Role | Hardware Model | Form Factor & Capacity | Serial Number | Mount Point | Status |
|---|---|---|---|---|---|
| **OS SSD** | MidasForce SSD 256GB (via SATA-to-M.2 adapter) | M.2 SATA in 2.5" Bay (256GB) | `RE202410151200000921` | `/` (sda) | **Active.** Boot, PVE LVM-thin pool, LXC root disks. |
| **HDD-Backup** (was `HDD-Music`, WD Green — **role in doubt**) | Western Digital Green (`WD20EZRX-00DC0B0`) | 3.5" SATA III (2TB) | `WD-WCC1T0899623` | `/mnt/hdd-backup` (device letter floats; renamed from `/mnt/hdd-music` 2026-09-21) | **⚠️ Up as of the 2026-09-21 rename, but reliability is unresolved.** Root cause remains the drive's own controller/firmware (confirmed not cable, not platters — see (56)/(59)). **2026-09-21: failed under a plain large-file sequential write** (copying video files) within ~2.5 minutes — the first time it failed on a workload type every prior test showed it tolerating (the read-based 717GB rescue ran 15hrs fine; this was a write of new data). EXT4 auto-remounted read-only, then the drive fully dropped from the kernel (`ata9.00: disable device`/`detaching`) — recovered via another physical power-cycle later the same session. **Revised conclusion: not reliably safe for bulk writes of any kind.** Renamed to `hdd-backup` anyway per user's explicit instruction (proceeding with the rename doesn't imply the reliability question is resolved — it isn't). **717GB of music from the original rescue is still physically present** (`music/` folder) — redundant with the canonical copy now on `hdd-music` (see below), kept as an incidental extra copy. **Do not write new data here without accepting real risk of another drop.** RMA sent to seller, no response — user has stopped waiting on it. |
| **HDD-Media** | Seagate Barracuda (`ST1000DM010-2EP102`) | 3.5" SATA III 7200 RPM (1TB) | `W9AS0LSD` | `/mnt/hdd-media` (sdd2) | **Active.** High-throughput Media: `videos/`, `manga-raw`, `manga-reader`, `qbittorrent`, **+ Nextcloud/Syncthing/misc personal folders** (absorbed from the old `hdd-cloud` 2026-09-21, ~112GB). Now at ~86% used, the fullest of the 3 active drives. |
| **HDD-Music** (was `HDD-Cloud`, Toshiba — now pure music) | Toshiba 2.5" HDD (`MQ04ABF100`) | 2.5" SATA III 5400 RPM (1TB) | `Y9CSTR0WT` | `/mnt/hdd-music` (sdb2; renamed from `/mnt/hdd-cloud` 2026-09-21) | **Active, healthy, repurposed 2026-09-21.** Was Nextcloud/Syncthing/LAN shared + music; now contains **only** `music/` (717GB, what Navidrome/Jellyfin actually serve) + `lost+found`. Nextcloud/Syncthing/personal folders moved to `hdd-media`. Full rename executed: `/etc/fstab` (by UUID), LXC `mp` configs on `docker-host`/`media-hosts`, every compose file referencing the old path, and Samba (`smb.conf`, share renamed `[hdd-cloud]`→`[hdd-music]`) all updated and verified working. |

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
├── jdownloader/            # JDownloader2 config + downloads
├── nextcloud/              # Nextcloud data (moved here from hdd-cloud 2026-09-21)
├── nextcloud-dropbox/      # Nextcloud files_external auto-ingest folder (added 2026-09-22)
├── syncthing/              # Syncthing data (moved here from hdd-cloud 2026-09-21)
├── nhdl/downloads/         # nhdl service dir per compose config
├── download/nhdl/          # nhdl's actual live working dir (logs/list state) — do not touch, actively written
├── personal/               # Misc personal folders, consolidated 2026-09-22 (was loose clutter in root:
│                            # Compressed/, Images/, Mods/, Tugas/, a stray PDF). Empty Windows-artifact
│                            # folders (Config.Msi, Recovery, Gapenting, Downloads, shared) deleted same day.
└── lost+found/
```

#### HDD-Music (`/mnt/hdd-music/`) — renamed 2026-09-21, was `hdd-cloud` (Toshiba)
```
/mnt/hdd-music/
├── music/                    # 717GB music collection scanned by Navidrome & Jellyfin
└── lost+found/
```

#### HDD-Backup (`/mnt/hdd-backup/`) — renamed 2026-09-21, was `hdd-music` (WD Green, unstable)
```
/mnt/hdd-backup/
├── music/                  # 717GB, redundant extra copy from the original rescue
├── backups/                # scripts/backup.sh target (when this drive is actually mounted)
├── download/                # legacy, mostly empty
├── qbittorrent/             # legacy, mostly empty
└── lost+found/
```

## Windows Network Access (SMB/Samba & WSDD)

- **Active Daemons:** `smbd` and `wsdd` systemd services running on `docker-host`.
- **Samba Shares (`/etc/samba/smb.conf`, current as of the 2026-09-21 rename):**
  - `homelab` → `/mnt` (everything, browse into subfolders)
  - `hdd-music` → `/mnt/hdd-music` (pure music library — renamed from `hdd-cloud`)
  - `hdd-media` → `/mnt/hdd-media`
  - `hdd-backup` → `/mnt/hdd-backup` (WD Green, unstable — renamed from `hdd-2tb`)
  - `manga` → `/mnt/hdd-media/manga-raw` (Read/Write, ingest for manga optimizer)
  - `projects` → `/mnt/homelab_projects` (restricted to `dev-host`/`pve` IPs, for T3 Code)
  - `projects` → `/mnt/homelab_projects` (Read/Write, restricted to PVE and dev-host for T3 Code /workspace)
- **WSDD (Web Services Dynamic Discovery):** Allows the homelab server to appear automatically under Windows Explorer "Network" without manual IP typing.