#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/tmp/e_download_library.db')
c = conn.cursor()
tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('Tables in E:\\Download\\library.db:', tables)
for t in tables:
    c.execute(f"PRAGMA table_info({t})")
    cols = [col[1] for col in c.fetchall()]
    c.execute(f"SELECT count(*) FROM {t}")
    cnt = c.fetchone()[0]
    print(f"\nTable '{t}' ({cnt} rows): columns={cols}")
    c.execute(f"SELECT * FROM {t} LIMIT 3")
    for r in c.fetchall():
        print("  Sample row:", r)
