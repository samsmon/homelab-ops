#!/usr/bin/env bash
# personal-hosts: create a central shared-postgres and move group-checklist onto it.
# Idempotent where possible. The bundled DB container + volume are only STOPPED, never removed.
# Any mismatch/failure rolls back to the bundled DB. Secrets only in server-side files (600), never printed.
set -uo pipefail
START=$(date +%s); echo "start $(date -u +%FT%TZ)"
PROJ=/opt/projects/shared-postgres
CK=/opt/projects/group-checklist
BK=/var/backups/postgres/cutover
DB=group_checklist
ROLE=group_checklist_app
OLD=group-checklist-db
pq() { docker exec shared-postgres psql -U admin -d "$1" -v ON_ERROR_STOP=1 -tA -c "$2"; }
CNT="select string_agg(format('%s=%s', relname, (xpath('/row/c/text()', query_to_xml(format('select count(*) as c from %I.%I', schemaname, relname), false, true, '')))[1]::text), ',' order by relname) from pg_stat_user_tables"

rb_pre()  { echo "ROLLBACK (pre-change): restarting original app"; docker start $OLD >/dev/null 2>&1; docker start group-checklist >/dev/null 2>&1; }
rb_post() { echo "ROLLBACK (post-change): restoring compose/.env, back to bundled DB"
  cd "$CK"; cp -f docker-compose.yml.pre-central docker-compose.yml; cp -f .env.pre-central .env
  docker start $OLD >/dev/null 2>&1; sleep 6; docker compose up -d --no-build >/dev/null 2>&1; }

echo "## 1 shared-postgres on this host"
mkdir -p "$PROJ" "$BK"; chmod 700 "$BK"
umask 077
[ -f "$PROJ/.env" ] || printf 'POSTGRES_PASSWORD=%s\n' "$(openssl rand -hex 24)" > "$PROJ/.env"
[ -f "$PROJ/.app-creds" ] || printf 'GROUP_CHECKLIST_PW=%s\n' "$(openssl rand -hex 24)" > "$PROJ/.app-creds"
. "$PROJ/.app-creds"
cat > "$PROJ/docker-compose.yml" << 'Y'
services:
  postgres:
    image: postgres:16-alpine
    container_name: shared-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - shared_net
volumes:
  pgdata:
networks:
  shared_net:
    external: true
Y
( cd "$PROJ" && docker compose up -d 2>&1 | tail -3 )
for i in $(seq 1 30); do docker exec shared-postgres pg_isready -U admin >/dev/null 2>&1 && break; sleep 1; done
docker exec shared-postgres pg_isready -U admin || { echo "shared-postgres not ready"; exit 1; }

echo "## 2 role + database (no drops)"
pq postgres "do \$\$ begin if not exists (select 1 from pg_roles where rolname='$ROLE') then create role $ROLE login password '$GROUP_CHECKLIST_PW'; end if; end \$\$" >/dev/null
[ "$(pq postgres "select count(*) from pg_database where datname='$DB'")" = "1" ] || pq postgres "create database $DB owner $ROLE" >/dev/null
pq postgres "revoke connect on database $DB from public" >/dev/null

echo "## 3 backup source, stop app, dump, restore, compare"
docker exec $OLD sh -c 'pg_dump -U "$POSTGRES_USER" -Fc "$POSTGRES_DB"' > "$BK/group_checklist_pre_$(date +%Y%m%d-%H%M%S).dump"
ls -t "$BK"/group_checklist_pre_*.dump | head -1 | xargs -I{} sh -c 'test -s {} && chmod 600 {} && echo "pre-cutover dump $(stat -c %s {}) bytes"' || { echo "dump failed"; exit 1; }
docker stop group-checklist >/dev/null
BEFORE=$(docker exec $OLD sh -c "psql -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\" -tAc \"$CNT\"") || { rb_pre; exit 1; }
echo "tables counted (source): $(echo "$BEFORE" | tr ',' '\n' | wc -l)"
DUMP="$BK/group_checklist_final_$(date +%Y%m%d-%H%M%S).dump"
docker exec $OLD sh -c 'pg_dump -U "$POSTGRES_USER" -Fc "$POSTGRES_DB"' > "$DUMP" && [ -s "$DUMP" ] || { echo "final dump failed"; rb_pre; exit 1; }
chmod 600 "$DUMP"
docker exec -i shared-postgres pg_restore -U admin -d $DB --clean --if-exists --no-owner --no-acl --role=$ROLE < "$DUMP" 2>&1 | tail -5
AFTER=$(docker exec shared-postgres psql -U admin -d $DB -tAc "$CNT")
if [ "$BEFORE" != "$AFTER" ]; then echo "MISMATCH"; echo " src: $BEFORE" | cut -c1-300; echo " dst: $AFTER" | cut -c1-300; rb_pre; exit 1; fi
echo "row counts identical on every table: $BEFORE" | cut -c1-300

echo "## 4 switch group-checklist to shared-postgres"
cd "$CK"; cp -f docker-compose.yml docker-compose.yml.pre-central; cp -f .env .env.pre-central
sed -i "s|^DATABASE_URL=.*|DATABASE_URL=postgresql://$ROLE:$GROUP_CHECKLIST_PW@shared-postgres:5432/$DB?sslmode=disable|" .env
cat > docker-compose.yml << 'Y'
services:
  group-checklist:
    build: .
    container_name: group-checklist
    restart: unless-stopped
    env_file: .env
    ports:
      - "3001:8080"
    networks:
      - default
      - shared_net
networks:
  shared_net:
    external: true
Y
docker compose config -q || { echo "compose invalid"; rb_post; exit 1; }
docker stop $OLD >/dev/null
docker compose up -d --no-build 2>&1 | tail -4
sleep 8

echo "## 5 verify (/health runs SELECT 1 through DATABASE_URL; bundled DB is stopped)"
H=$(curl -s -m 15 -w ' http=%{http_code}' http://127.0.0.1:3001/health)
echo "$H"
echo "app DATABASE_URL host: $(docker exec group-checklist printenv DATABASE_URL | sed -E 's#^[a-z]+://[^@]*@([^/]*)/.*#\1#')"
ROOT=$(curl -s -o /dev/null -m 15 -w '%{http_code}' http://127.0.0.1:3001/); echo "root http=$ROOT"
ERR=$(docker logs --since 2m group-checklist 2>&1 | grep -ciE 'ECONNREFUSED|password authentication|does not exist|\[error\]')
echo "error lines in last 2m: $ERR"
if ! echo "$H" | grep -q '"db":"ok"' || ! echo "$H" | grep -q 'http=200' || [ "$ROOT" != 200 ]; then echo "VERIFY FAILED"; rb_post; exit 1; fi
echo "OK: group-checklist now on shared-postgres. Bundled $OLD stopped (volume kept). Rollback: cd $CK; cp docker-compose.yml.pre-central docker-compose.yml; cp .env.pre-central .env; docker start $OLD; docker compose up -d --no-build"
echo "end $(date -u +%FT%TZ) elapsed $(( $(date +%s)-START ))s"
