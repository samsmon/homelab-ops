import os
import shutil
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

print("==================================================================")
print("=== STARTING MASTER REFINEMENT & WAV-TO-FLAC CONVERSION ===")
print("==================================================================")

def convert_wav_to_flac(folder, delete_wav=True):
    if not os.path.exists(folder):
        return
    print(f"\nConverting WAVs to FLAC in: {folder}")
    for f in sorted(os.listdir(folder)):
        if f.lower().endswith('.wav'):
            wav_path = os.path.join(folder, f)
            flac_name = os.path.splitext(f)[0] + ".flac"
            flac_path = os.path.join(folder, flac_name)
            cmd = ['flac', '--best', '--verify', '-o', flac_path, wav_path]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode == 0 and os.path.exists(flac_path) and os.path.getsize(flac_path) > 0:
                print(f"  Converted {f} -> {flac_name}")
                if delete_wav:
                    os.remove(wav_path)
            else:
                print(f"  Error converting {f}: {res.stderr.decode('utf-8', errors='replace')}")

# -----------------------------------------------------------------
# 1. MOJIBAKE FIX & WAV CONVERSIONS
# -----------------------------------------------------------------
# 1a. Imy: Fix mojibake track 6 before converting
imy_dir = os.path.join(ROOT, "Doujinshi/Imy ~/Beyond the despair")
if os.path.exists(imy_dir):
    for f in os.listdir(imy_dir):
        if "îÄÄ" in f or "06" in f and f.endswith(".wav"):
            bad_path = os.path.join(imy_dir, f)
            good_path = os.path.join(imy_dir, "06. 月時雨.wav")
            print(f"Fixing Imy track 6 mojibake: '{f}' -> '06. 月時雨.wav'")
            os.rename(bad_path, good_path)
    convert_wav_to_flac(imy_dir)

# 1b. Login Records: Never Forget Vacation 8
login_dir = os.path.join(ROOT, "Doujinshi/Login Records ~/Never Forget Vacation 8")
if os.path.exists(login_dir):
    convert_wav_to_flac(login_dir)

# 1c. 7uta -> nayuta: Relocate and convert
seven_uta = os.path.join(ROOT, "J-Pop/7uta ~/想い出を綴った歌を君へ。")
nayuta_target = os.path.join(ROOT, "Doujinshi/nayuta ~/想い出を綴った歌を君へ。")
if os.path.exists(seven_uta):
    print("Relocating 7uta album to Doujinshi/nayuta ~...")
    os.makedirs(os.path.dirname(nayuta_target), exist_ok=True)
    shutil.move(seven_uta, nayuta_target)
    seven_parent = os.path.join(ROOT, "J-Pop/7uta ~")
    if os.path.exists(seven_parent) and not os.listdir(seven_parent):
        os.rmdir(seven_parent)
    convert_wav_to_flac(nayuta_target)

# 1d. Kancolle: Convert and rename folder
kc_old = os.path.join(ROOT, "Game/Kancolle (艦隊これくしょん -艦これ-) ~/艦隊これくしょん -艦これ-」キャラクターソング 艦娘乃歌 Vol.1 [WAV 48.0kHz-24bit]")
kc_new = os.path.join(ROOT, "Game/Kancolle (艦隊これくしょん -艦これ-) ~/「艦隊これくしょん -艦これ-」キャラクターソング “艦娘乃歌” Vol.1")
if os.path.exists(kc_old):
    convert_wav_to_flac(kc_old)
    print("Renaming Kancolle album to canonical title...")
    os.rename(kc_old, kc_new)

# -----------------------------------------------------------------
# 2. RELOCATE HONEYWORKS ALBUM
# -----------------------------------------------------------------
hw_deformed = os.path.join(ROOT, "J-Pop/Kokuhaku Jikkouiinkai -flying Songs- Koishi Teru [48khz (告白実行委員会 -FLYING SONGS- 恋してる[48kHz) ~")
hw_target_parent = os.path.join(ROOT, "J-Pop/HoneyWorks ~")
if os.path.exists(hw_deformed):
    inner_album = os.path.join(hw_deformed, "告白実行委員会 -FLYING SONGS- 恋してる")
    target_album = os.path.join(hw_target_parent, "告白実行委員会 -FLYING SONGS- 恋してる")
    if os.path.exists(inner_album):
        print("Moving HoneyWorks album to J-Pop/HoneyWorks ~...")
        os.makedirs(hw_target_parent, exist_ok=True)
        if not os.path.exists(target_album):
            shutil.move(inner_album, target_album)
        else:
            for item in os.listdir(inner_album):
                shutil.move(os.path.join(inner_album, item), os.path.join(target_album, item))
            os.rmdir(inner_album)
        if os.path.exists(hw_deformed) and not os.listdir(hw_deformed):
            os.rmdir(hw_deformed)

# -----------------------------------------------------------------
# 3. FORMAT TAG RENAMING ACROSS CATEGORIES
# -----------------------------------------------------------------
renames = [
    # Game
    ("Game/O.N.G.E.K.I. (オンゲキ) ~", "2022.11.30 [ZMCZ-15812] ONGEKI Vocal Memory [USB+CD-FLAC]", "ONGEKI Vocal Memory {ZMCZ-15812}"),
    ("Game/Heaven Burns Red (ヘブンバーンズレッド) ~", "Goodbye Innocence HI-RES", "Goodbye Innocence"),
    ("Game/Heaven Burns Red (ヘブンバーンズレッド) ~", "War Alive ~Toki ni wa Yabure Kabure ni~ HI-RES", "War Alive ~Toki ni wa Yabure Kabure ni~"),
    ("Game/Heaven Burns Red (ヘブンバーンズレッド) ~", "Particle Effect HI-RES", "Particle Effect"),
    ("Game/Heaven Burns Red (ヘブンバーンズレッド) ~", "Overkill HI-RES", "Overkill"),
    ("Game/Heaven Burns Red (ヘブンバーンズレッド) ~", "Light Years HI-RES", "Light Years"),
    ("Game/Heaven Burns Red (ヘブンバーンズレッド) ~", "Indigo in Blue HI-RES", "Indigo in Blue"),
    ("Game/Azur Lane (アズールレーン) ~", "Sail Away Justice hi-res", "Sail Away Justice"),
    # Vtuber
    ("Vtuber/Azuma Seren (東雪蓮) ~", "Love-in-a-Mist [AZSE-0001, CD-FLAC]", "Love-in-a-Mist {AZSE-0001}"),
    ("Vtuber/Other ~/Princess Letter(s)! フロムアイドル ~", "Princess Letter(s)! Hajimete Tayori☆  Tayori (CV. Yu Serizawa) hi-res", "Princess Letter(s)! Hajimete Tayori☆  Tayori (CV. Yu Serizawa)"),
    ("Vtuber/Other ~/Princess Letter(s)! フロムアイドル ~", "Princess Letter(s)! From Idol TAIYAKI IDOL TAYORIN SANJOU! [feat. Hige Driver] HI-RES", "Princess Letter(s)! From Idol TAIYAKI IDOL TAYORIN SANJOU! [feat. Hige Driver]"),
    ("Vtuber/Other ~/Princess Letter(s)! フロムアイドル ~", "Princess Letter(s)! From Idol Sprout (feat. KOTONOHOUSE) HI-RES", "Princess Letter(s)! From Idol Sprout (feat. KOTONOHOUSE)"),
    ("Vtuber/Other ~/Princess Letter(s)! フロムアイドル ~", "Princess Letter(s)! From Idol Kotohana Letter(s)! hi-res", "Princess Letter(s)! From Idol Kotohana Letter(s)!"),
    ("Vtuber/Other ~/Princess Letter(s)! フロムアイドル ~", "Princess Letter(s)! From Idol Mienai Tsubasa (feat. bassy) HI-RES", "Princess Letter(s)! From Idol Mienai Tsubasa (feat. bassy)"),
    ("Vtuber/Other ~/Princess Letter(s)! フロムアイドル ~", "Princess Letter(s)! Floating Flower(s)! hi-res", "Princess Letter(s)! Floating Flower(s)!"),
    ("Vtuber/Other ~/GEMS COMPANY ~", "Cheery TA♡CHIA Girl ／ Imposing Dance, Gorgeous Girl hi-res", "Cheery TA♡CHIA Girl ／ Imposing Dance, Gorgeous Girl"),
    ("Vtuber/YuNi ~", "YuNi – eternal jorney (1st Album) HI-RES", "eternal jorney (1st Album)"),
    # J-Pop
    ("J-Pop/Mone Kamishiraishi (上白石萌音) ~", "name (Album) HI-RES", "name (Album)"),
    ("J-Pop/NOMELON NOLEMON ~", "Kankakuha flac", "Kankakuha"),
    ("J-Pop/NOMELON NOLEMON ~", "Rule flac", "Rule"),
    ("J-Pop/NOMELON NOLEMON ~", "POP flac", "POP"),
    # Doujinshi
    ("Doujinshi/Vivid Lila ~", "WEB FLAC", "Air of Celeste"),
    ("Doujinshi/Hanatan (花たん) ~", "柊 FLAC", "柊"),
    ("Doujinshi/Hanatan (花たん) ~", "Story has ended FLAC", "Story has ended"),
    ("Doujinshi/Hanatan (花たん) ~", "Summer☆Syrup FLAC", "Summer☆Syrup"),
    ("Doujinshi/Hanatan (花たん) ~", "花ノ宴 FLAC", "花ノ宴")
]

print("\n--- Renaming Format Noise Folders ---")
for parent_rel, old_name, new_name in renames:
    parent_p = os.path.join(ROOT, parent_rel)
    old_p = os.path.join(parent_p, old_name)
    new_p = os.path.join(parent_p, new_name)
    if os.path.exists(old_p):
        print(f"Renaming: '{old_name}' -> '{new_name}'")
        os.rename(old_p, new_p)

print("\n==================================================================")
print("=== MASTER REFINEMENT COMPLETED ===")
print("==================================================================")
