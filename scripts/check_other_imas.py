import os

base = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~"

print(f"=== CHECKING OTHER IMAS FRANCHISES ===")
for sub in sorted(os.listdir(base)):
    if sub.startswith("Gakuen") or sub.startswith("Shiny"):
        continue
    sp = os.path.join(base, sub)
    if os.path.isdir(sp):
        print(f"\n--- FRANCHISE: {sub} ---")
        for r, d, f in os.walk(sp):
            rel = os.path.relpath(r, sp)
            audio = [x for x in f if x.endswith(('.flac', '.wav', '.wv', '.m4a'))]
            # check empty leaves
            if not d and not audio:
                print(f"  [EMPTY LEAF] {rel} (files: {f})")
            # check alt or dup
            for x in f:
                if "_alt" in x.lower() or "_dup" in x.lower():
                    print(f"  [ALT/DUP] {os.path.join(rel, x)}")
            # check format noise
            for x in d:
                if any(t in x.lower() for t in ['cd-flac', 'web-flac', 'hi-res', '32bit', '24bit']):
                    print(f"  [FORMAT TAG] {os.path.join(rel, x)}")
