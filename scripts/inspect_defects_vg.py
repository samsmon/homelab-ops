import json

with open('/tmp/audit_defects_vocaloid_global.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== 1. MISSING COVER FILES (sample of 10) ===")
for p in data['missing_cover_file'][:10]:
    print(" ", p)
print(f"Total missing Cover.jpg: {len(data['missing_cover_file'])}")

print("\n=== 2. EXTRA CLUTTER FILES (all 67) ===")
for p in data['extra_clutter_files']:
    print(" ", p)

print("\n=== 3. MISSING TAGS BREAKDOWN ===")
tag_counts = {}
for p, tags in data['missing_tags']:
    for t in tags:
        tag_counts[t] = tag_counts.get(t, 0) + 1
for t, c in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {t}: {c} tracks")

print("\n=== 4. FORUM SPAM TAGS ===")
for item in data['forum_spam_tags']:
    print(" ", item)

print("\n=== 5. NON STANDARD FILENAMES (sample of 20) ===")
for p in data['non_standard_filename'][:20]:
    print(" ", p)
