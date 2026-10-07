#!/usr/bin/env bash
# docker-host: prune /mnt/hdd-backup/offsite (14 days) and fail loudly if a source host went stale.
# Installed at /usr/local/bin/offsite-rotate.sh, run daily by offsite-rotate.timer.
# The receiving key is write-only, so rotation MUST happen here, not on the senders.
set -uo pipefail
ROOT=/mnt/hdd-backup/offsite
KEEP_DAYS=14
STALE_HOURS=36
rc=0

n=$(find "$ROOT" -type f \( -name '*.dump' -o -name '*.tgz' \) -mtime +"$KEEP_DAYS" -print -delete | wc -l)
echo "rotated: $n file(s) older than $KEEP_DAYS days removed"

for d in "$ROOT"/*/; do
  h=$(basename "$d"); m="$d/last-success"
  if [ ! -f "$m" ]; then echo "STALE $h: no last-success marker"; rc=1; continue; fi
  age=$(( ( $(date +%s) - $(stat -c %Y "$m") ) / 3600 ))
  if [ "$age" -gt "$STALE_HOURS" ]; then echo "STALE $h: last success ${age}h ago"; rc=1; else echo "ok $h: last success ${age}h ago"; fi
done
exit $rc
