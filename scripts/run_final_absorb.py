import sys
import os
sys.path.append('/root')
from master_music_centralization import (
    phase_4_ingest_and_normalize,
    phase_5_purify_master_library,
    phase_6_permissions_and_catalog,
    PC_STAGING_ROOT, log
)
import shutil
from pathlib import Path

log("Absorbing final remaining staging folders...")
phase_4_ingest_and_normalize(PC_STAGING_ROOT)
phase_5_purify_master_library()
phase_6_permissions_and_catalog()

# Clean up empty staging directory
staging = Path('/mnt/hdd-backup/download_pc_staging')
for root, dirs, files in list(os.walk(staging, topdown=False)):
    for f in files:
        if f in ['robocopy_upload.log', 'upload_complete.flag']:
            try:
                os.remove(os.path.join(root, f))
            except OSError:
                pass
    for d in dirs:
        try:
            os.rmdir(os.path.join(root, d))
        except OSError:
            pass

try:
    staging.rmdir()
except OSError:
    pass

log("ALL FINAL INGESTION AND CENTRALIZATION COMPLETE!")
