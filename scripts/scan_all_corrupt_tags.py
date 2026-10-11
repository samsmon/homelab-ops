#!/usr/bin/env python3
import os
import subprocess
import json
import time

ROOT_DIR = "/mnt/hdd-backup/music/Lossless"
REPORT_FILE = "/tmp/full_corrupt_tags_report.json"

corrupt_tracks = []
scanned_count = 0
start_time = time.time()

print(f"Starting full library tag corruption scan on {ROOT_DIR}...", flush=True)

# Walk all directories
for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    flac_files = [f for f in filenames if f.lower().endswith(".flac")]
    if not flac_files:
        continue
    
    for f in flac_files:
        scanned_count += 1
        if scanned_count % 1000 == 0:
            print(f"Scanned {scanned_count} FLACs... Found {len(corrupt_tracks)} corrupt tags so far. ({time.time()-start_time:.1f}s)", flush=True)
            
        full_path = os.path.join(dirpath, f)
        
        # We check TITLE, ARTIST, ALBUM
        try:
            res = subprocess.run(
                ["metaflac", "--show-tag=TITLE", "--show-tag=ARTIST", "--show-tag=ALBUM", full_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                errors="replace"
            )
            lines = res.stdout.strip().split('\n')
            track_issues = {}
            for line in lines:
                if "=" in line:
                    k, v = line.split("=", 1)
                    v_clean = v.strip()
                    # Check if value consists entirely of question marks (e.g. ???, ?????) with len >= 2
                    if v_clean and all(c in '?' for c in v_clean) and len(v_clean) >= 2:
                        track_issues[k] = v_clean
            
            if track_issues:
                corrupt_tracks.append({
                    "file": full_path,
                    "filename": f,
                    "folder": dirpath,
                    "issues": track_issues
                })
        except Exception as e:
            pass

print(f"Scan complete! Total FLAC scanned: {scanned_count}. Total corrupt files found: {len(corrupt_tracks)}.")

with open(REPORT_FILE, "w", encoding="utf-8") as out:
    json.dump({
        "total_scanned": scanned_count,
        "total_corrupt": len(corrupt_tracks),
        "corrupt_tracks": corrupt_tracks
    }, out, ensure_ascii=False, indent=2)

print(f"Report saved to {REPORT_FILE}")
