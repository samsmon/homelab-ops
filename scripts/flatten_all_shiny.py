#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

BASE = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER ~/シャイニーカラーズ')
AUDIO_EXTS = {'.flac', '.aiff', '.aif', '.alac', '.wav', '.m4a', '.mp3'}

def get_album_dirs():
    albums = []
    for cat in BASE.iterdir():
        if not cat.is_dir():
            continue
        subdirs = [d for d in cat.iterdir() if d.is_dir()]
        has_subseries = any(d.name.startswith(('01.', '02.', '03.', '04.', '05.', '06.', '07.')) for d in subdirs)
        if has_subseries:
            for sub in subdirs:
                for alb in sub.iterdir():
                    if alb.is_dir():
                        albums.append(alb)
        else:
            for alb in subdirs:
                if alb.is_dir():
                    albums.append(alb)
    return albums

def flatten_album(alb: Path):
    # Check if multi-disc
    subdirs = [d for d in alb.iterdir() if d.is_dir()]
    if any(d.name.lower().startswith('disc') for d in subdirs):
        return # keep multi-disc intact

    # Extract any inner zips (booklets)
    for z in list(alb.rglob('*.zip')):
        bk_dir = alb / 'BK'
        bk_dir.mkdir(exist_ok=True)
        subprocess.run(['unzip', '-q', '-o', str(z), '-d', str(bk_dir)], check=False)
        z.unlink()

    # Move all audio files to alb root
    for f in list(alb.rglob('*')):
        if f.is_file() and f.suffix.lower() in AUDIO_EXTS:
            if f.parent != alb:
                dest = alb / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))

    # Move order receipts to BK
    for f in list(alb.glob('order*.*')):
        bk_dir = alb / 'BK'
        bk_dir.mkdir(exist_ok=True)
        dest = bk_dir / f.name
        if not dest.exists():
            shutil.move(str(f), str(dest))

    # Handle covers
    has_cover = any(f.name.lower() in ['cover.jpg', 'cover.png', 'folder.jpg'] for f in alb.glob('*'))
    for img in list(alb.rglob('*')):
        if img.is_file() and img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            if img.parent != alb and not str(img.parent).endswith('/BK'):
                if not has_cover:
                    shutil.move(str(img), str(alb / 'Cover.jpg'))
                    has_cover = True
                else:
                    bk_dir = alb / 'BK'
                    bk_dir.mkdir(exist_ok=True)
                    dest = bk_dir / img.name
                    if not dest.exists():
                        shutil.move(str(img), str(dest))

    # Remove empty directories
    for root, dirs, files in os.walk(alb, topdown=False):
        for d in dirs:
            dp = Path(root) / d
            if dp.name != 'BK' and not any(dp.iterdir()):
                try:
                    dp.rmdir()
                except Exception:
                    pass

if __name__ == '__main__':
    albums = get_album_dirs()
    print(f"Flattening and validating {len(albums)} albums...")
    for a in albums:
        flatten_album(a)

    print("Fixing permissions (100000:100000, 775/664)...")
    subprocess.run(['chown', '-R', '100000:100000', str(BASE)], check=False)
    subprocess.run(['find', str(BASE), '-type', 'd', '-exec', 'chmod', '775', '{}', '+'], check=False)
    subprocess.run(['find', str(BASE), '-type', 'f', '-exec', 'chmod', '664', '{}', '+'], check=False)
    print("Done!")
