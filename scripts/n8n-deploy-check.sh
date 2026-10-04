#!/bin/bash
# Per-project auto-deploy check, called over SSH by the n8n "auto-deploy" workflow.
#
# Usage: n8n-deploy-check.sh <project> [--apply]
#   (default)  dry-run: fetch + report only, never pulls or builds
#   --apply    pull --ff-only and `docker compose up -d --build` when safe
#
# Prints exactly one JSON line on stdout:
#   {"project","branch","behind","dirty","busy","action","detail"}
# action: uptodate | would-deploy | deployed | skip-dirty | skip-branch | skip-busy | skip-locked | error
#
# Safety: a project is only deployed when it is on main, has no tracked local
# changes, is fast-forwardable, and (for gddl/nhdl) has no download in progress.
# gamdl-dashboard is deliberately not handled here (excluded by decision).

set -uo pipefail

PROJECTS_ROOT="${PROJECTS_ROOT:-/opt/projects}"
BRANCH="main"
PROJECT="${1:-}"
APPLY=0
[ "${2:-}" = "--apply" ] && APPLY=1

emit() { # action detail
  printf '{"project":"%s","branch":"%s","behind":%s,"dirty":%s,"busy":%s,"action":"%s","detail":"%s"}\n' \
    "$PROJECT" "${CUR_BRANCH:-}" "${BEHIND:-0}" "${DIRTY:-0}" "${BUSY:-false}" "$1" "${2//\"/\'}"
}

[ -n "$PROJECT" ] && [[ "$PROJECT" =~ ^[A-Za-z0-9._-]+$ ]] || { emit error "bad project name"; exit 1; }
DIR="$PROJECTS_ROOT/$PROJECT"
[ -d "$DIR/.git" ] || { emit error "not a git repo: $DIR"; exit 1; }

# One run per project at a time.
exec 9>"/tmp/n8n-deploy-$PROJECT.lock"
flock -n 9 || { emit skip-locked "another run in progress"; exit 0; }

cd "$DIR" || exit 1

# Is a download in progress? Echoes "true"/"false". Unknown -> "true" (fail safe).
is_busy() {
  case "$PROJECT" in
    nhdl)
      local st
      st=$(curl -s -m 5 http://localhost:8098/api/status | sed -n 's/.*"engineStatus":"\([A-Z_]*\)".*/\1/p')
      case "$st" in
        PAUSED|IDLE|STOPPED) echo false ;;
        *) echo true ;; # RUNNING, COOLDOWN, empty/unreachable, anything unexpected
      esac ;;
    gddl)
      local f=/opt/projects/gddl/config/downloads.json
      if [ ! -r "$f" ]; then echo true; return; fi
      if grep -q -E '"status": *"(downloading|compressing|moving)"' "$f"; then echo true; return; fi
      # file touched in the last 2 min => something is still writing state
      if [ -n "$(find "$f" -mmin -2 2>/dev/null)" ]; then echo true; return; fi
      echo false ;;
    *) echo false ;;
  esac
}

if ! git fetch --quiet origin "$BRANCH" 2>/dev/null; then emit error "git fetch failed"; exit 0; fi

CUR_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BEHIND=$(git rev-list --count "HEAD..origin/$BRANCH" 2>/dev/null || echo 0)
DIRTY=$(git status --porcelain --untracked-files=no | wc -l)
BUSY=false

if [ "$BEHIND" -eq 0 ]; then emit uptodate ""; exit 0; fi
if [ "$CUR_BRANCH" != "$BRANCH" ]; then emit skip-branch "on $CUR_BRANCH, not $BRANCH"; exit 0; fi
if [ "$DIRTY" -gt 0 ]; then emit skip-dirty "$DIRTY tracked file(s) modified locally"; exit 0; fi

BUSY=$(is_busy)
if [ "$BUSY" = "true" ]; then emit skip-busy "download in progress or status unknown; retry next cycle"; exit 0; fi

NEW=$(git rev-parse --short "origin/$BRANCH")
if [ "$APPLY" -ne 1 ]; then emit would-deploy "behind $BEHIND -> $NEW"; exit 0; fi

if ! git merge --ff-only --quiet "origin/$BRANCH" 2>/dev/null; then emit error "ff-only merge failed"; exit 0; fi
if ls docker-compose.yml docker-compose.yaml compose.yml compose.yaml >/dev/null 2>&1; then
  if docker compose up -d --build >/tmp/n8n-deploy-"$PROJECT".log 2>&1; then
    emit deployed "now at $NEW"
  else
    emit error "compose up failed, see /tmp/n8n-deploy-$PROJECT.log"
  fi
else
  emit deployed "pulled to $NEW (no compose file)"
fi
