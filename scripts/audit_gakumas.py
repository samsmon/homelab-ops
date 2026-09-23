#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import hashlib
from pathlib import Path
from collections import defaultdict

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime')
imas_gakumas = BASE / 'Im@s ~' / '学園アイドルマスター'
flat_gakumas = BASE / '学園アイドルマスター ~'

print("="*60)
print("INTERNAL DUPLICATE CHECK IN GAKUMAS")
print("="*60)

all_audio_files = []
for p in [imas_gakumas, flat_gakumas]:
    if p.exists():
        for f in p.rglob('*'):
            if f.is_file() and f.suffix.lower() in ['.flac', '.wav', '.m4a']:
                all_audio_files.append(f)

# Group by size first
by_size = defaultdict(list)
for f in all_audio_files:
    by_size[f.stat().st_size].append(f)

potential_dups = {sz: files for sz, files in by_size.items() if len(files) > 1}
exact_dups = []

for sz, files in potential_dups.items():
    hashes = {}
    for f in files:
        h = hashlib.md5(f.read_bytes()).hexdigest()
        if h in hashes:
            exact_dups.append((f, hashes[h], sz))
        else:
            hashes[h] = f

print(f"Total exact duplicate audio files found: {len(exact_dups)}")
for f1, f2, sz in exact_dups:
    print(f"  DUP: {sz/(1024*1024):.2f} MB")
    print(f"    1: {f1}")
    print(f"    2: {f2}")

print("\n" + "="*60)
print("CHARACTER / ARTIST MAPPING")
print("="*60)

characters = [
    ('花海咲季', 'Saki Hanami'),
    ('月村手毬', 'Temari Tsukimura'),
    ('藤田ことね', 'Kotone Fujita'),
    ('有村麻央', 'Mao Arimura'),
    ('葛城リーリヤ', 'Lilja Katsuragi'),
    ('倉本千奈', 'China Kuramoto'),
    ('紫雲清夏', 'Sumika Shiun'),
    ('篠澤広', 'Hiro Shinosawa'),
    ('姫崎莉波', 'Rinami Himesaki'),
    ('花海佑芽', 'Ume Hanami'),
    ('秦谷美鈴', 'Misuzu Hataya'),
    ('十王星南', 'Sena Juo'),
    ('雨夜燕', 'Tsubame Amaya'),
    ('Begrazia', 'Begrazia'),
]

# All album folders from both sources
all_folders = []
if imas_gakumas.exists():
    for sub in imas_gakumas.iterdir():
        if sub.is_dir():
            for album in sub.iterdir():
                if album.is_dir():
                    all_folders.append(('Im@s', sub.name, album))

if flat_gakumas.exists():
    for album in flat_gakumas.iterdir():
        if album.is_dir():
            all_folders.append(('Flat', 'Root', album))

print(f"Total album folders to categorize: {len(all_folders)}")

artist_buckets = defaultdict(list)
all_cast = []

for src, parent_name, alb in all_folders:
    name = alb.name
    matched_char = None
    for jp, en in characters:
        if jp in name:
            matched_char = f"{jp} ({en})"
            break
            
    if matched_char:
        artist_buckets[matched_char].append((src, parent_name, alb))
    else:
        all_cast.append((src, parent_name, alb))

for char, albs in sorted(artist_buckets.items()):
    print(f"\n### {char} ({len(albs)} releases)")
    for src, p, a in albs:
        print(f"  - [{src}/{p}] {a.name}")

print(f"\n### 全体曲・ユニット (All Stars & Combinations) ({len(all_cast)} releases)")
for src, p, a in all_cast:
    print(f"  - [{src}/{p}] {a.name}")
