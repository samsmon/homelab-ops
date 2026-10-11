#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

lossless = Path('/mnt/hdd-backup/music/Lossless')

# 1. Gilded Dreams -> Revue Starlight
eldorado = lossless / 'J-Pop' / '遙かなるエルドラド テーマソング「Gilded Dreams」 ~'
starlight = lossless / 'Anime' / 'Revue Starlight (少女☆歌劇 レヴュースタァライト) ~' / 'Gilded Dreams'
if eldorado.exists():
    starlight.parent.mkdir(parents=True, exist_ok=True)
    inner = eldorado / 'Gilded Dreams'
    if inner.exists():
        shutil.move(str(inner), str(starlight))
    else:
        shutil.move(str(eldorado), str(starlight))
    try: shutil.rmtree(str(eldorado))
    except Exception: pass
    print("Moved Gilded Dreams to Revue Starlight.")

# 2. Iroawase
iro = lossless / 'J-Pop' / 'イロアワセ キャラクターソングHIRAETH」 ~'
iro_target = lossless / 'Anime' / 'Iroawase (イロアワセ) ~' / 'HIRAETH'
if iro.exists():
    iro_target.parent.mkdir(parents=True, exist_ok=True)
    for item in list(iro.iterdir()):
        shutil.move(str(item), str(iro_target))
    try: iro.rmdir()
    except Exception: pass
    print("Moved Iroawase to Anime/Iroawase (イロアワセ) ~.")

# 3. MEDA
meda = lossless / 'J-Pop' / 'MEDA ~'
rk_meda = lossless / 'Vtuber' / 'RK Music ~' / 'MEDA ~'
if meda.exists():
    rk_meda.mkdir(parents=True, exist_ok=True)
    for item in list(meda.iterdir()):
        shutil.move(str(item), str(rk_meda / item.name))
    try: meda.rmdir()
    except Exception: pass
    print("Merged MEDA into RK Music.")

print("Finished moving 3 items.")
