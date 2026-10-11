import os
import subprocess

p1 = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/02. Song for Prism Series/THE IDOLM@STER SHINY COLORS Song for Prism C'mon! Join Us ／ 愛なView ／ サマーサマーオーシャンパーリィバケーション/01 - シャイニーカラーズ - C'mon! Join Us.flac"
p2 = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/02. Song for Prism Series/THE IDOLM@STER SHINY COLORS Song for Prism C'mon! Join Us／愛なView／サマーサマーオーシャンパーリィバケーション/01. C'mon! Join Us.flac"

def check(p):
    out = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', p], universal_newlines=True).strip().split()
    return f"{out[0]}Hz / {out[1]}bit ({os.path.getsize(p)} bytes)"

print("C'mon Join Us with spaces:", check(p1))
print("C'mon Join Us without spaces:", check(p2))
