#!/usr/bin/env python3
import mutagen.flac
from pathlib import Path

target_dir = Path("/mnt/hdd-backup/music/Lossless/Anime/Denonbu (電音部) ~/0：00 (Prod. Funk Uchino)")

t1 = mutagen.flac.FLAC(target_dir / "01. 0：00 (Prod. Funk Uchino).flac")
t1["ALBUM"] = "0：00 (Prod. Funk Uchino)"
t1["TITLE"] = "0：00 (Prod. Funk Uchino)"
t1["ARTIST"] = "白金 煌 (CV: 小宮有紗)"
t1["ALBUMARTIST"] = "電音部"
t1["DATE"] = "2024-10-23"
t1["TRACKNUMBER"] = "01"
t1["TRACKTOTAL"] = "02"
t1["ORGANIZATION"] = "ASOBINOTES"
t1["ISRC"] = "JPR502416190"
t1.save()

t2 = mutagen.flac.FLAC(target_dir / "02. 0：00 (Prod. Funk Uchino) [Instrumental].flac")
t2["ALBUM"] = "0：00 (Prod. Funk Uchino)"
t2["TITLE"] = "0：00 (Prod. Funk Uchino) [Instrumental]"
t2["ARTIST"] = "白金 煌 (CV: 小宮有紗)"
t2["ALBUMARTIST"] = "電音部"
t2["DATE"] = "2024-10-23"
t2["TRACKNUMBER"] = "02"
t2["TRACKTOTAL"] = "02"
t2["ORGANIZATION"] = "ASOBINOTES"
t2.save()

print("Clean UTF-8 Vorbis tags saved successfully with mutagen.")
