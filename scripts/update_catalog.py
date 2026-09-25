import sqlite3
from pathlib import Path

MUSIC_ROOT = Path('/mnt/hdd-backup/music')
LOSSLESS_ROOT = MUSIC_ROOT / 'Lossless'
LOSSY_ROOT = MUSIC_ROOT / 'Lossy'
db_path = MUSIC_ROOT / 'catalog.sqlite'

if db_path.exists():
    db_path.unlink()

conn = sqlite3.connect(str(db_path))
c = conn.cursor()
c.execute('''
    CREATE TABLE tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        relative_path TEXT UNIQUE,
        filename TEXT,
        category TEXT,
        format TEXT,
        size_bytes INTEGER,
        is_lossless INTEGER
    )
''')
c.execute('CREATE INDEX idx_category ON tracks(category)')
c.execute('CREATE INDEX idx_format ON tracks(format)')

print("Indexing all tracks under /mnt/hdd-backup/music ...")
batch = []
count = 0

for root_dir in [LOSSLESS_ROOT, LOSSY_ROOT]:
    if not root_dir.exists():
        continue
    is_lossless = 1 if root_dir == LOSSLESS_ROOT else 0
    for p in root_dir.rglob('*'):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext not in ['.flac', '.wav', '.mp3', '.m4a', '.aac', '.ogg', '.opus', '.ape', '.wv', '.tak', '.aiff', '.aif', '.alac']:
            continue
            
        rel = str(p.relative_to(MUSIC_ROOT)).replace('\\', '/')
        parts = rel.split('/')
        category = parts[1] if len(parts) > 1 else 'Unknown'
        fmt = ext.replace('.', '').upper()
        size = p.stat().st_size
        
        batch.append((rel, p.name, category, fmt, size, is_lossless))
        count += 1
        if len(batch) >= 1000:
            c.executemany('''
                INSERT OR IGNORE INTO tracks 
                (relative_path, filename, category, format, size_bytes, is_lossless)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', batch)
            conn.commit()
            batch = []

if batch:
    c.executemany('''
        INSERT OR IGNORE INTO tracks 
        (relative_path, filename, category, format, size_bytes, is_lossless)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', batch)
    conn.commit()

print(f"Catalog indexed successfully: {count} total tracks.")

# Generate Master M3U8 Playlists for Music Players (MusicBee, Foobar2000, etc.)
print("Generating Master M3U8 Playlists...")

def write_m3u8(playlist_path, target_root, is_lossless_val):
    c.execute('''
        SELECT relative_path FROM tracks 
        WHERE is_lossless = ? 
        ORDER BY relative_path ASC
    ''', (is_lossless_val,))
    rows = c.fetchall()
    if not rows:
        return 0
    
    # Path inside playlist should be relative to the playlist file location
    prefix = f"{target_root.name}/"
    lines = ["#EXTM3U\n"]
    for (rel_path,) in rows:
        if rel_path.startswith(prefix):
            rel_entry = rel_path[len(prefix):]
        else:
            rel_entry = rel_path
        lines.append(f"{rel_entry}\n")
        
    with open(playlist_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    # Permissions for SMB access
    try:
        import os
        os.chown(playlist_path, 100000, 100000)
        os.chmod(playlist_path, 0o664)
    except Exception:
        pass
        
    return len(rows)

lossless_m3u8 = LOSSLESS_ROOT / 'Lossless.m3u8'
lossy_m3u8 = LOSSY_ROOT / 'Lossy.m3u8'

lossless_cnt = write_m3u8(lossless_m3u8, LOSSLESS_ROOT, 1)
print(f"  -> Generated {lossless_m3u8} ({lossless_cnt} tracks)")

lossy_cnt = write_m3u8(lossy_m3u8, LOSSY_ROOT, 0)
print(f"  -> Generated {lossy_m3u8} ({lossy_cnt} tracks)")

conn.close()
print("All catalog & playlist operations completed successfully.")
