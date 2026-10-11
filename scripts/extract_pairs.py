import json
import re

transcript_path = r"C:\Users\Sam\.gemini\antigravity\brain\423a7e7c-328c-4da5-b6e6-81eca21f020c\.system_generated\logs\transcript_full.jsonl"

pairs = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'drive.google.com' in line and 'THE IDOLM@STER SHINY COLORS' in line:
            # find all [title](url)
            matches = re.findall(r'\[([^\]]+)\]\((https://drive\.google\.com/file/d/[^\)]+)\)', line)
            if matches:
                pairs = matches
                break

print(f"Total matched (title, url) pairs: {len(pairs)}")

# Load server albums
server_albums = []
with open(r"c:\Users\Sam\Documents\GitHub\homelab-ops\scripts\server_albums.txt", "w", encoding="utf-8") as out:
    pass

import subprocess
res = subprocess.run(["ssh", "docker-host", "python3 /tmp/list_shiny_albums.py"], capture_output=True, text=True, encoding="utf-8")
server_albums = [l.strip() for l in res.stdout.split('\n') if l.strip() and not l.startswith('COUNT=')]

print(f"Total server albums: {len(server_albums)}")

missing_from_server = []
already_on_server = []

for title, url in pairs:
    # clean title
    # e.g. [230412]THE IDOLM@STER SHINY COLORS “CANVAS” 01(FLAC 96kHz_24bit).zip
    # extract series/disc info
    matched = False
    for sa in server_albums:
        # Check matching by key tokens
        # e.g. CANVAS 01, ECHOES 02, etc.
        # Let's check common substrings
        pass

with open(r"c:\Users\Sam\Documents\GitHub\homelab-ops\scripts\all_gdrive_pairs.json", "w", encoding="utf-8") as f:
    json.dump(pairs, f, ensure_ascii=False, indent=2)
