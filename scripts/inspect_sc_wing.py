import os

base = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~"

wing_dir = os.path.join(base, "01. WING & Main Game Series")
print("=== 01. WING & Main Game Series ===")
for sub in sorted(os.listdir(wing_dir)):
    p = os.path.join(wing_dir, sub)
    if os.path.isdir(p):
        print(f"\nSub: {sub}")
        for item in sorted(os.listdir(p)):
            ip = os.path.join(p, item)
            files = os.listdir(ip) if os.path.isdir(ip) else []
            audio = [x for x in files if x.endswith(('.flac', '.wav', '.wv', '.m4a', '.aif', '.aiff'))]
            print(f"  {item}: {len(audio)} audio, other: {[x for x in files if x not in audio]}")

feathers_dir = os.path.join(base, "04. COLORFUL FE@THERS Series")
print("\n=== 04. COLORFUL FE@THERS Series ===")
for item in sorted(os.listdir(feathers_dir)):
    ip = os.path.join(feathers_dir, item)
    files = os.listdir(ip) if os.path.isdir(ip) else []
    audio = [x for x in files if x.endswith(('.flac', '.wav', '.wv', '.m4a', '.aif', '.aiff'))]
    print(f"  {item}: {len(audio)} audio, other: {[x for x in files if x not in audio]}")
