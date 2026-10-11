import os

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=== CHECKING CASE-INSENSITIVE / SPLIT ARTIST DIRECTORIES ACROSS ALL CATEGORIES ===")
for cat in os.listdir(ROOT):
    cat_dir = os.path.join(ROOT, cat)
    if not os.path.isdir(cat_dir) or cat.startswith('.'):
        continue
    
    entries = os.listdir(cat_dir)
    # Check lowercase mapping
    lower_map = {}
    for e in entries:
        low = e.lower()
        if low in lower_map:
            lower_map[low].append(e)
        else:
            lower_map[low] = [e]
            
    for low, matches in lower_map.items():
        if len(matches) > 1:
            print(f"[{cat}] Case Collision: {matches}")
            for m in matches:
                p = os.path.join(cat_dir, m)
                print(f"  - {m}: {len(os.listdir(p))} items")

print("\n=== CHECKING SIMILAR ARTIST NAMES (KANJI/ROMAJI VARIATIONS) ===")
for cat in ['J-Pop', 'Vtuber', 'Vocaloid', 'Doujinshi', 'Global']:
    cat_dir = os.path.join(ROOT, cat)
    if not os.path.isdir(cat_dir):
        continue
    entries = sorted(os.listdir(cat_dir))
    import re
    def base_name(s):
        s = re.sub(r'\(.*?\)', '', s)
        s = re.sub(r'\[.*?\]', '', s)
        s = re.sub(r'[~\s_.]', '', s).lower()
        return s
    
    base_map = {}
    for e in entries:
        b = base_name(e)
        if b:
            if b in base_map:
                base_map[b].append(e)
            else:
                base_map[b] = [e]
                
    for b, matches in base_map.items():
        if len(matches) > 1:
            print(f"[{cat}] Base Match: {matches}")
            for m in matches:
                p = os.path.join(cat_dir, m)
                items = os.listdir(p) if os.path.isdir(p) else []
                print(f"  - {m}: {len(items)} items -> {items[:3]}")

print("\n=== CHECKING SHINY COLORS EMPTY ALBUM FOLDERS ===")
sc_dir = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/02. Song for Prism Series"
if os.path.exists(sc_dir):
    for d in os.listdir(sc_dir):
        dp = os.path.join(sc_dir, d)
        if os.path.isdir(dp):
            files = os.listdir(dp)
            audio = [f for f in files if f.endswith(('.flac', '.wav', '.m4a'))]
            if len(audio) == 0:
                print(f"Empty/No Audio in Shiny Colors: {d}")
                print(f"  Contents: {files}")
