#!/usr/bin/env bash
# Weekly TRIM of every running LXC rootfs on the Proxmox host (pve).
# Installed at /opt/scripts/pct-fstrim.sh, run by pct-fstrim.timer.
# Why: the stock fstrim.timer only trims host mounts, not LXC rootfs. Blocks freed inside an LXC (docker prune, rmi, logs)
# stay allocated in the LVM thin pool `data` until trimmed, so the pool filled to 100% while LXC `df` showed free space.
# Only issues discards (pct fstrim); no data, container or config is touched.
set -uo pipefail

fail=0
start=$(date +%s)
for id in $(pct list | awk 'NR>1 && $2=="running" {print $1}'); do
  t=$(date +%s)
  if out=$(timeout 600 pct fstrim "$id" 2>&1); then
    logger -t pct-fstrim "LXC $id ok ($(( $(date +%s)-t ))s): $(echo "$out" | tail -1)"
  else
    logger -t pct-fstrim -p user.err "LXC $id FAILED: $(echo "$out" | tail -1)"
    fail=1
  fi
done

pool=$(lvs --noheadings -o data_percent pve/data 2>/dev/null | tr -d ' ')
logger -t pct-fstrim "done in $(( $(date +%s)-start ))s, thin pool data ${pool:-?}%"
echo "pct-fstrim: pool data ${pool:-?}%"
exit "$fail"
