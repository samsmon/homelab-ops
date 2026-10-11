#!/usr/bin/env python3
import os

p_backup = "/mnt/hdd-backup/music/Lossless"
p_music = "/mnt/hdd-music/music/Lossless"

print("Comparing top-level directories between hdd-backup and hdd-music...")
backup_cats = set(os.listdir(p_backup))
music_cats = set(os.listdir(p_music))

print(f"Categories in backup: {backup_cats}")
print(f"Categories in music: {music_cats}")
print(f"Difference: {backup_cats ^ music_cats}")

# Check top folders in Anime
for cat in backup_cats & music_cats:
    b_dirs = set(os.listdir(os.path.join(p_backup, cat)))
    m_dirs = set(os.listdir(os.path.join(p_music, cat)))
    diff_bm = b_dirs - m_dirs
    diff_mb = m_dirs - b_dirs
    print(f"\n[{cat}] Backup has {len(b_dirs)}, Music has {len(m_dirs)}")
    if diff_bm:
        print(f"  Only in backup ({len(diff_bm)}): {list(diff_bm)[:5]}")
    if diff_mb:
        print(f"  Only in music ({len(diff_mb)}): {list(diff_mb)[:5]}")
