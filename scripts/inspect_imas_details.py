from pathlib import Path

imas = Path('/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~')
for p in imas.iterdir():
    print(f"=== {repr(p.name)} ===")
    if p.is_dir():
        for sub in sorted(p.iterdir()):
            print(f"   {repr(sub.name)}")
            if sub.is_dir() and len(list(sub.iterdir())) < 15:
                for sub2 in sorted(sub.iterdir()):
                    if sub2.is_dir():
                        print(f"       -> {repr(sub2.name)}")
