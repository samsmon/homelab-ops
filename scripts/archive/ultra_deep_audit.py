#!/usr/bin/env python3
import os
import re
import unicodedata

BASE_DIR = "/mnt/hdd-backup/music/Lossless"

print("=" * 80)
print("ULTRA DEEP AUDIT OF /mnt/hdd-backup/music/Lossless")
print("=" * 80)

categories = ["Anime", "Doujinshi", "Game", "Global", "J-Pop", "Vocaloid", "Vtuber"]

# -------------------------------------------------------------
# AUDIT 1: Root items in each category not ending with '~'
# -------------------------------------------------------------
print("\n[AUDIT 1] Folders in Category Roots without Trailing '~'")
missing_tilde = []
for cat in categories:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for item in sorted(os.listdir(cat_dir)):
        if item.endswith('.m3u') or item.endswith('.m3u8') or item.startswith('.'):
            continue
        item_path = os.path.join(cat_dir, item)
        if os.path.isfile(item_path):
            print(f"  FILE in category root: [{cat}] {item}")
        elif not item.endswith("~"):
            missing_tilde.append((cat, item))
            print(f"  DIR without '~': [{cat}] {item}")

print(f"Total folders without trailing '~': {len(missing_tilde)}")

# -------------------------------------------------------------
# AUDIT 2: Single-level Artist Folders that might actually be loose albums
# -------------------------------------------------------------
print("\n[AUDIT 2] Artist Folders with Audio Files directly at Artist Root")
loose_audio_artists = []
for cat in categories:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for artist in sorted(os.listdir(cat_dir)):
        artist_dir = os.path.join(cat_dir, artist)
        if not os.path.isdir(artist_dir):
            continue
        audio_files = [f for f in os.listdir(artist_dir) if f.lower().endswith(('.flac', '.mp3', '.m4a', '.wav', '.ape', '.wv'))]
        if audio_files:
            loose_audio_artists.append((cat, artist, len(audio_files)))
            print(f"  [{cat}] {artist}: {len(audio_files)} loose audio files directly in artist root!")

print(f"Total artists with loose audio: {len(loose_audio_artists)}")

# -------------------------------------------------------------
# AUDIT 3: Date tags, codec tags, or bitrate tags in album folder names
# -------------------------------------------------------------
print("\n[AUDIT 3] Date / Codec / Bitrate / Year Tags in Album Folder Names")
bracket_regex = re.compile(r'\[(FLAC|MP3|Hi-Res|WEB|24bit|96kHz|48kHz|320k|\d{4}\.\d{2}\.\d{2}|\d{4}-\d{2}-\d{2})', re.IGNORECASE)
year_parens_regex = re.compile(r'\((19\d\d|20\d\d)\)')
album_tags_found = []

for cat in categories:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for artist in os.listdir(cat_dir):
        artist_dir = os.path.join(cat_dir, artist)
        if not os.path.isdir(artist_dir):
            continue
        for root, dirs, files in os.walk(artist_dir):
            for d in dirs:
                if bracket_regex.search(d) or year_parens_regex.search(d):
                    rel = os.path.relpath(os.path.join(root, d), BASE_DIR)
                    album_tags_found.append(rel)
                    if len(album_tags_found) <= 15:
                        print(f"  Tagged album folder: {rel}")

print(f"Total album folders with date/codec tags: {len(album_tags_found)}")

# -------------------------------------------------------------
# AUDIT 4: Nested duplicate folders (Artist/Artist or Album/Album or Disc 1/Disc 1)
# -------------------------------------------------------------
print("\n[AUDIT 4] Nested Duplicate Folder Names")
nested_dups = []
for cat in categories:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for artist in os.listdir(cat_dir):
        artist_dir = os.path.join(cat_dir, artist)
        if not os.path.isdir(artist_dir):
            continue
        for root, dirs, files in os.walk(artist_dir):
            parent = os.path.basename(root)
            for d in dirs:
                # check if d is almost identical to parent
                clean_d = re.sub(r'[\s\~\(\)\[\]]+', '', d).lower()
                clean_p = re.sub(r'[\s\~\(\)\[\]]+', '', parent).lower()
                if clean_d and clean_d == clean_p:
                    rel = os.path.relpath(os.path.join(root, d), BASE_DIR)
                    nested_dups.append(rel)
                    print(f"  Nested duplicate: {rel}")

print(f"Total nested duplicate folders: {len(nested_dups)}")

# -------------------------------------------------------------
# AUDIT 5: 0-Byte or Corrupted Audio Files
# -------------------------------------------------------------
print("\n[AUDIT 5] Zero-byte Files")
zero_byte_files = []
for cat in categories:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for root, dirs, files in os.walk(cat_dir):
        for f in files:
            fp = os.path.join(root, f)
            try:
                if os.path.getsize(fp) == 0:
                    rel = os.path.relpath(fp, BASE_DIR)
                    zero_byte_files.append(rel)
                    print(f"  0-byte file: {rel}")
            except Exception as e:
                print(f"  Error reading {fp}: {e}")

print(f"Total zero-byte files: {len(zero_byte_files)}")

# -------------------------------------------------------------
# AUDIT 6: Junk / Temporary / Torrent / Archive Files
# -------------------------------------------------------------
print("\n[AUDIT 6] Residual Junk / Archives / Torrent Metadata")
junk_exts = ('.rar', '.zip', '.7z', '.tar', '.gz', '.torrent', '.url', '.aria2', '.part', '.tmp', 'thumbs.db', '.ds_store')
junk_files = []
for cat in categories:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for root, dirs, files in os.walk(cat_dir):
        for f in files:
            if f.lower().endswith(junk_exts) or f.lower() in ('read.txt', 'discord.txt', 'instructions.txt', 'tracklist.txt'):
                rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
                junk_files.append(rel)
                if len(junk_files) <= 15:
                    print(f"  Junk file: {rel}")

print(f"Total junk/archive files: {len(junk_files)}")

# -------------------------------------------------------------
# AUDIT 7: Listing of ALL items in Anime/ to verify if any game/vtuber/jpop remains
# -------------------------------------------------------------
print("\n[AUDIT 7] Full Survey of Anime/ Category Umbrellas")
anime_dir = os.path.join(BASE_DIR, "Anime")
if os.path.exists(anime_dir):
    anime_items = sorted(os.listdir(anime_dir))
    print(f"Total umbrella folders in Anime/: {len(anime_items)}")
    for item in anime_items:
        p = os.path.join(anime_dir, item)
        subitems = [d for d in os.listdir(p) if not d.startswith('.')] if os.path.isdir(p) else []
        # Check if item name contains game keywords
        game_hints = ['chronicle', 'game', 'rpg', 'genshin', 'star rail', 'honkai', 'nikke', 'fgo', 'fate/grand order', 'atelier', 'neptunia', 'touhou', 'senren', 'yuzu-soft', 'visual novel']
        is_game_hint = any(h in item.lower() for h in game_hints)
        if is_game_hint:
            print(f"  [POTENTIAL GAME IN ANIME]: {item} ({len(subitems)} albums)")

# -------------------------------------------------------------
# AUDIT 8: Listing of ALL items in Game/ Category
# -------------------------------------------------------------
print("\n[AUDIT 8] Full Survey of Game/ Category")
game_dir = os.path.join(BASE_DIR, "Game")
if os.path.exists(game_dir):
    game_items = sorted(os.listdir(game_dir))
    print(f"Total franchises in Game/: {len(game_items)}")
    for item in game_items:
        p = os.path.join(game_dir, item)
        subitems = [d for d in os.listdir(p) if not d.startswith('.')] if os.path.isdir(p) else []
        print(f"  {item} ({len(subitems)} items)")

# -------------------------------------------------------------
# AUDIT 9: Check All Artist Folders Across All Categories for Mojibake / Non-ASCII First
# -------------------------------------------------------------
print("\n[AUDIT 9] Non-ASCII First Character Check")
non_ascii_first = []
for cat in categories:
    cat_dir = os.path.join(BASE_DIR, cat)
    if not os.path.exists(cat_dir):
        continue
    for item in sorted(os.listdir(cat_dir)):
        if item.endswith('.m3u') or item.endswith('.m3u8') or item.startswith('.'):
            continue
        first_char = item[0]
        if ord(first_char) >= 128:
            non_ascii_first.append((cat, item))
            print(f"  [{cat}] Non-ASCII First: {item}")

print(f"Total non-ASCII first folders: {len(non_ascii_first)}")

print("\n" + "=" * 80)
print("ULTRA DEEP AUDIT COMPLETED")
print("=" * 80)
