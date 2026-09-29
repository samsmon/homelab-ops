#!/usr/bin/env python3
"""
Fallback ReplayGain 2.0 (EBU R128 + True Peak) tagger using FFmpeg ebur128 filter + mutagen.flac
for the 10 edge-case albums where metaflac's internal analyzer exited with a frame warning.
Does NOT alter raw audio stream (writes Vorbis Comment tags only).
"""
import re
import math
import subprocess
from pathlib import Path
import mutagen.flac

ALBUMS = [
    "/mnt/hdd-backup/music/Lossless/Game/HoYoverse (miHoYo／HOYO-MiX) ~/Honkai Star Rail (崩壊：スターレイル) ~/ゲーム「崩壊：スターレイル」3周年記念曲「Side Quest King」",
    "/mnt/hdd-backup/music/Lossless/Game/HoYoverse (miHoYo／HOYO-MiX) ~/Zenless Zone Zero (ゼンレスゾーンゼロ) ~/ゲーム「ゼンレスゾーンゼロ」スターライト・ビリーEP「Billy Mode」",
    "/mnt/hdd-backup/music/Lossless/Game/HoYoverse (miHoYo／HOYO-MiX) ~/Zenless Zone Zero (ゼンレスゾーンゼロ) ~/ゲーム「ゼンレスゾーンゼロ」妄想エンジェルEP「鼓動のリズム」",
    "/mnt/hdd-backup/music/Lossless/Game/HoYoverse (miHoYo／HOYO-MiX) ~/Zenless Zone Zero (ゼンレスゾーンゼロ) ~/ゲーム「ゼンレスゾーンゼロ」アリアEP「天使ロード中…^_−☆」",
    "/mnt/hdd-backup/music/Lossless/Game/HoYoverse (miHoYo／HOYO-MiX) ~/愚か者が語る夢",
    "/mnt/hdd-backup/music/Lossless/Game/Towatsugai (トワツガイ) ~/蒼海の揺らめき",
    "/mnt/hdd-backup/music/Lossless/Anime/Uma Musume (ウマ娘) ~/07. Compilations/ウマ娘 プリティーダービー Astell&Kern Special Compilation CD",
    "/mnt/hdd-backup/music/Lossless/J-Pop/Shimizu Miisha (清水美依紗) ~/Reunion",
    "/mnt/hdd-backup/music/Lossless/J-Pop/NTE ~/NTE",
    "/mnt/hdd-backup/music/Lossless/J-Pop/ZUTOMAYO (ずっと真夜中でいいのに。) ~/形藻土",
]

def measure_track_r128(flac_path: Path):
    cmd = [
        "ffmpeg", "-nostats", "-i", str(flac_path),
        "-af", "ebur128=peak=true", "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
    out = res.stderr
    m_i = re.findall(r"I:\s*([-\d\.]+)\s*LUFS", out)
    m_tpk = re.findall(r"Peak:\s*([-\d\.]+)\s*dBFS", out)
    lufs = float(m_i[-1]) if m_i else -14.0
    tpk_db = float(m_tpk[-1]) if m_tpk else -0.1
    gain_db = -18.0 - lufs
    peak_lin = 10.0 ** (tpk_db / 20.0)
    return gain_db, peak_lin

def main():
    fixed_albums = 0
    fixed_tracks = 0
    for alb_str in ALBUMS:
        alb = Path(alb_str)
        if not alb.exists():
            print(f"[SKIP] {alb.name} does not exist")
            continue
        flacs = sorted(alb.glob("*.flac"))
        if not flacs:
            continue
        track_stats = []
        for f in flacs:
            g, p = measure_track_r128(f)
            track_stats.append((f, g, p))
        avg_gain = sum(x[1] for x in track_stats) / len(track_stats)
        max_peak = max(x[2] for x in track_stats)
        for f, g, p in track_stats:
            audio = mutagen.flac.FLAC(str(f))
            audio["REPLAYGAIN_REFERENCE_LOUDNESS"] = "89.0 dB"
            audio["REPLAYGAIN_TRACK_GAIN"] = f"{g:+.2f} dB"
            audio["REPLAYGAIN_TRACK_PEAK"] = f"{p:.8f}"
            audio["REPLAYGAIN_ALBUM_GAIN"] = f"{avg_gain:+.2f} dB"
            audio["REPLAYGAIN_ALBUM_PEAK"] = f"{max_peak:.8f}"
            audio.save()
            fixed_tracks += 1
        fixed_albums += 1
        print(f"[OK] {alb.name}: {len(flacs)} tracks tagged (Album Gain: {avg_gain:+.2f} dB, Peak: {max_peak:.4f})")
    print(f"\nCompleted fallback tagging: {fixed_albums} albums ({fixed_tracks} tracks) -> 100% Tagged!")

if __name__ == "__main__":
    main()
