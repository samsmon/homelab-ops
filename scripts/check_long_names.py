#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

root = Path("/mnt/hdd-backup/music/Lossless")
for p in root.glob("*/*"):
    if len(p.name.encode("utf-8")) > 100:
        print(len(p.name.encode("utf-8")), str(p.relative_to(root)))
