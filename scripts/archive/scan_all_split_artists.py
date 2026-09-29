import os
import re

ROOT = "/mnt/hdd-backup/music/Lossless"

def clean_key(s):
    s = re.sub(r'\(.*?\)', '', s)
    s = re.sub(r'\[.*?\]', '', s)
    s = re.sub(r'\{.*?\}', '', s)
    s = re.sub(r'[~\s_.\-\'\"／]', '', s).lower()
    return s

for cat in os.listdir(ROOT):
    cat_path = os.path.join(ROOT, cat)
    if not os.path.isdir(cat_path) or cat.startswith('.'):
        continue
    
    # We want to check artists/franchises at depth 1 under category
    entries = sorted(os.listdir(cat_path))
    
    # 1. Exact case-insensitive match
    lower_map = {}
    for e in entries:
        low = e.lower()
        lower_map.setdefault(low, []).append(e)
        
    case_coll = {k: v for k, v in lower_map.items() if len(v) > 1}
    if case_coll:
        print(f"\n[{cat}] CASE COLLISIONS:")
        for k, v in case_coll.items():
            print(f"  {v}")
            
    # 2. Base name match (ignoring kanji in parentheses and spacing)
    base_map = {}
    for e in entries:
        b = clean_key(e)
        if b:
            base_map.setdefault(b, []).append(e)
            
    base_matches = {k: v for k, v in base_map.items() if len(v) > 1 and v not in case_coll.values()}
    if base_matches:
        print(f"\n[{cat}] BASE NAME MATCHES (POTENTIAL SPLIT ARTISTS):")
        for k, v in base_matches.items():
            print(f"  {v}")
