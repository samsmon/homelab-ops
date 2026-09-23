#!/usr/bin/env python3
import os
from pathlib import Path

music_root = Path('/mnt/hdd-backup/music/Lossless')

print("="*60)
print("AUDITING UNGROUPED / SCATTERED FOLDERS ACROSS LOSSLESS")
print("="*60)

for cat in ['Doujinshi', 'Vtuber', 'Anime', 'J-Pop', 'Vocaloid']:
    cat_dir = music_root / cat
    if not cat_dir.exists():
        continue
    all_dirs = sorted([d for d in cat_dir.iterdir() if d.is_dir()])
    artist_dirs = {d.name: d for d in all_dirs if d.name.endswith('~')}
    loose_dirs = [d for d in all_dirs if not d.name.endswith('~')]
    
    print(f"\n[{cat.upper()}] Total items: {len(all_dirs)} | Artist folders (~): {len(artist_dirs)} | Loose items: {len(loose_dirs)}")
    
    # 1. Existing artist folder matches
    matched_to_existing = []
    unmatched_loose = []
    
    for l in loose_dirs:
        lname = l.name.lower()
        matched = None
        for aname in artist_dirs:
            # check exact containment of key terms
            clean = aname.rstrip('~').strip()
            # check japanese / english parts
            parts = [clean]
            if '(' in clean and ')' in clean:
                p1 = clean[:clean.find('(')].strip()
                p2 = clean[clean.find('(')+1:clean.find(')')].strip()
                parts.extend([p1, p2])
            for p in parts:
                if len(p) >= 2 and p.lower() in lname:
                    matched = aname
                    break
            if matched:
                break
        if matched:
            matched_to_existing.append((l.name, matched))
        else:
            unmatched_loose.append(l.name)
            
    print(f"  Loose albums matching EXISTING '{cat}/<Artist> ~': {len(matched_to_existing)}")
    for l, a in matched_to_existing:
        print(f"    -> '{l}' fits into '{a}'")
        
    print(f"\n  Unmatched loose albums in {cat}: {len(unmatched_loose)}")
    # Find clusters among unmatched
    clusters = {}
    for l in unmatched_loose:
        # extract candidate prefix / artist name
        prefix = None
        for delim in [' - ', '／', ' / ', ' (', ' [', '【']:
            if delim in l:
                cand = l.split(delim)[0].strip()
                if cand.startswith('[') and ']' in cand:
                    cand = cand[cand.find(']')+1:].strip()
                if len(cand) >= 2:
                    prefix = cand
                    break
        if prefix:
            clusters.setdefault(prefix, []).append(l)
            
    multi_album_artists = {k: v for k, v in clusters.items() if len(v) > 1}
    print(f"  Detected new potential artist clusters (>1 album): {len(multi_album_artists)}")
    for artist, albums in multi_album_artists.items():
        print(f"    * New cluster '{artist} ~' ({len(albums)} albums):")
        for alb in albums:
            print(f"        - {alb}")
