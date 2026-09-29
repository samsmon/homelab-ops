import os
import subprocess
import unicodedata

gakumas = "/mnt/hdd-backup/music/Lossless/Anime/THE IDOLM@STER (アイドルマスター) ~/Gakuen Idolmaster (学園アイドルマスター) ~"

print("=================================================================")
print("=== COMPREHENSIVE GAKUMAS AUDIT ===")
print("=================================================================")

for category in sorted(os.listdir(gakumas)):
    cat_path = os.path.join(gakumas, category)
    if not os.path.isdir(cat_path):
        continue
    print(f"\n>>> CATEGORY: {category} <<<")
    for entity in sorted(os.listdir(cat_path)):
        ent_path = os.path.join(cat_path, entity)
        if not os.path.isdir(ent_path):
            print(f"  [STRAY FILE] {entity}")
            continue
        
        # Entity can be an idol (01. Solo/01. 花海咲季) or directly an album (in Duo/Trio/Units)
        items = sorted(os.listdir(ent_path))
        subdirs = [i for i in items if os.path.isdir(os.path.join(ent_path, i))]
        files = [i for i in items if not os.path.isdir(os.path.join(ent_path, i))]
        
        if subdirs:
            print(f"\n  [ENTITY CONTAINER] {entity} ({len(subdirs)} albums):")
            for alb in subdirs:
                alb_p = os.path.join(ent_path, alb)
                alb_files = os.listdir(alb_p)
                audio = [f for f in alb_files if f.endswith(('.flac', '.wav', '.wv', '.m4a'))]
                inner = [f for f in alb_files if os.path.isdir(os.path.join(alb_p, f))]
                
                # Check issues
                issues = []
                if any(tag in alb for tag in ['[CD-FLAC]', '[FLAC]', '[GOLD RUSH', '[1st Single']):
                    issues.append("TAG_NOISE")
                if "_alt" in " ".join(alb_files):
                    issues.append("ALT_FILES")
                if unicodedata.normalize('NFC', alb) != alb:
                    issues.append("NFD_UNICODE")
                if len(audio) == 0:
                    issues.append("NO_AUDIO")
                
                status = f" -> ISSUES: {', '.join(issues)}" if issues else ""
                print(f"    - {alb} ({len(audio)} audio, inner: {inner}){status}")
                if "ALT_FILES" in issues:
                    for af in alb_files:
                        if "_alt" in af:
                            print(f"        ALT: {af}")
        else:
            # ent_path is directly an album
            audio = [f for f in files if f.endswith(('.flac', '.wav', '.wv', '.m4a'))]
            issues = []
            if any(tag in entity for tag in ['[CD-FLAC]', '[FLAC]', '[GOLD RUSH', '[1st Single']):
                issues.append("TAG_NOISE")
            if "_alt" in " ".join(files):
                issues.append("ALT_FILES")
            if unicodedata.normalize('NFC', entity) != entity:
                issues.append("NFD_UNICODE")
            if len(audio) == 0:
                issues.append("NO_AUDIO")
            status = f" -> ISSUES: {', '.join(issues)}" if issues else ""
            print(f"  [DIRECT ALBUM] {entity} ({len(audio)} audio){status}")
