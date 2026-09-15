#!/usr/bin/env python3
import os
import json
import time

SRC_DIR = "/mnt/hdd-media/manga-raw"
DST_DIR = "/mnt/hdd-media/manga-reader"
STATE_FILE = "/tmp/manga_optimizer_state.json"

def get_tree_stats(base_dir):
    stats = {}
    if not os.path.exists(base_dir): return stats
    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == '.': continue
        
        top_folder = rel_path.split(os.sep)[0]
        archives = [f for f in files if f.lower().endswith(('.cbz', '.zip', '.cbr', '.rar', '.7z')) and not f.startswith('.')]
        
        if archives:
            if top_folder not in stats:
                stats[top_folder] = {"count": 0, "size": 0}
            stats[top_folder]["count"] += len(archives)
            for f in archives:
                try:
                    stats[top_folder]["size"] += os.path.getsize(os.path.join(root, f))
                except: pass
    return stats

def main():
    print("\033[2J\033[H", end="")
    print("=" * 50)
    print(" MANGA OPTIMIZER STATUS MONITOR")
    print("=" * 50)
    
    state = {"currently_converting": {}, "total_savings_mb": 0.0, "total_files_processed": 0}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
        except: pass

    raw_stats = get_tree_stats(SRC_DIR)
    reader_stats = get_tree_stats(DST_DIR)
    
    print("\n[ FOLDER TREE (MANGA-READER) ]")
    if not reader_stats:
        print("  (Empty or scanning...)")
    else:
        for folder, data in sorted(reader_stats.items()):
            size_gb = data['size'] / (1024**3)
            raw_size = raw_stats.get(folder, {}).get("size", 0)
            savings_pct = (1 - (data['size']/raw_size)) * 100 if raw_size > 0 else 0
            
            print(f" 📁 {folder}/")
            print(f"    ├─ Files: {data['count']} archives")
            print(f"    └─ Size : {size_gb:.2f} GB (Saved ~{savings_pct:.1f}%)")

    print(f"\n[ TOTAL LIFETIME SAVINGS ]")
    print(f"  Processed : {state['total_files_processed']} files")
    print(f"  Storage   : {state['total_savings_mb'] / 1024:.2f} GB saved")

    print("\n[ LIVE PROGRESS ]")
    active = state.get("currently_converting", {})
    if not active:
        print("  💤 Idle (No files are currently being converted)")
    else:
        for filepath, info in active.items():
            filename = os.path.basename(filepath)
            status = info.get("status", "Starting...")
            pct = info.get("pct", 0)
            
            bar_len = 20
            filled = int(bar_len * pct // 100)
            bar = '█' * filled + '-' * (bar_len - filled)
            
            print(f" ⏳ {filename}")
            print(f"    [{bar}] {pct}% - {status}")
            
    print('\n' + '='*50)

if __name__ == '__main__':
    main()
