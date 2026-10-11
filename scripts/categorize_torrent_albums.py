import json

with open('/tmp/torrent_audit_report.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

new_albums = d['not_in_library']
cats = {
    'Gakuen Idolmaster (学園アイドルマスター)': [],
    'Shiny Colors (シャイニーカラーズ)': [],
    'Love Live! (ラブライブ！)': [],
    'BanG Dream! (バンドリ！)': [],
    'D4DJ': [],
    'Vtuber / Hololive': [],
    'Other Anime / J-Pop': []
}

for a in new_albums:
    if '学園アイドルマスター' in a or '初星学園' in a:
        cats['Gakuen Idolmaster (学園アイドルマスター)'].append(a)
    elif 'SHINY COLORS' in a or 'シャイニーカラーズ' in a:
        cats['Shiny Colors (シャイニーカラーズ)'].append(a)
    elif 'ラブライブ' in a or '蓮ノ空' in a or '虹ヶ咲' in a or 'Liella' in a:
        cats['Love Live! (ラブライブ！)'].append(a)
    elif 'BanG Dream' in a or 'バンドリ' in a or 'Ave Mujica' in a or 'MyGO' in a:
        cats['BanG Dream! (バンドリ！)'].append(a)
    elif 'D4DJ' in a or 'Merm4id' in a or '燐舞曲' in a:
        cats['D4DJ'].append(a)
    elif any(k in a for k in ['hololive', 'すいせい', 'トワ', 'ルイ', 'Midnight Grand Orchestra', 'Hakos', 'あくあ', 'AZKi']):
        cats['Vtuber / Hololive'].append(a)
    else:
        cats['Other Anime / J-Pop'].append(a)

print("=== 157 NEW ALBUMS BREAKDOWN ===")
for k, v in cats.items():
    print(f"\n[{k}]: {len(v)} albums")
    for item in v[:5]:
        print(f"  - {item}")
    if len(v) > 5:
        print(f"  ... and {len(v) - 5} more")
