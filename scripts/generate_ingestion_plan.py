import os
import json

LOSSLESS_ROOT = "/mnt/hdd-backup/music/Lossless"
TORRENT_DONE = "/mnt/hdd-backup/music/Torrent/done"

with open('/tmp/truly_new_by_category.json', 'r', encoding='utf-8') as f:
    cats = json.load(f)

# Mapping functions
def map_gakumas(folder_name):
    # Characters map
    chars = [
        ("花海咲季", "01. 花海咲季 (Saki Hanami)"),
        ("月村手毬", "02. 月村手毬 (Temari Tsukimura)"),
        ("藤田ことね", "03. 藤田ことね (Kotone Fujita)"),
        ("有村麻央", "04. 有村麻央 (Mao Arimura)"),
        ("葛城リーリヤ", "05. 葛城リーリヤ (Lilja Katsuragi)"),
        ("倉本千奈", "06. 倉本千奈 (China Kuramoto)"),
        ("紫雲清夏", "07. 紫雲清夏 (Sumika Shiun)"),
        ("篠澤広", "08. 篠澤広 (Hiro Shinosawa)"),
        ("姫崎莉波", "09. 姫崎莉波 (Rinami Himesaki)"),
        ("花海佑芽", "10. 花海佑芽 (Ume Hanami)"),
        ("秦谷美鈴", "11. 秦谷美鈴 (Misuzu Hataya)"),
        ("十王星南", "12. 十王星南 (Sena Juo)"),
        ("雨夜燕", "13. 雨夜燕 (Tsubame Amaya)")
    ]
    base = os.path.join(LOSSLESS_ROOT, "Anime", "THE IDOLM@STER ~", "学園アイドルマスター")
    
    # Duo
    if "葛城リーリヤ&紫雲清夏" in folder_name or "有村麻央&姫崎莉波" in folder_name:
        return os.path.join(base, "02. Duo")
    
    # All Stars & Units
    if any(k in folder_name for k in ["初星学園", "わかし・さわがし・スカパンク", "修楽旅行", "ねえ、言っちゃうよ。"]):
        return os.path.join(base, "04. All Stars & Units")
    
    # Solo characters
    for c_jp, c_folder in chars:
        if c_jp in folder_name:
            return os.path.join(base, "01. Solo", c_folder)
            
    return os.path.join(base, "04. All Stars & Units")

def map_shiny(folder_name):
    base = os.path.join(LOSSLESS_ROOT, "Anime", "THE IDOLM@STER ~", "シャイニーカラーズ")
    if "無自覚アプリオリ" in folder_name:
        return os.path.join(base, "01. WING & Main Game Series", "06. CANVAS (2023)")
    elif "ECHOES" in folder_name:
        return os.path.join(base, "01. WING & Main Game Series", "07. ECHOES (2024)")
    elif "HOPEFUL FE@THERS" in folder_name:
        return os.path.join(base, "04. COLORFUL FE@THERS Series")
    return os.path.join(base, "05. Synthe-Side & Collaborations")

def map_album(cat, a):
    if cat == 'gakumas':
        return map_gakumas(a)
    elif cat == 'shiny':
        return map_shiny(a)
    elif cat == 'lovelive':
        return os.path.join(LOSSLESS_ROOT, "Anime", "Love Live ~")
    elif cat == 'bangdream':
        return os.path.join(LOSSLESS_ROOT, "Anime", "BanG Dream! ~")
    elif cat == 'd4dj':
        return os.path.join(LOSSLESS_ROOT, "Anime", "D4DJ ~")
    elif cat == 'idoly':
        return os.path.join(LOSSLESS_ROOT, "Anime", "IDOLY PRIDE ~")
    elif cat == 'jpop':
        return os.path.join(LOSSLESS_ROOT, "J-Pop", "Milet ~")
    elif cat == 'other_anime':
        if 'Tokyo 7th' in a:
            return os.path.join(LOSSLESS_ROOT, "Anime", "Tokyo 7th シスターズ ~")
        elif 'ポールプリンセス' in a:
            return os.path.join(LOSSLESS_ROOT, "Anime", "ポールプリンセス!! ~")
    elif cat == 'vtuber':
        if 'すいせい' in a:
            return os.path.join(LOSSLESS_ROOT, "Vtuber", "星街すいせい (Suisex) ~")
        elif '鷹嶺ルイ' in a:
            return os.path.join(LOSSLESS_ROOT, "Vtuber", "鷹嶺ルイ (Takane Lui) ~")
        elif 'トワ' in a:
            return os.path.join(LOSSLESS_ROOT, "Vtuber", "常闇トワ (Towa Tokoyami) ~")
        elif '桃鈴ねね' in a:
            return os.path.join(LOSSLESS_ROOT, "Vtuber", "桃鈴ねね (Nene Momosuzu) ~")
        elif 'さくらみこ' in a:
            return os.path.join(LOSSLESS_ROOT, "Vtuber", "さくらみこ (Sakura Miko) ~")
        elif 'miComet' in a:
            return os.path.join(LOSSLESS_ROOT, "Vtuber", "miComet ~")
        elif 'Midnight Grand Orchestra' in a:
            return os.path.join(LOSSLESS_ROOT, "Vtuber", "Midnight Grand Orchestra ~")
    return "UNKNOWN"

mapping_result = []
for c, albums in cats.items():
    for a in albums:
        target_dir = map_album(c, a)
        mapping_result.append({
            "source": a,
            "category": c,
            "target_dir": target_dir
        })

print(f"Total mapped: {len(mapping_result)}")
unknowns = [m for m in mapping_result if m['target_dir'] == "UNKNOWN"]
print(f"Unknowns: {len(unknowns)}")

with open('/tmp/ingestion_plan_142.json', 'w', encoding='utf-8') as f:
    json.dump(mapping_result, f, ensure_ascii=False, indent=2)

print("\n--- SAMPLE MAPPINGS ---")
for m in mapping_result[::10]:
    print(f"{m['source']}\n  --> {m['target_dir']}\n")
