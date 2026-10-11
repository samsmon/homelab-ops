#!/usr/bin/env python3
import os
import re
import subprocess
import json

LOSSLESS_ROOT = "/mnt/hdd-backup/music/Lossless"

def scan_library():
    anomalies = {
        "corrupt_tags": [],          # e.g. ?????? in tags
        "artwork_issues": [],        # bad embedded pictures
        "duplicate_artists": [],     # artist appears in both Anime and J-Pop or multiple folders
        "non_standard_folders": [],  # folder without trailing ~
        "loose_files": [],           # audio directly in category roots
        "raw_rips": [],              # wav+cue or monolithic files
        "nested_unwanted": []        # leftover cue/iso/log when flac exists
    }

    # 1. Check folder standards in root categories
    categories = ["Anime", "J-Pop", "Doujinshi", "Vtuber", "Vocaloid", "Global"]
    artist_map = {} # normalized_name -> list of paths

    for cat in categories:
        cat_path = os.path.join(LOSSLESS_ROOT, cat)
        if not os.path.exists(cat_path):
            continue
        
        for item in os.listdir(cat_path):
            item_path = os.path.join(cat_path, item)
            if os.path.isfile(item_path):
                anomalies["loose_files"].append(item_path)
            elif os.path.isdir(item_path):
                if not item.endswith("~"):
                    anomalies["non_standard_folders"].append(item_path)
                
                # track artist names across categories
                # clean up anime/franchise noise
                clean_name = re.sub(r'[\(\[\{].*?[\)\]\}]', '', item).replace('~', '').strip().lower()
                clean_name = re.sub(r'[^\w\s]', '', clean_name)
                if len(clean_name) >= 3:
                    if clean_name not in artist_map:
                        artist_map[clean_name] = []
                    artist_map[clean_name].append(item_path)

    # Detect duplicate artist/franchise locations
    for name, paths in artist_map.items():
        cats = set(p.split('/')[5] for p in paths)
        if len(paths) > 1 and len(cats) > 1:
            anomalies["duplicate_artists"].append({"name": name, "paths": paths})

    # 2. Walk entire library for raw rips, corrupt tags, and artwork bugs
    print("Auditing audio files...", flush=True)
    count = 0
    for root, dirs, files in os.walk(LOSSLESS_ROOT):
        # check for wav+cue
        has_wav = any(f.lower().endswith(".wav") for f in files)
        has_cue = any(f.lower().endswith(".cue") for f in files)
        has_flac = any(f.lower().endswith(".flac") for f in files)
        
        if has_wav and (has_cue or len(files) < 4):
            anomalies["raw_rips"].append(root)

        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext == ".flac":
                count += 1
                fpath = os.path.join(root, f)
                
                # Check tags for ?????? corruption
                try:
                    res = subprocess.run(["metaflac", "--show-tag=TITLE", fpath], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, errors="replace")
                    if res.stdout:
                        title_val = res.stdout.strip().replace("TITLE=", "")
                        if title_val and all(c in '?' for c in title_val) and len(title_val) >= 2:
                            anomalies["corrupt_tags"].append({"file": fpath, "tag": "TITLE", "val": title_val})
                except Exception:
                    pass

                # Check picture block errors
                try:
                    res_pic = subprocess.run(["metaflac", "--list", "--block-type=PICTURE", fpath], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, errors="replace")
                    # If multiple picture blocks or 0 length
                    pic_count = res_pic.stdout.count("type: 6 (PICTURE)")
                    if pic_count > 1:
                        anomalies["artwork_issues"].append({"file": fpath, "issue": f"Multiple picture blocks ({pic_count})"})
                except Exception:
                    pass

    print(f"Total FLAC scanned: {count}")
    return anomalies

if __name__ == "__main__":
    res = scan_library()
    with open("/tmp/full_audit_results.json", "w", encoding="utf-8") as out:
        json.dump(res, out, ensure_ascii=False, indent=2)
    print("Audit completed. Saved to /tmp/full_audit_results.json")
