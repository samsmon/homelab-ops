#!/bin/bash
# Backup script for homelab critical data
# Backs up: PostgreSQL dump, Docker compose configs & infra setups.
# Targets HDD-Backup if mounted, with fallback to HDD-Music (/mnt/hdd-music/backups).
# Supports optional offsite sync to Google Drive via rclone if configured.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Target directory selection
if [ -d "/mnt/hdd-backup" ] && mountpoint -q "/mnt/hdd-backup"; then
  BACKUP_DIR="/mnt/hdd-backup/backups"
else
  BACKUP_DIR="/mnt/hdd-music/backups"
fi

RETENTION_DAYS=30
DATE=$(date +%Y-%m-%d_%H-%M-%S)
DEST="$BACKUP_DIR/$DATE"
LOG_FILE="/var/log/homelab-backup.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

mkdir -p "$DEST"

log "Starting backup -> $DEST"

# 1. Dump shared PostgreSQL
if docker ps --format '{{.Names}}' | grep -q '^shared-postgres$'; then
  if docker exec shared-postgres pg_dumpall -U admin > "$DEST/postgres-dump.sql"; then
    log "PostgreSQL dump OK ($(du -h "$DEST/postgres-dump.sql" | cut -f1))"
  else
    log "ERROR: PostgreSQL dump failed"
    exit 1
  fi
else
  log "WARNING: shared-postgres container not running, skipping DB dump"
fi

# 2. Copy docker-compose configs and infra files
if [ -d "$REPO_DIR/configs" ]; then
  cp -r "$REPO_DIR/configs" "$DEST/configs"
  log "Configs backup OK"
fi

# 3. Prune local backups older than $RETENTION_DAYS days
find "$BACKUP_DIR" -maxdepth 1 -type d -name "20*" -mtime +"$RETENTION_DAYS" -exec rm -rf {} + 2>/dev/null || true
log "Pruned local backups older than ${RETENTION_DAYS}d"

# 4. Offsite sync to Google Drive via rclone if remote 'gdrive' exists
if command -v rclone &>/dev/null && rclone listremotes | grep -q '^gdrive:'; then
  log "Starting offsite sync to Google Drive (gdrive:homelab-backups)..."
  if rclone sync "$BACKUP_DIR" gdrive:homelab-backups --fast-list --transfers 4 --log-file="$LOG_FILE" --log-level NOTICE; then
    log "Offsite rclone sync OK"
  else
    log "WARNING: rclone offsite sync encountered an error"
  fi
fi

log "Backup complete: $DEST"
