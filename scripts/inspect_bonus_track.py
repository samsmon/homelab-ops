import subprocess

fp = "/mnt/hdd-backup/music/Lossless/Vtuber/La Prière ~/Galaxy Triangle/Bonus Track.mp3"
r = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format_tags:stream_tags",
    "-of", "default=noprint_wrappers=1", fp
], capture_output=True, text=True)
print("Tags:")
print(r.stdout)
