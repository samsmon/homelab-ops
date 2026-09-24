#!/bin/bash
# sync-from-master.sh — Reconcile each target drive against the Master archive (hdd-backup),
# driven by scripts/sync-config.conf. Designed to be run either by cron (scheduled) or manually
# on demand (e.g. "Run Now" in Cronicle right after adding new files).
#
# Behavior: NOT a blind full copy every run. Uses rsync --checksum, so only files that are
# missing, misplaced, or actually different get touched — files already correctly in place
# are skipped. Nothing is ever deleted unless --prune is explicitly passed.
#
# Usage:
#   bash scripts/sync-from-master.sh                 # report + execute (default: no deletes)
#   bash scripts/sync-from-master.sh --report-only    # dry-run: show what WOULD change, no writes
#   bash scripts/sync-from-master.sh --prune          # also remove target files no longer on master
#   bash scripts/sync-from-master.sh --only music      # limit to one MEDIA_TYPE from the config
#   bash scripts/sync-from-master.sh --config <path>   # override config file location

set -uo pipefail

LOCKFILE="/var/run/sync-from-master.lock"
LOGFILE="/var/log/sync-from-master.log"
CONFIG="/opt/scripts/sync-config.conf"

REPORT_ONLY=0
PRUNE=""
ONLY=""

while [ $# -gt 0 ]; do
  case "$1" in
    --report-only|-n) REPORT_ONLY=1 ;;
    --prune)          PRUNE="--delete" ;;
    --only)           shift; ONLY="$1" ;;
    --config)         shift; CONFIG="$1" ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--report-only] [--prune] [--only <media_type>] [--config <path>]"
      exit 1
      ;;
  esac
  shift
done

exec 200>"$LOCKFILE"
flock -n 200 || {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Another sync-from-master run is already in progress. Exiting." | tee -a "$LOGFILE"
  exit 1
}

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOGFILE"; }

if [ ! -f "$CONFIG" ]; then
  log "ERROR: config file not found at $CONFIG"
  exit 1
fi

log "=========================================================="
log "sync-from-master.sh starting (report_only=$REPORT_ONLY prune=$([ -n "$PRUNE" ] && echo yes || echo no) only=${ONLY:-all})"

DRY=""
[ "$REPORT_ONLY" -eq 1 ] && DRY="--dry-run"

TOTAL_ADDED=0
TOTAL_CHANGED=0
TOTAL_DELETED=0

while IFS='|' read -r media master target; do
  # skip comments/blank lines
  case "$media" in
    ''|'#'*) continue ;;
  esac
  [ -n "$ONLY" ] && [ "$media" != "$ONLY" ] && continue

  if [ ! -d "$master" ]; then
    log "SKIP [$media]: master path missing: $master"
    continue
  fi
  mkdir -p "$target"

  log "--- [$media] $master -> $target ---"

  # --itemize-changes gives per-file prefix codes we can tally without a second pass.
  # >f = file transferred (new or changed), *deleting = removed (only appears with --delete).
  OUT=$(rsync -a --checksum --itemize-changes $PRUNE $DRY "$master/" "$target/" 2>&1 | tee -a "$LOGFILE")

  added=$(echo "$OUT" | grep -c '^>f+++++++' || true)
  changed=$(echo "$OUT" | grep -cE '^>f\.' || true)
  deleted=$(echo "$OUT" | grep -c '^\*deleting' || true)

  TOTAL_ADDED=$((TOTAL_ADDED + added))
  TOTAL_CHANGED=$((TOTAL_CHANGED + changed))
  TOTAL_DELETED=$((TOTAL_DELETED + deleted))

  log "[$media] baru: $added | beda/misplaced: $changed | dihapus: $deleted"
done < "$CONFIG"

log "=========================================================="
log "RINGKASAN TOTAL: baru=$TOTAL_ADDED beda/misplaced=$TOTAL_CHANGED dihapus=$TOTAL_DELETED"
[ "$REPORT_ONLY" -eq 1 ] && log "(mode --report-only, tidak ada perubahan nyata dilakukan)"
log "sync-from-master.sh finished."
log "=========================================================="
