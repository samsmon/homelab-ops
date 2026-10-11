import os
import subprocess

sc_prism = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/02. Song for Prism Series"

albums = [
    "THE IDOLM@STER SHINY COLORS Song for Prism SUPER DUPER DREAMER／BEAST MODE",
    "THE IDOLM@STER SHINY COLORS Song for Prism Tokyo自由系＊ガール／My time",
    "THE IDOLM@STER SHINY COLORS Song for Prism ボーダーレス・ノンストレス／Oh Yeah!!",
    "THE IDOLM@STER SHINY COLORS Song for Prism 散花-sanka-／紅花-benibana-"
]

for a in albums:
    p = os.path.join(sc_prism, a)
    print(f"=== {a} ===")
    for f in sorted(os.listdir(p)):
        if f.endswith('.flac'):
            fp = os.path.join(p, f)
            out = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', fp], universal_newlines=True).strip().split()
            print(f"  {f}: {out[0]}Hz / {out[1]}bit ({os.path.getsize(fp)} bytes)")
