import os

sc = '/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/02. Song for Prism Series'

for d in sorted(os.listdir(sc)):
    dp = os.path.join(sc, d)
    if os.path.isdir(dp):
        audio = [f for f in os.listdir(dp) if f.endswith(('.flac', '.wav', '.wv', '.m4a'))]
        if len(audio) > 6:
            print(f"=== {d} ({len(audio)} audio files) ===")
            for a in sorted(audio):
                sz = os.path.getsize(os.path.join(dp, a))
                print(f"  {a} ({sz} bytes)")
