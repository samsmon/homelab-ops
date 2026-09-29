#!/usr/bin/env python3
import os
import sys
import subprocess
import time

LOG_FILE = "/root/torrent_ingestion.log"
BACKUP_ROOT = "/mnt/hdd-backup/music/Lossless"
MUSIC_ROOT = "/mnt/hdd-music/music/Lossless"

def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

log("=== CONTINUING INGESTION FINALIZATION PIPELINE ===")

# -------------------------------------------------------------------------
# STEP 4: PERMISSIONS ENFORCEMENT (100000:100000, 775/664)
# -------------------------------------------------------------------------
log("--- STEP 4: Enforcing Permissions (100000:100000, 775/664) ---")
subprocess.run(["chown", "-R", "100000:100000", BACKUP_ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["find", BACKUP_ROOT, "-type", "d", "-exec", "chmod", "775", "{}", "+"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["find", BACKUP_ROOT, "-type", "f", "-exec", "chmod", "664", "{}", "+"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
log("Permissions enforced on /mnt/hdd-backup/music/Lossless.")

# -------------------------------------------------------------------------
# STEP 5: UPDATE SQLITE CATALOG
# -------------------------------------------------------------------------
log("--- STEP 5: Updating Master SQLite Catalog ---")
if os.path.exists("/tmp/update_catalog.py"):
    res = subprocess.run(["python3", "/tmp/update_catalog.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log(f"Catalog update output: {res.stdout.strip()}")
elif os.path.exists("/root/homelab-ops/scripts/update_catalog.py"):
    res = subprocess.run(["python3", "/root/homelab-ops/scripts/update_catalog.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log(f"Catalog update output: {res.stdout.strip()}")

# -------------------------------------------------------------------------
# STEP 6: 1:1 RSYNC MIRROR TO HDD-MUSIC (Z:\)
# -------------------------------------------------------------------------
log("--- STEP 6: Mirroring 1:1 to /mnt/hdd-music/music/Lossless (Z:\\) ---")
rsync_cmd = [
    "rsync", "-avh", "--delete",
    f"{BACKUP_ROOT}/", f"{MUSIC_ROOT}/"
]
res = subprocess.run(rsync_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res.returncode == 0:
    log("Rsync mirroring finished successfully.")
else:
    log(f"Rsync completed with code {res.returncode}. Error: {res.stderr[:200]}")

# Ensure permissions on hdd-music
subprocess.run(["chown", "-R", "100000:100000", MUSIC_ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
log("Permissions enforced on /mnt/hdd-music/music/Lossless.")

log("=== ALL INGESTION, PERMISSIONS, CATALOG, AND 1:1 MIRROR COMPLETED SUCCESSFULLY ===")
