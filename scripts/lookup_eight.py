import urllib.request
import json

url = 'https://musicbrainz.org/ws/2/release/?query=release:Eight%20AND%20artist:%E5%85%AB%E7%8E%8B%E5%AD%90P&fmt=json'
req = urllib.request.Request(url, headers={'User-Agent': 'HomelabMusicAuditor/1.0 (samsmon)'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for r in data.get('releases', []):
            print(r.get('id'), "|", r.get('title'), "|", r.get('date'), "|", r.get('country'))
            # Check CAA
            caa_url = f"https://coverartarchive.org/release/{r.get('id')}"
            caa_req = urllib.request.Request(caa_url, headers={'User-Agent': 'HomelabMusicAuditor/1.0 (samsmon)'})
            try:
                with urllib.request.urlopen(caa_req) as caa_resp:
                    caa_data = json.loads(caa_resp.read().decode('utf-8'))
                    print("  CAA Front:", caa_data.get('images', [{}])[0].get('image'))
            except Exception as e:
                print("  CAA Error:", e)
except Exception as e:
    print("MB Error:", e)
