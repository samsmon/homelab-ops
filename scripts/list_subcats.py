import json

with open('/tmp/truly_new_by_category.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

for c in ['gakumas', 'shiny', 'vtuber', 'jpop', 'other_anime', 'idoly']:
    print(f"\n=== CATEGORY: {c} ({len(cats[c])}) ===")
    for a in cats[c]:
        print(" -", a)
