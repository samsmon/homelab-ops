import subprocess
import os

sample_aiff = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/01. WING & Main Game Series/02. FR@GMENT WING/THE IDOLM@STER SHINY COLORS FR@GMENT WING 05/THE IDOLM@STER SHINY COLORS FR@GMENT WING 05_01_Bloomy!.aiff"

print("--- AIFF TAGS via ffprobe ---")
r = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format_tags:stream_tags",
    "-of", "default=noprint_wrappers=1", sample_aiff
], capture_output=True, text=True)
print(r.stdout)

# Test flac direct conversion
test_out = "/tmp/test_bloomy.flac"
if os.path.exists(test_out):
    os.remove(test_out)

r_flac = subprocess.run(["flac", "--best", "--verify", "-o", test_out, sample_aiff], capture_output=True, text=True)
print("flac returncode:", r_flac.returncode)

# Check tags in test_out
r_tags = subprocess.run(["metaflac", "--export-tags-to=-", test_out], capture_output=True, text=True)
print("tags in converted FLAC:")
print(r_tags.stdout)

# Also test ffmpeg conversion
test_out_ffmpeg = "/tmp/test_bloomy_ffmpeg.flac"
if os.path.exists(test_out_ffmpeg):
    os.remove(test_out_ffmpeg)
subprocess.run(["ffmpeg", "-y", "-i", sample_aiff, "-c:a", "flac", "-compression_level", "8", test_out_ffmpeg], capture_output=True, text=True)
r_ff_tags = subprocess.run(["metaflac", "--export-tags-to=-", test_out_ffmpeg], capture_output=True, text=True)
print("tags in ffmpeg FLAC:")
print(r_ff_tags.stdout)
