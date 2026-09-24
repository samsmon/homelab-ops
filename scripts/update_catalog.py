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

conn.close()
print(f"Catalog indexed successfully: {count} total tracks.")
