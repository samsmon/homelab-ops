#!/usr/bin/env python3
import os
import re
import sys

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=" * 80)
print("DEEP ANALYSIS OF IDENTIFIED ANOMALIES")
print("=" * 80)

# 1. Inspect tuki. ~
tuki_path = os.path.join(BASE_DIR, "J-Pop", "tuki. ~")
if os.path.exists(tuki_path):
    print("\n--- Items in J-Pop/tuki. ~ ---")
    for item in sorted(os.listdir(tuki_path)):
        print(f"  {item}")

# 2. Inspect Toyama Nao
print("\n--- Items matching Toyama Nao in J-Pop or Anime ---")
for cat in ["J-Pop", "Anime"]:
    cat_dir = os.path.join(BASE_DIR, cat)
    if os.path.exists(cat_dir):
        for item in sorted(os.listdir(cat_dir)):
            if "yama" in item.lower() or "東山" in item:
                print(f"  [{cat}] {item}")
                sub_path = os.path.join(cat_dir, item)
                if os.path.isdir(sub_path):
                    for sub in sorted(os.listdir(sub_path)):
                        print(f"      -> {sub}")

# 3. Inspect Reona
print("\n--- Items matching Reona in J-Pop or Anime ---")
for cat in ["J-Pop", "Anime"]:
    cat_dir = os.path.join(BASE_DIR, cat)
    if os.path.exists(cat_dir):
        for item in sorted(os.listdir(cat_dir)):
            if "reona" in item.lower() or "レオナ" in item:
                print(f"  [{cat}] {item}")
                sub_path = os.path.join(cat_dir, item)
                if os.path.isdir(sub_path):
                    for sub in sorted(os.listdir(sub_path)):
                        print(f"      -> {sub}")

# 4. Inspect Bocchi the Rock!
print("\n--- Items in Bocchi the Rock! ---")
bocchi_path = os.path.join(BASE_DIR, "Anime", "Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~")
if os.path.exists(bocchi_path):
    for item in sorted(os.listdir(bocchi_path)):
        print(f"  {item}")

# 5. Inspect Hibana loose files
hibana_path = os.path.join(BASE_DIR, "J-Pop", "Hibana (ヒバナ) ~")
if os.path.exists(hibana_path):
    print("\n--- Items in Hibana (ヒバナ) ~ ---")
    for item in sorted(os.listdir(hibana_path)):
        print(f"  {item}")

# 6. Inspect White Album 2
print("\n--- White Album matches in Anime and Game ---")
for cat in ["Anime", "Game"]:
    cat_dir = os.path.join(BASE_DIR, cat)
    if os.path.exists(cat_dir):
        for item in sorted(os.listdir(cat_dir)):
            if "white" in item.lower() or "album" in item.lower():
                print(f"  [{cat}] {item}")

# 7. Inspect Character Songs in J-Pop
print("\n--- Character Songs in J-Pop ---")
for name in ["Nishiura Sora (cv. Aikawa Nao ) (西浦そら(CV.相川奈央)) ~", "Yura (cv. Oonishi Saori ) (ユラ(CV.大西沙織)) ~"]:
    p = os.path.join(BASE_DIR, "J-Pop", name)
    if os.path.exists(p):
        print(f"  {name}: {os.listdir(p)}")

# 8. Check 6 1-album person-like folders in Anime:
print("\n--- 1-album folders in Anime ---")
for f in ["Ultraman Arc (ウルトラマンアーク) ~", "Lycoris Recoil (リコリス・リコイル) ~", "Macross Delta (マクロスΔ) ~", "Yuru Camp (ゆるキャン△) ~", "Bad Girl (ばっどがーる) ~", "Slow Loop (スローループ) ~"]:
    p = os.path.join(BASE_DIR, "Anime", f)
    if os.path.exists(p):
        print(f"  {f} -> {os.listdir(p)}")

# 9. Cross-category splits detailed listing
print("\n--- Cross-Category Split Details ---")
cross_artists = [
    "Dadaizu (打打だいず)", "Endorfin.", "Endorfin", "FloweRiЯy", "Hagali", 
    "Hanatan", "HoneyWorks", "Imy", "Isle & Notes", "Islet (Tayori)", 
    "lapix", "Lapix", "Lucia", "nayuta", "NEUN", "Ruru (るる)", 
    "Tsukino (月乃)", "TUYU (ツユ)", "ubique", "Various Artists", "Vivid Lila"
]
for cat in ["Anime", "Doujinshi", "Game", "Global", "J-Pop", "Vocaloid", "Vtuber"]:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for item in os.listdir(cat_dir):
        for a in cross_artists:
            if a.lower() in item.lower():
                sub = os.path.join(cat_dir, item)
                n_items = len(os.listdir(sub)) if os.path.isdir(sub) else 0
                print(f"  [{cat}] {item} ({n_items} items/albums)")
