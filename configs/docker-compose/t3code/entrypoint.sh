#!/bin/bash
set -e

ensure_agy_links() {
    # Find agy_acp_server.par in persistent .t3 storage
    local agy_bin
    agy_bin=$(find /root/.t3/tools/antigravity-acp -maxdepth 4 -name "agy_acp_server.par" 2>/dev/null | head -n 1)
    if [ -n "$agy_bin" ] && [ -f "$agy_bin" ]; then
        chmod +x "$agy_bin" 2>/dev/null || true

        # Symlinks in PATH so T3 and subagents can always execute agy and antigravity
        ln -sf "$agy_bin" /usr/local/bin/agy
        ln -sf "$agy_bin" /usr/local/bin/antigravity
        ln -sf "$agy_bin" /usr/bin/agy 2>/dev/null || true
        ln -sf "$agy_bin" /usr/bin/antigravity 2>/dev/null || true

        # Sibling harness required by Antigravity
        local harness_dir
        harness_dir=$(dirname "$agy_bin")
        if [ -f "$harness_dir/localharness_external" ]; then
            chmod +x "$harness_dir/localharness_external" 2>/dev/null || true
            ln -sf "$harness_dir/localharness_external" /usr/local/bin/localharness_external
            ln -sf "$harness_dir/localharness_external" /usr/bin/localharness_external 2>/dev/null || true
        fi

        # Ensure active.json exists so T3 discovers the managed release
        local rel_id
        rel_id=$(basename "$harness_dir")
        local managed_dir="/root/.t3/tools/antigravity-acp/linux-x64"
        if [ -n "$rel_id" ] && [ ! -f "$managed_dir/active.json" ]; then
            mkdir -p "$managed_dir"
            echo "{\"releaseId\":\"$rel_id\"}" > "$managed_dir/active.json"
        fi
    fi
}

# Run once at startup only. Previously this re-ran every 5s in an unreaped
# background loop (`while true; sleep 5; find ...`), which was the direct
# cause of the constant I/O/CPU spikes and zombie process buildup on
# docker-host (see CHANGELOG 2026-09-15). Symlinks only go stale when `t3`
# self-updates its bundled Antigravity tool release, which is rare and
# handled by a container restart, not by continuous polling.
ensure_agy_links

# Fix permissions on SSH keys if present
if [ -d /root/.ssh ]; then
    chmod 700 /root/.ssh 2>/dev/null || true
    find /root/.ssh -type f -exec chmod 600 {} + 2>/dev/null || true
    find /root/.ssh -type f -name "*.pub" -exec chmod 644 {} + 2>/dev/null || true
fi

# Execute CMD passed to container
if [ $# -eq 0 ]; then
    exec t3 serve --host 0.0.0.0 --port 9000
else
    exec "$@"
fi
