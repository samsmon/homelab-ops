import glob
import subprocess
import os

archives = glob.glob('/mnt/hdd-backup/download_pc_staging/*/*/*.rar')
print(f"Found {len(archives)} rar files to extract...")
for r in archives:
    d = os.path.splitext(r)[0]
    os.makedirs(d, exist_ok=True)
    res = subprocess.run(['7z', 'x', '-y', f'-o{d}', r], capture_output=True)
    if res.returncode == 0:
        os.remove(r)
        print('EXTRACTED:', os.path.basename(r))
    else:
        print('FAIL:', os.path.basename(r), res.stderr.decode('utf-8', 'ignore'))
