#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/tmp/e_download_library.db')
c = conn.cursor()
c.execute("SELECT match_status, count(*) FROM comparison_results GROUP BY match_status")
print("=== COMPARISON RESULTS SUMMARY IN library.db ===")
for r in c.fetchall():
    print(f"  {r[0]}: {r[1]} albums")

c.execute("SELECT category, count(*) FROM local_library GROUP BY category")
print("\n=== LOCAL LIBRARY BY CATEGORY (E:\\Download) ===")
for r in c.fetchall():
    print(f"  {r[0]}: {r[1]} albums")
