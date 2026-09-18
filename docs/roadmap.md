# Roadmap

> What's planned, not what exists yet. Move items to CHANGELOG.md once done, and update architecture.md accordingly.

## Now

- [ ] Source a small mount/dock solution for HDD-Backup (WD Blue 320GB) — the 4th drive, beyond the original 3-drive dock plan
- [x] Deploy first batch of the 10 web projects — **started 2026-09-11: `portfolio` deployed** (`yorha-portfolio` container, port 3080, on docker-host) and `yado` (was `whitearchive`) on `yado-hosts` (LXC 101, was `whitearchive-hosts`). **`malas`, `sso-yado`, `pore-js` all deployed 2026-09-18** on the same host — see `docs/services.md`.

## Next

- [ ] Connect rclone OAuth to Google Drive (idle 5TB, AI Pro) — headless OAuth setup pending.
- [ ] homelab-sentinel: Telegram bot (Python, `python-telegram-bot`) — consolidates monitoring alerts + interactive queries + whitelisted management + short QnA (Gemini API free tier). Needs: Telegram bot token (@BotFather), Gemini API key (AI Studio).
- [ ] Deploy Home Assistant (once the smart power plug with HA support arrives)
- [ ] Deploy VaultS3 (lightweight S3-compatible object storage) — waiting for cross-drive placement.
- [ ] Deploy SnapOtter — self-hosted file-processing toolkit (200+ tools: convert/compress/OCR/transcribe across image/video/audio/PDF).
- [ ] (no hosting needed) CodeFlow — single-HTML architecture-map tool.

## After base homelab is up and stable

- [ ] Deploy CapRover — mini hosting panel for friends to self-deploy their own CRUD web apps (~15 apps planned).
- [ ] Deploy MySQL/MariaDB via CapRover's One-Click Apps catalog, dedicated to the friends'-apps pool.
- [ ] Extend Cloudflare Tunnel for CapRover apps.

## Later / Ideas

- [ ] k3s sandbox environment (separate LXC, for learning Kubernetes — not for production)
- [ ] VLAN isolation between homelab and personal devices
