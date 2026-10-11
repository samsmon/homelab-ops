import os

cues_to_inspect = [
    "/mnt/hdd-backup/music/Lossless/Doujinshi/Mamyukka ~/テアトルエトワール/テアトルエトワール.cue",
    "/mnt/hdd-backup/music/Lossless/Doujinshi/Mamyukka ~/THE 13th PANCER/THE 13th PANCER.cue",
    "/mnt/hdd-backup/music/Lossless/Doujinshi/Shinra-bansho (森羅万象) ~/toge/toge.cue",
    "/mnt/hdd-backup/music/Lossless/Vtuber/Azuma Seren (東雪蓮) ~/KEEP OUT {AZSE-0009}/KEEP OUT.cue",
    "/mnt/hdd-backup/music/Lossless/J-Pop/TUYU (ツユ) ~/「アンダーキッズ」ピアノアレンジCD/DSP-02365.cue"
]

for cp in cues_to_inspect:
    print(f"=== {cp} ===")
    if os.path.exists(cp):
        try:
            with open(cp, 'rb') as f:
                content = f.read().decode('utf-8', errors='replace')
            print(content[:500])
        except Exception as e:
            print(f"Error reading: {e}")
    else:
        print("File does not exist")

protocollon_dir = "/mnt/hdd-backup/music/Lossless/Doujinshi/PROTOCOLLON ~/J-HYPER NATION {PRT-003}"
print(f"\n=== PROTOCOLLON: {protocollon_dir} ===")
if os.path.exists(protocollon_dir):
    for f in sorted(os.listdir(protocollon_dir)):
        fp = os.path.join(protocollon_dir, f)
        print(f"  {f} ({os.path.getsize(fp)} bytes)")
