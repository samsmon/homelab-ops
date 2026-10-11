import os
import subprocess

gakumas = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~"

def inspect_flac(p):
    out = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', '--show-tag=TITLE', '--show-tag=ARTIST', '--show-tag=ALBUM', p], universal_newlines=True).strip().splitlines()
    return f"{os.path.getsize(p)} bytes | " + " | ".join(out)

print("=== CHECKING _ALT FILES ===")
alt_dirs = [
    "01. Solo/03. 藤田ことね (Kotone Fujita)/かちドキ",
    "01. Solo/10. 花海佑芽 (Ume Hanami)/真っ白いページと水彩の主人公",
    "01. Solo/11. 秦谷美鈴 (Misuzu Hataya)/Superlative",
    "01. Solo/11. 秦谷美鈴 (Misuzu Hataya)/VEIL",
    "01. Solo/13. 雨夜燕 (Tsubame Amaya)/MY STAGE",
    "01. Solo/13. 雨夜燕 (Tsubame Amaya)/三分半の創世",
    "04. All Stars & Units/ガラクタロード"
]

for ad in alt_dirs:
    p = os.path.join(gakumas, ad)
    print(f"\n--- {ad} ---")
    if os.path.exists(p):
        for f in sorted(os.listdir(p)):
            if f.endswith('.flac'):
                fp = os.path.join(p, f)
                print(f"  {f}: {inspect_flac(fp)}")

print("\n=== CHECKING 1ST SINGLE VS DIGITAL ===")
single_checks = [
    ("01. Solo/01. 花海咲季 (Saki Hanami)", "Fighting My Way"),
    ("01. Solo/02. 月村手毬 (Temari Tsukimura)", "Luna say maybe"),
    ("01. Solo/03. 藤田ことね (Kotone Fujita)", "世界一可愛い私"),
    ("01. Solo/03. 藤田ことね (Kotone Fujita)", "かちドキ")
]

for parent, name in single_checks:
    p_dir = os.path.join(gakumas, parent)
    print(f"\n--- {parent} : {name} ---")
    d1 = os.path.join(p_dir, name)
    # find cd folder
    cd_folders = [d for d in os.listdir(p_dir) if d.startswith(name) and d != name]
    print(f"Digital: {name} (exists: {os.path.exists(d1)})")
    if os.path.exists(d1):
        for f in sorted(os.listdir(d1)):
            if f.endswith('.flac'):
                print(f"  [Digital] {f}: {inspect_flac(os.path.join(d1, f))}")
    for cdf in cd_folders:
        cd_path = os.path.join(p_dir, cdf)
        print(f"CD: {cdf} (exists: True)")
        for f in sorted(os.listdir(cd_path)):
            if f.endswith('.flac'):
                print(f"  [CD] {f}: {inspect_flac(os.path.join(cd_path, f))}")

print("\n=== CHECKING GOLD RUSH 第3巻 ===")
gr3 = os.path.join(gakumas, "04. All Stars & Units/GOLD RUSH 第3巻 オリジナルCD付き特装版")
if os.path.exists(gr3):
    for r, d, f in os.walk(gr3):
        print(r, d, f)
