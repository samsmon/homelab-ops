import os

sc = '/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/02. Song for Prism Series'
for sub in ['神様は死んだ、って', 'THE IDOLM@STER SHINY COLORS Song for Prism Tokyo自由系＊ガール／My time']:
    p = os.path.join(sc, sub)
    print(f"=== {sub} ===")
    for r, d, f in os.walk(p):
        print(f"DIR: {r}")
        print(f"  Files: {f}")
