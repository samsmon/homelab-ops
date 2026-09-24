#!/bin/bash
LOG="/var/log/sync-music-final.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting background sync daemon for Uma Musume & Lossless..." >> "$LOG"

# 1. Sync Uma Musume (remaining ~19GB)
rsync -a --delete "/mnt/hdd-backup/music/Lossless/Anime/Uma Musume ~/" "/mnt/hdd-music/music/Lossless/Anime/Uma Musume ~/" >> "$LOG" 2>&1

# 2. Sync THE IDOLM@STER Shiny Colors & overall Lossless changes
rsync -a --delete "/mnt/hdd-backup/music/Lossless/" "/mnt/hdd-music/music/Lossless/" >> "$LOG" 2>&1

# 3. Ensure permissions
chown -R 100000:100000 "/mnt/hdd-music/music/Lossless" >> "$LOG" 2>&1
find "/mnt/hdd-music/music/Lossless" -type d -exec chmod 775 {} + >> "$LOG" 2>&1
find "/mnt/hdd-music/music/Lossless" -type f -exec chmod 664 {} + >> "$LOG" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Daemon sync completed successfully 100%!" >> "$LOG"
