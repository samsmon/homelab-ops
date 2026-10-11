#!/usr/bin/env python3
import os

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=== CHECKING MORI CALLIOPE IN J-POP ===")
mori_p = os.path.join(BASE_DIR, "J-Pop", "Mori Calliope ~")
if os.path.exists(mori_p):
    for item in sorted(os.listdir(mori_p)):
        print(f"  {item}")

print("\n=== CHECKING HOLOLIVE SUBFOLDERS IN VTUBER ===")
holo_p = os.path.join(BASE_DIR, "Vtuber", "Hololive (ホロライブ) ~")
if os.path.exists(holo_p):
    for item in sorted(os.listdir(holo_p)):
        print(f"  {item}")

print("\n=== CHECKING KOBO KANAERU IN VTUBER ===")
kobo_p = os.path.join(BASE_DIR, "Vtuber", "Kobo Kanaeru ~")
if os.path.exists(kobo_p):
    for item in sorted(os.listdir(kobo_p)):
        print(f"  {item}")

print("\n=== CHECKING SHIGURE UI DUPLICATION ===")
for u in ["Shigure Ui (しぐれうい) ~", "Ui Shigure (しぐれうい) ~"]:
    up = os.path.join(BASE_DIR, "Vtuber", u)
    if os.path.exists(up):
        print(f"  {u}: {os.listdir(up)}")

print("\n=== CHECKING RYUGASAKI RENE DUPLICATION ===")
for r in ["Ryugasaki Rene (龍ヶ崎リン) ~", "Ryuu Saki Rin (龍ヶ崎リン) ~"]:
    rp = os.path.join(BASE_DIR, "Vtuber", r)
    if os.path.exists(rp):
        print(f"  {r}: {os.listdir(rp)}")

print("\n=== CHECKING FATE GEAR, KOIAI, OCHA NORMA IN VOCALOID ===")
for v in ["FATE GEAR ~", "KOIAI ~", "OCHA NORMA ~"]:
    vp = os.path.join(BASE_DIR, "Vocaloid", v)
    if os.path.exists(vp):
        print(f"  {v}: {os.listdir(vp)}")
