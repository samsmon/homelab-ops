import os
import shutil
import subprocess

LOSSLESS = "/mnt/hdd-backup/music/Lossless"
LOSSY = "/mnt/hdd-backup/music/Lossy"

print("=" * 60)
print("STARTING ROUND 152 EXECUTION")
print("=" * 60)

# ==============================================================================
# PHASE 1: Un-nest Vtuber/Other ~
# ==============================================================================
print("\n--- PHASE 1: Un-nest Vtuber/Other ~ ---")
other_dir = os.path.join(LOSSLESS, "Vtuber", "Other ~")
vtuber_root = os.path.join(LOSSLESS, "Vtuber")

if os.path.exists(other_dir):
    for item in os.listdir(other_dir):
        src = os.path.join(other_dir, item)
        dst = os.path.join(vtuber_root, item)
        if not os.path.exists(dst):
            print(f"  Moving '{item}' -> Vtuber root")
            shutil.move(src, dst)
        else:
            print(f"  [WARN] Destination '{dst}' already exists, merging...")
            for sub in os.listdir(src):
                shutil.move(os.path.join(src, sub), os.path.join(dst, sub))
            shutil.rmtree(src)
    try:
        os.rmdir(other_dir)
        print("  Removed empty Vtuber/Other ~")
    except Exception as e:
        print(f"  Could not remove {other_dir}: {e}")
else:
    print("  Vtuber/Other ~ already un-nested.")


# ==============================================================================
# PHASE 2: Normalize Zhu Luo Qiu Xiang Album Name
# ==============================================================================
print("\n--- PHASE 2: Normalize Zhu Luo Qiu Xiang Album Name ---")
zhu_artist = os.path.join(LOSSLESS, "Doujinshi", "Zhu Luo Qiu Xiang (朱落秋乡) ~")
old_album = os.path.join(zhu_artist, "2018.12.15 [SWCD-009] 朱落秋乡 [COMICUP23]")
new_album = os.path.join(zhu_artist, "朱落秋乡 [COMICUP23] {SWCD-009}")

if os.path.exists(old_album):
    shutil.move(old_album, new_album)
    print(f"  Renamed '{os.path.basename(old_album)}' -> '{os.path.basename(new_album)}'")
else:
    print("  Old album name not found or already renamed.")


# ==============================================================================
# PHASE 3: Purge In-Album Playlist Clutter (.m3u/.m3u8)
# ==============================================================================
print("\n--- PHASE 3: Purge In-Album Playlist Clutter ---")
master_m3u8 = os.path.join(LOSSLESS, "Lossless.m3u8")
m3u_count = 0

for root, dirs, files in os.walk(LOSSLESS):
    for f in files:
        if f.lower().endswith(('.m3u', '.m3u8')):
            fp = os.path.join(root, f)
            if fp != master_m3u8:
                try:
                    os.remove(fp)
                    m3u_count += 1
                except Exception as e:
                    print(f"  Failed to delete {fp}: {e}")

print(f"  Purged {m3u_count} in-album .m3u/.m3u8 playlist clutter files.")


# ==============================================================================
# PHASE 4: Purge Redundant Albums from Lossy/
# ==============================================================================
print("\n--- PHASE 4: Purge Redundant Duplicate Albums from Lossy/ ---")
# List of known target directories in Lossy that duplicate Lossless FLACs
lossy_targets = [
    os.path.join(LOSSY, "Anime", "Azurlane"),
    os.path.join(LOSSY, "Anime", "Assault Lily", "Edel Lilie"),
    os.path.join(LOSSY, "Anime", "Princess Principal", "Princess Principal THE LIVE Yuki Kajiura×Void_Chords"),
    os.path.join(LOSSY, "Anime", "Tokyo 7th Sisters", "Tokyo 7th Sisters Memorial Live in NIPPON BUDOKAN Melody in the Pocket"),
    os.path.join(LOSSY, "Anime", "Gochiusa", "Gochuumon wa Usagi Desuka Sing for You Bonus CDs"),
    os.path.join(LOSSY, "Anime", "Gochiusa", "Gochuumon wa Usagi desu ka ~Dear My Sister~ Bonus Disc"),
    os.path.join(LOSSY, "Doujinshi", "KINEMA106 5th ANNIVERSARY COMPLETE BOX"),
    os.path.join(LOSSY, "Doujinshi", "KINEMA 5th ANNIVERSARY COMPLETE BOX"),
    os.path.join(LOSSY, "Doujinshi", "Bassy - 現代ポップスC & 続・現代ポップスC"),
]

for t in lossy_targets:
    if os.path.exists(t):
        try:
            shutil.rmtree(t)
            print(f"  Purged redundant lossy album: {os.path.relpath(t, LOSSY)}")
        except Exception as e:
            print(f"  Failed to delete {t}: {e}")

# Clean up empty parent directories in Lossy
for root, dirs, files in os.walk(LOSSY, topdown=False):
    if not dirs and not files and root != LOSSY:
        try:
            os.rmdir(root)
            print(f"  Cleaned empty lossy dir: {os.path.relpath(root, LOSSY)}")
        except Exception:
            pass

print("\nEXECUTION FINISHED!")
