#!/bin/bash
# Daily read-stress test for hdd-backup (WD Green), monitoring whether UDMA_CRC_Error_Count
# stays flat after the 2026-09-22 power cable swap (splitter -> dedicated single-lane cable).
# Self-removes from cron after 7 runs. See docs/decisions.md for context.
set -uo pipefail

MOUNT=/mnt/hdd-backup
LOGFILE=/var/log/hdd-backup-daily-test.log
COUNTFILE=/var/lib/hdd-backup-daily-test.count
CRONFILE=/etc/cron.d/hdd-backup-daily-test

DEV=$(findmnt -n -o SOURCE "$MOUNT" | sed -E 's/[0-9]+$//')
if [ -z "$DEV" ]; then
  echo "$(date): ERROR - $MOUNT not mounted, skipping run" >> "$LOGFILE"
  exit 1
fi

RUN=$(( $(cat "$COUNTFILE" 2>/dev/null || echo 0) + 1 ))

{
  echo "===== $(date) - Run $RUN/7 START ====="
  echo "Device: $DEV"
  BEFORE=$(smartctl -A "$DEV" 2>/dev/null | grep -i UDMA_CRC | awk '{print $NF}')
  echo "UDMA_CRC_Error_Count before: $BEFORE"

  # Fase 1: ~12 menit scan random + streaming bareng
  END=$(( $(date +%s) + 720 ))
  while [ "$(date +%s)" -lt "$END" ]; do
    find "$MOUNT/music" -iname "*.flac" -size +50M 2>/dev/null | shuf -n 2 | xargs -I{} dd if={} of=/dev/null bs=1M 2>/dev/null
    find "$MOUNT/music" -type f 2>/dev/null | shuf -n 300 | xargs -I{} md5sum {} > /dev/null 2>&1
  done
  echo "Fase 1 (scan+stream) selesai: $(date)"

  # Fase 2: ~1 jam simulasi puter musik beneran — baca satu file per satu dengan rate
  # dibatasi (pv -L) kira-kira sekitar bitrate FLAC hi-res (~800KB/s), jadi durasi baca
  # tiap file kurang lebih sama kayak durasi lagu aslinya, bukan burst-read-lalu-jeda.
  END2=$(( $(date +%s) + 3600 ))
  while [ "$(date +%s)" -lt "$END2" ]; do
    FILE=$(find "$MOUNT/music" -iname "*.flac" 2>/dev/null | shuf -n 1)
    if [ -n "$FILE" ]; then
      echo "  now playing: $FILE"
      pv -q -L 800k "$FILE" > /dev/null 2>/dev/null
    fi
  done
  echo "Fase 2 (simulasi playback throttled) selesai: $(date)"

  AFTER=$(smartctl -A "$DEV" 2>/dev/null | grep -i UDMA_CRC | awk '{print $NF}')
  echo "UDMA_CRC_Error_Count after: $AFTER"
  if [ "$BEFORE" != "$AFTER" ]; then
    echo "!!! PERINGATAN: UDMA_CRC_Error_Count NAIK dari $BEFORE ke $AFTER !!!"
  fi
  echo "===== $(date) - Run $RUN/7 DONE ====="
  echo
} >> "$LOGFILE" 2>&1

echo "$RUN" > "$COUNTFILE"

if [ "$RUN" -ge 7 ]; then
  echo "$(date): 7 run selesai, self-removing cron job" >> "$LOGFILE"
  rm -f "$CRONFILE"
fi
