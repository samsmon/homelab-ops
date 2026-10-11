#!/usr/bin/env python3
import json
import re

with open("/tmp/gdrive_pairs.json", "r", encoding="utf-8") as f:
    pairs = json.load(f)

with open("/tmp/list_shiny_albums.py", "r", encoding="utf-8") as f:
    pass

import subprocess
res = subprocess.run(["python3", "/tmp/list_shiny_albums.py"], capture_output=True, text=True, encoding="utf-8")
server_albums = [l.strip() for l in res.stdout.split('\n') if l.strip() and not l.startswith('COUNT=')]

truly_missing = []

for title, url in pairs:
    clean_title = title.replace(r'\[', '[').replace(r'\]', ']').replace(' - Google Drive', '').strip()
    
    # Check if exact or equivalent exists in server_albums
    # 1. CANVAS 01-08: on server we have 0 CANVAS! (server folder CANVAS (2023) is empty) -> ALL MISSING
    # 2. ECHOES 02, 03, 04, 05, 06: on server only 01, 07, 08, 09 -> 02..06 MISSING
    # 3. PANOR@MA WING: on server we have 01, 02, 03, 04, 06 -> 05, 07, 08 MISSING
    # 4. WING COLLECTION: A-side, B-side -> MISSING
    # 5. -28 colors- COLLECTION -> MISSING
    # 6. シャイニーPRオファー Vol.1, 2, 3 -> MISSING
    # 7. 円環 -Halo around- 01, 02, 03, 04 -> MISSING
    # 8. Song for Prism editions:
    # On server we have:
    # [2024.05.22] ... Happier／枕木の歌 (generic single)
    # [2024.07.24] ... 時限式狂騒ワンダーランド／LINKs
    # [2024.09.25] ... After Run／mellow mellow
    # [2024.11.20] ... C'mon! Join Us...
    # [2024.11.27] ... Heads or Tails...
    # [2025.01.29] ... Shower of light...
    # [2025.03.26] ... Real Mind Shakes...
    # [2025.09.03] ... 愛しき日々...
    # [2026.01.07] ... カウントダウンラブ
    # [2026.01.28] ... QUEEN OF THE PIRATES
    # [2026.02.04] ... Karma
    # [2026.03.04] ... ボーダーレス
    # [2026.04.01] ... SUPER DUPER
    # [2026.04.29] ... Ring Ring Ring
    # [2026.06.03] ... 散花
    # [2026.07.01] ... Tokyo自由系
    # But missing:
    # - 星の声 (231018)
    # - Borderline／クローバー／Summer Night Paradise (251224)
    # - 裸足じゃイラレナイ／明日もBeautiful Day (240124)
    # - ハナムケのハナタバ／青空 (240403)
    
    # Let's see if this item is considered truly missing:
    is_missing = False
    
    if "CANVAS" in clean_title:
        is_missing = True
    elif re.search(r'ECHOES 0[2-6]', clean_title):
        is_missing = True
    elif re.search(r'PANOR@MA WING 0[578]', clean_title):
        is_missing = True
    elif "WING COLLECTION" in clean_title:
        is_missing = True
    elif "-28 colors- COLLECTION" in clean_title:
        is_missing = True
    elif "シャイニーPRオファー" in clean_title:
        is_missing = True
    elif "Halo around" in clean_title or "円環" in clean_title:
        is_missing = True
    elif "星の声" in clean_title:
        is_missing = True
    elif "Borderline" in clean_title:
        is_missing = True
    elif "裸足じゃイラレナイ" in clean_title:
        is_missing = True
    elif "ハナムケのハナタバ" in clean_title:
        is_missing = True
    elif "神様は死んだ、って" in clean_title:
        is_missing = True
    
    if is_missing:
        truly_missing.append((clean_title, url))

print(f"TRULY MISSING COUNT: {len(truly_missing)}")
for t, u in truly_missing:
    print(f"- [{t}]({u})")

with open("/tmp/truly_missing_categorized.json", "w", encoding="utf-8") as f:
    json.dump(truly_missing, f, ensure_ascii=False, indent=2)
