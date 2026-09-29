import os
import re

ROOT = "/mnt/hdd-backup/music/Lossless"

FORBIDDEN_CHARS = set(':*?"<>|')
AUDIO_EXTS = {'.flac', '.wav', '.ape', '.wv', '.m4a', '.mp3', '.ogg', '.dsf', '.dff'}

print(f"=== Ultra-Deep Comprehensive Audit on {ROOT} ===")

categories = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d))]
print(f"Categories found: {categories}")

stats = {
    'total_dirs': 0,
    'total_files': 0,
    'audio_files': 0,
    'cue_files': 0,
    'zip_files': 0,
    'zero_byte_files': 0,
    'forbidden_chars': 0,
    'loose_audio': 0,
    'unsplit_cues': 0,
    'duplicate_albums': 0
}

loose_audio_list = []
forbidden_list = []
cue_list = []
zip_list = []
zero_byte_list = []
duplicate_album_list = []

for root, dirs, files in os.walk(ROOT):
    stats['total_dirs'] += len(dirs)
    stats['total_files'] += len(files)
    
    rel = os.path.relpath(root, ROOT)
    parts = rel.split(os.sep) if rel != '.' else []
    
    # 1. Check forbidden characters in path
    for d in dirs:
        if any(c in d for c in FORBIDDEN_CHARS):
            stats['forbidden_chars'] += 1
            forbidden_list.append(os.path.join(root, d))
    for f in files:
        if any(c in f for c in FORBIDDEN_CHARS):
            stats['forbidden_chars'] += 1
            forbidden_list.append(os.path.join(root, f))
            
    # 2. Check loose audio
    # A loose audio file is an audio file at category root (depth 1) or artist root (depth 2)
    # Depth 1: Category root (e.g. Lossless/Anime/song.flac)
    # Depth 2: Artist root (e.g. Lossless/J-Pop/Artist/song.flac)
    # In Game/Anime umbrellas, depth might be Category/Franchise/song.flac (depth 2) or Category/Franchise/Sub/song.flac
    # Let's check: if len(parts) <= 2, any audio file is definitely loose.
    # Exception: if parts has category/artist and files are loose.
    if len(parts) == 1: # in category root
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in AUDIO_EXTS:
                stats['loose_audio'] += 1
                loose_audio_list.append(os.path.join(root, f))
    elif len(parts) == 2: # in artist root or franchise root
        # Check if dirs exists here (meaning it has album subdirectories)
        # Even if dirs is empty, an artist root with loose tracks violates the album container rule!
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in AUDIO_EXTS:
                stats['loose_audio'] += 1
                loose_audio_list.append(os.path.join(root, f))
                
    # 3. Check files
    for f in files:
        fp = os.path.join(root, f)
        ext = os.path.splitext(f)[1].lower()
        if ext in AUDIO_EXTS:
            stats['audio_files'] += 1
        elif ext == '.cue':
            stats['cue_files'] += 1
            cue_list.append(fp)
        elif ext == '.zip':
            stats['zip_files'] += 1
            zip_list.append(fp)
            
        try:
            if os.path.getsize(fp) == 0:
                stats['zero_byte_files'] += 1
                zero_byte_list.append(fp)
        except Exception:
            pass

    # 4. Check duplicate albums in current directory
    # If this directory contains album subdirectories (e.g. artist directory)
    if dirs:
        norm_map = {}
        for d in dirs:
            # normalize name: lowercase, strip tags [FLAC], (Digital), etc.
            n = d.lower()
            n = re.sub(r'\[.*?\]|\(.*?\)', '', n).strip()
            # remove punctuation
            n = re.sub(r'[^\w\s]', '', n)
            n = re.sub(r'\s+', ' ', n).strip()
            if n:
                if n in norm_map:
                    # check if both have audio files
                    p1 = os.path.join(root, norm_map[n])
                    p2 = os.path.join(root, d)
                    stats['duplicate_albums'] += 1
                    duplicate_album_list.append((p1, p2))
                else:
                    norm_map[n] = d

# Check CUE files for unsplit whole-disc audio
for cp in cue_list:
    cdir = os.path.dirname(cp)
    flacs = [f for f in os.listdir(cdir) if f.lower().endswith('.flac')]
    # If there is only 1 FLAC and 1 CUE, it might be an unsplit disc image
    if len(flacs) == 1:
        # Check size of the flac
        flac_path = os.path.join(cdir, flacs[0])
        try:
            sz = os.path.getsize(flac_path)
            # if > 60MB, highly likely a whole album disc image
            if sz > 60 * 1024 * 1024:
                stats['unsplit_cues'] += 1
                print(f"[!] Potential Unsplit Disc Image: {flac_path} ({sz / (1024*1024):.1f} MB)")
        except Exception:
            pass

print("\n=== AUDIT SUMMARY RESULTS ===")
print(f"Total directories : {stats['total_dirs']}")
print(f"Total files       : {stats['total_files']}")
print(f"Audio files       : {stats['audio_files']}")
print(f"CUE sheets found  : {stats['cue_files']}")
print(f"Unsplit CUE discs : {stats['unsplit_cues']}")
print(f"Zip files         : {stats['zip_files']}")
print(f"Zero-byte files   : {stats['zero_byte_files']}")
print(f"Forbidden chars   : {stats['forbidden_chars']}")
print(f"Loose audio files : {stats['loose_audio']}")
print(f"Duplicate albums  : {stats['duplicate_albums']}")

if loose_audio_list:
    print(f"\nLoose audio ({len(loose_audio_list)}):")
    for l in loose_audio_list[:10]:
        print(f"  {l}")

if forbidden_list:
    print(f"\nForbidden chars ({len(forbidden_list)}):")
    for f in forbidden_list[:10]:
        print(f"  {f}")

if zip_list:
    print(f"\nZip files ({len(zip_list)}):")
    for z in zip_list:
        print(f"  {z}")

if zero_byte_list:
    print(f"\nZero-byte files ({len(zero_byte_list)}):")
    for z in zero_byte_list:
        print(f"  {z}")

if duplicate_album_list:
    print(f"\nPotential duplicate albums ({len(duplicate_album_list)}):")
    for p1, p2 in duplicate_album_list[:10]:
        print(f"  A: {p1}\n  B: {p2}\n")

print("\nAudit complete.")
