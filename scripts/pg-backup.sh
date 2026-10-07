#!/usr/bin/env bash
# Daily logical backup of every Postgres container on yado-hosts (pg_dump -Fc per database).
# Installed at /opt/scripts/pg-backup.sh, run by pg-backup.timer. Retention: 7 days.
# Container list is "container:superuser"; missing containers are skipped, so removing a
# bundled DB after migration needs no script change.
set -uo pipefail

DEST=/var/backups/postgres
KEEP_DAYS=7
TARGETS=(
  "shared-postgres:admin"
  "malas-db-1:admin"
  "sso-yado-postgres-1:postgres"
)

ts=$(date +%Y%m%d-%H%M%S)
fail=0
umask 077
mkdir -p "$DEST"

for t in "${TARGETS[@]}"; do
  c=${t%%:*}; u=${t##*:}
  if ! docker inspect -f '{{.State.Running}}' "$c" 2>/dev/null | grep -q true; then
    echo "skip $c (not running)"; continue
  fi
  mkdir -p "$DEST/$c"
  dbs=$(docker exec "$c" psql -U "$u" -d postgres -tAc "select datname from pg_database where not datistemplate and datname<>'postgres'") || { echo "FAIL list dbs on $c"; fail=1; continue; }
  for db in $dbs; do
    out="$DEST/$c/${db}_${ts}.dump"
    if docker exec "$c" pg_dump -U "$u" -Fc "$db" > "$out.tmp" && [ -s "$out.tmp" ]; then
      mv "$out.tmp" "$out"; echo "ok $c/$db $(stat -c %s "$out") bytes"
    else
      rm -f "$out.tmp"; echo "FAIL $c/$db"; fail=1
    fi
  done
done

find "$DEST" -name '*.dump' -mtime +"$KEEP_DAYS" -delete
exit $fail
