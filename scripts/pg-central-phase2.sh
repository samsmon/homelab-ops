#!/usr/bin/env bash
# yado-hosts: prepare shared-postgres for app databases (idempotent, NO drops).
# - restore-tests the latest malas dump into a scratch DB
# - creates roles sso_yado / malas_app, hands the existing EMPTY db_sso / malas to them
# Passwords are generated once into /opt/projects/shared-postgres/.app-creds (root-only, never in repo).
set -euo pipefail
pq() { docker exec shared-postgres psql -U admin -d "$1" -v ON_ERROR_STOP=1 -tA -c "$2"; }

echo "## restore test (latest malas dump -> scratch db)"
D=$(ls -t /var/backups/postgres/malas-db-1/malas_*.dump | head -1)
pq postgres "drop database if exists restore_test" >/dev/null
pq postgres "create database restore_test" >/dev/null
docker exec -i shared-postgres pg_restore -U admin -d restore_test --no-owner --no-acl < "$D"
pq restore_test "select 'volumes='||(select count(*) from volumes)||' series='||(select count(*) from series)||' collections='||(select count(*) from collections)||' users='||(select count(*) from users)"
pq postgres "drop database restore_test" >/dev/null

echo "## guard: target DBs must be empty"
for d in db_sso malas; do
  n=$(pq "$d" "select count(*) from pg_stat_user_tables"); echo "$d user tables: $n"
  [ "$n" = "0" ] || { echo "ABORT: $d not empty"; exit 1; }
done

echo "## roles + ownership"
CF=/opt/projects/shared-postgres/.app-creds
umask 077
[ -f "$CF" ] || printf 'SSO_YADO_PW=%s\nMALAS_APP_PW=%s\n' "$(openssl rand -hex 24)" "$(openssl rand -hex 24)" > "$CF"
. "$CF"
pq postgres "do \$\$ begin
  if not exists (select 1 from pg_roles where rolname='sso_yado') then create role sso_yado login password '$SSO_YADO_PW'; end if;
  if not exists (select 1 from pg_roles where rolname='malas_app') then create role malas_app login password '$MALAS_APP_PW'; end if;
end \$\$" >/dev/null
pq postgres "alter database db_sso owner to sso_yado" >/dev/null
pq postgres "alter database malas owner to malas_app" >/dev/null
pq postgres "revoke connect on database db_sso from public" >/dev/null
pq postgres "revoke connect on database malas from public" >/dev/null

echo "## verify"
pq postgres "select datname||' owner='||pg_get_userbyid(datdba) from pg_database where datname in ('db_sso','malas') order by 1"
ls -l "$CF" | awk '{print $1, $3, $9}'
docker exec -e PGPASSWORD="$SSO_YADO_PW" shared-postgres psql -h 127.0.0.1 -U sso_yado -d db_sso -tAc "select 'sso_yado->db_sso login ok'"
docker exec -e PGPASSWORD="$MALAS_APP_PW" shared-postgres psql -h 127.0.0.1 -U malas_app -d malas -tAc "select 'malas_app->malas login ok'"
if docker exec -e PGPASSWORD="$SSO_YADO_PW" shared-postgres psql -h 127.0.0.1 -U sso_yado -d malas -tAc "select 1" >/dev/null 2>&1; then echo "WARN: cross-db access allowed"; else echo "cross-db access denied (good)"; fi
