import os
import shutil

ROOT = "/mnt/hdd-backup/music/Lossless"

print("=== FINISHING MASTER REFINEMENT ===")

# 1. Remove duplicate Light Years HI-RES
hbr = os.path.join(ROOT, "Game/Heaven Burns Red (ヘブンバーンズレッド) ~")
ly_dup = os.path.join(hbr, "Light Years HI-RES")
if os.path.exists(ly_dup):
    shutil.rmtree(ly_dup)
    print("Removed duplicate Light Years HI-RES.")

renames = [
    # Game
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

for parent_rel, old_name, new_name in renames:
    parent_p = os.path.join(ROOT, parent_rel)
    old_p = os.path.join(parent_p, old_name)
    new_p = os.path.join(parent_p, new_name)
    if os.path.exists(old_p):
        if os.path.exists(new_p):
            print(f"Target '{new_name}' already exists! Merging '{old_name}' into it...")
            for f in os.listdir(old_p):
                src_f = os.path.join(old_p, f)
                dst_f = os.path.join(new_p, f)
                if not os.path.exists(dst_f):
                    shutil.move(src_f, dst_f)
                else:
                    if os.path.getsize(src_f) > os.path.getsize(dst_f):
                        os.remove(dst_f)
                        shutil.move(src_f, dst_f)
                    else:
                        os.remove(src_f)
            os.rmdir(old_p)
        else:
            print(f"Renaming: '{old_name}' -> '{new_name}'")
            os.rename(old_p, new_p)

print("\nFinished finish_master_refinement.py successfully.")
