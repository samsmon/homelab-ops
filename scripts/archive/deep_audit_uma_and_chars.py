#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep audit for:
1. Windows-illegal characters in directory/file names causing Samba mangling (_FCR9Q~X, etc.)
2. Luna folder placement across Doujinshi, J-Pop, and Vocaloid
3. Uma Musume complete discography analysis and pattern classification
4. Cross-franchise structure comparison (e.g. Im@s, Shiny Colors, Love Live)
"""
import os
import re
from pathlib import Path

BASE = Path('/mnt/hdd-backup/music/Lossless')

print("="*60)
print("1. SCANNING FOR WINDOWS-ILLEGAL CHARACTERS")
print("="*60)
illegal_chars = set(':*?"<>|\\')
mangled_dirs = []

for p in BASE.rglob('*'):
    if p.is_dir() and any(c in illegal_chars for c in p.name):
        mangled_dirs.append(p)

print(f"Total directories with illegal chars: {len(mangled_dirs)}")
for d in mangled_dirs:
    print(f"  DIR:  {d.relative_to(BASE)}")

print("\n" + "="*60)
print("2. LUNA FOLDERS ACROSS ALL CATEGORIES")
print("="*60)
for cat in ['Doujinshi', 'J-Pop', 'Vocaloid']:
    cat_dir = BASE / cat
    if cat_dir.exists():
        for d in cat_dir.iterdir():
            if 'luna' in d.name.lower():
                print(f"  [{cat}] {d.name}")
                for sub in d.iterdir():
                    print(f"      -> {sub.name}")

print("\n" + "="*60)
print("3. EXAMINING EXISTING FRANCHISE HIERARCHIES IN ANIME")
print("="*60)
for target in ['学園アイドルマスター ~', 'アイドルマスター シャイニーカラーズ ~', 'Im@s ~', 'BanG Dream! ~']:
    p = BASE / 'Anime' / target
    if p.exists():
        subdirs = [d for d in p.iterdir() if d.is_dir()]
        has_subsub = any(any(sd.is_dir() for sd in d.iterdir()) for d in subdirs)
        print(f"Franchise: {target} (Subdirs: {len(subdirs)}, Has sub-subdirs: {has_subsub})")
        for s in sorted(subdirs)[:6]:
            print(f"   - {s.name}")
        if len(subdirs) > 6:
            print(f"   ... and {len(subdirs)-6} more")
        print()

print("\n" + "="*60)
print("4. UMA MUSUME COMPREHENSIVE DISCOGRAPHY AUDIT")
print("="*60)
uma_dir = BASE / 'Anime' / 'Uma Musume ~'
if uma_dir.exists():
    albums = sorted([d for d in uma_dir.iterdir() if d.is_dir()])
    print(f"Total Albums in Uma Musume ~: {len(albums)}\n")
    
    patterns = {
        '01. WINNING LIVE Series (Game Themes & Vocals)': [],
        '02. ANIMATION DERBY Series (TV Anime Season 1 & 2, Umayon)': [],
        '03. STARTING GATE Series (Original Character Singles)': [],
        '04. Theatrical & Web Specials (Films & ONA)': [],
        '05. Special Compilations & Hi-Res': []
    }
    
    for a in albums:
        name = a.name
        audio_files = [f for f in a.rglob('*') if f.suffix.lower() in ['.flac', '.aiff', '.alac', '.m4a', '.wav']]
        size_mb = sum(f.stat().st_size for f in a.rglob('*') if f.is_file()) / (1024*1024)
        
        entry = (name, len(audio_files), size_mb, a)
        
        if 'WINNING LIVE' in name:
            patterns['01. WINNING LIVE Series (Game Themes & Vocals)'].append(entry)
        elif 'ANIMATION DERBY' in name or 'うまよん' in name:
            patterns['02. ANIMATION DERBY Series (TV Anime Season 1 & 2, Umayon)'].append(entry)
        elif 'STARTING GATE' in name:
            patterns['03. STARTING GATE Series (Original Character Singles)'].append(entry)
        elif '新時代の扉' in name or 'ROAD TO THE TOP' in name:
            patterns['04. Theatrical & Web Specials (Films & ONA)'].append(entry)
        else:
            patterns['05. Special Compilations & Hi-Res'].append(entry)
            
    for cat, items in patterns.items():
        total_cat_tracks = sum(x[1] for x in items)
        total_cat_size = sum(x[2] for x in items)
        print(f"### {cat} ({len(items)} albums, {total_cat_tracks} tracks, {total_cat_size/1024:.2f} GB)")
        for n, tc, sz, p in items:
            print(f"  - {n} [{tc} tracks, {sz:.1f} MB]")
        print()
