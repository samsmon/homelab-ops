#!/usr/bin/env python3
import os
import re
import json

LOSSLESS_ROOT = "/mnt/hdd-backup/music/Lossless"

anomalies = {
    "cross_category_duplicates": [],
    "non_standard_artist_folders": [],
    "loose_files_in_roots": [],
    "raw_wav_cue_folders": [],
    "tag_issue_samples": []
}

categories = ["Anime", "J-Pop", "Doujinshi", "Vtuber", "Vocaloid", "Global"]
artist_dirs = {} # clean_name -> list of paths

for cat in categories:
    cat_dir = os.path.join(LOSSLESS_ROOT, cat)
    if not os.path.exists(cat_dir):
        continue
    for item in os.listdir(cat_dir):
        full = os.path.join(cat_dir, item)
        if os.path.isfile(full):
            anomalies["loose_files_in_roots"].append(full)
        elif os.path.isdir(full):
            if not item.endswith("~"):
                anomalies["non_standard_artist_folders"].append(full)
            clean = re.sub(r'[\(\[\{].*?[\)\]\}]', '', item).replace('~', '').strip().lower()
            clean = re.sub(r'[^\w\s]', '', clean)
            if len(clean) >= 3:
                if clean not in artist_dirs:
                    artist_dirs[clean] = []
                artist_dirs[clean].append(full)

for name, paths in artist_dirs.items():
    cats = set(p.split('/')[5] for p in paths)
    if len(paths) > 1 and len(cats) > 1:
        anomalies["cross_category_duplicates"].append({"name": name, "paths": paths})

# Quick scan for wav files
for root, dirs, files in os.walk(LOSSLESS_ROOT):
    if any(f.lower().endswith(".wav") for f in files):
        anomalies["raw_wav_cue_folders"].append(root)

with open("/tmp/quick_audit.json", "w", encoding="utf-8") as f:
    json.dump(anomalies, f, ensure_ascii=False, indent=2)

print("QUICK_AUDIT_DONE")
