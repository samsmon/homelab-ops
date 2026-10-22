#!/usr/bin/env bash
# Telegram alert for the Proxmox LVM thin pool `pve/data` (pve host), so it never silently fills to 100% again.
# Installed at /opt/scripts/pool-alert.sh, run every 15 min by pool-alert.timer.
# Credentials: /etc/pool-alert.env (root:root 0600, NOT in the repo) with TG_TOKEN= and TG_CHAT=. Empty/missing = journal only.
# Levels: warn at data >= WARN_PCT (85) or metadata >= META_WARN_PCT (70); crit at data >= CRIT_PCT (92).
# Sends on level change, repeats every REPEAT_SEC (24h) while not ok, and once on recovery. Exits 1 on crit so the unit shows in `systemctl --failed`.
# Usage: pool-alert.sh [--test]   (--test sends one test message and exits)
set -uo pipefail
export LC_ALL=C

ENV_FILE=${ENV_FILE:-/etc/pool-alert.env}
[ -r "$ENV_FILE" ] && . "$ENV_FILE"
STATE_DIR=${STATE_DIR:-/var/lib/pool-alert}
POOL=${POOL:-pve/data}
WARN_PCT=${WARN_PCT:-85}
CRIT_PCT=${CRIT_PCT:-92}
META_WARN_PCT=${META_WARN_PCT:-70}
REPEAT_SEC=${REPEAT_SEC:-86400}
TG_TOKEN=${TG_TOKEN:-}
TG_CHAT=${TG_CHAT:-}

log() { logger -t pool-alert "$*"; echo "pool-alert: $*"; }

send() {
  if [ -z "$TG_TOKEN" ] || [ -z "$TG_CHAT" ]; then
    log "Telegram not configured ($ENV_FILE empty), message only in journal"
    return 1
  fi
  local code
  # token goes through stdin config so it never appears in `ps`
  code=$(printf 'url = "https://api.telegram.org/bot%s/sendMessage"\n' "$TG_TOKEN" \
    | curl -sS --max-time 15 -K - --data-urlencode "chat_id=$TG_CHAT" --data-urlencode "text=$1" \
        -o /dev/null -w '%{http_code}' 2>/dev/null)
  if [ "$code" = "200" ]; then return 0; fi
  log "Telegram send failed (HTTP ${code:-none})"
  return 1
}

if [ "${1:-}" = "--test" ]; then
  if send "pool-alert test dari $(hostname): kanal Telegram berfungsi."; then log "test message sent"; exit 0; fi
  exit 1
fi

read -r data meta size < <(lvs --noheadings --nosuffix --units g -o data_percent,metadata_percent,lv_size "$POOL" 2>/dev/null | awk '{print $1, $2, $3}')
if [ -z "${data:-}" ]; then log "cannot read $POOL via lvs"; exit 2; fi

d=${data%.*}; m=${meta%.*}
level=ok
[ "$d" -ge "$WARN_PCT" ] || [ "$m" -ge "$META_WARN_PCT" ] && level=warn
[ "$d" -ge "$CRIT_PCT" ] && level=crit
free=$(awk -v s="$size" -v p="$data" 'BEGIN{printf "%.0f", s*(100-p)/100}')

mkdir -p "$STATE_DIR"
prev=ok; last=0
[ -r "$STATE_DIR/state" ] && read -r prev last < "$STATE_DIR/state"
now=$(date +%s)

summary="thin pool $POOL: data ${data}% (sisa ~${free} GB dari ${size%.*} GB), metadata ${meta}%"
action=none
if [ "$level" != ok ]; then
  if [ "$level" != "$prev" ] || [ $(( now - last )) -ge "$REPEAT_SEC" ]; then action=alert; fi
elif [ "$prev" != ok ]; then
  action=recover
fi

case $action in
  alert)
    tag=$([ "$level" = crit ] && echo "KRITIS" || echo "PERINGATAN")
    log "$tag $summary"
    if send "[$tag] pve $summary. Langkah awal: systemctl start pct-fstrim.service di pve, lalu cek docker prune di LXC."; then
      echo "$level $now" > "$STATE_DIR/state"
    fi ;;
  recover)
    log "PULIH $summary"
    if send "[PULIH] pve $summary."; then echo "ok $now" > "$STATE_DIR/state"; fi ;;
  none)
    [ "$level" = ok ] && echo "ok $now" > "$STATE_DIR/state"
    log "$level $summary" ;;
esac

[ "$level" = crit ] && exit 1
exit 0
