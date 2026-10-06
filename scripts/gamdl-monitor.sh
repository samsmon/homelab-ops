#!/usr/bin/env bash
# gamdl-dashboard server-side monitor (media-hosts). Run every 5 min by gamdl-monitor.timer.
# Report-only: never changes the service. Writes a status line per run and de-duplicated ALERT lines.
#   /var/log/gamdl-monitor.log         one status line per run (trimmed to 2000 lines)
#   /var/log/gamdl-monitor-alerts.log  alerts only (a kind is re-alerted every 6h while it persists)
set -u
API=http://localhost:8110
DB=/opt/gamdl-dashboard/data/dashboard.sqlite
LOG=/var/log/gamdl-monitor.log
ALERTS=/var/log/gamdl-monitor-alerts.log
STATE=/var/lib/gamdl-monitor.state
mkdir -p "$(dirname "$STATE")"

python3 - "$API" "$DB" "$LOG" "$ALERTS" "$STATE" <<'PY'
import json, sqlite3, subprocess, sys, time, urllib.request
api, db, log, alerts, statef = sys.argv[1:6]
now = time.time()
stamp = lambda t=None: time.strftime("%F %T %z", time.localtime(t or now))
found = {}  # kind -> message

svc = subprocess.run(["systemctl", "is-active", "gamdl-dashboard"], capture_output=True, text=True).stdout.strip()
st = None
try:
    st = json.load(urllib.request.urlopen(api + "/api/state", timeout=8))
except Exception as e:
    found["API_DOWN"] = f"service={svc}, /api/state failed: {e}"
if svc != "active":
    found["SERVICE_DOWN"] = f"systemctl is-active = {svc}"

try:
    prev = json.load(open(statef))
except Exception:
    prev = {}
line = f"{stamp()} svc={svc}"
if st:
    items = st["items"]
    c = {}
    for i in items:
        c[i["status"]] = c.get(i["status"], 0) + 1
    paused, banner, cap = st["paused"], st.get("banner"), st["cap"]
    last = 0
    try:
        d = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        last = d.execute("select coalesce(max(ts),0) from log").fetchone()[0]
    except Exception as e:
        found["DB_READ"] = str(e)
    idle_min = int((now - last) / 60) if last else -1
    line += f" paused={paused} banner={(banner or {}).get('kind')} cap={cap['used']}/{cap['limit']} items={c} last_log_min_ago={idle_min}"
    running = c.get("running", 0) + c.get("downloading", 0)
    queued = c.get("queued", 0)
    kind = (banner or {}).get("kind")
    # pause since when (for stale-pause detection)
    since = prev.get("paused_since") if paused else None
    if paused and not since:
        since = now
    if kind == "cap_reached" and paused and cap["used"] < cap["limit"] and since and now - since > 600:
        found["STALE_CAP_PAUSE"] = (f"paused with cap_reached but only {cap['used']}/{cap['limit']} used; "
                                   "auto-resume did not fire (paused >10 min with free slots)")
    elif paused and queued and since and now - since > 3600 and kind != "cap_reached":
        found["PAUSED_LONG"] = f"paused >1h, banner={kind}, queued={queued}"
    if kind and kind != "cap_reached":
        found["BANNER_" + kind.upper()] = (banner or {}).get("reason", "")
    if not paused and queued and not running and last and now - last > 1800:
        found["STALLED"] = f"not paused, {queued} queued, nothing running, no log activity for {idle_min} min"
    errs = st.get("errors", 0)
    if errs > prev.get("errors", errs):
        found["ERRORS_UP"] = f"error count {prev.get('errors')} -> {errs}"
    new_prev = {"paused_since": since, "errors": errs}
else:
    new_prev = {"paused_since": prev.get("paused_since"), "errors": prev.get("errors", 0)}
    line += " api=DOWN"

last_alert = prev.get("alerts", {})
out_alerts = {}
with open(alerts, "a") as f:
    for k, msg in found.items():
        t = last_alert.get(k, 0)
        if now - t > 6 * 3600:
            f.write(f"{stamp()} ALERT {k}: {msg}\n")
            t = now
        out_alerts[k] = t
new_prev["alerts"] = out_alerts
json.dump(new_prev, open(statef, "w"))
line += " ALERTS=" + ",".join(found) if found else " ok"
with open(log, "a") as f:
    f.write(line + "\n")
try:
    L = open(log).read().splitlines()
    if len(L) > 2000:
        open(log, "w").write("\n".join(L[-2000:]) + "\n")
except Exception:
    pass
PY
