#!/usr/bin/env python3
import sys
import mutagen

p = sys.argv[1]
f = mutagen.File(p)
print(dict(f))
