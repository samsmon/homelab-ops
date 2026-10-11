#!/usr/bin/env python3
import json

with open('/tmp/audit_lossless_report.json') as f:
    d = json.load(f)

print('=== 4 FOLDERS MISSING TILDE ===')
for item in d['missing_tilde']:
    print(f"[{item['category']}] '{item['folder']}'")
