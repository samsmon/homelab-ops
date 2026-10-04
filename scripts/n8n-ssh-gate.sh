#!/bin/bash
# Forced-command gate for the n8n SSH key (authorized_keys: restrict,command="/opt/scripts/n8n-ssh-gate.sh" ...).
# Only allows:  n8n-deploy-check <project> [--apply]
# The n8n SSH node always prefixes commands with "cd <dir> ; ", so that exact prefix
# (plain path chars only) is tolerated and ignored. Anything else is rejected, so the
# key cannot be used for a shell or arbitrary commands.

if [[ "${SSH_ORIGINAL_COMMAND:-}" =~ ^(cd\ [A-Za-z0-9._/-]+\ \;\ )?n8n-deploy-check\ ([A-Za-z0-9._-]+)(\ --apply)?$ ]]; then
  exec /opt/scripts/n8n-deploy-check.sh "${BASH_REMATCH[2]}" ${BASH_REMATCH[3]:+--apply}
fi
echo '{"action":"error","detail":"command not allowed"}'
exit 1
