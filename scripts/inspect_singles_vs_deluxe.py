import os

pairs = [
    ("/mnt/hdd-backup/music/Lossless/J-Pop/Nishino Kana Feat. Niziu (西野カナ feat. NiziU) ~", "LOVE BEAT (Single Edition)", "LOVE BEAT (Full Release)"),
    ("/mnt/hdd-backup/music/Lossless/J-Pop/Nogizaka46 (乃木坂46) ~", "是非に及ばず", "是非に及ばず (Special Edition)"),
    ("/mnt/hdd-backup/music/Lossless/J-Pop/H／／PE Princess ~", "17.7", "17.7 (Japan Deluxe Edition)")
]

for parent, d1, d2 in pairs:
    p1 = os.path.join(parent, d1)
    p2 = os.path.join(parent, d2)
    print(f"=== {parent} ===")
    print(f"  {d1}: {os.listdir(p1) if os.path.exists(p1) else 'NOT FOUND'}")
    print(f"  {d2}: {os.listdir(p2) if os.path.exists(p2) else 'NOT FOUND'}")
