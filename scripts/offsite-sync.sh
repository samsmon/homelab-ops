#!/usr/bin/env bash
# Push local backups to docker-host:/mnt/hdd-backup/offsite/<this host>/ via a write-only rrsync key.
# Installed at /opt/scripts/offsite-sync.sh, run by offsite-sync.timer (after pg-backup.timer).
# - /var/backups/postgres/ (except cutover/)           -> postgres/
# - Docker volumes listed in /opt/scripts/offsite-volumes.list (one name per line) -> volumes/
# - last-success marker (only written when everything succeeded)
# Retention on the receiver is handled by offsite-rotate.sh on docker-host (the key cannot delete).
set -uo pipefail

DEST=backup-recv@192.168.18.225
KEY=/root/.ssh/offsite_ed25519
SSH="ssh -i $KEY -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=15"
LIST=/opt/scripts/offsite-volumes.list
VOLDIR=/var/backups/volumes
ts=$(date +%Y%m%d-%H%M%S)
fail=0
echo "start $(date -u +%FT%TZ)"

rsync -a --mkpath -e "$SSH" --exclude 'cutover/' /var/backups/postgres/ "$DEST:postgres/" || { echo "FAIL postgres rsync"; fail=1; }

if [ -f "$LIST" ]; then
  umask 077; mkdir -p "$VOLDIR"
  while read -r v; do
    case "$v" in ''|\#*) continue ;; esac
    out="$VOLDIR/${v}_${ts}.tgz"
    if docker run --rm -v "$v":/v:ro -v "$VOLDIR":/out alpine tar czf "/out/$(basename "$out")" -C /v . && [ -s "$out" ]; then
      echo "ok tar $v $(stat -c %s "$out") bytes"
    else
      rm -f "$out"; echo "FAIL tar $v"; fail=1
    fi
  done < "$LIST"
  rsync -a --mkpath -e "$SSH" "$VOLDIR/" "$DEST:volumes/" || { echo "FAIL volumes rsync"; fail=1; }
  find "$VOLDIR" -name '*.tgz' -mtime +3 -delete
fi

if [ $fail = 0 ]; then
  m=$(mktemp); date -u +%FT%TZ > "$m"
  rsync -a -e "$SSH" "$m" "$DEST:last-success" && echo "marker written" || { echo "FAIL marker"; fail=1; }
  rm -f "$m"
fi
echo "end $(date -u +%FT%TZ) fail=$fail"
exit $fail
