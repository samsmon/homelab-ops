#!/usr/bin/env bash
# yado-hosts: move one app from its bundled Postgres to shared-postgres. Usage: pg-cutover.sh sso|malas
# Safe by design: bundled DB + volume are only STOPPED (never removed). Any mismatch/failure rolls back.
# Row counts of EVERY table are compared exactly before/after. Secrets come from .app-creds, never printed.
set -uo pipefail
APP=${1:?usage: pg-cutover.sh sso|malas}
. /opt/projects/shared-postgres/.app-creds
START=$(date +%s); echo "start $(date -u +%FT%TZ)"

case $APP in
  sso)   DIR=/opt/projects/sso.yado; STOP="sso-yado-nginx-1 sso-yado-app-1"; BUNDLED=sso-yado-postgres-1; BUSER=postgres
         DB=db_sso; ROLE=sso_yado; PW=$SSO_YADO_PW; APPC=sso-yado-app-1; URL=http://127.0.0.1:8081/health ;;
  malas) DIR=/opt/projects/malas; STOP="malas-nginx-1 malas-queue-1 malas-app-1"; BUNDLED=malas-db-1; BUSER=admin
         DB=malas; ROLE=malas_app; PW=$MALAS_APP_PW; APPC=malas-app-1; URL=http://127.0.0.1:8082/ ;;
  *) echo "bad app"; exit 2 ;;
esac
BK=/var/backups/postgres/cutover; mkdir -p "$BK"; chmod 700 "$BK"
TS=$(date +%Y%m%d-%H%M%S)
CNT="select string_agg(format('%s=%s', relname, (xpath('/row/c/text()', query_to_xml(format('select count(*) as c from %I.%I', schemaname, relname), false, true, '')))[1]::text), ',' order by relname) from pg_stat_user_tables"

rb_pre()  { echo "ROLLBACK (pre-change): restarting original containers"; docker start $BUNDLED >/dev/null 2>&1; for c in $STOP; do docker start "$c" >/dev/null 2>&1; done; }
rb_post() { echo "ROLLBACK (post-change): restoring env/override, back to bundled DB"
  cd "$DIR"; cp -f .env.pre-central .env; cp -f docker-compose.override.yml.pre-central docker-compose.override.yml 2>/dev/null || rm -f docker-compose.override.yml
  docker start $BUNDLED >/dev/null 2>&1; sleep 8; docker compose --profile bundled-db up -d --no-build >/dev/null 2>&1; }

echo "## 1 fresh backup"; /opt/scripts/pg-backup.sh | tail -6
echo "## 2 stop app containers (bundled DB stays up)"; for c in $STOP; do docker stop "$c" >/dev/null; done
BEFORE=$(docker exec $BUNDLED psql -U $BUSER -d $DB -tAc "$CNT") || { rb_pre; exit 1; }
echo "$BEFORE" | tr ',' '\n' | wc -l | xargs echo "tables counted (source):"
echo "## 3 dump source -> restore into shared-postgres/$DB"
DUMP="$BK/${APP}_pre_cutover_$TS.dump"
docker exec $BUNDLED pg_dump -U $BUSER -Fc $DB > "$DUMP" && [ -s "$DUMP" ] || { echo "dump failed"; rb_pre; exit 1; }
chmod 600 "$DUMP"
docker exec -i shared-postgres pg_restore -U admin -d $DB --clean --if-exists --no-owner --no-acl --role=$ROLE < "$DUMP" 2>&1 | tail -5
AFTER=$(docker exec shared-postgres psql -U admin -d $DB -tAc "$CNT")
if [ "$BEFORE" != "$AFTER" ]; then echo "MISMATCH"; echo " src: $BEFORE" | cut -c1-300; echo " dst: $AFTER" | cut -c1-300; rb_pre; exit 1; fi
echo "row counts identical on every table (source == shared-postgres)"
docker exec shared-postgres psql -U admin -d $DB -tAc "select 'owners: '||string_agg(distinct tableowner,',') from pg_tables where schemaname='public'"

echo "## 4 switch app to shared-postgres"
cd "$DIR"; cp -f .env .env.pre-central; cp -f docker-compose.override.yml docker-compose.override.yml.pre-central 2>/dev/null || true
setenv() { if grep -q "^$1=" .env; then sed -i "s|^$1=.*|$1=$2|" .env; else echo "$1=$2" >> .env; fi; }
setenv DB_HOST shared-postgres; setenv DB_USERNAME $ROLE; setenv DB_PASSWORD $PW
if [ $APP = sso ]; then
  setenv DB_READ_HOST shared-postgres; setenv DB_WRITE_HOST shared-postgres
  cat > docker-compose.override.yml << 'Y'
services:
  postgres:
    profiles: ["bundled-db"]
    restart: unless-stopped
    ports: !reset []
  app:
    restart: unless-stopped
    depends_on: !reset []
    networks: !override [sso, shared_net]
    environment:
      DB_HOST: shared-postgres
      DB_READ_HOST: shared-postgres
      DB_WRITE_HOST: shared-postgres
  nginx:
    restart: unless-stopped
networks:
  shared_net:
    external: true
Y
else
  cat > docker-compose.override.yml << 'Y'
services:
  db:
    profiles: ["bundled-db"]
  app:
    depends_on: !reset []
    networks: !override [default, shared_net]
  queue:
    depends_on: !reset []
    networks: !override [default, shared_net]
networks:
  shared_net:
    external: true
Y
fi
docker compose config -q || { echo "compose config invalid"; rb_post; exit 1; }
docker stop $BUNDLED >/dev/null
docker compose up -d --no-build 2>&1 | tail -6
sleep 15
docker exec $APPC php artisan config:clear >/dev/null 2>&1

echo "## 5 verify"
CODE=$(curl -s -o /dev/null -m 15 -w '%{http_code}' $URL); echo "local $URL -> $CODE"
docker exec $APPC php artisan migrate:status 2>&1 | tail -3
EFF=$(docker exec $APPC php artisan config:show database.connections.pgsql 2>&1)
EFF_USER=$(echo "$EFF" | grep -E '^ *username ' | awk '{print $NF}')
EFF_HOSTS=$(echo "$EFF" | grep -E 'host' | awk '{print $NF}' | sort -u | tr '
' ' ')
docker exec $APPC php artisan migrate:status >/dev/null 2>&1; MIG=$?
echo "effective db user: $EFF_USER | hosts: $EFF_HOSTS | migrate:status exit: $MIG"
case "${CODE:0:1}" in 2|3) HOK=1 ;; *) HOK=0 ;; esac
if [ $HOK = 0 ] || [ "$MIG" != 0 ] || [ "$EFF_USER" != "$ROLE" ] || ! echo "$EFF_HOSTS" | grep -q shared-postgres || echo "$EFF_HOSTS" | grep -qE '(^| )(postgres|db)( |$)'; then echo "VERIFY FAILED"; rb_post; exit 1; fi
CONN=shared-postgres
echo "OK: $APP now on shared-postgres. Bundled $BUNDLED stopped (volume kept). Rollback: cp .env.pre-central .env; cp docker-compose.override.yml.pre-central docker-compose.override.yml; docker start $BUNDLED; docker compose --profile bundled-db up -d --no-build"
END=$(date +%s); echo "end $(date -u +%FT%TZ) elapsed $((END-START))s"
