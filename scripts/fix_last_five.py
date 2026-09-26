#!/usr/bin/env python3
import os
import shutil

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

# 1. YENA
yena_inner = os.path.join(BASE_DIR, "J-Pop", "YENA ~", "YENA ~")
if os.path.exists(yena_inner):
    yena_nemo = os.path.join(BASE_DIR, "J-Pop", "YENA ~", "NEMONEMO")
    os.makedirs(yena_nemo, exist_ok=True)
    for f in os.listdir(yena_inner):
        shutil.move(os.path.join(yena_inner, f), os.path.join(yena_nemo, f))
    os.rmdir(yena_inner)
    print("Fixed YENA ~")

# 2. Various Artists ~
va_inner = os.path.join(BASE_DIR, "J-Pop", "Various Artists ~", "Various Artists ~")
if os.path.exists(va_inner):
    for f in os.listdir(va_inner):
        base, ext = os.path.splitext(f)
        album_dir = os.path.join(BASE_DIR, "J-Pop", "Various Artists ~", base)
        os.makedirs(album_dir, exist_ok=True)
        shutil.move(os.path.join(va_inner, f), os.path.join(album_dir, f))
    os.rmdir(va_inner)
    print("Fixed Various Artists ~")

# 3. Isekaijoucho
isekai_inner = os.path.join(BASE_DIR, "Vtuber", "KAMITSUBAKI STUDIO (神椿スタジオ) ~", "Isekaijoucho (ヰ世界情緒) ~", "眠りゆく芽吹き", "眠りゆく芽吹き")
if os.path.exists(isekai_inner):
    shutil.rmtree(isekai_inner)
    print("Fixed Isekaijoucho")

# 4. Juara Khatulistiwa
juara_outer = os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~", "Hololive Official ~", "Juara Khatulistiwa")
juara_inner = os.path.join(juara_outer, "Juara Khatulistiwa")
if os.path.exists(juara_inner):
    for f in os.listdir(juara_inner):
        shutil.move(os.path.join(juara_inner, f), os.path.join(juara_outer, f))
    os.rmdir(juara_inner)
    print("Fixed Juara Khatulistiwa")

# 5. Amane Kanata
kanata_inner = os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~", "Amane Kanata (天音かなた) ~", "中空の庭", "中空の庭")
if os.path.exists(kanata_inner):
    shutil.rmtree(kanata_inner)
    print("Fixed Amane Kanata")
