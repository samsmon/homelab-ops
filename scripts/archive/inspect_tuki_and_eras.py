#!/usr/bin/env python3
import os
import subprocess

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=== CHECKING ALBUMS IN J-Pop/tuki. ~ ===")
tuki_dir = os.path.join(BASE_DIR, "J-Pop", "tuki. ~")
if os.path.exists(tuki_dir):
    for item in sorted(os.listdir(tuki_dir)):
        p = os.path.join(tuki_dir, item)
        if os.path.isdir(p):
            subfiles = os.listdir(p)
            first_audio = next((f for f in subfiles if f.endswith(('.flac', '.mp3', '.m4a', '.wav'))), None)
            artist_tag = "UNKNOWN"
            if first_audio:
                audio_path = os.path.join(p, first_audio)
                try:
                    res = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format_tags=ARTIST,artist,ALBUMARTIST,albumartist,ALBUM,album', '-of', 'default=noprint_wrappers=1', audio_path], stdout=subprocess.PIPE, text=True)
                    artist_tag = res.stdout.replace('\n', ' | ')
                except Exception as e:
                    artist_tag = str(e)
            print(f"  Folder: {item} ({len(subfiles)} files) -> Tag: {artist_tag}")

print("\n=== CHECKING [Nemuri] Tōyama Nao 東山奈央 ===")
toyo_dir = os.path.join(BASE_DIR, "J-Pop", "T Shou Yama Nao 東山 Go (Tōyama Nao 東山奈央) ~")
if os.path.exists(toyo_dir):
    for root, dirs, files in os.walk(toyo_dir):
        rel = os.path.relpath(root, toyo_dir)
        audio = [f for f in files if f.endswith(('.flac', '.mp3'))]
        if audio:
            print(f"  Dir: {rel} ({len(audio)} audio files)")

print("\n=== CHECKING Reona ERAs ===")
reona_dir = os.path.join(BASE_DIR, "J-Pop", "Reona (レオナ) ~")
if os.path.exists(reona_dir):
    for item in sorted(os.listdir(reona_dir)):
        p = os.path.join(reona_dir, item)
        if os.path.isdir(p):
            subdirs = [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))]
            print(f"  {item}: subdirs={subdirs[:5]}... (total {len(subdirs)})")

print("\n=== CHECKING Bocchi the Rock! containers ===")
bocchi_dir = os.path.join(BASE_DIR, "Anime", "Bocchi the Rock! (結束バンド／ぼっち・ざ・ろっく！) ~")
if os.path.exists(bocchi_dir):
    for item in sorted(os.listdir(bocchi_dir)):
        p = os.path.join(bocchi_dir, item)
        if os.path.isdir(p):
            subdirs = [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))]
            print(f"  {item}: subdirs={subdirs}")
