import os
import shutil
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

print("==================================================================")
print("=== STARTING MASTER PERFECTION EXECUTION ===")
print("==================================================================")

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
def move_merge(src, dst):
    if not os.path.exists(src):
        return
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s_item = os.path.join(src, item)
        d_item = os.path.join(dst, item)
        if os.path.isdir(s_item):
            if os.path.exists(d_item):
                move_merge(s_item, d_item)
            else:
                shutil.move(s_item, d_item)
        else:
            if not os.path.exists(d_item):
                shutil.move(s_item, d_item)
            else:
                # file collision: if dst is larger, keep dst, else overwrite
                if os.path.getsize(s_item) > os.path.getsize(d_item):
                    os.remove(d_item)
                    shutil.move(s_item, d_item)
                else:
                    os.remove(s_item)
    if os.path.exists(src) and not os.listdir(src):
        os.rmdir(src)

# ---------------------------------------------------------
# PHASE 1: CUE SPLITTING (Mamyukka)
# ---------------------------------------------------------
print("\n--- PHASE 1: CUE SPLITTING ---")
mamyukka_dir = os.path.join(ROOT, "Doujinshi", "Mamyukka ~")

# 1. テアトルエトワール
t_dir = os.path.join(mamyukka_dir, "テアトルエトワール")
t_cue = os.path.join(t_dir, "テアトルエトワール.cue")
t_flac = os.path.join(t_dir, "テアトルエトワール.flac")
if os.path.exists(t_cue) and os.path.exists(t_flac):
    print("Splitting テアトルエトワール...")
    # read cp932 cue, fix FILE
    with open(t_cue, 'rb') as f:
        content = f.read().decode('cp932', errors='replace')
    fixed = []
    for line in content.splitlines():
        if line.strip().upper().startswith("FILE "):
            fixed.append('FILE "テアトルエトワール.flac" WAVE')
        else:
            fixed.append(line)
    tmp_cue = os.path.join(t_dir, "split.cue")
    with open(tmp_cue, 'w', encoding='utf-8') as f:
        f.write("\n".join(fixed))
    cmd = ['shnsplit', '-f', tmp_cue, '-t', '%n. %t', '-o', 'flac', '-P', 'none', '-d', t_dir, t_flac]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if res.returncode == 0:
        print("  Successfully split テアトルエトワール into FLAC tracks.")
        os.remove(t_flac)
        os.remove(t_cue)
        if os.path.exists(tmp_cue):
            os.remove(tmp_cue)
    else:
        print("  Error splitting テアトルエトワール:", res.stderr)

# 2. THE 13th PANCER
p_dir = os.path.join(mamyukka_dir, "THE 13th PANCER")
p_cue = os.path.join(p_dir, "THE 13th PANCER.cue")
p_flac = os.path.join(p_dir, "THE 13th PANCER.flac")
if os.path.exists(p_cue) and os.path.exists(p_flac):
    print("Splitting THE 13th PANCER...")
    with open(p_cue, 'rb') as f:
        content = f.read().decode('utf-8', errors='replace')
    fixed = []
    for line in content.splitlines():
        if line.strip().upper().startswith("FILE "):
            fixed.append('FILE "THE 13th PANCER.flac" WAVE')
        else:
            fixed.append(line)
    tmp_cue = os.path.join(p_dir, "split.cue")
    with open(tmp_cue, 'w', encoding='utf-8') as f:
        f.write("\n".join(fixed))
    cmd = ['shnsplit', '-f', tmp_cue, '-t', '%n. %t', '-o', 'flac', '-P', 'none', '-d', p_dir, p_flac]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if res.returncode == 0:
        print("  Successfully split THE 13th PANCER into FLAC tracks.")
        os.remove(p_flac)
        os.remove(p_cue)
        if os.path.exists(tmp_cue):
            os.remove(tmp_cue)
    else:
        print("  Error splitting THE 13th PANCER:", res.stderr)

# Remove redundant CUE clutter
cues_to_remove = [
    os.path.join(ROOT, "Doujinshi/Shinra-bansho (森羅万象) ~/toge/toge.cue"),
    os.path.join(ROOT, "Vtuber/Azuma Seren (東雪蓮) ~/KEEP OUT {AZSE-0009}/KEEP OUT.cue"),
    os.path.join(ROOT, "Vtuber/Hololive (ホロライブ) ~/Mori Calliope ~/DISASTERPIECE/DISASTERPIECE.cue"),
    os.path.join(ROOT, "J-Pop/TUYU (ツユ) ~/「アンダーキッズ」ピアノアレンジCD/DSP-02365.cue"),
    os.path.join(ROOT, "J-Pop/Various Artists ~/｢カーストルーム｣ ／ZAQ/LACM-14647.cue"),
    os.path.join(ROOT, "Doujinshi/Mamyukka ~/Trick Or Mamyukka/Mamyukka - Trick Or Mamyukka.cue"),
    os.path.join(ROOT, "Doujinshi/PROTOCOLLON ~/J-HYPER NATION {PRT-003}/J-HYPER NATION.cue"),
    os.path.join(ROOT, "Doujinshi/PROTOCOLLON ~/J-HYPER NATION {PRT-003}/J-HYPER NATION.log")
]
for cp in cues_to_remove:
    if os.path.exists(cp):
        os.remove(cp)
        print(f"Removed redundant CUE/log: {cp}")

# ---------------------------------------------------------
# PHASE 2: REDUNDANT DUPLICATES & DEFORMED DIRECTORIES
# ---------------------------------------------------------
print("\n--- PHASE 2: REDUNDANT DUPLICATES PURGE ---")

# 1. PROTOCOLLON duplicate files
proto_dir = os.path.join(ROOT, "Doujinshi/PROTOCOLLON ~/J-HYPER NATION {PRT-003}")
if os.path.exists(proto_dir):
    for f in os.listdir(proto_dir):
        if "_dup" in f:
            fp = os.path.join(proto_dir, f)
            os.remove(fp)
            print(f"Removed PROTOCOLLON duplicate file: {f}")

# 2. Shirakami Fubuki unbracketed duplicate
fubuki_bad = os.path.join(ROOT, "Vtuber/Hololive (ホロライブ) ~/Shirakami Fubuki (白上フブキ) ~/hololive 白上フブキ , さくらみこ , 百鬼あやめ , 大神ミオ EPヤマトファンタジア」")
if os.path.exists(fubuki_bad):
    shutil.rmtree(fubuki_bad)
    print(f"Removed Fubuki defective duplicate folder: {fubuki_bad}")

# 3. Singles redundant with full/deluxe releases
singles_to_purge = [
    os.path.join(ROOT, "J-Pop/Nishino Kana Feat. Niziu (西野カナ feat. NiziU) ~/LOVE BEAT (Single Edition)"),
    os.path.join(ROOT, "J-Pop/Nogizaka46 (乃木坂46) ~/是非に及ばず"),
    os.path.join(ROOT, "J-Pop/H／／PE Princess ~/17.7")
]
for sp in singles_to_purge:
    if os.path.exists(sp):
        shutil.rmtree(sp)
        print(f"Purged redundant single folder: {sp}")

# ---------------------------------------------------------
# PHASE 3: J-POP SPLIT ARTISTS CONSOLIDATION
# ---------------------------------------------------------
print("\n--- PHASE 3: J-POP SPLIT ARTISTS CONSOLIDATION ---")
jpop = os.path.join(ROOT, "J-Pop")

artist_merges = [
    ("96 Neko (96猫) ~", "96Neko (96猫) ~"),
    ("9lana ~", "9Lana ~"),
    ("Ado ~", "Ado (アド) ~"),
    ("Boku Ga Mita Katta Aozora (僕が見たかった青空) ~", "Boku ga Mitakatta Aozora (僕が見たかった青空) ~"),
    ("Cö Shu Nie ~", "Cö shu Nie ~"),
    ("Haku . (ハク。) ~", "Haku. (ハク。) ~"),
    ("Kotonohouse ~", "KOTONOHOUSE ~"),
    ("Miminari ~", "MIMiNARI ~"),
    ("Milet ~", "milet ~"),
    ("Murasaki Ima (紫今) ~", "Murasaki Ima (紫 今) ~"),
    ("Nomelon Nolemon ~", "NOMELON NOLEMON ~"),
    ("No Hana Koyori (乃花こより) ~", "Nohana Koyori (乃花こより) ~"),
    ("Sa Na (紗奈) ~", "Sana (鎖那) ~"),
    ("SawanoHiroyuki ~", "Sawano Hiroyuki (澤野弘之) ~"),
    ("Takane Nonadeshiko (高嶺のなでしこ) ~", "Takane no Nadeshiko (高嶺のなでしこ) ~"),
    ("Tsukuyomi ~", "Tsukuyomi (月詠み) ~"),
    ("Washio Rei Na (鷲尾伶菜) ~", "Washio Reina (鷲尾伶菜) ~"),
    ("YU-KA (由薫) ~", "Yu-ka (由薫) ~"),
    ("otsumami feat.mikan ~", "otsumami feat. mikan ~")
]

for src_name, dst_name in artist_merges:
    src_p = os.path.join(jpop, src_name)
    dst_p = os.path.join(jpop, dst_name)
    if os.path.exists(src_p):
        print(f"Merging J-Pop: '{src_name}' -> '{dst_name}'")
        move_merge(src_p, dst_p)

# Normalize Su Mi Ka (す み か) ~ to Sumika (す み か) ~
sumika_bad = os.path.join(jpop, "Su Mi Ka (す み か) ~")
sumika_good = os.path.join(jpop, "Sumika (す み か) ~")
if os.path.exists(sumika_bad):
    print("Normalizing Su Mi Ka (す み か) ~ -> Sumika (す み か) ~")
    os.rename(sumika_bad, sumika_good)

# ---------------------------------------------------------
# PHASE 4: SHINY COLORS RESTRUCTURING & CLEANUP
# ---------------------------------------------------------
print("\n--- PHASE 4: SHINY COLORS PERFECTION ---")

# 1. CANVAS Series: Merge cover/order from _CANVAS_ into ''CANVAS''
canvas_dir = os.path.join(ROOT, "Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/01. WING & Main Game Series/06. CANVAS")
if os.path.exists(canvas_dir):
    for i in range(1, 9):
        num = f"{i:02d}"
        empty_canvas = os.path.join(canvas_dir, f"THE IDOLM@STER SHINY COLORS _CANVAS_ {num}")
        real_canvas = os.path.join(canvas_dir, f"THE IDOLM@STER SHINY COLORS ''CANVAS'' {num}")
        if os.path.exists(empty_canvas) and os.path.exists(real_canvas):
            print(f"Moving covers from _CANVAS_ {num} -> ''CANVAS'' {num}...")
            for f in os.listdir(empty_canvas):
                shutil.move(os.path.join(empty_canvas, f), os.path.join(real_canvas, f))
            os.rmdir(empty_canvas)

# 2. Song for Prism Series: Empty folders with _ instead of ／
sc_prism = os.path.join(ROOT, "Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/02. Song for Prism Series")
if os.path.exists(sc_prism):
    for d in list(os.listdir(sc_prism)):
        dp = os.path.join(sc_prism, d)
        if not os.path.isdir(dp):
            continue
        audio = [f for f in os.listdir(dp) if f.endswith(('.flac', '.wav', '.wv', '.m4a', '.aif', '.aiff'))]
        if len(audio) == 0 and (" _ " in d or " 快盗Vを見逃すな" in d or " グッバイ" in d or " THE LAST PRIDE" in d or " サマーサマーオーシャンパーリィバケーション" in d):
            # Find counterpart
            c_name = d.replace(" _ ", " ／ ").replace("  快盗V", " ／ 快盗V").replace(" 快盗V", " ／ 快盗V").replace(" グッバイ", " ／ グッバイ").replace(" THE LAST PRIDE", " ／ THE LAST PRIDE").replace(" 愛なView サマーサマーオーシャンパーリィバケーション", " ／ 愛なView ／ サマーサマーオーシャンパーリィバケーション")
            counterpart = os.path.join(sc_prism, c_name)
            if not os.path.exists(counterpart):
                # Try without space around slash
                c_name2 = d.replace(" _ ", "／")
                counterpart = os.path.join(sc_prism, c_name2)
            
            print(f"Empty Prism folder: '{d}' -> counterpart: '{os.path.basename(counterpart)}' (exists: {os.path.exists(counterpart)})")
            if os.path.exists(counterpart):
                for f in os.listdir(dp):
                    tgt = os.path.join(counterpart, f)
                    if not os.path.exists(tgt):
                        shutil.move(os.path.join(dp, f), tgt)
                    else:
                        os.remove(os.path.join(dp, f))
                os.rmdir(dp)

    # 3. 神様は死んだ、って: flatten nested
    kami_dir = os.path.join(sc_prism, "神様は死んだ、って")
    if os.path.exists(kami_dir):
        deep_dir = os.path.join(kami_dir, "斑鳩ルカ (CV．川口莉奈)", "神様は死んだ、って")
        if os.path.exists(deep_dir):
            print("Flattening 神様は死んだ、って nested tracks...")
            for f in os.listdir(deep_dir):
                shutil.move(os.path.join(deep_dir, f), os.path.join(kami_dir, f))
            os.rmdir(deep_dir)
            middle_dir = os.path.join(kami_dir, "斑鳩ルカ (CV．川口莉奈)")
            if os.path.exists(middle_dir) and not os.listdir(middle_dir):
                os.rmdir(middle_dir)

    # 4. Tokyo自由系＊ガール／My time: Purge 16-bit duplicates and nested subdir
    tokyo_dir = os.path.join(sc_prism, "THE IDOLM@STER SHINY COLORS Song for Prism Tokyo自由系＊ガール／My time")
    if os.path.exists(tokyo_dir):
        print("Cleaning Tokyo自由系＊ガール／My time 16-bit duplicates...")
        for f in [
            "01. Tokyo自由系＊ガール.flac",
            "02. My time.flac",
            "03. Tokyo自由系＊ガール (Game Size).flac",
            "04. My time (Game Size).flac",
            "05. Tokyo自由系＊ガール (Off Vocal).flac",
            "06. My time (Off Vocal).flac"
        ]:
            fp = os.path.join(tokyo_dir, f)
            if os.path.exists(fp):
                os.remove(fp)
        nested_dir = os.path.join(tokyo_dir, "No 1 feel alone")
        if os.path.exists(nested_dir):
            shutil.rmtree(nested_dir)

    # 5. ボーダーレス・ノンストレス／Oh Yeah!!: Purge 16-bit duplicates
    border_dir = os.path.join(sc_prism, "THE IDOLM@STER SHINY COLORS Song for Prism ボーダーレス・ノンストレス／Oh Yeah!!")
    if os.path.exists(border_dir):
        print("Cleaning ボーダーレス・ノンストレス／Oh Yeah!! 16-bit duplicates...")
        for f in [
            "01. ボーダーレス・ノンストレス.flac",
            "02. Oh Yeah!!.flac",
            "03. ボーダーレス・ノンストレス (Game Size).flac",
            "04. Oh Yeah!! (Game Size).flac",
            "05. ボーダーレス・ノンストレス (Off Vocal).flac",
            "06. Oh Yeah!! (Off Vocal).flac"
        ]:
            fp = os.path.join(border_dir, f)
            if os.path.exists(fp):
                os.remove(fp)

    # 6. SUPER DUPER DREAMER／BEAST MODE: Purge duplicate filenames
    sdd_dir = os.path.join(sc_prism, "THE IDOLM@STER SHINY COLORS Song for Prism SUPER DUPER DREAMER／BEAST MODE")
    if os.path.exists(sdd_dir):
        print("Cleaning SUPER DUPER DREAMER duplicates...")
        for f in [
            "01 SUPER DUPER DREAMER.flac",
            "02 BEAST MODE.flac",
            "03 SUPER DUPER DREAMER (Game Size).flac",
            "04 BEAST MODE (Game Size).flac",
            "05 SUPER DUPER DREAMER (Off Vocal).flac",
            "06 BEAST MODE (Off Vocal).flac"
        ]:
            fp = os.path.join(sdd_dir, f)
            if os.path.exists(fp):
                os.remove(fp)

    # 7. 散花-sanka-／紅花-benibana-: Purge duplicate filenames
    sanka_dir = os.path.join(sc_prism, "THE IDOLM@STER SHINY COLORS Song for Prism 散花-sanka-／紅花-benibana-")
    if os.path.exists(sanka_dir):
        print("Cleaning 散花-sanka- duplicates...")
        for f in [
            "01. 散花-sanka-.flac",
            "02. 紅花-benibana-.flac",
            "03. 散花-sanka- (Game Size).flac",
            "04. 紅花-benibana- (Game Size).flac",
            "05. 散花-sanka- (Off Vocal).flac",
            "06. 紅花-benibana- (Off Vocal).flac"
        ]:
            fp = os.path.join(sanka_dir, f)
            if os.path.exists(fp):
                os.remove(fp)

    # 8. C'mon! Join Us duplicate directory merge
    cmon_with_space = os.path.join(sc_prism, "THE IDOLM@STER SHINY COLORS Song for Prism C'mon! Join Us ／ 愛なView ／ サマーサマーオーシャンパーリィバケーション")
    cmon_no_space = os.path.join(sc_prism, "THE IDOLM@STER SHINY COLORS Song for Prism C'mon! Join Us／愛なView／サマーサマーオーシャンパーリィバケーション")
    if os.path.exists(cmon_with_space) and os.path.exists(cmon_no_space):
        print("Merging C'mon! Join Us duplicate folders...")
        for f in os.listdir(cmon_with_space):
            tgt = os.path.join(cmon_no_space, f)
            if not os.path.exists(tgt):
                shutil.move(os.path.join(cmon_with_space, f), tgt)
        shutil.rmtree(cmon_with_space)

print("\n==================================================================")
print("=== MASTER PERFECTION EXECUTION FINISHED ===")
print("==================================================================")
