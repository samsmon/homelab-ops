#!/bin/bash
# Standby rescue script for hdd-music (WD Green 2TB, sdd1) — see CHANGELOG.md (55)/(56).
# Drive is intermittently unreadable (likely controller-board fault, not cable).
# Run this the moment /mnt/hdd-music becomes readable again, to grab as much
# of the 717GB music library onto /mnt/hdd-cloud (763GB free) as possible
# before it drops again. Safe to re-run — rsync resumes/skips completed files.
#
# Usage (on docker-host):
#   bash scripts/emergency-music-rescue.sh

set -uo pipefail  # no -e: a single file read error must not abort the whole rescue

SRC="/mnt/hdd-music/jellyfin/music"
DEST="/mnt/hdd-cloud/music-rescue"
LOG="/var/log/music-rescue.log"

mkdir -p "$DEST"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting rescue rsync: $SRC -> $DEST" | tee -a "$LOG"

rsync -avh --info=progress2 --partial --inplace \
  --log-file="$LOG" \
  "$SRC/" "$DEST/"

RC=$?
echo "[$(date '+%Y-%m-%d %H:%M:%S')] rsync exited with code $RC (0=complete, 23/24=partial due to vanished/errored files — re-run to resume)" | tee -a "$LOG"
du -sh "$DEST" | tee -a "$LOG"
