import os
import re
import subprocess

ROOT_LOSSLESS = "/mnt/hdd-backup/music/Lossless"
ROOT_LOSSY = "/mnt/hdd-backup/music/Lossy"

print("=" * 70)
print("MASTER ZERO-DEFECT AUDIT (ROUND 155)")
print("=" * 70)

# Check df
res = subprocess.run(["df", "-h", "/mnt/hdd-backup"], capture_output=True, text=True)
print("Disk Usage:")
print(res.stdout.strip())

# -------------------------------------------------------------
# 1. LOSSLESS AUDIT
# -------------------------------------------------------------
print("\n--- 1. LOSSLESS LIBRARY AUDIT ---")
lossless_stats = {
    'total_dirs': 0,
    'total_files': 0,
    'flac_files': 0,
    'non_flac_audio': 0,
    'cue_sheets': 0,
    'clutter_files': 0,
    'm3u_clutter': 0,
    'duplicate_covers': 0,
    'case_collisions': 0,
    'missing_tilde': 0,
    'loose_audio': 0,
    'empty_dirs': 0,
    'format_noise': 0,
    'date_prefixes': 0,
}

clutter_exts = {'.cue', '.log', '.accurip', '.html', '.htm', '.url', '.ini'}
audio_non_flac_exts = {'.wav', '.aiff', '.aif', '.wv', '.mp3', '.m4a', '.aac', '.ogg', '.dsf', '.dff', '.wma', '.ape'}
noise_pat = re.compile(r'\[(FLAC|WEB-FLAC|CD-FLAC|Hi-Res|24bit|24bit[^\s]*|96kHz[^\s]*|48kHz[^\s]*|FLAC[^\s]*)\]|\((Hi-Res|FLAC|24bit|96kHz)\)|【FLAC】', re.IGNORECASE)
date_pat = re.compile(r'^\d{4}[\.-]\d{2}[\.-]\d{2}\s+')

# Missing tildes
cats = [d for d in os.listdir(ROOT_LOSSLESS) if os.path.isdir(os.path.join(ROOT_LOSSLESS, d))]
for c in cats:
    cp = os.path.join(ROOT_LOSSLESS, c)
    for a in os.listdir(cp):
        ap = os.path.join(cp, a)
        if os.path.isdir(ap) and not a.endswith("~"):
            lossless_stats['missing_tilde'] += 1

# Traversal
master_m3u8 = os.path.join(ROOT_LOSSLESS, "Lossless.m3u8")
for root, dirs, files in os.walk(ROOT_LOSSLESS):
    lossless_stats['total_dirs'] += len(dirs)
    lossless_stats['total_files'] += len(files)

    if not dirs and not files:
        lossless_stats['empty_dirs'] += 1

    # Case collisions
    seen_d = {}
    for d in dirs:
        dl = d.lower()
        if dl in seen_d:
            lossless_stats['case_collisions'] += 1
        seen_d[dl] = d
        if noise_pat.search(d):
            lossless_stats['format_noise'] += 1
        if date_pat.search(d):
            lossless_stats['date_prefixes'] += 1

    seen_f = {}
    for f in files:
        fl = f.lower()
        if fl in seen_f:
            lossless_stats['case_collisions'] += 1
        seen_f[fl] = f

    # Covers check
    imgs = [f.lower() for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    has_jpg = any('cover.jpg' in i or 'cover.jpeg' in i for i in imgs)
    has_png = any('cover.png' in i for i in imgs)
    if has_jpg and has_png:
        lossless_stats['duplicate_covers'] += 1

    # Audio & clutter
    rel = os.path.relpath(root, ROOT_LOSSLESS)
    parts = rel.split(os.sep) if rel != '.' else []
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        fp = os.path.join(root, f)
        if ext == '.flac':
            lossless_stats['flac_files'] += 1
            if len(parts) <= 2:
                lossless_stats['loose_audio'] += 1
        elif ext in audio_non_flac_exts:
            lossless_stats['non_flac_audio'] += 1
        elif ext == '.cue':
            lossless_stats['cue_sheets'] += 1
        elif ext in clutter_exts:
            lossless_stats['clutter_files'] += 1
        elif ext in ['.m3u', '.m3u8'] and fp != master_m3u8:
            lossless_stats['m3u_clutter'] += 1

print(f"Total directories      : {lossless_stats['total_dirs']}")
print(f"Total files            : {lossless_stats['total_files']}")
print(f"Bit-perfect FLAC tracks: {lossless_stats['flac_files']}")
print(f"Non-FLAC audio files   : {lossless_stats['non_flac_audio']}")
print(f"CUE sheets             : {lossless_stats['cue_sheets']}")
print(f"Clutter files          : {lossless_stats['clutter_files']}")
print(f"In-album M3U playlists : {lossless_stats['m3u_clutter']}")
print(f"Duplicate cover art    : {lossless_stats['duplicate_covers']}")
print(f"Case collisions        : {lossless_stats['case_collisions']}")
print(f"Artists missing ~      : {lossless_stats['missing_tilde']}")
print(f"Loose audio tracks     : {lossless_stats['loose_audio']}")
print(f"Empty directories      : {lossless_stats['empty_dirs']}")
print(f"Album format noise tags: {lossless_stats['format_noise']}")
print(f"Album raw date prefixes: {lossless_stats['date_prefixes']}")

# -------------------------------------------------------------
# 2. LOSSY AUDIT
# -------------------------------------------------------------
print("\n--- 2. LOSSY LIBRARY AUDIT ---")
lossy_stats = {
    'flac_files': 0,
    'lossy_audio': 0,
    'clutter_files': 0,
    'empty_dirs': 0,
    'case_collisions': 0
}
master_lossy_m3u8 = os.path.join(ROOT_LOSSY, "Lossy.m3u8")
for root, dirs, files in os.walk(ROOT_LOSSY):
    if not dirs and not files:
        lossy_stats['empty_dirs'] += 1
    seen = {}
    for d in dirs:
        dl = d.lower()
        if dl in seen:
            lossy_stats['case_collisions'] += 1
        seen[dl] = d
    seen_f = {}
    for f in files:
        fl = f.lower()
        if fl in seen_f:
            lossy_stats['case_collisions'] += 1
        seen_f[fl] = f
        ext = os.path.splitext(f)[1].lower()
        fp = os.path.join(root, f)
        if ext == '.flac':
            lossy_stats['flac_files'] += 1
        elif ext in ['.mp3', '.m4a', '.aac', '.ogg', '.opus']:
            lossy_stats['lossy_audio'] += 1
        elif ext in clutter_exts or (ext in ['.m3u', '.m3u8'] and fp != master_lossy_m3u8):
            lossy_stats['clutter_files'] += 1

print(f"Lossy audio tracks     : {lossy_stats['lossy_audio']}")
print(f"FLAC files in Lossy    : {lossy_stats['flac_files']}")
print(f"Clutter files in Lossy : {lossy_stats['clutter_files']}")
print(f"Empty dirs in Lossy    : {lossy_stats['empty_dirs']}")
print(f"Case collisions in Lossy: {lossy_stats['case_collisions']}")

# -------------------------------------------------------------
# 3. MASTER CATALOG CHECK
# -------------------------------------------------------------
print("\n--- 3. MASTER CATALOG & PLAYLISTS ---")
cat_sqlite = "/mnt/hdd-backup/music/catalog.sqlite"
if os.path.exists(cat_sqlite):
    import sqlite3
    conn = sqlite3.connect(cat_sqlite)
    c = conn.cursor()
    c.execute("SELECT count(*) FROM tracks")
    tot = c.fetchone()[0]
    c.execute("SELECT count(*) FROM tracks WHERE is_lossless=1")
    ll = c.fetchone()[0]
    c.execute("SELECT count(*) FROM tracks WHERE is_lossless=0")
    ls = c.fetchone()[0]
    print(f"catalog.sqlite tracks: {tot} (Lossless: {ll}, Lossy: {ls})")
    conn.close()

if os.path.exists(master_m3u8):
    with open(master_m3u8, 'r', encoding='utf-8', errors='ignore') as mf:
        lines = [l for l in mf if not l.startswith('#') and l.strip()]
        print(f"Lossless.m3u8 tracks : {len(lines)}")

if os.path.exists(master_lossy_m3u8):
    with open(master_lossy_m3u8, 'r', encoding='utf-8', errors='ignore') as mf:
        lines = [l for l in mf if not l.startswith('#') and l.strip()]
        print(f"Lossy.m3u8 tracks    : {len(lines)}")

print("\nMASTER AUDIT FINISHED!")
