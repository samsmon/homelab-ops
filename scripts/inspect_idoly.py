import json

with open('/tmp/torrent_audit_report.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for a in d['not_in_library']:
    if 'IDOLY' in a or '月のテンペスト' in a or 'Sweet Rouge' in a or '星見プロダクション' in a or 'ⅢX' in a:
        print("IDOLY:", a)
