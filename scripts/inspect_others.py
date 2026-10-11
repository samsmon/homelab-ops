import json

with open('/tmp/torrent_audit_report.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

new_albums = d['not_in_library']

known_keys = [
    "学園アイドルマスター", "初星学園", "SHINY COLORS", "シャイニーカラーズ",
    "ラブライブ", "蓮ノ空", "虹ヶ咲", "Liella",
    "BanG Dream", "バンドリ", "Ave Mujica", "MyGO",
    "D4DJ", "Merm4id", "燐舞曲",
    "hololive", "すいせい", "トワ", "ルイ", "Midnight Grand Orchestra", "Hakos", "あくあ", "AZKi"
]

others = []
for a in new_albums:
    if not any(k in a for k in known_keys):
        others.append(a)

print(f"Total 'Others' albums: {len(others)}")
for o in others:
    print(" -", o)
