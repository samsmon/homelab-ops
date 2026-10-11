#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess

def romanize(text: str) -> str:
    p1 = subprocess.Popen(["iconv", "-f", "utf-8", "-t", "euc-jp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["kakasi", "-Ja", "-Ha", "-Ka", "-Ea", "-s"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p3 = subprocess.Popen(["iconv", "-f", "euc-jp", "-t", "utf-8"], stdin=p2.stdout, stdout=subprocess.PIPE)
    p2.stdout.close()
    out, _ = p1.communicate(text.encode('utf-8'))
    out, _ = p3.communicate()
    return out.decode('utf-8').strip()

words = ['うたごえはミルフィーユ', 'ウルトラマンアーク', 'テトリス', 'ばっどがーる', '五等分の花嫁']
for w in words:
    print(f"{w} -> {romanize(w)}")
