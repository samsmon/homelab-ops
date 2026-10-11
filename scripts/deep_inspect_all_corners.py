#!/usr/bin/env python3
import os
import re

BASE_DIR = "/mnt/hdd-backup/music"

print("=" * 80)
print("EXHAUSTIVE INSPECTION OF ALL CORNERS (Lossless & Lossy)")
print("=" * 80)

# 1. Inspect Lossy directory
lossy_dir = os.path.join(BASE_DIR, "Lossy")
if os.path.exists(lossy_dir):
    print("\n[LOSSY DIRECTORY SURVEY]")
    lossy_cats = os.listdir(lossy_dir)
    print(f"Categories in Lossy: {lossy_cats}")
    for cat in lossy_cats:
        cp = os.path.join(lossy_dir, cat)
        if os.path.isdir(cp):
            artists = os.listdir(cp)
            no_tilde = [a for a in artists if not a.endswith('~') and not a.startswith('.')]
            print(f"  [{cat}] {len(artists)} artists/folders, {len(no_tilde)} without tilde")
            if no_tilde:
                print(f"      No tilde examples: {no_tilde[:5]}")
else:
    print("\nLossy directory does not exist.")

# 2. Check all CUE files across Lossless
print("\n[CUE FILES IN LOSSLESS]")
cue_files = []
for root, dirs, files in os.walk(os.path.join(BASE_DIR, "Lossless")):
    for f in files:
        if f.lower().endswith('.cue'):
            rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
            cue_files.append(rel)
            print(f"  CUE: {rel}")
print(f"Total CUE files: {len(cue_files)}")

# 3. Check all WAV files across Lossless
print("\n[WAV FILES IN LOSSLESS]")
wav_files = []
for root, dirs, files in os.walk(os.path.join(BASE_DIR, "Lossless")):
    for f in files:
        if f.lower().endswith('.wav'):
            rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
            wav_files.append(rel)
            if len(wav_files) <= 15:
                print(f"  WAV: {rel}")
print(f"Total WAV files: {len(wav_files)}")

# 4. Check track filenames for mora raw IDs or strange patterns
print("\n[SUSPICIOUS AUDIO FILENAMES]")
suspicious_tracks = []
for root, dirs, files in os.walk(os.path.join(BASE_DIR, "Lossless")):
    for f in files:
        if f.lower().endswith(('.flac', '.mp3', '.m4a')):
            # check if starts with mora id like 1-0007... or _01_ or track01 or similar
            if re.match(r'^\d+-\d{4,}', f) or re.match(r'^track\d+', f, re.I) or f.startswith('._'):
                rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
                suspicious_tracks.append(rel)
                if len(suspicious_tracks) <= 15:
                    print(f"  Suspicious track name: {rel}")
print(f"Total suspicious audio tracks: {len(suspicious_tracks)}")

# 5. Check if any artist in J-Pop is actually Anime/Game/Vtuber
print("\n[CHECKING J-POP ARTISTS FOR UNMATCHED AGENCIES OR CHARACTER SONGS]")
jpop_dir = os.path.join(BASE_DIR, "Lossless", "J-Pop")
if os.path.exists(jpop_dir):
    for artist in sorted(os.listdir(jpop_dir)):
        ap = os.path.join(jpop_dir, artist)
        if not os.path.isdir(ap):
            continue
        # check for CV or character song hints
        if 'cv.' in artist.lower() or 'cv:' in artist.lower() or 'character' in artist.lower():
            print(f"  CV in J-Pop: {artist}")
        # check for VTuber keywords
        if any(vk in artist.lower() for vk in ['channel', 'vtuber', 'project', 'virtual']):
            print(f"  VTuber keyword in J-Pop: {artist}")

# 6. Check if any artist in Anime is actually a Game
print("\n[CHECKING ANIME FOR MOBILE / CONSOLE GAMES]")
anime_dir = os.path.join(BASE_DIR, "Lossless", "Anime")
game_candidates = [
    "IDOLiSH7 (アイドリッシュセブン) ~",
    "Idoly Pride (アイドリープライド) ~",
    "Lapis ReLiGHTs ~",
    "LiveRevolt ~",
    "Tokyo 7th Sisters (Tokyo 7th シスターズ) ~"
]
for gc in game_candidates:
    gp = os.path.join(anime_dir, gc)
    if os.path.exists(gp):
        print(f"  Game candidate in Anime: {gc}")

# 7. Check Doujinshi artists count & survey
print("\n[DOUJINSHI SURVEY]")
doujin_dir = os.path.join(BASE_DIR, "Lossless", "Doujinshi")
if os.path.exists(doujin_dir):
    d_artists = sorted(os.listdir(doujin_dir))
    print(f"Total artists in Doujinshi: {len(d_artists)}")
    for da in d_artists[:10]:
        print(f"  {da}")
    if len(d_artists) > 10:
        print(f"  ... and {len(d_artists) - 10} more")

# 8. Check Vocaloid artists count & survey
print("\n[VOCALOID SURVEY]")
voc_dir = os.path.join(BASE_DIR, "Lossless", "Vocaloid")
if os.path.exists(voc_dir):
    v_artists = sorted(os.listdir(voc_dir))
    print(f"Total artists in Vocaloid: {len(v_artists)}")
    for va in v_artists:
        print(f"  {va}")

# 9. Check Vtuber agencies count & survey
print("\n[VTUBER SURVEY]")
vtuber_dir = os.path.join(BASE_DIR, "Lossless", "Vtuber")
if os.path.exists(vtuber_dir):
    vt_items = sorted(os.listdir(vtuber_dir))
    print(f"Total items in Vtuber: {len(vt_items)}")
    for vti in vt_items:
        print(f"  {vti}")
