import os
import subprocess

p1 = "/mnt/hdd-backup/music/Lossless/Game/O.N.G.E.K.I. (オンゲキ) ~/ONGEKI 6th Anniversary CD「Individual on parade!」"
p2 = "/mnt/hdd-backup/music/Lossless/Game/O.N.G.E.K.I. (オンゲキ) ~/ONGEKI Collection/2024.07.26 [ZMCZ-17641] ONGEKI 6th Anniversary CD 「Individual on parade!」"

def check_flac(fp):
    r = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate,bits_per_raw_sample",
        "-of", "default=noprint_wrappers=1:nokey=1", fp
    ], capture_output=True, text=True)
    return r.stdout.strip().replace("\n", " / ")

print("P1 track 1:", check_flac(os.path.join(p1, "01 - Individual on parade!.flac")))
print("P2 track 1 (small):", check_flac(os.path.join(p2, "01 - オンゲキシューターズ - Individual on parade!.flac")))
print("P2 track 1 (large):", check_flac(os.path.join(p2, "01-Individual on parade!.flac")))
