# yado-hosts (LXC 101) — Infrastruktur & Microservice Yado

> Dokumen referensi lengkap untuk LXC `yado-hosts` dan keluarga proyek **Yado** (`yado.my.id`).
> **Terakhir diverifikasi live via SSH: 2026-10-07.** Sumber kebenaran "apa yang ada sekarang" tetap `docs/architecture.md`
> dan `docs/services.md`; file ini merangkum dan menjelaskan hubungan antar-komponen.

---

## 1. Ringkasan

| Item | Nilai |
|---|---|
| Nama / VMID | `yado-hosts` / LXC **101** pada Proxmox node `pve` |
| Nama lama | `whitearchive-hosts` (rename 2026-09-18). Label Tailscale yang lebih tua: `apps-host` |
| Fungsi | Lingkungan khusus untuk keluarga proyek web Yado, dipisah dari `docker-host` agar beban/error tidak mengganggu media stack dan layanan inti |
| OS | Ubuntu Server 24.04 LTS, **unprivileged LXC** |
| Resource | 2 vCPU, 4 GB RAM (pemakaian ±300 MB), disk 30 GB thin-pool `vm-101-disk-0` (terpakai 11 GB / 37%) |
| Fitur LXC | `nesting=1,keyctl=1` (Docker di dalam LXC) + passthrough `/dev/net/tun` (Tailscale) |
| Software | Docker Engine 29.8 + Compose, Tailscale (systemd native), postfix (hanya `localhost:25`) |
| Storage | Hanya SSD 30 GB. **Tidak ada bind-mount HDD**. Data hidup di volume Docker |

---

## 2. Jaringan

### 2.1 Topologi

```
Internet
   │
   ▼
Cloudflare edge ◀──── QUIC outbound (tanpa port-forward; WAN di belakang CGNAT)
   │
   ▼
cloudflared  (container di yado-hosts, tunnel TERPISAH dari docker-host)
   │  routing per-hostname dikonfigurasi di Cloudflare Zero Trust dashboard
   ├── yado.my.id            → :3000   yado        (Next.js)
   ├── sso.yado.my.id        → :8081   sso-yado    (Laravel, OAuth2 IdP)
   ├── malas.yado.my.id      → :8082   malas       (Laravel)
   └── pore.yado.my.id       → :8083   porejs-demo (nginx static)
```

Origin tunnel terlihat dial ke `100.110.235.57:<port>` (IP Tailscale `yado-hosts` sendiri), bukan ke `192.168.18.226`
(terlihat dari log `cloudflared`). Perlu dicek di dashboard bila ingin mengubahnya.

### 2.2 Alamat

| Antarmuka | Alamat | Catatan |
|---|---|---|
| LAN `eth0` | `192.168.18.226/24`, gw `192.168.18.1` | statik, di belakang switch Mercusys MS105G |
| Tailscale | `100.110.235.57` (node `yado-hosts`) | akses privat ke semua port, tanpa DNS/domain |
| DNS resolver | `1.1.1.1`, `192.168.18.1`; search `taila813af.ts.net` | tidak memakai AdGuard `.225` |
| Docker bridge | `172.17–172.23.0.0/16` | satu bridge per compose project |

Tetangga LAN: pve `.224`, docker-host `.225`, dev-host `.227`, personal-hosts `.228`, media-hosts `.229`.

### 2.3 Port yang listen

| Port | Bind | Layanan |
|---|---|---|
| 22 | `*` | sshd |
| 3000 | `0.0.0.0` + `::` | yado |
| 8081 | `0.0.0.0` | sso-yado nginx |
| 8082 | `0.0.0.0` + `::` | malas nginx |
| 8083 | `0.0.0.0` + `::` | porejs-demo |
| 5432 | **`127.0.0.1` saja** | shared-postgres |
| 2375 | `*` | **Docker API tanpa TLS/auth** (LAN-only, untuk `homelab-cockpit`; risiko sudah diterima user 2026-09-21) |
| 25 | localhost | postfix |

### 2.4 Docker network

| Network | Dipakai oleh |
|---|---|
| `shared_net` (external) | cloudflared |
| `yado_default` | yado |
| `yado_sso` | sso-yado (app, nginx, postgres) |
| `malas_default` | malas (app, queue, nginx, db) |
| `porejs-demo_default` | porejs-demo |
| `t3code_default` | sisa lama, tidak terpakai |

Karena Cloudflare mengakses origin lewat IP host:port (bukan lewat nama container), antar-network tidak perlu saling terhubung.

---

## 3. Inventaris container

Semua container memakai `restart: unless-stopped` (diverifikasi 2026-10-07).

| Container | Image | Port host | Fungsi | Data |
|---|---|---|---|---|
| `yado` | `yado-yado` (Next.js 16 standalone) | 3000 | Frontend utama | stateless |
| `sso-yado-app-1` | build lokal (PHP-FPM, Laravel) | — | Aplikasi SSO | `./storage`, volume `sso_public` |
| `sso-yado-nginx-1` | nginx:alpine | 8081 | Web front SSO | — |
| `sso-yado-postgres-1` | postgres:16-alpine | — | DB SSO (`db_sso`), auth `trust` | volume `sso-yado_sso_postgres_data` |
| `malas-app-1` | `malas:latest` | — | Aplikasi malas (PHP-FPM) | volume `malas_storage` |
| `malas-queue-1` | `malas:latest` | — | Queue worker (`QUEUE_CONNECTION=database`) | sama |
| `malas-nginx-1` | nginx:1.27-alpine | 8082 | Web front malas | `malas_public_build` |
| `malas-db-1` | postgres:16-alpine | — | DB malas | volume `malas_db-data` |
| `porejs-demo` | `porejs-demo:local` (nginx) | 8083 | Demo pore-js, statis | — |
| `cloudflared` | cloudflare/cloudflared | — | Tunnel publik | token di `.env` |
| `shared-postgres` | postgres:16-alpine | 127.0.0.1:5432 | Postgres bersama; DB `malas` & `db_sso` **kosong dan tidak dipakai** | volume `shared-postgres_pgdata` |

Kode di server: `/opt/projects/{yado,sso.yado,malas,pore-js,porejs-demo,cloudflared,shared-postgres}`.
Skrip otomasi: `/opt/scripts/{n8n-deploy-check.sh,n8n-ssh-gate.sh}`.

---

## 4. Microservice Yado

### 4.1 yado — frontend
- Repo: `samsmon/yado`. Next.js 16.3, React 19, TypeScript. Multi-stage build → standalone.
- `docker-compose.yml` (service key `yado`, container `yado`, port 3000, `env_file: .env`) ikut ter-track di repo.
- `NEXT_PUBLIC_*` (URL SSO, malas, client id, redirect URI) **di-bake saat `next build`**, jadi mengubah env wajib **rebuild**.
- Fungsi SSO: tombol Sign In memakai PKCE (`src/lib/pkce.ts`), callback server-side di `src/app/api/auth/callback/route.ts` plus halaman `src/app/auth/callback/page.tsx`. `client_secret` hanya di server.
- Health check ke `https://sso.yado.my.id/health`.

### 4.2 sso-yado — Identity Provider
- Repo: `samsmon/sso.yado`. PHP ≥ 8.3, Laravel `^13.8` (badge README masih tertulis 11.x, abaikan), **Laravel Passport `^13.7`** sebagai OAuth2 server, Inertia v2 + Svelte 5 + Tailwind 4 + Vite 8, Postgres 16.
- Protokol: **OAuth 2.0 Authorization Code + PKCE (S256)**. Dokumentasi rinci ada di repo (`docs/INTEGRATION.md`, `API.md`, `PRD.md`, `SRS.md`).
- Fitur (dari `routes/web.php`): login (email atau username), registrasi, registrasi via undangan, lupa/reset password, verifikasi email, **2FA** (challenge, enable, confirm, disable), halaman akun (password, tema, locale, avatar), manajemen sesi/token/perangkat (revoke satu atau semua), dashboard **superadmin**, endpoint `/health`. Rate-limit di tiap endpoint sensitif (login, 2FA 5/menit, dst).
- Sesi memakai `SESSION_DRIVER=database`, `SESSION_DOMAIN=null`, lifetime 120 menit. `APP_URL=https://sso.yado.my.id`, `APP_PORT=8081`.
- Postgres sendiri (bundled). `docker-compose.override.yml` **lokal, tidak di-commit** berisi:
  - `postgres.ports: !reset []` supaya tidak bentrok dengan `shared-postgres` di port 5432
  - `restart: unless-stopped` untuk app, nginx, postgres (**ditambahkan 2026-10-07**, lihat bagian 8)
- Catatan: compose menyetel `DB_HOST/DB_READ_HOST/DB_WRITE_HOST=postgres` karena proyek memakai read/write split. `DB_USERNAME/DB_PASSWORD` di `.env` harus cocok dengan role `postgres` (trust-auth) milik DB bundled-nya.
- Working tree di server punya perubahan lokal belum di-commit: `docker/nginx/default.conf`, `resources/js/Layouts/AccountLayout.svelte`.

### 4.3 malas — manga library
- Repo: `samsmon/malas`. Laravel `^12`, PHP ≥ 8.2, Postgres 16 bundled, queue worker berbasis database.
- Data dimigrasi dari SQLite di `docker-host` pada 2026-09-18 (114 series, 773 volume, 39 koleksi, 149 collection volume, 363 cover ±51 MB). `APP_KEY` disamakan agar setting terenkripsi (Gemini AI, Resend mail) tetap bisa didekripsi.
- Deploy: `public/build` disinkronkan ke volume bersama pada tiap boot (fix white screen setelah rebuild, commit `8324e5f`); `public/storage` di-symlink untuk serving media langsung oleh nginx.
- Terdaftar sebagai OAuth client SSO sendiri (`SSO_CLIENT_ID/SECRET`, `SSO_BASE_URL`, `SSO_REDIRECT_URI`).

### 4.4 pore-js demo
- Repo: `samsmon/pore-js`, hanya `apps/demo` (statis, tanpa backend/secret).
- Image `ghcr.io/samsmon/porejs-demo:latest` bersifat private, jadi di-build lokal sebagai `porejs-demo:local` (Vite → nginx:alpine). Rebuild manual saat ada commit baru.
- Tidak terhubung ke SSO.

---

## 5. Alur SSO (OAuth2 Authorization Code + PKCE)

```
 Browser            App (yado / malas)                 sso-yado
    │  klik Sign In         │                              │
    │──────────────────────▶│ buat code_verifier + challenge│
    │◀── redirect ──────────│                              │
    │ GET sso.yado.my.id/oauth/authorize?client_id&redirect_uri&code_challenge&scope=profile:read
    │─────────────────────────────────────────────────────▶│
    │            login (email/username) + 2FA bila aktif    │
    │◀──── redirect {redirect_uri}?code=… ─────────────────│
    │──────────────────────▶│                              │
    │                       │ POST token: code + code_verifier + client_secret (server-side)
    │                       │─────────────────────────────▶│
    │                       │◀──────── access token ───────│
    │                       │ GET /api/user  (butuh scope profile:read)
    │                       │─────────────────────────────▶│
    │                       │◀──────── profil user ────────│
    │◀── sesi login ────────│                              │
```

| App | Redirect URI | Konfigurasi |
|---|---|---|
| yado | `https://yado.my.id/auth/callback` | `NEXT_PUBLIC_SSO_URL`, `NEXT_PUBLIC_SSO_CLIENT_ID`, `NEXT_PUBLIC_SSO_REDIRECT_URI` (build-time), `SSO_CLIENT_SECRET` (server) |
| malas | `https://malas.yado.my.id/auth/callback` | `SSO_BASE_URL`, `SSO_CLIENT_ID`, `SSO_CLIENT_SECRET`, `SSO_REDIRECT_URI` |

Poin penting:
- Tiap app = **satu OAuth client confidential terpisah** di Passport.
- Tidak ada komunikasi langsung antar-container. Semua lewat URL publik `sso.yado.my.id` (via tunnel), jadi **login semua app bergantung pada SSO dan cloudflared yang hidup**.
- Bukan Forward-Auth NPM. IdP lama (`homelab-idp`) dihapus 2026-09-18.
- Scope `profile:read` wajib, kalau tidak `/api/user` ditolak.
- Secret tidak disimpan di repo. Hanya ada di `.env` di server masing-masing.

---

## 6. Deploy & otomasi

- **Cara deploy manual:** `cd /opt/projects/<proj> && git pull --ff-only && docker compose up -d --build`. Server **tidak punya kredensial push GitHub**; commit dilakukan dari `docker-host`/mesin lain.
- **n8n auto-deploy** (workflow `auto-deploy` di n8n pada docker-host): polling tiap 5 menit via SSH ke `yado-hosts` (proyek: yado, sso.yado, malas, pore-js). Key SSH dibatasi forced-command `n8n-ssh-gate.sh`; hanya `n8n-deploy-check <project> [--apply]`. Aturan: hanya deploy bila di branch `main`, tidak ada tracked change lokal, fast-forward saja. **Status: dry-run** (belum `--apply`). Detail: `docs/n8n-auto-deploy.md`.
- Karena aturan "tidak ada tracked change lokal", **jangan mengubah file tracked di server**. Itu sebabnya perubahan restart policy ditaruh di `docker-compose.override.yml`.

---

## 7. Operasional

```bash
# status
ssh yado-hosts 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
# health SSO
curl -s -o /dev/null -w '%{http_code}\n' https://sso.yado.my.id/health
# log
ssh yado-hosts 'docker logs --tail 30 sso-yado-app-1'
ssh yado-hosts 'docker logs --tail 20 cloudflared'
# naikkan SSO setelah mati
ssh yado-hosts 'cd /opt/projects/sso.yado && docker compose up -d --no-build'
```

Backup: **belum ada backup terjadwal** untuk volume Postgres (`malas_db-data`, `sso-yado_sso_postgres_data`) maupun `malas_storage`. Ini celah.

---

## 8. Riwayat insiden / perubahan penting

| Tanggal | Peristiwa |
|---|---|
| 2026-09-18 | Rebrand White Archive → Yado, rename LXC, fresh redeploy yado & sso-yado, migrasi data malas, deploy pore-js dan cloudflared |
| 2026-09-20 | SSO login yado diperbaiki penuh (PKCE, callback, scope), pore.yado.my.id live |
| 2026-10-07 | **sso-yado ditemukan mati** (3 container `Exited (255)` ±2 minggu, tanpa restart policy; kemungkinan tidak naik lagi setelah reboot LXC. Sebab pasti belum dibuktikan). Dinyalakan ulang dan ditambah `restart: unless-stopped` lewat `docker-compose.override.yml` (backup: `docker-compose.override.yml.bak`). `/health` 200 via localhost, Tailscale, dan publik |

---

## 9. Masalah terbuka

1. `cloudflared` sesekali: `lookup region1.v2.argotunnel.com: i/o timeout`. Tunnel tetap tersambung, tapi mirip pola ISP DNS hijack yang diperbaiki di nhdl; resolver LXC `1.1.1.1` + `192.168.18.1`.
2. `shared-postgres` berisi DB kosong tak terpakai; bisa dipangkas.
3. Network `t3code_default` tak terpakai.
4. Docker API `:2375` tanpa auth.
5. Belum ada backup terjadwal untuk data Postgres.
6. Perubahan lokal belum di-commit di repo `sso.yado` di server.
7. `docs/services.md` masih menulis domain "belum dibeli" dan route ke `192.168.18.226`; perlu disinkronkan dengan kondisi live.
8. Rute tunnel dikelola di Cloudflare dashboard, tidak ter-track di repo.
