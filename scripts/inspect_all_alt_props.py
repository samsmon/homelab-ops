import os
import subprocess

ROOT = "/mnt/hdd-backup/music/Lossless"

def get_prop(p):
    try:
        out = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', p], universal_newlines=True).strip().split()
        return f"{out[0]}Hz/{out[1]}bit, {os.path.getsize(p)} bytes"
    except Exception as e:
        return f"err: {e}"

targets = [
    "Anime/BanG Dream! (バンドリ！) ~/MyGO!!!!! ~/BanG Dream! MyGO!!!!! 3rdアルバム「致並跡」",
    "Anime/BanG Dream! (バンドリ！) ~/Mugendai Mewtype (夢限大みゅーたいぷ) ~/BanG Dream! 夢限大みゅーたいぷ 4thシングル「超惑星Xへの旅」",
    "Anime/Utahime Dream (ウタヒメドリーム) ~/AMBITION",
    "Anime/Utahime Dream (ウタヒメドリーム) ~/TVアニメ「無自覚聖女は今日も無意識に力を垂れ流す」EDテーマ「アンノウンミー」／ウタヒメドリーム オールスターズ",
    "Anime/THE IDOLM@STER (アイドルマスター) ~/Shiny Colors (シャイニーカラーズ) ~/03. Anime Series/TVアニメ「アイドルマスター シャイニーカラーズ 2nd Season」主題歌アルバム「Over the prism」/Disc 1",
    "Anime/Love Live! (ラブライブ！) ~/Liella! (ラブライブ！スーパースター!!) ~/ラブライブ！スーパースター!! Liella!と結ぶプロジェクト ミニアルバム「Hyper Glowing!」",
    "J-Pop/Hanabie. (花冷え。) ~/TVアニメ「対ありでした。 ～お嬢さまは格闘ゲームなんてしない～」OPテーマ「命短し対する乙女よ」／花冷え。",
    "J-Pop/PassCode ~/Liberator",
    "J-Pop/TUYU (ツユ) ~/アンダーメンタリティ",
    "J-Pop/Kaya (花耶) ~/TVアニメ「ヘルモード ～やり込み好きのゲーマーは廃設定の異世界で無双する～」EDテーマ「Sanctuary」／花耶",
    "J-Pop/Various Artists ~/雪花繚乱",
    "J-Pop/Yuki Tanaka (田中有紀) ~/I need",
    "J-Pop/Maejima Ami (前島亜美) ~/Determination/前島亜美 1stアルバム「Determination」",
    "J-Pop/Riria . (りりあ。) ~/軌跡"
]

for t in targets:
    p = os.path.join(ROOT, t)
    print(f"\n=== {t} ===")
    if not os.path.exists(p):
        print("  DIR NOT FOUND")
        continue
    files = sorted(os.listdir(p))
    for f in files:
        if "_alt" in f or "_dup" in f:
            base_f = f.replace("_alt.flac", ".flac").replace("_dup.flac", ".flac").replace("_dup.jpg", ".jpg")
            fp_alt = os.path.join(p, f)
            fp_base = os.path.join(p, base_f)
            if f.endswith('.flac'):
                prop_alt = get_prop(fp_alt)
                prop_base = get_prop(fp_base) if os.path.exists(fp_base) else "BASE MISSING"
                print(f"  {f} ({prop_alt})\n    vs base {base_f} ({prop_base})")
            else:
                sz_alt = os.path.getsize(fp_alt)
                sz_base = os.path.getsize(fp_base) if os.path.exists(fp_base) else 0
                print(f"  {f} ({sz_alt} B) vs {base_f} ({sz_base} B)")
