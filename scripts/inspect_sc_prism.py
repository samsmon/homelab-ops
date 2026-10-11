import os

sc_prism_dir = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/02. Song for Prism Series"
print("=== SHINY COLORS SONG FOR PRISM SERIES ALL DIRS ===")
for d in sorted(os.listdir(sc_prism_dir)):
    dp = os.path.join(sc_prism_dir, d)
    if os.path.isdir(dp):
        files = os.listdir(dp)
        audio = [f for f in files if f.endswith(('.flac', '.wav', '.m4a'))]
        subdirs = [f for f in files if os.path.isdir(os.path.join(dp, f))]
        print(f"Dir: {d}")
        print(f"  Audio: {len(audio)}, Subdirs: {subdirs}, Other files: {[f for f in files if not f.endswith(('.flac', '.wav', '.m4a')) and not os.path.isdir(os.path.join(dp, f))]}")
