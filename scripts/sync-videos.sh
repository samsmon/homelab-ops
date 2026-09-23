#!/bin/bash
# sync-videos.sh — Synchronize Video media between Master (hdd-backup) and Playback/Serving (hdd-media).
#
# Architecture (Alur A):
#   Master Storage:   /mnt/hdd-backup/videos/ (Cold master archive)
#   Playback/Serving: /mnt/hdd-media/videos/  (Active serving library for Jellyfin)
#
# Usage:
#   bash scripts/sync-videos.sh              # Sync Master (hdd-backup) -> Playback (hdd-media)
#   bash scripts/sync-videos.sh --to-backup  # Seed/Backup from hdd-media -> hdd-backup
#   bash scripts/sync-videos.sh --dry-run    # Dry run preview
#

set -uo pipefail

LOCKFILE="/var/run/sync-videos.lock"
LOGFILE="/var/log/sync-videos.log"

MASTER_DIR="/mnt/hdd-backup/videos"
PLAYBACK_DIR="/mnt/hdd-media/videos"

DIRECTION="to-media"
DRY_RUN=""

for arg in "$@"; do
  case "$arg" in
    --to-backup|--seed)
      DIRECTION="to-backup"
      ;;
    --to-media)
      DIRECTION="to-media"
      ;;
    --dry-run|-n)
      DRY_RUN="--dry-run"
      ;;
    *)
      echo "Unknown option: $arg"
      echo "Usage: $0 [--to-backup | --to-media] [--dry-run]"
      exit 1
      ;;
  esac
done

# Ensure flock is respected
exec 200>"$LOCKFILE"
flock -n 200 || {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Another video sync process is already running. Exiting." | tee -a "$LOGFILE"
  exit 1
}

if [ "$DIRECTION" = "to-backup" ]; then
  SRC="$PLAYBACK_DIR/"
  DEST="$MASTER_DIR/"
  DESC="Seed/Backup (hdd-media -> hdd-backup)"
else
  SRC="$MASTER_DIR/"
  DEST="$PLAYBACK_DIR/"
  DESC="Sync Master -> Playback (hdd-backup -> hdd-media)"
fi

mkdir -p "$DEST"

echo "==========================================================" | tee -a "$LOGFILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting video sync: $DESC" | tee -a "$LOGFILE"
echo "Source:      $SRC" | tee -a "$LOGFILE"
echo "Destination: $DEST" | tee -a "$LOGFILE"
[ -n "$DRY_RUN" ] && echo "Mode:        DRY RUN (no changes)" | tee -a "$LOGFILE"
echo "==========================================================" | tee -a "$LOGFILE"

# rsync parameters:
# -a: archive (preserves perms, times, symlinks, owners)
# -v: verbose
# -h: human readable numbers
# --partial: keep partially transferred files
# --inplace: update destination files directly (saves disk space during copy)
# --info=progress2: print overall progress
rsync -avh --partial --inplace --info=progress2 $DRY_RUN \
  --log-file="$LOGFILE" \
  "$SRC" "$DEST"

RC=$?

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync finished with exit code $RC" | tee -a "$LOGFILE"
echo "Storage Usage:" | tee -a "$LOGFILE"
df -h "$MASTER_DIR" "$PLAYBACK_DIR" | tee -a "$LOGFILE"
echo "==========================================================" | tee -a "$LOGFILE"

exit $RC
