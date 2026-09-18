#!/usr/bin/env python3
"""
Manga Auto-Optimizer Pipeline Daemon
Monitors /mnt/hdd-media/manga-raw for CBZ/ZIP files.
Optimizes heavy comic archives to lightweight WebP (max 2048px width, Q85)
and mirrors the folder hierarchy into /mnt/hdd-media/manga-reader for Kavita / readers.
Preserves hardlinks for already-light WebP archives (0 extra disk space).
Handles real-time additions, moves, renames, and deletions.
"""

import os
import sys
import time
import shutil
import zipfile
import io
import logging
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

SRC_DIR = "/mnt/hdd-media/manga-raw"
DST_DIR = "/mnt/hdd-media/manga-reader"
LOG_FILE = "/var/log/manga-optimizer.log"
MAX_WORKERS = 2
MAX_IMAGE_WIDTH = 2048
WEBP_QUALITY = 85

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

import json
STATE_FILE = "/tmp/manga_optimizer_state.json"
state_lock = threading.Lock()
state_data = {
    "currently_converting": {},
    "total_savings_mb": 0.0,
    "total_files_processed": 0
}

def update_state(src_path=None, status_dict=None, remove=False):
    with state_lock:
        if src_path:
            if remove:
                state_data["currently_converting"].pop(src_path, None)
            else:
                if src_path not in state_data["currently_converting"]:
                    state_data["currently_converting"][src_path] = {}
                if status_dict:
                    state_data["currently_converting"][src_path].update(status_dict)
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(state_data, f)
        except Exception:
            pass

def is_archive_already_optimized(src_path):
    """Check if an archive is small enough and already uses WebP."""
    try:
        size = os.path.getsize(src_path)
        if size > 45 * 1024 * 1024:  # > 45MB needs inspection/conversion
            return False
        with zipfile.ZipFile(src_path, 'r') as z:
            for item in z.infolist():
                ext = os.path.splitext(item.filename)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png']:
                    return False
        return True
    except Exception:
        return False

def optimize_archive(src_path, dst_path):
    """Convert images in archive to WebP and output to dst_path."""
    tmp_path = dst_path + ".tmp"
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    
    # If already small and all WebP, use hardlink or copy
    if is_archive_already_optimized(src_path):
        try:
            if os.path.exists(dst_path):
                os.remove(dst_path)
            os.link(src_path, dst_path)
            logging.info(f"Hardlinked (already light): {os.path.basename(src_path)}")
            return True
        except OSError:
            shutil.copy2(src_path, dst_path)
            logging.info(f"Copied (already light): {os.path.basename(src_path)}")
            return True

    orig_size = os.path.getsize(src_path)
    t0 = time.time()
    
    # Create temporary extraction folder in DST_DIR
    ext_base_dir = os.path.join(DST_DIR, ".extraction")
    ext_dir = os.path.join(ext_base_dir, f"{os.path.basename(src_path)}_{int(time.time())}")
    os.makedirs(ext_dir, exist_ok=True)
    
    try:
        update_state(src_path, {"status": "Extracting archive...", "pct": 0})
        # 1. Force extract everything using 7z (handles zip, rar, 7z, etc. regardless of extension)
        result = subprocess.run(['7z', 'x', '-y', f'-o{ext_dir}', src_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"7z extraction failed: {result.stderr.decode('utf-8', errors='ignore')}")

        # Gather all files to track progress
        all_files = []
        for root, dirs, files in os.walk(ext_dir):
            for file in files:
                all_files.append(os.path.join(root, file))
        total_files = len(all_files)

        update_state(src_path, {"status": f"Converting 0/{total_files}", "pct": 0})

        # 2. Convert to WebP and save to new Zip
        with zipfile.ZipFile(tmp_path, 'w', compression=zipfile.ZIP_STORED) as z_out:
            for idx, file_path in enumerate(all_files):
                if total_files > 0:
                    pct = int((idx / total_files) * 100)
                    if idx % max(1, total_files // 20) == 0:  # Update progress every 5% roughly
                        update_state(src_path, {"status": f"Converting {idx}/{total_files}", "pct": pct})
                        
                arcname = os.path.relpath(file_path, ext_dir)
                ext = os.path.splitext(os.path.basename(file_path))[1].lower()
                
                if ext in ['.jpg', '.jpeg', '.png']:
                    try:
                        img = Image.open(file_path)
                        if img.mode not in ('RGB', 'L'):
                            img = img.convert('RGB')
                        w, h = img.size
                        if w > MAX_IMAGE_WIDTH:
                            new_h = int(h * (MAX_IMAGE_WIDTH / w))
                            img = img.resize((MAX_IMAGE_WIDTH, new_h), Image.Resampling.LANCZOS)
                        
                        buf = io.BytesIO()
                        img.save(buf, format='WEBP', quality=WEBP_QUALITY, method=4)
                        new_data = buf.getvalue()
                        
                        new_arcname = os.path.splitext(arcname)[0] + '.webp'
                        z_out.writestr(new_arcname, new_data)
                    except Exception as e:
                        # Fallback to original file bytes if conversion fails
                        z_out.write(file_path, arcname)
                else:
                    # Write non-image files as is
                    z_out.write(file_path, arcname)
                        
        # Adu ukuran: kalo di manga-reader udah ada & ukurannya lebih kecil, keep yg lama
        tmp_size = os.path.getsize(tmp_path)
        if os.path.exists(dst_path) and os.path.getsize(dst_path) <= tmp_size:
            dst_size = os.path.getsize(dst_path)
            logging.info(f"Existing file is smaller/equal ({dst_size/1024/1024:.1f}MB vs {tmp_size/1024/1024:.1f}MB). Keeping existing.")
            os.remove(tmp_path)
        else:
            os.replace(tmp_path, dst_path)
            
        # Match mtime (Penting banget biar gak terjadi proses berulang-ulang tanpa henti)
        stat = os.stat(src_path)
        os.utime(dst_path, (stat.st_atime, stat.st_mtime))
        
        new_size = os.path.getsize(dst_path)
        reduction = (1 - (new_size / orig_size)) * 100 if orig_size > 0 else 0
        elapsed = time.time() - t0
        
        with state_lock:
            state_data["total_savings_mb"] += max(0, (orig_size - new_size) / (1024 * 1024))
            state_data["total_files_processed"] += 1
            
        logging.info(f"Optimized: {os.path.basename(src_path)} ({orig_size/1024/1024:.1f}MB -> {new_size/1024/1024:.1f}MB, -{reduction:.1f}%) in {elapsed:.1f}s")
        return True
        
    except Exception as e:
        logging.error(f"Error optimizing {src_path}: {e}")
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        
        # Fallback if even 7z fails (e.g. completely corrupted file)
        try:
            if os.path.exists(dst_path):
                os.remove(dst_path)
            os.link(src_path, dst_path)
            logging.warning(f"Fallback hardlink (optimize failed): {os.path.basename(src_path)}")
        except OSError:
            try:
                shutil.copy2(src_path, dst_path)
                logging.warning(f"Fallback copy (optimize failed): {os.path.basename(src_path)}")
            except OSError as copy_err:
                logging.error(f"Fallback copy also failed for {src_path}: {copy_err}")
                return False
        return True
        
    finally:
        update_state(src_path, remove=True)
        # 3. Clean up temporary extraction folder
        if os.path.exists(ext_dir):
            try:
                shutil.rmtree(ext_dir)
            except OSError as e:
                logging.error(f"Failed to cleanup extraction directory {ext_dir}: {e}")

def get_dst_path(src_path):
    rel = os.path.relpath(src_path, SRC_DIR)
    return os.path.join(DST_DIR, rel)

active_files = set()
processing_lock = threading.Lock()

def process_file_if_needed(src_path):
    """Process a single file if it's missing or newer than the destination."""
    if not src_path.lower().endswith(('.cbz', '.zip')):
        return
    
    # Prevent concurrent processing of the exact same file
    with processing_lock:
        if src_path in active_files:
            return
        active_files.add(src_path)
        
    try:
        # Only check file settling if it was modified very recently (< 15 seconds ago)
        try:
            mtime = os.path.getmtime(src_path)
            if time.time() - mtime < 15:
                s1 = os.path.getsize(src_path)
                time.sleep(1)
                s2 = os.path.getsize(src_path)
                if s1 != s2:
                    time.sleep(3) # Wait for file write to settle
        except OSError:
            return
    
        dst_path = get_dst_path(src_path)
        if os.path.exists(dst_path):
            try:
                if os.path.getmtime(dst_path) >= os.path.getmtime(src_path) and os.path.getsize(dst_path) > 0:
                    return  # Up to date
            except OSError:
                pass
                
        optimize_archive(src_path, dst_path)
    finally:
        with processing_lock:
            if src_path in active_files:
                active_files.remove(src_path)

def initial_sync(pool):
    logging.info("Starting initial synchronization scan...")
    futures = []
    for root, dirs, files in os.walk(SRC_DIR):
        for f in files:
            if f.lower().endswith(('.cbz', '.zip')) and not f.startswith('.'):
                src_path = os.path.join(root, f)
                futures.append(pool.submit(process_file_if_needed, src_path))
    logging.info(f"Queued {len(futures)} archives for verification/optimization.")

def prune_orphaned():
    """Remove files in DST_DIR that no longer exist in SRC_DIR."""
    for root, dirs, files in os.walk(DST_DIR, topdown=False):
        for f in files:
            dst_file = os.path.join(root, f)
            rel = os.path.relpath(dst_file, DST_DIR)
            src_file = os.path.join(SRC_DIR, rel)
            if not os.path.exists(src_file):
                try:
                    os.remove(dst_file)
                    logging.info(f"Removed orphaned file: {rel}")
                except OSError:
                    pass
        for d in dirs:
            dst_d = os.path.join(root, d)
            rel = os.path.relpath(dst_d, DST_DIR)
            src_d = os.path.join(SRC_DIR, rel)
            if not os.path.exists(src_d):
                try:
                    os.rmdir(dst_d)
                    logging.info(f"Removed orphaned directory: {rel}")
                except OSError:
                    pass

class MangaEventHandler(FileSystemEventHandler):
    def __init__(self, pool):
        self.pool = pool
        super().__init__()

    def on_created(self, event):
        if event.is_directory:
            dst = get_dst_path(event.src_path)
            os.makedirs(dst, exist_ok=True)
        elif event.src_path.lower().endswith(('.cbz', '.zip')) and not os.path.basename(event.src_path).startswith('.'):
            logging.info(f"Detected new archive: {event.src_path}")
            # Delay slightly to allow write completion
            threading.Timer(3.0, self.pool.submit, args=[process_file_if_needed, event.src_path]).start()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.cbz', '.zip')) and not os.path.basename(event.src_path).startswith('.'):
            threading.Timer(3.0, self.pool.submit, args=[process_file_if_needed, event.src_path]).start()

    def on_moved(self, event):
        src_dst = get_dst_path(event.src_path)
        dest_dst = get_dst_path(event.dest_path)
        if os.path.exists(src_dst):
            os.makedirs(os.path.dirname(dest_dst), exist_ok=True)
            try:
                os.replace(src_dst, dest_dst)
                logging.info(f"Mirrored move: {src_dst} -> {dest_dst}")
            except OSError as e:
                logging.error(f"Failed to mirror move {src_dst} -> {dest_dst}: {e}")
        else:
            if not event.is_directory:
                self.pool.submit(process_file_if_needed, event.dest_path)

    def on_deleted(self, event):
        dst = get_dst_path(event.src_path)
        if event.is_directory:
            if os.path.exists(dst):
                try:
                    shutil.rmtree(dst)
                    logging.info(f"Mirrored dir deletion: {dst}")
                except OSError as e:
                    logging.error(f"Failed to delete {dst}: {e}")
        else:
            if os.path.exists(dst):
                try:
                    os.remove(dst)
                    logging.info(f"Mirrored file deletion: {dst}")
                except OSError as e:
                    logging.error(f"Failed to delete {dst}: {e}")

def main():
    # Lower process priority to prevent high CPU impact on interactive services
    try:
        os.nice(10)
    except Exception:
        pass

    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(DST_DIR, exist_ok=True)

    logging.info("==========================================")
    logging.info("Manga Auto-Optimizer Pipeline Daemon Started")
    logging.info(f"Source (Master):   {SRC_DIR}")
    logging.info(f"Target (Reader):   {DST_DIR}")
    logging.info("==========================================")

    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS, thread_name_prefix="OptimizerWorker")
    
    # Run initial sync and orphan cleanup in background
    prune_orphaned()
    initial_sync(pool)

    # Start Watchdog
    event_handler = MangaEventHandler(pool)
    observer = Observer()
    observer.schedule(event_handler, SRC_DIR, recursive=True)
    observer.start()
    logging.info(f"Watching for events on {SRC_DIR}...")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    pool.shutdown(wait=True)

if __name__ == "__main__":
    main()
