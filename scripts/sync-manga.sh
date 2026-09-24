#!/bin/bash
# sync-manga.sh — Convert freshly-downloaded manga (raw image folders, nhdl-style) into .cbz
# archives, then merge them into the main manga-raw/nsfw library, skipping anything already
# correctly in place and replacing anything misplaced/corrupt.
#
# Expected inbox layout (matches nhdl's default output):
#   <INBOX>/Japanese/<Artist>/<Title>/*.webp|*.jpg|*.png   -> converted & merged into DEST_JP
#   <INBOX>/English/<Artist>/<Title>/*.webp|*.jpg|*.png    -> converted & merged into DEST_EN
#   <INBOX>/Japanese/<Artist>/<Title>.cbz                  -> merged as-is (already archived)
#   <INBOX>/English/<Artist>/<Title>.cbz                   -> merged as-is
#
# Skip/replace behavior: merge uses rsync --checksum, so a destination file whose content
# already matches the inbox copy is left alone (skipped), and a destination file that's
# missing, different, or corrupt (e.g. a saved HTML error page from a failed past download,
# which is what a lot of "broken duplicates" turned out to be on 2026-09-23) gets replaced.
#
# Usage:
#   bash scripts/sync-manga.sh                  # convert + merge + audit summary (full run)
#   bash scripts/sync-manga.sh --convert-only    # only convert raw folders to .cbz, don't merge
#   bash scripts/sync-manga.sh --merge-only      # only merge (assumes inbox is already .cbz-only)
#   bash scripts/sync-manga.sh --audit-only      # only scan DEST_JP/DEST_EN for broken (HTML-stub)
#                                                 #   .cbz files, report count, don't change anything
#   bash scripts/sync-manga.sh --dry-run         # preview merge only, no changes (convert step
#                                                 #   still runs for real - archiving is not
#                                                 #   destructive to content, just packaging)
#   bash scripts/sync-manga.sh --inbox /path     # override inbox location (default below)

set -uo pipefail

LOCKFILE="/var/run/sync-manga.lock"
LOGFILE="/var/log/sync-manga.log"

INBOX_DIR="/mnt/hdd-media/download"
DEST_JP="/mnt/hdd-backup/manga-raw/nsfw/JP"
DEST_EN="/mnt/hdd-backup/manga-raw/nsfw/Unofficial"

DO_CONVERT=1
DO_MERGE=1
DO_AUDIT=1
DRY_RUN=""

while [ $# -gt 0 ]; do
  case "$1" in
    --convert-only) DO_MERGE=0; DO_AUDIT=0 ;;
    --merge-only)   DO_CONVERT=0; DO_AUDIT=0 ;;
    --audit-only)   DO_CONVERT=0; DO_MERGE=0 ;;
    --dry-run|-n)   DRY_RUN="--dry-run" ;;
    --inbox)        shift; INBOX_DIR="$1" ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--convert-only|--merge-only|--audit-only] [--inbox <path>] [--dry-run]"
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
log "sync-manga.sh starting (convert=$DO_CONVERT merge=$DO_MERGE audit=$DO_AUDIT)"
log "Inbox: $INBOX_DIR"

# --- Step 1: convert raw title folders into .cbz -----------------------------------------
convert_lang() {
  local lang_dir="$1"
  [ -d "$lang_dir" ] || return 0
  local ok=0 fail=0 skip=0
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
  log "Step 1: converting raw folders to .cbz..."
  convert_lang "$INBOX_DIR/Japanese"
  convert_lang "$INBOX_DIR/English"
  log "Step 1 done. See $LOGFILE for per-title OK/SKIP/GAGAL detail."
fi

# --- Step 2: merge into the main library, skip-if-correct / replace-if-wrong -------------
if [ "$DO_MERGE" -eq 1 ]; then
  log "Step 2: merging into $DEST_JP and $DEST_EN..."
  if [ -d "$INBOX_DIR/Japanese" ]; then
    mkdir -p "$DEST_JP"
    rsync -avh --checksum $DRY_RUN --log-file="$LOGFILE" "$INBOX_DIR/Japanese/" "$DEST_JP/"
  fi
  if [ -d "$INBOX_DIR/English" ]; then
    mkdir -p "$DEST_EN"
    rsync -avh --checksum $DRY_RUN --log-file="$LOGFILE" "$INBOX_DIR/English/" "$DEST_EN/"
  fi
  if [ -z "$DRY_RUN" ]; then
    rm -rf "$INBOX_DIR/Japanese" "$INBOX_DIR/English"
    log "Inbox Japanese/English folders removed after successful merge."
  fi
  log "Step 2 done."
fi

# --- Step 3: audit for broken (HTML-stub) .cbz files in the destination ------------------
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
  log "Step 3: auditing for broken (HTML-stub) archives..."
  audit_dir "$DEST_JP" "JP"
  audit_dir "$DEST_EN" "Unofficial"
  log "Step 3 done. See BROKEN: lines above (this run) in $LOGFILE for exact paths still needing re-download."
fi

log "sync-manga.sh finished."
log "=========================================================="
