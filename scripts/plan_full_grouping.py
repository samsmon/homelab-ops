#!/usr/bin/env python3
import json
from pathlib import Path
from collections import defaultdict

MUSIC_ROOT = Path('/mnt/hdd-backup/music/Lossless')
RULES_FILE = Path(__file__).resolve().parent.parent / 'configs' / 'music_grouping_rules.json'

def load_rules():
    if not RULES_FILE.exists():
        # Fallback to local script dir if running remotely
        alt = Path('/tmp/music_grouping_rules.json')
        if alt.exists():
            with open(alt, 'r', encoding='utf-8') as f:
                return json.load(f)
        raise FileNotFoundError(f"Rules file not found at {RULES_FILE}")
    with open(RULES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_plan():
    rules = load_rules()
    plan = defaultdict(list)

    for cat, cfg in rules.items():
        cat_dir = MUSIC_ROOT / cat
        if not cat_dir.exists():
            continue

        exact_map = cfg.get('exact', {})
        patterns = cfg.get('patterns', [])

        for d in sorted(cat_dir.iterdir()):
            if not d.is_dir() or d.name.endswith('~'):
                continue
            name = d.name
            lower = name.lower()
            target = None

            # 1. Exact match check
            if name in exact_map:
                target = exact_map[name]
            else:
                # 2. Pattern keyword check
                for p in patterns:
                    if any(k in lower for k in p['keywords']):
                        target = p['target']
                        break

            if target:
                plan[cat].append((name, target))

    return plan

if __name__ == '__main__':
    p = build_plan()
    print("=" * 60)
    print("GROUPING SIMULATION RESULTS")
    print("=" * 60)
    for cat in ['Doujinshi', 'Vtuber', 'Anime', 'J-Pop', 'Vocaloid']:
        items = p.get(cat, [])
        print(f"\n[{cat.upper()}] Groupable Loose Albums: {len(items)}")
        for src, dst in items:
            print(f"  '{src}'\n    -> '{cat}/{dst}'")
