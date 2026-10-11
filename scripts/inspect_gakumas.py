import json
import re

with open('/tmp/torrent_audit_report.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

new_albums = d['not_in_library']

for a in new_albums:
    if '学園アイドルマスター' in a or '初星学園' in a:
        print("GAKUMAS:", a)
