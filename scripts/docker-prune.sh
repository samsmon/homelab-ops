#!/usr/bin/env bash
# Weekly Docker disk cleanup for small-root LXCs (personal-hosts: / is 15 GB, every `compose up --build` grows build cache).
# Installed at /opt/scripts/docker-prune.sh, run by docker-prune.timer.
# Removes only: build cache unused for >72h (recent cache kept so back-to-back builds stay fast) and dangling images.
# Never touches tagged images (base images golang:1.23-alpine / nginx:alpine, rollback tags *:prev-*), containers or volumes.
# If / is still at or above FORCE_PCT afterwards, all unused build cache is dropped (next build re-downloads layers).
set -uo pipefail

FORCE_PCT=${FORCE_PCT:-80}

use_pct() { df --output=pcent / | tail -1 | tr -dc '0-9'; }

before=$(use_pct)
docker builder prune -a -f --filter until=72h >/dev/null
docker image prune -f >/dev/null
after=$(use_pct)

if [ "$after" -ge "$FORCE_PCT" ]; then
  docker builder prune -a -f >/dev/null
  after=$(use_pct)
  echo "docker-prune: / ${before}% -> ${after}% (forced full builder prune, threshold ${FORCE_PCT}%)"
else
  echo "docker-prune: / ${before}% -> ${after}%"
fi

if [ "$after" -ge "$FORCE_PCT" ]; then
  echo "docker-prune: WARNING / still ${after}% after prune; check images (rollback tags *:prev-*) and journal" >&2
  exit 1
fi
