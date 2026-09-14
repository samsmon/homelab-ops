# Architecture - Current State

> This file reflects what EXISTS right now. Update it whenever the actual topology changes.
> Last verified: 2026-09-11 (via SSH, during Proxmox VE install + docker-host LXC setup)

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
  └── LXC 100: "docker-host" (Ubuntu Server 24.04 LTS) — 192.168.18.225
        RAM allocated: 12GB (of 32GB total)
        CPU allocated: 4 cores (of 4 total on the actual i5-7500 — no hyperthreading, so this
          is the host's full core count, not the 3C/6T-of-4C/8T originally planned around the
          i7-7700 spec)
        Storage: 150GB (local-lvm thin pool; pool extended from 140.87GB to ~156.88GB using the
          VG's remaining free space, to fully back this volume without thin-pool overcommit)
        Proxmox container features "nesting=1,keyctl=1" enabled (required for Docker inside LXC)
        Docker Engine 29.8.0 + Compose plugin v5.5.1 installed, verified working (hello-world)
        IPv6 disabled on this LXC (network is IPv4-only; avoids dead-route connection failures
          when pulling images/DNS)
```

**LXC, not VM** — chosen over a VM for docker-host because LXC shares the host kernel (near-zero
overhead, RAM/CPU used efficiently) vs. a VM's full hardware virtualization (heavier, RAM/CPU
allocation less flexible). Trade-off: Docker running inside an LXC needs the Proxmox container
feature `nesting=1` enabled (and sometimes `keyctl=1`) to work — without it, Docker/container
operations inside the LXC fail with permission/cgroup errors. See `decisions.md`.

## Network

```
Router ISP (main house WiFi)
  └── Switch Gigabit: Mercusys MS105G (5-port, TP-Link)
        └── PC + Homelab (M710q)
```

- **Router:** the ISP's own router — no dedicated MikroTik router deployed for now (see
  `decisions.md`: skipped for budget efficiency, not currently needed).
- **Switch:** Mercusys MS105G (by TP-Link), 5-port Gigabit — added specifically so PC↔Homelab file
  transfer gets full Gigabit speed. This works even though the ISP router's own ports may not
  all be Gigabit, because switch-to-switch-port speed between devices on the same switch isn't
  limited by the router's uplink port speed.
- **MikroTik RB941-2nD (hAP Lite):** originally considered as a second router for network
  isolation, but it's Fast Ethernet (100Mbps) only — and is currently skipped entirely (see
  network decision below), not deployed as a second-layer router either.
- **Proxmox host:** `pve.suryatmaja.dev` — `192.168.18.224/24`, gateway `192.168.18.1`
- **Static IP for docker-host:** `192.168.18.225/24`, gateway `192.168.18.1`
- **DNS:** `192.168.18.1` (router-forwarded)
- **Remote access:** Tailscale — installed and connected on docker-host (2026-09-11). Tailnet IP
  `100.89.249.96`, hostname `docker-host`, MagicDNS suffix `taila813af.ts.net` (tailnet
  `srytmj.github`). Joined via a pre-generated auth key (not interactive browser login) — see
  CHANGELOG.md. `--accept-dns=false` was used so Tailscale's own DNS doesn't override the LXC's
  resolver setup (which was tuned to fix registry DNS issues — see CHANGELOG). Per-service
  MagicDNS subdomains (via `tailscale serve`) not yet set up — still just the one node identity.
- **Domain/DNS / Cloudflare Tunnel:** **one exception** to the Tailscale-only policy — the
  `portfolio` project is exposed to the public internet via Cloudflare Tunnel (no ports opened
  on the router/firewall). Every other service, including the Homepage dashboard the portfolio
  links to via its hidden button, stays Tailscale-only. See `decisions.md` for the full
  reasoning.

## Services Running (Docker containers on docker-host)

See `docs/services.md` for the full list with ports and data locations. As of this verification
pass, docker-host has only the bare Docker Engine installed — no services deployed yet.

Planned (per roadmap/decisions, not yet deployed):
- Reverse proxy: Traefik / Nginx Proxy Manager
- Container management: Portainer
- Shared DB: PostgreSQL (multi-database) + Redis (shared, per-project key prefix)
- 10 personal web projects
- Media stack: Jellyfin (movies/TV + music library), Kavita, Nextcloud

## Storage Path Convention

| Data type | Location |
|---|---|
| OS, Docker engine, images | OS SSD (M.2 SATA, via adapter in the internal 2.5" bay) |
| Project code + dependencies | OS SSD |
| Database metadata (Postgres/Redis) | OS SSD |
| Music (Jellyfin) | HDD-Music, 2TB 3.5" (`/mnt/hdd-music/`) |
| Movies/TV, anime (video), manga | HDD-Media, 1TB 2.5" (`/mnt/hdd-media/`) |
| Nextcloud (incl. images) + VaultS3 | HDD-Cloud, 1TB 3.5" (`/mnt/hdd-cloud/`) |

**Rule:** never let bulk media default-write to the OS SSD. Always explicitly map Docker volumes to the correct HDD's path.

## Storage Drives — 3 HDDs, Each With a Dedicated Purpose

Supersedes the earlier single-HDD (`/mnt/hdd2tb/`) plan. Final topology is **3 separate drives**,
each single-purpose — no RAID/pooling across them, so a failure on one drive only affects that
drive's category of data (e.g. losing HDD-Cloud doesn't touch music or media).

| Drive | Capacity | Form factor | Mount point | Purpose |
|---|---|---|---|---|
| HDD-Music (Seagate Barracuda, already purchased) | 2TB | 3.5" | `/mnt/hdd-music/` | Music only, for Jellyfin |
| HDD-Media (new) | 1TB | 2.5" | `/mnt/hdd-media/` | Movies/TV, anime (video), manga — images moved to Nextcloud instead |
| HDD-Cloud (new) | 1TB | 3.5" | `/mnt/hdd-cloud/` | Nextcloud + VaultS3 |
| HDD-Backup (WD Blue, already owned/idle) | 320GB | 3.5" | `/mnt/hdd-backup/` | Dedicated Restic backup target for DB dumps + config (`scripts/backup.sh`) — physically separate from the 3 drives above, so it protects against any one of them failing, not just accidental deletion |

An extra 1TB 2.5" HDD is also on hand but currently **unallocated (spare)** — not assigned to
any role yet. A RAID1 (mirrored) setup for HDD-Cloud using this spare was considered and
deferred; single-drive-per-category (no RAID) remains the plan for now.

**Physical mounting:** resolved — a multi-bay dock/enclosure was sourced for HDD-Media +
HDD-Cloud (HDD-Music keeps its original single-bay dock). HDD-Backup (WD Blue) needs its own
small mounting/dock solution too, since it's a 4th drive beyond the original 3.

**LM418 port usage:** 4 of the LM418's 5 SATA ports are now used (HDD-Music, HDD-Media,
HDD-Cloud, HDD-Backup) — 1 port still spare.

**Cooling:** the multi-bay dock is bought without a built-in fan; cooling instead comes from 3
reused fans (salvaged from an old PC, Molex-powered natively) — 1 for the HDD-Music dock, 2 for
the multi-bay dock (push-pull or one per drive). This uses 3 of the Enhance ENP-2320's 5 Molex
outputs directly; the other 2 Molex outputs feed the Molex-to-SATA splitters (dual + triple) for
the drives' power. See `decisions.md` for the full reasoning (why fans are needed for 24/7
operation, and why reused fans are sufficient despite lower RPM).

**No backup exists yet for any of this media/file data** — `scripts/backup.sh`/Databasus only
covers the PostgreSQL database, not Nextcloud/Jellyfin file content. See the Restic → VaultS3
backup decision in `decisions.md` for the plan (now scoped to Nextcloud, since Immich was
dropped — see below).

### HDD-Music (`/mnt/hdd-music/`)

```
/mnt/hdd-music/
└── jellyfin/
    └── music/
```

### HDD-Media (`/mnt/hdd-media/`)

```
/mnt/hdd-media/
├── jellyfin/
│   ├── movies/
│   ├── tv/
│   └── anime/            # video anime — same handling as movies/tv, watched through Jellyfin
└── kavita/
    └── manga/
```

Images (anime wallpapers, phone/pc/laptop screenshots) don't live here — they go into **Nextcloud**
on HDD-Cloud instead (see below), organized as folders inside Nextcloud's own storage. HDD-Media
is now purely video + manga.

### HDD-Cloud (`/mnt/hdd-cloud/`)

```
/mnt/hdd-cloud/
├── nextcloud/
├── vaults3/
└── shared/                # ad-hoc file drop, accessed from Windows via SMB — lives here since this is the general-purpose storage drive
```

Each app-specific folder is bind-mounted into its own Docker container, on whichever drive its
data type belongs to per the table above. `shared/` is not tied to any container; it's a
general-purpose folder for manual file transfers (see SMB access below).

**Which folders are safe to drop files into manually (via SMB) vs. app-managed only:**

| Folder | Manual file drop via SMB? | Why |
|---|---|---|
| `jellyfin/movies/`, `/tv/`, `/anime/`, `/music/` | ✅ Yes — this is the normal workflow | Jellyfin scans the folder for new files; no separate upload step needed |
| `kavita/manga/` | ✅ Yes — this is the normal workflow | Same as Jellyfin — Kavita scans the folder |
| `nextcloud/` | ❌ No | Has its own internal DB tracking files (this now includes images — anime wallpapers, phone/pc/laptop screenshots) — must go through Nextcloud's app/web UI/sync client, not direct filesystem copy, or the DB gets out of sync |
| `vaults3/` | ❌ No (usually) | Written to via S3 API by whatever app/backup process uses it as a target, not typically browsed/edited by hand |
| `shared/` | ✅ Yes | General-purpose, not tied to any app |

## Windows Network Access (SMB/Samba)

Yes — folders on the homelab can be made accessible from Windows File Explorer as a network
share, via a Samba service. Shares span all 3 drives, per the table above:

- **Planned setup:** Samba running as a container (or host-level `smbd` inside the docker-host
  LXC) exposing `hdd-cloud/shared/` (read-write), plus `hdd-media/jellyfin/{movies,tv,anime}`,
  `hdd-media/kavita/manga`, and `hdd-music/jellyfin/music` (all read-write, for dropping in
  media/files) — each as its own SMB share or subfolder under one share. `nextcloud/` and
  `vaults3/` are **not** exposed for direct write, only managed through their own apps/APIs
  (images now live in Nextcloud, not a plain SMB folder — see above).
- **Access from Windows:** map network drive to `\\<docker-host-ip>\<share-name>`, or type the
  path directly into File Explorer's address bar.
- **Auth:** local Samba user/password (not tied to any app's own auth) — set up during Setup mode.
- Not yet implemented — this is a planned addition, tracked in `docs/roadmap.md`.
