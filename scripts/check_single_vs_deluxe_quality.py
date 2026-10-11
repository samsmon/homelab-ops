import os
import subprocess

def check(p):
    out = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', p], universal_newlines=True).strip().split()
    return f"{out[0]}Hz / {out[1]}bit ({os.path.getsize(p)} bytes)"

print("Nishino Kana:")
p1 = "/mnt/hdd-backup/music/Lossless/J-Pop/Nishino Kana Feat. Niziu (西野カナ feat. NiziU) ~/LOVE BEAT (Single Edition)/01. LOVE BEAT.flac"
p2 = "/mnt/hdd-backup/music/Lossless/J-Pop/Nishino Kana Feat. Niziu (西野カナ feat. NiziU) ~/LOVE BEAT (Full Release)/01. LOVE BEAT.flac"
print("  Single:", check(p1))
print("  Full  :", check(p2))

print("Nogizaka46:")
p1 = "/mnt/hdd-backup/music/Lossless/J-Pop/Nogizaka46 (乃木坂46) ~/是非に及ばず/01. 是非に及ばず.flac"
p2 = "/mnt/hdd-backup/music/Lossless/J-Pop/Nogizaka46 (乃木坂46) ~/是非に及ばず (Special Edition)/01. 是非に及ばず.flac"
print("  Single:", check(p1))
print("  Full  :", check(p2))

print("H//PE Princess:")
p1 = "/mnt/hdd-backup/music/Lossless/J-Pop/H／／PE Princess ~/17.7/01. Stolen.flac"
p2 = "/mnt/hdd-backup/music/Lossless/J-Pop/H／／PE Princess ~/17.7 (Japan Deluxe Edition)/01. Stolen.flac"
print("  Standard:", check(p1))
print("  Deluxe  :", check(p2))
