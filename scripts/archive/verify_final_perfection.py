#!/usr/bin/env python3
import os
from pathlib import Path

lossless = Path('/mnt/hdd-backup/music/Lossless')

print("=== 1. GAKUMAS 01. SOLO ===")
solo = lossless / 'Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~/01. Solo'
items = sorted(os.listdir(solo))
print(f"Total items in 01. Solo: {len(items)} (MUST BE EXACTLY 13)")
for x in items:
    subdirs = [s for s in (solo / x).iterdir() if s.is_dir()]
    print(f"  {x} -> {len(subdirs)} albums")

print("\n=== 2. GAME CATEGORY ===")
game = lossless / 'Game'
for x in sorted(os.listdir(game)):
    subdirs = [s for s in (game / x).iterdir() if s.is_dir()]
    print(f"  {x} -> {len(subdirs)} albums")

print("\n=== 3. VOCALOID CHECKS ===")
for v in ['Hiiragi Magnetite (柊マグネタイト) ~', 'Harumaki Gohan (はるまきごはん) ~', 'MIMI ~', 'TAK ~']:
    p = lossless / 'Vocaloid' / v
    print(f"  {v}: exists={p.exists()}")

print("\n=== 4. J-POP CHECKS ===")
for j in ['Yui Ogura (小倉唯) ~', 'Ikkyu Nakajima (中嶋イッキュウ) ~', 'Atarayo (あたらよ) ~', 'JUNNA ~', 'Ten ~', 'Hakoniwa Lily (ハコニワリリィ) ~']:
    p = lossless / 'J-Pop' / j
    print(f"  {j}: exists={p.exists()}")

print("\n=== 5. ANIME CHECKS ===")
for a in ['100 Kanojo (君のことが大大大大大好きな100人の彼女) ~', 'Oshi no Ko (【推しの子】) ~', 'Utahime Dream (ウタヒメドリーム) ~', 'MILGRAM ~', 'iMarine Project ~']:
    p = lossless / 'Anime' / a
    print(f"  {a}: exists={p.exists()}")
