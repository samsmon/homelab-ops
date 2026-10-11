import os
import subprocess

mamyukka_dir = "/mnt/hdd-backup/music/Lossless/Doujinshi/Mamyukka ~"

def test_cue(album_dir, cue_name, flac_name, encoding='utf-8'):
    cue_path = os.path.join(album_dir, cue_name)
    flac_path = os.path.join(album_dir, flac_name)
    print(f"\n======================================")
    print(f"Testing {album_dir}")
    print(f"======================================")
    with open(cue_path, 'rb') as f:
        raw = f.read()
    
    content = raw.decode(encoding, errors='replace')
    print("--- CUE CONTENT ---")
    print(content)
    
    # Check if shnsplit can parse it
    # We will write a utf-8 temp cue with proper FILE target
    fixed_cue = []
    for line in content.splitlines():
        if line.strip().upper().startswith("FILE "):
            fixed_cue.append(f'FILE "{flac_name}" WAVE')
        else:
            fixed_cue.append(line)
            
    temp_cue = os.path.join(album_dir, "temp_split.cue")
    with open(temp_cue, 'w', encoding='utf-8') as f:
        f.write("\n".join(fixed_cue))
        
    cmd = ['shnsplit', '-f', temp_cue, '-t', '%n. %t', '-P', 'none', '-d', '/tmp/test_split', flac_path]
    print(f"Running test shnsplit...")
    os.makedirs('/tmp/test_split', exist_ok=True)
    # clean /tmp/test_split
    for f in os.listdir('/tmp/test_split'):
        os.remove(os.path.join('/tmp/test_split', f))
        
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print("Returncode:", res.returncode)
    print("STDOUT:", res.stdout[:500])
    print("STDERR:", res.stderr[:500])
    print("Generated files in /tmp/test_split:")
    for f in sorted(os.listdir('/tmp/test_split')):
        sz = os.path.getsize(os.path.join('/tmp/test_split', f))
        print(f"  {f} ({sz} bytes)")
    if os.path.exists(temp_cue):
        os.remove(temp_cue)

test_cue(os.path.join(mamyukka_dir, "テアトルエトワール"), "テアトルエトワール.cue", "テアトルエトワール.flac", encoding='cp932')
test_cue(os.path.join(mamyukka_dir, "THE 13th PANCER"), "THE 13th PANCER.cue", "THE 13th PANCER.flac", encoding='utf-8')
