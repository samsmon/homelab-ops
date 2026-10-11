import os
import subprocess

gakumas_root = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~"

print("=== DEEP GAKUMAS AUDIT ===")

all_dirs = []
all_files = []
alt_files = []
anomalies = []

for r, d, f in os.walk(gakumas_root):
    rel = os.path.relpath(r, gakumas_root)
    # Check if folder has loose files or no audio
    audio = [x for x in f if x.endswith(('.flac', '.wav', '.wv', '.m4a', '.aif', '.aiff', '.mp3'))]
    non_audio = [x for x in f if x not in audio]
    
    # check alt files
    for x in f:
        if "_alt" in x:
            alt_files.append((os.path.join(r, x), x))
            
    # check for weird filenames
    for x in f:
        if x.startswith('.') or x.endswith(('.tmp', '.part', '.bak')):
            anomalies.append(f"Suspicious file: {os.path.join(rel, x)}")

    # Check depth & structure
    parts = rel.split(os.sep) if rel != '.' else []
    # If this is an album (leaf folder), check audio count
    if not d:
        if len(audio) == 0:
            anomalies.append(f"Leaf dir with NO AUDIO: {rel} ({f})")
    else:
        if len(audio) > 0:
            anomalies.append(f"Dir with both subdirs AND audio: {rel} ({len(audio)} audio, subdirs: {d})")

print(f"Total subdirectories in Gakumas: {len(all_dirs)}")
print(f"Alt files found ({len(alt_files)}):")
for path, name in alt_files:
    print(f"  {path}")
    # inspect audio properties of alt vs regular
    reg_name = name.replace("_alt.flac", ".flac")
    reg_path = os.path.join(os.path.dirname(path), reg_name)
    if os.path.exists(reg_path):
        sz1 = os.path.getsize(path)
        sz2 = os.path.getsize(reg_path)
        print(f"    Alt size: {sz1}, Reg size: {sz2}")
        try:
            p1 = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', path], universal_newlines=True).strip().split()
            p2 = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', reg_path], universal_newlines=True).strip().split()
            print(f"    Alt prop: {p1}, Reg prop: {p2}")
        except Exception as e:
            print(f"    Error checking metaflac: {e}")

print(f"\nAnomalies found ({len(anomalies)}):")
for a in anomalies:
    print(f"  {a}")

print("\n--- Listing complete tree of Gakumas ---")
for r, d, f in os.walk(gakumas_root):
    rel = os.path.relpath(r, gakumas_root)
    audio = [x for x in f if x.endswith(('.flac', '.wav', '.wv', '.m4a', '.aif', '.aiff', '.mp3'))]
    subdirs = [x for x in d]
    print(f"[{rel}] dirs={len(subdirs)}, audio={len(audio)}, other={[x for x in f if x not in audio]}")
