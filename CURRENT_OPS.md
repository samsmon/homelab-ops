# Current Operations & Multi-Agent Locks

> Single source of live coordination across parallel AI agents (Claude Code, Gemini/Antigravity, Roo, Copilot, etc.).
> **Rule**: Check this file before starting any task. Record your active task/lock, and remove it immediately upon completion.

## Active Task Registry

- [Claude-Code] 2026-09-23 21:15 WIB: Moving hdd-media/qbittorrent/watch-torrents (77GB) -> hdd-backup/music/Torrent/done, then FLAC integrity scan | Locks: /mnt/hdd-media/qbittorrent/watch-torrents, /mnt/hdd-backup/music/Torrent/done
- [Gemini/Antigravity] 2026-09-23 21:21 WIB: Restructure GochiUsa into 3 subseries, convert/split WAV+CUE to FLAC, clean duplicates, and consolidate Gakumas, Shiny Colors (Song for Prism), and vα-liv under THE IDOLM@STER ~ | Locks: /mnt/hdd-backup/music/Lossless/Anime/ご注文はうさぎですか？？ (Gochuumon wa Usagi Desu ka) ~, /mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~, /mnt/hdd-backup/music/Lossless/Anime/学園アイドルマスター ~, /mnt/hdd-backup/music/Lossless/Anime/アイドルマスター シャイニーカラーズ ~






---

## Quick Coordination Rules
1. **Pull First**: `git pull` before anything else.
2. **Locking**: If your task modifies a service/compose file, list it above under Active Task Registry.
3. **No Collision**: Do NOT touch files or containers locked by another active agent.
4. **Push Immediately**: Selesai task, update `CHANGELOG.md`, bersihkan lock dari file ini, lalu `git add . && git commit && git push`.
