#!/bin/bash
# sync-music.sh — Synchronize music between Master (hdd-backup) and curated Playback (hdd-music).
#
# Architecture:
#   Master Storage:   /mnt/hdd-backup/music/ (full archive, cold-backup drive)
#   Playback/Serving: /mnt/hdd-music/music/  (curated subset for Navidrome/Jellyfin — hdd-music
#                                              is smaller and doesn't need to hold everything)
#
# Skip/replace behavior: uses rsync --checksum, so a file already in place with matching content
# is skipped entirely (no re-copy), and a file that exists but differs (misplaced/wrong/corrupt)
# gets replaced. This is safer than a plain size+mtime check.
#
# Usage:
#   bash scripts/sync-music.sh                    # Sync Master (hdd-backup) -> Playback (hdd-music)
#   bash scripts/sync-music.sh --to-backup         # Push Playback -> Master (rare; Master should
#                                                   #   normally be the source of truth)
#   bash scripts/sync-music.sh --path "Lossless/J-Pop"  # Only sync a specific subfolder (curation)
#   bash scripts/sync-music.sh --delete            # Also remove files from destination that are
#                                                   #   no longer in source (use with care)
#   bash scripts/sync-music.sh --dry-run           # Preview only, no changes

set -uo pipefail

LOCKFILE="/var/run/sync-music.lock"
LOGFILE="/var/log/sync-music.log"

MASTER_DIR="/mnt/hdd-backup/music"
PLAYBACK_DIR="/mnt/hdd-music/music"

DIRECTION="to-music"
DRY_RUN=""
DELETE=""
SUBPATH=""

while [ $# -gt 0 ]; do
  case "$1" in
    --to-backup)
      DIRECTION="to-backup"
      ;;
    --to-music)
      DIRECTION="to-music"
      ;;
    --dry-run|-n)
      DRY_RUN="--dry-run"
      ;;
    --delete)
      DELETE="--delete"
      ;;
    --path)
      shift
      SUBPATH="$1"
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--to-backup | --to-music] [--path <subfolder>] [--delete] [--dry-run]"
      exit 1
      ;;
  esac
  shift
done

exec 200>"$LOCKFILE"
flock -n 200 || {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Another music sync process is already running. Exiting." | tee -a "$LOGFILE"
  exit 1
}

if [ "$DIRECTION" = "to-backup" ]; then
  SRC="$PLAYBACK_DIR/${SUBPATH}"
  DEST="$MASTER_DIR/${SUBPATH}"
  DESC="Push Playback -> Master (hdd-music -> hdd-backup)"
else
  SRC="$MASTER_DIR/${SUBPATH}"
  DEST="$PLAYBACK_DIR/${SUBPATH}"
  DESC="Sync Master -> Playback (hdd-backup -> hdd-music)"
fi

mkdir -p "$DEST"

echo "==========================================================" | tee -a "$LOGFILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting music sync: $DESC" | tee -a "$LOGFILE"
echo "Source:      $SRC" | tee -a "$LOGFILE"
echo "Destination: $DEST" | tee -a "$LOGFILE"
[ -n "$SUBPATH" ] && echo "Subpath:     $SUBPATH" | tee -a "$LOGFILE"
[ -n "$DELETE" ] && echo "Mode:        --delete enabled (destination will be pruned to match source)" | tee -a "$LOGFILE"
[ -n "$DRY_RUN" ] && echo "Mode:        DRY RUN (no changes)" | tee -a "$LOGFILE"
echo "==========================================================" | tee -a "$LOGFILE"

# --checksum: skip files whose content already matches (not just size/mtime) - true
#   "already correct, skip it" behavior. A file that exists but differs gets replaced.
# --partial --inplace: safe to interrupt/resume on large files without losing all progress.
rsync -avh --checksum --partial --inplace --info=progress2 $DELETE $DRY_RUN \
  --log-file="$LOGFILE" \
  "$SRC" "$DEST"

RC=$?

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync finished with exit code $RC" | tee -a "$LOGFILE"
echo "Storage Usage:" | tee -a "$LOGFILE"
df -h "$MASTER_DIR" "$PLAYBACK_DIR" | tee -a "$LOGFILE"
echo "==========================================================" | tee -a "$LOGFILE"

exit $RC
