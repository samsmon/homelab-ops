# Panduan Lengkap AGY Web Terminal (`agy.suryatmaja.dev`)

Dokumentasi operasional untuk menggunakan **Google Antigravity / Agentic CLI Terminal** berbasis web di homelab `dev-host` (LXC 102).

- **URL Akses**: [https://agy.suryatmaja.dev](https://agy.suryatmaja.dev)
- **Akses LAN / Fallback**: `http://192.168.18.227:7681`
- **Lokasi Project**: `/workspace/` (semua repo: `stream-vault`, `homelab-dashboard`, `malas`, dll.)

---

## 1. Konsep Dasar & Navigasi Project

Terminal ini selalu membuka sesi persistent `tmux` bernama `agy-workspace` dengan root direktori di `/workspace`.

### Pindah Project & Mulai Coding
Setiap project homelab Anda tersimpan di direktori `/workspace/<nama-project>`. Cukup `cd` ke folder project yang ingin Anda kerjakan:

```bash
# Contoh 1: Masuk ke project stream-vault
cd /workspace/stream-vault

# Contoh 2: Masuk ke dashboard homelab
cd /workspace/homelab-dashboard

# Contoh 3: Masuk ke portfolio
cd /workspace/portofolio
```

---

## 2. Cara Menjalankan AGY / Agentic CLI

Ada 2 cara menjalankan agent di dalam terminal ini:

### Cara A: Menjalankan Perintah di dalam Environment Developer (Container)
Gunakan helper **`agy-dev`** yang sudah disiapkan:
```bash
# Membuka interactive bash di dalam container dev T3/AGY
agy-dev bash

# Langsung menjalankan perintah spesifik
agy-dev claude
```

### Cara B: Mengirim Perintah via Orchestration (Suruh Claude / Antigravity Utama)
Jika Anda sedang ngobrol dengan Claude Code atau Antigravity di PC, Anda cukup bilang:
> *"Tolong jalankan di tmux agy: cd ke /workspace/stream-vault lalu jalankan perintah revisi scanner"*

Agent utama akan otomatis mengirim *keystrokes* ke sesi `agy-workspace` tanpa Anda perlu mengetik manual!

---

## 3. Shortcut Sakti Multi-Terminal (`tmux`)

Karena berjalan di atas `tmux`, Anda bisa membuka banyak terminal sekaligus (multi-window & split pane) tanpa takut sesi tertutup saat browser ditutup.

> **PENTING**: Semua shortcut tmux diawali dengan menekan tombol prefix: **`Ctrl + B`**, lalu lepas, baru tekan tombol berikutnya.

### A. Manajemen Tab / Jendela (Windows)
| Aksi | Shortcut | Penjelasan |
|---|---|---|
| **Buka Tab Terminal Baru** | `Ctrl + B` lalu tekan `C` | Membuka tab shell baru di pojok bawah status bar. |
| **Ganti Nama Tab** | `Ctrl + B` lalu tekan `,` | Memberi nama tab (misal: "stream-vault", "logs", "agy-worker"). |
| **Pindah ke Tab Berikutnya** | `Ctrl + B` lalu tekan `N` | Pindah ke tab kanan (Next). |
| **Pindah ke Tab Sebelumnya** | `Ctrl + B` lalu tekan `P` | Pindah ke tab kiri (Previous). |
| **Pindah ke Tab Nomor X** | `Ctrl + B` lalu tekan `0..9` | Langsung lompat ke tab nomor 0, 1, 2, dst. |
| **Tutup Tab Aktif** | Ketik `exit` atau `Ctrl + D` | Menutup tab saat ini. |

### B. Tiling Window ala Hyprland & Mouse Support (Baru!)
Terminal sekarang sudah mendukung **full mouse interaction** dan auto-split ala tiling window manager:

| Fitur / Aksi | Shortcut / Cara Pakai | Penjelasan |
|---|---|---|
| **Klik Pindah Window** | **Klik Mouse Langsung** | Cukup klik panel mana pun dengan mouse, kursor langsung aktif di sana! |
| **Ubah Ukuran Layar** | **Drag Border dengan Mouse** | Klik garis pemisah antar terminal lalu geser pakai mouse. |
| **Scroll Layar Bebas** | **Scroll Wheel Mouse** | Putar roda mouse langsung untuk melihat history log (tanpa shortcut!). |
| **Buka Layar di KANAN (Tiling)** | `Ctrl + B` lalu tekan `Enter` (atau `V`) | Otomatis membelah layar dan membuka terminal baru di sebelah KANAN. |
| **Buka Layar di BAWAH** | `Ctrl + B` lalu tekan `S` | Otomatis membelah layar ke BAWAH. |
| **Pindah Panel Cepat (No Prefix)**| `Alt + Panah Kiri/Kanan/Atas/Bawah` | Langsung pindah fokus antar panel tanpa perlu tekan `Ctrl + B`! |
| **Zoom/Maximize Panel** | `Ctrl + B` lalu tekan `Z` | Membesarkan panel aktif jadi 1 layar penuh (ulangi `Ctrl+B Z` untuk un-zoom). |

### C. Scroll Layar / Melihat Log Panjang
* Tekan **`Ctrl + B`** lalu tekan **`[`** (kurung siku buka).
* Gunakan tombol **Panah Atas / Bawah** atau **Page Up / Page Down** untuk scroll riwayat teks terminal.
* Tekan tombol **`Q`** untuk keluar dari mode scroll dan kembali mengetik normal.

---

## 4. Cara Manajemen & Ganti Akun Google / AI Auth

Agar antar akun Google (misal akun personal vs akun kerja/cadangan) tidak saling menimpa token atau bentrok kuota:

### Metode 1: Isolasi Profil via Sub-User Linux (Paling Rapi & Permanen)
Di Linux, kita bisa membuat user khusus untuk tiap akun:

1. Buat user baru di dev-host (misal: `maja-work`):
   ```bash
   adduser --disabled-password --gecos "" maja-work
   usermod -aG sudo,docker maja-work
   ```
2. Untuk switch akun saat mau coding:
   ```bash
   # Masuk ke profil akun kerja
   su - maja-work
   cd /workspace/stream-vault

   # Login Google / AI auth pertama kali
   # (Token akan tersimpan rapi di /home/maja-work/.config)
   ```
3. Token milik `root` dan `maja-work` terpisah 100% dan tidak akan saling logout!

### Metode 2: Backup / Switch File Kredensial Langsung
Jika menggunakan user yang sama:
* Token OAuth Google/Antigravity tersimpan di:
  `~/.gemini/` dan `~/.config/antigravity/`
* Anda bisa membuat alias folder sederhana:
  ```bash
  # Simpan sesi akun A
  cp -r ~/.gemini ~/.gemini-personal

  # Simpan sesi akun B
  cp -r ~/.gemini ~/.gemini-work

  # Switch ke akun personal
  rm -rf ~/.gemini && cp -r ~/.gemini-personal ~/.gemini
  ```

---

## 5. Tips Operasional & Troubleshooting

* **Terminal Terasa Freeze / Macet**:
  Jika ada proses yang hang di terminal, batalkan dengan `Ctrl + C`. Jika masih nyangkut, tekan `Ctrl + \`.
* **Koneksi Browser Terputus**:
  Tidak perlu panik! Semua proses yang sedang berjalan di `tmux` tidak akan mati. Cukup refresh halaman `https://agy.suryatmaja.dev`, terminal Anda akan kembali tepat seperti sebelum terputus.
* **Restart Service ttyd**:
  Jika web terminal ingin di-restart dari sisi host:
  ```bash
  systemctl restart ttyd
  ```
