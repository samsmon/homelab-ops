import os

canvas_dir = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/01. Main Discography Series/06. CANVAS"
print("=== 06. CANVAS CONTENTS ===")
for d in sorted(os.listdir(canvas_dir)):
    dp = os.path.join(canvas_dir, d)
    files = os.listdir(dp)
    print(f"  {d}: {len(files)} files -> {files[:3]}")

feathers_dir = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/04. COLORFUL FE@THERS Series"
print("\n=== COLORFUL FEATHERS CONTENTS ===")
for d in sorted(os.listdir(feathers_dir)):
    dp = os.path.join(feathers_dir, d)
    files = os.listdir(dp)
    print(f"  {d}: {len(files)} files -> {files[:3]}")
