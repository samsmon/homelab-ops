import os

ROOT = "/mnt/hdd-backup/music/Lossy"

print(f"=== AUDIT OF LOSSY DIRECTORY: {ROOT} ===")
if not os.path.exists(ROOT):
    print("Lossy does not exist!")
    exit(0)

stats = {
    'total_dirs': 0,
    'total_files': 0,
    'audio_files': 0,
    'forbidden': 0,
    'loose': 0,
    'empty_dirs': 0
}

AUDIO_EXTS = {'.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wma', '.flac'}
FORBIDDEN = set(':*?"<>|')

forbidden_list = []
loose_list = []
empty_list = []

for r, d, f in os.walk(ROOT):
    stats['total_dirs'] += len(d)
    stats['total_files'] += len(f)
    rel = os.path.relpath(r, ROOT)
    parts = rel.split(os.sep) if rel != '.' else []
    
    # check forbidden chars
    for name in d + f:
        if any(c in name for c in FORBIDDEN):
            stats['forbidden'] += 1
            forbidden_list.append(os.path.join(r, name))
            
    # check loose audio (depth <= 2)
    if len(parts) <= 2:
        for file in f:
            ext = os.path.splitext(file)[1].lower()
            if ext in AUDIO_EXTS:
                stats['loose'] += 1
                loose_list.append(os.path.join(r, file))
                
    # check empty dirs
    if not d and not f:
        stats['empty_dirs'] += 1
        empty_list.append(r)
        
    for file in f:
        ext = os.path.splitext(file)[1].lower()
        if ext in AUDIO_EXTS:
            stats['audio_files'] += 1

print(f"Total dirs   : {stats['total_dirs']}")
print(f"Total files  : {stats['total_files']}")
print(f"Audio files  : {stats['audio_files']}")
print(f"Forbidden    : {stats['forbidden']}")
print(f"Loose audio  : {stats['loose']}")
print(f"Empty dirs   : {stats['empty_dirs']}")

if forbidden_list:
    print(f"\nForbidden ({len(forbidden_list)}):")
    for fb in forbidden_list[:10]:
        print(f"  {fb}")

if loose_list:
    print(f"\nLoose audio ({len(loose_list)}):")
    for l in loose_list[:10]:
        print(f"  {l}")

if empty_list:
    print(f"\nEmpty dirs ({len(empty_list)}):")
    for ed in empty_list[:10]:
        print(f"  {ed}")
