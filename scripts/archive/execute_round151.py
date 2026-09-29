import os
import re
import shutil
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=" * 60)
print("STARTING ROUND 151 EXECUTION")
print("=" * 60)

# ==============================================================================
# PHASE 1: nayuta consolidation
# ==============================================================================
print("\n--- PHASE 1: Consolidate nayuta (7uta.com) ---")
uta_dir = os.path.join(ROOT, "J-Pop", "7uta ~")
nayuta_dir = os.path.join(ROOT, "Doujinshi", "nayuta ~")

if os.path.exists(uta_dir):
    os.makedirs(nayuta_dir, exist_ok=True)
    for album in sorted(os.listdir(uta_dir)):
        src = os.path.join(uta_dir, album)
        dst = os.path.join(nayuta_dir, album)
        if os.path.exists(dst):
            print(f"  [WARN] Destination already exists: {dst}")
        else:
            print(f"  Moving {album} -> Doujinshi/nayuta ~")
            shutil.move(src, dst)
    # Remove empty 7uta ~
    try:
        os.rmdir(uta_dir)
        print("  Removed empty J-Pop/7uta ~")
    except Exception as e:
        print(f"  Could not remove J-Pop/7uta ~: {e}")
else:
    print("  J-Pop/7uta ~ not found or already moved.")


# ==============================================================================
# PHASE 2: ONGEKI Consolidation
# ==============================================================================
print("\n--- PHASE 2: Consolidate ONGEKI Franchise ---")
canonical_ongeki = os.path.join(ROOT, "Game", "ONGEKI (オンゲキ) ~")
os.makedirs(canonical_ongeki, exist_ok=True)

# 2a. Move SEGA Game Music ~ to Game/ root
sega_arcade_root = os.path.join(ROOT, "Game", "SEGA & Arcade Games ~")
sega_game_music_src = os.path.join(sega_arcade_root, "SEGA Game Music ~")
sega_game_music_dst = os.path.join(ROOT, "Game", "SEGA Game Music ~")

if os.path.exists(sega_game_music_src):
    if not os.path.exists(sega_game_music_dst):
        print(f"  Moving SEGA Game Music ~ to Game/ root")
        shutil.move(sega_game_music_src, sega_game_music_dst)
    else:
        # Merge if exists
        for item in os.listdir(sega_game_music_src):
            shutil.move(os.path.join(sega_game_music_src, item), os.path.join(sega_game_music_dst, item))
        shutil.rmtree(sega_game_music_src)

# 2b. Move albums from SEGA & Arcade Games ~/ONGEKI (オンゲキ) ~ into canonical
sega_ongeki_src = os.path.join(sega_arcade_root, "ONGEKI (オンゲキ) ~")
if os.path.exists(sega_ongeki_src):
    for item in sorted(os.listdir(sega_ongeki_src)):
        s = os.path.join(sega_ongeki_src, item)
        d = os.path.join(canonical_ongeki, item)
        if not os.path.exists(d):
            print(f"  Moving SEGA ONGEKI album '{item}' -> canonical")
            shutil.move(s, d)
        else:
            print(f"  [WARN] Canonical already has '{item}', skipping or manual merge needed")
    try:
        os.rmdir(sega_ongeki_src)
        print("  Removed empty SEGA & Arcade Games ~/ONGEKI (オンゲキ) ~")
    except Exception as e:
        print(f"  Could not remove SEGA ONGEKI src: {e}")

# Remove SEGA & Arcade Games ~ if empty
try:
    if os.path.exists(sega_arcade_root) and not os.listdir(sega_arcade_root):
        os.rmdir(sega_arcade_root)
        print("  Removed empty Game/SEGA & Arcade Games ~")
except Exception as e:
    print(f"  Could not remove sega_arcade_root: {e}")

# 2c. Process Game/O.N.G.E.K.I. (オンゲキ) ~
old_ongeki_root = os.path.join(ROOT, "Game", "O.N.G.E.K.I. (オンゲキ) ~")

# Handle ONGEKI 6th Anniversary Hi-Res upgrade first
ongeki_6th_hi_res = os.path.join(old_ongeki_root, "ONGEKI Collection", "2024.07.26 [ZMCZ-17641] ONGEKI 6th Anniversary CD 「Individual on parade!」")
ongeki_6th_16bit = os.path.join(old_ongeki_root, "ONGEKI 6th Anniversary CD「Individual on parade!」")
canonical_6th = os.path.join(canonical_ongeki, "ONGEKI 6th Anniversary CD「Individual on parade!」")

if os.path.exists(ongeki_6th_hi_res):
    print("  Processing ONGEKI 6th Anniversary 24-bit Hi-Res upgrade...")
    os.makedirs(canonical_6th, exist_ok=True)
    # The 24-bit files in hi-res folder are formatted as '01-Individual on parade!.flac', etc.
    # Check all files in hi-res folder
    for f in os.listdir(ongeki_6th_hi_res):
        fp = os.path.join(ongeki_6th_hi_res, f)
        # Check if it's the 24-bit version (starts with \d\d- and has size > 40MB)
        m = re.match(r'^(\d{2})-(.*\.flac)$', f)
        if m:
            num = m.group(1)
            title = m.group(2)
            new_name = f"{num}. {title}"
            dst_file = os.path.join(canonical_6th, new_name)
            shutil.move(fp, dst_file)
            print(f"    Moved Hi-Res track: {new_name}")
        elif f.lower().endswith(('.jpg', '.png', '.jpeg')):
            dst_file = os.path.join(canonical_6th, f)
            if not os.path.exists(dst_file):
                shutil.copy2(fp, dst_file)
    # Also rescue Front.jpg from 16-bit folder if needed
    if os.path.exists(ongeki_6th_16bit):
        front_jpg = os.path.join(ongeki_6th_16bit, "Front.jpg")
        if os.path.exists(front_jpg) and not os.path.exists(os.path.join(canonical_6th, "Cover.jpg")):
            shutil.copy2(front_jpg, os.path.join(canonical_6th, "Cover.jpg"))
        # Remove redundant 16-bit folder
        shutil.rmtree(ongeki_6th_16bit)
        print("    Purged redundant 16-bit ONGEKI 6th folder.")
    # Remove hi-res src folder
    shutil.rmtree(ongeki_6th_hi_res)

# Handle ONGEKI Sound Memory (flatten nested CD)
sound_mem_src = os.path.join(old_ongeki_root, "ONGEKI Collection", "2024.03.27 [ZMCZ-17041] ONGEKI Sound Memory")
sound_mem_dst = os.path.join(canonical_ongeki, "ONGEKI Sound Memory {ZMCZ-17041}")
if os.path.exists(sound_mem_src):
    os.makedirs(sound_mem_dst, exist_ok=True)
    cd_dir = os.path.join(sound_mem_src, "CD")
    if os.path.exists(cd_dir):
        for f in os.listdir(cd_dir):
            shutil.move(os.path.join(cd_dir, f), os.path.join(sound_mem_dst, f))
    for f in os.listdir(sound_mem_src):
        fp = os.path.join(sound_mem_src, f)
        if os.path.isfile(fp):
            shutil.move(fp, os.path.join(sound_mem_dst, f))
    shutil.rmtree(sound_mem_src)
    print("    Flattened and moved ONGEKI Sound Memory {ZMCZ-17041}")

# Handle Southern Cross
sc_src = os.path.join(old_ongeki_root, "ONGEKI Collection", "2024.06.20 ONGEKI Memorial Soundtrack Nexture 03「Southern Cross」")
sc_dst = os.path.join(canonical_ongeki, "ONGEKI Memorial Soundtrack Nexture 03「Southern Cross」")
if os.path.exists(sc_src):
    shutil.move(sc_src, sc_dst)
    print("    Moved Southern Cross to canonical ONGEKI")

# Handle Sound Jewelry 01
sj1_src = os.path.join(old_ongeki_root, "ONGEKI Collection", "2024.08.10 [WM-0877] ONGEKI Sound Jewelry 01")
sj1_dst = os.path.join(canonical_ongeki, "ONGEKI Sound Jewelry 01 {WM-0877}")
if os.path.exists(sj1_src):
    shutil.move(sj1_src, sj1_dst)
    print("    Moved Sound Jewelry 01 {WM-0877} to canonical ONGEKI")

# Remove ONGEKI Collection if empty
col_dir = os.path.join(old_ongeki_root, "ONGEKI Collection")
if os.path.exists(col_dir):
    try:
        shutil.rmtree(col_dir)
        print("    Removed ONGEKI Collection container.")
    except Exception as e:
        print(f"    Could not remove ONGEKI Collection: {e}")

# Process remaining albums in O.N.G.E.K.I. (オンゲキ) ~
if os.path.exists(old_ongeki_root):
    for item in sorted(os.listdir(old_ongeki_root)):
        src = os.path.join(old_ongeki_root, item)
        if not os.path.isdir(src):
            continue
        # Format name
        m = re.match(r'^\d{4}\.\d{2}\.\d{2}\s+(?:\[(.*?)\]\s+)?(.*)$', item)
        if m:
            cat = m.group(1)
            title = m.group(2)
            if cat:
                clean_name = f"{title} {{{cat}}}"
            else:
                clean_name = title
        else:
            clean_name = item
        
        dst = os.path.join(canonical_ongeki, clean_name)
        if not os.path.exists(dst):
            print(f"  Moving & Renaming '{item}' -> '{clean_name}'")
            shutil.move(src, dst)
        else:
            print(f"  [WARN] Target already exists: '{clean_name}'")
            for sub_f in os.listdir(src):
                s_fp = os.path.join(src, sub_f)
                d_fp = os.path.join(dst, sub_f)
                if not os.path.exists(d_fp):
                    shutil.move(s_fp, d_fp)
            shutil.rmtree(src)
    
    # Remove empty old_ongeki_root
    try:
        if not os.listdir(old_ongeki_root):
            os.rmdir(old_ongeki_root)
            print("  Successfully removed empty Game/O.N.G.E.K.I. (オンゲキ) ~")
    except Exception as e:
        print(f"  Could not remove old ONGEKI root: {e}")


# ==============================================================================
# PHASE 3: Shiny Colors AIFF & WV Conversion & Cleanup
# ==============================================================================
print("\n--- PHASE 3: Shiny Colors AIFF & WV Conversion ---")
shiny_root = os.path.join(ROOT, "Anime", "THE IDOLM@STER (アイドルマスター) ~", "Shiny Colors (シャイニーカラーズ) ~")

# 3a. Purge redundant duplicate folder Spread the Wings!!
dup_spread = os.path.join(shiny_root, "01. WING & Main Game Series", "01. BRILLI@NT WING", "Spread the Wings!!")
if os.path.exists(dup_spread):
    shutil.rmtree(dup_spread)
    print("  Purged redundant duplicate folder: 01. BRILLI@NT WING/Spread the Wings!!")

# 3b. Find and convert all AIFF and WV files
to_convert = []
for root, dirs, files in os.walk(shiny_root):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.aiff', '.aif', '.wv']:
            to_convert.append(os.path.join(root, f))

print(f"  Total files to convert: {len(to_convert)}")

success_count = 0
fail_count = 0

for idx, src_fp in enumerate(to_convert, 1):
    base, ext = os.path.splitext(src_fp)
    dst_flac = base + ".flac"
    cmd = [
        "ffmpeg", "-y", "-i", src_fp,
        "-c:a", "flac", "-compression_level", "8",
        dst_flac
    ]
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode == 0 and os.path.exists(dst_flac) and os.path.getsize(dst_flac) > 0:
        # Verify flac
        v = subprocess.run(["flac", "-t", dst_flac], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if v.returncode == 0:
            os.remove(src_fp)
            success_count += 1
            if idx % 10 == 0 or idx == len(to_convert):
                print(f"    Progress: {idx}/{len(to_convert)} converted and verified.")
        else:
            print(f"    [FAIL VERIFY] {dst_flac}")
            os.remove(dst_flac)
            fail_count += 1
    else:
        print(f"    [FAIL ENCODE] {src_fp}: {r.stderr.decode('utf-8', errors='ignore')[:100]}")
        fail_count += 1

print(f"  Conversion complete: {success_count} succeeded, {fail_count} failed.")


# ==============================================================================
# PHASE 4: Purge MP3s, Clutter & Case Collisions
# ==============================================================================
print("\n--- PHASE 4: Purge MP3s, Clutter & Case Collisions ---")

# 4a. Duplicate MP3s
dup_mp3s = [
    os.path.join(ROOT, "Anime/BanG Dream! (バンドリ！) ~/Morfonica ~/ビューティ・フォー/01. ビューティ・フォー.mp3"),
    os.path.join(ROOT, "Vtuber/KAMITSUBAKI STUDIO (神椿スタジオ) ~/Koko (幸祜) ~/Prayer/mcard-bonustracks/Hana_to_mitsu.mp3"),
    os.path.join(ROOT, "Vtuber/KAMITSUBAKI STUDIO (神椿スタジオ) ~/Koko (幸祜) ~/Prayer/mcard-bonustracks/Senoko_no_kanata.mp3"),
]
# Add 8 MP3s in Fuling Cat Mark
fuling_dir = os.path.join(ROOT, "J-Pop/Fuling Cat Mark (フーリンキャットマーク) ~/ルチア")
if os.path.exists(fuling_dir):
    for f in os.listdir(fuling_dir):
        if f.lower().endswith('.mp3'):
            dup_mp3s.append(os.path.join(fuling_dir, f))

for m in dup_mp3s:
    if os.path.exists(m):
        os.remove(m)
        print(f"  Deleted duplicate MP3: {os.path.basename(m)}")

# 4b. Transcode La Priere bonus track
lp_bonus_mp3 = os.path.join(ROOT, "Vtuber/La Prière ~/Galaxy Triangle/Bonus Track.mp3")
lp_bonus_flac = os.path.join(ROOT, "Vtuber/La Prière ~/Galaxy Triangle/08. mogetama.flac")
if os.path.exists(lp_bonus_mp3):
    r = subprocess.run([
        "ffmpeg", "-y", "-i", lp_bonus_mp3,
        "-c:a", "flac", "-compression_level", "8",
        lp_bonus_flac
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode == 0 and os.path.exists(lp_bonus_flac):
        os.remove(lp_bonus_mp3)
        print("  Converted La Prière Bonus Track.mp3 -> 08. mogetama.flac")

# 4c. Delete .log and .accurip files
clutter_to_delete = []
for root, dirs, files in os.walk(ROOT):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.log', '.accurip']:
            clutter_to_delete.append(os.path.join(root, f))

for c in clutter_to_delete:
    try:
        os.remove(c)
        print(f"  Deleted clutter: {os.path.relpath(c, ROOT)}")
    except Exception as e:
        print(f"  Failed to delete {c}: {e}")

# 4d. Resolve Case Collisions
print("  Resolving case collisions (cover.jpg vs Cover.jpg)...")
for root, dirs, files in os.walk(ROOT):
    lower_map = {}
    for f in files:
        fl = f.lower()
        if fl in lower_map:
            # Case collision!
            f1 = lower_map[fl]
            f2 = f
            fp1 = os.path.join(root, f1)
            fp2 = os.path.join(root, f2)
            # If one is lowercase 'cover.jpg' and one has uppercase 'Cover.jpg' or 'COVER.jpg'
            if f1 == 'cover.jpg' and f2 in ['Cover.jpg', 'COVER.jpg']:
                if os.path.exists(fp1):
                    os.remove(fp1)
                    print(f"    Removed lowercase collision: {fp1}")
            elif f2 == 'cover.jpg' and f1 in ['Cover.jpg', 'COVER.jpg']:
                if os.path.exists(fp2):
                    os.remove(fp2)
                    print(f"    Removed lowercase collision: {fp2}")
        else:
            lower_map[fl] = f

print("\nEXECUTION FINISHED!")
