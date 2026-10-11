#!/usr/bin/env python3
import json

transcript_path = r'C:\Users\Sam\.gemini\antigravity\brain\423a7e7c-328c-4da5-b6e6-81eca21f020c\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if '"type":"USER_INPUT"' in line:
            obj = json.loads(line)
            content = obj.get('content', '')
            print(f"=== STEP {obj.get('step_index')} ===")
            print(content[:500])
            print("...\n")
