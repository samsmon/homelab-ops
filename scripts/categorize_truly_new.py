import json

with open('/tmp/truly_new_torrent_albums.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

truly_new = d['truly_new']

cats = {
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

for a in truly_new:
    if '学園アイドルマスター' in a or '初星学園' in a:
        cats['gakumas'].append(a)
    elif 'SHINY COLORS' in a or 'シャイニーカラーズ' in a:
        cats['shiny'].append(a)
    elif any(k in a for k in ['ラブライブ', '蓮ノ空', '虹ヶ咲', 'Liella', 'サンシャイン', 'GKSS', 'NIJIGAKU']):
        cats['lovelive'].append(a)
    elif any(k in a for k in ['BanG Dream', 'バンドリ', 'Ave Mujica', 'MyGO']):
        cats['bangdream'].append(a)
    elif any(k in a for k in ['D4DJ', 'Merm4id', '燐舞曲']):
        cats['d4dj'].append(a)
    elif 'IDOLY' in a or '月のテンペスト' in a or 'Sweet Rouge' in a or '星見プロダクション' in a or 'ⅢX' in a:
        cats['idoly'].append(a)
    elif any(k in a for k in ['hololive', 'すいせい', 'トワ', 'ルイ', 'Midnight Grand Orchestra', 'さくらみこ', '桃鈴ねね']):
        cats['vtuber'].append(a)
    elif 'milet' in a:
        cats['jpop'].append(a)
    elif any(k in a for k in ['Tokyo 7th', 'ポールプリンセス']):
        cats['other_anime'].append(a)
    else:
        cats['unmatched'].append(a)

print("=== FINAL BREAKDOWN OF TRULY NEW ALBUMS (142 TOTAL) ===")
total = 0
for k, v in cats.items():
    print(f"[{k}]: {len(v)} albums")
    total += len(v)
print(f"TOTAL: {total} / {len(truly_new)}")
if cats['unmatched']:
    print("UNMATCHED:", cats['unmatched'])

with open('/tmp/truly_new_by_category.json', 'w', encoding='utf-8') as f:
    json.dump(cats, f, ensure_ascii=False, indent=2)
