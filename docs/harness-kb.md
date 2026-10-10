# Harness & Knowledge Base (token efficiency)

Tujuan: kurangi token per sesi tanpa menurunkan akurasi. Dibuat 2026-10-10.

## Pengaman mekanis (`.claude/hooks/guard.py`, Claude Code saja)
| Kasus | Hasil |
|---|---|
| `Read` file `.md/.log/.json/.yml/.sql` > 24 KB tanpa `limit` | deny, diarahkan ke KB atau offset/limit |
| `cat`/`Get-Content` pada `CHANGELOG*` tanpa `head`/`tail`/`grep` | deny |
| Loop `while/until ... sleep` atau `sleep N && ...` | deny (aturan no-polling) |
| `git push --force`, `reset --hard`, `clean -f` | ask (user memutuskan) |

Hook tidak pernah memblokir bila input rusak. Uji: 10 kasus, semuanya lulus.
Agent lain (Antigravity, Roo) tidak menjalankan hook ini; aturan teks di `CLAUDE.md` tetap berlaku untuk mereka.

## Knowledge base
Repo `rag-kb` (CLI `kb`, Postgres+pgvector di `rag-postgres`, embedding Voyage `voyage-4`).
Sumber `homelab-ops` mengindeks: `docs/**`, `CHANGELOG.md`, `README.md`.
Tidak diindeks: `CLAUDE.md`, `AGENTS.md`, `CURRENT_OPS.md`, `scripts/**`, `configs/**`.

Cara pakai (DB hanya terjangkau lewat Tailscale):
- PowerShell: `& "$HOME\Documents\GitHub\rag-kb\kb.cmd" ask 'rumusan 1' 'rumusan 2'`
- sh: `~/Documents/GitHub/rag-kb/kb ask '...'`
- Satu chunk penuh: `kb show <id>`. Daftar lengkap: tambah `--top 10`.

Aturan akurasi:
1. KB hanya untuk dokumentasi dan riwayat. State server live **selalu** diverifikasi lewat SSH.
2. Salin baris `PENANDA:` dari hasil ke jawaban. `TANPA KB`, hasil lemah, atau DB tidak terjangkau: katakan terus terang, jangan menebak.
3. Klaim penting dari KB dicek ke file sumber (`repo/path` + lokasi) sebelum mengubah apa pun.
4. Setelah mengubah `docs/` atau `CHANGELOG.md`: `kb sync` (hanya file berubah yang di-embed).
