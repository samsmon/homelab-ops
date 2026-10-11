import os

sc_base = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~"

print(f"=== CHECKING ALL SUBDIRS IN SHINY COLORS: {sc_base} ===")
for series in sorted(os.listdir(sc_base)):
    sp = os.path.join(sc_base, series)
    if os.path.isdir(sp):
        print(f"\nSeries: {series}")
        subdirs = sorted(os.listdir(sp))
        for s in subdirs:
            s_path = os.path.join(sp, s)
            if os.path.isdir(s_path):
                audio = [f for f in os.listdir(s_path) if f.endswith(('.flac', '.wav', '.wv', '.m4a'))]
                inner_dirs = [f for f in os.listdir(s_path) if os.path.isdir(os.path.join(s_path, f))]
                if len(audio) == 0:
                    print(f"  [EMPTY/NO AUDIO] {s} (subdirs: {inner_dirs})")
                elif len(inner_dirs) > 0:
                    print(f"  [HAS SUBDIRS] {s} ({len(audio)} audio, subdirs: {inner_dirs})")
