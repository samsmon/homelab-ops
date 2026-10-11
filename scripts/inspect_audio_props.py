import os
import subprocess

def inspect_flac(p):
    try:
        out = subprocess.check_output(['metaflac', '--show-sample-rate', '--show-bps', '--show-total-samples', p], universal_newlines=True)
        return out.strip().split('\n')
    except Exception as e:
        return [str(e)]

toge_dir = "/mnt/hdd-backup/music/Lossless/Doujinshi/Shinra-bansho (森羅万象) ~/toge"
print(f"=== TOGE DIR: {toge_dir} ===")
for f in os.listdir(toge_dir):
    print(" ", f)

proto_dir = "/mnt/hdd-backup/music/Lossless/Doujinshi/PROTOCOLLON ~/J-HYPER NATION {PRT-003}"
print(f"\n=== PROTOCOLLON FLAC PROPERTIES ===")
for f in sorted(os.listdir(proto_dir)):
    if f.endswith('.flac'):
        fp = os.path.join(proto_dir, f)
        props = inspect_flac(fp)
        sz = os.path.getsize(fp)
        print(f"  {f} ({sz} bytes): {props}")
