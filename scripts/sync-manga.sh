#!/bin/bash
# sync-manga.sh — Two jobs in one script:
#   1) Convert freshly-downloaded raw-image manga folders (nhdl-style) into .cbz archives.
#   2) Sync the manga-raw master (hdd-backup) to hdd-media, where manga-optimizer.py watches
#      for new files and generates the WebP-optimized manga-reader library that Komga reads.
#      This script does NOT do any WebP conversion itself — that's manga-optimizer.py's job,
#      running as its own watchdog daemon on hdd-media.
#
# Inbox layout expected for the convert step (matches nhdl's default output):
#   <INBOX>/Japanese/<Artist>/<Title>/*.webp|*.jpg|*.png   -> converted, then merged as .cbz
#   <INBOX>/English/<Artist>/<Title>/*.webp|*.jpg|*.png    -> converted, then merged as .cbz
#   <INBOX>/Japanese/<Artist>/<Title>.cbz                  -> merged as-is (already archived)
#   <INBOX>/English/<Artist>/<Title>.cbz                   -> merged as-is
#
# Skip/replace behavior for both the inbox merge and the master->media sync: rsync --checksum,
# so a destination file whose content already matches is left alone, and a destination file
# that's missing, different, or corrupt (e.g. a saved HTML error page from a failed past
# download — this is what most "broken duplicates" turned out to be on 2026-09-23) gets
# replaced. Nothing is deleted unless --prune is passed to the sync step.
#
# Usage:
#   bash scripts/sync-manga.sh                    # convert inbox + merge into master + sync to
#                                                  #   hdd-media + audit summary (full run)
#   bash scripts/sync-manga.sh --convert-only      # only convert raw inbox folders to .cbz
#   bash scripts/sync-manga.sh --merge-only        # only merge inbox .cbz into MASTER_DIR
#   bash scripts/sync-manga.sh --sync-only         # only sync MASTER_DIR -> MEDIA_DIR (no inbox)
#   bash scripts/sync-manga.sh --audit-only        # only scan MASTER_DIR for broken (HTML-stub)
#                                                  #   .cbz files, report count, no changes
#   bash scripts/sync-manga.sh --prune             # let the sync step delete on MEDIA_DIR
#                                                  #   anything no longer on MASTER_DIR
#   bash scripts/sync-manga.sh --dry-run           # preview merge/sync only, no writes (convert
#                                                  #   step still runs for real - archiving isn't
#                                                  #   destructive to content, just packaging)
#   bash scripts/sync-manga.sh --inbox /path       # override inbox location

set -uo pipefail

LOCKFILE="/var/run/sync-manga.lock"
LOGFILE="/var/log/sync-manga.log"

INBOX_DIR="/mnt/hdd-media/download"
MASTER_DIR="/mnt/hdd-backup/manga-raw"
MEDIA_DIR="/mnt/hdd-media/manga-raw"

DO_CONVERT=1
DO_MERGE=1
DO_SYNC=1
DO_AUDIT=1
DRY_RUN=""
PRUNE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --convert-only) DO_MERGE=0; DO_SYNC=0; DO_AUDIT=0 ;;
    --merge-only)   DO_CONVERT=0; DO_SYNC=0; DO_AUDIT=0 ;;
    --sync-only)    DO_CONVERT=0; DO_MERGE=0; DO_AUDIT=0 ;;
    --audit-only)   DO_CONVERT=0; DO_MERGE=0; DO_SYNC=0 ;;
    --prune)        PRUNE="--delete" ;;
    --dry-run|-n)   DRY_RUN="--dry-run" ;;
    --inbox)        shift; INBOX_DIR="$1" ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--convert-only|--merge-only|--sync-only|--audit-only] [--prune] [--inbox <path>] [--dry-run]"
      exit 1
      ;;
  esac
  shift
done

exec 200>"$LOCKFILE"
flock -n 200 || {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Another manga sync process is already running. Exiting." | tee -a "$LOGFILE"
  exit 1
}

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOGFILE"; }

log "=========================================================="
log "sync-manga.sh starting (convert=$DO_CONVERT merge=$DO_MERGE sync=$DO_SYNC audit=$DO_AUDIT)"
log "Inbox: $INBOX_DIR | Master: $MASTER_DIR | Media(Komga): $MEDIA_DIR"

# --- Step 1: convert raw title folders (in the inbox) into .cbz --------------------------
convert_lang() {
  local lang_dir="$1"
  [ -d "$lang_dir" ] || return 0
  find "$lang_dir" -mindepth 2 -maxdepth 2 -type d | while IFS= read -r dir; do
    local parent name cbz
    parent=$(dirname "$dir")
    name=$(basename "$dir")
    cbz="$parent/$name.cbz"
    if [ -f "$cbz" ]; then
      echo "SKIP (cbz sudah ada): $dir" >> "$LOGFILE"
      continue
    fi
    (cd "$dir" && zip -0 -r -q "$cbz" .) 2>> "$LOGFILE"
    if [ -f "$cbz" ] && unzip -tq "$cbz" > /dev/null 2>&1; then
      rm -rf "$dir"
      echo "OK: $dir" >> "$LOGFILE"
    else
      echo "GAGAL verifikasi, folder asli dipertahankan: $dir" >> "$LOGFILE"
      rm -f "$cbz"
    fi
  done
}

if [ "$DO_CONVERT" -eq 1 ]; then
  log "Step 1: converting raw inbox folders to .cbz..."
  convert_lang "$INBOX_DIR/Japanese"
  convert_lang "$INBOX_DIR/English"
  log "Step 1 done. See $LOGFILE for per-title OK/SKIP/GAGAL detail."
fi

# --- Step 2: merge inbox .cbz into the master archive (hdd-backup) -----------------------
if [ "$DO_MERGE" -eq 1 ]; then
  log "Step 2: merging inbox into $MASTER_DIR/nsfw/{JP,Unofficial}..."
  if [ -d "$INBOX_DIR/Japanese" ]; then
    mkdir -p "$MASTER_DIR/nsfw/JP"
    rsync -avh --checksum $DRY_RUN --log-file="$LOGFILE" "$INBOX_DIR/Japanese/" "$MASTER_DIR/nsfw/JP/"
  fi
  if [ -d "$INBOX_DIR/English" ]; then
    mkdir -p "$MASTER_DIR/nsfw/Unofficial"
    rsync -avh --checksum $DRY_RUN --log-file="$LOGFILE" "$INBOX_DIR/English/" "$MASTER_DIR/nsfw/Unofficial/"
  fi
  if [ -z "$DRY_RUN" ]; then
    rm -rf "$INBOX_DIR/Japanese" "$INBOX_DIR/English"
    log "Inbox Japanese/English folders removed after successful merge into master."
  fi
  log "Step 2 done."
fi

# --- Step 3: sync master (hdd-backup) -> hdd-media, where manga-optimizer.py picks it up --
if [ "$DO_SYNC" -eq 1 ]; then
  log "Step 3: syncing $MASTER_DIR -> $MEDIA_DIR (manga-optimizer.py watches this path)..."
  mkdir -p "$MEDIA_DIR"
  rsync -avh --checksum $PRUNE $DRY_RUN --log-file="$LOGFILE" "$MASTER_DIR/" "$MEDIA_DIR/"
  log "Step 3 done."
fi

# --- Step 4: audit master for broken (HTML-stub) .cbz files ------------------------------
audit_dir() {
  local dir="$1" label="$2"
  [ -d "$dir" ] || return 0
  local broken=0 total=0
  while IFS= read -r f; do
    total=$((total+1))
    if file -b "$f" 2>/dev/null | grep -q HTML; then
      broken=$((broken+1))
      echo "BROKEN: $f" >> "$LOGFILE"
    fi
  done < <(find "$dir" -iname "*.cbz" -not -iname "*.nhdl-id")
  log "$label: $broken broken / $total total .cbz files"
}

if [ "$DO_AUDIT" -eq 1 ]; then
  log "Step 4: auditing master for broken (HTML-stub) archives..."
  audit_dir "$MASTER_DIR/nsfw/JP" "JP"
  audit_dir "$MASTER_DIR/nsfw/Unofficial" "Unofficial"
  log "Step 4 done. See BROKEN: lines above (this run) in $LOGFILE for exact paths still needing re-download."
fi

log "sync-manga.sh finished."
log "=========================================================="
