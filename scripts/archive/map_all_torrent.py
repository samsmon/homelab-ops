import json
import re

with open('/tmp/torrent_audit_report.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

new_albums = d['not_in_library']

patterns = {
    'gakumas': [],
    'shiny': [],
    'lovelive': [],
    'bangdream': [],
    'd4dj': [],
    'idoly': [],
    'vtuber': [],
    'jpop': [],
    'other_anime': [],
    'unmatched': []
}

for a in new_albums:
    if '学園アイドルマスター' in a or '初星学園' in a:
        patterns['gakumas'].append(a)
    elif 'SHINY COLORS' in a or 'シャイニーカラーズ' in a:
        patterns['shiny'].append(a)
    elif 'ラブライブ' in a or '蓮ノ空' in a or '虹ヶ咲' in a or 'Liella' in a or 'サンシャイン' in a or 'GKSS' in a or 'NIJIGAKU' in a:
        patterns['lovelive'].append(a)
    elif 'BanG Dream' in a or 'バンドリ' in a or 'Ave Mujica' in a or 'MyGO' in a:
        patterns['bangdream'].append(a)
    elif 'D4DJ' in a or 'Merm4id' in a or '燐舞曲' in a:
        patterns['d4dj'].append(a)
    elif 'IDOLY PRIDE' in a:
        patterns['idoly'].append(a)
    elif any(k in a for k in ['hololive', 'すいせい', 'トワ', 'ルイ', 'Midnight Grand Orchestra', 'さくらみこ', '桃鈴ねね', 'Overture', 'Starpeggio']):
        patterns['vtuber'].append(a)
    elif 'milet' in a:
        patterns['jpop'].append(a)
    elif 'Tokyo 7th' in a or 'ポールプリンセス' in a:
        patterns['other_anime'].append(a)
    else:
        patterns['unmatched'].append(a)

print("SUMMARY MAPPING COUNTS:")
total = 0
for k, v in patterns.items():
    print(f" - {k}: {len(v)}")
    total += len(v)
print(f"TOTAL: {total} / {len(new_albums)}")

if patterns['unmatched']:
    print("\nUNMATCHED:")
    for u in patterns['unmatched']:
        print(" *", u)
