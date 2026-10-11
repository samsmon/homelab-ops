#!/usr/bin/env python3
"""
Comprehensive Deep Audit Script for /mnt/hdd-backup/music/Lossless
Saves full report to /tmp/audit_lossless_report.json and prints summary.
"""

import os
import sys
import re
import json
from collections import defaultdict
from pathlib import Path

BASE = '/mnt/hdd-backup/music/Lossless'
CATEGORIES = ['Anime', 'Doujinshi', 'J-Pop', 'Vtuber', 'Vocaloid', 'Global']

JP_CHAR_RE = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]')
LATIN_RE = re.compile(r'[a-zA-Z]')

DATE_PREFIX_RE = re.compile(r'^\[\s*\d{2,4}[.\-\s]\d{1,2}[.\-\s]\d{1,2}\s*\]\s*')
YEAR_PAREN_RE = re.compile(r'[\(\[]\s*(19\d{2}|20\d{2})\s*[\)\]]')
AUDIO_TAG_RE = re.compile(
    r'\[\s*(FLAC|WEB-FLAC|Hi-Res|MP3|AAC|WAV|DSD|CD-FLAC|\d+kHz[\/／]\d+bit|\d+bit[\/／]\d+kHz|\d+k)[\w\s\+\/／\-]*\]',
    re.IGNORECASE
)

def sanitize_pure_album(folder_name):
    name = folder_name
    name = DATE_PREFIX_RE.sub('', name)
    name = YEAR_PAREN_RE.sub('', name)
    name = AUDIO_TAG_RE.sub('', name)
    name = re.sub(r'\[(FLAC|WEB|Hi-Res|CD)\]', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def main():
    report = {
        "top_folders_by_cat": {},
        "missing_tilde": [],
        "jp_first_folders": [],
        "pure_jp_folders": [],
        "container_folders": [],
        "deep_nested_paths": [],
        "loose_tracks": [],
        "empty_dirs": [],
        "non_flac_audio": [],
        "video_files": [],
        "archive_files": [],
        "cue_images": [],
        "multi_disc_albums": [],
        "collisions": {},
        "stats": {}
    }

    all_tracks_count = 0
    uid_gid_issues = 0
    perm_issues = 0

    for cat in CATEGORIES:
        cat_path = os.path.join(BASE, cat)
        if not os.path.isdir(cat_path):
            continue
        
        entries = sorted(os.listdir(cat_path))
        report["top_folders_by_cat"][cat] = entries
        
        for top_f in entries:
            top_p = os.path.join(cat_path, top_f)
            if not os.path.isdir(top_p):
                report["loose_tracks"].append({"path": f"{cat}/{top_f}", "count": 1})
                continue
            
            # Check trailing tilde
            if not top_f.endswith(' ~'):
                report["missing_tilde"].append({"category": cat, "folder": top_f})
            
            # Check Japanese first
            clean_name = re.sub(r'\s*~\s*$', '', top_f).strip()
            first_c = clean_name[0] if clean_name else ''
            if JP_CHAR_RE.match(first_c):
                if '(' in clean_name or '（' in clean_name:
                    report["jp_first_folders"].append({"category": cat, "folder": top_f})
                else:
                    report["pure_jp_folders"].append({"category": cat, "folder": top_f})
            
            # Collect album folders for collision check
            artist_albums = []

            for root, dirs, files in os.walk(top_p):
                rel_root = os.path.relpath(root, top_p)
                depth = len(Path(rel_root).parts) if rel_root != '.' else 0
                basename = os.path.basename(root)

                # Empty dir
                if not dirs and not files:
                    report["empty_dirs"].append(root)
                    continue

                # Loose audio in artist root
                audio_in_dir = [f for f in files if f.lower().endswith(('.flac', '.wav', '.mp3', '.m4a', '.ogg', '.opus'))]
                if depth == 0 and audio_in_dir:
                    report["loose_tracks"].append({"path": f"{cat}/{top_f}", "count": len(audio_in_dir)})

                # Container folders
                if depth > 0 and re.search(r'(ERA\s*\d+|LIVE\s*&|Collection|Singles|Albums|Discography)', basename, re.IGNORECASE):
                    # verify it has subdirectories
                    if dirs:
                        report["container_folders"].append(root)

                # Deep nesting
                if depth >= 3:
                    report["deep_nested_paths"].append({"path": root, "depth": depth})

                # Multi-disc
                if re.match(r'^(Disc|CD)\s*\d+$', basename, re.IGNORECASE):
                    report["multi_disc_albums"].append(root)

                # CUE check
                cue_files = [f for f in files if f.lower().endswith('.cue')]
                flac_wav_files = [f for f in files if f.lower().endswith(('.flac', '.wav'))]
                if cue_files and len(flac_wav_files) <= len(cue_files):
                    for cf in cue_files:
                        report["cue_images"].append({"folder": root, "cue": cf, "audio": flac_wav_files})

                # Check album folder (dirs directly containing audio or multi-disc subdirs)
                if any(f.lower().endswith('.flac') for f in files):
                    # If this is inside a Disc 1/CD1 folder, the album folder is parent
                    album_dir = os.path.dirname(root) if re.match(r'^(Disc|CD)\s*\d+$', basename, re.IGNORECASE) else root
                    if album_dir != top_p and album_dir not in artist_albums:
                        artist_albums.append(album_dir)

                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    fp = os.path.join(root, f)
                    
                    if ext in ('.mp3', '.wav', '.m4a', '.aac', '.ogg', '.opus', '.ape', '.wv', '.dsf', '.dff'):
                        report["non_flac_audio"].append(fp)
                    elif ext in ('.mkv', '.mp4', '.avi', '.ts', '.m2ts', '.webm', '.mov'):
                        sz = os.path.getsize(fp) / (1024 * 1024)
                        report["video_files"].append({"path": fp, "size_mb": round(sz, 1)})
                    elif ext in ('.zip', '.7z', '.rar', '.tar', '.gz'):
                        sz = os.path.getsize(fp) / (1024 * 1024)
                        report["archive_files"].append({"path": fp, "size_mb": round(sz, 1)})
                    elif ext == '.flac':
                        all_tracks_count += 1

                    # Ownership
                    try:
                        st = os.stat(fp)
                        if st.st_uid != 100000 or st.st_gid != 100000:
                            uid_gid_issues += 1
                        if (st.st_mode & 0o777) != 0o664:
                            perm_issues += 1
                    except Exception:
                        pass

            # Check collisions within this artist
            pure_map = defaultdict(list)
            for ad in artist_albums:
                bname = os.path.basename(ad)
                pure = sanitize_pure_album(bname)
                pure_map[pure].append(ad)
            
            collisions = {k: v for k, v in pure_map.items() if len(v) > 1}
            if collisions:
                report["collisions"][f"{cat}/{top_f}"] = collisions

    report["stats"] = {
        "all_tracks_count": all_tracks_count,
        "uid_gid_issues": uid_gid_issues,
        "perm_issues": perm_issues
    }

    with open('/tmp/audit_lossless_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("Audit completed successfully! Report saved to /tmp/audit_lossless_report.json")
    print(f"Total top folders: {sum(len(v) for v in report['top_folders_by_cat'].values())}")
    print(f"Missing tilde: {len(report['missing_tilde'])}")
    print(f"Japanese first: {len(report['jp_first_folders'])}")
    print(f"Pure Japanese: {len(report['pure_jp_folders'])}")
    print(f"Container folders: {len(report['container_folders'])}")
    print(f"Deep nested paths: {len(report['deep_nested_paths'])}")
    print(f"Loose tracks: {len(report['loose_tracks'])}")
    print(f"Empty dirs: {len(report['empty_dirs'])}")
    print(f"Non-FLAC audio: {len(report['non_flac_audio'])}")
    print(f"Video files: {len(report['video_files'])}")
    print(f"Archives: {len(report['archive_files'])}")
    print(f"Unsplit CUE images: {len(report['cue_images'])}")
    print(f"Multi-disc folders: {len(report['multi_disc_albums'])}")
    print(f"Artists with Pure Album collisions: {len(report['collisions'])}")
    print(f"Total FLAC tracks: {all_tracks_count}")
    print(f"UID/GID != 100000: {uid_gid_issues}")

if __name__ == '__main__':
    main()
