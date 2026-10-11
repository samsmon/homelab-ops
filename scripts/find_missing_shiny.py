#!/usr/bin/env python3
import json
import re

transcript_path = "/tmp/transcript_full.jsonl"
pairs = []

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        if "drive.google.com" in line and "THE IDOLM@STER SHINY COLORS" in line:
            # Look for markdown links: [Title](URL) or raw URL patterns
            found = re.findall(r'\[(.*?)\]\((https://drive\.google\.com/file/d/[^\)\s]+)\)', line)
            if found:
                for t, u in found:
                    t_clean = t.replace(r'\[', '[').replace(r'\]', ']').strip()
                    pairs.append((t_clean, u))
                break

print(f"Total matched pairs: {len(pairs)}")

# Save to json
with open("/tmp/gdrive_pairs.json", "w", encoding="utf-8") as out:
    json.dump(pairs, out, ensure_ascii=False, indent=2)

# Load server albums from /tmp/list_shiny_albums.py
import subprocess
res = subprocess.run(["python3", "/tmp/list_shiny_albums.py"], capture_output=True, text=True, encoding="utf-8")
server_albums = [l.strip() for l in res.stdout.split('\n') if l.strip() and not l.startswith('COUNT=')]

print(f"Total server albums: {len(server_albums)}")

# Compare each pair to see if it is in server_albums
missing_items = []
existing_items = []

for title, url in pairs:
    # Match criteria
    matched = False
    # Clean title for matching
    # extract e.g. "CANVAS” 01" or "ECHOES 02" or date+title
    # Check date [YYMMDD] -> [20YY.MM.DD]
    date_m = re.match(r'\[(\d{2})(\d{2})(\d{2})\]', title)
    date_prefix = None
    if date_m:
        date_prefix = f"[20{date_m.group(1)}.{date_m.group(2)}.{date_m.group(3)}]"
    
    # Check by specific series identifiers
    patterns_to_check = [
        r'CANVAS["”]?\s*0?\d+',
        r'ECHOES\s*0?\d+',
        r'PANOR@MA WING\s*0?\d+',
        r'L@YERED WING\s*0?\d+',
        r'GR@DATE WING\s*0?\d+',
        r'FR@GMENT WING\s*0?\d+',
        r'BRILLI@NT WING\s*0?\d+',
        r'Synthe-Side\s*0?\d+',
        r'円環 -Halo around-["”]?\s*0?\d+',
        r'シャイニーPRオファー\s*Vol\.\d+',
        r'WING COLLECTION -[AB] side-',
        r'-28 colors- COLLECTION',
        r'Song for Prism [^（\(]+',
    ]

    for sa in server_albums:
        if date_prefix and date_prefix in sa:
            # Check if main keywords also match
            # e.g. ECHOES 07 vs ECHOES 07
            matched = True
            break
        # also check exact series match
        for pat in patterns_to_check:
            m1 = re.search(pat, title)
            m2 = re.search(pat, sa)
            if m1 and m2 and m1.group(0).lower().replace('"', '').replace('”', '') == m2.group(0).lower().replace('"', '').replace('”', ''):
                matched = True
                break
        if matched:
            break

    if matched:
        existing_items.append((title, url))
    else:
        missing_items.append((title, url))

print(f"ALREADY ON SERVER: {len(existing_items)}")
print(f"MISSING FROM SERVER: {len(missing_items)}")

with open("/tmp/missing_gdrive.json", "w", encoding="utf-8") as out:
    json.dump(missing_items, out, ensure_ascii=False, indent=2)

print("\n--- MISSING ITEMS PREVIEW ---")
for t, u in missing_items:
    print(f"- {t} -> {u}")
