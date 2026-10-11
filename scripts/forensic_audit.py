import os
import re

ROOT = "/mnt/hdd-backup/music/Lossless"

print("==================================================================")
print("=== FORENSIC EXHAUSTIVE AUDIT ACROSS LOSSLESS ===")
print("==================================================================")

extraneous_exts = {'.log', '.txt', '.url', '.nfo', '.accurip', '.sfv', '.md5', '.torrent', '.db', '.ini'}
non_flac_audio_exts = {'.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wma', '.wav', '.ape', '.wv', '.aif', '.aiff', '.dsf', '.dff'}

findings = {
    'double_spaces': [],
    'extraneous_files': [],
    'non_flac_audio': [],
    'no_track_number': [],
    'single_digit_number': [],
    'trailing_or_leading_space': []
}

for root, dirs, files in os.walk(ROOT):
    rel = os.path.relpath(root, ROOT)
    parts = rel.split(os.sep) if rel != '.' else []
    
    # Check directory names
    for d in dirs:
        if "  " in d:
            findings['double_spaces'].append(os.path.join(rel, d))
        if d.strip() != d or d.rstrip(' ~').rstrip() != d.rstrip(' ~'):
            findings['trailing_or_leading_space'].append(os.path.join(rel, d))
            
    # Check files
    for f in files:
        fp = os.path.join(root, f)
        rel_fp = os.path.join(rel, f)
        base, ext = os.path.splitext(f)
        ext_low = ext.lower()
        
        if "  " in f:
            findings['double_spaces'].append(rel_fp)
        if f.strip() != f:
            findings['trailing_or_leading_space'].append(rel_fp)
            
        if ext_low in extraneous_exts:
            findings['extraneous_files'].append(rel_fp)
            
        if ext_low in non_flac_audio_exts:
            findings['non_flac_audio'].append(rel_fp)
            
        if ext_low == '.flac':
            # Check track numbering pattern
            # Expected: "01. Title.flac" or "01 - Title.flac" or "01 Title.flac"
            if not re.match(r'^\d{2,}', f):
                # Is it a single digit?
                if re.match(r'^\d\b', f):
                    findings['single_digit_number'].append(rel_fp)
                else:
                    findings['no_track_number'].append(rel_fp)

print("\n--- AUDIT RESULTS ---")
print(f"1. Double spaces in names         : {len(findings['double_spaces'])}")
print(f"2. Leading/trailing whitespace    : {len(findings['trailing_or_leading_space'])}")
print(f"3. Extraneous clutter files       : {len(findings['extraneous_files'])}")
print(f"4. Non-FLAC audio files           : {len(findings['non_flac_audio'])}")
print(f"5. Single-digit track numbers     : {len(findings['single_digit_number'])}")
print(f"6. Tracks with no leading number  : {len(findings['no_track_number'])}")

if findings['double_spaces']:
    print("\nSample double spaces (first 10):")
    for s in findings['double_spaces'][:10]:
        print(f"  {s}")

if findings['extraneous_files']:
    print("\nSample extraneous clutter files (first 15):")
    for s in findings['extraneous_files'][:15]:
        print(f"  {s}")

if findings['non_flac_audio']:
    print("\nSample non-FLAC audio files:")
    for s in findings['non_flac_audio'][:15]:
        print(f"  {s}")

if findings['single_digit_number']:
    print("\nSample single-digit track numbers:")
    for s in findings['single_digit_number'][:15]:
        print(f"  {s}")

if findings['no_track_number']:
    print("\nSample tracks with no leading number:")
    for s in findings['no_track_number'][:15]:
        print(f"  {s}")
